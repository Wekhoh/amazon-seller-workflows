#!/usr/bin/env python3
"""Generate fictional local workbooks for the offline advertising readers."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

BULK_HEADERS = [
    "Entity", "Campaign ID", "Campaign Name", "Start Date", "State",
    "SKU", "ASIN (Informational only)", "Campaign State (Informational only)",
    "Ad Group State (Informational only)", "Placement", "Percentage",
    "Daily Budget", "Bidding Strategy", "Operation",
]
REPORT_HEADERS = ["Original Sheet", "Original record #", "Error type", "Error code", "Error message"]


def write_example(path: Path, sheets: dict[str, list[list]]) -> None:
    wb = Workbook()
    wb.remove(wb.active)
    wb.properties.creator = "Synthetic examples"
    wb.properties.description = "Fictional demonstration data; not an upload file or business evidence."
    try:
        for name, rows in sheets.items():
            ws = wb.create_sheet(name)
            for row in rows:
                ws.append(row)
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for cell in ws[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="305F72")
            for index, values in enumerate(zip(*rows), 1):
                width = max(len(str(value)) if value is not None else 0 for value in values)
                ws.column_dimensions[get_column_letter(index)].width = min(max(width + 2, 12), 60)
        wb.save(path)
    finally:
        wb.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    bulk = args.output_dir / "synthetic_bulk.xlsx"
    report = args.output_dir / "synthetic_report_invalid_headers.xlsx"
    existing = [path.name for path in (bulk, report) if path.exists()]
    if existing:
        parser.error(f"Refusing to overwrite existing example files: {existing}")

    def campaign(cid, name, state="enabled"):
        return {"Entity": "Campaign", "Campaign ID": cid, "Campaign Name": name,
                "Start Date": "20260101", "State": state, "Daily Budget": 12,
                "Bidding Strategy": "Dynamic bids - down only"}

    def product(cid, asin, sku, campaign_state="enabled"):
        return {"Entity": "Product Ad", "Campaign ID": cid, "State": "enabled",
                "SKU": sku, "ASIN (Informational only)": asin,
                "Campaign State (Informational only)": campaign_state,
                "Ad Group State (Informational only)": "enabled"}

    rows = [
        campaign("1001", "Demo Aurora Mugs"),
        product("1001", "B0EXAMPLE01", "EXAMPLE-SKU"),
        product("1001", "B0SYNTH003", "DEMO-MUG-RED"),
        {"Entity": "Bidding Adjustment", "Campaign ID": "1001",
         "Placement": "Placement Top", "Percentage": 0},
        {"Entity": "Bidding Adjustment", "Campaign ID": "1001",
         "Placement": "Placement Rest Of Search", "Percentage": None},
        campaign("1002", "Demo Harbor Notebooks"),
        product("1002", "B0SYNTH002", "DEMO-NOTEBOOK-GREEN"),
        {"Entity": "Bidding Adjustment", "Campaign ID": "1002",
         "Placement": "Placement Top", "Percentage": 25},
        campaign("1003", "Demo Aurora Paused", "paused"),
        product("1003", "B0EXAMPLE01", "EXAMPLE-SKU", "paused"),
    ]
    bulk_sheets = {"Sponsored Products Campaigns": [
        BULK_HEADERS, *[[row.get(header) for header in BULK_HEADERS] for row in rows],
    ]}
    report_sheets = {
        "Campaign errors": [
            REPORT_HEADERS,
            ["Sponsored Products Campaigns", 1, "Input Error", "Invalid header",
             "The fictional upload contains an unrecognized header: Demo campaign column."],
            ["Sponsored Products Campaigns", 2, "Warning", "Not Processed",
             "This fictional record was not processed after the header error."],
        ],
        "Product errors": [
            REPORT_HEADERS,
            ["Sponsored Products Campaigns", 1, "Input Error", "Invalid header",
             "The fictional upload contains an unrecognized header: Demo product column."],
        ],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_example(bulk, bulk_sheets)
    write_example(report, report_sheets)
    print(json.dumps({"synthetic_files": [str(bulk), str(report)]}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except OSError as exc:
        raise SystemExit(f"Cannot create synthetic examples: {exc}")
