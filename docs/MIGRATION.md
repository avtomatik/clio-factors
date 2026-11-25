# Migration: Remnants → ClioFactors

## Finding a coherent purpose

The supplied `remnants` snapshot contained ~38 Python scripts, an almost empty README, seven nested CSV ZIPs plus loose data files, and experiments in econometric models, U.S. historical series, visualization, Fourier transforms, autocorrelation and BEA/Census sources. It was not a self-contained, consistently runnable package: many modules execute immediately on import; legacy tests rely on absent datasets; some functions refer to undefined names; and online sources are not reproducible without versioned snapshots.

We elected **not** to force every disconnected experiment into the supported codebase. The new through-line is verifiable historical data → defensible analytical method → reproducible report.

## Renaming map

| Before | After | Reason |
|---|---|---|
| Repository `remnants` | **ClioFactors** | Signals cliometrics and production factors |
| Package `src/core/` | `src/cliofactors/{catalog,data,model,reporting,charts}.py` | Domain-specific, explicit module names; fresh reviewed implementation |
| `src/usa_cobb_douglas.py` | `cliofactors.model.fit_cobb_douglas` + reference recipe | Separate the model from data acquisition and top-level plots |
| `src/core/test.py` | `tests/test_*.py` | Real, portable automated tests rather than exploratory scripts |
| `src/visualization/*`, plotting scripts | `cliofactors.charts` | Explicit headless plotting API |
| `src/core/constants.py` | `cliofactors.catalog` | Discoverable, typed dataset metadata rather than long magic ID lists |
| `data/dataset_*.zip` | `src/cliofactors/datasets/*.zip` | Immutable pip-installable package resources |
| Original `src` | `legacy/experiments` | Historical preservation without importing abandoned code |
| Original `uv.lock` | `legacy/uv.lock` | Its Python 3.14 constraints do not describe the new package |

The new code is **not** a line-for-line port of the old scripts; unsupported analyses remain in the legacy area. No source data ZIP was modified. The original `.txt`, `.xls` and loose CSV-in-subfolder material is preserved under `legacy/data`.

## Quality fixes

- No side effects on `import cliofactors`.
- No hard-coded machine-specific paths or network calls.
- Explicit, safer CSV members loaded via `zipfile` rather than arbitrary extraction.
- Input validation for identifiers, dates, missing/nonpositive values and collinearity.
- Side-by-side level and growth specifications to expose trend sensitivity.
- SHA-256 data integrity, output provenance, CLI errors, automated tests, CI.
- Honest limits: historical transcription, license, and econometric identification require separate verification.

## What was intentionally not repaired

The original live BEA integrations, U.S. Fed historical CSV loaders, annotation drafts, random legacy correlations and experimental Fourier plots were preserved for future research but excluded from the release surface. They need original data, method decisions and source checks before promotion. See `ROADMAP.md`.
