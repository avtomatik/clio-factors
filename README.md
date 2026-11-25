# ClioFactors

**Reproducible research for historical economic data and production functions.**

ClioFactors revives an archive of economic-history experiments as a documented, offline-first Python research toolkit. It preserves the original historical datasets, provides a searchable series catalog, and makes one complete reference analysis reproducible end to end. The original exploratory scripts are retained under `legacy/`, but do not form part of the supported API.

> **Research status:** Version 1.0 is a focused, working research foundation — **not** an endorsed econometric model, a validated historical database, or a general-purpose forecasting platform. Historical sources and data redistribution rights require independent review before public distribution.

## Why this project exists

Older research code often mixes raw files, notebooks, hard-coded paths, downloads, and plotting side effects. ClioFactors separates sources from transformations and statistical methods. Every run emits an input fingerprint, a machine-readable coefficient summary, aligned observations, diagnostics, and a readable research report. No API keys, live network access, or cloud service are necessary for the reference run.

## Start here

Python **3.11+** required. From the extracted project directory:

```bash
python -m pip install -e .
python -m cliofactors verify
python -m cliofactors catalog
python -m cliofactors series douglas --contains DT19AS0
python -m cliofactors reproduce --out results/massachusetts-manufacturing
```

Equivalent console command after installation: `cliofactors reproduce`. The last command writes `report.md`, fitted-observation CSV files, JSON statistics, `manifest.json`, and high-resolution PNG charts to the selected directory. A verified reference run also lives in `examples/reference-run/`.

## Reproduced reference: Massachusetts manufacturing, 1890–1926

The default recipe uses *Paul H. Douglas, The Theory of Wages*, Table 19 (p. 160), as transcribed in the supplied dataset. Its three original 1899=100 manufacturing indexes are:

| Role | Original ID | Meaning |
|---|---|---|
| Output | `DT19AS01` | Manufacturing product index (`P`) |
| Labor | `DT19AS02` | Labor index (`L`) |
| Capital | `DT19AS03` | Capital index (`C`) |

Two model specifications are generated:

- **Levels:** `log(Y) = c + α log(K) + β log(L) + ε` (37 annual observations).
- **Growth:** `Δlog(Y) = c + α Δlog(K) + β Δlog(L) + ε` (36 annual changes).

Results may be strongly sensitive to common trends; this project deliberately reports *both* specifications. The coefficients describe conditional historical associations and should not be interpreted as causal technology parameters without much stronger identification assumptions. See [Methodology](docs/METHODOLOGY.md).

## Explore your datasets

```bash
cliofactors catalog
cliofactors series cobb-douglas --limit 50
cliofactors series us-census --contains P0107
cliofactors inspect douglas DT19AS03 --limit 8
cliofactors verify
```

Run a custom same-dataset regression (choose **meaningful compatible series**, not arbitrary combinations):

```bash
cliofactors fit \
  --dataset douglas \
  --output-id DT19AS01 \
  --capital-id DT19AS03 \
  --labor-id DT19AS02 \
  --start-year 1899 --end-year 1926 \
  --spec both \
  --out results/custom
```

Run `cliofactors --help` and `cliofactors fit --help` for all flags. Output paths are overwritten if the command is run in the same directory; choose a new folder to preserve previous runs.

## Architecture

```text
src/cliofactors/
  catalog.py       Explicit dataset schema and provenance notes
  data.py          ZIP/CSV loading, series discovery, SHA-256 verification
  model.py         Log-linear Cobb–Douglas fits, diagnostics, HAC standard errors
  reporting.py     Reproducible CSV, JSON, Markdown and run manifests
  charts.py        Headless, two-panel PNG plots
  cli.py           Tested command-line interface
  datasets/        Original bundled ZIP files and integrity manifest
examples/
  reference-run/   Generated example results for immediate inspection
docs/
  ARCHITECTURE.md  System boundaries and extension strategy
  DATA.md          Source inventory, historical caveats and licensing notes
  METHODOLOGY.md   Estimation choices and limitations
  MIGRATION.md     Archive audit, renames and preserved originals
  LEGACY_INVENTORY.md  Map of all 38 archived Python experiments
  ROADMAP.md       Focused future expansion plan
legacy/
  experiments/     Original experimental Python sources, not imported
  data/            Miscellaneous unattached original data snapshots
  uv.lock          Original dependency lockfile (historical, not authoritative)
tests/             Regression, data integrity and CLI tests
.github/workflows/  CI: Python 3.11, 3.13 and 3.14
```

## Quality checks

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python -m compileall -q src
python -m cliofactors verify
```

A CI workflow runs tests and reproduces the report without plots. The package works as an installed distribution because it reads its data with `importlib.resources`, not from a fragile repository-relative path. The original archives are never extracted or overwritten.

## Scope and limitations

This project does **not** reconstruct unavailable BEA/Federal Reserve snapshots referenced by the old code, make network calls, or pretend the historical archives are checked against primary-source publications. `legacy/experiments/` is a preservation area. It should not be run without a separate dependency and data audit; several scripts import missing functions/files or plot at import time.

See [Data provenance](docs/DATA.md), [Migration](docs/MIGRATION.md), [Experiment inventory](docs/LEGACY_INVENTORY.md), [Roadmap](docs/ROADMAP.md), [Contributing](CONTRIBUTING.md) and [Security](SECURITY.md).

## License

MIT for this project's **code** (retained from the supplied archive). Data may carry third-party conditions that MIT does not override: consult [DATA.md](docs/DATA.md) before sharing or republishing historical source material.
