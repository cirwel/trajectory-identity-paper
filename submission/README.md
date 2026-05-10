# Submission package — Adaptive Behavior

Materials for submitting *Trajectory Identity: A Mathematical Framework for Enactive AI Self-Hood* to *Adaptive Behavior* (SAGE).

## Contents

- `cover_letter.md` — cover letter to the editor, including reviewer suggestions and AI-use summary.
- `ai_use_disclosure.md` — full AI-use disclosure per SAGE policy (referenced in the cover letter).
- `README.md` — this file.

## Submission target

**Adaptive Behavior** (SAGE; official journal of the International Society for Adaptive Behavior).

- Submission portal: <https://journals.sagepub.com/home/adb>
- Author guidelines: <https://journals.sagepub.com/author-instructions/ADB>

## SAGE submission requirements (key ones)

- **Word count**: 6,000–12,000 for original research articles.
- **Abstract**: unstructured, 250 words max.
- **Format**: Word preferred; LaTeX accepted (SAGE LaTeX template on [Overleaf](https://www.overleaf.com/latex/templates/a-demonstration-of-the-latex2e-class-file-for-sage-publications/jcdyknyjrkzb)).
- **Mandatory AI-use disclosure** at submission.
- **Three to five suggested reviewers**.

## Decision still required (operator action)

The current manuscript variants in this repo do **not** match the journal's word-count band:

- `TRAJECTORY_IDENTITY_PAPER.md` (long form) — 13,704 words. Above the 12,000 cap. Needs ~1,700 words trimmed.
- `TRAJECTORY_IDENTITY_WORKSHOP.md` (workshop variant) — 4,029 words. Below the 6,000 floor. Needs ~2,000 words expanded.

**Three reasonable paths:**

1. **Trim the long form** to ~12,000 words. Preserves the full theoretical apparatus and empirical reporting. Cuts: condense §5 operational semantics, abridge §6.1 implementation pointers, drop Appendix A code listing (point at the public repo instead), trim some of the §1.4 Related Work.
2. **Expand the workshop variant** to ~7,000-8,000 words. Lift §3.1 identity-as-coupling, §2.4 expressive-sufficiency justification, §4.3 operational-continuity reframe, and the §5.5 adversarial-considerations material from the long form into the workshop frame.
3. **Hybrid: workshop variant + select long-form sections**. Use the workshop variant as the spine, lift §6.4 (empirical), §3.1 (identity-as-coupling), §5.5 (adversarial) into it. Roughly equivalent to path 2 but more curated.

Path 1 is fastest; path 2/3 produces a tighter manuscript at the cost of more editing.

## Pre-submission checklist (operator)

- [ ] Choose manuscript variant (paths 1, 2, or 3 above) and produce a `journal_manuscript.md` (or `.tex`).
- [ ] Convert to SAGE format (Word or SAGE LaTeX template).
- [ ] Verify abstract is exactly 250 words or under.
- [ ] Run a final word-count check against journal limits.
- [ ] Compile final PDF for submission.
- [ ] Fill out the SAGE submission portal:
  - [ ] Manuscript file
  - [ ] Cover letter (`cover_letter.md` content)
  - [ ] AI-use disclosure (`ai_use_disclosure.md` content; or paste into the portal's AI-disclosure field)
  - [ ] 3-5 suggested reviewers (cover letter has 5; pick the 3 most-directly-relevant)
  - [ ] Author affiliation: "Independent Researcher, CIRWEL Systems"
  - [ ] ORCID: 0009-0006-7544-2374
  - [ ] Acknowledgments section if needed
- [ ] Submit.

## What happens after submission

SAGE Adaptive Behavior typically returns a first decision in 2-3 months. Possible outcomes:
- **Accept** (rare on first submission)
- **Minor revisions** (most common when craft is solid)
- **Major revisions** (likely given v0.12.1's honest single-agent scope; the journal will probably ask for at least one of: multi-agent discrimination, transplant test, or sharper framing of what's claimed). The HANDOFF B5/B6 experiments map directly to a major-revision response.
- **Reject without review** (if the journal decides it's not a fit; unlikely given the topic match)
- **Reject after review**

A "Major revisions" verdict is consistent with where v0.12.1 honestly stands. Plan the timeline accordingly: first decision in ~2-3 months, a revision cycle of 1-3 months, possibly a second revision round, then accept. Realistic timeline from submission to publication: 6-12 months.
