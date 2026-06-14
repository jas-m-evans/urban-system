# Curated Reading List

All resources are free unless noted.  Difficulty labels: 🟢 Easy · 🟡 Medium · 🔴 Deep.

---

## Experimental Design (3 core resources)

| # | Title & Link | Format | Difficulty | Time | Note |
|---|-------------|--------|-----------|------|------|
| 1 | [Khan Academy: Designing Studies](https://www.khanacademy.org/math/statistics-probability/designing-studies) | Video + exercises | 🟢 | 90 min | Best no-jargon intro to controls, randomisation, and sampling. Exercises help cement ideas. |
| 2 | [Daniel Lakens — Statistical Power (interactive)](https://lakens.github.io/statistical_inferences/02-power.html) | Interactive web | 🟡 | 60 min | Move a slider and watch power change. Explains effect size, sample size, α in a coherent picture. |
| 3 | [Calling Bullshit — The Basics of Bullshit](https://www.callingbullshit.org/notes.html) | Web essay | 🟢 | 30 min | Written by two professors for the general public. Hilarious real examples of confounded studies. |
| ⭐4 | [Hernán & Robins "Causal Inference: What If" Ch. 1–2](https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/) | Textbook chapter | 🔴 | 90 min | The cleanest formal treatment of confounding available. Free PDF. |
| ⭐5 | [Simply Statistics blog — Replication Crisis](https://simplystatistics.org/posts/2012-06-19-blog-post/) | Blog post | 🟢 | 20 min | Short and cutting; immunises you against p-hacking traps. |

---

## Bayesian Thinking + Credible Intervals (3 core resources)

| # | Title & Link | Format | Difficulty | Time | Note |
|---|-------------|--------|-----------|------|------|
| 1 | [3Blue1Brown — Bayes' theorem (YouTube)](https://www.youtube.com/watch?v=HZGCoVF3YvM) | Video | 🟢 | 15 min | Perfect geometric intuition. Watch before reading anything else on Bayes. |
| 2 | [Seeing Theory — Bayesian Inference (interactive)](https://seeing-theory.brown.edu/bayesian-inference/index.html) | Interactive visual | 🟢 | 45 min | Drag sliders for prior/likelihood; posterior updates live. No equations required. |
| 3 | [Probabilistic Programming & Bayesian Methods for Hackers — Ch. 1](https://nbviewer.org/github/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/blob/master/Chapter1_Introduction/Ch1_Introduction_PyMC.ipynb) | Jupyter notebook | 🟡 | 90 min | Code-first approach. Coin flips become priors; MCMC sampling becomes intuitive. |
| ⭐4 | [StatQuest: Credible Intervals (YouTube)](https://www.youtube.com/watch?v=2-BsVz38Xzk) | Video | 🟢 | 12 min | Clearest side-by-side explanation of Bayesian vs. frequentist intervals. |
| ⭐5 | [Gelman et al. "Bayesian Data Analysis" 3e Ch. 1 (free)](http://www.stat.columbia.edu/~gelman/book/) | Textbook chapter | 🔴 | 2 hr | The canonical graduate text; Ch. 1 is surprisingly gentle and motivating. |

---

## Optimization + Explore/Exploit (3 core resources)

| # | Title & Link | Format | Difficulty | Time | Note |
|---|-------------|--------|-----------|------|------|
| 1 | [Distill — "Why Momentum Really Works"](https://distill.pub/2017/momentum/) | Interactive essay | 🟡 | 45 min | The best visual explanation of gradient methods. Loss landscape animations make it click. |
| 2 | [Lilian Weng — Multi-Armed Bandit](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/) | Blog post | 🟡 | 60 min | Thorough treatment of ε-greedy, UCB, Thompson Sampling with pseudocode. The explore/exploit bible. |
| 3 | [Martin Krasser — Bayesian Optimization](https://krasserm.github.io/2018/03/21/bayesian-optimization/) | Blog + notebook | 🟡 | 90 min | Code-first BO tutorial. Directly mirrors what this repo's BayesianStrategy does. |
| ⭐4 | [Andrej Karpathy — Recipe for Training NNs](http://karpathy.github.io/2019/04/25/recipe/) | Blog post | 🟡 | 40 min | Practical wisdom on exploring hyperparameters without losing your mind. |
| ⭐5 | [Garnett "Bayesian Optimization" textbook (free)](https://bayesoptbook.com/) | Textbook | 🔴 | 2 hr | The modern reference. Ch. 1–2 give rigorous foundations behind this repo's Bayesian strategy. |

---

## Reproducibility in Computational Experiments (2 core resources)

| # | Title & Link | Format | Difficulty | Time | Note |
|---|-------------|--------|-----------|------|------|
| 1 | [The Turing Way — Reproducible Research](https://the-turing-way.netlify.app/reproducible-research/reproducible-research.html) | Web book | 🟢 | 45 min | Community-maintained guide. Covers seeds, environments, version control. Friendly tone. |
| 2 | [Joelle Pineau — NeurIPS 2021 Reproducibility Talk](https://www.youtube.com/watch?v=Vh4H0gOwdIg) | Video | 🟢 | 20 min | The researcher who introduced the ML reproducibility checklist explains why it matters. |
| ⭐3 | [Papers with Code Reproducibility Challenge overview](https://paperswithcode.com/rc2020) | Web essay | 🟢 | 20 min | Shows how often published results can't be reproduced and what breaks. |
| ⭐4 | [Sculley et al. — Hidden Technical Debt in ML Systems (PDF)](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf) | Research paper | 🔴 | 90 min | Classic paper. Sobering but important for anyone running repeated experiments at scale. |

---

## Quick reference: reading order if you only have 5 hours total

1. Calling Bullshit (30 min) — why this matters
2. Khan Academy Designing Studies (60 min) — core vocabulary
3. 3Blue1Brown Bayes (15 min) — the single best intuition-builder
4. Seeing Theory interactive (30 min) — posterior hands-on
5. Lilian Weng Multi-Armed Bandit (60 min) — explore/exploit
6. Martin Krasser Bayesian Optimization (60 min) — exactly what this repo does
7. Turing Way Reproducibility (45 min) — how not to fool yourself
