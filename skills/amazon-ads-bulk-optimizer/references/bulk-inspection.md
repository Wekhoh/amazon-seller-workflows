# Offline workbook inspection

Use these tools only for supplied exports and processing reports. They open input files read-only, emit JSON and do not connect to Amazon or generate upload files. Verify a current platform format before extending support; these supported column names are not a claim that every future export has the same schema.

The helpers require Python 3.11 or later and the dependency in [requirements.txt](../requirements.txt), tested with Python 3.14 and openpyxl 3.1.5. Use a verified interpreter; if needed, install these requirements into the task's isolated environment. Reading the workflow alone requires no Python setup. Do not modify an unrelated environment or expose credentials to run offline inspection.

## Configuration lookup

Run `scripts/inspect_bulk.py --bulk PATH --asin VALUE` and/or `--sku VALUE` with a current export. Both supplied identifiers must match the same Product Ad. Each requested identity column must contain text values; numeric cells are rejected because spreadsheet conversion may have lost leading zeros or precision. Re-export those identifiers as text from the original source rather than guessing the missing characters. The inspector reads the `Sponsored Products Campaigns` sheet. It reports enabled product/campaign matches from the actual Campaign, Product Ad and informational state fields; check the returned scope and any error before interpreting an empty result.

Current placement adjustments are configuration values in `Bidding Adjustment` rows, not placement performance. Keep a missing Percentage unknown; a zero is an actual zero. Common labels include `Placement Top`, `Placement Rest Of Search`, `Placement Product Page`, and `Placement Amazon Business`; do not relabel or merge unknown placements.

The result is a configuration lookup. A matched product does not establish exclusive campaign ownership, full historical coverage, actual target delivery or authorization to change the campaign. Read the other entity layers and current source when a subsequent task requires them.

## Processing-report explanation

Run `scripts/explain_report.py --report PATH`. The recognized error columns are `Original Sheet`, `Original record #`, `Error type`, `Error code`, and `Error message`. Inspect all returned sheets and findings. Root `Input Error` rows can cause `Not Processed` warnings in otherwise valid sheets. Fixing a root error is a preparation step, not a successful resubmission.

An absent or unsupported report schema is unknown, not a successful upload. A report containing no recognized input errors still does not establish live store state. Use the actual submission receipt and independent current configuration evidence for those claims.

## Handling outputs

The JSON may contain private identifiers and paths from the supplied file. Keep real output outside the public checkout. Source files remain unchanged. The generated examples are fictional; do not replace them with exported store data in commits or CI.
