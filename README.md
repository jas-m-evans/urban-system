# Autonomous-Science Toy Lab

A beginner-friendly Python project for learning the foundations of automated
experimentation: experimental design, Bayesian inference, and optimization.

The mini-project simulates a **toy lab** with a hidden response function.
You run "experiments" (noisy measurements) and compare three search strategies:
random search, grid search, and Bayesian optimization.

---

## Table of Contents

- [Concept overview](#concept-overview)
- [Setup](#setup)
- [Project structure](#project-structure)
- [How to run experiments](#how-to-run-experiments)
- [How to interpret the plots](#how-to-interpret-the-plots)
- [Running tests](#running-tests)
- [Expected outputs](#expected-outputs)
- [Suggested extensions](#suggested-extensions)
- [4-week learning curriculum](#4-week-learning-curriculum)

---

## Concept overview

Imagine you are a scientist tuning the temperature of a chemical reaction.
The reaction yield changes with temperature, but your measurement instrument
is noisy — every reading has a random error.  You have a budget of 30
experiments.  **How do you find the best temperature?**

Three strategies are compared:

| Strategy | How it works | When it wins |
|----------|-------------|-------------|
| **Random** | Picks uniformly random temperatures | Simple baseline; surprisingly decent |
| **Grid** | Sweeps evenly from min to max | Good when budget is large relative to space |
| **Bayesian** | Builds a probabilistic model (GP), picks the next point with highest UCB | Finds the optimum with fewer experiments |

The Bayesian strategy is the heart of modern **automated experimentation**
(also called Bayesian Optimization).  After each experiment it updates its
*posterior belief* about the response function and uses that belief to decide
where to experiment next.  This is the explore/exploit trade-off in action.

---

## Setup

```bash
# 1. Clone the repo (if you haven't already)
git clone <repo-url>
cd urban-system

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Project structure

```
urban-system/
├── README.md
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── simulator.py    # Hidden response function + noisy observations
│   ├── strategies.py   # Random, Grid, and Bayesian search strategies
│   ├── metrics.py      # best_found, simple_regret, cumulative_best
│   └── plots.py        # Learning curves, GP posterior, uncertainty bands
│
├── notebooks/
│   └── walkthrough.ipynb   # End-to-end tutorial notebook
│
├── tests/
│   ├── test_simulator.py   # Noise, reproducibility, history tests
│   └── test_metrics.py     # Metric correctness tests
│
└── curriculum/
    ├── 4_week_plan.md        # 4-week reading plan (8–10 h/week)
    ├── reading_list.md       # Curated resources with links and difficulty tags
    ├── cheat_sheet.md        # One-page summary of key concepts
    └── weekly_checklists.md  # "If you only do 3 things this week" checklists
```

---

## How to run experiments

### Option A: Jupyter notebook (recommended for learning)

```bash
jupyter notebook notebooks/walkthrough.ipynb
```

Run cells top-to-bottom with **Shift+Enter**.  The notebook shows plots inline
and explains each step.

### Option B: Quick Python script

```python
from src.simulator  import LabSimulator
from src.strategies import RandomStrategy, GridStrategy, BayesianStrategy
from src.metrics    import summarise
from src.plots      import plot_learning_curves
import matplotlib.pyplot as plt

# Create the simulator (fixed seed → reproducible noise)
sim = LabSimulator(noise_std=0.12, bounds=(-2.0, 2.0), rng=42)

results = {}

for StrategyClass, name, kwargs in [
    (RandomStrategy,   'Random',   {'seed': 0}),
    (GridStrategy,     'Grid',     {}),
    (BayesianStrategy, 'Bayesian', {'n_init': 5, 'kappa': 2.0, 'seed': 0}),
]:
    sim.reset()
    strat = StrategyClass(sim, n_experiments=30, **kwargs)
    xs, ys = strat.run()
    results[name] = (xs, ys)

summarise(results, sim)
fig = plot_learning_curves(results, sim)
plt.show()
```

### Option C: Sanity-check script

```bash
python -c "
from src.simulator import LabSimulator
from src.strategies import RandomStrategy, GridStrategy, BayesianStrategy
from src.metrics import summarise

sim = LabSimulator(noise_std=0.1, rng=42)
results = {}
for Cls, name, kw in [
    (RandomStrategy,   'Random',   {'seed': 0}),
    (GridStrategy,     'Grid',     {}),
    (BayesianStrategy, 'Bayesian', {'n_init': 5, 'seed': 0}),
]:
    sim.reset()
    results[name] = Cls(sim, n_experiments=30, **kw).run()
summarise(results, sim)
"
```

---

## How to interpret the plots

### Learning curve (left panel)
The y-axis shows the **best observation found so far** after each experiment.
A strategy that rises quickly is efficient — it found good regions early.

- **Flat line** → the strategy is not learning; random chance or stuck in a valley.
- **Steep early rise** → smart exploration found the peak quickly.
- **Dashed horizontal line** → the true global optimum (ground truth).

### Regret curve (right panel)
**Simple regret** = true_optimum − true_value_at_our_best_guess.
Lower is better; 0 means you found the exact optimum.

A strategy with quickly-falling regret learns fast.

### GP posterior snapshots
Green line = GP mean estimate of f(x).
Green shaded band = ±2σ uncertainty.
Dashed black = true f(x) (hidden in real life).
Orange dots = experiments run so far.

Wide bands → "I don't know what's here".
Narrow bands near the peak → "I've sampled here a lot; I'm confident".

---

## Running tests

```bash
pytest tests/ -v
```

Expected output: **24 passed**.

Tests cover:
- Noise distribution (mean ≈ 0, std ≈ noise_std over 2000 samples)
- Reproducibility (same seed → same observations)
- History recording and reset
- `best_found`, `cumulative_best`, `simple_regret`, `cumulative_regret` correctness

---

## Expected outputs

Running the quick script above should print something like:

```
Strategy          Best found   Simple regret   # experiments
------------------------------------------------------------
Random                0.98          0.14              30
Grid                  1.15          0.05              30
Bayesian              1.07          0.01              30

True optimum: 1.1196
```

Exact numbers will vary slightly depending on the Python/numpy version, but
Bayesian should consistently have the lowest simple regret.

---

## Suggested extensions

1. **2-D parameter space** — swap `response_1d_multimodal` for
   `response_2d_gaussian_mixture` and update strategies to handle 2-D inputs.

2. **Thompson Sampling** — implement a fourth strategy that, at each step,
   draws a sample from the GP posterior and picks its argmax.  Compare to UCB.

3. **Expected Improvement (EI)** — replace UCB acquisition with EI:
   `EI(x) = E[max(0, f(x) - f_best)]`.  Often converges faster.

4. **Multiple runs + confidence bands** — run each strategy 20 times with
   different seeds and plot mean ± std learning curves.

5. **Noisy Bayesian Optimization** — tell the GP the exact noise variance
   (`alpha=noise_std**2` in `GaussianProcessRegressor`) so it doesn't try to
   interpolate through noise.

6. **Cost-aware search** — give different "costs" to different x values
   (maybe high temperatures cost more) and compare strategies by
   cost-adjusted regret.

---

## 4-week learning curriculum

See [`curriculum/`](curriculum/) for:

- [`4_week_plan.md`](curriculum/4_week_plan.md) — weekly reading plan with
  time estimates and learning goals
- [`reading_list.md`](curriculum/reading_list.md) — curated resources with
  links, difficulty tags (🟢 Easy / 🟡 Medium / 🔴 Deep), and "why bother" notes
- [`cheat_sheet.md`](curriculum/cheat_sheet.md) — one-page summary of
  controls/confounders, posterior intuition, credible vs. confidence intervals,
  and exploration vs. exploitation
- [`weekly_checklists.md`](curriculum/weekly_checklists.md) — "if you only
  do 3 things this week" minimal-viable checklists
