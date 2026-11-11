"""Exercise offline tools through their public command-line interfaces."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "amazon-ads-bulk-optimizer" / "scripts"
BULK_HEADERS = [
    "Entity", "Campaign ID", "Campaign Name", "Start Date", "State",
    "SKU", "ASIN (Informational only)", "Campaign State (Informational only)",
    "Ad Group State (Informational only)", "Placement", "Percentage",
    "Daily Budget", "Bidding Strategy", "Operation",
]

REPORT_HEADERS = ["Original Sheet", "Original record #", "Error type", "Error code", "Error message"]


class ReaderCLITests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def run_cli(self, name, *arguments):
        env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *map(str, arguments)],
            capture_output=True, text=True, encoding="utf-8", env=env,
            check=False,
        )

    def write_bulk(self, rows, headers=None):
        path = self.directory / "bulk.xlsx"
        wb = Workbook()
        ws = wb.active
        ws.title = "Sponsored Products Campaigns"
        selected_headers = BULK_HEADERS if headers is None else headers
        ws.append(selected_headers)
        for row in rows:
            ws.append([row.get(header) for header in selected_headers])
        wb.save(path)
        wb.close()
        return path

    def campaign(self, campaign_id):
        return {
            "Entity": "Campaign", "Campaign ID": campaign_id,
            "Campaign Name": "Fictional campaign " + campaign_id,
            "Start Date": "20260101", "State": "enabled",
            "Daily Budget": 12, "Bidding Strategy": "Dynamic bids - down only",
        }

    def product(self, campaign_id, asin="B0EXAMPLE01", sku="EXAMPLE-SKU"):
        return {
            "Entity": "Product Ad", "Campaign ID": campaign_id,
            "State": "enabled", "SKU": sku, "ASIN (Informational only)": asin,
            "Campaign State (Informational only)": "enabled",
            "Ad Group State (Informational only)": "enabled",
        }

    def test_both_identity_filters_must_match_the_same_product_ad(self):
        rows = [
            self.campaign("1001"), self.product("1001"),
            self.campaign("1002"), self.product("1002", sku="DEMO-MUG-RED"),
            self.campaign("1003"), self.product("1003", asin="B0SYNTH002"),
        ]
        result = self.run_cli(
            "inspect_bulk.py", "--bulk", self.write_bulk(rows),
            "--asin", "B0EXAMPLE01", "--sku", "EXAMPLE-SKU",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["target_enabled_campaign_count"], 1)
        self.assertEqual(payload["target_enabled_campaigns"][0]["campaign_id"], "1001")


    def test_non_text_requested_identity_requires_text_export(self):
        cases = [
            ("SKU", self.product("1001", sku=123),
             ["--asin", "B0EXAMPLE01"],
             ["--asin", "B0EXAMPLE01", "--sku", "123"]),
            ("ASIN (Informational only)", self.product("1001", asin=1234567890),
             ["--sku", "EXAMPLE-SKU"],
             ["--asin", "1234567890", "--sku", "EXAMPLE-SKU"]),
        ]
        for column, product, other_filter, paired_filters in cases:
            with self.subTest(column=column):
                path = self.write_bulk([self.campaign("1001"), product])
                unfiltered = self.run_cli("inspect_bulk.py", "--bulk", path, *other_filter)
                self.assertEqual(unfiltered.returncode, 0, unfiltered.stderr)
                self.assertEqual(json.loads(unfiltered.stdout)["target_enabled_campaign_count"], 1)
                filtered = self.run_cli("inspect_bulk.py", "--bulk", path, *paired_filters)
                self.assertEqual(filtered.returncode, 2, filtered.stdout[:500] + filtered.stderr)
                payload = json.loads(filtered.stderr)
                self.assertEqual(payload["status"], "invalid_input")
                self.assertIn(column, payload["error"])
                self.assertIn("Re-export", payload["error"])
                self.assertIn("as text", payload["error"])

    def test_missing_identity_or_parent_state_column_is_an_input_error(self):
        for column in ("ASIN (Informational only)", "Ad Group State (Informational only)"):
            with self.subTest(column=column):
                headers = [name for name in BULK_HEADERS if name != column]
                result = self.run_cli(
                    "inspect_bulk.py", "--bulk",
                    self.write_bulk([self.campaign("1001"), self.product("1001")], headers),
                    "--asin", "B0EXAMPLE01",
                )
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn(column, result.stderr)


    def test_ambiguous_or_incomplete_bulk_structure_is_not_a_clean_result(self):
        campaign = self.campaign("1001")
        product = self.product("1001")
        placement = {"Entity": "Bidding Adjustment", "Campaign ID": "1001",
                     "Placement": "Placement Top", "Percentage": 0}
        incomplete_product = dict(product, State=None)
        incomplete_identity = dict(product, **{"ASIN (Informational only)": None})
        cases = [
            ("duplicate header", [campaign, product], BULK_HEADERS + ["State"]),
            ("duplicate campaign", [campaign, campaign, product], BULK_HEADERS),
            ("duplicate placement", [campaign, product, placement, placement], BULK_HEADERS),
            ("orphan product", [product], BULK_HEADERS),
            ("missing product state", [campaign, incomplete_product], BULK_HEADERS),
            ("missing identity value", [campaign, incomplete_identity], BULK_HEADERS),
            ("no data", [], BULK_HEADERS),
        ]
        for label, rows, headers in cases:
            with self.subTest(case=label):
                result = self.run_cli(
                    "inspect_bulk.py", "--bulk", self.write_bulk(rows, headers),
                    "--asin", "B0EXAMPLE01",
                )
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stderr)["status"], "invalid_input")


    def test_product_match_retains_missing_placement_and_export_scope_without_writing(self):
        rows = [self.campaign("1001"), self.product("1001"),
                self.product("1001", asin="B0SYNTH002", sku="DEMO-NOTEBOOK-GREEN"),
                {"Entity": "Bidding Adjustment", "Campaign ID": "1001",
                 "Placement": "Placement Top", "Percentage": 0},
                {"Entity": "Bidding Adjustment", "Campaign ID": "1001",
                 "Placement": "Placement Rest Of Search", "Percentage": None}]
        path = self.write_bulk(rows)
        original = path.read_bytes()
        result = self.run_cli("inspect_bulk.py", "--bulk", path, "--asin", "B0EXAMPLE01")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        campaign = payload["target_enabled_campaigns"][0]
        self.assertEqual(campaign["placements"]["Placement Top"], 0)
        self.assertIsNone(campaign["placements"]["Placement Rest Of Search"])
        self.assertIsNone(campaign["placements"]["Placement Product Page"])
        self.assertEqual(path.read_bytes(), original)
        self.assertIs(payload["campaign_exclusive_scope_verified"], False)
        self.assertEqual(campaign["product_ad_scope"], {
            "total_rows_in_export": 2, "matching_rows_in_export": 1,
            "other_rows_in_export": 1,
        })
        self.assertEqual(payload["target_product_ad_count"], 1)


    def write_report(self, sheets):
        path = self.directory / "report.xlsx"
        wb = Workbook()
        wb.remove(wb.active)
        for name, rows in sheets.items():
            ws = wb.create_sheet(name)
            for row in rows:
                ws.append(row)
        wb.save(path)
        wb.close()
        return path

    def test_unknown_or_ambiguous_report_schema_is_not_success(self):
        valid = [REPORT_HEADERS, ["Sponsored Products Campaigns", 2, "Input Error",
                                 "Invalid header", "The original upload header is invalid."]]
        cases = [
            ("unrecognized", {"Unknown": [["Status"], ["Accepted"]]}, 0),
            ("partial", {"Recognized": valid, "Partial": [REPORT_HEADERS[:-1]]}, 1),
            ("duplicate", {"Recognized": valid,
                           "Ambiguous": [REPORT_HEADERS + ["Error type"]]}, 1),
        ]
        for label, sheets, expected_errors in cases:
            with self.subTest(case=label):
                result = self.run_cli("explain_report.py", "--report", self.write_report(sheets))
                self.assertEqual(result.returncode, 2, result.stdout[:500] + result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "invalid_input")
                self.assertTrue(payload["schema_issues"])
                self.assertEqual(len(payload["root_input_errors"]), expected_errors)


    def test_generated_examples_are_read_across_sheets_without_modifying_exports(self):
        output = self.directory / "generated"
        generated = subprocess.run(
            [sys.executable, str(ROOT / "examples" / "make_examples.py"),
             "--output-dir", str(output)],
            capture_output=True, text=True, encoding="utf-8", check=False,
            env=dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1"),
        )
        self.assertEqual(generated.returncode, 0, generated.stderr)
        bulk = output / "synthetic_bulk.xlsx"
        report = output / "synthetic_report_invalid_headers.xlsx"
        originals = {path: path.read_bytes() for path in (bulk, report)}
        inspection = self.run_cli("inspect_bulk.py", "--bulk", bulk,
                                  "--asin", "B0EXAMPLE01", "--sku", "EXAMPLE-SKU")
        self.assertEqual(inspection.returncode, 0, inspection.stderr)
        self.assertEqual(json.loads(inspection.stdout)["target_enabled_campaign_count"], 1)
        explanation = self.run_cli("explain_report.py", "--report", report)
        self.assertEqual(explanation.returncode, 0, explanation.stderr)
        payload = json.loads(explanation.stdout)
        self.assertEqual(len(payload["root_input_errors"]), 2)
        self.assertEqual({row["report_sheet"] for row in payload["root_input_errors"]},
                         {"Campaign errors", "Product errors"})
        self.assertEqual(payload["not_processed_warning_count"], 1)
        self.assertIs(payload["upload_success_verified"], False)
        for path, original in originals.items():
            self.assertEqual(path.read_bytes(), original)


    def test_required_identity_and_unreadable_files_are_clear_input_errors(self):
        valid = self.write_bulk([self.campaign("1001"), self.product("1001")])
        result = self.run_cli("inspect_bulk.py", "--bulk", valid)
        self.assertEqual(result.returncode, 2, result.stdout[:500] + result.stderr)
        self.assertIn("--asin", result.stderr)
        self.assertIn("--sku", result.stderr)
        corrupt = self.directory / "corrupt.xlsx"
        corrupt.write_bytes(b"This is not an Excel workbook.")
        missing = self.directory / "missing.xlsx"
        for path in (corrupt, missing):
            for name, flag in (("inspect_bulk.py", "--bulk"), ("explain_report.py", "--report")):
                with self.subTest(file=path.name, reader=name):
                    arguments = [flag, path]
                    if name == "inspect_bulk.py":
                        arguments += ["--asin", "B0EXAMPLE01"]
                    result = self.run_cli(name, *arguments)
                    self.assertEqual(result.returncode, 2, result.stdout[:500] + result.stderr)
                    self.assertEqual(json.loads(result.stderr)["status"], "invalid_input")


    def test_report_error_without_type_is_retained_and_marked_incomplete(self):
        path = self.write_report({"Incomplete": [REPORT_HEADERS,
            ["Sponsored Products Campaigns", 2, None, "Invalid header", "A header is invalid."]]})
        result = self.run_cli("explain_report.py", "--report", path)
        self.assertEqual(result.returncode, 2, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["finding_count"], 1)
        self.assertEqual(payload["findings"][0]["error_code"], "Invalid header")
        self.assertEqual(payload["schema_issues"][0]["row"], 2)

    def test_report_without_error_rows_does_not_verify_upload_success(self):
        path = self.write_report({"Recognized": [REPORT_HEADERS]})
        result = self.run_cli("explain_report.py", "--report", path)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["finding_count"], 0)
        self.assertIs(payload["upload_success_verified"], False)


if __name__ == "__main__":
    unittest.main()
