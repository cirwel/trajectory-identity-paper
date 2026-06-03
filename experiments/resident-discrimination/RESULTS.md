# Resident-discrimination pilot — results

**Date:** 2026-06-02 · **Scope:** N=4 resident agents, one operator's fleet,
governance EISV+phi state. A *within-ecosystem* pilot, not external validation.

## Question
The trajectory-identity framework (Wang 2026b) claims trajectory signatures can
**discriminate distinct agents**. v0.13 §6.4/§7.2/§8.3 flag this as untested
(single-agent data only). This pilot runs the first multi-agent discrimination
test on existing fleet telemetry.

## Data
`core.agent_state`, real (non-synthetic) rows, last 60 days, four dense
residents: Lumen (embodied, 21.3k check-ins), Sentinel (monitor, 12.9k),
Watcher (edit-hook, 4.3k), Vigil (cron, 2.4k). 40,929 rows, 0% null on E/phi.
State per check-in: `[E, I, S, V, phi]` (coherence dropped — degenerate ~0.49).
Reduced signature per window: α(mean+std) · ρ(lag-1 autocorr) · Δ(corr) = 25-D.
Held-out test uses a **temporal split** (train = each agent's earliest 70% by
time) to bar adjacent-window leakage and same-period memorization.

## Headline findings
1. **Discrimination is real and significant.** Equal-weight nearest-centroid
   (the similarity primitive): **4-way 71%** (perm-null 25%±13%, p<0.0001),
   **software-only 60%** (3 overlapping-marginal residents; p=0.012, 2000-shuffle
   null). Robust across window sizes (software ~52–60% for W=100–200). Per-agent
   recall: Lumen 81%, Watcher 78%, Sentinel 62%, Vigil 20% (Vigil N=5 test —
   too small to evaluate). The result is not carried by one agent.

2. **The similarity primitive works — better than a RandomForest.** Equal-weight
   centroid matching (71/60) beat RF (63/52). (An earlier silhouette ≈ 0 reading
   was *misleading*: agents have separable central tendencies despite high
   within-class window scatter, which silhouette penalizes but centroid-matching
   does not.)

3. **§4.1's weighting guidance is contradicted on this data.** The paper argues
   informativeness/Fisher weighting is the "principled fix" and demotes
   inverse-variance as "inadequate for multi-agent discrimination." Observed
   (W=150, software-only): equal **60%**, inv-within-var **57%**, sqrt-F **38%**,
   F (Fisher) **32% (≈chance)**. Fisher weighting *hurt*; inverse-variance ≈ equal.
   The opposite of the §4.1 prediction. This is exactly the test §4.1/§7.2 said
   needed multi-agent data, and it overturns the stated expectation.

4. **The signal is in variability/dynamics, not the rest point.** Top informative
   components: std_I, std_S, std_phi, mean_S, ar1_S — i.e. how *variable* an
   agent's integrity/entropy are, and entropy's autocorrelation, identify it more
   than its mean location. Supports "trajectory shape over snapshot."

## Honest caveats / what this does NOT establish
- **N=4, one ecosystem, one operator.** The silo critique stands: clean result,
  self-validated metrics. Does not substitute for an external agent population.
- **Governance EISV, not the paper's anima state.** The software residents have no
  sensors, so the shared substrate is EISV+phi — a different state space than the
  §6.4 Lumen validation. The paper would have to frame it as such.
- **Vigil under-powered** (11 windows). Drop or gather more before citing it.
- The §4.1 contradiction uses one operationalization of "Fisher informativeness"
  (sklearn `f_classif`). Worth confirming against the paper's exact intended
  estimator before asserting as a settled correction — but it is robust across
  F and sqrt-F.

## Files
`fetch.sql` (regenerates data; CSV gitignored — raw production rows) ·
`discriminate.py` (signature + within/between + RF) ·
`discriminate2.py` (window sweep + 3 discriminators + perm-null + top features) ·
`discriminate3.py` (weighting variants + perm-null on winner + per-agent recall) ·
figs 1–6.
