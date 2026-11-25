# Contributing to ClioFactors

1. Open an issue describing the research question and intended series provenance.
2. Preserve raw source snapshots byte-for-byte; add a new named version instead of editing old data.
3. Put tested, import-safe functions in `src/cliofactors/`; never import from `legacy/` in production.
4. Add tests for at least one successful example and realistic failures (missing years, invalid data, collinearity).
5. Describe source, time range, units, transformations, and limitations in the relevant documentation.
6. Run `python -m pytest -q`, `python -m compileall -q src`, `python -m cliofactors verify`.
7. Avoid making causal claims from ordinary regressions or distributing third-party data without permission.

The historical files are potentially governed by source-specific terms. Verify rights and bibliographic details before submitting a public data change. Security issues should be disclosed privately to the repository maintainer rather than including exploits or secrets in an issue.
