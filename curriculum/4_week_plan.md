# 4-Week Autonomous-Science Learning Sprint

**Goal:** Build a practical foundation in experimental design, Bayesian
inference, and optimization — enough to understand and extend the mini-project
in this repo, and to hold your own in conversations about automated
experimentation.

**Pace:** ~8–10 hours per week.  Readings marked 🚀 are the "do these first"
items; ⭐ are "if you have extra time".

---

## Week 1 — Experimental Design: Controls, Confounders & Power

**Learning goals:**
- Understand what a controlled experiment is, and why randomisation matters.
- Identify confounders and explain how they distort results.
- Explain statistical power in plain English.
- Understand measurement uncertainty and why noise is not the enemy.

| # | Resource | Format | Difficulty | Est. time | Why bother |
|---|----------|--------|-----------|-----------|------------|
| 🚀1 | [Calling Bullshit — Ch. 1 "The Basics of Bullshit" (free online)](https://www.callingbullshit.org/notes.html) | Web essay | Easy | 30 min | Brilliant framing of why experiments fool us; funny examples |
| 🚀2 | [Khan Academy: Experimental Design](https://www.khanacademy.org/math/statistics-probability/designing-studies) | Video + exercises | Easy | 90 min | Controls/confounders/random assignment explained with care |
| 🚀3 | [Statistical Power — "What Is Power?" by Daniel Lakens](https://lakens.github.io/statistical_inferences/02-power.html) | Interactive web | Medium | 60 min | Best plain-English treatment of power; interactive simulations |
| ⭐4 | [Common Statistical Fallacies — Simply Statistics blog](https://simplystatistics.org/posts/2012-06-19-blog-post/) | Blog post | Easy | 20 min | Short and funny; inoculates against p-hacking |
| ⭐5 | [Hernán & Robins "Causal Inference: What If" Ch. 1–2 (free PDF)](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/) | Textbook chapter | Deep | 90 min | The cleanest formal treatment of confounding; optional |

**Weekly mini-challenge:** Look at any claim ("This drug reduces cholesterol by
10%") and identify: What is the control?  What could be confounders?  How many
subjects would give 80% power?

---

## Week 2 — Probability & Bayesian Thinking

**Learning goals:**
- Update beliefs with Bayes' theorem (prior → posterior).
- Understand credible intervals vs. confidence intervals intuitively.
- Read a posterior distribution and say what it means.
- Simulate a simple Beta-Binomial update by hand.

| # | Resource | Format | Difficulty | Est. time | Why bother |
|---|----------|--------|-----------|-----------|------------|
| 🚀1 | [3Blue1Brown — "Bayes theorem, the geometry of changing beliefs"](https://www.youtube.com/watch?v=HZGCoVF3YvM) | Video (15 min) | Easy | 15 min | Best visual intuition for Bayes; watch it twice |
| 🚀2 | [Seeing Theory — Chapter 3 "Bayesian Inference"](https://seeing-theory.brown.edu/bayesian-inference/index.html) | Interactive visual | Easy | 45 min | Click and drag prior sliders; instant intuition |
| 🚀3 | ["Probabilistic Programming & Bayesian Methods for Hackers" Ch. 1](https://nbviewer.org/github/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/blob/master/Chapter1_Introduction/Ch1_Introduction_PyMC.ipynb) | Jupyter notebook | Medium | 90 min | Code-first; uses coin-flipping analogies throughout |
| ⭐4 | [StatQuest: "Credible Intervals"](https://www.youtube.com/watch?v=2-BsVz38Xzk) | Video (12 min) | Easy | 12 min | Clearest side-by-side with frequentist CI |
| ⭐5 | [Gelman et al. "Bayesian Data Analysis" 3rd ed. Ch. 1 (free PDF)](http://www.stat.columbia.edu/~gelman/book/) | Textbook chapter | Deep | 2 hr | The canonical reference; Ch. 1 is surprisingly readable |

**Weekly mini-challenge:** Simulate the coin-flip example from resource 3 in a
notebook.  Start with a flat prior (Beta(1,1)), flip 10 heads in a row, and
plot how the posterior sharpens.

---

## Week 3 — Optimization: Gradient Methods, Black-Box Search & Explore/Exploit

**Learning goals:**
- Explain why gradient descent works and when it fails.
- Understand black-box (derivative-free) optimization.
- Articulate the exploration–exploitation trade-off with a real analogy.
- Describe the multi-armed bandit problem and at least one solution.

| # | Resource | Format | Difficulty | Est. time | Why bother |
|---|----------|--------|-----------|-----------|------------|
| 🚀1 | [Distill.pub — "Why Momentum Really Works"](https://distill.pub/2017/momentum/) | Interactive essay | Easy/Medium | 45 min | Best visual explanation of gradient-based methods |
| 🚀2 | [Lilian Weng — "The Multi-Armed Bandit Problem and Its Solutions"](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/) | Blog post | Medium | 60 min | Thorough walkthrough of ε-greedy, UCB, Thompson Sampling |
| 🚀3 | [Martin Krasser — "Bayesian Optimization" blog post](https://krasserm.github.io/2018/03/21/bayesian-optimization/) | Blog + notebook | Medium | 90 min | Code-first; exactly what the mini-project implements |
| ⭐4 | [Andrej Karpathy — "A Recipe for Training Neural Networks"](http://karpathy.github.io/2019/04/25/recipe/) | Blog post | Medium | 40 min | Practical exploration/exploitation wisdom from someone who's done it a lot |
| ⭐5 | [Garnett "Bayesian Optimization" textbook Ch. 1–2 (free PDF)](https://bayesoptbook.com/) | Textbook chapter | Deep | 2 hr | The cleanest modern treatment of BO; Ch. 1 is gentle |

**Weekly mini-challenge:** Open the mini-project notebook in this repo, run all
three strategies, and try changing the `kappa` parameter in BayesianStrategy.
What happens when kappa=0 (pure exploitation)?  When kappa=10 (wild exploration)?

---

## Week 4 — Reproducibility & Putting It All Together

**Learning goals:**
- Understand what makes a computational experiment reproducible.
- Apply random seeds and environment pinning in your own projects.
- Synthesise Weeks 1–3: design an experiment, run it, interpret results.
- Extend the mini-project with one of the suggested upgrades.

| # | Resource | Format | Difficulty | Est. time | Why bother |
|---|----------|--------|-----------|-----------|------------|
| 🚀1 | [The Turing Way — "Reproducible Research"](https://the-turing-way.netlify.app/reproducible-research/reproducible-research.html) | Web book chapter | Easy | 45 min | Friendly, comprehensive; great on seeds + environments |
| 🚀2 | [Papers with Code — "Reproducibility Crisis in ML"](https://paperswithcode.com/rc2020) | Web essay | Easy | 20 min | Motivates why reproducibility matters with concrete examples |
| 🚀3 | [Joelle Pineau — NeurIPS 2021 Reproducibility Checklist Talk](https://www.youtube.com/watch?v=Vh4H0gOwdIg) | Video (20 min) | Easy | 20 min | Practical checklist from the researcher who pushed this culture |
| ⭐4 | [Gundersen & Kjensmo "State of the Art: Reproducibility in AI" (arXiv)](https://arxiv.org/abs/1810.03673) | Research paper | Medium | 60 min | Survey of what actually breaks; sobering and actionable |
| ⭐5 | [Sculley et al. "Hidden Technical Debt in ML Systems" (NIPS 2015)](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf) | Research paper | Deep | 90 min | Classic paper on what goes wrong at scale; eye-opening |

**Weekly mini-challenge:** Add one "upgrade" to the mini-project (see README
for suggestions), write a short note explaining what changed, and confirm your
results are identical when you rerun with the same seed.

---

## Total reading-time estimate

| Week | Core (🚀) | Optional (⭐) | Total range |
|------|-----------|--------------|-------------|
| 1    | ~3.5 hr   | ~2 hr        | 3.5–5.5 hr  |
| 2    | ~2.5 hr   | ~2 hr        | 2.5–4.5 hr  |
| 3    | ~3 hr     | ~2.5 hr      | 3–5.5 hr    |
| 4    | ~1.5 hr   | ~2.5 hr      | 1.5–4 hr    |

The remaining time each week is for the mini-challenges and code exploration.
