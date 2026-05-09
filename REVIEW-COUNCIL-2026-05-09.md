# Council Review of v0.11.1 — 2026-05-09 (third independent pass)

**Reviewers (parallel):** dialectic-knowledge-architect (conceptual frame) · feature-dev:code-reviewer (internal consistency) · live-verifier (ground-truth check of named artifacts).
**Brief:** find what Claude (v0.10) and Codex (v0.11) missed. Read-only review of `TRAJECTORY_IDENTITY_PAPER.md` v0.11.1 archived at DOI 10.5281/zenodo.20098168.

---

## Headline finding (dialectic-architect)

**The §2.4 minimality argument is structurally hollowed out by the §6.4 / §8.3 honesty pass, and the polish passes did not face this.** Each section is locally sound; their combination is not.

§2.4 justifies the six-component decomposition by *between-agent discriminability* — "removing any single component creates an identity-distinction the framework can no longer represent." The discriminability premise is asserted but **never demonstrated**: §6.4 explicitly acknowledges single-agent scope, §8.3 says between-agent claims require multi-agent experiments not yet run, and the cross-LLM experiment in `experiments/cross-llm-discrimination/` produced discrimination ratio 0.87 — within-cell variance swallows between-cell distance.

Result: §2.4's minimality argument is now circular — *the six components are minimally necessary because each preserves a discrimination capacity the framework has elsewhere conceded it has not demonstrated.* This is a level above Codex's variance-prose fix (which corrected one inverted claim); this corrupts the *cardinality* of the decomposition that the rest of §3, §4, §5 are built on.

A second symptom: the §2.1 autopoiesis-to-attractor translation. Autopoiesis is network-topological (closure of self-production); attractor dynamics is state-space. §3.3 then concedes Alpha is a state-distribution summary, not a basin. §3.6 demotes Eta — the only component carrying the autopoietic anchor — to a "derived view." By the time we reach Σ, every link in the autopoietic chain has been weakened or downgraded except the names. §2.4 still cites Eta as "the autopoietic anchor" while §3.6 says it's not an independent component.

**Why prior reviews missed it**: Claude added the §2.4 minimality argument *as the fix* in v0.10. Codex worked the empirical wing in v0.11. Neither reviewer asked whether the layers are mutually consistent. The §2.4 minimality argument was added *before* §3.6's Eta demotion and *before* §6.4's single-agent honesty pass — and was not revisited when those changes landed.

---

## Code-review-style findings (feature-dev:code-reviewer)

### Blocker
- **Appendix A `similarity()` method retains the 6-weight Eta scheme** `[0.15, 0.15, 0.25, 0.20, 0.10, 0.15]`, directly contradicting §4.1's renormalized 5-weight table after Eta's §3.6 demotion. This is in the reference implementation that's most likely to be copied into a real codebase. Citable archive currently ships internally inconsistent code.

### Major (5)
- **§5.5.2 cites old weight values** (Alpha 0.25, Rho 0.20, Pi 0.15, Delta 0.10) when arguing that Alpha and Rho dominate. The renormalized §4.1 values are 0.30, 0.22, 0.18, 0.12. Argument unaffected; numerics wrong.
- **§4.3 calibration procedure step 4** still uses `theta_identity` — inside the section that just retired the name. Two more occurrences at §5.1 (Forking, "Eventually: sim < theta_identity") and §7.1 Q4 ("What theta_identity minimizes false positives").
- **§3.3 properties bullet** still uses `Sigma` (covariance) twice — was supposed to be renamed to `C_alpha` per the v0.11 symbol-overload fix.
- **§8.4 Failure Modes table** uses `Sigma` for covariance (`det(Sigma) ≈ 0`, `Sigma + epsilon*I`) — same rename gap.
- **§2.4 Eta minimality bullet** ("Without Eta: have basin and recovery as separate facts but no unified self-maintenance signature; lose the autopoietic anchor") contradicts §3.6's explicit "do not include Eta as an independently weighted term." This is the textual surface of the dialectic-architect's headline finding.

### Minor (5)
- §1.3 Contribution 2 says "detecting identity" — undermines §4.3's careful operational-continuity reframe at the top of the paper.
- §6.1 UNITARES mapping table maps "Viability bounds → Eta" without footnoting §3.6's caveat that Eta is a view, not a sink.
- Appendix C Symbol Reference defines Eta as "Unified self-maintenance" with no acknowledgment of derived/non-independent status.
- §5.1 Forking and §7.1 Q4 (above) — same `theta_identity` rename misses.

### Calibration check (good news)
- §6.4.1 variance rewrite is clean — within/between framing dropped, autocorrelation reading installed, no residue.
- §4.3 operational-continuity reframe holds consistently across §4.3, §5.3, §6.4.4, §8.3 (modulo the theta_identity stragglers).
- §6.4.3 Beta table fix is precise — bad row removed, smoothing prior explained.

---

## Live-verification findings

| # | Claim | Result |
|---|-------|--------|
| 1 | Zenodo record 20098169 metadata matches CITATION.cff | ✅ verified |
| 2 | Concept DOI 10.5281/zenodo.20098168 resolves | ✅ verified |
| 3 | UNITARES v6 DOI 10.5281/zenodo.19647159 resolves; abstract matches | ✅ verified |
| 4 | anima-mcp source files cited in §6.1 exist with claimed content | ⚠️ **partial: §6.1 implementation table cites `growth.relationships`, that module does NOT exist; correct module is `growth/visitors.py` (line 262 has `get_relational_disposition()`).** |
| 5 | `scripts/paper_figures.py` exists with attractor + recovery functions | ✅ verified |
| 6 | Lumen sensor models (AHT20, BMP280, VEML7700) match deployed config | ✅ verified |
| 7 | UNITARES EISV dimension labels match runtime | ✅ verified (paper says "Void" for V; matches `eisv_format.py`) |
| 8 | UNITARES governance MCP port 8767 | ✅ verified |
| 9 | "226,093 state observations across 47 active days" Jan 11–Mar 16 | ❌ **DB query on May 9 backup returns 226,029 not 226,093 (delta 64). 47-active-day count matches.** |
| 10 | `REVIEW-CODEX-2026-05-09.md` exists in repo | ✅ verified |

**Two refutations** in a citable Zenodo record:
- Wrong filename in §6.1 implementation table (`growth.relationships` doesn't exist).
- Observation count off by 64 (226,093 → 226,029) for the cited window.

---

## v0.12 edit list (from this council)

### Mechanical fixes (~30 minutes total; could ship as v0.11.2 patch)

| # | Section | Fix |
|---|---------|-----|
| M1 | Appendix A | Drop Eta from `similarity()` weights; renormalize to `[0.18, 0.18, 0.30, 0.22, 0.12]` |
| M2 | §5.5.2 | Update weight citations: Alpha 0.30, Rho 0.22, Pi 0.18, Delta 0.12 |
| M3 | §4.3 step 4, §5.1 Forking, §7.1 Q4 | `theta_identity` → `theta_continuity` (3 occurrences) |
| M4 | §3.3 properties, §8.4 Failure Modes | `Sigma` (covariance) → `C_alpha` (4 occurrences) |
| M5 | §6.1 implementation table | `growth.relationships` → `growth.visitors` |
| M6 | §6.4 observation count | `226,093` → `226,029` (or document which DB snapshot the original numbers came from) |
| M7 | §1.3 Contribution 2 | "detecting identity" → "detecting operational continuity" |
| M8 | §6.1 UNITARES table | Add footnote: "Eta is a derived summary (§3.6); viability bounds flow through Alpha and V directly for similarity computation" |
| M9 | Appendix C Symbol Reference | Eta definition append "(derived summary of Alpha + Rho + V; see §3.6)" |
| M10 | §2.4 Eta row | Acknowledge dependency: "informationally a view onto (Alpha, Rho, V)" |

### Conceptual rework (the §2.4 hollowing-out)

The dialectic-architect's headline finding can't be patched mechanically; it needs a deliberate rework. Three options for v0.12:

- **Option A** (proposed by dialectic-architect): reframe §2.4 from *minimality* to *expressive sufficiency*. Stop claiming "removing any single component creates an identity-distinction the framework can no longer represent" — replace with "each component captures a theoretical commitment in our stack; together they span the phenomena §3 sets out to characterize. We do not claim the decomposition is minimal; establishing minimality requires the discrimination experiments in §7.2." Downgrades §2.4 from license to roadmap. Consistent with the rest of the v0.11 honesty pass.
- **Option B**: keep §2.4 as is but add a conditional clause acknowledging that the minimality argument is *contingent on the multi-agent discrimination experiments* in §7.2 — frame the current paper as "minimal modulo the discrimination test."
- **Option C**: actually run the multi-agent discrimination experiment (B5 in HANDOFF). The §2.4 argument either lands or gets revised based on data. ~2-3 months.

### Autopoiesis-to-attractor translation (§2.1)
Add a paragraph acknowledging this is a *modeling commitment*, not a definitional equivalence — autopoiesis is network-topological, attractor dynamics is state-space, the bridge is operational. The §3.6 Eta demotion then becomes coherent: "we do not have the autopoietic anchor as a separate signal; we have its state-space shadow distributed across Alpha, Rho, and the viability envelope." Light edit; sharpens the §2.1 → §3.6 chain.

---

## A meta-finding worth keeping

The recurring failure mode across these three reviews is *layered honesty without cross-layer consistency check* — each pass softens local overclaims but doesn't ask whether earlier justification structures still load-bear after the softening.

For papers undergoing successive fix passes (the proprioception paper will hit this too): **after each polish pass, ask whether previous justification arguments still load-bear, not just whether prose still sounds right.** Adding to memory as a review-skill anchor for future paper work.
