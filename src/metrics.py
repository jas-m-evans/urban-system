"""
metrics.py — How we measure "who found the best setting fastest?"

Three simple numbers tell most of the story:

  best_found      The highest noisy observation in the run.
  simple_regret   Gap between the true global optimum and the true value at
                  our best-guess x (lower is better; 0 is perfect).
  cumulative_best The running maximum of noisy observations — produces the
                  "learning curve" you see in the plots.

Cumulative regret (the sum of per-step regrets) is also computed; it is the
standard metric used in the explore/exploit literature.
"""

import numpy as np
from typing import List, Tuple

from src.simulator import LabSimulator


# ---------------------------------------------------------------------------
# Point-in-time metrics
# ---------------------------------------------------------------------------

def best_found(ys: List[float]) -> float:
    """Highest noisy observation recorded in the run."""
    return float(np.max(ys))


def simple_regret(
    xs: List[float],
    ys: List[float],
    simulator: LabSimulator,
) -> float:
    """
    Simple regret = true_optimum_value − true_value_at_our_best_x.

    "Our best guess for x" is the one with the highest noisy observation.
    We then evaluate the *true* (noiseless) function there to measure how
    far we are from the global optimum.

    Returns
    -------
    float ≥ 0   (0 means we found the exact optimum)
    """
    best_idx = int(np.argmax(ys))
    x_best_guess = xs[best_idx]
    _, f_star = simulator.best_true_value()
    f_at_guess = simulator.true_value(x_best_guess)
    return float(f_star - f_at_guess)


# ---------------------------------------------------------------------------
# Trajectory metrics (one value per experiment step)
# ---------------------------------------------------------------------------

def cumulative_best(ys: List[float]) -> np.ndarray:
    """
    Running maximum of noisy observations.

    Plots as a non-decreasing "learning curve": how quickly does the strategy
    latch onto good regions?
    """
    return np.maximum.accumulate(np.array(ys, dtype=float))


def cumulative_regret(
    xs: List[float],
    ys: List[float],
    simulator: LabSimulator,
) -> np.ndarray:
    """
    At each step t, compute the *simple* regret of our best-so-far guess.

    Returns an array of length len(xs) showing how regret shrinks over time.
    """
    _, f_star = simulator.best_true_value()
    regrets = []
    for t in range(1, len(xs) + 1):
        best_x_so_far = xs[int(np.argmax(ys[:t]))]
        f_at_guess = simulator.true_value(best_x_so_far)
        regrets.append(f_star - f_at_guess)
    return np.array(regrets, dtype=float)


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

def summarise(
    results: dict,
    simulator: LabSimulator,
) -> None:
    """
    Print a comparison table for a dict of {strategy_name: (xs, ys)}.

    Example
    -------
    >>> summarise({"Random": (xs_r, ys_r), "Bayesian": (xs_b, ys_b)}, sim)
    """
    _, f_star = simulator.best_true_value()
    header = f"{'Strategy':<15} {'Best found':>12} {'Simple regret':>15} {'# experiments':>15}"
    print(header)
    print("-" * len(header))
    for name, (xs, ys) in results.items():
        bf = best_found(ys)
        sr = simple_regret(xs, ys, simulator)
        print(f"{name:<15} {bf:>12.4f} {sr:>15.4f} {len(xs):>15d}")
    print(f"\nTrue optimum: {f_star:.4f}")
