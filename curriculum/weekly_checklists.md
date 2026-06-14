# Weekly Checklists — "If You Only Do 3 Things This Week"

These are your minimum-viable learning tasks.  They take 2–3 hours each week.
Do them before everything else in the 4-week plan.

---

## Week 1 · Experimental Design

- [ ] **Watch / read:** Khan Academy "Designing Studies" (just the first 3 videos)
- [ ] **Define in your own words:** control, confounder, statistical power
- [ ] **Apply it:** Pick a headline ("Coffee reduces cancer risk by 20%") and list
      two plausible confounders that could explain the result without any causal link.

---

## Week 2 · Bayesian Thinking

- [ ] **Watch:** 3Blue1Brown Bayes video (15 min) — write down the formula on paper
- [ ] **Play:** Drag the sliders at seeing-theory.brown.edu for 20 minutes
- [ ] **Code:** Open a Python REPL and simulate a Beta(1,1) prior updated with 5
      coin flips (all heads):
      ```python
      from scipy.stats import beta
      import matplotlib.pyplot as plt
      import numpy as np
      x = np.linspace(0, 1, 200)
      # Prior: Beta(1,1)  After 5 heads: Beta(1+5, 1+0) = Beta(6,1)
      plt.plot(x, beta.pdf(x, 6, 1)); plt.show()
      ```

---

## Week 3 · Optimization & Explore/Exploit

- [ ] **Read:** Lilian Weng's Multi-Armed Bandit post — just the ε-greedy and UCB sections
- [ ] **Run:** `python -m notebooks` or open `notebooks/walkthrough.ipynb` and
      execute all cells
- [ ] **Experiment:** Change `kappa` from 0 to 5 in `BayesianStrategy` and note how
      the learning curve changes.  Which kappa finds the optimum fastest?

---

## Week 4 · Reproducibility + Synthesis

- [ ] **Read:** The Turing Way "Reproducible Research" intro page (20 min)
- [ ] **Verify:** Run `pytest` in the project root — all 24 tests should pass
- [ ] **Extend:** Pick one "Next 2 upgrades" suggestion from the README and implement
      it; confirm you get identical results by re-running with the same seed
