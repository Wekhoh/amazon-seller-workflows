---
name: amazon-ads-bulk-optimizer
description: Review Amazon Ads campaigns, search terms, placements and change history; inspect supplied Bulk exports and explain processing reports. Use for manual retrospectives and evidence-backed recommendations. Includes offline read-only helpers; live writes, automated data collection and product selection are outside this release.
---

# Amazon Ads Manual Review

The name is retained for compatibility. This Skill is self-contained: it does not require an old store repository, scheduler, credentials, hosted service or memory system. For the review sequence and evidence limitations, read [manual-review.md](references/manual-review.md). For a supplied Bulk or processing report, also read [bulk-inspection.md](references/bulk-inspection.md).

## Start from the actual task

Use the owner's current objective, product stage and exact requested entities. In an active managed project, read its applicable instructions and current policy; otherwise use the supplied current evidence and the owner's statements. Historical notes are navigation and evidence, not current instructions or approval. Check for later corrections before reusing a prior decision. Ask only when a missing fact changes the conclusion or authorization; continue independent useful analysis.

Keep real inputs and results in the task's private location outside this public repository. Use available authorized read-only sources when the task needs refreshed evidence; a tool appearing in a catalog does not prove the account's capabilities. This package contains no API client. Source identity, capture time, pagination/coverage, marketplace, timezone and attribution basis accompany the analysis.

## Review and explain

- Separate current configuration, change history and performance. Show full campaign names, with stable entity IDs used for matching. Separate paused/archived/recreated instances rather than merging by name.
- Record the owner-stated reason, the observed action and the assistant's inference separately. A later explanation is not evidence that it was recorded at the original action time. Do not attribute platform or automated bidding changes to the owner without evidence.
- Reconstruct the previous and current configuration windows, including budgets, bids, placements, negatives, status, price, inventory, promotions and variant changes when relevant. Do not assign a multi-change outcome to just one event.
- Match metric grain, dates, attribution maturity and denominators before comparing. Missing is not zero. Search Term, Targeting, campaign and placement rows answer different questions. Campaign/query and campaign/placement marginal tables do not establish a joint query-by-placement conversion rate.
- Compare absolute spend, orders/units and sales with CPC, CVR, CTR, ACOS or TACOS as applicable. Distinguish ad-attributed sales from total product results. Ratios improving through reduced traffic do not alone prove improvement. Organic attribution and ranking causal claims need their own evidence.
- Use current data maturity to label uncertainty, not to invent a universal waiting period. Do not manufacture fixed negative-click thresholds, bid changes, budget bands or permanent category exclusions from an old example.
- For the requested scope, deliver what changed and why, what the evidence supports, what remains unknown, and a specific recommendation. A compact table or conversation may be sufficient; preserve the user's requested output format.

## Decisions and follow-up

A recommendation names the full entity, current value, proposed value and affected neighbors. Campaign placement changes can affect other targets; a target bid can affect multiple queries. A Search Term without its own bid/state cannot be directly paused or repriced. Preserve all unrequested fields and distinguish proposals from approved actions.

This release does not generate uploads or execute store writes. A request to implement recommendations must use a separately supported, currently authorized route with approval of the exact list. Existing specific approvals remain valid within their conditions; analysis or a prior example does not widen them. Unknown or partial write outcomes must be reconciled before retrying. Current-value drift blocks blind replay or rollback.

Keep preparation, accepted submission, independent configuration readback and observed business effect separate. API observations must not be relabelled as Bulk evidence. Preserve the original action time, decision reason and source window for later feedback; delayed bookkeeping does not restart the feedback clock. A final review states unresolved data or feedback gaps rather than filling them with zero or claiming success.
