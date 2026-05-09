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

## Status: v0.10 polish pass complete (2026-05-09)

The three priorities the prior session identified are now addressed in the main paper. Reviewers can still press, but the structural gaps the prior session flagged are closed:

| Priority | Where addressed in v0.10 |
|----------|---------------------------|
| Defend $\theta_{\text{lineage}} < \theta_{\text{anomaly}}$ | §5.3 — cost-asymmetry framing, three-regime worked example |
| Develop behavioral-CAPTCHA section | §5.5 — Dolev-Yao threat model, per-component mimicry-resistance, expanded protocol with failure modes |
| Justify "why these six components" | §2.4 — theoretical anchoring per component, minimality argument, honest acknowledgment that this is *a* valid decomposition |

Plus four supporting edits the polish pass added:

- §1.4 Related Work (was absent; backported from workshop variant)
- §4.3 + §7.4 threshold-circularity fix (operational defaults vs validated thresholds)
- §6.1 trimmed from full implementation status table to one paragraph
- §8.3 Limitations expanded with phase-transition / multi-modal-identity caveat and explicit single-agent empirical-scope acknowledgment

References list expanded; byline updated; version bumped to v0.10. See the Changelog at the bottom of the paper for the full diff.

---

## Path to Zenodo DOI (B1 still open)

Zenodo's standard flow is GitHub-integrated: connect Zenodo to a GitHub repo, create a GitHub release tag, Zenodo auto-archives and mints a DOI. To take the v0.10 draft to a citable Zenodo DOI:

1. **Create the GitHub repo.** From `~/projects/trajectory-identity-paper/`:
   ```bash
   gh repo create cirwel/trajectory-identity-paper --public --source=. --remote=origin --push
   ```
   (Or `--private` for a soft launch — Zenodo can still archive private repos.)

2. **Connect Zenodo.** At zenodo.org, sign in with GitHub, enable webhook for `cirwel/trajectory-identity-paper`. (Same account that holds the v6 concept DOI.)

3. **Tag a release.**
   ```bash
   git tag -a paper-v0.10 -m "First Zenodo-archived draft"
   git push origin paper-v0.10
   gh release create paper-v0.10 --title "v0.10: structured polish pass" --notes-file <(awk '/## Changelog/,/v0.9/' TRAJECTORY_IDENTITY_PAPER.md)
   ```

4. **Zenodo mints concept-DOI + version-DOI** automatically. Add the concept-DOI badge to README, update CITATION.cff with the DOI, push the badge update as a doc-only commit.

5. **Update bridge paper references** when bridge paper becomes reachable.

Alternative path if you don't want a public GitHub yet: direct upload to Zenodo via the web UI (drag PDF + CITATION.cff). Same DOI outcome, no automation. Less convenient for future versions.

---

## Open follow-ups beyond v0.10

### B2. Workshop submission target identification
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

### B3. The substantive experimental program
Now that v0.10 honestly flags single-agent scope, the experimental gap is the bottleneck for top-tier conference acceptance. §7.2 sketches five experiments. Experiment 2 (multi-agent discrimination) is the highest-leverage one. Realistic timeline: 2-3 months once a second long-running embodied agent exists.

### B4. Backport v0.10 expansions into workshop variant
Workshop variant (April 1 draft) is closer to publication-ready in some ways (Related Work present) but doesn't have the v0.10 substantive expansions. Before workshop submission, lift the §2.4 minimality argument, §5.3 asymmetry defense, and at minimum the §5.5.1 threat model + §5.5.2 component-resistance analysis into the workshop draft.

---

## What was done across the two sessions on 2026-05-09

**Session 1 (handoff + repo move):**
1. Audited references in `anima-mcp/` (5 code-comment, 5 doc — all soft cross-links).
2. Created `~/projects/trajectory-identity-paper/` (git init on `main`).
3. Moved four drafts out of `anima-mcp/docs/theory/`.
4. Updated 8 anima-mcp references (5 code, 3 live doc); left 2 archive references alone.
5. Wrote initial README.md and HANDOFF.md.
6. Committed both repos. anima-mcp commit `63233a0`.

**Session 2 (v0.10 polish pass):**
1. Backported §1.4 Related Work from workshop into main paper.
2. Added §2.4 Justification of the Six Components.
3. Fixed §4.3 + §7.4 threshold circularity.
4. Expanded §5.3 with explicit asymmetric-threshold defense.
5. Substantially developed §5.5 (Dolev-Yao threat model, per-component analysis, behavioral-CAPTCHA expansion, boundary-of-compromise discussion).
6. Trimmed §6.1 from full status table to one paragraph.
7. Added phase-transition + single-agent caveats to §8.3.
8. Expanded references list (added Banerjee, De Jaegher, Freeman, Froese, Granatyr, Packer, Sabater, Skarda, van Gelder, Wang G., Weber, Xu).
9. Updated byline, bumped to v0.10, added Changelog.
10. Created CITATION.cff.
11. Updated README + this HANDOFF for Zenodo path.

The earlier session's `papers/trajectory-identity/` plan (nested inside unitares, gitignored) was not durable — Kenny's existing convention is one-paper-per-repo at `~/projects/<paper-name>/` (like `unitares-paper-v6/`). This repo follows that pattern.

---

## Conversation context

The substantive prior conversation is in earlier Claude Code sessions and isn't reachable from this thread. This handoff is reconstructed from:

- The text of the previous session's handoff message (which described state — `papers/trajectory-identity/` with two commits — that turned out not to be on disk; the work was the drafts in `anima-mcp/docs/theory/`).
- Direct read of the drafts themselves.
- The auto-memory at `~/.claude/projects/-Users-cirwel/memory/` for project context.

If you need more, the conversation context for the bridge paper specifically lives somewhere outside this filesystem. Don't try to reconstruct it from scratch — wait until it's reachable.
