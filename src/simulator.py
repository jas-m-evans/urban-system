"""
simulator.py — The "toy lab" that we run experiments on.

Imagine you have a mysterious black box — a real physical experiment, a
manufacturing process, or a drug dose-response curve.  You can *poke* the box
by choosing a parameter setting x and you get back a noisy measurement y.
The true relationship f(x) is hidden from you; you can only discover it by
running experiments.

This file provides:
  - Two built-in response functions (1-D bumpy, 2-D Gaussian mixture)
  - LabSimulator: records every experiment and adds realistic noise
"""

import numpy as np
from typing import Callable, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Built-in response functions — the "hidden truth" inside the black box
# ---------------------------------------------------------------------------

def response_1d_multimodal(x: float) -> float:
    """
    A bumpy 1-D landscape with a clear global maximum but plenty of local
    traps.  Inspired by dose-response curves where "more is not always better".

    Domain: x in [-2, 2]
    """
    return float(np.sin(3.0 * x) + 0.5 * np.sin(8.0 * x) - 0.3 * x ** 2)


def response_2d_gaussian_mixture(xy: np.ndarray) -> float:
    """
    A 2-D surface with two peaks, like a material property that peaks at two
    different (temperature, pressure) combinations.

    xy : array-like of shape (2,), both components in [0, 1]
    """
    xy = np.asarray(xy, dtype=float)
    x0, x1 = xy[0], xy[1]
    peak1 = np.exp(-((x0 - 0.30) ** 2 + (x1 - 0.70) ** 2) / 0.05)
    peak2 = 0.8 * np.exp(-((x0 - 0.75) ** 2 + (x1 - 0.25) ** 2) / 0.04)
    return float(peak1 + peak2)


# ---------------------------------------------------------------------------
# LabSimulator
# ---------------------------------------------------------------------------

class LabSimulator:
    """
    Simulates running noisy experiments on a hidden response function.

    Each call to ``observe(x)`` returns a noisy reading of the true function:
        y = f(x) + ε,  ε ~ Normal(0, noise_std²)

    All (x, y) pairs are stored in ``self.history`` so strategies can look
    back at what they've already measured.

    Parameters
    ----------
    response_fn : callable
        The true (hidden) function.  Takes a scalar (1-D) or 1-D array (2-D)
        and returns a float.
    noise_std : float
        Standard deviation of Gaussian measurement noise.  Larger → noisier
        experiments.
    bounds : (lo, hi) for 1-D  OR  [(lo0, hi0), (lo1, hi1)] for 2-D
    rng : int seed or np.random.Generator
        Controls reproducibility.  Pass the same seed to get the same noise.
    """

    def __init__(
        self,
        response_fn: Callable = response_1d_multimodal,
        noise_std: float = 0.10,
        bounds: Union[Tuple[float, float], List[Tuple[float, float]]] = (-2.0, 2.0),
        rng: Union[int, np.random.Generator, None] = 42,
    ):
        self.response_fn = response_fn
        self.noise_std = noise_std
        self.bounds = bounds

        if isinstance(rng, int):
            self.rng = np.random.default_rng(rng)
        elif rng is None:
            self.rng = np.random.default_rng()
        else:
            self.rng = rng

        # Experiment log: list of (x, y_noisy) tuples
        self.history: List[Tuple] = []

    # ------------------------------------------------------------------
    def observe(self, x) -> float:
        """
        Run one experiment at parameter setting x.

        Returns the *noisy* measurement (what you'd see in a real lab).
        Also appends (x, y) to self.history.
        """
        true_value = float(self.response_fn(x))
        noise = float(self.rng.normal(0.0, self.noise_std))
        y_noisy = true_value + noise
        self.history.append((x, y_noisy))
        return y_noisy

    def true_value(self, x) -> float:
        """Return the noiseless ground-truth (used only for evaluation)."""
        return float(self.response_fn(x))

    def reset(self) -> None:
        """Clear experiment history so the same simulator can be re-used."""
        self.history.clear()

    # ------------------------------------------------------------------
    def best_true_value(self, n_grid: int = 2000) -> Tuple[float, float]:
        """
        Find the global optimum on a fine grid (1-D only).

        Returns
        -------
        (x_best, f_best) : the true optimal parameter and its true value.
        """
        if not isinstance(self.bounds[0], (int, float)):
            raise NotImplementedError("best_true_value is only implemented for 1-D bounds.")
        lo, hi = self.bounds
        xs = np.linspace(lo, hi, n_grid)
        ys = np.array([self.response_fn(x) for x in xs])
        idx = int(np.argmax(ys))
        return float(xs[idx]), float(ys[idx])
