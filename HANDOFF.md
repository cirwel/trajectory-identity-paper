# Handoff — trajectory-identity paper

This file is the cold-start orientation for any session (Claude Code, Codex, human) picking up this repo. Read this first.

---

## Three-paper context

| Paper | Status | Where |
|-------|--------|-------|
| **UNITARES v6** — *Information-Theoretic Governance of Heterogeneous Agent Fleets* | Published, [DOI: 10.5281/zenodo.19647159](https://doi.org/10.5281/zenodo.19647159), latest tag `paper-v6.9.1` | `~/projects/unitares-paper-v6/` · [github.com/CIRWEL/unitares-paper-v6](https://github.com/CIRWEL/unitares-paper-v6) |
| **Trajectory Identity** (this repo) — *A Mathematical Framework for Enactive AI Self-Hood* | Working draft v0.9, pre-submission | `~/projects/trajectory-identity-paper/` |
| **Bridge paper** — links governance to identity | Late draft (not in this session's reach) | TBD — when located, its references list will need updating once this paper has a DOI |

This paper is the **load-bearing standalone**. The bridge paper cross-cites it. v6 doesn't depend on it but provides the EISV state vector and class-conditional calibration it builds on.

---

## Decisions treated as defaults

These were settled in prior sessions; reopen only with new evidence.

- **Publish standalone.** Not nested under v6's repo or DOI. Independent Zenodo concept DOI when published.
- **Zenodo first**, no arXiv (Kenny doesn't have arXiv credentials and arXiv endorsement is friction for Independent Researcher byline). Zenodo issues a citable DOI on the same day as the GitHub release. arXiv cross-post can come later.
- **Reference style matches the bridge paper.** When the bridge paper is reachable, align here rather than the other way.
- **Don't renumber section anchors.** The bridge paper cross-cites specific section numbers from this draft. Renumbering breaks those cites. The v0.10 polish pass added §1.4 and §2.4 — neither disrupts the existing 3.x / 4.x / 5.x numbering the bridge paper cites.
- **CC BY 4.0** matches v6's licensing.

---

## Status: v0.11 — second-reviewer cycle complete (2026-05-09)

After v0.10 was committed, an independent Codex review (gpt-5.5, xhigh reasoning) caught three substantive issues v0.10 missed and several smaller ones. v0.11 addresses them. Codex review preserved at [`REVIEW-CODEX-2026-05-09.md`](./REVIEW-CODEX-2026-05-09.md).

### What Codex caught (v0.10 → v0.11)

| Issue | Status |
|-------|--------|
| Variance interpretation in empirical section was inverted vs the data table (prose claimed within > between, table showed between > within) | **Fixed in §6.4.1** — autocorrelation interpretation; absolute drift claim retained, ratio framing dropped |
| Eta double-counted Alpha and Rho data in the §4.1 weighted similarity sum | **Fixed in §3.6 + §4.1** — Eta now a derived summary, not a weighted term; weights renormalized to 5 components |
| §1.1 table claimed "Strong (behavioral fingerprint)" impersonation resistance — directly contradicts Purpose-and-Scope non-goal | **Fixed** — softened to "Moderate, component-dependent (per §5.5; not a substitute for cryptographic auth)" |
| "Same identity iff sim > theta" + "NOT necessarily transitive" was a logical contradiction (identity is transitive by definition) | **Fixed in §4.3** — relabeled "Operational Continuity Relation"; "identity" reserved for philosophical interpretation |
| §3.3 "Attractor Basin" overclaimed — first/second moments are not basin estimation | **Fixed** — relabeled "state-distribution summary"; honest naming caveat added |
| Symbol overload `Sigma` (signature) vs `Sigma` (covariance) | **Fixed** — covariance renamed to `C_alpha` throughout |
| Bhattacharyya assumptions (Gaussian, regularization) implicit | **Fixed in §4.2** — assumption stated, regularization made explicit |
| Inverse-variance weighting could promote nuisance-stable components | **Fixed in §4.1** — explicit caveat added; informativeness-weighting flagged as principled fix (future work) |
| Beta belief table had "0.940 confidence with 0:0 evidence" row (was a prior, not a posterior) | **Fixed in §6.4.3** — row removed, smoothing prior explained |
| §6.4.6 cold-start framing — "full confidence at 50 obs" misleadingly suggested identity established | **Fixed** — reframed as "implementation stops down-weighting" |
| "Continuous operation" vs "47 active days" inconsistency | **Fixed** — explicit 65-calendar-days / 47-active-days distinction |
| §6.4.2 "bimodal structure" claim with no histogram | **Retracted** |
| Empirical content lived in a separate file; main paper §8.3 referenced "§7 reports validation" but §7 was Research Agenda | **Fixed** — empirical content integrated as §6.4; cross-ref updated |
| Identity-as-coupling not flagged | **Fixed in §3.1** — explicit "Identity as agent-environment coupling" subsection citing Beer 1995 / Barandiaran et al. 2009; transplant test flagged as most informative single follow-up |
| Workshop variant stale relative to v0.10/v0.11 | Still open — see B4 |
| Missing literature: ID-RAG, persona-consistency benchmarks, Adaptive Behavior canon | **Fixed in §1.4** — added ID-RAG (Park 2025), PersonaChat, RoleLLM, CharacterEval; added Beer, Barandiaran, Villalobos & Dewhurst, Ikegami |
| Missing reproducibility pointers | **Partially fixed** — paper_figures.py and state_history table referenced; raw data still on request |

### Three priorities from prior session — still adequate per Codex

| Priority | Where addressed |
|----------|-----------------|
| Defend $\theta_{\text{lineage}} < \theta_{\text{anomaly}}$ | §5.3 (v0.10; Codex confirmed adequate) |
| Develop behavioral-CAPTCHA section | §5.5 (v0.10; Codex confirmed adequate) |
| Justify "why these six components" | §2.4 (v0.10; v0.11 also clarified Eta is a summary not a 6th independent component, narrowing the framework to 5 informationally-independent + 1 narrative wrapper) |

### Reviewer-grade verdict on v0.11 (Codex's projection of where v0.11 lands)

Codex's v0.10 verdict was "Major revision" for Adaptive Behavior, "Borderline" for NeurIPS workshop, "Reject" for top-tier conference. The v0.11 fixes address most of the journal-blocker concerns Codex named, but **two structural limits remain unchanged and would need new experiments to clear**:

- N=1 empirical scope (single-agent observations only)
- No multi-agent discrimination experiment (the central testable framework prediction)

The v0.11 paper is honest about these limits throughout. Codex's likely v0.11 verdict (extrapolating from the review): journal Major-revision is now achievable in 1–2 review cycles rather than blocked outright; workshop Borderline → likely Accept with the v0.11 caveats lifted into the workshop variant.

---

## Closed milestones

### B1. GitHub repo + Zenodo DOI — **DONE 2026-05-09**
Repo: <https://github.com/cirwel/trajectory-identity-paper> (public)
Concept DOI (cite this): [10.5281/zenodo.20098168](https://doi.org/10.5281/zenodo.20098168) — auto-resolves to latest version
Version DOI (paper-v0.11.1): [10.5281/zenodo.20098169](https://doi.org/10.5281/zenodo.20098169)
Zenodo metadata verified clean (title, author, license, abstract, keywords picked up from CITATION.cff).

### B4. Workshop-variant backport — **DONE 2026-05-09**
`TRAJECTORY_IDENTITY_WORKSHOP.md` brought current with v0.11 prose: variance interpretation, operational-continuity reframe, Eta double-counting fix, "Confirmed" → "observed in Lumen", continuous/47-active-days clarification, identity-as-coupling subsection, threshold-circularity acknowledgment, expanded references (ID-RAG, persona-consistency benchmarks, Beer, Barandiaran et al., Villalobos & Dewhurst, Ikegami).
**Note**: `TRAJECTORY_IDENTITY_WORKSHOP.pdf` is now stale relative to the .md. Regenerate before any actual workshop submission (pandoc or LaTeX, depending on the workshop's preferred format).

---

## Open follow-ups beyond v0.11.1

### B5. Multi-agent discrimination experiment (the deferred substantive blocker)
The framework's between-agent claims are not yet empirically tested. §7.2 Experiment 2 sketches the design. Realistic timeline: 2–3 months once a second long-running embodied agent exists. This is the gating experiment for top-tier conference acceptance and for principled threshold calibration.

### B6. Transplant test for identity-as-coupling (sharper, smaller experiment)
Move Lumen (or an instance) to a different physical environment and re-measure $\Sigma$. Components that shift under transplant are coupling-determined; components that remain stable are agent-intrinsic. Smaller-scope than B5, high-information-density. §3.1 flags this as the most informative single follow-up.

### B7. Adaptive Behavior journal submission preparation
v0.11.1 is in defensible state for journal submission. Pre-submission tasks:
- Convert markdown to journal's preferred format (LaTeX with SAGE class, or Word per their submission portal)
- Cover letter framing the contribution (identity-as-trajectory operationalized in a deployed system; companion to UNITARES)
- Mandatory AI-use disclosure (SAGE policy: state how AI was/wasn't used in writing)
- Include the Codex review (`REVIEW-CODEX-2026-05-09.md`) reference if useful for transparency
- Submit at <https://journals.sagepub.com/home/adb>

### B8. Companion bridge paper references update
When the bridge paper (linking governance to identity) becomes reachable, update its references to cite this concept DOI (`10.5281/zenodo.20098168`).

### B9. Workshop PDF regeneration
The compiled `TRAJECTORY_IDENTITY_WORKSHOP.pdf` is stale. Before any workshop submission: pandoc-convert the current .md to PDF, or convert to LaTeX with the workshop's style file.

---

## Workshop submission target identification (B2)
v0.10 is workshop-submittable. Researched venues as of 2026-05-09:

**Recommended primary target — `Adaptive Behavior` (SAGE journal):** Official journal of the International Society for Adaptive Behavior. Bimonthly peer-review. Topics include embodied cognition, AI, artificial life, coordination dynamics, evolutionary robotics — direct fit for the autopoiesis-to-dynamical-systems framing. **Rolling submissions, no deadline pressure.** This is the natural long-form home for this paper and avoids the conference-cycle race entirely. Note SAGE's mandatory AI-use disclosure (state how AI was/wasn't used in writing) at submission. https://journals.sagepub.com/home/adb

**Future conference target — NeurIPS 2026 workshops (December 11-13, Sydney/Paris/Atlanta):** Workshop *proposals* due 2026-06-06. Workshop *paper* CFPs from accepted workshops typically appear August-September 2026. Strategy: post v0.10 to Zenodo now (citable preprint), watch for accepted workshops in agent identity / embodied AI / multi-agent safety topics, submit once CFPs open. https://neurips.cc/Conferences/2026/CallForWorkshops

**Closed for 2026 cycle:**
- ICML 2026 workshops — paper submission deadline was 2026-04-24, past. (44 accepted workshops, two adjacent: "Compositional Learning: Safety, Interpretability, and Agents"; "Statistical Frameworks for Uncertainty in Agentic Systems".) Worth tracking for ICML 2027.
- ICLR 2026 workshops — held April 2026, past. (Strong-fit workshops were "Lifelong Agents: Learning, Aligning, Evolving", "MemAgents", "Agents in the Wild".) Worth tracking for ICLR 2027.
- AAAI 2026 — held February 2026, past. AAAI 2027 calls open ~June-July 2026.

**Secondary journal targets (rolling, no deadline):**
- Frontiers in Robotics and AI
- Cognitive Systems Research
- Artificial Life (MIT Press)

Workshop variant (`TRAJECTORY_IDENTITY_WORKSHOP.md`) is the version to submit to a workshop — shorter and already has Related Work. It does *not* yet incorporate the v0.10 expansions to §5.3, §5.5, §2.4 — backporting those to the workshop variant is a B4 task.

For the Adaptive Behavior journal target, the *long* paper (`TRAJECTORY_IDENTITY_PAPER.md` v0.10) is the right unit. Word count is appropriate for the journal's typical article length.

---

## Session log (2026-05-09)

**Session 1 (handoff + repo move):**
- Audited references in `anima-mcp/`. Created `~/projects/trajectory-identity-paper/` (git init on `main`). Moved four drafts out of `anima-mcp/docs/theory/`. Updated 8 anima-mcp references; committed `63233a0`. Wrote initial README and HANDOFF.

**Session 2 (v0.10 polish pass — three-priority fixes):**
- §1.4 Related Work backported. §2.4 component justification. §4.3 / §7.4 threshold circularity. §5.3 asymmetric-threshold defense. §5.5 Dolev-Yao + per-component mimicry analysis. §6.1 compressed. §8.3 phase-transition + single-agent caveats. References expanded. Bumped to v0.10; trajectory-identity-paper commit `70ce1a1`.

**Session 3 (v0.11 — second-reviewer cycle):**
- Summoned Codex (gpt-5.5, xhigh) for adversarial second review (`REVIEW-CODEX-2026-05-09.md`).
- Codex caught three issues Claude missed (variance inversion, Eta double-counting, §1.1 contradiction) plus several smaller ones.
- v0.11 fixed all of these — see "What Codex caught" table above.
- Empirical content integrated as §6.4. EMPIRICAL_RESULTS_DRAFT.md deleted (superseded).

**Session 4 (publication + workshop backport):**
- Created public GitHub repo cirwel/trajectory-identity-paper, pushed v0.11, tagged paper-v0.11 release.
- User enabled Zenodo webhook; tagged paper-v0.11.1 trigger release.
- Zenodo minted concept DOI 10.5281/zenodo.20098168 (auto-latest) + version DOI 10.5281/zenodo.20098169.
- Updated README with DOI badge; CITATION.cff with DOI metadata.
- Backported v0.11 fixes into workshop variant (B4 DONE).
- Verified Zenodo record metadata is clean (no manual UI edits needed).

---

## Conversation context

The substantive prior conversation is in earlier Claude Code sessions and isn't reachable from this thread. This handoff is reconstructed from:

- The text of the previous session's handoff message (which described state — `papers/trajectory-identity/` with two commits — that turned out not to be on disk; the work was the drafts in `anima-mcp/docs/theory/`).
- Direct read of the drafts themselves.
- The auto-memory at `~/.claude/projects/-Users-cirwel/memory/` for project context.

If you need more, the conversation context for the bridge paper specifically lives somewhere outside this filesystem. Don't try to reconstruct it from scratch — wait until it's reachable.
