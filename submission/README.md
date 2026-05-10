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

## Manuscript size — now within journal limits

`TRAJECTORY_IDENTITY_PAPER.md` (v0.13, the canonical paper) was trimmed for journal submission and now sits at **~10,754 body words** (excluding the 213-word abstract, ~585 words of references, and the repository-only changelog). This fits comfortably within *Adaptive Behavior*'s 6,000–12,000-word band for original research articles. The trim removed only redundant or implementation-specific content (Appendix A's Python listing, the §1.1 redundant comparison table, §6.1.1-6.1.3 deployment-specific math); no claims were weakened or strengthened. See the v0.13 entry in the paper's Changelog for full diff.

The workshop variant (`TRAJECTORY_IDENTITY_WORKSHOP.md`, ~4,000 words) is below the journal's 6,000-word floor and is **not** the right submission unit; it's the conference-workshop unit.

**Use the canonical paper (v0.13) as the journal submission manuscript.** Strip the Changelog section before uploading (it's a repo artifact); the rest is journal-ready prose.

## Pre-submission checklist (operator)

- [ ] Strip the Changelog section from the canonical `TRAJECTORY_IDENTITY_PAPER.md` to produce the submission manuscript (everything else is journal-ready as-is).
- [ ] Convert to SAGE format. Easiest path: pandoc to LaTeX with the SAGE Overleaf template, OR pandoc to Word for direct submission.
- [ ] Verify abstract is ≤ 250 words (currently 213; ✓).
- [ ] Compile final PDF for submission (use `scripts/build_pdf.sh` or the SAGE LaTeX template's compile chain).
- [ ] Fill out the SAGE submission portal:
  - [ ] Manuscript file
  - [ ] Cover letter (paste from `cover_letter.md`)
  - [ ] AI-use disclosure (paste from `ai_use_disclosure.md` into the portal's AI-disclosure field, or upload as supplementary)
  - [ ] 3-5 suggested reviewers (cover letter lists 5: Froese, Di Paolo, Barandiaran, Ikegami, Beer; pick the 3 most-directly-relevant)
  - [ ] Author affiliation: "Independent Researcher, CIRWEL Systems"
  - [ ] ORCID: 0009-0006-7544-2374
  - [ ] Acknowledgments section: thank the human and AI reviewers per the Codex and council review files
- [ ] Submit.

## What happens after submission

SAGE Adaptive Behavior typically returns a first decision in 2-3 months. Possible outcomes:
- **Accept** (rare on first submission)
- **Minor revisions** (most common when craft is solid)
- **Major revisions** (likely given v0.12.1's honest single-agent scope; the journal will probably ask for at least one of: multi-agent discrimination, transplant test, or sharper framing of what's claimed). The HANDOFF B5/B6 experiments map directly to a major-revision response.
- **Reject without review** (if the journal decides it's not a fit; unlikely given the topic match)
- **Reject after review**

A "Major revisions" verdict is consistent with where v0.12.1 honestly stands. Plan the timeline accordingly: first decision in ~2-3 months, a revision cycle of 1-3 months, possibly a second revision round, then accept. Realistic timeline from submission to publication: 6-12 months.
