#!/usr/bin/env python3
"""Explain supplied Amazon Ads processing-report workbooks without changing them."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from openpyxl import load_workbook

from amazon_ads_bulk_core import ERROR_REPORT_COLUMNS, INPUT_ERRORS, counter_to_dict, print_json, sha256_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()

    findings = []
    schema_issues = []
    recognized_sheets = []
    empty_sheets = []
    wb = load_workbook(args.report, read_only=True, data_only=True)
    try:
        for ws in wb.worksheets:
            ws.reset_dimensions()
            rows = ws.iter_rows(values_only=True)
            header = next(rows, None)
            if header is None:
                empty_sheets.append(ws.title)
                continue
            missing = [name for name in ERROR_REPORT_COLUMNS if name not in header]
            duplicates = [name for name in ERROR_REPORT_COLUMNS if header.count(name) > 1]
            if missing or duplicates:
                schema_issues.append({
                    "sheet": ws.title,
                    "missing_columns": missing,
                    "duplicate_columns": duplicates,
                    "error": "Unsupported or ambiguous processing-report header",
                })
                continue
            recognized_sheets.append(ws.title)
            positions = {name: header.index(name) for name in ERROR_REPORT_COLUMNS}
            for row_index, row in enumerate(rows, 2):
                values = {name: row[index] if index < len(row) else None
                          for name, index in positions.items()}
                error_values = [values[name] for name in ("Error type", "Error code", "Error message")]
                if all(value is None or str(value).strip() == "" for value in error_values):
                    continue
                if values["Error type"] is None or str(values["Error type"]).strip() == "":
                    schema_issues.append({
                        "sheet": ws.title, "row": row_index,
                        "error": "Error code or message is present without Error type",
                    })
                findings.append({
                    "report_sheet": ws.title,
                    "report_row": row_index,
                    "original_sheet": values["Original Sheet"],
                    "original_record": values["Original record #"],
                    "error_type": values["Error type"],
                    "error_code": values["Error code"],
                    "error_message": values["Error message"],
                })
    finally:
        wb.close()

    if not recognized_sheets:
        schema_issues.append({"sheet": None, "error": "No recognized processing-report schema found"})
    root_errors = [finding for finding in findings
                   if str(finding["error_type"]).strip().casefold() == "input error"]
    not_processed = [finding for finding in findings
                     if str(finding["error_code"]).strip().casefold() == "not processed"]
    if schema_issues:
        interpretation = "Some sheets or rows could not be interpreted; resolve schema issues before drawing a complete conclusion."
    elif root_errors:
        interpretation = "Fix Input Error rows first; Not Processed rows may be cascading warnings."
    else:
        interpretation = "No Input Error rows were found in the recognized report sheets."
    interpretation += " This report does not verify upload success or the resulting live configuration."
    payload = {
        "status": "invalid_input" if schema_issues else "report_read",
        "report_file": str(args.report),
        "report_sha256": sha256_file(args.report),
        "recognized_report_sheets": recognized_sheets,
        "empty_sheets": empty_sheets,
        "schema_issues": schema_issues,
        "upload_success_verified": False,
        "finding_count": len(findings),
        "by_error_type": counter_to_dict(Counter(finding["error_type"] for finding in findings)),
        "by_error_code": counter_to_dict(Counter(finding["error_code"] for finding in findings)),
        "root_input_errors": root_errors,
        "not_processed_warning_count": len(not_processed),
        "interpretation": interpretation,
        "findings": findings,
    }
    print_json(payload)
    return 2 if schema_issues else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except INPUT_ERRORS as exc:
        print(json.dumps({"status": "invalid_input", "error": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
