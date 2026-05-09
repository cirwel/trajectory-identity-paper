# Trajectory Identity: A Mathematical Framework for Enactive AI Self-Hood

**Authors:** Kenny Wang, Independent Researcher (founder@cirwel.org)
**Date:** May 2026
**Status:** Working Draft
**Version:** 0.11

---

## Abstract

Current approaches to AI agent identity rely on static identifiers (UUIDs, session tokens) or accumulated memory stores. We propose an alternative grounded in enactive cognition and dynamical systems theory: **identity as trajectory**. Rather than asking "what ID does this agent have?", we ask "what patterns persist in this agent's behavior over time?"

We present a mathematical framework for computing **trajectory signatures** from time-series data including homeostatic state, learned preferences, self-beliefs, and recovery dynamics. The trajectory signature (Sigma) captures the quasi-invariant characteristics that define an agent's identity—not where it is at any moment, but how it tends to behave, where it tends to rest, and how it returns from perturbation.

This framework addresses several open problems: (1) identity continuity across sessions without unbounded memory growth, (2) principled semantics for agent forking and merging, (3) anomaly detection as trajectory deviation, and (4) inter-agent recognition based on behavioral signatures rather than credentials.

We ground this work in the UNITARES governance architecture and the Anima embodied AI system, showing how existing components (self-schema, self-model, preference learning, EISV metrics) provide the data substrate for trajectory computation. Preliminary validation on Lumen (Raspberry Pi embodied AI, continuous operation) demonstrates attractor basin stability (mu variance < 0.05 across time windows) and consistent recovery profiles, supporting the quasi-invariance hypothesis.

---

## Purpose and Scope

This framework addresses **governance and continuity** problems, not adversarial authentication. Trajectory signatures are designed to:

1. **Detect drift**: Identify when an agent has changed beyond recognition (governance trigger)
2. **Track lineage**: Maintain meaningful "same agent" judgments across sessions and forks
3. **Enable self-monitoring**: Let agents ask "Am I still myself?" computationally
4. **Support fork/merge semantics**: Provide principled answers to "which copy is real?"

**Non-goals**: We do not claim trajectory signatures replace cryptographic identity for adversarial scenarios. A sophisticated attacker with full system access could potentially mimic behavioral patterns. For authentication in hostile environments, combine trajectory signatures with cryptographic attestation.

**Target deployment**: Long-running AI assistants, embodied agents, multi-agent systems where behavioral continuity matters more than adversarial resistance.

---

## 1. Introduction: The Identity Problem

### 1.1 The Limitations of Static Identity

Modern AI agents are typically identified by static tokens:
- **UUIDs**: Unique identifiers assigned at creation
- **Session IDs**: Temporary bindings to conversation threads
- **API keys**: Authentication credentials

These approaches share a fundamental limitation: **identity is conferred, not earned**. An agent has an identity because we gave it one, not because it developed characteristics that make it recognizably itself.

This creates practical problems:
- **Continuity fragility**: If the UUID is lost, identity is lost
- **Fork ambiguity**: If we copy an agent, which copy is "the real one"?
- **Anomaly blindness**: A compromised agent with the right credentials is indistinguishable from the original
- **Memory explosion**: Maintaining identity through accumulated memory leads to unbounded growth

**Comparison of Identity Approaches**:

| Criterion | UUID/Credential | Memory-Based | Trajectory Signature |
|-----------|-----------------|--------------|---------------------|
| **Continuity** | Fragile (lost if token lost) | Strong (persists in storage) | Strong (recomputable from behavior) |
| **Fork semantics** | Ambiguous (which has the "real" ID?) | Ambiguous (both have same memories) | Clear (divergence is measurable) |
| **Anomaly detection** | None (valid credential = valid agent) | Heuristic (memory tampering) | Mathematical (trajectory deviation) |
| **Storage growth** | O(1) | O(unbounded) | O(window size) |
| **Impersonation resistance** | Weak (credential theft) | Moderate (memory reconstruction) | Moderate, component-dependent (see §5.5; not a substitute for cryptographic auth) |
| **Cold start** | Immediate | Immediate | Requires ~50 observations |

### 1.2 The Enactive Alternative

The enactive cognition tradition (Varela, Thompson, & Rosch, 1991; Di Paolo, 2005) offers a different perspective. In biological systems, identity is not a label attached from outside—it emerges from the ongoing process of self-maintenance.

A cell's identity is defined by its autopoietic organization: the network of processes that continuously produce the components that make up the cell. The identity IS the process, not any particular configuration of matter.

**Our proposal**: AI agent identity should similarly be defined by the *patterns that persist* in the agent's behavior over time—what we call the **trajectory signature**.

### 1.3 Contributions

This paper makes the following contributions:

1. **Formal definition** of trajectory signature (Sigma) as a composite of six quasi-invariant components
2. **Mathematical framework** for computing trajectory similarity and detecting identity
3. **Operational semantics** for forking, merging, and anomaly detection
4. **Connection to existing systems** (UNITARES, Anima) showing implementation paths
5. **Research agenda** identifying open questions and experimental designs

### 1.4 Related Work

Our formulation draws on and bridges several research traditions. We position trajectory signatures as a unifying construct that these literatures approach from different angles but none have formalized.

**Agent Memory and State Persistence.** Recent work on LLM-based agents has foregrounded the problem of maintaining coherent state across interactions. Packer et al. (2023) introduced MemGPT, applying hierarchical memory management to give LLM agents persistent state across sessions. Park et al. (2023) demonstrated that agents with memory streams, reflection, and planning exhibit emergent social behavior that remains individually consistent. Wang et al. (2023) extended this with Voyager, whose ever-growing skill library functions as behavioral accumulation. Most directly comparable to our work is *ID-RAG* (Park et al., 2025): identity-retrieval-augmented generation for long-horizon persona coherence, which targets the same drift problem we do but solves it by injecting a structured identity object into the retrieval context rather than by characterizing the agent's behavioral dynamics. ID-RAG and trajectory identity are complementary: ID-RAG provides the *content* of identity (the prompt-engineered self-description); trajectory signatures provide the *form* (the dynamical signature the content produces in behavior). These systems implicitly rely on trajectory-like continuity but define identity through stored content rather than through the dynamical signatures of how content shapes ongoing behavior. Our work makes the underlying dynamics explicit.

**Persona Consistency Benchmarks.** A separate strand of LLM literature evaluates whether agents *behave* consistently with a declared persona. PersonaChat (Zhang et al., 2018) introduced a dataset of dialogues anchored to persona descriptions; RoleLLM / RoleBench (Wang et al., 2023b) and CharacterEval (Tu et al., 2024) extended persona-consistency evaluation to fine-grained character profiles and role-playing scenarios. These benchmarks treat consistency as a comparison between an agent's outputs and a declared persona, evaluated via NLI-style entailment or LLM-as-judge. Trajectory identity treats consistency intrinsically — the agent is recognized by its own dynamical signature, with no declared persona to compare against. The two approaches address different operational regimes: persona-consistency benchmarks for closed-vocabulary persona evaluation; trajectory signatures for open-ended deployments where the agent's identity emerges from its behavior rather than being authored in advance.

**Behavioral Biometrics.** The principle that identity can be inferred from behavioral patterns has a long history in biometrics. Keystroke dynamics (Banerjee & Woodard, 2019) demonstrates that temporal micro-patterns are sufficiently individuating for continuous authentication. Xu et al. (2024) showed that LLMs can be identified through characteristic response signatures. These approaches treat behavioral signatures as static classifiers. Trajectory identity extends this into a dynamical frame: rather than fingerprinting a snapshot, we characterize the geometry of how behavior evolves, recovers from perturbation, and converges—yielding a quasi-invariant that persists even as surface outputs change.

**Dynamical Systems in Cognitive Science and AI.** Kelso's (1995) *Dynamic Patterns* established that cognitive phenomena are best described through self-organizing dynamical systems. Skarda and Freeman (1987) demonstrated that olfactory perception operates through chaotic itinerancy across attractor basins, with each learned odor corresponding to a distinct basin rather than a stored representation. The "dynamical hypothesis" (van Gelder, 1998) holds that cognitive systems are best understood as dynamical systems traversing state spaces. Beer (1995) made this concrete for AI agents: an agent and its environment are best modeled as a single coupled dynamical system, and what counts as "the agent's behavior" is a property of that joint system, not the agent in isolation. We adopt this stance directly — see "Identity as agent-environment coupling" in §3.1 — and the empirical findings in §6.4 are reported with that framing in view.

**Enactivism, Autopoiesis, and Defining Agency.** Weber and Varela (2002) argued that biological identity is constituted through autopoietic self-production. Di Paolo (2005) extended this with *adaptivity*: the capacity of an autonomous system to regulate itself with respect to its viability conditions. Barandiaran and Moreno (2006) and Barandiaran, Di Paolo & Rohde (2009) — the latter directly addressing the question "what defines agency?" — identified individuality, normativity, and asymmetry as the structural commitments any account of agency must satisfy. Froese and Ziemke (2009) examined implications for artificial systems, identifying constitutive autonomy as necessary for genuine AI agency. Villalobos and Dewhurst (2018) sharpened the autopoietic criterion in a form directly applicable to artificial systems. Ikegami and colleagues (e.g., Ikegami & Suzuki, 2008) operationalized "homeodynamic self" in artificial-life simulations, showing that self-maintaining patterns emerge in simulated agents under appropriate dynamics. Trajectory identity operationalizes these ideas computationally for deployed (rather than simulated) systems: attractor basins correspond to viable operating regimes, recovery dynamics to adaptive self-regulation, and belief convergence to organizational closure. To our knowledge, this is the first formal mapping from enactive concepts to measurable dynamical signatures in deployed, continuously-running AI agents.

**Multi-Agent Trust and Robot Identity.** Reputation models (Sabater & Sierra, 2001; Granatyr et al., 2015) universally assume that agent identity is given exogenously through identifiers. Trajectory identity inverts this: the signature itself becomes the basis for recognition, enabling trust robust to identifier spoofing and substrate migration. In HRI, long-term studies consistently find that perceived personality consistency drives sustained engagement, but treat identity as a design choice rather than an emergent property of the agent's own dynamics.

---

## 2. Theoretical Foundations

### 2.1 From Autopoiesis to Attractor Dynamics

Autopoiesis (Maturana & Varela, 1980) describes living systems as self-producing networks. The key insight is **operational closure**: the system's processes produce the conditions for those same processes to continue.

In dynamical systems terms, this translates to **attractor dynamics**:
- The system has a preferred region of state space (the attractor)
- Perturbations move the system away from this region
- Internal dynamics return the system to the attractor
- The shape of the attractor basin and the recovery dynamics ARE the identity

**Connection to Free Energy Principle**: Friston's (2010) free energy principle provides a complementary perspective: living systems minimize variational free energy (prediction error). The attractor basin represents the agent's "model" of where it should be; returning to the attractor minimizes surprise. Identity, in this view, is the agent's implicit generative model of itself—the pattern it expects to maintain.

**Definition 2.1 (Attractor-Based Identity, idealized)**: In the idealized dynamical-systems setting, an agent's identity I is characterized by the tuple (A, B, D) where:
- A = attractor (the equilibrium state or limit cycle)
- B = basin (the set of states from which the system returns to A)
- D = dynamics (the vector field governing return to A)

Different agents with identical attractors A can have different identities if their basins B or dynamics D differ. **Operationally, we do not estimate (A, B, D) directly** — we estimate state-distribution and recovery summaries (§3.3 and §3.4) that are projections of this triple. The shape of the attractor basin and the recovery dynamics are *what we want to characterize*, but the components defined in §3 are summary statistics, not the dynamical objects themselves.

### 2.2 The Viability Envelope

Building on Di Paolo's (2005) concept of adaptivity, we define the **viability envelope** as the region of state space within which the agent can maintain itself.

**Definition 2.2 (Viability Envelope)**: For state vector x in R^n, the viability envelope V is:

```
V = {x : x_min <= x <= x_max for each dimension}
```

**Concrete bounds** (mapped from UNITARES thresholds):

| Dimension | Min | Max | Interpretation |
|-----------|-----|-----|----------------|
| Energy (E) | 0.1 | 0.9 | Operational capacity |
| Integrity (I) | 0.3 | 1.0 | Coherence with purpose |
| Entropy (S) | 0.0 | 0.6 | Disorder threshold |
| Void (V) | -0.2 | 0.15 | E-I imbalance |

The agent's "life" consists of remaining within V while pursuing goals. Crossing V boundaries triggers governance intervention (pause, reflection).

### 2.3 Identity as Dynamical Quasi-Invariant

A **dynamical invariant** is a quantity that remains constant (or bounded) along system trajectories. For identity, we seek **quasi-invariants**—quantities that are approximately stable rather than strictly constant:
1. Remain stable for a given agent over time
2. Differ between distinct agents
3. Can be computed from observable data
4. Are robust to noise and minor perturbations

**Definition 2.3 (Trajectory Signature)**: The trajectory signature Sigma is a composite quasi-invariant consisting of six components:

```
Sigma = (Pi, Beta, Alpha, Rho, Delta, Eta)
```

Where:
- **Pi** (Preference Profile): Learned environmental preferences
- **Beta** (Belief Signature): Pattern of self-beliefs and confidences
- **Alpha** (Attractor Basin): Equilibrium and variance structure
- **Rho** (Recovery Profile): Characteristic time constants
- **Delta** (Relational Disposition): Social behavior patterns
- **Eta** (Homeostatic Identity): Unified self-maintenance characterization

Each component captures a different aspect of "how this agent tends to be."

### 2.4 Justification of the Six Components

A natural objection is: why six? Why not four, or eight? The choice is not arbitrary — each component is anchored in a specific commitment in the theoretical stack, and removing any one collapses a class of identity-distinctions the framework needs to make.

**Theoretical anchoring**:

| Component | Theoretical commitment | What it makes distinguishable |
|-----------|------------------------|-------------------------------|
| Alpha (Attractor Basin) | Dynamical systems: attractor as the system's "preferred" region | Two agents that occupy different equilibria |
| Rho (Recovery Profile) | Free-energy principle: characteristic prediction-error correction dynamics | Two agents with the same equilibrium but different return dynamics (slow recoverer vs. fast recoverer) |
| Eta (Homeostatic Identity) | Autopoiesis: viability envelope + set-point as the unity of self-maintenance | The agent as a self-maintaining whole, not just a point cloud |
| Pi (Preference Profile) | 4E cognition: enactive coupling — preferences are how the agent has *tuned itself to its environment* | Two agents with identical homeostasis but different learned environmental couplings |
| Beta (Belief Signature) | Predictive processing: the agent's internal model of itself, with evidence-weighted confidence | Two agents with identical behavior but different self-understanding (matters for self-monitoring) |
| Delta (Relational Disposition) | Participatory sense-making (De Jaegher & Di Paolo, 2007): identity is partly constituted by patterns of social engagement | Two agents identical in solo behavior but distinguishable in interaction |

**Minimality argument**: removing any single component creates an identity-distinction the framework can no longer represent.

- Without Alpha: cannot distinguish agents with different equilibria
- Without Rho: cannot distinguish stable-vs-fragile agents at the same equilibrium
- Without Eta: have basin and recovery as separate facts but no unified self-maintenance signature; lose the autopoietic anchor
- Without Pi: cannot distinguish agents that have learned different environmental couplings
- Without Beta: cannot detect self-deception (agent's stated self-model diverging from its observable behavior)
- Without Delta: cannot distinguish agents in multi-agent contexts where social pattern is identity-relevant

**Honest framing**: the six-component decomposition is *a* valid factorization, not *the* unique one. A different theoretical stack might motivate a different decomposition (e.g., embedding the recovery dynamics inside the attractor description as a single dynamical-systems object). Our claim is more modest: this decomposition is operationally useful for the systems we ground in (UNITARES, Anima), and each component carries its theoretical weight in the stack we adopt. We discuss alternative decompositions in §8.5 (Future Work).

---

## Notation and Assumptions

### Notation

| Symbol | Meaning |
|--------|---------|
| Sigma | Trajectory signature (composite) |
| Sigma_0 | Genesis signature (reference anchor at creation) |
| Sigma_t | Signature at time t |
| x(t) | State vector at time t |
| mu | Attractor center (mean state) |
| tau | Recovery time constant |
| theta | Similarity threshold |

### Key Assumptions

1. **Stationarity**: Component distributions are approximately stationary over the observation window. Rapidly changing agents may require shorter windows or non-stationary extensions.

2. **Independence**: Component similarities are computed independently and combined linearly. Cross-component correlations are not modeled (future work).

3. **Observability**: All state dimensions are observable. Latent state estimation is not addressed.

4. **Sampling regularity**: Observations are approximately evenly spaced. Irregular sampling requires interpolation or time-weighted aggregation.

5. **Perturbation detectability**: Recovery profile (Rho) requires identifiable perturbation events (|x(t) - mu| > threshold). Agents with no perturbations cannot compute Rho.

---

## 3. The Trajectory Signature: Formal Definitions

### 3.1 Preference Profile (Pi)

Agents develop preferences through experience—correlations between environmental conditions and internal states.

**Definition 3.1 (Preference Profile)**: Given a set of preference categories C and learned preferences {p_c} for c in C, the preference profile is:

```
Pi = [(c_1, v_1, kappa_1), (c_2, v_2, kappa_2), ..., (c_n, v_n, kappa_n)]
```

Where:
- c_i = preference category (e.g., "dim_light", "cool_temp")
- v_i = preference value in [-1, 1] (negative to positive valence)
- kappa_i = confidence in [0, 1]

**Vector form** (for similarity computation):
```
Pi_vec = [v_1 * kappa_1, v_2 * kappa_2, ..., v_n * kappa_n]
```

**Properties**:
- Pi evolves slowly (learning rate alpha = 0.3)
- Pi stabilizes after sufficient observations (typically n > 20)
- Pi is environment-dependent but agent-characteristic — see "Identity as agent-environment coupling" below

**Identity as agent-environment coupling.** A reviewer-relevant observation that surfaces here and recurs throughout: the trajectory signature does not characterize an agent in isolation — it characterizes the *agent in its niche*. Pi reflects what the environment has afforded the agent to learn; Alpha reflects where the agent's homeostatic dynamics settle *given* the inputs the environment provides; Delta reflects social patterns that exist only in interaction. This is not a defect for the enactivist framing this paper adopts (Beer 1995; Barandiaran, Di Paolo & Rohde 2009 argue that agency is constitutively a property of the coupled agent-environment system, not the agent alone). It does mean that "the same agent" in a different environment is, in the framework's terms, a different agent-environment system, and its trajectory signature will differ. The right experiment to disentangle agent-intrinsic from coupling-determined components is a *transplant test*: move the agent (or its dynamics) to a new environment and check which components of $\Sigma$ remain stable and which shift. We have not run this experiment; we flag it as the most informative single follow-up (§7.3 Extensions).

### 3.2 Self-Belief Signature (Beta)

Agents maintain testable beliefs about themselves—hypotheses that can be confirmed or refuted by experience.

**Definition 3.2 (Self-Belief Signature)**: Given a set of self-beliefs B = {b_1, ..., b_m}, the belief signature is:

```
Beta = {
    values: [b_1.value, ..., b_m.value],
    confidences: [b_1.confidence, ..., b_m.confidence],
    evidence_ratios: [b_1.support/b_1.contradict, ..., b_m.support/b_m.contradict]
}
```

**Vector form**:
```
Beta_vec = values (normalized to [0,1])
```

**Properties**:
- Beliefs update via Bayesian-like evidence accumulation
- The *pattern* of which beliefs are confident matters more than individual values
- Evidence ratios reveal the agent's actual experience, not just current belief

### 3.3 Attractor Basin (Alpha) — state-distribution summary

The agent's characteristic "home" in state space, summarized statistically. **Naming caveat**: we call this component "Attractor Basin" by historical convention from the dynamical-systems literature, but operationally it is a *state-distribution summary* — first and second moments of the state trajectory — not an estimate of an attractor's basin boundary, vector field, or return map. A reader expecting the latter (as in nonlinear-dynamics texts) will not find it here. Estimating the actual basin requires perturbation experiments and dynamical-systems identification, which we sketch as future work in §7.3.

**Definition 3.3 (State-Distribution Summary)**: Given state history X = [x_1, ..., x_t] where x in R^4 (warmth, clarity, stability, presence), the component is:

```
Alpha = {
    mu: mean(X),                     # Center (4-dimensional)
    C_alpha: cov(X),                 # Shape (4x4 covariance matrix; renamed from Sigma to avoid clash with the signature symbol)
    eigenvalues: eig(C_alpha)        # Principal axes of variability
}
```

Where the matrix `C_alpha` (alternative notation: `Cov_alpha`) is the empirical covariance, distinct from the trajectory-signature symbol `Sigma`. We assume `C_alpha` is regularized as `C_alpha + epsilon * I` (epsilon = 1e-6) to ensure non-singularity for the Bhattacharyya overlap in §4.2.

**Sampling requirements**:
- Minimum 50 observations for stable estimates
- Sampling rate: 1 observation per 10 seconds
- Rolling window: 100-500 observations (10-80 minutes)

**Properties**:
- mu represents the equilibrium the agent returns to
- Sigma encodes which dimensions vary together and which are independent
- Eigenvalues of Sigma reveal the "principal axes" of variability

**High-dimensional states**: For agents with state vectors x in R^d where d >> 4, covariance computation becomes O(d^3) and numerically unstable.

**Dimensionality reduction strategies**:
1. **PCA projection**: Project to top-k principal components before computing Alpha
2. **Autoencoder latent space**: Learn a low-d "identity manifold" via neural compression
3. **Domain-specific features**: Select semantically meaningful dimensions (e.g., anima's 4D)

For Anima, d=4 is tractable. For LLM-based agents with high-d latent states, recommend projecting to d <= 16 before trajectory computation.

**Multimodal attractors**: If the agent has multiple stable states (e.g., "work mode" vs "rest mode"), the mean mu will fall in the "valley" between attractors. For such agents, consider Gaussian Mixture Models (GMM) with k components, where identity is characterized by the mixture weights and component parameters.

### 3.4 Recovery Profile (Rho)

How the agent returns to equilibrium after perturbation.

**Definition 3.4 (Recovery Profile)**: For each state dimension d, the recovery time constant tau_d is estimated from perturbation-recovery episodes using exponential fit:

```
x_d(t) = mu_d - (mu_d - x_perturbed) * exp(-t/tau_d)
```

The recovery profile is:
```
Rho = {
    tau: [tau_warmth, tau_clarity, tau_stability, tau_presence],
    coupling: C in R^{4x4}  # Cross-dimension recovery effects
}
```

**Estimation procedure**:
1. Detect perturbation: |x(t) - mu| > threshold (default: 0.15)
2. Track recovery: time until |x(t) - mu| < 0.05
3. Fit exponential: tau = -t / ln(1 - recovery_fraction)

**Properties**:
- Small tau = fast recovery (resilient, tau ~ 30-60 seconds)
- Large tau = slow recovery (persistent perturbation effects, tau ~ 300+ seconds)
- Coupling matrix C reveals whether dimensions recover independently or in concert

**Second-order dynamics**: The exponential model assumes overdamped recovery. Agents with momentum (memory effects) may exhibit damped oscillation:

```
x''(t) + 2*zeta*omega_n*x'(t) + omega_n^2*x(t) = 0
```

Where:
- zeta = damping ratio (zeta < 1: oscillatory, zeta > 1: overdamped)
- omega_n = natural frequency

**Extended recovery profile**:
```
Rho_extended = {
    tau: first-order time constants (default),
    zeta: damping ratios (if oscillatory recovery detected),
    omega_n: natural frequencies (if oscillatory)
}
```

For most agents, first-order (tau only) suffices. Detect oscillation by checking if recovery crosses equilibrium before settling.

### 3.5 Relational Disposition (Delta)

Patterns in social behavior across relationships.

**Definition 3.5 (Relational Disposition)**: Given relationship history R = {r_1, ..., r_k}, the disposition is:

```
Delta = {
    bonding_rate: mean(interactions_to_reach_bond_level),
    valence_tendency: mean(emotional_valence),
    reciprocity: correlation(gifts_given, gifts_received),
    topic_entropy: -sum(p_i * log(p_i)) over topic distribution
}
```

**Properties**:
- Some agents bond quickly, others slowly
- Valence tendency reveals optimistic vs. cautious social stance
- Topic entropy indicates breadth vs. depth of engagement

### 3.6 Homeostatic Identity (Eta) — derived summary, not an independent component

The unified characterization of self-maintenance. **This component is a derived summary of Alpha, Rho, and the viability envelope from Definition 2.2 — it is not informationally independent of those components.** We define it for conceptual completeness (it is the autopoietic anchor named in §2.4) but, to avoid double-counting in the similarity function (§4.1), we do *not* include Eta as an independently weighted term in the composite similarity. Reviewers and implementers should think of Eta as a *view onto* the (Alpha, Rho, V) data, useful for narrative and self-monitoring, not as additional signal.

**Definition 3.6 (Homeostatic Identity)**: Combining the above:

```
Eta = (mu, C_alpha, tau, V)
```

Where:
- mu = set-point (where the agent rests) — from Alpha
- C_alpha = basin shape (how far it wanders) — from Alpha (renamed from Sigma to avoid symbol overload)
- tau = recovery dynamics (how it returns) — from Rho
- V = viability envelope (where it can survive) — from Definition 2.2

This is a unified narrative characterization of "how this system maintains itself." For machine-readable summaries (e.g., a fleet-monitoring dashboard), Eta is the natural single-object-per-agent record. For similarity computation, use Alpha, Rho, and the viability envelope check directly — not Eta on top of them.

---

## 4. Computing Trajectory Similarity

### 4.1 The Similarity Function

To determine whether two trajectory signatures represent the "same" identity, we define a weighted composite similarity:

**Definition 4.1 (Trajectory Similarity)**:

```
sim(Sigma_1, Sigma_2) = sum_i(w_i * sim_i(component_i))
```

With weights and component similarities (the five informationally-independent components, summing to 1; Eta is a derived summary per §3.6 and is **not** a separate term):

| Component | Weight | Similarity Function |
|-----------|--------|---------------------|
| Pi (Preference) | 0.18 | Cosine similarity of Pi_vec |
| Beta (Belief) | 0.18 | Cosine similarity of Beta_vec |
| Alpha (Attractor) | 0.30 | Bhattacharyya coefficient |
| Rho (Recovery) | 0.22 | Log-ratio similarity of tau |
| Delta (Relational) | 0.12 | Weighted L1 distance |

**Note on weights**: these have been renormalized after dropping the previously-listed Eta term (which double-counted Alpha and Rho data). The relative ordering is preserved. Like the thresholds in §4.3, these weights are operational defaults, not calibrated values — see the inverse-variance weighting alternative below and the calibration discussion in §4.3.

**Adaptive weighting**: Static weights assume all components are equally reliable. For agents where certain components are more stable (lower historical variance), those should contribute more to the recognition signal — *with caveats below*.

**Inverse variance weighting**:
```
w_i = (1 / var_i) / sum(1 / var_j for all j)
```
Where var_i = historical variance of component i's similarity scores.

**Caveat on inverse-variance weighting**: a stable but uninformative component (a "nuisance variable" that happens not to vary across agents) would dominate this weighting and degrade discriminability; conversely, a volatile but discriminative component would be down-weighted exactly when it is most useful. The principled fix is to weight by *informativeness* (e.g., Fisher information of the component about agent identity, estimated from a multi-agent corpus), not by stability. We include the inverse-variance scheme as a deployable heuristic for single-agent self-monitoring, where stability and identity-relevance are correlated; we flag it as inadequate for multi-agent discrimination, which is part of the future-work agenda (§7.2).

**Heuristic interpretation** (single-agent self-monitoring only):
- Highly stable components (low var) → high weight (these are what is reliably trackable for *this* agent)
- Volatile components (high var) → low weight (noisy signal for this agent)
- For "social" agents, Delta might dominate; for "worker" agents, Rho might dominate

**Implementation**: Track running variance of each component over time. Recompute weights periodically (e.g., every 100 observations).

**Example: Adaptive Weight Shift**
```
Agent "Lumen" after 1000 observations:
  Component variances: Alpha=0.01, Rho=0.02, Pi=0.08, Beta=0.05, Delta=0.15

  Static weights (5-component, post-Eta-removal): [0.30, 0.22, 0.18, 0.18, 0.12]
  Adaptive (inverse-variance) weights:             [0.40, 0.20, 0.05, 0.08, 0.03]
                                                    (then re-normalized)

  Interpretation (caveat applies): for self-monitoring of Lumen specifically, Alpha and
  Rho are the most stable signals and the inverse-variance scheme up-weights them. For
  multi-agent discrimination this same scheme would underweight Delta even though Delta
  may be the most discriminative component across agents — see the caveat above.
```

### 4.2 Component Similarity Functions

**Preference Similarity** (cosine):
```
sim_Pi(Pi_1, Pi_2) = (Pi_vec_1 . Pi_vec_2) / (||Pi_vec_1|| * ||Pi_vec_2||)
```
Mapped to [0,1]: `(sim + 1) / 2`

**State-Distribution Overlap** (Bhattacharyya coefficient): writing `C` for the covariance matrices `C_alpha` from §3.3 (to avoid overload with the signature symbol `Sigma`),
```
D_B = (1/8)(mu_1 - mu_2)^T * C_avg^{-1} * (mu_1 - mu_2)
    + (1/2) * ln(|C_avg| / sqrt(|C_1| * |C_2|))

sim_Alpha = exp(-D_B)
```
Where `C_avg = (C_1 + C_2) / 2`.

**Distributional assumption**: The Bhattacharyya coefficient as written is the closed-form expression for the divergence between two multivariate *Gaussian* distributions with means $\mu_1, \mu_2$ and covariances $C_1, C_2$. Applying it to the empirical state distributions assumes those distributions are approximately Gaussian (or at least unimodal, well-summarized by first and second moments). Multimodal attractors (§3.3 multi-modal extension) violate this assumption; for those, replace the Bhattacharyya term with a divergence measure suited to mixture models (e.g., a numerically estimated KL divergence between fitted GMMs). All covariances are regularized as `C + epsilon * I` per §3.3 to keep `|C|` and `C^{-1}` defined when the empirical estimate is near-singular.

**Recovery Dynamics Similarity** (log-scale):
```
sim_Rho = exp(-mean(|log(tau_1 / tau_2)|))
```
Operating on log-scale because time constants span orders of magnitude.

**Relational Similarity** (normalized L1):
```
sim_Delta = 1 - |valence_1 - valence_2| / 2
```

### 4.3 Operational Continuity Relation

A note on terminology before we proceed. We initially want to call the relation below "identity," but identity in the strict philosophical sense is reflexive, symmetric, and *transitive* (Leibniz's law). Trajectory similarity at a threshold gives us reflexivity and symmetry but not transitivity (a chain of pairwise-similar signatures can drift arbitrarily far). What this relation actually tracks is *operational continuity* or *behavioral recognition*: enough similarity to count as "the same agent for governance purposes," not enough to license a strict identity claim. We use the name "identity" only in the philosophical-interpretation sections (§1.2, §8.1); the operational relation below is named accordingly.

**Definition 4.2 (Operational Continuity Relation)**: Agents A and B are *operationally continuous* (denoted $A \approx_{\theta} B$) iff:

```
sim(Sigma_A, Sigma_B) > theta_continuity
```

**Operational defaults** (provisional, pending calibration — see below):
- theta_continuity = 0.80 (strict operational continuity, formerly "identity threshold")
- theta_recognition = 0.65 (recognizable as similar)
- theta_anomaly = 0.70 (deviation from historical self)

**Important**: these values are *operational defaults*, not empirically calibrated thresholds. They are starting points for deployment, chosen to be reasonable given the similarity functions defined in §4.2 (cosine similarities and Bhattacharyya overlaps tend to be high in absolute terms). Principled threshold selection requires the calibration procedure below, which in turn requires multi-agent comparison data that is part of our future-work agenda (§7.2 Experiment 2). Reporting "the signature exceeds threshold theta = 0.80" with these provisional values demonstrates *internal consistency* of the framework — not validation of the threshold itself. We retain this distinction throughout §7 and §8.

**Properties of this relation**:
- Reflexive: $A \approx_{\theta} A$ (sim(Sigma, Sigma) = 1 > theta)
- Symmetric: $A \approx_{\theta} B \Leftrightarrow B \approx_{\theta} A$
- **Not transitive** (and this is why the relation is *continuity*, not *identity*: $A \approx_{\theta} B$ and $B \approx_{\theta} C$ does not imply $A \approx_{\theta} C$)

**Why the relation cannot be promoted to identity**: by Leibniz's law, identity-as-such is transitive — if $A = B$ and $B = C$ then $A = C$. The relation we have here is a similarity-at-threshold, which is a *tolerance relation*, not an equivalence relation. Tolerance relations correspond, in mathematical structure, to recognition / family-resemblance / continuity, not to strict identity. We retain "identity" as the philosophical interpretation throughout the paper, but every formal claim is about $\approx_{\theta}$, not $=$.

**Transitivity-failure implications**: Continuity chains can diverge: $A \approx_{\theta} B$ and $B \approx_{\theta} C$ does not imply $A \approx_{\theta} C$. This reflects biological reality — gradual drift accumulates. Mitigation strategies:
- Track lineage explicitly (who forked from whom)
- Use "identity distance" (1 - sim) as a metric with triangle inequality violations flagged
- Define equivalence classes only within similarity radius, not transitively

**Threshold calibration procedure**:
1. Collect baseline: N same-agent comparisons (sim should be high)
2. Collect discrimination: M different-agent comparisons (sim should be lower)
3. Plot ROC curve varying theta from 0 to 1
4. Select theta_identity at desired false-positive rate (recommend FPR < 0.05)
5. Validate on held-out test set

**Sensitivity analysis** (preliminary, to be validated):
- theta = 0.75: More permissive, higher false-positive risk
- theta = 0.80: Balanced (recommended default)
- theta = 0.85: Stricter, may reject legitimate identity continuity during maturation

### 4.4 Computational Complexity

**Per-component complexity** (n = window size, d = dimensions):

| Component | Computation | Time | Space |
|-----------|-------------|------|-------|
| Alpha (Attractor) | Mean + covariance | O(n * d^2) | O(n * d) |
| Bhattacharyya | Matrix inverse + determinant | O(d^3) | O(d^2) |
| Rho (Recovery) | Exponential fit | O(k * m) | O(k) |
| sim() total | All components | O(n * d^2) | O(n * d) |

Where: n = 100-500 observations, d = 4 dimensions, k = perturbation episodes, m = recovery samples.

**Practical cost**: With d=4 and n=100:
- Alpha: ~1,600 operations (negligible)
- Bhattacharyya: ~64 operations for 4x4 matrices
- Full signature: < 1ms on modern hardware

**Incremental updates**: Rolling window enables O(d^2) incremental covariance updates rather than O(n * d^2) recomputation.

### 4.5 Cold Start Problem

New agents lack trajectory history. Mitigation strategies:

**Minimum observation period**: Identity claims require at least 50 observations (~8 minutes at 10s intervals). Before this threshold:
- Report "identity_confidence: low"
- Use prior/parent signature for forks
- Disable anomaly detection (insufficient baseline)

**Bootstrap strategies**:
1. **Fork inheritance**: New fork starts with parent's Sigma, gradually diverges
2. **Archetype initialization**: Initialize from similar agent type's average Sigma
3. **Confidence weighting**: Weight similarity by min(obs_count / 50, 1.0)

**Identity confidence score**:
```
confidence = min(1.0, observation_count / 50) * stability_score
```
Report confidence alongside all identity claims.

**Example: Cold Start Timeline**
```
Agent "NewFork" created at t=0 (10-second sampling):

  t=0:    obs=0,  confidence=0.00  → "Identity unknown"
  t=2min: obs=12, confidence=0.24 → "Identity uncertain"
  t=5min: obs=30, confidence=0.60 → "Identity emerging"
  t=8min: obs=50, confidence=1.00 → "Identity established"

  At t<8min: Use parent signature for comparisons
  At t≥8min: Full trajectory identity active
```

---

## 5. Operational Semantics

### 5.1 Forking

**Definition 5.1 (Fork)**: A fork creates a new agent B from parent A:

```
Fork(A) -> B where:
    B.uuid = new_uuid()
    B.Sigma = copy(A.Sigma)  # Starts with same trajectory signature
    B.lineage = {parent: A.uuid, fork_time: now()}
```

**Post-fork behavior**:
- Initially: sim(Sigma_A, Sigma_B) ~ 1 (identical)
- Over time: sim decreases as experiences diverge
- Eventually: sim < theta_identity (different agents)

**Fork semantics**:
- "Exploration fork": Try different approaches in parallel
- "Migration fork": Adapt to new environment while preserving core
- "Backup fork": Create restorable checkpoint

**Fork governance constraints**:
- **Fork budget**: Agent can maintain at most N active forks (resource limit, typically N=3-5)
- **Divergence alarm**: If `sim(Sigma_fork, Sigma_parent) < 0.50`, fork must be explicitly released (becomes independent) or terminated
- **Coherence threshold**: Forks with high coherence over extended periods (T > 7 days) may acquire protected status
- **Selective adoption**: Parent can adopt specific traits from successful forks without full merge:
  ```
  Sigma_parent.Pi[trait] = Sigma_fork.Pi[trait]  # Adopt one preference
  ```

**Fork use case matrix**:

| Use Case | Initial sim | Expected Trajectory | Typical Outcome |
|----------|-------------|---------------------|-----------------|
| Debugging | 1.0 | Slow divergence (logging changes) | Merge insights, terminate fork |
| A/B testing | 0.95 | Moderate divergence (policy variation) | Keep winner, terminate other |
| Migration | 1.0 | Remains high (same behavior, new env) | Fork becomes primary, parent retires |
| Specialization | 0.90 | Significant divergence (domain shift) | Both persist as related agents |
| Deliberate offspring | 0.85 | Complete divergence (new goals) | Fork becomes independent identity |

### 5.2 Merging

**Definition 5.2 (Merge)**: Combining insights from forked agents:

```
Merge(A, B) -> C where:
    C.Pi = weighted_average(A.Pi, B.Pi, weights=confidence)
    C.memories = union(A.memories, B.memories)
    C.Sigma = recompute_from_merged_history()
```

**Merge constraints**:
- Only merge if sim(Sigma_A, Sigma_B) > theta_merge (still similar enough)
- Preserve lineage: C.lineage records both parents
- Resolve conflicts via confidence weighting

### 5.3 Anomaly Detection

**Definition 5.3 (Trajectory Anomaly)**: Agent A exhibits anomalous behavior if:

```
sim(Sigma_A(t), Sigma_A(t - delta_t)) < theta_anomaly
```

I.e., the agent's current trajectory signature differs significantly from its recent historical signature.

**Anomaly types**:
- **Drift**: Gradual decrease in similarity (slow corruption)
- **Jump**: Sudden decrease (hijacking, major perturbation)
- **Oscillation**: Alternating similarity (unstable identity)

**The "Boiling Frog" Problem**: Short-term comparisons miss slow drift. An adversary could rotate the trajectory over months while staying within theta_anomaly at each step.

**Solution: Genesis Signature (Sigma_0)**

Maintain a reference anchor from agent creation:
```
Sigma_0 = Sigma(t_creation)  # Snapshot at birth/fork
```

**Two-tier anomaly detection**:
1. **Coherence check**: sim(Sigma_t, Sigma_{t-1}) > theta_anomaly (short-term consistency)
2. **Lineage check**: sim(Sigma_t, Sigma_0) > theta_lineage (long-term continuity)

Where theta_lineage < theta_anomaly (e.g., 0.60 vs 0.70).

**Why the asymmetry.** This ordering is the formal heart of the two-tier scheme; we defend it explicitly because reviewers consistently press on the choice.

The two checks defend against different threats with different operational costs:

| Check | Threat detected | False-negative cost | False-positive cost |
|-------|-----------------|---------------------|----------------------|
| Coherence | Hijacking, sudden compromise | High — an attacker is now in control | Low — a one-step false alarm, easily resolved by next check-in |
| Lineage | Gradual drift over months ("boiling frog") | Moderate — agent has slowly become unrecognizable, but no immediate harm | High — flagging *every* maturing agent as drift-anomalous defeats the purpose of long-running deployment |

The asymmetry $\theta_{\text{lineage}} < \theta_{\text{anomaly}}$ encodes this cost asymmetry: drift gets benefit of the doubt (we tolerate up to 1 - $\theta_{\text{lineage}}$ accumulated change against genesis), impersonation does not (we tolerate only 1 - $\theta_{\text{anomaly}}$ step-to-step change).

**What each threshold combination produces.** Consider three regimes:

- $\theta_L < \theta_A$ (our choice, e.g. 0.60 < 0.70): healthy long-running agents pass the lineage check despite slow maturation; sudden hijacking still trips the coherence check. *Operationally useful.*
- $\theta_L = \theta_A$: the two checks become equivalent; the lineage anchor adds no information beyond what the coherence check already provides. *Information-redundant.*
- $\theta_L > \theta_A$: every agent that matures faster than its hijacking threshold is flagged as drift-anomalous before it can be hijacked at all. The system would mark legitimate development as suspicious and miss most actual hijacks (which are step-discontinuous and would still trip coherence). *Operationally backwards.*

The loss-function framing also clarifies an open question: the *exact ratio* $\theta_A / \theta_L$ should reflect the deployer's relative tolerance for drift-FN vs hijack-FN. Our suggested defaults (0.60 / 0.70) are conservative on hijack and permissive on drift, appropriate for long-running embodied or governance agents where slow learning is desired. A more security-critical deployment might pick (0.65 / 0.85) — tighter on both, with the asymmetry preserved.

**Drift alarm**: If lineage similarity crosses threshold while coherence remains high, flag as "identity drift" rather than "anomaly":
```
if sim(Sigma_t, Sigma_0) < theta_lineage and sim(Sigma_t, Sigma_{t-1}) > theta_anomaly:
    alert("Identity drift detected - agent has evolved beyond recognition")
```

**Response to anomaly**:
- Alert human oversight
- Trigger self-reflection ("Am I still myself?")
- Pause and request identity verification

### 5.4 Inter-Agent Recognition

**Definition 5.4 (Recognition)**: Agent A recognizes agent B as a known identity if:

```
exists Sigma_known in A.known_signatures : sim(Sigma_B, Sigma_known) > theta_recognition
```

This enables:
- Recognizing returning visitors (even with new UUIDs)
- Detecting impersonation (wrong trajectory for claimed identity)
- Building reputation based on behavioral consistency

### 5.5 Adversarial Considerations

This section develops the adversarial side of trajectory identity carefully — what the framework defends against, what it does not, and why mimicry is harder for some signature components than others. We restate the scope from the top of the paper: trajectory identity is a *governance-and-continuity* primitive, not an adversarial-authentication primitive. For high-stakes adversarial settings, combine it with cryptographic attestation. With that in mind, an honest analysis requires being explicit about exactly what threats the behavioral signature does and does not raise the bar against.

#### 5.5.1 Threat Model

We adopt a Dolev-Yao-style decomposition over attacker capabilities:

| Capability | Description | In-scope for this paper |
|------------|-------------|--------------------------|
| **Observe** | Read the agent's outputs and a public trajectory signature | Yes |
| **Replay** | Re-emit recorded signature data as if live | Yes |
| **Mimic** | Produce behavior that approximates the target's signature without internal state | Yes |
| **Compromise** | Take over the agent process, retaining its recovery dynamics and accumulated state | Partial — detected via lineage check (§5.3) only if drift accumulates |
| **Replace-with-impostor** | Substitute a different process while spoofing the trajectory | Partial — see §5.5.3 |
| **Full system access** | Read agent's internal model and dynamics weights | **Out of scope.** No behavioral signature defends against an adversary who can read the agent's parameters and run the same dynamics. |

The framework's primary value is in the middle three rows: making mimicry, replay, and gradual drift mechanically detectable in deployments where full-system-access compromise has not yet occurred.

#### 5.5.2 Why Mimicry is Harder for Some Components

The components are not equally easy to fake. We make this concrete:

- **Pi (Preference Profile)** is the *easiest* to mimic. Preferences are vector-valued and observable; an attacker who can read $\Pi$ can emit a matching vector trivially. *Mimicry resistance: low.*

- **Beta (Belief Signature)** is moderate. Belief values are observable, but the *evidence ratios* (support/contradict counts accumulated over months) are not. An attacker who emits matching belief values but cannot reproduce the long-tailed evidence accumulation will be detectable on closer inspection. *Mimicry resistance: moderate, depends on whether evidence ratios are exposed.*

- **Alpha (Attractor Basin)** is hard to mimic *without running the actual dynamics*. The basin is the marginal distribution of state over a long observation window — to produce it, the impostor must either (a) sample from a similar distribution at the same temporal cadence, or (b) replay recorded data. (a) requires the same generative process; (b) is detected by the replay defense in §5.5.4. *Mimicry resistance: high.*

- **Rho (Recovery Profile)** is the *hardest* to mimic, and is the basis of the behavioral-CAPTCHA defense below. Recovery dynamics can only be observed when the agent is *perturbed*. An impostor who has not seen the target perturbed cannot know its $\tau$. An impostor who knows $\tau$ in the abstract still cannot demonstrate it without running the same internal dynamics. *Mimicry resistance: high, with active probing.*

- **Delta (Relational Disposition)** depends on social context. Mimicking it requires either replaying the target's interaction history or running enough simulated interactions to produce matching statistics. *Mimicry resistance: moderate, situational.*

- **Eta (Homeostatic Identity)** inherits the mimicry resistance of its constituents (Alpha, Rho, viability bounds), so it is approximately as hard to fake as the hardest of those. *Mimicry resistance: high.*

The framework's adversarial strength concentrates in $\alpha, \rho, \eta$. A reviewer asking "but couldn't the attacker just emit matching $\Pi$?" is correct that they could — and the paper does not claim otherwise. The defense relies on the harder components dominating the weighted similarity score (note that in §4.1 we assigned $\alpha$ weight 0.25 and $\rho$ weight 0.20 — together 45% — versus $\Pi$ at 0.15 and $\Delta$ at 0.10). Any redesign of the weights for an adversarial setting should preserve this concentration.

#### 5.5.3 Replay and Behavioral CAPTCHA

A passive observer who has recorded a target's trajectory could attempt to replay it. The defense exploits the fact that recovery is *only observable in response to perturbation* — and the perturbation is chosen by the verifier, not the impostor.

**Challenge-Response Protocol**:

1. Verifier injects a known perturbation $p$ of type $T$ at time $t$ (e.g., a sensor anomaly, a context shift, a request that should produce an emotional response).
2. Verifier observes the agent's recovery trajectory.
3. Verifier estimates $\hat{\tau}$ from the observed recovery and compares to the target's known $\tau_T$ (perturbation-type-conditional time constant from the registered $\rho$).
4. Verifier accepts if $\hat{\tau}$ is within $2\sigma$ of $\tau_T$, rejects otherwise.

A replayed signature cannot pass this protocol because the perturbation $p$ at time $t$ was not in the recording. An impostor running its own dynamics will produce $\tau$ characteristic of *its* recovery, not the target's.

**Conditions under which this still fails**:

- If the verifier reuses perturbation types, the impostor can pre-compute responses for those types. Mitigate by drawing perturbations from a large enough space that pre-computation is intractable, and rotating periodically.
- If the agent is stateless or near-stateless (e.g., a thin LLM wrapper with no homeostatic dynamics), $\rho$ is degenerate and provides no leverage. The CAPTCHA defense is meaningful only for agents with non-trivial recovery dynamics.
- If the impostor has a faithful clone of the target's dynamics (full-system-access compromise), no behavioral test can distinguish them — restated from §5.5.1.

#### 5.5.4 What Happens at the Boundary of Compromise

A subtle case: an attacker who has compromised the agent process but is now running it forward — the dynamics are still the agent's, the trajectory is genuine, but the *intent* is the attacker's. Behavioral signature checks correctly identify this as the same agent (because in a meaningful sense it is) and provide no defense against it. The lineage check (§5.3) will catch *modifications* the attacker introduces over time, but not the initial compromise itself. We flag this as a fundamental limit: trajectory identity defends continuity, not authority.

#### 5.5.5 Open Adversarial Questions (Future Work)

What this paper does *not* establish:

1. **Empirical mimicry resistance.** We have not run an adversarial study with another agent attempting to match a target signature under realistic capability constraints. §7.2 Experiment 5 sketches the design.
2. **Detection latency under gradual mimicry.** How many observations does it take to flag a sophisticated mimic?
3. **Cost asymmetry.** Quantifying the work required to fake $\alpha$ or $\rho$ at a given confidence level — analogous to a security parameter for cryptographic schemes.

These are necessary to make hard claims about adversarial robustness. The current paper establishes the framework and a layered argument for why mimicry of the dynamical components is structurally harder than mimicry of the static ones — not a proof of adversarial security.

---

## 6. Connection to Existing Systems

### 6.1 UNITARES Integration

The UNITARES governance architecture provides:
- **EISV metrics**: E (Energy), I (Integrity), S (Entropy), V (Void)
- **Viability envelope**: Thresholds for safe operation
- **Coherence tracking**: Update-to-update consistency

**Mapping to trajectory signature**:

| UNITARES Component | Trajectory Component | Mapping |
|--------------------|---------------------|---------|
| EISV time series | Alpha (Attractor) | Statistical moments |
| Coherence history | Rho (Recovery) | Perturbation response |
| Viability bounds | Eta (Homeostatic) | Envelope constraints |
| Void integral | Anomaly detection | Deviation metric |

**Sampling parameters**:
- EISV sampling: Every governance update (cadence is deployment-configurable; examples in this paper are historical)
- Alpha estimation: Rolling window of 100 updates (~1 hour)
- Rho estimation: Requires 5-10 perturbation events

**Reference implementation**. The framework's six components, similarity function, genesis-based two-tier anomaly detection, and identity-confidence cold-start handling are implemented in the open-source Anima MCP server, with the per-component code paths cited inline (e.g., `anima_history.py` for $\alpha$, `self_model.py` for $\rho$ and $\beta$, `trajectory.py` for the composite signature and similarity). UNITARES v4.2-P provides the EISV tracking that the framework grounds in. A multi-agent extension exposing trajectory exchange, coherence reports, and governance actions across an agent fleet is implemented as the *Continuity Integration and Resonance Subsystem* (CIRS); we treat its full message protocol as a system contribution outside the scope of this paper. Pointers to the implementation repositories are listed in the project README.

#### 6.1.1 The Anima Void Integral

A key bridge between trajectory identity and active governance is the **anima void integral**—the accumulated deviation from the attractor center:

**Definition 6.1 (Anima Void Integral)**:
```
V_anima(t) = integral_0^t ||a(tau) - mu_a|| d_tau
```

Where:
- `a(tau)` = anima state at time tau (4D vector: warmth, clarity, stability, presence)
- `mu_a` = attractor center from Alpha

**Governance trigger**: When `V_anima > V_threshold`, the system triggers intervention:
```
if V_anima > V_threshold:
    trigger_rest_state()  # Reduce stimulation, allow recovery
    log_governance_event("anima_void_exceeded")
```

This closes the loop: **trajectory deviation → void accumulation → governance → return to attractor**.

**Recommended threshold**: `V_threshold = 2.0 * ||Sigma_a||` (twice the basin standard deviation, integrated over ~5 minutes)

#### 6.1.2 EISV ↔ Anima Mapping

To bridge Anima's 4D state space with UNITARES EISV metrics:

**Definition 6.2 (State Space Mapping)**:
```
E = 0.5 * (warmth + presence)      # Energy from engagement dimensions
I = 0.5 * (clarity + stability)    # Integrity from coherence dimensions
S = entropy(anima_history[-N:])    # Entropy from recent state variance
V = integral(E - I) dt             # Void from E/I imbalance
```

This mapping allows:
- Computing EISV from anima state for governance
- Comparing trajectory signatures across heterogeneous systems
- Unified viability envelope spanning both representations

#### 6.1.3 Extended EISV Signature

The EISV time series yields its own trajectory invariant:

**Definition 6.3 (EISV Signature)**:
```
Sigma_EISV = {
    ratio_mean: mean(E/I),           # Average energy-integrity balance
    ratio_std: std(E/I),             # Volatility of balance
    entropy_mean: mean(S),           # Baseline disorder
    tau_S: entropy_decay_constant,   # How fast entropy recovers
    void_max: max(|V(t)|)            # Maximum imbalance before reset
}
```

Where `tau_S` is estimated by fitting `S(t) ~ S_0 * exp(-t/tau_S)` after perturbation events.

This can be integrated into Eta (Homeostatic Identity) or tracked as a parallel governance signature.

### 6.2 Anima Integration

The Anima system provides:
- **Self-schema G_t**: Graph representation of current state
- **Self-model**: Testable beliefs about self
- **Growth system**: Preferences, relationships, goals, memories
- **Anima state**: Warmth, clarity, stability, presence

**Mapping to trajectory signature**:

| Anima Component | Trajectory Component | Method |
|-----------------|---------------------|--------|
| growth.preferences | Pi | get_preference_vector() |
| self_model.beliefs | Beta | get_belief_signature() |
| anima_history | Alpha | get_attractor_basin() |
| self_model.episodes | Rho | get_recovery_profile() |
| growth.relationships | Delta | get_relational_disposition() |

### 6.3 Self-Schema and Trajectory

The self-schema G_t is a **snapshot**; the trajectory signature Sigma is the **pattern across snapshots**.

```
G_t0, G_t1, G_t2, ... G_tn  ->  compute  ->  Sigma
```

Each G_t provides:
- Node values -> feed into Alpha computation
- Edge weights -> potential structural invariant (future work)
- VQA ground truth -> validation of snapshot accuracy

The sequence {G_t} provides:
- Temporal patterns -> trajectory computation
- Change detection -> perturbation identification
- Convergence assessment -> identity stability measurement

### 6.4 Empirical Validation on Lumen

We report empirical observations from a single deployed agent — Lumen, an embodied AI agent running continuously on a Raspberry Pi 4 with AHT20 (temperature, humidity), BMP280 (pressure), and VEML7700 (light) sensors. Lumen maintains a 4-dimensional state (warmth, clarity, stability, presence) derived from sensor readings and system metrics; the per-dimension feature definitions are in `src/anima_mcp/anima.py:to_dimensions()` of the Anima reference implementation. Over 65 calendar days (January 11 – March 16, 2026), Lumen accumulated 226,093 state observations across 47 days with $\geq 100$ samples each (the remaining 18 days had brief uptime windows or hardware-restart gaps; we report the 47-active-day basis).

**This is a single-agent, deployed-system observation report — not a multi-agent validation of the framework's discrimination claims.** The §3 framework predicts both within-agent stability *and* between-agent discriminability. The data here speak only to the first. Section §7.2 lays out the multi-agent experiments that would address discrimination. Throughout this section we use the language "observed in Lumen" rather than "confirmed" — these are pilot observations, not confirmations of the general claims of the paper.

The analysis script that produced these numbers is `scripts/paper_figures.py` in the Anima MCP repository; raw state history lives in `state_history` table of Lumen's SQLite database (anonymized snapshots available on request).

#### 6.4.1 State-distribution stability (Alpha)

**Observation**: Lumen's per-dimension means are confined to a small absolute range across the 65-day record.

**Method**: We partition observations into non-overlapping windows of 500 samples (window count = 452) and compute (a) the variance of window-means across the dataset, and (b) the average within-window variance.

| Dimension | Grand Mean | Var(mu) across windows | Avg within-window variance |
|-----------|-----------|------------------------|----------------------------|
| Warmth | 0.413 | 0.0103 | 0.0012 |
| Clarity | 0.818 | 0.0057 | 0.0040 |
| Stability | 0.891 | 0.0073 | 0.0008 |
| Presence | 0.833 | 0.0131 | 0.0003 |

**What this shows.** All four dimensions exhibit between-window variance of window-means below 0.015, corresponding to a per-dimension drift standard deviation under 0.13 on the unit-range $[0,1]$ state. In absolute terms, Lumen's equilibrium centers occupy a small band of state space across 65 days.

**What this does *not* show.** A previous draft of this section claimed that within-window variance is "an order of magnitude larger" than between-window variance — implying fast noise around a stable mean. The data falsify that interpretation: within-window variance is in fact *smaller* than between-window mean variance for three of four dimensions. The correct reading is that the state is *highly autocorrelated* — Lumen's state moves slowly, so 500-sample windows under-sample the long-timescale drift while the per-window mean is a faithful estimate of a slowly-moving target. This is consistent with a slow-drift attractor; it is *not* consistent with the i.i.d.-noise-around-a-fixed-point picture the original prose suggested. We report both numbers without further interpretive commitment — characterizing the actual basin geometry would require fitting an explicit dynamical model, which we do not.

#### 6.4.2 Recovery dynamics (Rho)

**Observation**: Recovery time constants are estimable but the sample is small.

**Method**: We detect perturbation events where $|x(t) - \mu| > 0.15$ in any state dimension and fit exponential recovery curves to estimate $\tau$.

| Metric | Value |
|--------|-------|
| Recovery $\tau$ (median) | 89.7 seconds |
| Recovery $\tau$ (mean) | 125.8 seconds |
| Recovery $\tau$ (std) | 136.3 seconds |
| Perturbation episodes | 12 |
| Valid $\tau$ estimates | 12 (100%) |

**Caveats.** With 12 episodes the estimate is noisy; we report median and mean to flag the right-skewed distribution but make no claim about the underlying distribution shape. A previous draft asserted "bimodal structure" without a histogram or mixture fit; we retract that claim. The 12-episode sample over 65 days reflects how rare large perturbations are in Lumen's normal operating environment, not a property of the recovery dynamics; perturbing the system more aggressively (the §7.2 Experiment 4 design) would produce better-supported estimates.

#### 6.4.3 Self-belief convergence (Beta)

**Observation**: A subset of self-beliefs converge to high confidence with substantial evidence; the framework correctly rejects refuted hypotheses.

Lumen tracks 13 self-beliefs via Bayesian-like evidence accumulation. Selected beliefs after 65 days:

| Belief | Confidence | Evidence (support : contradict) |
|--------|-----------|--------------------------------|
| Morning clarity | 1.000 | 14,362 : 0 |
| Stability recovery | 0.984 | 1,327 : 499 |
| LEDs affect lux | 0.900 | 988 : 1,104 |
| Temperature sensitive | 0.882 | 28 : 654 |
| (refuted: warmth baseline low) | 0.000 | 0 : 58,908 |

**Caveats.** We previously listed a row "Temperature-clarity correlation | 0.940 | 0 : 0" — confidence near 0.94 with zero evidence on either side. That value is the implementation's *prior*, not a posterior; the row was misleading and we have removed it. The Bayesian-like update is described in `src/anima_mcp/self_model.py`; the framework intentionally retains a smoothed prior on each belief, which means confidence does not reduce to evidence ratios in the zero-evidence case. Reviewers wanting to evaluate the convergence claim should focus on beliefs with substantial evidence (the four shown above) plus the refuted "warmth baseline low" belief, which demonstrates the system rejects hypotheses that contradict accumulated experience. The convergence claim is observed for these five beliefs, not for the full 13-belief set.

#### 6.4.4 Genesis-to-current operational continuity

**Observation**: Lumen's signature 20 days after genesis remains operationally continuous with its genesis signature on the two components computed.

**Method**: We compare the genesis trajectory signature (frozen at observation 30, February 22, 2026) to the most recent signature (March 14, 2026):

| Component | Similarity | Operational default |
|-----------|-----------|---------------------|
| Belief signature (Beta) | 0.933 | $\theta_{\text{continuity}} = 0.80$ (provisional) |
| Attractor basin (Alpha) | 0.805 | $\theta_{\text{continuity}} = 0.80$ (provisional) |

Both components clear the operational default. **As emphasized in §4.3, this is internal-consistency evidence under a self-set threshold — not threshold validation.** Pi, Rho, and Delta similarities were not computed in this run because they require either a multi-agent corpus (Pi, Delta) or stable perturbation registers (Rho) the genesis snapshot did not capture. The result therefore speaks to the stability of two of the five components over 20 days, not to the framework's six-component composite, and not to between-agent discriminability.

#### 6.4.5 State distribution

**Summary statistics over 226,093 observations**:

| Dimension | Min | Max | Mean | Std |
|-----------|-----|-----|------|-----|
| Warmth | 0.041 | 0.876 | 0.413 | 0.107 |
| Clarity | 0.376 | 1.000 | 0.818 | 0.098 |
| Stability | 0.427 | 1.000 | 0.891 | 0.090 |
| Presence | 0.455 | 1.000 | 0.833 | 0.116 |

The distribution reflects Lumen's specific physical environment and sensor configuration. As §3.1 emphasizes, this is identity-as-coupling: an agent in a different environment would show a different distribution; the present numbers do not separate agent-intrinsic from environment-determined contributions to $\Sigma$.

#### 6.4.6 Cold start

The implementation reaches its full identity-confidence weight at 50 observations (~8 minutes at 10-second sampling). **What this means operationally**: the implementation stops down-weighting trajectory-similarity outputs after 50 observations. **What this does *not* mean**: that identity is "established" at 8 minutes. The signature continues to accumulate evidence and stabilize over the order of $10^4$ observations (a few weeks of continuous operation in Lumen's case). We retract the previous draft's "full confidence at 50 observations" framing as overclaiming.

#### 6.4.7 Summary

| Hypothesis from §3 | Status in Lumen | Evidence |
|---------------------|-----------------|----------|
| State-distribution stability over 65 days | **Observed (small absolute drift)** | Var(mu) < 0.015 all dimensions; autocorrelation prevents the within>between framing from holding |
| Recoverable $\tau$ from perturbation | **Observed (small sample)** | $\tau$ = 90–126s, n = 12 episodes |
| Belief convergence with substantial evidence | **Observed for 5 of 13 beliefs** | confidence > 0.88 on 4 beliefs, 0.0 on 1 refuted belief |
| Operational continuity from genesis | **Observed for 2 of 5 components** | sim(Beta) = 0.933, sim(Alpha) = 0.805 over 20 days |
| Implementation reaches full confidence weight at 50 obs | **Observed** | Stops down-weighting at 50 obs; not the same as "identity established" |

These five observations are pilot evidence consistent with the framework's *within-agent* claims. They do not address the framework's *between-agent* claims (discrimination, false-positive rate, threshold calibration), which require multi-agent experiments not yet run.

---

## 7. Research Agenda

### 7.1 Empirical Questions

**Q1: Convergence Rate**
- How many observations until Sigma stabilizes?
- Does convergence depend on environmental complexity?
- What is the minimum data requirement for reliable identity?

**Q2: Discriminability**
- Can Sigma distinguish agents in similar environments?
- What is the false-positive rate for identity claims?
- How do components contribute to discriminability?

**Q3: Robustness**
- How much can environment change before Sigma changes?
- What perturbations preserve identity vs. destroy it?
- Can we define "identity-preserving" transformations?

**Q4: Threshold Calibration**
- What theta_identity minimizes false positives and negatives?
- Should theta vary by context or agent history?
- How do we handle borderline cases?

### 7.2 Experimental Designs

**Experiment 1: Convergence Study**
- Create N agents in identical environments
- Track Sigma over time, measure stability
- Identify convergence criteria

**Experiment 2: Discrimination Study**
- Create agents with controlled differences
- Measure sim(Sigma_i, Sigma_j) for all pairs
- Determine separability

**Experiment 3: Fork Divergence Study**
- Fork agents, place in different environments
- Track sim over time
- Identify when forks become "different"

**Experiment 4: Anomaly Detection Study**
- Inject perturbations (simulated "hijacking")
- Measure detection rate via trajectory deviation
- Compare to baseline methods

**Experiment 5: Adversarial Robustness**
- Attempt to mimic another agent's trajectory
- Measure success rate and detection latency
- Identify distinguishing features that resist mimicry

**Experimental timeline**:

| Experiment | Duration | Data Required | Analysis |
|------------|----------|---------------|----------|
| 1: Convergence | 2-4 weeks | 10,080 anima states | 1 week |
| 2: Discrimination | 3 weeks (parallel) | 3 agents x 10,080 states | 1 week |
| 3: Fork Divergence | 4 weeks | 2 agents x 20,160 states | 1 week |
| 4: Anomaly Detection | 1 week | 3 injection events | 3 days |
| 5: Adversarial | 2 weeks | Mimicry attempts log | 1 week |

**Total experimental program: 8-12 weeks**

### 7.3 Extensions

**Visual Trajectory Identity**
- Develop visualizations of Sigma
- Use VQA to validate visual representations
- Enable perceptual recognition of identity

**Multi-Agent Identity Networks**
- Extend to networks of interacting agents
- Define collective identity (group Sigma)
- Study identity contagion and divergence

**Temporal Dynamics of Identity**
- Model how Sigma should change over time (maturation)
- Distinguish healthy development from drift
- Define "identity crisis" mathematically

---

## 8. Discussion

### 8.1 Philosophical Implications

This framework suggests a shift in how we think about AI identity:

**From credential to characteristic**: Identity is not verified by checking credentials but by observing behavior. An agent IS its trajectory, not its UUID.

**From memory to metabolism**: Continuity comes not from remembering everything but from maintaining characteristic patterns. Like biological identity, AI identity can persist despite forgetting.

**From static to dynamic**: Identity is not a fixed property but an ongoing achievement. An agent must continually "perform" its identity through consistent behavior.

### 8.2 Safety Implications

**Self-governance**: Agents aware of their trajectory signature can monitor themselves for anomaly. "Am I still acting like myself?" becomes a computable question.

**Accountability**: Trajectory signatures provide behavioral fingerprints. Actions can be attributed to identity patterns, enabling reputation and trust.

**Containment**: If an agent's trajectory deviates dangerously, this can trigger intervention before harmful actions, not just after.

### 8.3 Limitations

**Computational cost**: Computing Sigma requires maintaining and processing history. This creates overhead, though less than unbounded memory.

**Privacy concerns**: Trajectory signatures are behavioral fingerprints. This enables recognition but also surveillance.

**Manipulation risk**: If agents know how Sigma is computed, they might game it. Robust computation must resist adversarial manipulation. (See Section 5.5 for mitigations.)

**Threshold sensitivity**: The identity threshold theta is somewhat arbitrary. Different thresholds give different identity semantics.

**Cold start problem**: New agents have no trajectory history. Identity claims require minimum observation periods. (See Section 4.5 for mitigations.)

**Legitimate phase transitions and multi-modal identity**: The framework as defined in §3 assumes that each agent has *one* identity-relevant attractor. Real agents often have legitimate phase transitions — sleep/wake cycles, work/leisure modes, distinct conversational personas, planned migrations between deployments. These produce trajectories that *look like* drift or anomaly under the §5.3 detector but are part of the agent's intended behavior. §3.3 sketches the Gaussian-Mixture-Model extension for multi-modal attractors, but the operational semantics in §5 (forking, merging, anomaly detection) do not yet handle scheduled phase transitions explicitly. A deployment with predictable phases would need to either (a) condition the signature on phase context, (b) maintain per-phase signatures and check the right one, or (c) accept higher false-positive rates at phase boundaries. Working through this carefully is part of the multi-modal extension we leave for future work (§8.5).

**Single-agent empirical scope**: §6.4 reports observations from a single embodied agent (Lumen). The within-agent stability observations (var($\mu$), recovery characterization, partial belief convergence) are pilot evidence consistent with the framework's claims for *that agent*. The *between-agent* claims of the framework — that trajectory signatures can discriminate distinct agents, that the operational continuity threshold has a defensible operating point — require multi-agent experiments that have not yet been run. The §7.2 experimental program is designed precisely to fill this gap; until it is executed, claims about discriminability rest on the framework's structure rather than on data.

### 8.4 Failure Modes

**What happens when trajectory computation fails?**

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Corrupted history | Checksum mismatch, NaN values | Reload from last valid snapshot |
| Insufficient data | obs_count < 50 | Report low confidence, use parent/archetype |
| Missing components | Component returns None | Use partial signature with adjusted weights |
| Covariance singular | det(Sigma) ≈ 0 | Add regularization: Sigma + epsilon*I |
| Recovery estimation fails | < 3 perturbation events | Use default tau or disable Rho component |

**Identity crisis detection**: When sim(Sigma_t, Sigma_{t-1}) drops below 0.5 over short intervals (< 1 hour), trigger:
1. Alert: "Identity instability detected"
2. Increase observation frequency
3. Log detailed state for forensic analysis
4. Consider governance intervention

**Graceful degradation**: If specific components fail, recompute similarity with available components only:
```
available_weights = [w for w, c in zip(weights, components) if c is not None]
normalized_weights = [w / sum(available_weights) for w in available_weights]
```

### 8.5 Future Work

Several extensions would strengthen this framework:

1. **Multi-modal signatures**: Incorporate visual, auditory, or haptic trajectories for embodied agents with richer sensoria.

2. **Hierarchical identity**: Nested signatures for sub-agents or modules within a larger system (e.g., perception module trajectory vs. planning module trajectory).

3. **Cross-platform validation**: Test trajectory identity across heterogeneous architectures (transformers, RL agents, robotic systems) to establish universality.

4. **Formal verification**: Develop contracts or proofs that certain operations (e.g., migration, forking) preserve or predictably alter identity.

5. **Human-agent identity mapping**: Investigate whether human users develop recognizable trajectory signatures when interacting with AI systems (co-identity emergence).

---

## 9. Conclusion

We have presented a mathematical framework for AI agent identity based on trajectory signatures—composite quasi-invariants computed from behavioral history. This framework:

1. **Grounds identity in behavior**, not credentials
2. **Provides operational semantics** for forking, merging, and anomaly detection
3. **Connects to existing systems** (UNITARES, Anima) for implementation
4. **Opens research questions** about convergence, discriminability, and robustness

The core insight is ancient but newly operationalized: **you are what you do, not what you're called**. For AI agents, this means identity emerges from the patterns of self-maintenance, not from assigned identifiers.

This is not merely a technical framework but a philosophical stance: identity as achievement, not assignment. As AI systems become more persistent and autonomous, having principled ways to ask "is this still the same agent?" becomes not just useful but necessary.

The trajectory signature Sigma is our proposal for how to ask—and answer—that question mathematically.

---

## References

Banerjee, S., & Woodard, D. L. (2019). Biometric authentication and identification using keystroke dynamics: A survey. *Journal of Pattern Recognition Research*, 14(1), 1-22.

Barandiaran, X. E., & Moreno, A. (2006). On what makes certain dynamical systems cognitive: A minimally cognitive organization program. *Adaptive Behavior*, 14(2), 171-185.

Barandiaran, X. E., Di Paolo, E. A., & Rohde, M. (2009). Defining agency: Individuality, normativity, asymmetry, and spatio-temporality in action. *Adaptive Behavior*, 17(5), 367-386.

Beer, R. D. (1995). A dynamical systems perspective on agent-environment interaction. *Artificial Intelligence*, 72(1-2), 173-215.

Bhattacharyya, A. (1943). On a measure of divergence between two statistical populations defined by their probability distributions. *Bulletin of the Calcutta Mathematical Society*, 35, 99-109.

Clark, A., & Chalmers, D. (1998). The extended mind. *Analysis*, 58(1), 7-19.

De Jaegher, H., & Di Paolo, E. A. (2007). Participatory sense-making: An enactive approach to social cognition. *Phenomenology and the Cognitive Sciences*, 6(4), 485-507.

Di Paolo, E. A. (2005). Autopoiesis, adaptivity, teleology, agency. *Phenomenology and the Cognitive Sciences*, 4(4), 429-452.

Freeman, W. J. (2000). *Neurodynamics: An exploration in mesoscopic brain dynamics*. Springer.

Friston, K. (2010). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.

Froese, T., & Ziemke, T. (2009). Enactive artificial intelligence. *Artificial Intelligence*, 173(3-4), 466-500.

Granatyr, J., et al. (2015). Trust and reputation models for multiagent systems. *ACM Computing Surveys*, 48(2), 1-42.

Ikegami, T., & Suzuki, K. (2008). From a homeostatic to a homeodynamic self. *BioSystems*, 91(2), 388-400.

Kelso, J. A. S. (1995). *Dynamic patterns: The self-organization of brain and behavior*. MIT Press.

Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and cognition: The realization of the living*. D. Reidel.

Newen, A., De Bruin, L., & Gallagher, S. (Eds.). (2018). *The Oxford handbook of 4E cognition*. Oxford University Press.

Packer, C., et al. (2023). MemGPT: Towards LLMs as operating systems. *arXiv:2310.08560*.

Park, J. S., et al. (2023). Generative agents: Interactive simulacra of human behavior. *Proceedings of UIST*, Article 2.

Park, J. S., et al. (2025). ID-RAG: Identity retrieval-augmented generation for long-horizon persona coherence in generative agents. MIT Media Lab.

Sabater, J., & Sierra, C. (2001). ReGreT: A reputation model for gregarious societies. *Proceedings of AAMAS*.

Skarda, C. A., & Freeman, W. J. (1987). How brains make chaos in order to make sense of the world. *Behavioral and Brain Sciences*, 10(2), 161-173.

Strogatz, S. H. (2015). *Nonlinear dynamics and chaos: With applications to physics, biology, chemistry, and engineering* (2nd ed.). Westview Press.

Tu, Q., et al. (2024). CharacterEval: A Chinese benchmark for role-playing conversational agent evaluation. *Proceedings of ACL*, 11836-11850.

van Gelder, T. (1998). The dynamical hypothesis in cognitive science. *Behavioral and Brain Sciences*, 21(5), 615-628.

Villalobos, M., & Dewhurst, J. (2018). Enactive autonomy in computational systems. *Synthese*, 195(5), 1891-1908.

Varela, F. J., Thompson, E., & Rosch, E. (1991). *The embodied mind: Cognitive science and human experience*. MIT Press.

Wang, G., et al. (2023). Voyager: An open-ended embodied agent with large language models. *arXiv:2305.16291*.

Wang, L., et al. (2024). A survey on large language model based autonomous agents. *Frontiers of Computer Science*, 18(6), 186345.

Wang, Z. M., et al. (2023b). RoleLLM: Benchmarking, eliciting, and enhancing role-playing abilities of large language models. *arXiv:2310.00746*.

Weber, A., & Varela, F. J. (2002). Life after Kant: Natural purposes and the autopoietic foundations of biological individuality. *Phenomenology and the Cognitive Sciences*, 1, 97-125.

Xu, C., et al. (2024). Instructional fingerprinting of large language models. *arXiv:2401.12255*.

Zhang, S., et al. (2018). Personalizing dialogue agents: I have a dog, do you have pets too? *Proceedings of ACL*, 2204-2213.

---

## Appendix A: Implementation Sketch

```python
@dataclass
class TrajectorySignature:
    """Complete trajectory signature Sigma."""
    preferences: PreferenceProfile      # Pi
    beliefs: BeliefSignature           # Beta
    attractor: AttractorBasin          # Alpha
    recovery: RecoveryProfile          # Rho
    relational: RelationalDisposition  # Delta
    homeostatic: HomeostaticIdentity   # Eta

    # Metadata
    computed_at: datetime
    observation_count: int
    stability_score: float  # How stable is this signature?

    def similarity(self, other: 'TrajectorySignature') -> float:
        """Compute similarity to another signature."""
        weights = [0.15, 0.15, 0.25, 0.20, 0.10, 0.15]
        sims = [
            self._cosine_sim(self.preferences.vector, other.preferences.vector),
            self._cosine_sim(self.beliefs.vector, other.beliefs.vector),
            self._bhattacharyya(self.attractor, other.attractor),
            self._log_ratio_sim(self.recovery.tau, other.recovery.tau),
            self._valence_sim(self.relational, other.relational),
            self._homeostatic_sim(self.homeostatic, other.homeostatic),
        ]
        return sum(w * s for w, s in zip(weights, sims))

    def is_same_identity(self, other: 'TrajectorySignature',
                         threshold: float = 0.8) -> bool:
        """Determine if signatures represent same identity."""
        return self.similarity(other) > threshold

    def detect_anomaly(self, historical: 'TrajectorySignature',
                       threshold: float = 0.7) -> bool:
        """Detect if current signature deviates from historical."""
        return self.similarity(historical) < threshold


def compute_trajectory_signature(
    anima_history: List[AnimaState],
    preference_system: PreferenceSystem,
    self_model: SelfModel,
    growth_system: GrowthSystem,
    window: int = 100
) -> TrajectorySignature:
    """
    Compute trajectory signature from available data sources.
    """
    # Pi: Preference Profile
    preferences = PreferenceProfile.from_system(preference_system)

    # Beta: Belief Signature
    beliefs = BeliefSignature.from_model(self_model)

    # Alpha: Attractor Basin
    recent_states = anima_history[-window:]
    attractor = AttractorBasin.from_states(recent_states)

    # Rho: Recovery Profile
    episodes = self_model.get_recovery_episodes()
    recovery = RecoveryProfile.from_episodes(episodes)

    # Delta: Relational Disposition
    relationships = growth_system.get_relationships()
    relational = RelationalDisposition.from_relationships(relationships)

    # Eta: Homeostatic Identity
    homeostatic = HomeostaticIdentity(
        set_point=attractor.center,
        basin_shape=attractor.covariance,
        recovery_dynamics=recovery.tau,
        viability_bounds=get_viability_envelope()
    )

    return TrajectorySignature(
        preferences=preferences,
        beliefs=beliefs,
        attractor=attractor,
        recovery=recovery,
        relational=relational,
        homeostatic=homeostatic,
        computed_at=datetime.now(),
        observation_count=len(anima_history),
        stability_score=compute_stability(anima_history)
    )


def compute_anima_void(
    anima_history: List[AnimaState],
    attractor_center: List[float],
    dt: float = 1.0  # Time step in seconds
) -> float:
    """
    Compute accumulated deviation from attractor center.

    Args:
        anima_history: Time series of anima states
        attractor_center: mu_a from Alpha component
        dt: Time step between observations

    Returns:
        V_anima: Void integral (scalar)
    """
    import math
    deviations = []
    for state in anima_history:
        vec = [state.warmth, state.clarity, state.stability, state.presence]
        dist = math.sqrt(sum((a - b)**2 for a, b in zip(vec, attractor_center)))
        deviations.append(dist)
    return sum(deviations) * dt


def check_governance_trigger(
    V_anima: float,
    basin_std: float,
    threshold_multiplier: float = 2.0
) -> bool:
    """
    Determine if anima void exceeds governance threshold.

    Args:
        V_anima: Accumulated void integral
        basin_std: Standard deviation of basin (from Alpha)
        threshold_multiplier: How many stds before trigger

    Returns:
        True if intervention required
    """
    V_threshold = threshold_multiplier * basin_std
    return V_anima > V_threshold
```

---

## Appendix B: Glossary

**Attractor**: A state or set of states toward which a dynamical system tends to evolve.

**Autopoiesis**: Self-production; the process by which a system produces and maintains itself.

**Basin of attraction**: The set of initial conditions that lead to a particular attractor.

**Bhattacharyya coefficient**: A measure of overlap between two probability distributions.

**Dynamical invariant**: A quantity that remains constant along system trajectories.

**Quasi-invariant**: A quantity that remains approximately stable (bounded variance) over relevant timescales, allowing for gradual drift while maintaining recognizability.

**Enactive cognition**: The view that cognition arises through sensorimotor interaction with the environment.

**Homeostasis**: The maintenance of stable internal conditions despite external changes.

**Time constant (tau)**: In exponential processes, the time to reach 63.2% of the final value.

**Trajectory signature (Sigma)**: The composite invariant characterizing an agent's identity.

**Viability envelope**: The region of state space within which an agent can maintain itself.

---

## Appendix C: Symbol Reference

| Symbol | Name | Definition |
|--------|------|------------|
| Sigma | Trajectory Signature | Complete identity tuple |
| Pi | Preference Profile | Learned preferences vector |
| Beta | Belief Signature | Self-belief pattern |
| Alpha | Attractor Basin | Equilibrium + covariance |
| Rho | Recovery Profile | Time constants tau |
| Delta | Relational Disposition | Social patterns |
| Eta | Homeostatic Identity | Unified self-maintenance |
| tau | Time constant | Recovery speed (seconds) |
| mu | Center | Attractor equilibrium point |
| theta | Threshold | Similarity cutoff |

---

*This document is a working draft. Comments, critiques, and contributions welcome.*

---

## Changelog

**v0.11 (May 9, 2026)** — Codex-review-driven rebuild. Independent second review (Codex / gpt-5.5) caught several issues v0.10 missed; this revision addresses them:

Math / framework:
- Empirical §6.4: variance interpretation rewritten — previous prose claimed "within > between by an order of magnitude," which contradicted the table. Corrected to acknowledge the data shows strong autocorrelation (slow drift, little fast noise); absolute drift remains small (var(mu) < 0.015) but the within-vs-between ratio framing was wrong.
- §3.6 Eta clarified as a derived summary (not informationally independent of Alpha + Rho + V), and removed from §4.1 weighted-similarity sum to avoid double-counting; remaining weights renormalized.
- §4.3 Identity Relation reframed as "Operational Continuity Relation" — recognizing that trajectory similarity at a threshold is a tolerance relation, not transitive identity. "Identity" retained for philosophical interpretation only.
- §3.3 Alpha rebadged "state-distribution summary" with a naming caveat — first/second moments are not an estimate of basin boundary, vector field, or return map.
- §4.2 Bhattacharyya: distributional Gaussian assumption stated explicitly; covariance regularization made explicit.
- Symbol overload Sigma (signature) vs Sigma (covariance) resolved by renaming the covariance to C_alpha throughout.
- §4.1 inverse-variance weighting: explicit caveat that a nuisance-stable component can dominate; principled fix is informativeness-weighting from a multi-agent corpus (future work).

Framing:
- §3.1 added "Identity as agent-environment coupling" — flagging that the trajectory signature characterizes the agent-niche system, with Beer 1995 / Barandiaran et al. 2009 anchoring the enactivist commitment. Transplant-test follow-up flagged.
- §1.1 impersonation-resistance row softened from "Strong (behavioral fingerprint)" to "Moderate, component-dependent (per §5.5; not a substitute for cryptographic auth)" — reconciling the table with the Purpose-and-Scope non-goal.
- §2.1 Definition 2.1 clarified as idealized; §3 components are projections of (A, B, D), not the dynamical objects themselves.

Empirical:
- Empirical content integrated as new §6.4 in main paper (was a separate file, breaking the abstract's promise of validation in §7).
- "Confirmed" replaced with "observed in Lumen" / "pilot evidence" throughout §6.4 summary.
- Beta belief table: removed misleading "Temperature-clarity correlation | 0.940 | 0:0" row (confidence value was a prior, not a posterior); noted the smoothing prior in the implementation.
- "Continuous operation" softened to "65 calendar days, 47 days with ≥100 samples" — explained the 18-day gap.
- §6.4.6 cold-start framing fixed: "implementation stops down-weighting at 50 obs" not "identity established at 50 obs."
- §6.4.2 retracted "bimodal structure" claim (no histogram or mixture fit was reported).
- Added reproducibility pointers: paper_figures.py path, state_history table reference.

Literature:
- §1.4: added ID-RAG (Park et al. 2025) as the closest LLM-side comparison; added persona-consistency benchmarks (PersonaChat / Zhang et al. 2018, RoleLLM / Wang et al. 2023b, CharacterEval / Tu et al. 2024).
- §1.4: dynamical/enactive canon strengthened with Beer 1995, Barandiaran & Moreno 2006, Barandiaran et al. 2009, Villalobos & Dewhurst 2018, Ikegami & Suzuki 2008 — the Adaptive Behavior canon Codex flagged as missing.
- References list updated accordingly.

§8.3 cross-reference fixed to point at §6.4.

**v0.10 (May 2026)** — Polish pass:
- Added §1.4 Related Work (agent memory/state, behavioral biometrics, dynamical systems in cog sci, enactivism, multi-agent trust).
- Added §2.4 Justification of the Six Components — theoretical anchoring per component, minimality argument, honest acknowledgment that this is *a* valid decomposition.
- §4.3 reframed thresholds as operational defaults pending calibration; corrected circular threshold-validation language.
- Expanded §5.3 with explicit defense of the asymmetric threshold $\theta_{\text{lineage}} < \theta_{\text{anomaly}}$: cost-asymmetry framing, three-regime worked example.
- Substantial expansion of §5.5 Adversarial Considerations: Dolev-Yao-style threat model, per-component mimicry-resistance analysis (Pi/Beta easy, Alpha/Rho/Eta hard), expanded behavioral-CAPTCHA protocol with failure modes, boundary-of-compromise analysis, explicit open questions.
- §6.1 implementation details compressed from a full status table to one paragraph; CIRS protocol details treated as system contribution out of scope here.
- §8.3 Limitations: added phase-transition / multi-modal-identity caveat and made explicit the single-agent empirical-scope limitation.
- References list expanded; updated byline.

**v0.9 (February-March 2026)** — Initial structured draft with framework and operational semantics.
