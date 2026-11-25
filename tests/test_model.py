import numpy as np
import pandas as pd
import pytest

from cliofactors.model import fit_cobb_douglas


def synthetic(n=30):
    year = pd.Index(range(1990, 1990 + n), name='year')
    t = np.arange(n)
    capital = 100.0 * np.exp(0.02*t + 0.04*np.sin(t*0.9))
    labor = 50.0 * np.exp(0.01*t + 0.05*np.cos(t*1.2))
    output = 2.3 * capital**0.35 * labor**0.65
    return pd.DataFrame({'output': output, 'capital': capital, 'labor': labor}, index=year)


def test_exact_synthetic_fit_recovers_known_parameters():
    result = fit_cobb_douglas(synthetic())
    s = result.statistics
    assert s.n == 30
    assert s.capital_elasticity == pytest.approx(.35, abs=1e-9)
    assert s.labor_elasticity == pytest.approx(.65, abs=1e-9)
    assert s.productivity_scale == pytest.approx(2.3, abs=1e-8)
    assert s.r_squared == pytest.approx(1, abs=1e-9)
    assert s.returns_to_scale == pytest.approx(1, abs=1e-9)
    assert result.observations.predicted.to_numpy() == pytest.approx(synthetic().output.to_numpy())


def test_growth_fit_exact_synthetic_log_difference():
    result = fit_cobb_douglas(synthetic(), specification='growth')
    s = result.statistics
    assert s.n == 29
    assert s.first_year == 1991
    assert s.capital_elasticity == pytest.approx(.35, abs=1e-8)
    assert s.labor_elasticity == pytest.approx(.65, abs=1e-8)
    assert s.productivity_scale is None
    assert result.observations.actual_pct_change.notna().all()


@pytest.mark.parametrize('mutation,match', [
    (lambda f: f.assign(capital=-1.0), 'positive'),
    (lambda f: f.assign(labor=np.nan), 'nonmissing'),
    (lambda f: f.assign(output=np.inf), 'finite'),
    (lambda f: f.iloc[:7], 'At least 8'),
    (lambda f: f.assign(labor=f.capital * 2), 'collinear'),
    (lambda f: f.iloc[::-1], 'increasing'),
])
def test_invalid_series_fail_loudly(mutation, match):
    with pytest.raises(ValueError, match=match):
        fit_cobb_douglas(mutation(synthetic()))


@pytest.mark.parametrize('specification', ['levels', 'growth'])
def test_missing_year_rejected(specification):
    with pytest.raises(ValueError, match='consecutive'):
        fit_cobb_douglas(synthetic().drop(index=2005), specification=specification)


def test_invalid_spec_and_hac_lag():
    with pytest.raises(ValueError, match='specification'):
        fit_cobb_douglas(synthetic(), specification='unknown')
    with pytest.raises(ValueError, match='hac_lags'):
        fit_cobb_douglas(synthetic(), hac_lags=100)
