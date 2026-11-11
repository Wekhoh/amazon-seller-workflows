#!/usr/bin/env python3
"""Inspect Amazon Ads bulk workbook structure and target SP campaign state."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from amazon_ads_bulk_core import (
    DEFAULT_PLACEMENTS,
    INPUT_ERRORS,
    SP_SHEET,
    bidding_adjustment_map,
    counter_to_dict,
    normalize_date,
    print_json,
    product_matches,
    read_sheet,
    require_columns,
    row_name,
    sha256_file,
    target_enabled_campaigns_by_product,
    workbook_sheet_summary,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bulk", required=True, type=Path)
    parser.add_argument("--asin")
    parser.add_argument("--sku")
    args = parser.parse_args()
    if not (args.asin or args.sku):
        parser.error("Provide --asin and/or --sku to define the product scope")
    if args.asin is not None and not args.asin.strip():
        parser.error("--asin cannot be blank")
    if args.sku is not None and not args.sku.strip():
        parser.error("--sku cannot be blank")

    headers, rows = read_sheet(args.bulk, SP_SHEET)
    required = [
        "Entity", "Campaign ID", "Start Date", "State", "Placement", "Percentage",
        "Campaign State (Informational only)", "Ad Group State (Informational only)",
    ]
    if args.asin is not None:
        required.append("ASIN (Informational only)")
    if args.sku is not None:
        required.append("SKU")
    require_columns(headers, required)
    enabled_targets = target_enabled_campaigns_by_product(rows, asin=args.asin, sku=args.sku)
    ba_map = bidding_adjustment_map(rows)
    matching_products = [row for row in rows
                         if row.get("Entity") == "Product Ad"
                         and product_matches(row, args.asin, args.sku)]

    target_details = []
    for cid, campaign in sorted(enabled_targets.items(), key=lambda item: (normalize_date(item[1].get("Start Date")), row_name(item[1]))):
        placements = {placement: ba_map.get((cid, placement), {}).get("Percentage") for placement in DEFAULT_PLACEMENTS + ["Placement Amazon Business"]}
        placements.update({placement: row.get("Percentage")
                           for (campaign_id, placement), row in ba_map.items()
                           if campaign_id == cid})
        campaign_products = [row for row in rows if row.get("Entity") == "Product Ad"
                             and str(row.get("Campaign ID")) == cid]
        matching_count = sum(product_matches(row, args.asin, args.sku)
                             for row in campaign_products)
        target_details.append(
            {
                "campaign_id": cid,
                "campaign_name": row_name(campaign),
                "start_date": normalize_date(campaign.get("Start Date")),
                "state": campaign.get("State"),
                "budget": campaign.get("Daily Budget"),
                "bidding_strategy": campaign.get("Bidding Strategy"),
                "placements": placements,
                "product_ad_scope": {
                    "total_rows_in_export": len(campaign_products),
                    "matching_rows_in_export": matching_count,
                    "other_rows_in_export": len(campaign_products) - matching_count,
                },
            }
        )

    payload = {
        "status": "inspected",
        "campaign_exclusive_scope_verified": False,
        "scope_note": "A product match does not certify campaign-exclusive scope. "
                      "Product counts describe only this export; confirm its coverage separately.",
        "file": str(args.bulk),
        "sha256": sha256_file(args.bulk),
        "sheet_summary": workbook_sheet_summary(args.bulk),
        "sp_rows": len(rows),
        "sp_columns": len(headers),
        "entity_counts": counter_to_dict(Counter(row.get("Entity") for row in rows)),
        "operation_counts": counter_to_dict(Counter(row.get("Operation") for row in rows)),
        "placement_counts": counter_to_dict(Counter(row.get("Placement") for row in rows if row.get("Entity") == "Bidding Adjustment")),
        "target": {"asin": args.asin, "sku": args.sku},
        "target_product_ad_count": len(matching_products),
        "target_product_ads": [
            {
                "row": row["_row_number"],
                "campaign_id": str(row.get("Campaign ID")),
                "asin": row.get("ASIN (Informational only)"),
                "sku": row.get("SKU"),
                "state": row.get("State"),
                "campaign_state": row.get("Campaign State (Informational only)"),
                "ad_group_state": row.get("Ad Group State (Informational only)"),
            }
            for row in matching_products
        ],
        "target_enabled_campaign_count": len(enabled_targets),
        "target_enabled_start_date_counts": counter_to_dict(Counter(normalize_date(c.get("Start Date")) for c in enabled_targets.values())),
        "target_enabled_campaigns": target_details,
    }
    print_json(payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except INPUT_ERRORS as exc:
        print(json.dumps({"status": "invalid_input", "error": str(exc)}), file=sys.stderr)
        raise SystemExit(2)
