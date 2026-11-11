# Amazon Seller Workflows

Practical seller Skills, evidence-led playbooks and small local tools. MIT licensed. The collection supports manual Amazon Ads review, read-only workbook inspection and owner-directed use of existing Amazon MCP tools.

这是一个按需使用的运营工作流与技能库。提供广告手动复盘、Bulk 检查、处理报告解释，以及通过已有 MCP 操作店铺的流程说明；真实经营资料留在使用者本机。

## What is ready

- [Manual advertising review Skill](skills/amazon-ads-bulk-optimizer/SKILL.md): reconstruct changes, compare compatible evidence, explain uncertainty and prepare owner-reviewed recommendations.
- [Owner-directed MCP operations Skill](skills/amazon-store-operations/SKILL.md): identify current targets, obtain specific approval, use existing tools and reconcile the result. It installs no connector or automation.
- `inspect_bulk.py`: inspect a supplied Sponsored Products Bulk export, scoped by ASIN and/or SKU.
- `explain_report.py`: explain errors in a supplied upload-processing report across sheets.
- A fictional workbook generator and CLI tests. No account, API key or model subscription is required for these scripts.

The historical advertising-review Skill identifier is retained for compatibility; its scripts remain **read-only inspectors**. The separate operations Skill gives instructions for existing, independently configured MCP tools; it includes no API client or executable writer. This repository does not run an autonomous store, collect store data or schedule jobs. Existing applications, product-selection tools and private knowledge systems remain separate projects.

## Quick start

Python 3.11 or later is required; validation currently uses Python 3.14. Windows commands below use PowerShell 7.

```powershell
git clone https://github.com/Wekhoh/amazon-seller-workflows.git
cd amazon-seller-workflows
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe examples/make_examples.py --output-dir outputs/demo
.\.venv\Scripts\python.exe skills/amazon-ads-bulk-optimizer/scripts/inspect_bulk.py --bulk outputs/demo/synthetic_bulk.xlsx --asin B0EXAMPLE01 --sku EXAMPLE-SKU
.\.venv\Scripts\python.exe skills/amazon-ads-bulk-optimizer/scripts/explain_report.py --report outputs/demo/synthetic_report_invalid_headers.xlsx
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

On other systems, use `python3 -m venv .venv` and `.venv/bin/python` for the same commands. The examples are fictional, including their names and identifiers. Generated files are excluded from Git. For actual work, pass the path of an export stored **outside this checkout**. Do not move private reports here just to run a command.

The current readers support the documented English workbook headers; unsupported structures are reported explicitly. The scripts emit JSON to stdout and read the input export without modifying it. Errors return a nonzero exit status. A product match is a lookup result, not permission or proof of exclusive campaign scope. Processing-report findings are evidence about that file, not proof of successful upload or current store configuration.

## Use with an assistant

Ask an assistant to read [SKILL.md](skills/amazon-ads-bulk-optimizer/SKILL.md), then give the review question, current goals and private evidence locations. The folder is self-contained and may be copied to a host-supported Skill directory. If the same Skill is already installed, back it up and replace it intentionally rather than merging old references into the new version. The instruction files can also be used directly without installation.

The [review workflow](skills/amazon-ads-bulk-optimizer/references/manual-review.md) and [review worksheet](examples/review-template.md) define useful inputs and a concise output. They do not impose a fixed bid, click threshold, reporting window or budget.

## Project guide

- [Design and acceptance](docs/design.md): scope, module interfaces and evidence semantics.
- [Development workflow](CONTRIBUTING.md): focused TDD, review and privacy expectations.
- [Agent working agreement](AGENTS.md): instructions for changing this repository.
- [Current delivery](TASKS.md): completed work and actual remaining scope.
- [MIT license](LICENSE).

CI runs the offline tests only for relevant source, test or workflow changes. It has no schedule, account secrets, model calls or store access.

## Public methods, private evidence

Keep credentials, account IDs, customer/order data, raw reports, private change logs and company context outside the repository. Public examples must be synthetic. A generic lesson may be retained with its conditions and uncertainty; an individual store decision is not a universal rule. The existing private reference library and its third-party materials are not part of this release.
