# Project working agreement

Read README.md, docs/design.md and the relevant TASKS.md item before changing this project. This is a small public collection of seller workflows and local tools. It has no dependency on another store repository or on personal memory.

- Keep reusable instructions and configuration documentation in English. Use the user's requested language for reports.
- Keep real reports, credentials, customer data, account identifiers, private operations and raw conversations outside this checkout. Use synthetic fixtures. A .gitignore is an aid, not proof that a staged file is safe.
- Preserve source evidence, missing-versus-zero semantics, entity scope, units and dates. Do not turn a historical threshold or individual preference into a universal operating rule.
- Choose a narrow interface and test through it. For a code defect, reproduce the failure, make the minimal repair, then run affected tests. Reuse valid results; do not expand a small repair into a framework or coverage campaign.
- Run `python -m unittest discover -s tests -v` for script changes. Review changed instructions semantically and verify their local references. Use fresh independent review for publication privacy, execution permissions or consequential scope changes.
- The shipped scripts are offline and read-only with respect to supplied exports. The fixture generator writes only synthetic files to its specified output directory. No store writes, model calls, schedulers or uploads are included.
- Keep one writer per file set. Record current delivery and remaining work in TASKS.md; avoid competing status files or transcript dumps. Use short-lived branches for subsequent changes.
- Review the staged file list before publication; never copy an old repository's Git history. Preserve unknown or unique material during cleanup. Retire task-owned temporary outputs only after delivery or recovery no longer needs them.
