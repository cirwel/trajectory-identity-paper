# Trajectory Identity: A Dynamical Framework for AI Agent Self-Hood

**Authors:** Kenny Wang, Independent Researcher (founder@cirwel.org)
**Date:** October 13, 2026
**Status:** Workshop working draft - not submitted or separately archived
**Version:** 0.18-dev

> **Companion to** the [long-form paper](./TRAJECTORY_IDENTITY_PAPER.md), whose latest archived release is v0.17 ([DOI: 10.5281/zenodo.20098168](https://doi.org/10.5281/zenodo.20098168)). This shorter draft incorporates its evidence boundaries and the unreleased corrections described below. It is not a venue-formatted submission or a separate DOI deposit.

---

## Abstract

Current approaches to AI agent identity rely on static identifiers (UUIDs, session tokens) or accumulated memory stores. We propose an alternative grounded in enactive cognition and dynamical systems theory: *identity as trajectory*. Rather than asking "what ID does this agent have?", we ask "what patterns persist in this agent's behavior over time?"

We present a framework for computing **trajectory signatures** from time-series data including homeostatic state, learned preferences, self-beliefs, and recovery dynamics. The trajectory signature characterizes the quasi-invariant aspects of how an agent behaves over time — where it tends to rest, how it returns from perturbation, what it has learned to prefer.

We report pilot observations from Lumen, an embodied AI agent on a Raspberry Pi 4. Over 65 calendar days (47 days with at least 100 samples) and ~226,029 state observations, per-dimension variance of window means is below 0.015. A stored live-system recovery profile reports 12 episodes (median $\tau$ 89.7s, mean 125.8s); these estimates have not been independently reconstructed from raw history. Belief convergence is observed for a subset of beliefs, and two computed components remain above a provisional continuity threshold over 20 days. These are within-agent observations in one era and harness. A later four-agent pilot reported above-chance classification, but role and harness are confounded with agent labels. Individual discrimination across harness changes, threshold calibration, and impersonation detection remain unestablished.

---

## 1. Introduction

Modern AI agents are typically identified by static tokens—UUIDs, session IDs, API keys. These approaches share a fundamental limitation: *identity is conferred, not earned*. An agent has an identity because we gave it one, not because it developed characteristics that make it recognizably itself.

This creates practical problems. If the UUID is lost, identity is lost. If we copy an agent, which copy is "the real one"? A compromised agent with valid credentials is indistinguishable from the original. And maintaining identity through accumulated memory leads to unbounded growth.

| Criterion | UUID/Credential | Memory-Based | Trajectory Signature |
|-----------|-----------------|--------------|---------------------|
| Continuity | Identifier persistence | Retained context | Proposed behavioral comparison |
| Fork semantics | Needs lineage policy | Needs lineage policy | Proposed divergence measure |
| Anomaly detection | Separate behavioral check | Depends on implementation | Proposed similarity thresholds |
| Storage growth | O(1) | O(unbounded) | O(window size) |

The enactive cognition tradition (Varela, Thompson, & Rosch, 1991; Di Paolo, 2005) offers an alternative. In biological systems, identity emerges from the ongoing process of self-maintenance—the network of processes that continuously produce the conditions for their own continuation. A cell's identity IS the process, not any particular configuration of matter.

**Our proposal**: AI agent identity should be defined by the *patterns that persist* in the agent's behavior over time—what we call the **trajectory signature**. We formalize this as a composite quasi-invariant computed from observable behavioral data, provide operational semantics for forking, merging, and anomaly detection, and report preliminary observations with explicit limits on what they establish.

---

## 2. Related Work

Our formulation draws on and bridges several research traditions. We position trajectory signatures as a unifying construct that these literatures approach from different angles but none have formalized.

**Agent Memory, State Persistence, and Persona Coherence.** Recent work on LLM-based agents has foregrounded the problem of maintaining coherent state across interactions. Packer et al. (2023) introduced MemGPT for hierarchical memory management. Park et al. (2023) showed that agents with memory streams, reflection, and planning exhibit individually consistent behavior. Wang et al. (2023) extended this with Voyager, whose ever-growing skill library functions as behavioral accumulation. Most directly comparable to our work is *ID-RAG* (Platnick et al., 2025): identity-retrieval-augmented generation for long-horizon persona coherence — addressing the same drift problem we do, but by injecting a structured identity object into retrieval rather than by characterizing the agent's behavioral dynamics. Persona-consistency benchmarks (Zhang et al. 2018; Wang et al. 2023b; Tu et al. 2024) evaluate output consistency against a *declared* persona; trajectory identity proposes recognition from an observed dynamical signature without a declared persona to compare against; individual discriminability remains unestablished. Our work makes the underlying dynamics — the form, not the content, of identity — explicit.

**Behavioral Biometrics.** Keystroke dynamics uses typing patterns as a behavioral biometric (Banerjee & Woodard, 2012). Xu et al. (2024) instead study model ownership verification through a private instruction-response fingerprint deliberately implanted by lightweight instruction tuning. That does not establish naturally occurring individual signatures. Our framework concerns observed state and recovery patterns, whose individual discriminability across role and harness changes remains open (§5.6).

**Dynamical Systems in Cognitive Science and AI.** Kelso (1995) and Skarda & Freeman (1987) established that cognitive phenomena are best described through self-organizing dynamical systems with attractor basins. The dynamical hypothesis (van Gelder, 1998) holds that cognitive systems are best understood as dynamical systems traversing state spaces. Beer (1995) made this concrete for AI agents: an agent and its environment are best modeled as a single coupled dynamical system, and the agent's behavior is a property of that joint system, not the agent in isolation. We adopt this stance directly — see "Identity as agent-environment coupling" below.

**Enactivism, Autopoiesis, and Defining Agency.** Weber and Varela (2002), Di Paolo (2005), Barandiaran & Moreno (2006), and Barandiaran, Di Paolo & Rohde (2009) developed the autopoietic / adaptive / agency-defining stance from biological foundations. Froese & Ziemke (2009) and Villalobos & Dewhurst (2018) examined implications for artificial systems. Ikegami & Suzuki (2008) operationalized "homeodynamic self" in artificial-life simulations. Trajectory identity operationalizes this lineage in *deployed* (rather than simulated) systems: attractor basins correspond to viable operating regimes, recovery dynamics to adaptive self-regulation, belief convergence to organizational closure.

**Multi-Agent Trust and Robot Identity.** Reputation models (Sabater & Sierra, 2001; Granatyr et al., 2015) universally assume that agent identity is given exogenously through identifiers. Trajectory identity inverts this: the signature itself becomes the basis for recognition, proposing a behavioral continuity signal alongside credential-based authorization; robustness to spoofing and substrate migration is not established. In HRI, long-term studies consistently find that perceived personality consistency drives sustained engagement, but treat identity as a design choice rather than an emergent property of the agent's own dynamics.

---

## 3. The Trajectory Signature Framework

### 3.1 Foundations

We translate autopoiesis into a **dynamical-systems** framing: the system has a preferred region of state space (the attractor), perturbations move it away, internal dynamics return it. We *characterize* this through trajectory summaries; we do not claim that our summaries *are* the basin (a real basin estimate would require explicit dynamical-systems identification, which we sketch as future work).

**On the autopoiesis-to-attractor translation**: this is a *modeling commitment*, not a definitional equivalence. Autopoiesis is a network-topological claim about the closure of self-producing processes; attractor dynamics is a state-space claim about preferred regions and return maps. The framework characterizes the *state-space shadow* of autopoietic self-maintenance, not the network-topological organization itself. The Eta component (introduced below) is best understood as a derived narrative summary of this shadow rather than a direct measurement of the autopoietic organization.

Building on Di Paolo's (2005) concept of adaptivity, we define the **viability envelope** V as the region of state space within which the agent can maintain itself: V = {x : x_min <= x <= x_max for each dimension}. The agent's continued operation consists of remaining within V.

We seek **quasi-invariants** — quantities approximately stable over time for a given agent, differing between agents, and computable from observable data.

**Identity as agent-environment coupling.** Several signature components (preferences, attractor center, social patterns) reflect the agent *in its niche* — what the environment afforded the agent to learn or where the agent's homeostasis settles given the inputs the environment provides. Following Beer (1995) and Barandiaran et al. (2009), we treat this not as a defect but as a feature: agency is constitutively a property of the coupled agent-environment system. The empirically informative experiment to disentangle agent-intrinsic from coupling-determined components is a *transplant test* (move the agent or its dynamics to a new environment). We have not run that experiment; it is flagged as the most informative single follow-up.

### 3.2 Trajectory Signature Definition

**Definition 3.1 (Trajectory Signature)**: The trajectory signature $\Sigma$ is a composite of five informationally-independent components plus one derived narrative summary:

```
Sigma = (Pi, Beta, Alpha, Rho, Delta; Eta)
```

| Component | Name | Captures |
|-----------|------|----------|
| Pi | Preference Profile | Learned environmental preferences |
| Beta | Belief Signature | Pattern of self-beliefs and evidence ratios |
| Alpha | State-Distribution Summary | Equilibrium center $\mu$, covariance $C_\alpha$, eigenvalues |
| Rho | Recovery Profile | Time constants $\tau$ from perturbation-recovery episodes |
| Delta | Relational Disposition | Social behavior patterns (bonding rate, valence, reciprocity) |
| Eta | Homeostatic Identity (derived view) | Narrative summary $(\mu, C_\alpha, \tau, V)$ — not informationally independent of Alpha + Rho + V; useful for self-monitoring records but not a separate term in the similarity sum |

A naming caveat for Alpha: we retain "attractor basin" by historical convention, but operationally it is a *state-distribution summary* (first and second moments), not an estimate of an attractor's basin boundary, vector field, or return map. To avoid symbol overload between the trajectory-signature symbol $\Sigma$ and the covariance, we write the covariance as $C_\alpha$ (regularized as $C_\alpha + \epsilon I$ to ensure non-singularity).

**On the cardinality of the decomposition**: a stronger paper version had argued that these six components are *minimal* — that removing any one collapses an identity-distinction the framework needs to make. That argument requires between-agent discriminability we have not yet demonstrated (§5.6 and §6 Future Work). We therefore make the weaker, defensible claim of *expressive sufficiency*: the listed components, taken together, can represent the phenomena the theoretical stack commits us to. Whether all five scored components are necessary remains a research question; the long-form paper develops the full argument and acknowledges that the cardinality may shift downward if the multi-agent experiment reveals component redundancy at the discrimination level.

**State-Distribution Summary (Alpha)**: Given state history $X = [x_1, \ldots, x_t]$ where $x \in \mathbb{R}^d$, $\alpha = \{\mu: \text{mean}(X), C_\alpha: \text{cov}(X), \text{eigenvalues}: \text{eig}(C_\alpha)\}$. The mean $\mu$ represents the equilibrium; $C_\alpha$ encodes covariation structure.

**Recovery Profile (Rho)**: For each dimension d, we estimate tau_d from perturbation-recovery episodes using exponential fit: x_d(t) = mu_d - (mu_d - x_perturbed) * exp(-t/tau_d). Perturbations are detected when |x(t) - mu| > threshold.

**Belief Signature (Beta)**: Beliefs update via Bayesian-like evidence accumulation. The pattern of which beliefs are confident, and their evidence ratios, characterizes the agent's learned self-understanding.

### 3.3 Computing Similarity

**Definition 3.2 (Trajectory Similarity)**: $\text{sim}(\Sigma_1, \Sigma_2) = \sum_i w_i \cdot \text{sim}_i(\text{component}_i)$, summing over the five informationally-independent components (Eta excluded to avoid double-counting):

| Component | Weight | Similarity Function |
|-----------|--------|---------------------|
| Pi (Preference) | 0.18 | Cosine similarity |
| Beta (Belief) | 0.18 | Cosine similarity |
| Alpha (State-Distribution) | 0.30 | Bhattacharyya coefficient |
| Rho (Recovery) | 0.22 | Log-ratio: $\exp(-\text{mean}(|\log(\tau_1/\tau_2)|))$ |
| Delta (Relational) | 0.12 | Normalized L1 distance |

Weights are operational defaults, not calibrated values; principled selection requires multi-agent comparison data (future work).

**State-Distribution Overlap (Alpha)** uses the Bhattacharyya coefficient between the two Gaussian-approximated distributions: $D_B = (1/8)(\mu_1 - \mu_2)^T C_{\text{avg}}^{-1} (\mu_1 - \mu_2) + (1/2) \ln(|C_{\text{avg}}| / \sqrt{|C_1| \cdot |C_2|})$; $\text{sim}_\alpha = \exp(-D_B)$, where $C_\text{avg} = (C_1 + C_2)/2$. The Gaussian approximation breaks down for multi-modal attractors; a GMM-based replacement is sketched in the long form.

Inverse-variance weighting gives more influence to stable components, which need not be individually discriminative. Informativeness weighting was proposed as a remedy, but the later pilot did not support that conjecture: on the software subset, equal weighting reached 60% accuracy, inverse-within-variance 57%, and ANOVA F-statistic weighting 32% (approximately chance). This is a result for one reduced signature and corpus, not a general ranking of weighting schemes (long form §6.5).

**Operational Continuity Relation**: Agents A and B are *operationally continuous* (denoted $A \approx_\theta B$) iff $\text{sim}(\Sigma_A, \Sigma_B) > \theta_{\text{continuity}}$ (operational default $\theta = 0.80$, provisional). This is reflexive and symmetric but **not transitive** — and the non-transitivity is the reason we name the relation *continuity* rather than *identity*: identity-as-such is transitive by Leibniz's law, but a similarity-at-threshold is a tolerance relation, formally a recognition or family-resemblance relation. We retain "identity" only for the philosophical interpretation; every formal claim is about $\approx_\theta$, not strict equality.

**Cold Start**: Until ~50 observations (~8 minutes at 10s sampling), the implementation down-weights similarity outputs by $\min(1, \text{obs\_count}/50)$. After 50 observations the implementation stops down-weighting; this is *not* the same as "identity established" — the signature continues to stabilize over the order of $10^4$ observations.

---

## 4. Operational Semantics

### 4.1 Forking

A fork creates agent B from parent A: B inherits A's Sigma and begins accumulating its own trajectory. Initially sim(Sigma_A, Sigma_B) ~ 1; over time it decreases as experiences diverge. When similarity falls below the chosen threshold, the pair no longer meets the proposed operational continuity relation; this is not a test of strict philosophical identity. This provides principled answers to "which copy is real?"—both are real, with measurable divergence.

### 4.2 Merging

Combining insights from forked agents: C.Pi = weighted_average(A.Pi, B.Pi), with conflict resolution via confidence weighting. Merging is constrained to agents where sim(Sigma_A, Sigma_B) > theta_merge (still similar enough for coherent combination).

### 4.3 Anomaly Detection

An agent exhibits anomalous behavior if sim(Sigma_t, Sigma_{t-delta}) < theta_anomaly. To address gradual drift ("boiling frog"), we maintain a **genesis signature** Sigma_0 frozen at creation and apply two-tier detection:

1. **Coherence check**: sim(Sigma_t, Sigma_{t-1}) > theta_anomaly (short-term consistency)
2. **Lineage check**: sim(Sigma_t, Sigma_0) > theta_lineage (long-term continuity)

Where theta_lineage < theta_anomaly to allow healthy maturation while detecting fundamental drift.

### 4.4 Inter-Agent Recognition

Agent A recognizes agent B if sim(Sigma_B, Sigma_known) > theta_recognition for some known signature. This defines a proposed recognition rule when process trajectories are observable. Individual recognition, impersonation detection, and recognition across UUID or harness changes have not been validated. Static workspace artifacts alone do not supply the required process trajectory, and this score does not authorize access.

---

## 5. Empirical Observations and Their Limits

We report pilot observations from Lumen, an embodied AI agent running on a Raspberry Pi 4 with AHT20 (temperature, humidity), BMP280 (pressure), and VEML7700 (light) sensors. Lumen maintains a 4-dimensional state (warmth, clarity, stability, presence) derived from sensor readings and system metrics. Over 65 calendar days (January 11 – March 16, 2026), Lumen accumulated approximately 226,029 state observations (count from May 9, 2026 backup snapshot at `~/backups/lumen/anima_20260509_0700.db`) across 47 days with $\geq 100$ samples each (the remaining days had brief uptime windows or hardware-restart gaps).

**Sections 5.1-5.5 report a single-agent observation study**; they do not establish between-agent discrimination. Section 5.6 summarizes the later, confounded resident pilot. Neither study validates individual recognition across changes in role or harness.

### 5.1 State-distribution stability (Alpha)

**Method**: We partition observations into non-overlapping windows of 500 samples and report (a) the variance of window-means across the dataset, and (b) the average within-window variance.

| Dimension | Grand Mean | Var($\mu$) across windows | Avg within-window variance |
|-----------|-----------|---------------------------|----------------------------|
| Warmth | 0.413 | 0.0103 | 0.0012 |
| Clarity | 0.818 | 0.0057 | 0.0040 |
| Stability | 0.891 | 0.0073 | 0.0008 |
| Presence | 0.833 | 0.0131 | 0.0003 |

All dimensions exhibit per-dimension between-window Var($\mu$) below 0.015 — corresponding to a drift standard deviation under 0.13 on the unit-range $[0,1]$ state, over 65 calendar days. In absolute terms, Lumen's equilibrium centers occupy a small band of state space. The within- vs between-window ratio shows the state is *strongly autocorrelated* (slow drift, little fast noise within 500-sample windows); we do not claim the i.i.d.-around-a-fixed-point picture an earlier draft suggested. Characterizing the actual basin geometry would require fitting an explicit dynamical model.

### 5.2 Recovery Dynamics

**Provenance and method.** These are summaries of the live system's recorded recovery profile, read from `trajectory_last.json` by `figure_2_recovery_profile()` in the [Anima figure script](https://github.com/cirwel/anima-mcp/blob/c82a01cac912c8e174dac442d75fc24fcd89e7b2/scripts/paper_figures.py#L105-L120). That function prints stored estimates; it does not detect events or fit recovery curves from the raw `state_history` rows. The table therefore describes 12 episodes retained by the live detector at snapshot time, not an independently recomputed episode count over the 65-day history. A frozen detector specification and episode-level export are needed for independent reproduction.

| Metric | Value |
|--------|-------|
| Recovery $\tau$ (median) | 89.7 seconds |
| Recovery $\tau$ (mean) | 125.8 seconds |
| Recovery $\tau$ (std) | 136.3 seconds |
| Perturbation episodes | 12 |
| Valid $\tau$ estimates | 12 (100%) |

With 12 episodes the estimate is noisy; we report median and mean to flag the right-skewed distribution but make no claim about underlying distribution shape. The snapshot summary does not establish complete event coverage over the 65-day record, so it cannot support an episode rate or an inference that perturbations were rare. Controlled perturbations with exported event records would provide better-supported estimates.

### 5.3 Belief Convergence

Lumen tracks 13 self-beliefs via Bayesian-like evidence accumulation. Selected beliefs after 65 days:

| Belief | Confidence | Evidence (support : contradict) |
|--------|-----------|--------------------------------|
| Morning clarity | 1.000 | 14,362 : 0 |
| Stability recovery | 0.984 | 1,327 : 499 |
| LEDs affect lux | 0.900 | 988 : 1,104 |
| Temperature sensitive | 0.882 | 28 : 654 |
| (refuted: warmth baseline low) | 0.000 | 0 : 58,908 |

"Morning clarity" converged with substantial supporting observations and zero contradictions; the system correctly rejects "warmth baseline low" with 58,908 contradicting observations. Convergence is observed for 4 of 13 beliefs with substantial evidence, plus 1 refuted. The implementation retains a smoothing prior on each belief — in zero-evidence cases, confidence reflects that prior, not a posterior.

### 5.4 Genesis-to-Current Operational Continuity

We compare the genesis signature (February 22, 2026) to the current signature (March 14, 2026) — a span of 20 days:

| Component | Similarity | Operational default |
|-----------|-----------|---------------------|
| Belief signature (Beta) | 0.933 | $\theta_{\text{continuity}} = 0.80$ (provisional) |
| State-distribution (Alpha) | 0.805 | $\theta_{\text{continuity}} = 0.80$ (provisional) |

Both clear the operational default. **This is internal-consistency evidence under a self-set threshold — not threshold validation.** Pi, Rho, and Delta were not computed in this run. The result speaks to stability of two of five components over 20 days, not to the framework's full composite signature, and not to between-agent discrimination.

### 5.5 Summary

| Hypothesis from §3 | Status in Lumen | Evidence |
|---------------------|-----------------|----------|
| State-distribution stability over 65 days | **Observed (small absolute drift)** | Var($\mu$) < 0.015 all dimensions |
| Recovery profile at snapshot time | **Recorded (small sample)** | median 89.7s; mean 125.8s; n = 12 |
| Belief convergence with substantial evidence | **Observed for 4 of 13 + 1 refuted** | confidence > 0.88 on 4 beliefs |
| Operational continuity from genesis | **Observed for 2 of 5 components** | sim 0.81–0.93 over 20 days |
| Cold-start down-weighting resolves at 50 obs | **Observed** | not the same as "identity established" |

### 5.6 Resident discrimination: a confounded pilot

The long-form paper §6.5 reports a separate pilot on 40,929 governance check-ins from four residents in one operator's fleet (Lumen, Sentinel, Watcher, Vigil). A 25-dimensional reduced signature summarizes the shared $(E,I,S,V,\phi)$ state through means and spreads, lag-1 autocorrelations, and inter-dimension correlations. It omits preference and belief channels and does not use Eta. Nearest-centroid matching over 150-check-in windows with a per-agent 70/30 temporal split reported 71% four-way accuracy (25% chance), and 60% for the three software residents (33% chance). These are the previously reported values, not a new experiment or a test of the full five-component similarity rule.

**The pilot is confounded by role and harness.** The residents differ systematically in embodiment, cadence, and duty cycle. A subsequent audit of the separate production similarity measure found between-agent similarity 0.63 versus within-agent similarity across eras 0.12. Because that audit uses a different instrument, it does not directly refute the reduced-signature pilot; it exposes the live alternative that the labels separate roles or regimes rather than individuals. The temporal split does not remove that confound. Discrimination remains open pending a within-agent/across-harness test and a between-agent/same-harness test. The reported values stand with this narrower interpretation.

**Implementation boundary.** The paper's five weights exclude derived Eta (§3.3). The long-form Appendix A records that the cited Anima implementation instead included Eta until its August 14 correction (`3ac59e6`). This correction does not apply to the separate UNITARES implementation: at the [October 11 source snapshot](https://github.com/cirwel/unitares/blob/5c871945f3596770722d4e144c193729527fd7de/src/trajectory_identity.py#L308-L374), available Eta receives nominal weight 0.15, with missing components skipped and available weights renormalized. The experiments use standalone analysis code; neither this workshop revision nor the Anima correction changes their reported numbers.

---

## 6. Discussion

### Limitations

The single-agent observations and the resident pilot remain preliminary. Several limitations apply:

**Discrimination remains open**: The resident pilot does not separate individual identity from role and harness (§5.6). Same-harness comparisons between individuals and migrations of the same agent across harnesses are required before claiming individual recognition. Independent operators and a preregistered protocol are also needed.

**Low-dimensional state**: Lumen's 4D state space is tractable but simple. LLM-based agents with higher-dimensional states may require dimensionality reduction before trajectory computation.

**Environmental coupling (transplant test)**: As §3.1 emphasized, Alpha and Pi are partly determined by Lumen's physical environment; the trajectory signature characterizes the agent-niche system. The transplant test (move the agent to a different location) is the most informative single follow-up to disentangle agent-intrinsic from coupling-determined components.

**Threshold sensitivity**: The operational continuity threshold $\theta = 0.80$ is provisional, not calibrated. Systematic calibration requires multi-agent comparison data and ROC-curve selection at a chosen false-positive rate.

**Phase transitions and multi-modal identity**: The framework as stated assumes one identity-relevant attractor. Agents with legitimate phase transitions (sleep/wake modes, distinct conversational personas) need either phase-conditional signatures or per-phase signature checking. The Bhattacharyya overlap also implicitly assumes Gaussian state distributions; multi-modal attractors need a GMM-based replacement.

**Recovery reproducibility**: The 12-episode recovery table is a live-system snapshot summary. Its original detector and episode records must be frozen and exported before independent reproduction. The archived offline routine excludes the samples it needs to detect recovery, so its zero output is not evidence against the table (long form §6.4.2).

**Adversarial robustness — out of scope here**: trajectory identity is a governance-and-continuity primitive, not adversarial authentication; the long-form paper §5.5 develops the threat model, per-component mimicry-resistance analysis, and behavioral-CAPTCHA defense. We do not claim cryptographic-grade impersonation resistance.

### Philosophical Implications

This framework suggests a shift in how we think about AI identity. It treats persistent behavioral organization as a proposed account of identity, while operational authorization remains credential-based. Continuity comes not from remembering everything but from maintaining characteristic patterns. And identity is not a fixed property but an ongoing achievement: an agent must continually "perform" its identity through consistent behavior.

### Future Work

**Disentangling identity and harness**: Run within-agent/across-harness and between-agent/same-harness tests, then estimate false-positive rates and operating thresholds on held-out data from independent operators. **Transplant test**: move Lumen (or its dynamics) to a different physical environment; check which components of $\Sigma$ shift (coupling-determined) and which remain stable (agent-intrinsic). **Adversarial robustness**: empirical mimicry studies under realistic capability constraints — see long-form §5.5 for the threat model and behavioral-CAPTCHA defense. **Cross-platform validation**: test on LLM-based agents (MemGPT, ID-RAG, Generative Agents) and persona-consistency benchmarks (PersonaChat, RoleBench, CharacterEval). **Governance state**: the resident pilot already uses UNITARES EISV plus $\phi$; the remaining task is validating its interpretation and its relation to the full specification, not claiming that integration alone validates identity.

---

## 7. Conclusion

We have presented a framework for AI agent identity based on trajectory signatures — composite quasi-invariants computed from behavioral history — and reported preliminary within-agent observations plus a resident classification pilot confounded by role and harness. The framework proposes operational continuity in behavioral dynamics and provides operational semantics for forking, merging, and a two-tier (coherence + lineage) anomaly detection scheme.

The trajectory signature is a proposal for operationalizing behavioral continuity. The within-agent observations are consistent with limited stability in one deployment; individual discrimination, recovery reproducibility, threshold calibration, and adversarial robustness remain unresolved. The framework complements explicit identifiers and authorization rather than replacing them.

---

## References

Banerjee, S. P., & Woodard, D. L. (2012). Biometric authentication and identification using keystroke dynamics: A survey. *Journal of Pattern Recognition Research*, 7(1), 116-139. [doi:10.13176/11.427](https://doi.org/10.13176/11.427).

Barandiaran, X. E., & Moreno, A. (2006). On what makes certain dynamical systems cognitive. *Adaptive Behavior*, 14(2), 171–185.

Barandiaran, X. E., Di Paolo, E. A., & Rohde, M. (2009). Defining agency: Individuality, normativity, asymmetry, and spatio-temporality in action. *Adaptive Behavior*, 17(5), 367–386.

Beer, R. D. (1995). A dynamical systems perspective on agent-environment interaction. *Artificial Intelligence*, 72(1–2), 173–215.

Bhattacharyya, A. (1943). On a measure of divergence between two statistical populations. *Bulletin of the Calcutta Mathematical Society*, 35, 99–109.

Di Paolo, E. A. (2005). Autopoiesis, adaptivity, teleology, agency. *Phenomenology and the Cognitive Sciences*, 4(4), 429–452.

Freeman, W. J. (2000). *Neurodynamics: An exploration in mesoscopic brain dynamics*. Springer.

Friston, K. (2010). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127–138.

Froese, T., & Ziemke, T. (2009). Enactive artificial intelligence. *Artificial Intelligence*, 173(3–4), 466–500.

Granatyr, J., et al. (2015). Trust and reputation models for multiagent systems. *ACM Computing Surveys*, 48(2), 1–42.

Ikegami, T., & Suzuki, K. (2008). From a homeostatic to a homeodynamic self. *BioSystems*, 91(2), 388–400.

Kelso, J. A. S. (1995). *Dynamic Patterns: The Self-Organization of Brain and Behavior*. MIT Press.

Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition*. D. Reidel.

Packer, C., et al. (2023). MemGPT: Towards LLMs as operating systems. *arXiv:2310.08560*.

Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human behavior. *Proceedings of UIST*.

Platnick, D., Bengueddache, M. E., Alirezaie, M., Newman, D. J., Pentland, A., & Rahnama, H. (2025). ID-RAG: Identity retrieval-augmented generation for long-horizon persona coherence in generative agents. [arXiv:2509.25299](https://arxiv.org/abs/2509.25299).

Sabater, J., & Sierra, C. (2001). ReGreT: A reputation model for gregarious societies. *Proceedings of AAMAS*.

Skarda, C. A., & Freeman, W. J. (1987). How brains make chaos in order to make sense of the world. *Behavioral and Brain Sciences*, 10(2), 161–173.

Tu, Q., et al. (2024). CharacterEval: A Chinese benchmark for role-playing conversational agent evaluation. *Proceedings of ACL*, 11836–11850.

van Gelder, T. (1998). The dynamical hypothesis in cognitive science. *Behavioral and Brain Sciences*, 21(5), 615–628.

Varela, F. J., Thompson, E., & Rosch, E. (1991). *The Embodied Mind*. MIT Press.

Villalobos, M., & Dewhurst, J. (2018). Enactive autonomy in computational systems. *Synthese*, 195(5), 1891–1908.

Wang, G., et al. (2023). Voyager: An open-ended embodied agent with large language models. *arXiv:2305.16291*.

Wang, Z. M., et al. (2023b). RoleLLM: Benchmarking, eliciting, and enhancing role-playing abilities of large language models. *arXiv:2310.00746*.

Weber, A., & Varela, F. J. (2002). Life after Kant. *Phenomenology and the Cognitive Sciences*, 1, 97–125.

Xu, J., Wang, F., Ma, M. D., Koh, P. W., Xiao, C., & Chen, M. (2024). Instructional fingerprinting of large language models. [arXiv:2401.12255](https://arxiv.org/abs/2401.12255).

Zhang, S., et al. (2018). Personalizing dialogue agents: I have a dog, do you have pets too? *Proceedings of ACL*, 2204–2213.
