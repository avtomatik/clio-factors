# Legacy experiment inventory

The **38 original Python files** in the uploaded `remnants` project are preserved, unmodified, under `legacy/experiments/`. This inventory describes their broad *apparent* research theme from static inspection; it is not a claim that those scripts have been executed or audited.

| Research group | Preserved files | Policy |
|---|---|---|
| Historical production and productivity | `usa_cobb_douglas.py`, `usa_cobb_douglas_3d.py`, `usa_capital.py`, `extend_labor.py`, `lab_cap_inty_lab_prty.py`, `employment_structure.py`, `usa_historical.py`, `usa_bea_fixed_assets_series.py`, `dataset_usa_cobb_douglas_meta.py` | Examine for future documented production-function recipes. The initial reference regression is a new implementation, not a direct port. |
| Price indexes and deflators | `usa_deflator.py`, `usa_price_index.py`, `prices.py` | Requires period, nominal/real measure and base-year verification. |
| Time-series and exploratory statistics | `autocorrelation_bootstrap_lag.py`, `autocorrelation_plot_caputl_b50001_a.py`, `discrete_fourier_transform.py`, `test_corr.py`, `calculate_curve_fit_params.py`, `center_by_period.py` | Keep out of the supported model API pending statistical validity checks and reproducible inputs. |
| Visualization and annotation | `annotations.py`, `visualization/annotations.py`, `visualization/usa_un.py`, `visualization/usa_unemployment.py`, `turnover_take_one.py` | Legacy plotting drafts; new reporting uses `cliofactors.charts` with no import-time plotting. |
| Acquisition and data plumbing | `core/classes.py`, `core/combine.py`, `core/constants.py`, `core/funcs.py`, `core/paths.py`, `core/read.py`, `core/transform.py`, `core/tools.py`, `proposition.py`, `statcan_some.py`, `delete_if_same.py` | Old data readers depend on absent sources or live network calls; reimplement functionality with source-verified contracts. |
| Archived testing and notes | `core/test.py`, `core/plot.py`, `refactoring_thesis.py`, `note.py` | Original context only; do not put the archived test script into the supported CI suite. |

Some older files reference original BEA and Federal Reserve snapshots absent from the uploaded archive. Others contain top-level instructions that run on import. No legacy code is included in the installable `cliofactors` wheel. Check `legacy/manifest.json` for individual SHA-256 hashes, and use the migration guide for module renaming.

**Promotion rule:** a legacy experiment becomes part of the supported package only after its input datasets, bibliographic origin, variable units, methodology, tests and licensing have been separately documented and validated.
