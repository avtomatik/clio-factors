# Dataset provenance and integrity

All ZIP files are **byte-for-byte copies of the supplied original repository archive**. They are historical snapshots, not retrieved afresh from their primary sources, and do not imply that the original transcriptions are correct. A SHA-256 of each ZIP is recorded in `src/cliofactors/datasets/manifest.json`; run `cliofactors verify` to re-check.

| Slug | Raw ZIP | Source described in archive | Status |
|---|---|---|---|
| `douglas` | `dataset_douglas.zip` | Paul H. Douglas, *The Theory of Wages* | Supported series browsing and reference recipe |
| `cobb-douglas` | `dataset_usa_cobb-douglas.zip` | C. W. Cobb & P. H. Douglas, *A Theory of Production* | Browseable; needs independent source audit |
| `kendrick` | `dataset_usa_kendrick.zip` | John W. Kendrick, *Productivity Trends* | Browseable; needs independent source audit |
| `us-census` | `dataset_uscb.zip` | *Historical Statistics of the United States* | Browseable; many domains, units and period types |
| `brown` | `dataset_usa_brown.zip` | Brown, technical-progress material | Browseable; some metadata-only rows |
| `mcconnell-brue` | `dataset_usa_mc_connell_brue.zip` | McConnell & Brue, *Economics*, 2006 | Browseable; labels in Russian |
| `china-turkey-gdp` | `CHN_TUR_GDP.zip` | Country GDP history (source not asserted) | Browseable; current US$; no adjustment for inflation |

The bundled CSV schemas differ. The explicit catalog maps the relevant identifier, period and value columns without guessing. The substantial original US Census CSV is read directly from ZIP without extracting the 22 MB member to disk.

The original autocorrelation TXT and BEA deflator XLS (`dataset_usa_bea-GDPDEF.xls`) are preserved under `legacy/data/`, not included in the supported dataset catalog. The legacy Python code refers to other BEA, Federal Reserve and archival files **absent from the supplied snapshot**; those references are not satisfied or silently downloaded.

## Historical bibliographic review needed

The source fields and table titles come from the original archive; page numbers and series interpretation have **not** been checked against scanned publications. Before publication or policy use, verify historical definitions, units, discontinuities, data collection methods, source revisions and permissible uses.

## Copyright and redistribution

The MIT license copied from the old project covers the project code, but **does not automatically license third-party published tables or transcriptions**. This user's supplied ZIP contains bundled historical tabular material, including modern published materials. Confirm copyright status, relevant licenses and redistribution rights before pushing the dataset resources to a public GitHub repository or publishing wheels. If necessary, replace bundled datasets with a separately licensed retrieval/ingestion workflow, and preserve checksummed local copies privately.
