#!/usr/bin/env bash
# resume-zenodo-v0.15.sh — finish the v0.15 Zenodo deposit that stalled on a Zenodo outage.
#
# CONTEXT (2026-07-28)
#   The v0.15 correction is already public on GitHub. The Zenodo version was started
#   but not finished: Zenodo began returning HTTP 504 on every write, then went fully
#   unreachable (site + read API timing out). A new-version DRAFT already exists and is
#   unsubmitted with no files attached.
#
#   Do NOT re-run publish-to-zenodo.sh — that would create a SECOND draft under the same
#   concept. This script resumes the existing one.
#
#   Draft record : 21659982      (reserved DOI 10.5281/zenodo.21659982)
#   Concept      : 20098168      (auto-resolves to latest; currently paper-v0.14 / 20531932)
#
# USAGE
#   set -a; . ~/.config/cirwel/secrets.env; set +a
#   ./scripts/resume-zenodo-v0.15.sh              # publish
#   DRY_RUN=1 ./scripts/resume-zenodo-v0.15.sh    # show what it would do
#
# Check Zenodo is back first:  curl -sS -o /dev/null -w '%{http_code}\n' https://zenodo.org
# Anything other than 200 — wait. Zenodo outages usually clear within hours.

set -euo pipefail

DRAFT_ID=21659982
BUCKET="https://zenodo.org/api/files/fb365201-a089-4883-835e-850a49b76296"
PDF="TRAJECTORY_IDENTITY_PAPER.pdf"
VERSION="paper-v0.15"
API="https://zenodo.org"
: "${DRY_RUN:=0}"

[[ -n "${ZENODO_TOKEN:-}" ]] || { echo "error: ZENODO_TOKEN not set" >&2; exit 64; }
[[ -f "$PDF" ]] || { echo "error: run from repo root ($PDF not found)" >&2; exit 66; }
[[ -f .zenodo.json ]] || { echo "error: .zenodo.json missing" >&2; exit 66; }

AUTH=(-H "Authorization: Bearer ${ZENODO_TOKEN}")

echo "==> Checking draft ${DRAFT_ID}"
curl -sS "${AUTH[@]}" "${API}/api/deposit/depositions/${DRAFT_ID}" -o /tmp/zdraft.json --max-time 30
python3 - <<'PY'
import json,sys
d=json.load(open('/tmp/zdraft.json'))
state=d.get('state'); files=[f.get('filename') for f in d.get('files',[])]
print(f"    state={state} submitted={d.get('submitted')} files={files}")
if d.get('submitted'):
    print("    ALREADY PUBLISHED — nothing to do. Check https://doi.org/10.5281/zenodo.21659982")
    sys.exit(3)
PY

if [[ "$DRY_RUN" == "1" ]]; then echo "[dry-run] would upload, set metadata, publish"; exit 0; fi

echo "==> Uploading ${PDF}"
code=$(curl -sS "${AUTH[@]}" --upload-file "$PDF" "${BUCKET}/${PDF}" -o /tmp/zup.json -w "%{http_code}" --max-time 120)
echo "    HTTP ${code}"
[[ "$code" =~ ^20[01]$ ]] || { echo "error: upload failed (Zenodo still degraded?)" >&2; exit 71; }

echo "==> Setting metadata"
meta=$(python3 -c "
import json,datetime
z=json.load(open('.zenodo.json'))
z['version']='${VERSION}'
z['publication_date']=datetime.date.today().isoformat()
print(json.dumps({'metadata':z}))
")
code=$(curl -sS -X PUT "${AUTH[@]}" -H "Content-Type: application/json" \
  "${API}/api/deposit/depositions/${DRAFT_ID}" -d "$meta" -o /tmp/zmeta.json -w "%{http_code}" --max-time 60)
echo "    HTTP ${code}"
[[ "$code" =~ ^20[01]$ ]] || { echo "error: metadata PUT failed" >&2; head -c 400 /tmp/zmeta.json >&2; exit 71; }

echo "==> Publishing"
code=$(curl -sS -X POST "${AUTH[@]}" -H "Content-Type: application/json" \
  "${API}/api/deposit/depositions/${DRAFT_ID}/actions/publish" -o /tmp/zpub.json -w "%{http_code}" --max-time 60)
echo "    HTTP ${code}"
[[ "$code" =~ ^20[02]$ ]] || { echo "error: publish failed" >&2; head -c 400 /tmp/zpub.json >&2; exit 71; }

echo
echo "Published:"
echo "  Version DOI: 10.5281/zenodo.${DRAFT_ID}"
echo "  Concept DOI: 10.5281/zenodo.20098168 (auto-resolves here)"
echo "  Record:      https://zenodo.org/records/${DRAFT_ID}"
echo
echo "Then: git push origin paper-v0.15"
