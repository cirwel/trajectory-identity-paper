# Trajectory Identity

**A Mathematical Framework for Enactive AI Self-Hood**

[![DOI](https://zenodo.org/badge/1233972561.svg)](https://doi.org/10.5281/zenodo.20098168)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Status: Draft](https://img.shields.io/badge/status-draft%20v0.13-orange.svg)](./TRAJECTORY_IDENTITY_PAPER.md)



- 📄 [`TRAJECTORY_IDENTITY_PAPER.md`](./TRAJECTORY_IDENTITY_PAPER.md) — main paper, working draft v0.13 (~10,754 body words; trimmed for journal submission)
- 🖨 [`TRAJECTORY_IDENTITY_PAPER.pdf`](./TRAJECTORY_IDENTITY_PAPER.pdf) — compiled PDF of v0.12 (~30 pages); rebuild via `scripts/build_pdf.sh`
- 📝 [`TRAJECTORY_IDENTITY_WORKSHOP.md`](./TRAJECTORY_IDENTITY_WORKSHOP.md) — workshop variant (current with v0.11 prose; needs v0.12 council-fixes backport before workshop submission)
- 🖨 [`TRAJECTORY_IDENTITY_WORKSHOP.pdf`](./TRAJECTORY_IDENTITY_WORKSHOP.pdf) — compiled workshop PDF (stale; regenerate before submission)
- 📋 [`HANDOFF.md`](./HANDOFF.md) — orientation for any session picking this up cold
- 🔍 [`REVIEW-CODEX-2026-05-09.md`](./REVIEW-CODEX-2026-05-09.md) — independent second-reviewer pass (Codex) that drove v0.11
- 🔍 [`REVIEW-COUNCIL-2026-05-09.md`](./REVIEW-COUNCIL-2026-05-09.md) — three-agent parallel council (dialectic-architect, code-reviewer, live-verifier) that drove v0.12
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

§7 reports validation on **Lumen** — an embodied AI agent on a Raspberry Pi 4, continuous operation since January 2026 — 226,093 state observations over 65 days. The attractor center $\mu$ shows variance < 0.015 across all four anima dimensions over the full observation period, supporting the quasi-invariance hypothesis.

## Status

Working draft v0.11 (May 9, 2026). Pre-peer-review. Archived on Zenodo with concept DOI [10.5281/zenodo.20098168](https://doi.org/10.5281/zenodo.20098168) (auto-resolves to latest version). See [`HANDOFF.md`](./HANDOFF.md) for current priorities and remaining follow-ups (workshop-variant backport, multi-agent discrimination experiment).

**Citation:** see [`CITATION.cff`](./CITATION.cff) for full metadata. The Zenodo concept DOI (auto-resolves to the latest archived version) is `10.5281/zenodo.20098168`. The version DOI for this v0.11.1 release is `10.5281/zenodo.20098169`.

## Related work in the same line

- [**UNITARES v6**](https://github.com/CIRWEL/unitares-paper-v6) ([DOI: 10.5281/zenodo.19647159](https://doi.org/10.5281/zenodo.19647159)) — *Information-Theoretic Governance of Heterogeneous Agent Fleets*. Provides the EISV state vector and class-conditional calibration this paper builds on.
- **Bridge paper** (forthcoming) — late-draft companion piece linking governance (UNITARES) to identity (this paper).

## License

Released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) when published.
