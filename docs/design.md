# Design and acceptance

## Outcome

Provide reusable, inspectable seller workflows that an owner and an AI assistant can execute on demand. The first delivery is a manual Amazon Ads retrospective with offline workbook inspection. Public methods and code live here; real inputs and execution records stay in a separately chosen private location.

## Scope

Included: a self-contained Skill, a source-linked review worksheet, inspection of supplied Sponsored Products Bulk exports, explanation of supplied processing reports, and generated synthetic examples.

Not included in this release: an autonomous store operator, data collection service, ad upload builder, live API writer, hosted application, account management, product selection, shared budget service, memory system or recurring job. Existing independent projects retain their responsibilities. Adding one requires a concrete need and separate scope decision, not merely a migration opportunity.

## Modules and interfaces

| Module | Interface | Responsibility |
| --- | --- | --- |
| Manual review Skill | Task plus current owner context and supplied evidence | Reconstruct changes, compare like-for-like results, expose unknowns and prepare recommendations |
| Bulk inspector | `inspect_bulk.py --bulk PATH --asin VALUE` and/or `--sku VALUE` | Read configuration evidence and identity/state coverage; both identity filters must match when both are supplied |
| Processing-report reader | `explain_report.py --report PATH` | Read every sheet and distinguish root errors from cascading warnings; never certify upload success from absent errors |
| Fixture generator | `make_examples.py --output-dir PATH` | Create fictional local workbooks for onboarding and tests |

These CLI interfaces are the test seams. Tests use actual temporary workbooks and subprocess results, not mocks of helper functions. Read-only inspection must preserve the input bytes. Missing placement values remain null. Invalid/missing structure must not be reported as an empty successful analysis. A target match does not certify that all other products in its campaign are safe to change.

## Evidence vocabulary

Configuration describes values at a captured time. Change history describes observed events and their coverage. Performance describes a metric at a stated grain, window and attribution basis. These are distinct inputs. Campaign totals and placement margins cannot manufacture query-by-placement observations.

Prepared recommendation, accepted submission, observed configuration and business effect are separate states. This release reaches review/recommendation only. A future live action must use the user's separately authorized current route, exact scope, before/after values, result reconciliation and readback.

## Delivery acceptance

- A fresh checkout can run the documented synthetic example and tests with only its declared dependency.
- An independent reader can complete a review from the Skill without private paths or a retired project's runtime.
- Tests cover identity scope, missing data, actual read-only behavior and processing errors across sheets.
- Public files contain no business inputs, credentials, private account identifiers or old operational history.
- Local installation matches the reviewed public files, with a recoverable previous installation.
- Release, local installation and demonstrated business effect are reported separately; synthetic tests do not prove sales improvement.
