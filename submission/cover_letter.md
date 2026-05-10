# Cover letter — Adaptive Behavior submission

To the Editor, *Adaptive Behavior*:

I am submitting *Trajectory Identity: A Mathematical Framework for Enactive AI Self-Hood* for consideration as an original research article in *Adaptive Behavior*.

## Summary

The paper proposes that AI agent identity should be defined by the dynamical patterns that persist in an agent's behavior — what I call a **trajectory signature** — rather than by static identifiers (UUIDs, session tokens) or accumulated memory stores. The framework operationalizes commitments from autopoiesis (Maturana & Varela), enactivism (Di Paolo, Beer, Barandiaran et al.), and the free-energy principle (Friston) into a six-component composite signature computable from observable behavioral data, and reports pilot empirical results from 65 days of continuous operation of an embodied AI agent (Lumen) on a Raspberry Pi 4.

## Why *Adaptive Behavior*

The paper sits at the intersection of three of the journal's stated topic areas:
1. **Embodied cognition** and enactive identity (Sections 2.1, 3.1).
2. **Dynamical systems** in cognitive science and AI (Sections 2.4, 3.3, 6.4).
3. **Autonomous artificial systems** with measurable adaptive dynamics (Section 6, all of the empirical reporting in §6.4).

The core contribution is a formal mapping from enactive concepts to measurable dynamical signatures *in deployed AI systems* — to my knowledge the first such mapping in the literature this journal serves. The empirical work on Lumen complements simulated artificial-life work (e.g., Ikegami & Suzuki 2008) by showing that homeodynamic self can be operationalized in a continuously-running embodied agent rather than only in simulation.

## Honest framing of contribution and scope

The paper is forthright about its empirical scope. The reported observations are **single-agent, within-agent stability** evidence consistent with the framework's quasi-invariance hypothesis. The framework's *between-agent discrimination* claims are explicitly flagged as future work (§7.2 Experiment 2), and the paper has been revised through three independent review passes (preserved as `REVIEW-CODEX-2026-05-09.md` and `REVIEW-COUNCIL-2026-05-09.md` in the public repository) to ensure the prose does not overclaim what the data support. A negative pilot result on cross-LLM discrimination is reported in `experiments/cross-llm-discrimination/results.md` to prevent a reviewer asking "did you try?" from finding a silent gap.

## Provenance and reproducibility

The paper, raw analysis script, experimental data, and all three review passes are publicly archived at:

- GitHub: <https://github.com/cirwel/trajectory-identity-paper>
- Zenodo concept DOI: [10.5281/zenodo.20098168](https://doi.org/10.5281/zenodo.20098168) (auto-resolves to latest version)
- Author ORCID: [0009-0006-7544-2374](https://orcid.org/0009-0006-7544-2374)

The reference implementation of the framework's components lives in the open-source [Anima MCP](https://github.com/cirwel/anima-mcp) repository (see §6.1 of the manuscript).

## AI-use disclosure

Per SAGE's policy on AI use in scholarly publishing: this manuscript was developed with substantial assistance from large language models in the role of *editorial reviewers and analysis tooling*. Specifically: Anthropic's Claude (Claude Code CLI, GPT-equivalent role) was used to draft and revise prose under the author's direction; OpenAI's Codex (gpt-5.5) was used as an independent second-pass reviewer; a parallel three-agent review council was used as a third pass. All conceptual contributions, framework design, empirical observations, and final-decision authority remain the author's. The full drafting and review trail is preserved in the public Git history for transparency.

## Suggested reviewers

Researchers whose published work most directly engages the substantive questions the paper raises:

- **Tom Froese** (Embodied Cognitive Science, OIST) — on enactive AI and constitutive autonomy; co-author of Froese & Ziemke (2009) cited in §1.4.
- **Ezequiel Di Paolo** (IKERBASQUE / University of the Basque Country) — on autopoiesis, adaptivity, and the dynamical-systems framing of identity; cited extensively in §1.4 and §2.4.
- **Xabier Barandiaran** (University of the Basque Country) — on defining agency (Barandiaran, Di Paolo & Rohde 2009 cited in §1.4); the most directly-relevant Adaptive Behavior contributor.
- **Takashi Ikegami** (University of Tokyo) — on homeodynamic self in artificial systems (Ikegami & Suzuki 2008 cited in §1.4).
- **Randall Beer** (Indiana University) — on dynamical-systems perspective on agent-environment interaction (Beer 1995 cited in §1.4).

## Author and affiliation

Kenny Wang
Independent Researcher, CIRWEL Systems
founder@cirwel.org
ORCID: 0009-0006-7544-2374

Thank you for considering this submission.

Sincerely,
Kenny Wang
