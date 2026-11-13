# Manual advertising retrospective

## Inputs needed for this question

Identify the product/account scope, owner objective, review dates/timezone and relevant comparison baseline. Use an existing decision if its conditions still apply. Do not infer current clearance, growth, profit or ranking goals from old notes.

Gather only the evidence the question needs:

| Evidence | Supports | Does not establish |
| --- | --- | --- |
| Configuration snapshot | Values and entity/product mapping at capture time | Every intermediate change or current values after capture |
| Change history | Changes within its observed type/date/pagination coverage | Actor identity when the source omits it; completeness outside coverage |
| Campaign/target/query/placement reports | Metrics at the report's own grain and attribution basis | Unobserved cross-dimensions or live configuration |
| Product-level business report | Overall orders/units, sales and traffic at its defined grain | Exact organic-order attribution from subtraction alone |
| Owner explanation | Stated goal, reason or confirmed manual action | A fact the owner did not state or a future action approval |

Report incomplete coverage, partial days, changed baselines and immature attribution. Label estimates. Use zero only when the source actually reports zero. For a ratio with a zero or missing denominator, show unavailable rather than 0%.

## Analysis

Build a short timeline before computing a causal story. Separate product stage, price, inventory, review/variant changes and promotion effects from advertising changes. Compare aligned windows and note which configurations were actually active. A lower-bid restart may have a different traffic mix and sampling rate; aggregate orders alone do not isolate the restart's effect.

Use query data for query-specific conclusions and placement data for placement conclusions. If genuine joint query/campaign/placement observations exist for the requested window, use their actual coverage. Do not infer that joint data always exists or never exists. Keep Amazon Business and Off Amazon separate until their overlap, units and requested denominator are established.

Evaluate both absolute outcomes and efficiency. Explain relevant sample size, volatility, costs and alternative explanations. A smaller advertising bill can reduce losses while also reducing useful orders; the owner decides the tradeoff from current evidence. A specific successful campaign does not prove a universal matching, naming, threshold or budget strategy.

### Combined bid and placement changes

Compare the applicable target bid (or inherited default) and placement adjustment together. For the placement-only component, `base bid * (1 + adjustment percent / 100)` gives the placement-adjusted base. Synthetic example: $0.50 with +200% gives $1.50; $0.40 with +250% gives $1.40. The percentage rose while this component fell. This is neither realized CPC nor a universal final bid ceiling: dynamic, rule-based or other applicable modifiers need their own current configuration. Preserve unknowns rather than assuming those modifiers are absent. Amazon's [Sponsored Products guide](https://advertising.amazon.com/library/guides/sponsored-products-best-practices) distinguishes placement adjustments, bidding strategies and actual CPC.

### Query groups and shared totals

Define whether a result describes an exact query, a token/phrase group or an intent family. State normalization and membership rules; a substring search for `hat` also matches `what`. An exact query and its broader group can have different outcomes. Retain source rows and count control totals at their original metric grain. When a query belongs to multiple groups, overlapping group totals or word-weighted orders must not be added as independent orders.

For campaigns spanning products, include known campaign totals once and show any unsupported product allocation as shared/unallocated. Allocate only from compatible, actual product-level evidence; distinguish advertised-product from purchased-product attribution. Do not copy the total to every product or guess a split from overall product sales. Reconcile allocated plus unallocated amounts to the campaign total; the missing breakout does not invalidate the known total or prove incrementality.

### Contribution and break-even checks

For an economic comparison, define pre-ad contribution after the applicable product, platform, fulfillment, logistics, discount and return costs; do not deduct a cost twice. State any excluded costs and keep fixed-overhead allocation separate. Unknown costs remain unknown.

Use the same product mix, dates and advertising attribution basis throughout:

- `ad CVR = attributed orders / clicks` as a decimal; whole-product Unit Session Percentage is not a substitute.
- `break-even average CPC = ad CVR × pre-ad contribution per attributed order`.
- `break-even ACOS = total pre-ad contribution of attributed orders / attributed revenue` as a ratio (multiply by 100 for percent).

Use order-level contribution for multi-unit orders. Missing or zero denominators make the affected calculation unavailable. When revenue and net receipts differ, reconcile them rather than substituting one denominator for another. These are accounting identities for the stated cohort, not a causal model, a bid recommendation or a prediction of future conversion. Attributed profit does not establish incremental profit; whole-business profitability needs its own cost reconciliation.

Synthetic example: $10 contribution per order and 10% ad CVR imply $1 break-even average CPC. This does not create a universal $1 target or prove that any campaign is profitable. Tie the recommendation to the current owner's objective rather than requiring organic share or rank to rise in every case. Amazon's [ACOS guide](https://advertising.amazon.com/library/guides/acos-advertising-cost-of-sales) connects break-even ACOS with profit margin; the CPC equation above follows from the stated units.

### Historical orders and negative recommendations

Assess the dominant buying need against the product's verified form; word overlap, query length and match labels alone do not establish fit. A bundle containing an accessory does not prove suitability for a buyer seeking that accessory alone. Use available query/result evidence and observed purchases, keeping ambiguous intent explicit. This informs a recommendation, not automatic exclusion or permission to apply a negative across other products or campaigns.

A historical order is relevant evidence, not permanent immunity from a negative recommendation. Conversely, zero orders for one product do not erase another product's conversions. Compare the actual product/campaign scope, related queries, current economics, preserved exceptions and attribution maturity. Separate an owner's business tradeoff under uncertainty from statistical proof; a historical example grants no new execution permission.

## Output and follow-up

For each requested entity, summarize the prior action and stated reason, current observed configuration, direct advertising performance, product-level result where available, confounders, recommendation and remaining unknowns. Cite the private source file or returned evidence and capture/window dates next to material numbers.

When proposing a change, include exact before/after values and affected entities, plus the evidence that would confirm or disconfirm the expected result. Do not invent owner reasons or reopen already-settled routine choices. Keep recommendations, owner decisions, observed actions, later readback and business outcomes distinct.

Use the user's requested follow-up window when known. Evidence maturity can qualify the result without blocking otherwise authorized work. Preserve historical successes, failures and counterexamples together; retire an obsolete recommendation rather than silently converting it into a new task.
