# ClioFactors | Production-function analysis

**Dataset:** Douglas: The Theory of Wages (`douglas`)
**Series:** output `DT19AS01`, capital `DT19AS03`, labor `DT19AS02`.
**Data archive SHA-256:** `bbe0ad253ec84261e1d8e2c236fa302f36fc83be5fea178663f56d73d467e1ad`

## Estimates

| Measure | levels | growth |
|:--|--:|--:|
| Years | 1890–1926 | 1891–1926 |
| Observations | 37 | 36 |
| Capital elasticity α | 0.2182 | -0.1289 |
| Labor elasticity β | 0.8457 | 0.6897 |
| α + β (returns to scale) | 1.0638 | 0.5608 |
| R² (transformed outcome) | 0.9598 | 0.5610 |
| RMSE (log units) | 0.0816 | 0.0422 |
| Durbin–Watson | 0.4064 | 2.3362 |
| Condition number | 171.3119 | 18.7492 |
| HAC SE capital elasticity | 0.0814 | 0.0983 |
| HAC SE labor elasticity | 0.1512 | 0.1007 |

## Specification and interpretation

**Levels:** log(output) = c + α·log(capital) + β·log(labor) + ε. For historical indexes, α and β are conditional associations, not causal effects. Estimated scale exp(c) = 0.7504.

**Growth:** Δlog(output) = c + α·Δlog(capital) + β·Δlog(labor) + ε. The reported fitted changes use 100·(exp(Δlog output)−1). Growth models are sensitive to measurement error and short samples.

## Reproducibility and limits

- Data are historical user-provided snapshots, not refreshed official series. See the project’s `docs/DATA.md`.
- Complete-case years are inner-joined; no interpolation, rebasing, or inferred observations.
- Estimates are ordinary least squares. HAC standard errors use a Bartlett-weighted Newey–West covariance with 2 lags; they do not resolve confounding, nonstationarity, or specification error.
- High level-regression R² may reflect common trends. Review the growth specification separately.
- The coefficient sum is a model statistic, **not** proof of technological returns to scale.
- Units and series compatibility must be evaluated before interpreting custom selections.
- Figures and CSV files record actual values and fitted observations. `manifest.json` records the input checksum, versions, and arguments.

## Files

- `input.csv`: overlapping unmodified numeric observations.
- `levels.csv`, `levels.json`, `levels.png`.
- `growth.csv`, `growth.json`, `growth.png`.
- `manifest.json`: run parameters and provenance.
