# One-Page Cheat Sheet: Autonomous-Science Foundations

---

## 1 · Controls, Confounders & Power

| Concept | Plain-English meaning | Real-world example |
|---------|----------------------|-------------------|
| **Control** | The group/condition kept identical to the experiment group in every way except the one thing you're testing. | Drug trial: placebo group is the control. |
| **Confounder** | A hidden variable that affects both the "treatment" and the "outcome", making it look like they're connected when they might not be. | Ice cream sales and drowning both rise in summer; heat is the confounder. |
| **Randomisation** | Randomly assign units to treatment/control so confounders balance out on average across groups. | Random split of website users into A (old design) and B (new design). |
| **Statistical power** | Probability of detecting a real effect if one exists. Power = 1 − β (β = false-negative rate). | "80% power" means 8 out of 10 well-run experiments will find the effect if it's real. |
| **Effect size** | How big the difference actually is, in standardised units (e.g., Cohen's d). | Small effect → need many experiments; large effect → fewer. |
| **Measurement noise** | Random variability in your instrument. Unavoidable but manageable via replication. | Weighing a compound: read 10.01 g, 9.99 g, 10.02 g — noise is ~0.01 g. |

**Rule of thumb for sample size:** n ≈ 16/δ² per group for 80% power, where δ = effect size (Cohen's d).

---

## 2 · Posterior Intuition

Bayes' theorem in words:

> **Posterior ∝ Likelihood × Prior**

| Term | What it represents |
|------|--------------------|
| **Prior** | What you believed before seeing data. Can be vague ("any value is plausible") or informed ("we expect the peak near x=1"). |
| **Likelihood** | How probable the data you observed is, given a particular hypothesis. |
| **Posterior** | Your updated belief after combining prior knowledge with new data. |
| **Posterior update** | Each new experiment narrows the posterior — uncertainty shrinks as evidence accumulates. |

**Analogy:** You start with a blurry photo of a suspect (prior). Each witness
description (likelihood) sharpens the image. After many witnesses you have a
clear picture (posterior).

---

## 3 · Credible Intervals vs. Confidence Intervals

| | Bayesian Credible Interval | Frequentist Confidence Interval |
|--|---------------------------|----------------------------------|
| **Meaning** | "There's a 95% probability that the true value lies in this interval" (given the data and prior). | "If we repeated the experiment many times, 95% of intervals constructed this way would contain the true value." |
| **Statement about** | The parameter (probability) | The procedure (frequency) |
| **Intuition** | ✅ What you actually want to say | ⚠️ Often misquoted as the Bayesian meaning |
| **Requires prior?** | Yes | No |
| **Width shrinks with** | More data AND tighter prior | More data only |

**Key point:** A 95% credible interval *is* a probability statement about the
parameter.  A 95% confidence interval is *not* — it's a statement about the
long-run behaviour of the procedure.

---

## 4 · Exploration vs. Exploitation

**The dilemma:** You have a limited budget of experiments.  Do you:
- **Exploit** — keep testing the setting that looks best so far?
- **Explore** — probe uncertain regions in case something better is hiding there?

| Strategy | Behaviour | Risk |
|----------|-----------|------|
| Pure exploit | Always pick current best | Miss a better region you never visited |
| Pure explore | Try everything uniformly | Waste budget on obviously bad regions |
| ε-greedy | Exploit most of the time, random probe with probability ε | Crude but often good enough |
| UCB (Upper Confidence Bound) | Pick x with highest μ(x) + κ·σ(x) | κ tunes explore/exploit; κ=0 is pure exploit |
| Thompson Sampling | Sample a function from the posterior, then pick its argmax | Elegant; naturally balances exploration |

**Regret** = cumulative gap between the true optimum and what you actually
observed.  Good algorithms have *sublinear* regret — the per-experiment gap
shrinks over time.

**Analogy:** Choosing a restaurant in a new city.  Yelp rating = μ (exploit).
"Only 2 reviews" = high σ (explore).  UCB says: go to the place with the best
(rating + confidence_bonus).

---

## Quick formula card

```
Bayes:          P(θ|data) ∝ P(data|θ) · P(θ)
GP posterior:   μ(x*) = k(x*,X)[K(X,X)+σ²I]⁻¹ y
UCB:            acq(x) = μ(x) + κ·σ(x)
Simple regret:  r_T = f* − f(x_T)  where x_T = argmax_{t≤T} y_t
Power (approx): n ≈ 16/δ²  per group for α=0.05, power=0.80
```
