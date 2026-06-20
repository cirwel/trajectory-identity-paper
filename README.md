# Trajectory Identity

**A Mathematical Framework for Enactive AI Self-Hood**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20098168.svg)](https://doi.org/10.5281/zenodo.20098168)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: Archived](https://img.shields.io/badge/status-v0.14%20archived-blue.svg)](./TRAJECTORY_IDENTITY_PAPER.md)

> **Plain-language summary.** What makes an AI agent recognizably itself isn't its UUID, its credentials, or its saved memory — it's the way it behaves over time. Recurrent patterns of attention, recovery from interruption, preferences across similar situations. This paper formalizes that intuition: identity as the *dynamical signature* of a running agent, computed from time-series of internal state. The result is an observability-grounded framework for "is this still the same agent?" that doesn't rely on credentials, and detects impersonation differently than ordinary drift. Grounded in 65 days of pilot observations from one long-running embodied AI agent (Lumen, ~226,000 readings) — single-agent evidence for within-agent stability — plus a first multi-agent pilot (§6.5) that significantly discriminates four agents within one operator's ecosystem; external validation is still ahead.



- 📄 [`TRAJECTORY_IDENTITY_PAPER.md`](./TRAJECTORY_IDENTITY_PAPER.md) — main paper, working draft v0.14 (~11,500 body words; adds §6.5 multi-agent discrimination pilot)
- 🖨 [`TRAJECTORY_IDENTITY_PAPER.pdf`](./TRAJECTORY_IDENTITY_PAPER.pdf) — compiled PDF of v0.14 (~32 pages); rebuild via `scripts/build_pdf.sh`
- 📝 [`TRAJECTORY_IDENTITY_WORKSHOP.md`](./TRAJECTORY_IDENTITY_WORKSHOP.md) — workshop variant (needs backport to current v0.14 prose before workshop submission)
- 🖨 [`TRAJECTORY_IDENTITY_WORKSHOP.pdf`](./TRAJECTORY_IDENTITY_WORKSHOP.pdf) — compiled workshop PDF (stale; regenerate before submission)
- 🧪 [`experiments/cross-llm-discrimination/`](./experiments/cross-llm-discrimination/) — cross-LLM discrimination pilot (negative result, informs §7.3)
- 📊 [`scripts/analysis_v0.11.1.py`](./scripts/analysis_v0.11.1.py) — reproducibility script for §6.4.1 with bootstrap CIs and AR(1) coefficients

---

**In one line:** Identity as the dynamical invariant of an agent's behavior — attractor basin, recovery profile, preference profile — rather than a UUID, a credential, or accumulated memory.

---

## What the paper argues

Modern AI agents are identified by static tokens: UUIDs, session IDs, API keys. These confer identity from outside; an agent has an identity because we gave it one, not because it developed characteristics that make it recognizably itself. This produces well-known failure modes: lost-token continuity collapse, ambiguous fork semantics, anomaly-blindness to compromised-but-credentialed agents, and unbounded memory growth as the substitute solution.

The paper proposes an alternative grounded in enactive cognition and dynamical systems theory: a **trajectory signature** $\Sigma = \{\Pi, \mathrm{B}, \mathrm{A}, \mathrm{P}, \Delta, \mathrm{H}\}$ composed of six quasi-invariant components — preference profile, self-belief signature, attractor basin, recovery profile, relational disposition, and homeostatic identity — computed from time-series of agent state.

Three structural moves:

1. **Identity as process, not property.** Following autopoiesis (Varela, Thompson, Rosch) and the free-energy principle (Friston), the identity of a system *is* the pattern of self-maintenance, not any particular configuration.

2. **Two-tier anomaly detection.** Coherence violations and lineage violations are detected against asymmetric thresholds, with $\theta_{\text{lineage}} < \theta_{\text{anomaly}}$ — drift gets benefit of the doubt, impersonation does not.

3. **Operational semantics for fork, merge, and recognition.** Trajectory similarity replaces credential equality as the primitive for "is this the same agent?", with bounded storage (O(window size), not O(unbounded memory)).

## Empirical grounding

§6.4 is a single-agent observation report on **Lumen** — an embodied AI agent on a Raspberry Pi 4, in continuous operation since January 2026 — ~226,029 state observations over 65 calendar days (47 active days with ≥100 samples each). The attractor center $\mu$ shows between-window variance below 0.015 across all four anima dimensions: pilot evidence consistent with *within-agent* quasi-invariance. §6.4 is itself single-agent; the framework's discrimination claims are addressed by **§6.5**, a first multi-agent pilot — significant discrimination across four resident agents within one operator's ecosystem (the first direct evidence for the discrimination criterion), with independent-operator/harness validation still in the research agenda (§7.2).

## Status

Working draft **v0.14** (June 2026), archived on Zenodo. The concept DOI [10.5281/zenodo.20098168](https://doi.org/10.5281/zenodo.20098168) auto-resolves to the latest archived version (now **v0.14**, which adds §6.5, a first multi-agent discrimination pilot). Remaining follow-ups: workshop-variant backport; escalating the discrimination study beyond a single operator's fleet.

**Citation:** see [`CITATION.cff`](./CITATION.cff) for full metadata. The Zenodo concept DOI (auto-resolves to the latest archived version) is `10.5281/zenodo.20098168`.

## Related work in the same line

- [**UNITARES v6**](https://github.com/cirwel/unitares-paper-v6) ([DOI: 10.5281/zenodo.19647159](https://doi.org/10.5281/zenodo.19647159)) — *Information-Theoretic Governance of Heterogeneous Agent Fleets*. Provides the EISV state vector and class-conditional calibration this paper builds on.
- **Bridge paper** (forthcoming) — late-draft companion piece linking governance (UNITARES) to identity (this paper).

## License

Released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) when published.
