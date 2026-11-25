"""Headless, publication-friendly exploratory charts."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .model import ModelFit


def plot_fit(fit: ModelFit, destination: Path, *, title: str) -> None:
    observations = fit.observations
    is_levels = fit.statistics.specification == "levels"
    y_actual, y_fit = (("actual", "predicted") if is_levels else
                       ("actual_pct_change", "predicted_pct_change"))
    fig, (ax, residual_ax) = plt.subplots(
        2, 1, figsize=(10, 6.5), sharex=True,
        gridspec_kw={"height_ratios": [3, 1]}, constrained_layout=True,
    )
    fig.patch.set_facecolor("#ffffff")
    ax.plot(observations.index, observations[y_actual], lw=2, color="#164e63", label="Observed")
    ax.plot(observations.index, observations[y_fit], lw=1.8, color="#e07a36", label="Model")
    ax.set_title(title, loc="left", fontweight="bold", fontsize=14, pad=14)
    ax.set_ylabel("Historical index" if is_levels else "Annual change (%)")
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", frameon=False, ncol=2)
    residual_ax.axhline(0, color="#666666", lw=0.8)
    residual_ax.plot(observations.index, observations["residual_log"], color="#476a8a", lw=1.5)
    residual_ax.set_ylabel("Log residual")
    residual_ax.set_xlabel("Year")
    residual_ax.grid(axis="y", alpha=0.2)
    residual_ax.spines[["top", "right"]].set_visible(False)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(destination, dpi=170, bbox_inches="tight", metadata={"Software": "ClioFactors"})
    plt.close(fig)
