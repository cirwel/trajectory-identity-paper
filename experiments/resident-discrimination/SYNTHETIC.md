# Synthetic reproducibility artifact

`synthesize.py` → `synthetic_states.csv` (releasable; **no production rows**) +
`fig7_synthetic_check.png`.

## What it is
A per-agent VAR(1) model fit to each resident's real (E,I,S,V,φ) series, then
simulated to a synthetic series of the same length. VAR(1) preserves exactly the
structure the reduced signature reads — mean, contemporaneous covariance
(→ std + inter-dim correlation), and lag-1 autocovariance (→ autocorrelation.
Moment fidelity is tight: per-agent mean Δ ≈ 0.01, std Δ ≈ 0.005, ar1 matched to
~0.02.

## What it is FOR
Letting a reviewer **re-run the §6.5 pipeline on data we can release**, and
confirming the *qualitative* findings:
- discrimination works (synthetic software-subset ≈ 92% ≫ chance 33%);
- the similarity primitive runs as described;
- the §4.1 ordering holds (equal ≥ Fisher).

## What it is NOT — read this before citing it
- **It does not reproduce the empirical numbers.** Synthetic discrimination
  (~92%) is *higher* than the real result (60%, §6.5) because VAR(1) is unimodal
  and Gaussian: it strips the multimodality and cross-agent overlap visible in the
  real densities (compare `fig7` to `fig1b`). The clean model makes the agents
  *easier* to tell apart than they are in production. The headline number and its
  p-value stay anchored to the private production data.
- **The §4.1 gap is understated by it.** On real data equal beats Fisher 60→32;
  on synthetic only 92→88. The reversal is real but starker in reality.
- **It is not tuned to match the real numbers.** That would be fitting the artifact
  to a target — a dishonesty. We keep the principled model and report the gap.

So: a *pipeline-and-structure* reproducibility aid on releasable data, with an
explicit, stated idealization gap. Independent validation still requires
real data from independent operators (§6.5 limitations).

## Transfers to Wang 2026c
The same distribution-preserving recipe (fit a model that preserves the
statistics the analysis reads; simulate; ship synthetic + code; state the
idealization gap) is the artifact the digital-proprioception paper needs for its
self-cited 28.9% basin-flip counterfactual. One pattern, both papers.
