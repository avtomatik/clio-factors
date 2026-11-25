# Methodology and research cautions

## Reference series

The reference selection is taken from the bundled `dataset_douglas.zip`, Table 19 of Paul H. Douglas, *The Theory of Wages*, page 160 (bibliography reproduced from source-file metadata, not independently source-verified). The dataset describes the movement of product `P`, labor `L`, and capital `C` in Massachusetts manufacturing from 1890 to 1926, with 1899=100.

- `DT19AS01` → `output`
- `DT19AS02` → `labor`
- `DT19AS03` → `capital`

All 37 years are present, and no imputation is needed. These indexes are historical proxies, not physical measures of value-added or the modern BEA capital stock.

## Fitting method

The first exploratory specification is:

`log Y_t = c + α log K_t + β log L_t + ε_t`.

The second fits consecutive annual changes:

`Δlog Y_t = c + α Δlog K_t + β Δlog L_t + ε_t`.

Each is estimated using NumPy's least-squares solver on an intercept and two regressors. We reject missing, non-finite and non-positive series, collinear design matrices, and samples shorter than eight points. Both specifications require consecutive annual observations, since the serial-correlation diagnostics assume equally spaced years. Both report `R²` on the **transformed** dependent variable, log-RMSE, the Durbin–Watson statistic and condition number.

We report a Bartlett-weighted Newey–West heteroskedasticity and autocorrelation consistent (HAC) covariance estimator with default lag `2` and no finite-sample correction. Formula: `V = (X'X)^(-1) S (X'X)^(-1)`, where `S` sums contemporaneous and weighted lead/lag outer products of `X_t ε_t`. HAC standard errors are *not* a substitute for causal identification or unit-root testing. Adjust `--hac-lags` as a sensitivity check; results should not be treated as confirmed confidence intervals from short samples.

## Reading the reports

- `α` and `β` are sample associations conditional on the chosen transformation and assumptions, sometimes loosely called elasticities.
- `α+β` measures *fitted* returns to scale in the specified function, not observed technological returns to scale.
- The levels intercept exponentiates to a coefficient for the three historic indexes; it is not a universal productivity level.
- The growth intercept represents fitted log growth outside contemporaneous log changes in the two inputs.
- `exp(Δlog Y)-1` is the exact fractional change; figures show the value times 100.
- Regressions on trended variables can be spurious; large R² in levels cannot establish a meaningful structural relationship.
- Publication-quality historical inference requires original-source auditing, measurement consistency, economic historical context, unit-root and cointegration checks, alternative sample periods, and independent replication.

## No assumptions silently filled in

We do not rebase the indexes, splice missing series, deflate nominal variables, assume equal annual units for other datasets, or mix distinct sources into the default recipe. The `fit` CLI permits other same-archive identifiers as an exploratory convenience, but statistical validity and variable interpretation remain the researcher's responsibility.
