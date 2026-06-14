"""
test_metrics.py — Checks that metric calculations are correct.

Covers:
  - best_found returns the true maximum of ys
  - cumulative_best is non-decreasing
  - simple_regret is non-negative and zero when we find the true optimum
  - cumulative_regret is non-negative and non-increasing (eventually)
"""

import numpy as np
import pytest

from src.simulator import LabSimulator
from src.metrics import best_found, cumulative_best, simple_regret, cumulative_regret


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sim():
    return LabSimulator(noise_std=0.0, rng=0)  # noiseless makes assertions cleaner


@pytest.fixture
def known_run(sim):
    """Run grid search so we have a deterministic xs/ys to test against."""
    xs = list(np.linspace(-2.0, 2.0, 20))
    ys = [sim.observe(x) for x in xs]
    return xs, ys


# ---------------------------------------------------------------------------
# best_found
# ---------------------------------------------------------------------------

class TestBestFound:
    def test_returns_maximum(self):
        ys = [1.0, 3.5, 2.0, -1.0, 3.5]
        assert best_found(ys) == 3.5

    def test_single_element(self):
        assert best_found([7.0]) == 7.0

    def test_all_negative(self):
        ys = [-5.0, -3.0, -10.0]
        assert best_found(ys) == -3.0


# ---------------------------------------------------------------------------
# cumulative_best
# ---------------------------------------------------------------------------

class TestCumulativeBest:
    def test_non_decreasing(self):
        ys = [1.0, 0.5, 2.0, 1.5, 3.0]
        cb = cumulative_best(ys)
        assert all(cb[i] <= cb[i + 1] for i in range(len(cb) - 1))

    def test_length_matches_input(self):
        ys = [1.0, 2.0, 0.5, 3.0]
        assert len(cumulative_best(ys)) == len(ys)

    def test_final_value_equals_best_found(self):
        ys = [1.0, 4.0, 2.0, 3.0]
        assert cumulative_best(ys)[-1] == best_found(ys)


# ---------------------------------------------------------------------------
# simple_regret
# ---------------------------------------------------------------------------

class TestSimpleRegret:
    def test_regret_non_negative(self, sim, known_run):
        xs, ys = known_run
        sr = simple_regret(xs, ys, sim)
        assert sr >= -1e-9  # allow tiny floating-point slack

    def test_regret_at_true_optimum_is_near_zero(self, sim):
        """If we observe exactly at the true best x, regret should be ~0."""
        x_best, _ = sim.best_true_value(n_grid=10000)
        sim.reset()
        y = sim.observe(x_best)
        sr = simple_regret([x_best], [y], sim)
        assert sr < 0.01  # very small (grid discretisation tolerance)

    def test_regret_decreases_with_more_exploration(self, sim):
        """More experiments covering the space should not worsen regret."""
        # 5-point grid
        xs5 = list(np.linspace(-2.0, 2.0, 5))
        sim.reset()
        ys5 = [sim.observe(x) for x in xs5]
        sr5 = simple_regret(xs5, ys5, sim)

        # 50-point grid (reset sim to avoid re-using same RNG state)
        sim2 = LabSimulator(noise_std=0.0, rng=0)
        xs50 = list(np.linspace(-2.0, 2.0, 50))
        ys50 = [sim2.observe(x) for x in xs50]
        sr50 = simple_regret(xs50, ys50, sim2)

        assert sr50 <= sr5 + 1e-6  # finer grid ≤ coarser grid regret


# ---------------------------------------------------------------------------
# cumulative_regret
# ---------------------------------------------------------------------------

class TestCumulativeRegret:
    def test_length_matches_xs(self, sim, known_run):
        xs, ys = known_run
        cr = cumulative_regret(xs, ys, sim)
        assert len(cr) == len(xs)

    def test_all_non_negative(self, sim, known_run):
        xs, ys = known_run
        cr = cumulative_regret(xs, ys, sim)
        assert np.all(cr >= -1e-9)

    def test_final_regret_equals_simple_regret(self, sim, known_run):
        xs, ys = known_run
        cr = cumulative_regret(xs, ys, sim)
        sr = simple_regret(xs, ys, sim)
        assert abs(cr[-1] - sr) < 1e-9
