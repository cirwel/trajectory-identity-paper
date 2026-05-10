#!/usr/bin/env bash
# Build a PDF from the markdown source.
#
# Default: builds TRAJECTORY_IDENTITY_PAPER.pdf (long form).
# Pass "workshop" as first arg to build the workshop variant instead.
#
# Requires: pandoc, xelatex (TeX Live or MacTeX).
# Run from the repo root: ./scripts/build_pdf.sh [workshop]

set -euo pipefail
cd "$(dirname "$0")/.."

VARIANT="${1:-long}"
case "${VARIANT}" in
  long)
    INPUT=TRAJECTORY_IDENTITY_PAPER.md
    OUTPUT=TRAJECTORY_IDENTITY_PAPER.pdf
    TITLE="Trajectory Identity: A Mathematical Framework for Enactive AI Self-Hood"
    ;;
  workshop)
    INPUT=TRAJECTORY_IDENTITY_WORKSHOP.md
    OUTPUT=TRAJECTORY_IDENTITY_WORKSHOP.pdf
    TITLE="Trajectory Identity: A Dynamical Framework for AI Agent Self-Hood (workshop variant)"
    ;;
  *)
    echo "Usage: $0 [long|workshop]" >&2
    exit 2
    ;;
esac

VERSION=$(awk -F'"' '/^version:/ {print $2; exit}' CITATION.cff)
DOI=$(awk -F'"' '/^doi:/ {print $2; exit}' CITATION.cff)

echo "Building ${OUTPUT} from ${INPUT} (version ${VERSION}, DOI ${DOI})..."

pandoc "${INPUT}" \
  --pdf-engine=xelatex \
  -V geometry:margin=0.9in \
  -V mainfont="Helvetica" \
  -V monofont="Menlo" \
  -V fontsize=10pt \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  -V toc \
  -V toc-depth=2 \
  --metadata title="${TITLE}" \
  --metadata author="Kenny Wang" \
  --metadata date="May 2026 — Working Draft ${VERSION} — DOI ${DOI}" \
  -o "${OUTPUT}"

echo "Built ${OUTPUT} ($(du -h "${OUTPUT}" | awk '{print $1}'))"
