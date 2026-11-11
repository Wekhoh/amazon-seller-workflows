#!/usr/bin/env python3
"""Read-only helpers for offline Amazon Ads workbook inspection."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple
from xml.etree.ElementTree import ParseError
from zipfile import BadZipFile

from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException

INPUT_ERRORS = (OSError, ValueError, KeyError, BadZipFile, InvalidFileException, ParseError)
SP_SHEET = "Sponsored Products Campaigns"
PLACEMENT_TOS = "Placement Top"
PLACEMENT_ROS = "Placement Rest Of Search"
PLACEMENT_PP = "Placement Product Page"
PLACEMENT_AB = "Placement Amazon Business"
DEFAULT_PLACEMENTS = [PLACEMENT_TOS, PLACEMENT_ROS, PLACEMENT_PP]

ERROR_REPORT_COLUMNS = ["Original Sheet", "Original record #", "Error type", "Error code", "Error message"]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def json_default(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return str(value)

def print_json(payload: Mapping[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=json_default))

def normalize_date(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, int):
        return str(value)
    text = str(value).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return text.replace("-", "")
    return text

def read_sheet(path: Path, sheet: str = SP_SHEET) -> Tuple[List[str], List[Dict[str, Any]]]:
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        if sheet not in wb.sheetnames:
            raise ValueError(f"Sheet not found: {sheet}")
        ws = wb[sheet]
        ws.reset_dimensions()
        rows_iter = ws.iter_rows(values_only=True)
        header_row = next(rows_iter, None)
        if not header_row or all(value in (None, "") for value in header_row):
            raise ValueError(f"Sheet header is empty: {sheet}")
        headers = [str(value) if value is not None else "" for value in header_row]
        duplicates = [name for name, count in Counter(headers).items() if name and count > 1]
        if duplicates:
            raise ValueError(f"Duplicate column headers in {sheet}: {duplicates}")
        rows = []
        for row_number, values in enumerate(rows_iter, 2):
            if all(value in (None, "") for value in values):
                continue
            if any(value not in (None, "") for value in values[len(headers):]):
                raise ValueError(f"Row {row_number} has data without a column header")
            if any(not name and index < len(values) and values[index] not in (None, "")
                   for index, name in enumerate(headers)):
                raise ValueError(f"Row {row_number} has data under a blank column header")
            row = {name: values[index] if index < len(values) else None
                   for index, name in enumerate(headers) if name}
            row["_row_number"] = row_number
            rows.append(row)
        if not rows:
            raise ValueError(f"No data rows in sheet: {sheet}")
        return headers, rows
    finally:
        wb.close()

def workbook_sheet_summary(path: Path) -> List[Dict[str, Any]]:
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        summaries = []
        for ws in wb.worksheets:
            ws.reset_dimensions()
            dimension = ws.calculate_dimension(force=True)
            rows_iter = ws.iter_rows(values_only=True)
            header = next(rows_iter, None) or ()
            data_rows = sum(any(value not in (None, "") for value in row) for row in rows_iter)
            summaries.append({
                "sheet": ws.title,
                "dimension": dimension,
                "data_rows": data_rows,
                "first_three_headers": list(header[:3]),
            })
        return summaries
    finally:
        wb.close()

def require_columns(headers: Sequence[str], columns: Sequence[str]) -> None:
    missing = [c for c in columns if c not in headers]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def row_name(row: Mapping[str, Any]) -> str:
    return str(row.get("Campaign Name") or row.get("Campaign Name (Informational only)") or "")



def campaign_rows(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Mapping[str, Any]]:
    result = {}
    for row in rows:
        if not row.get("Entity"):
            raise ValueError(f"Missing Entity at row {row.get('_row_number')}")
        if row.get("Entity") != "Campaign":
            continue
        if row.get("Campaign ID") in (None, ""):
            raise ValueError(f"Missing Campaign ID at row {row.get('_row_number')}")
        cid = str(row["Campaign ID"])
        if cid in result:
            raise ValueError(f"Ambiguous duplicate Campaign ID: {cid}")
        require_state(row.get("State"), f"campaign {cid}")
        result[cid] = row
    return result

def target_enabled_campaigns_by_product(
    rows: Sequence[Mapping[str, Any]], asin: str | None = None, sku: str | None = None
) -> Dict[str, Mapping[str, Any]]:
    campaigns = campaign_rows(rows)
    target = {}
    for row in rows:
        if row.get("Entity") != "Product Ad":
            continue
        for column, selected_value in (("ASIN (Informational only)", asin), ("SKU", sku)):
            value = row.get(column)
            if selected_value is not None and (value is None or str(value).strip() == ""):
                raise ValueError(f"Missing {column} at Product Ad row {row.get('_row_number')}")
        cid = str(row.get("Campaign ID"))
        campaign = campaigns.get(cid)
        if campaign is None:
            raise ValueError(f"Product Ad row {row.get('_row_number')} has no Campaign row")
        if not product_matches(row, asin, sku):
            continue
        states = [
            require_state(row.get("State"), f"Product Ad row {row.get('_row_number')}"),
            require_state(row.get("Campaign State (Informational only)"), "product campaign state"),
            require_state(row.get("Ad Group State (Informational only)"), "product ad group state"),
            require_state(campaign.get("State"), f"campaign {cid}"),
        ]
        if states[1] != states[3]:
            raise ValueError(f"Conflicting campaign states for Campaign ID: {cid}")
        if all(state == "enabled" for state in states):
            target[cid] = campaign
    return target

def bidding_adjustment_map(rows: Sequence[Mapping[str, Any]]) -> Dict[Tuple[str, str], Mapping[str, Any]]:
    campaigns = {str(row.get("Campaign ID")) for row in rows if row.get("Entity") == "Campaign"}
    result = {}
    for row in rows:
        if row.get("Entity") != "Bidding Adjustment":
            continue
        cid = str(row.get("Campaign ID"))
        if cid not in campaigns:
            raise ValueError(f"Bidding Adjustment row {row.get('_row_number')} has no Campaign row")
        placement = row.get("Placement")
        if placement in (None, ""):
            raise ValueError(f"Missing Placement at row {row.get('_row_number')}")
        key = (cid, str(placement))
        if key in result:
            raise ValueError(f"Ambiguous duplicate placement for campaign {cid}: {placement}")
        result[key] = row
    return result

def counter_to_dict(counter: Counter) -> Dict[str, int]:
    return {str(k): int(v) for k, v in counter.items()}


def require_state(value: Any, location: str) -> str:
    state = str(value).strip().lower()
    if state not in {"enabled", "paused", "archived"}:
        raise ValueError(f"Missing or unsupported state at {location}: {value!r}")
    return state


def product_matches(row: Mapping[str, Any], asin: str | None, sku: str | None) -> bool:
    for column, selected_value in (("ASIN (Informational only)", asin), ("SKU", sku)):
        if selected_value is not None and not isinstance(row.get(column), str):
            raise ValueError(
                f"Non-text {column} at Product Ad row {row.get('_row_number')}. "
                f"Re-export the {column} column as text from the original source; "
                "numeric cells may have lost leading zeros or precision."
            )
    return ((asin is None or row.get("ASIN (Informational only)") == asin)
            and (sku is None or row.get("SKU") == sku))
