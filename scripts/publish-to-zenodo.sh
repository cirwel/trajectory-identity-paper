#!/usr/bin/env bash
# publish-to-zenodo.sh — publish a new paper version to Zenodo with PDF + source zip
# as top-level files (so the PDF is previewable directly on the Zenodo record page).
#
# This script replaces what the Zenodo-GitHub integration would have done. The
# integration only attaches the source tarball, which buries the PDF inside a zip.
# This script attaches the PDF as a separate top-level asset.
#
# IMPORTANT: For this to work without creating duplicate records, you must disable
# the Zenodo-GitHub integration for this repo at:
#   https://zenodo.org/account/settings/github/repository/cirwel/trajectory-identity-paper
#
# Usage (from repo root):
#   ZENODO_TOKEN=xxx ./scripts/publish-to-zenodo.sh paper-v6.8.2 unitares-v6.pdf [source.zip]
#
# The source-zip argument is optional. Omit it to publish a PDF-only record
# (cleaner for readers; avoids shipping .github/FUNDING.yml and other repo
# bric-a-brac inside the archive).
#
# Optional env:
#   ZENODO_CONCEPT_RECID  Concept record ID (default: 19647159 — the v6 concept DOI)
#   ZENODO_API_BASE       API base (default: https://zenodo.org; sandbox.zenodo.org for testing)
#   DRY_RUN               If "1", print actions without calling write endpoints
#
# Run locally for one-off backfills (e.g. add the PDF to an already-published version
# by minting v6.8.2 with no other content changes).

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 <tag> <pdf-path> [source-zip-path]" >&2
  exit 64
fi

TAG="$1"
PDF_PATH="$2"
ZIP_PATH="${3:-}"
# Keep the full tag as the Zenodo version string for consistency with prior
# releases (e.g. "paper-v6.8.1"). Existing concept history uses this form.
VERSION="$TAG"
: "${ZENODO_CONCEPT_RECID:=19647159}"
: "${ZENODO_API_BASE:=https://zenodo.org}"
: "${DRY_RUN:=0}"

if [[ -z "${ZENODO_TOKEN:-}" ]]; then
  echo "error: ZENODO_TOKEN env var required" >&2
  exit 64
fi

required_files=("$PDF_PATH" .zenodo.json)
[[ -n "$ZIP_PATH" ]] && required_files+=("$ZIP_PATH")
for f in "${required_files[@]}"; do
  [[ -f "$f" ]] || { echo "error: missing file: $f" >&2; exit 66; }
done

command -v jq >/dev/null || { echo "error: jq required" >&2; exit 69; }
command -v curl >/dev/null || { echo "error: curl required" >&2; exit 69; }

API_AUTH=(-H "Authorization: Bearer ${ZENODO_TOKEN}")
API_JSON=(-H "Content-Type: application/json")

api() {
  # api METHOD PATH [data-flags...]
  local method="$1" path="$2"; shift 2
  curl -sS -X "$method" "${API_AUTH[@]}" "${API_JSON[@]}" \
    -w "\n%{http_code}\n" "${ZENODO_API_BASE}${path}" "$@"
}

run_or_dry() {
  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[dry-run] $*" >&2
    return 0
  fi
  "$@"
}

echo "==> Resolving latest record under concept ${ZENODO_CONCEPT_RECID}"
latest_resp="$(curl -sSL "${API_AUTH[@]}" \
  "${ZENODO_API_BASE}/api/records/${ZENODO_CONCEPT_RECID}/versions/latest")"
latest_recid="$(printf '%s' "$latest_resp" | jq -r '.id')"
latest_version="$(printf '%s' "$latest_resp" | jq -r '.metadata.version // "(none)"')"
[[ "$latest_recid" != "null" && -n "$latest_recid" ]] || {
  echo "error: could not resolve latest record id" >&2
  echo "$latest_resp" | head -c 500 >&2
  exit 70
}
echo "    latest record id=${latest_recid} version=${latest_version}"

if [[ "$latest_version" == "$VERSION" ]]; then
  echo "error: version ${VERSION} already published as record ${latest_recid}" >&2
  echo "       bump the tag and try again" >&2
  exit 65
fi

echo "==> Creating new version draft"
if [[ "$DRY_RUN" == "1" ]]; then
  echo "[dry-run] would POST /api/deposit/depositions/${latest_recid}/actions/newversion"
  exit 0
fi

newver_out="$(api POST "/api/deposit/depositions/${latest_recid}/actions/newversion")"
newver_body="$(printf '%s' "$newver_out" | sed '$d')"
newver_status="$(printf '%s' "$newver_out" | tail -n1)"
[[ "$newver_status" =~ ^20[01]$ ]] || {
  echo "error: newversion returned HTTP ${newver_status}" >&2
  echo "$newver_body" >&2
  exit 71
}

draft_url="$(printf '%s' "$newver_body" | jq -r '.links.latest_draft')"
draft_id="${draft_url##*/}"
echo "    draft id=${draft_id}"

echo "==> Fetching draft (need bucket URL)"
draft_out="$(api GET "/api/deposit/depositions/${draft_id}")"
draft_body="$(printf '%s' "$draft_out" | sed '$d')"
bucket_url="$(printf '%s' "$draft_body" | jq -r '.links.bucket')"
[[ -n "$bucket_url" && "$bucket_url" != "null" ]] || {
  echo "error: no bucket URL in draft" >&2
  echo "$draft_body" >&2
  exit 71
}

echo "==> Removing inherited files from draft"
inherited_ids="$(printf '%s' "$draft_body" | jq -r '.files[].id')"
for fid in $inherited_ids; do
  echo "    deleting file id=$fid"
  curl -sS -X DELETE "${API_AUTH[@]}" \
    "${ZENODO_API_BASE}/api/deposit/depositions/${draft_id}/files/${fid}" \
    -o /dev/null -w "    HTTP %{http_code}\n"
done

upload_to_bucket() {
  # Uses curl --upload-file (-T), which sends the raw bytes as a PUT with
  # no default Content-Type. --data-binary PUT was previously used and
  # sent Content-Type: application/x-www-form-urlencoded, which Zenodo's
  # bucket endpoint began rejecting with HTTP 415. --upload-file is the
  # correct primitive for binary PUT to object storage.
  local local_path="$1" remote_name="$2"
  local status
  echo "    uploading ${remote_name} ($(wc -c <"$local_path") bytes)"
  status="$(curl -sS "${API_AUTH[@]}" \
    --upload-file "${local_path}" \
    "${bucket_url}/${remote_name}" \
    -o /dev/null -w "%{http_code}")"
  echo "    HTTP ${status}"
  [[ "$status" =~ ^20[01]$ ]] || {
    echo "error: upload ${remote_name} returned HTTP ${status}" >&2
    exit 71
  }
}

echo "==> Uploading files"
upload_to_bucket "$PDF_PATH" "$(basename "$PDF_PATH")"
if [[ -n "$ZIP_PATH" ]]; then
  upload_to_bucket "$ZIP_PATH" "$(basename "$ZIP_PATH")"
fi

echo "==> Updating metadata"
metadata="$(jq --arg v "$VERSION" \
              --arg d "$(date -u +%Y-%m-%d)" \
              '{metadata: (. + {version: $v, publication_date: $d})}' \
              .zenodo.json)"

meta_out="$(api PUT "/api/deposit/depositions/${draft_id}" -d "$metadata")"
meta_status="$(printf '%s' "$meta_out" | tail -n1)"
[[ "$meta_status" =~ ^20[01]$ ]] || {
  echo "error: metadata PUT returned HTTP ${meta_status}" >&2
  printf '%s' "$meta_out" | sed '$d' >&2
  exit 71
}

echo "==> Publishing"
pub_out="$(api POST "/api/deposit/depositions/${draft_id}/actions/publish")"
pub_body="$(printf '%s' "$pub_out" | sed '$d')"
pub_status="$(printf '%s' "$pub_out" | tail -n1)"
[[ "$pub_status" =~ ^20[02]$ ]] || {
  echo "error: publish returned HTTP ${pub_status}" >&2
  echo "$pub_body" >&2
  exit 71
}

new_doi="$(printf '%s' "$pub_body" | jq -r '.doi // .metadata.doi')"
new_record_url="$(printf '%s' "$pub_body" | jq -r '.links.record_html // .links.html')"
echo
echo "Published:"
echo "  Version DOI: 10.5281/zenodo.${draft_id}"
echo "  DOI URL:     https://doi.org/${new_doi}"
echo "  Record:      ${new_record_url}"
echo "  Concept DOI: 10.5281/zenodo.${ZENODO_CONCEPT_RECID} (auto-resolves to this version)"
