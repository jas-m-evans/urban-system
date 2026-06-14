"""
test_simulator.py — Checks that the LabSimulator behaves correctly.

Covers:
  - Noise distribution (mean ≈ 0, std ≈ noise_std over many samples)
  - Reproducibility with fixed seeds
  - History recording
  - True-value and best-true-value helpers
"""

import numpy as np
import pytest

from src.simulator import LabSimulator, response_1d_multimodal, response_2d_gaussian_mixture


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sim():
    """Default 1-D simulator with fixed seed."""
    return LabSimulator(noise_std=0.1, bounds=(-2.0, 2.0), rng=0)


# ---------------------------------------------------------------------------
# Noise behaviour
# ---------------------------------------------------------------------------

class TestNoiseBehaviour:
    def test_noise_mean_near_zero(self, sim):
        """Over many observations, noise should average out to roughly zero."""
        true_val = sim.true_value(0.0)
        n = 2000
        observations = [sim.observe(0.0) for _ in range(n)]
        sample_mean = np.mean(observations)
        # Expect |mean - true_val| < 3 * (noise_std / sqrt(n))
        tolerance = 3 * sim.noise_std / np.sqrt(n)
        assert abs(sample_mean - true_val) < tolerance, (
            f"Expected sample mean ≈ {true_val:.4f}, got {sample_mean:.4f} "
            f"(tolerance ±{tolerance:.4f})"
        )

    def test_noise_std_close_to_specified(self, sim):
        """Observed noise standard deviation should be close to noise_std."""
        true_val = sim.true_value(0.5)
        n = 2000
        observations = [sim.observe(0.5) for _ in range(n)]
        sample_std = np.std([o - true_val for o in observations])
        assert abs(sample_std - sim.noise_std) < 0.01, (
            f"Expected std ≈ {sim.noise_std}, got {sample_std:.4f}"
        )

    def test_zero_noise_returns_true_value(self):
        """A noiseless simulator should return exact true values."""
        sim_noiseless = LabSimulator(noise_std=0.0, rng=7)
        x = 1.23
        for _ in range(5):
            obs = sim_noiseless.observe(x)
            assert abs(obs - sim_noiseless.true_value(x)) < 1e-12


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------

class TestReproducibility:
    def test_same_seed_same_observations(self):
        """Two simulators with identical seeds produce identical results."""
        sim1 = LabSimulator(noise_std=0.2, rng=42)
        sim2 = LabSimulator(noise_std=0.2, rng=42)
        xs = [-1.0, 0.0, 0.5, 1.5]
        for x in xs:
            assert sim1.observe(x) == sim2.observe(x)

    def test_different_seeds_differ(self):
        """Different seeds should (almost certainly) produce different noise."""
        sim1 = LabSimulator(rng=1)
        sim2 = LabSimulator(rng=2)
        obs1 = sim1.observe(0.0)
        obs2 = sim2.observe(0.0)
        assert obs1 != obs2


# ---------------------------------------------------------------------------
# History recording
# ---------------------------------------------------------------------------

class TestHistory:
    def test_history_grows_with_observations(self, sim):
        for i in range(5):
            sim.observe(float(i) * 0.1)
        assert len(sim.history) == 5

    def test_history_stores_correct_x(self, sim):
        x_val = 0.777
        sim.observe(x_val)
        assert sim.history[-1][0] == x_val

    def test_reset_clears_history(self, sim):
        sim.observe(0.0)
        sim.observe(1.0)
        sim.reset()
        assert len(sim.history) == 0


# ---------------------------------------------------------------------------
# True value and best-true-value
# ---------------------------------------------------------------------------

class TestTrueValues:
    def test_true_value_matches_function(self, sim):
        for x in [-1.5, 0.0, 1.0]:
            assert np.isclose(sim.true_value(x), response_1d_multimodal(x))

    def test_best_true_value_returns_tuple(self, sim):
        result = sim.best_true_value()
        assert isinstance(result, tuple) and len(result) == 2

    def test_best_true_value_is_global_max(self, sim):
        x_best, f_best = sim.best_true_value(n_grid=5000)
        # Check on a random sample that no point beats the claimed optimum
        rng = np.random.default_rng(0)
        xs_sample = rng.uniform(-2.0, 2.0, 500)
        for x in xs_sample:
            assert sim.true_value(x) <= f_best + 1e-3

    def test_2d_response_function(self):
        """2-D response function should return a scalar for a 2-element array."""
        val = response_2d_gaussian_mixture(np.array([0.3, 0.7]))
        assert isinstance(val, float)
        assert val > 0.9  # this point is near the first peak
