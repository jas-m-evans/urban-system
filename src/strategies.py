"""
strategies.py — Different ways to search the parameter space.

Think of these as different "scientists" with different personalities:

  RandomStrategy   → Picks random settings.  Simple baseline, often surprisingly
                     decent, but never learns from past experiments.

  GridStrategy     → Sweeps evenly through the space.  Great for low dimensions
                     but scales badly (10 points per dimension → 100 in 2-D,
                     1000 in 3-D, …).

  BayesianStrategy → Builds a probabilistic model (Gaussian Process) of f(x)
                     after each experiment and picks the next point using an
                     acquisition function.  Learns fast; the workhorse of
                     automated experimentation.

All three classes share the same interface:
    strategy = XxxStrategy(simulator, n_experiments=30)
    xs, ys = strategy.run()
"""

import numpy as np
from typing import List, Tuple

from src.simulator import LabSimulator


# ---------------------------------------------------------------------------
# Random search
# ---------------------------------------------------------------------------

class RandomStrategy:
    """
    Pick uniformly random settings; the simplest possible baseline.

    Analogy: a chemist who throws darts at a periodic table to pick
    experimental conditions.
    """

    def __init__(
        self,
        simulator: LabSimulator,
        n_experiments: int = 30,
        seed: int = 0,
    ):
        self.sim = simulator
        self.n = n_experiments
        self.rng = np.random.default_rng(seed)

    def run(self) -> Tuple[List[float], List[float]]:
        """Run all experiments and return (xs, ys)."""
        lo, hi = self.sim.bounds
        xs, ys = [], []
        for _ in range(self.n):
            x = float(self.rng.uniform(lo, hi))
            y = self.sim.observe(x)
            xs.append(x)
            ys.append(y)
        return xs, ys


# ---------------------------------------------------------------------------
# Grid search
# ---------------------------------------------------------------------------

class GridStrategy:
    """
    Sweep evenly spaced settings — like a systematic dose-escalation screen.

    Works well in 1-D but misses resolution if the budget is small compared
    to the landscape's complexity.
    """

    def __init__(self, simulator: LabSimulator, n_experiments: int = 30):
        self.sim = simulator
        self.n = n_experiments

    def run(self) -> Tuple[List[float], List[float]]:
        lo, hi = self.sim.bounds
        xs_grid = np.linspace(lo, hi, self.n)
        xs, ys = [], []
        for x in xs_grid:
            y = self.sim.observe(float(x))
            xs.append(float(x))
            ys.append(y)
        return xs, ys


# ---------------------------------------------------------------------------
# Bayesian / GP-surrogate strategy
# ---------------------------------------------------------------------------

class BayesianStrategy:
    """
    Gaussian-Process surrogate + Upper Confidence Bound (UCB) acquisition.

    How it works, step by step:
    1. Start with a few random experiments (warm-up phase).
    2. Fit a Gaussian Process (GP) to all data so far.
       A GP is a flexible model that also tells you *how uncertain* it is at
       each x — think of it as drawing a "confidence band" over possible f(x).
    3. Choose the next x by maximising UCB = μ(x) + κ·σ(x):
       - Large μ(x) → looks promising (exploit)
       - Large σ(x) → we're very uncertain there (explore)
       κ controls the explore/exploit trade-off (higher κ → more exploration).
    4. Observe y at that x, update the GP, repeat.

    This mirrors real Bayesian inference: each experiment updates our posterior
    belief about f, and we act on that posterior.

    Parameters
    ----------
    simulator : LabSimulator
    n_experiments : int
        Total budget (including warm-up).
    n_init : int
        Number of random warm-up experiments before the GP kicks in.
    kappa : float
        Exploration weight in UCB.  Try 1.0 (greedy) to 5.0 (exploratory).
    seed : int
        For reproducibility of the warm-up random draws.
    matern_nu : float
        Smoothness parameter for the Matérn kernel (default 2.5 → twice
        differentiable).  Common choices: 0.5, 1.5, 2.5.
    length_scale_bounds : (float, float)
        Lower and upper bounds on the GP length-scale hyperparameter during
        optimisation.  Tighten if you see many convergence warnings.
    n_restarts_optimizer : int
        Number of random restarts for GP hyperparameter optimisation.
    """

    def __init__(
        self,
        simulator: LabSimulator,
        n_experiments: int = 30,
        n_init: int = 5,
        kappa: float = 2.0,
        seed: int = 0,
        matern_nu: float = 2.5,
        length_scale_bounds: tuple = (1e-2, 10.0),
        n_restarts_optimizer: int = 3,
    ):
        self.sim = simulator
        self.n = n_experiments
        self.n_init = n_init
        self.kappa = kappa
        self.rng = np.random.default_rng(seed)
        self.matern_nu = matern_nu
        self.length_scale_bounds = length_scale_bounds
        self.n_restarts_optimizer = n_restarts_optimizer

    # ------------------------------------------------------------------
    def _make_gpr(self):
        """Create a fresh GaussianProcessRegressor with the configured kernel."""
        from sklearn.gaussian_process import GaussianProcessRegressor
        from sklearn.gaussian_process.kernels import Matern

        kernel = Matern(nu=self.matern_nu, length_scale_bounds=self.length_scale_bounds)
        return GaussianProcessRegressor(
            kernel=kernel,
            n_restarts_optimizer=self.n_restarts_optimizer,
            random_state=0,
        )

    # ------------------------------------------------------------------
    def _ucb(self, xs_candidate: np.ndarray, gpr) -> np.ndarray:
        """Upper Confidence Bound acquisition value at each candidate point."""
        mu, sigma = gpr.predict(xs_candidate.reshape(-1, 1), return_std=True)
        return mu + self.kappa * sigma

    # ------------------------------------------------------------------
    def run(self) -> Tuple[List[float], List[float]]:
        lo, hi = self.sim.bounds
        xs_all: List[float] = []
        ys_all: List[float] = []

        # ---- Phase 1: random warm-up --------------------------------
        for _ in range(self.n_init):
            x = float(self.rng.uniform(lo, hi))
            y = self.sim.observe(x)
            xs_all.append(x)
            ys_all.append(y)

        # ---- Phase 2: GP-guided experiments -------------------------
        gpr = self._make_gpr()

        # Dense candidate grid for acquisition maximisation
        xs_candidates = np.linspace(lo, hi, 1000)

        for _ in range(self.n - self.n_init):
            X_train = np.array(xs_all).reshape(-1, 1)
            y_train = np.array(ys_all)
            gpr.fit(X_train, y_train)

            acq_values = self._ucb(xs_candidates, gpr)
            x_next = float(xs_candidates[np.argmax(acq_values)])

            y = self.sim.observe(x_next)
            xs_all.append(x_next)
            ys_all.append(y)

        return xs_all, ys_all

    # ------------------------------------------------------------------
    def posterior_at(self, xs_query: np.ndarray, xs_observed, ys_observed):
        """
        Return (mean, std) of the GP posterior at xs_query, given observations.
        Useful for plotting uncertainty bands.
        """
        gpr = self._make_gpr()
        gpr.fit(np.array(xs_observed).reshape(-1, 1), np.array(ys_observed))
        mu, sigma = gpr.predict(xs_query.reshape(-1, 1), return_std=True)
        return mu, sigma
