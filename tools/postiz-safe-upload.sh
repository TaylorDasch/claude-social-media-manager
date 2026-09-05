#!/usr/bin/env bash
# postiz-safe-upload.sh — the ONLY sanctioned path from a local file into the Postiz media library.
#
#   postiz-safe-upload.sh <file> [--dry-run]
#
# Refuses to upload anything that fails preflight; auto-normalizes anything that only warns.
# Every upload is appended to a ledger with a sha256, so a later post can be traced to a real asset.
# Claude and Codex should call THIS, never `postiz upload` directly.

set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFLIGHT="$HERE/social-preflight.sh"
LEDGER="$HERE/upload-ledger.tsv"
R=$'\e[31m'; G=$'\e[32m'; Y=$'\e[33m'; B=$'\e[1m'; N=$'\e[0m'

IN="${1:-}"; DRY=0; [ "${2:-}" = "--dry-run" ] && DRY=1
[ -z "$IN" ] && { echo "usage: postiz-safe-upload.sh <file> [--dry-run]"; exit 2; }
[ -f "$IN" ] || { echo "${R}no such file:${N} $IN"; exit 2; }

# --- gate 1: preflight -------------------------------------------------
echo "${B}[1/3] preflight${N}"
OUTPUT=$("$PREFLIGHT" check "$IN" 2>&1); RC=$?
echo "$OUTPUT"
if [ $RC -ne 0 ]; then
  echo
  echo "${R}BLOCKED — not uploading.${N} This file would publish as a dead post."
  echo "Re-export it from CapCut, then run this again."
  exit 1
fi

# --- gate 2: normalize if it only warned -------------------------------
UP="$IN"
if echo "$OUTPUT" | grep -q "warn"; then
  echo
  echo "${B}[2/3] normalizing (warnings found)${N}"
  "$PREFLIGHT" fix "$IN" || { echo "${R}BLOCKED — normalize failed.${N}"; exit 1; }
  UP="${IN%.*}-READY.mp4"
else
  echo
  echo "${B}[2/3] clean — no normalize needed${N}"
fi

# --- gate 3: upload ----------------------------------------------------
# NOTE: never `source` shared-keys.env — it clobbers PATH and curl/head vanish.
KEY=$(grep -m1 '^[[:space:]]*\(export[[:space:]]\+\)\?POSTIZ_API_KEY=' ~/shared-keys.env 2>/dev/null \
      | sed 's/.*POSTIZ_API_KEY=//' | tr -d '"'"'"' \r')
[ -z "$KEY" ] && { echo "${R}POSTIZ_API_KEY not found in ~/shared-keys.env${N}"; exit 2; }

SHA=$(shasum -a 256 "$UP" | awk '{print $1}')
DUR=$(ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$UP")

echo
echo "${B}[3/3] upload${N}  $(basename "$UP")  ${DUR}s  sha:${SHA:0:12}"
if [ $DRY -eq 1 ]; then
  echo "${Y}--dry-run: stopping before upload. File is verified and ready.${N}"
  exit 0
fi

RES=$(POSTIZ_API_KEY="$KEY" postiz upload "$UP" 2>&1); URC=$?
if [ $URC -ne 0 ]; then echo "${R}upload failed:${N}"; echo "$RES" | head -5; exit 1; fi
echo "$RES" | tail -5

[ -f "$LEDGER" ] || printf "timestamp\tsha256\tduration\tsource\tuploaded\tresult\n" > "$LEDGER"
printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$(date -u +%FT%TZ)" "$SHA" "$DUR" "$IN" "$UP" \
  "$(echo "$RES" | tr '\n' ' ' | tail -c 200)" >> "$LEDGER"

echo "${G}uploaded + logged to $(basename "$LEDGER")${N}"
