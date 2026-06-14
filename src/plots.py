"""
plots.py — Visualisations that make experiments easy to understand.

Four main plots are provided:

  plot_true_function       The hidden f(x) + noise distribution.
  plot_observations        Scatter of every (x, y) experiment so far.
  plot_gp_posterior        GP mean ± 2σ uncertainty band after k experiments.
  plot_learning_curves     Cumulative-best and cumulative-regret vs experiments.

All functions accept an optional ``ax`` argument so you can embed them inside
larger figure layouts.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Helper: consistent colour palette across strategies
# ---------------------------------------------------------------------------
STRATEGY_COLORS = {
    "Random": "#e07b54",
    "Grid": "#5b8db8",
    "Bayesian": "#3a9e6b",
}

def _strategy_color(name: str) -> str:
    for key, color in STRATEGY_COLORS.items():
        if key.lower() in name.lower():
            return color
    return "#888888"


# ---------------------------------------------------------------------------
# 1.  True function + noise illustration
# ---------------------------------------------------------------------------

def plot_true_function(
    simulator,
    ax: Optional[plt.Axes] = None,
    n_points: int = 400,
    show_noise_band: bool = True,
) -> plt.Axes:
    """
    Draw the hidden response function and a ±1σ noise band.

    In a real experiment you never see this curve — only noisy dots.
    Showing it here lets us understand how well each strategy does.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 4))

    lo, hi = simulator.bounds
    xs = np.linspace(lo, hi, n_points)
    ys_true = np.array([simulator.true_value(x) for x in xs])

    ax.plot(xs, ys_true, color="black", linewidth=2, label="True f(x)", zorder=3)

    if show_noise_band:
        ax.fill_between(
            xs,
            ys_true - simulator.noise_std,
            ys_true + simulator.noise_std,
            alpha=0.15,
            color="black",
            label=f"±1σ noise (σ={simulator.noise_std})",
        )

    ax.set_xlabel("Parameter x")
    ax.set_ylabel("Response y")
    ax.set_title("Hidden response function (you never see this!)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    return ax


# ---------------------------------------------------------------------------
# 2.  Scatter of observations
# ---------------------------------------------------------------------------

def plot_observations(
    xs: List[float],
    ys: List[float],
    simulator,
    ax: Optional[plt.Axes] = None,
    label: str = "Observations",
    color: str = "#e07b54",
) -> plt.Axes:
    """Overlay noisy observations on the true function curve."""
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 4))

    # Draw true function in background
    lo, hi = simulator.bounds
    xs_line = np.linspace(lo, hi, 400)
    ys_true = np.array([simulator.true_value(x) for x in xs_line])
    ax.plot(xs_line, ys_true, color="black", linewidth=1.5, alpha=0.5, label="True f(x)")

    ax.scatter(xs, ys, color=color, s=40, alpha=0.8, label=label, zorder=4)
    ax.set_xlabel("Parameter x")
    ax.set_ylabel("Response y")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    return ax


# ---------------------------------------------------------------------------
# 3.  GP posterior with uncertainty band
# ---------------------------------------------------------------------------

def plot_gp_posterior(
    xs_observed: List[float],
    ys_observed: List[float],
    simulator,
    strategy,          # BayesianStrategy instance (has posterior_at method)
    ax: Optional[plt.Axes] = None,
    title: str = "GP posterior belief",
) -> plt.Axes:
    """
    Show the GP's current belief (mean ± 2σ) given the observations so far.

    The shaded band represents *epistemic uncertainty* — regions we haven't
    explored much yet remain wide; well-sampled regions narrow down.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 4))

    lo, hi = simulator.bounds
    xs_query = np.linspace(lo, hi, 500)

    mu, sigma = strategy.posterior_at(xs_query, xs_observed, ys_observed)

    # True function (dashed)
    ys_true = np.array([simulator.true_value(x) for x in xs_query])
    ax.plot(xs_query, ys_true, "k--", linewidth=1.5, alpha=0.6, label="True f(x)")

    # GP mean
    ax.plot(xs_query, mu, color="#3a9e6b", linewidth=2, label="GP mean")

    # 2-sigma uncertainty band
    ax.fill_between(
        xs_query,
        mu - 2 * sigma,
        mu + 2 * sigma,
        alpha=0.25,
        color="#3a9e6b",
        label="GP ±2σ",
    )

    # Observations
    ax.scatter(
        xs_observed, ys_observed,
        color="#e07b54", s=50, zorder=5, label="Observations",
    )

    ax.set_xlabel("Parameter x")
    ax.set_ylabel("Response y")
    ax.set_title(title)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    return ax


# ---------------------------------------------------------------------------
# 4.  Learning curves
# ---------------------------------------------------------------------------

def plot_learning_curves(
    results: Dict[str, Tuple[List[float], List[float]]],
    simulator,
    figsize: Tuple[int, int] = (12, 5),
) -> plt.Figure:
    """
    Two-panel figure:
      Left  — cumulative best observation vs. experiment number
      Right — simple regret vs. experiment number

    Parameters
    ----------
    results : dict of {strategy_name: (xs, ys)}
    simulator : LabSimulator (needed to compute regret against true optimum)
    """
    from src.metrics import cumulative_best, cumulative_regret

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

    _, f_star = simulator.best_true_value()

    for name, (xs, ys) in results.items():
        color = _strategy_color(name)
        steps = np.arange(1, len(xs) + 1)

        # Left panel: cumulative best
        ax1.plot(steps, cumulative_best(ys), color=color, linewidth=2, label=name)

        # Right panel: cumulative regret (log scale helps read early differences)
        regret = cumulative_regret(xs, ys, simulator)
        ax2.plot(steps, regret, color=color, linewidth=2, label=name)

    # True optimum reference line
    ax1.axhline(f_star, color="black", linestyle="--", linewidth=1, label="True optimum")

    ax1.set_xlabel("Experiment #")
    ax1.set_ylabel("Best y found so far")
    ax1.set_title("Learning curve: best found")
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    ax2.set_xlabel("Experiment #")
    ax2.set_ylabel("Simple regret")
    ax2.set_title("Regret over time (lower = better)")
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 5.  GP posterior evolution (multi-panel)
# ---------------------------------------------------------------------------

def plot_posterior_snapshots(
    xs_all: List[float],
    ys_all: List[float],
    simulator,
    strategy,
    snapshots: Tuple[int, ...] = (5, 10, 20, 30),
    figsize: Tuple[int, int] = (14, 8),
) -> plt.Figure:
    """
    Show how the GP's belief evolves as more experiments are run.

    snapshots : tuple of experiment counts at which to draw the posterior.
    """
    n_panels = len(snapshots)
    fig, axes = plt.subplots(2, (n_panels + 1) // 2, figsize=figsize)
    axes = axes.flatten()

    i = -1
    for i, k in enumerate(snapshots):
        if k > len(xs_all):
            break
        plot_gp_posterior(
            xs_all[:k],
            ys_all[:k],
            simulator,
            strategy,
            ax=axes[i],
            title=f"After {k} experiments",
        )

    # Hide unused panels
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("GP posterior: how beliefs update with each experiment", fontsize=12)
    fig.tight_layout()
    return fig
