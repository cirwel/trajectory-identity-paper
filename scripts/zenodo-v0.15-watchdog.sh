#!/usr/bin/env bash
# zenodo-v0.15-watchdog.sh — one-shot watchdog: finish the v0.15 Zenodo deposit
# once Zenodo recovers from its 2026-07-28 outage, then REMOVE ITSELF.
#
# Driven by launchd (com.cirwel.zenodo-v015-watchdog), every 20 minutes.
# Self-removing by design: a parked item needs a wake condition, and a wake
# condition that outlives its purpose is just noise. On success — or once the
# deadline passes — this unloads and deletes its own LaunchAgent.
#
# Manual equivalent, if you'd rather just do it yourself:
#   cd ~/projects/trajectory-identity-paper
#   set -a; . ~/.config/cirwel/secrets.env; set +a
#   ./scripts/resume-zenodo-v0.15.sh
# Doing that by hand is fine — the watchdog will notice it's published and retire.

set -uo pipefail

REPO="/Users/cirwel/projects/trajectory-identity-paper"
LABEL="com.cirwel.zenodo-v015-watchdog"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
LOG="$REPO/.zenodo-watchdog.log"
DEADLINE_FILE="$REPO/.zenodo-watchdog.deadline"
DRAFT_ID=21659982

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" >> "$LOG"; }

retire() {
  log "RETIRING watchdog: $1"
  launchctl unload "$PLIST" 2>/dev/null || true
  rm -f "$PLIST" "$DEADLINE_FILE"
  log "watchdog removed. plist deleted: $PLIST"
  exit 0
}

cd "$REPO" || { log "repo missing, retiring"; retire "repo gone"; }

# 48h deadline — Zenodo outages clear in hours; if it's been two days something
# else is wrong and a human should look rather than a timer keep firing.
if [[ ! -f "$DEADLINE_FILE" ]]; then
  date -u -v+48H +%s > "$DEADLINE_FILE" 2>/dev/null || date -u -d '+48 hours' +%s > "$DEADLINE_FILE"
  log "watchdog armed; deadline $(cat "$DEADLINE_FILE")"
fi
now=$(date -u +%s)
if (( now > $(cat "$DEADLINE_FILE") )); then
  log "DEADLINE PASSED without publishing. Draft ${DRAFT_ID} is still unsubmitted."
  log "Run ./scripts/resume-zenodo-v0.15.sh by hand, or check https://zenodo.org"
  retire "48h deadline expired — needs a human"
fi

# Health gate: only touch write endpoints when the read API is genuinely healthy.
# curl -w always emits a code (000 on connect failure/timeout), so no `|| echo`
# fallback — that just concatenates a second 000 and makes the log read "000000".
code=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 25 \
  "https://zenodo.org/api/records/20098168" 2>/dev/null)
code="${code:-000}"
if [[ "$code" != "200" ]]; then
  log "zenodo not healthy (http=$code) — waiting"
  exit 0
fi

set -a; . "$HOME/.config/cirwel/secrets.env" 2>/dev/null; set +a
[[ -n "${ZENODO_TOKEN:-}" ]] || { log "ZENODO_TOKEN missing"; retire "no token"; }

# Already published (possibly by hand)? Then retire quietly.
curl -sS -H "Authorization: Bearer $ZENODO_TOKEN" --max-time 30 \
  "https://zenodo.org/api/deposit/depositions/${DRAFT_ID}" -o /tmp/zwatch.json 2>/dev/null
if python3 -c "
import json,sys
try: d=json.load(open('/tmp/zwatch.json'))
except Exception: sys.exit(1)
sys.exit(0 if d.get('submitted') else 1)
" 2>/dev/null; then
  log "draft ${DRAFT_ID} already submitted — nothing to do"
  retire "already published"
fi

log "zenodo healthy (http=200) — attempting resume"
if ./scripts/resume-zenodo-v0.15.sh >> "$LOG" 2>&1; then
  log "SUCCESS: published 10.5281/zenodo.${DRAFT_ID}"
  git push origin paper-v0.15 >> "$LOG" 2>&1 || log "note: tag push failed/already pushed"
  retire "published successfully"
else
  log "resume attempt failed (exit $?) — will retry next interval"
  exit 0
fi
