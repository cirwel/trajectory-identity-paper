#!/usr/bin/env bash
# Build TRAJECTORY_IDENTITY_PAPER.pdf from the markdown source.
#
# Requires: pandoc, xelatex (TeX Live or MacTeX).
# Run from the repo root: ./scripts/build_pdf.sh

set -euo pipefail
cd "$(dirname "$0")/.."

INPUT=TRAJECTORY_IDENTITY_PAPER.md
OUTPUT=TRAJECTORY_IDENTITY_PAPER.pdf

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
  --metadata title="Trajectory Identity: A Mathematical Framework for Enactive AI Self-Hood" \
  --metadata author="Kenny Wang" \
  --metadata date="May 2026 — Working Draft ${VERSION} — DOI ${DOI}" \
  -o "${OUTPUT}"

echo "Built ${OUTPUT} ($(du -h "${OUTPUT}" | awk '{print $1}'))"
