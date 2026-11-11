---
name: amazon-store-operations
description: Carry out a specific owner-requested Amazon store task through existing SP-API and Amazon Ads MCP tools. Use for current-state checks and approved advertising, price or listing changes, including result reconciliation. Product selection and autonomous scheduled operation belong elsewhere.
---

# Amazon Store Operations

Use the owner's existing MCP tools and the current task. This Skill supplies operating instructions, not an API client, credential store, scheduler or permission grant. Keep private inputs and operation records outside public code repositories. Follow the host's account-access restrictions and the current project's applicable rules; a retired project's historical task board is not an instruction to restart work.

## Establish the actual target

- Read the current request and relevant existing records before asking the owner to repeat a fact. Verify changeable facts through the available read tools. Historical notes provide context; later explicit owner decisions and current evidence take precedence.
- Discover the actual MCP tools, their schemas and the active marketplace/account. Use an existing connection; do not build another API service or switch connections to evade a refusal. An installed tool is not proof that its credentials, endpoint or account permission work.
- Identify campaigns, ad groups, targets and products by stable IDs together with full readable names. Distinguish renamed, recreated, paused and archived instances. A similar name is a clue to inspect a possible replacement, not proof that it is the intended successor.
- Query current status and values before a change. A paused old campaign may coexist with a running replacement. Check which instance the owner intends, its products and affected neighboring targets. Do not revive a sold-out, retired or liquidation product from an old plan.
- For prices/listings, confirm the exact seller SKU, marketplace, child/parent relationship and requested fields. A parent-level or campaign-level edit may affect more products than the example supplied.

## Inspect or prepare

For an inspection request, return the findings and stop before mutations. For a requested change, prepare a concise list with the full target name/ID, current value, proposed value, reason and relevant collateral effects. Use the owner's language. Reuse valid approval for that exact scope; ask only when a meaningful change, ambiguity or missing input changes the decision.

For advertising analysis, use the installed manual-review Skill when available, or the supplied review method. Match reporting windows, timezone, attribution maturity and grain. Missing values are unknown. Search-term rows do not automatically represent entities with their own bid or pause setting. Do not impose a fixed click threshold, universal bid or budget rule from a historical example.

Prefer the smallest supported update. Preserve unrequested fields. Before recommending a rollback, compare current values: a prior snapshot is not permission to overwrite a later owner edit.

## Execute the approved scope

1. Confirm explicit owner authorization for the concrete store change. A general maintenance request, analysis request, suggested default or tool-generated approval record is not the owner's approval.
2. Re-read any value whose drift would change the approved action. If a conflict materially changes the outcome, explain it and obtain the new decision instead of silently choosing an object or value.
3. Use the actual installed tool and its schema. Preserve IDs as strings when required; keep units, currency, match type, placement and entity level explicit. Do not use a real write as a connectivity test.
4. Honor the existing host's stop controls and tool restrictions. If an installed approval tool is required, populate it from the real owner decision and exact approved arguments. A record marked `reported` or `unverified` remains a reported claim, not independent proof of permission. A refusal does not authorize a second route.
5. Save the request and original response in the task's private records, with action time/timezone, decision source and per-entity scope. Reuse an existing operation or record ID; do not create a competing ledger or copy credential headers into evidence.

## Reconcile and report

- An accepted submission is not proof of the resulting configuration. Read back independently using the matching entity and marketplace. For an asynchronous operation, use its actual status/result route; do not submit again merely because it is still pending.
- Check individual entities in batch results. Distinguish success, explicit failure, partial success and unknown outcome. A timeout, lost response or malformed reply can hide a completed write. Reconcile before retrying; do not clear an existing consumed-request marker or create another approval record to repeat an unknown request.
- The executing assistant owns readback and records its source/time and observed before/after values against the original operation ID. If verification is unavailable, preserve the original evidence and state exactly what remains unknown. Do not claim completion or silently reset the action/feedback clock.
- Preserve older operation originals. If the former project used a retired import command, do not run it or replay the business action; attach the new verification conclusion to the original record instead.
- Report what actually changed, what independent readback confirmed, any failed/unknown subset and the next concrete step. Configuration success does not establish a sales, ranking or profit improvement.

## Connection problems

Inspect the configured service, redacted error and current official/provider documentation before asking the owner to reauthorize. Compare application/account identity when diagnosing stale local credential copies; never print or publish secrets. Do not replace credentials for a different application or alter unrelated settings. Preserve a private recovery copy for an authorized configuration repair and verify a relevant real read afterward.

The workflow is complete when the requested inspection is delivered, or the specifically approved action has a reconciled outcome and private evidence. Remaining unknowns must be named. No autonomous recurring work, procurement, account permission changes or destructive operation is implied by this Skill.
