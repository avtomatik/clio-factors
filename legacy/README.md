# Preserved legacy experiments

This directory contains the original research scripts and supplementary data supplied in the `remnants.zip` archive, preserved to avoid losing experimental ideas. `experiments/` contains all **38 original Python files**, **unaltered**; `data/` contains the original loose TXT and XLS files. The original `pyproject.toml`, README and `uv.lock` are also retained as historical records.

**Not a supported package:** do not add these modules to `PYTHONPATH`, assume the scripts are import-safe, or run them against modern BEA or Federal Reserve sources without checking definitions. Many files reference absent historical datasets, undefined functions, and side-effecting plots. The new, supported code is in `src/cliofactors/`.

`legacy/manifest.json` records individual original-script hashes for independent comparison.
