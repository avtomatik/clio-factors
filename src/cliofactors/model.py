"""Transparent log-linear Cobb–Douglas OLS for exploratory historical analysis."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True, slots=True)
class FitStatistics:
    specification: str
    n: int
    first_year: int
    last_year: int
    intercept_log: float
    productivity_scale: float | None
    capital_elasticity: float
    labor_elasticity: float
    returns_to_scale: float
    r_squared: float
    rmse_log: float
    durbin_watson: float | None
    condition_number: float
    hac_lags: int
    hac_std_error_intercept: float
    hac_std_error_capital: float
    hac_std_error_labor: float

    def as_dict(self) -> dict:
        from dataclasses import asdict
        return asdict(self)


@dataclass(slots=True)
class ModelFit:
    statistics: FitStatistics
    observations: pd.DataFrame


def _hac_standard_errors(x: np.ndarray, residuals: np.ndarray, lags: int) -> np.ndarray:
    """Bartlett-weighted Newey–West HAC estimate, no finite-sample correction."""
    u = x * residuals[:, None]
    meat = u.T @ u
    for lag in range(1, lags + 1):
        weight = 1.0 - lag / (lags + 1.0)
        cross = u[lag:].T @ u[:-lag]
        meat += weight * (cross + cross.T)
    bread = np.linalg.inv(x.T @ x)
    variance = bread @ meat @ bread
    return np.sqrt(np.maximum(0.0, np.diag(variance)))


def fit_cobb_douglas(frame: pd.DataFrame, *, specification: str = "levels", hac_lags: int = 2) -> ModelFit:
    """Fit log(Y)=log(A)+alpha log(K)+beta log(L)+error.

    'growth' instead models first differences of log output/capital/labor.
    HAC standard errors are descriptive; no causal claim or p-values.
    """
    if specification not in {"levels", "growth"}:
        raise ValueError("specification must be 'levels' or 'growth'")
    if not isinstance(hac_lags, int) or hac_lags < 0:
        raise ValueError("hac_lags must be a non-negative integer")
    required = ["output", "capital", "labor"]
    if not set(required).issubset(frame):
        raise ValueError(f"Expected columns: {', '.join(required)}")
    if frame.index.has_duplicates or not frame.index.is_monotonic_increasing:
        raise ValueError("Year index must be unique and increasing")
    numeric = frame[required].astype(float)
    if numeric.isna().any().any() or not np.isfinite(numeric.to_numpy()).all():
        raise ValueError("All input values must be finite and nonmissing")
    if (numeric <= 0).any().any():
        raise ValueError("Cobb–Douglas log fit requires strictly positive values")
    # HAC/Durbin–Watson diagnostics assume equally spaced yearly observations.
    years = np.asarray(frame.index, dtype=int)
    if np.any(np.diff(years) != 1):
        raise ValueError("Analysis requires consecutive annual years; no gaps or interpolation")
    logged = np.log(numeric)
    if specification == "growth":
        logged = logged.diff().iloc[1:]
    n = len(logged)
    if n < 8:
        raise ValueError("At least 8 observations are required after transformation")
    if hac_lags >= n:
        raise ValueError("hac_lags must be smaller than the observation count")
    y = logged["output"].to_numpy()
    x = np.column_stack([np.ones(n), logged["capital"].to_numpy(), logged["labor"].to_numpy()])
    coefficients, _, rank, singular = np.linalg.lstsq(x, y, rcond=None)
    if rank != 3:
        raise ValueError("Capital/labor series are collinear: cannot identify two elasticities")
    y_hat = x @ coefficients
    residuals = y - y_hat
    ss_total = float(np.sum((y - np.mean(y)) ** 2))
    if ss_total <= 1e-20:
        raise ValueError("Dependent series has essentially zero variation")
    se = _hac_standard_errors(x, residuals, hac_lags)
    dw = float(np.sum(np.diff(residuals) ** 2) / np.sum(residuals**2)) if np.any(residuals) else None
    index = logged.index.copy()
    observations = pd.DataFrame(
        {"actual_log": y, "predicted_log": y_hat, "residual_log": residuals},
        index=index,
    )
    if specification == "levels":
        observations["actual"] = np.exp(y)
        observations["predicted"] = np.exp(y_hat)
    else:
        # exp(delta(log x))-1 is the exact percentage change.
        observations["actual_pct_change"] = 100.0 * np.expm1(y)
        observations["predicted_pct_change"] = 100.0 * np.expm1(y_hat)
    observations.index.name = "year"
    stats = FitStatistics(
        specification=specification,
        n=n,
        first_year=int(index.min()),
        last_year=int(index.max()),
        intercept_log=float(coefficients[0]),
        productivity_scale=float(np.exp(coefficients[0])) if specification == "levels" else None,
        capital_elasticity=float(coefficients[1]),
        labor_elasticity=float(coefficients[2]),
        returns_to_scale=float(coefficients[1] + coefficients[2]),
        r_squared=1.0 - float(np.sum(residuals**2)) / ss_total,
        rmse_log=float(np.sqrt(np.mean(residuals**2))),
        durbin_watson=dw,
        condition_number=float(singular[0] / singular[-1]),
        hac_lags=hac_lags,
        hac_std_error_intercept=float(se[0]),
        hac_std_error_capital=float(se[1]),
        hac_std_error_labor=float(se[2]),
    )
    return ModelFit(stats, observations)
