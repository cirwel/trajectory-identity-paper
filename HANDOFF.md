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
- **arXiv first**, then Zenodo for the citable archival copy.
- **Reference style matches the bridge paper.** When the bridge paper is reachable, align here rather than the other way.
- **Don't renumber section anchors.** The bridge paper cross-cites specific section numbers from this draft. Renumbering breaks those cites.
- **CC BY 4.0** matches v6's licensing.

---

## Three priorities (the polish lift)

These are the substantive gaps between v0.9-draft and submission-ready. Drive on these in order.

### 1. Defend the asymmetric threshold

The asymmetry $\theta_{\text{lineage}} < \theta_{\text{anomaly}}$ is the formal heart of the two-tier detection scheme but is currently asserted rather than derived. The defense needs:

- A clear statement of the loss function being minimized (drift false-negative is operationally cheaper than impersonation false-negative; the asymmetry encodes that).
- A worked example showing what happens at each threshold combination ($\theta_L < \theta_A$, $\theta_L = \theta_A$, $\theta_L > \theta_A$) and why the current choice is principled.
- Connection to the operational semantics in §5 — fork tolerance vs anomaly intolerance fall out of this.

This is where reviewers will press hardest. Treat it as the section that has to land.

### 2. Develop the behavioral-CAPTCHA section

Currently a sketch in §5.5 (Adversarial Considerations). The full development:

- Explicit threat model — what does the attacker know, what can they observe, what can they emit?
- Why behavioral mimicry is harder than credential theft *for the specific signature components* — not a hand-wave to "behaviors are hard to fake."
- Where it fails — sophisticated full-system-access attackers; this paper's scope is governance/continuity, not adversarial authentication. Keep that boundary crisp.

### 3. Address "why these six components"

§3 defines $\Sigma = \{\Pi, \mathrm{B}, \mathrm{A}, \mathrm{P}, \Delta, \mathrm{H}\}$ but the choice of *six* and *these six* is currently presentation-driven. Reviewers will ask: minimal set? Orthogonal? Why not five, why not eight?

The defense path:

- Argue from the theoretical sources: each component maps to a specific commitment in the autopoiesis / free-energy / 4E-cognition stack.
- Show an ablation argument: removing any one collapses a class of identity-distinctions the framework needs to make.
- Acknowledge that the set is **a** valid decomposition, not **the** unique one — and explain why this decomposition is operationally useful for the systems the paper grounds in (UNITARES, Anima).

---

## Blockers (not in priority order — independent)

### B1. GitHub repo creation
Local repo exists at `~/projects/trajectory-identity-paper/` but no remote yet. When ready:
```bash
gh repo create cirwel/trajectory-identity-paper --public --source=. --remote=origin --push
```
Don't push prematurely — the draft is in flux and a public repo with a half-finished paper costs goodwill.

### B2. Draft import from anima-mcp — DONE in this session
Drafts moved out of `~/projects/anima-mcp/docs/theory/` and into this repo. anima-mcp references updated to point here. Earlier handoff listed this as a blocker; it isn't anymore.

### B3. Polish lift
Priorities 1–3 above. This is the substantive work, not paperwork.

---

## What was done in this session (2026-05-09)

1. Audited references in `anima-mcp/` to the four theory files (5 code-comment cross-links, 5 doc cross-links — all soft references, none load-bearing).
2. Created this repo: `~/projects/trajectory-identity-paper/` (git init on `main`).
3. Moved the four drafts out of `anima-mcp/docs/theory/`:
   - `TRAJECTORY_IDENTITY_PAPER.md` (51KB / 1204 lines)
   - `TRAJECTORY_IDENTITY_WORKSHOP.md` (21KB / 278 lines)
   - `TRAJECTORY_IDENTITY_WORKSHOP.pdf` (62KB)
   - `EMPIRICAL_RESULTS_DRAFT.md` (7KB)
4. Updated 5 code-comment references in anima-mcp to point at this repo by name (not URL — no published location yet).
5. Updated 3 live doc references in anima-mcp; left 2 archive references alone.
6. Wrote `README.md` and this `HANDOFF.md`.

The earlier session's `papers/trajectory-identity/` plan (nested inside unitares, gitignored) was not durable — Kenny's existing convention is one-paper-per-repo at `~/projects/<paper-name>/` (like `unitares-paper-v6/`). This repo follows that pattern.

---

## Conversation context

The substantive prior conversation is in earlier Claude Code sessions and isn't reachable from this thread. This handoff is reconstructed from:

- The text of the previous session's handoff message (which described state — `papers/trajectory-identity/` with two commits — that turned out not to be on disk; the work was the drafts in `anima-mcp/docs/theory/`).
- Direct read of the drafts themselves.
- The auto-memory at `~/.claude/projects/-Users-cirwel/memory/` for project context.

If you need more, the conversation context for the bridge paper specifically lives somewhere outside this filesystem. Don't try to reconstruct it from scratch — wait until it's reachable.
