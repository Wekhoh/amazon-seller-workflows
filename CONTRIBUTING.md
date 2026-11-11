# Development workflow

Start with the user outcome and existing code. Read docs/design.md; add a new module only when an actual caller needs an independently useful interface.

For code changes, use a short red-green cycle at a public interface: write one representative failing case, confirm it fails for the expected behavior, implement the smallest complete change, then run the affected existing tests. Do not create tests for harmless prose or assert the implementation against itself. Instruction changes need semantic review and realistic use, not a large test suite.

Use synthetic temporary inputs and the documented local commands. Run `python -m unittest discover -s tests -v` before a script delivery. Inspect the diff, privacy boundary, changed callers and relevant error behavior. Broaden verification only for a real change, failure or unresolved concern. Record meaningful validation in the commit or PR, and update TASKS.md at delivery.

Subsequent work uses a short-lived branch and a focused PR. Preserve earlier approvals within their exact scope. Public publication does not authorize store actions or paid services. CI runs offline tests only when code, test or workflow inputs change, with no scheduled jobs, credentials or paid APIs.

Keep actual customer/store inputs outside this checkout. Any example must be generated or deliberately fictional, including workbook metadata. Check `git diff --cached` and the staged file names before pushing. MIT applies to project-authored material; review upstream licenses and attribution before importing third-party content.

The development approach draws on Matt Pocock's module-interface design, writing-for-agents and TDD guidance. It is adapted to this project's real interfaces and risk; contributors do not need a particular agent plugin installed.
