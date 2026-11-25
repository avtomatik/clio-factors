"""Deterministic research outputs: JSON, CSV, charts and Markdown."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import platform

import numpy as np
import pandas as pd

from . import __version__
from .catalog import dataset
from .data import archive_sha256, load_production_frame
from .model import ModelFit, fit_cobb_douglas


@dataclass(frozen=True, slots=True)
class Selection:
    slug: str
    output_id: str
    labor_id: str
    capital_id: str
    start_year: int | None = None
    end_year: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)


REFERENCE_SELECTION = Selection(
    slug="douglas", output_id="DT19AS01", labor_id="DT19AS02", capital_id="DT19AS03",
    start_year=1890, end_year=1926,
)


def _run_selection(selection: Selection, specifications: tuple[str, ...], hac_lags: int) -> tuple[pd.DataFrame, dict[str, ModelFit]]:
    frame = load_production_frame(
        selection.slug,
        output_id=selection.output_id,
        labor_id=selection.labor_id,
        capital_id=selection.capital_id,
        start_year=selection.start_year,
        end_year=selection.end_year,
    )
    return frame, {
        spec: fit_cobb_douglas(frame, specification=spec, hac_lags=hac_lags)
        for spec in specifications
    }


def _number(value: float | None) -> str:
    return "—" if value is None else f"{value:.4f}"


def render_report(
    selection: Selection, fits: dict[str, ModelFit], checksum: str, *, plots: bool
) -> str:
    source = dataset(selection.slug)
    lines = [
        "# ClioFactors | Production-function analysis", "",
        f"**Dataset:** {source.title} (`{selection.slug}`)",
        f"**Series:** output `{selection.output_id}`, capital `{selection.capital_id}`, labor `{selection.labor_id}`.",
        f"**Data archive SHA-256:** `{checksum}`", "",
        "## Estimates", "",
        "| Measure | " + " | ".join(fits) + " |",
        "|:--|" + "--:|" * len(fits),
    ]
    rows = [
        ("Years", lambda s: f"{s.first_year}–{s.last_year}"),
        ("Observations", lambda s: str(s.n)),
        ("Capital elasticity α", lambda s: _number(s.capital_elasticity)),
        ("Labor elasticity β", lambda s: _number(s.labor_elasticity)),
        ("α + β (returns to scale)", lambda s: _number(s.returns_to_scale)),
        ("R² (transformed outcome)", lambda s: _number(s.r_squared)),
        ("RMSE (log units)", lambda s: _number(s.rmse_log)),
        ("Durbin–Watson", lambda s: _number(s.durbin_watson)),
        ("Condition number", lambda s: _number(s.condition_number)),
        ("HAC SE capital elasticity", lambda s: _number(s.hac_std_error_capital)),
        ("HAC SE labor elasticity", lambda s: _number(s.hac_std_error_labor)),
    ]
    for row_name, accessor in rows:
        lines.append("| " + row_name + " | " + " | ".join(accessor(f.statistics) for f in fits.values()) + " |")
    lines += ["", "## Specification and interpretation", ""]
    for spec, fit in fits.items():
        stats = fit.statistics
        if spec == "levels":
            lines += [
                "**Levels:** log(output) = c + α·log(capital) + β·log(labor) + ε. "
                "For historical indexes, α and β are conditional associations, not causal effects. "
                f"Estimated scale exp(c) = {_number(stats.productivity_scale)}.", "",
            ]
        else:
            lines += [
                "**Growth:** Δlog(output) = c + α·Δlog(capital) + β·Δlog(labor) + ε. "
                "The reported fitted changes use 100·(exp(Δlog output)−1). "
                "Growth models are sensitive to measurement error and short samples.", "",
            ]
    lines += [
        "## Reproducibility and limits", "",
        "- Data are historical user-provided snapshots, not refreshed official series. See the project’s `docs/DATA.md`.",
        "- Complete-case years are inner-joined; no interpolation, rebasing, or inferred observations.",
        "- Estimates are ordinary least squares. HAC standard errors use a Bartlett-weighted "
        f"Newey–West covariance with {next(iter(fits.values())).statistics.hac_lags} lags; "
        "they do not resolve confounding, nonstationarity, or specification error.",
        "- High level-regression R² may reflect common trends. Review the growth specification separately.",
        "- The coefficient sum is a model statistic, **not** proof of technological returns to scale.",
        "- Units and series compatibility must be evaluated before interpreting custom selections.",
        "- Figures and CSV files record actual values and fitted observations. `manifest.json` records "
        "the input checksum, versions, and arguments.", "",
        "## Files", "",
        "- `input.csv`: overlapping unmodified numeric observations.",
        *[f"- `{spec}.csv`, `{spec}.json`" + (f", `{spec}.png`." if plots else ".")
          for spec in fits],
        "- `manifest.json`: run parameters and provenance.", "",
    ]
    return "\n".join(lines)


def run_analysis(
    selection: Selection,
    out_dir: Path,
    *,
    specifications: tuple[str, ...] = ("levels", "growth"),
    hac_lags: int = 2,
    plots: bool = True,
) -> dict:
    """Write deterministic evidence outputs, never modifying source archives."""
    if not specifications or len(set(specifications)) != len(specifications):
        raise ValueError("Choose at least one unique specification")
    frame, fits = _run_selection(selection, specifications, hac_lags)
    source = dataset(selection.slug)
    checksum = archive_sha256(source)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out_dir / "input.csv", float_format="%.12g")
    for spec, fit in fits.items():
        fit.observations.to_csv(out_dir / f"{spec}.csv", float_format="%.12g")
        (out_dir / f"{spec}.json").write_text(
            json.dumps(fit.statistics.as_dict(), indent=2, sort_keys=True, allow_nan=False) + "\n",
            encoding="utf-8",
        )
        if plots:
            from .charts import plot_fit
            plot_fit(
                fit, out_dir / f"{spec}.png",
                title=f"{source.title} | {'Levels' if spec == 'levels' else 'Growth'}",
            )
    result = {
        "tool": "ClioFactors",
        "version": __version__,
        "dataset": selection.to_dict(),
        "source_title": source.title,
        "source_archive": source.filename,
        "source_sha256": checksum,
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "specifications": list(specifications),
        "hac_lags": hac_lags,
        "year_join": "inner",
        "missing_years_imputed": False,
        "plots": plots,
    }
    (out_dir / "manifest.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out_dir / "report.md").write_text(render_report(selection, fits, checksum, plots=plots), encoding="utf-8")
    return result
