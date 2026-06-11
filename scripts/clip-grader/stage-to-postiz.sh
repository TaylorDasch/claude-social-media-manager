#!/usr/bin/env bash
# stage-to-postiz.sh — for /clip-grader skill
#
# Reads a keepers manifest (JSON), uploads each clip to Postiz, and creates
# DRAFT posts on TikTok + Instagram + Facebook with the suggested caption.
#
# Drafts stay in DRAFT state until Taylor manually promotes them to scheduled.
#
# Manifest format (JSON array):
# [
#   {
#     "path": "/abs/path/to/clip.mp4",
#     "caption_tiktok": "...",
#     "caption_instagram": "...",
#     "caption_facebook": "...",
#     "publish_date": "2026-05-30T23:00:00Z"
#   }
# ]
#
# Usage:
#   ./stage-to-postiz.sh <manifest.json>
#
# Env (already in shared-keys.env):
#   POSTIZ_API_KEY  — required

set -euo pipefail

MANIFEST="${1:-}"
if [[ -z "$MANIFEST" || ! -f "$MANIFEST" ]]; then
  echo "Usage: $0 <manifest.json>" >&2
  exit 1
fi

if [[ -z "${POSTIZ_API_KEY:-}" ]]; then
  if [[ -f "$HOME/shared-keys.env" ]]; then
    # shellcheck disable=SC1090
    set -a; source "$HOME/shared-keys.env"; set +a
  fi
fi

if ! command -v postiz >/dev/null 2>&1; then
  echo "ERROR: postiz CLI not on PATH" >&2
  exit 1
fi

# Integration IDs (from `postiz integrations:list` 2026-05-23)
TIKTOK_ID="cmoevc6uq0499mt0yh5czkk2g"
INSTAGRAM_ID="cmoevb9lg04hzq70yhuho21x2"
FACEBOOK_ID="cmoevbuj704i5q70yvnvaw9q0"

LOG_DIR="$HOME/claude-social-media-manager/shorts/reports"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/stage-log-$(date +%Y-%m-%d-%H%M).log"

n=$(jq 'length' "$MANIFEST")
echo "Staging $n keeper(s) to Postiz as DRAFTS..." | tee "$LOG"

for i in $(seq 0 $((n - 1))); do
  path=$(jq -r ".[$i].path" "$MANIFEST")
  cap_tt=$(jq -r ".[$i].caption_tiktok" "$MANIFEST")
  cap_ig=$(jq -r ".[$i].caption_instagram" "$MANIFEST")
  cap_fb=$(jq -r ".[$i].caption_facebook" "$MANIFEST")
  pub_date=$(jq -r ".[$i].publish_date" "$MANIFEST")

  fname=$(basename "$path")
  echo -e "\n[$((i + 1))/$n] $fname" | tee -a "$LOG"

  if [[ ! -f "$path" ]]; then
    echo "  SKIP: file missing: $path" | tee -a "$LOG"
    continue
  fi

  echo "  Uploading to Postiz..." | tee -a "$LOG"
  upload_raw=$(postiz upload "$path" 2>&1)
  upload_status=$?
  if [[ $upload_status -ne 0 ]]; then
    echo "  UPLOAD FAILED: $upload_raw" | tee -a "$LOG"
    continue
  fi
  # postiz prepends a status line before the JSON object; extract the JSON block robustly
  video_url=$(printf '%s' "$upload_raw" | python3 -c "
import sys, json, re
raw = sys.stdin.read()
m = re.search(r'\{.*\}', raw, re.DOTALL)
if not m:
    sys.exit(1)
try:
    obj = json.loads(m.group(0))
    print(obj.get('path',''))
except json.JSONDecodeError:
    sys.exit(1)
" 2>/dev/null)
  if [[ -z "$video_url" ]]; then
    echo "  UPLOAD FAILED (no path returned): $upload_raw" | tee -a "$LOG"
    continue
  fi
  echo "  Uploaded: $video_url" | tee -a "$LOG"

  # TikTok draft (schema confirmed via Postiz API errors 2026-05-23)
  echo "  -> TikTok draft..." | tee -a "$LOG"
  tt_out=$(postiz posts:create \
    -c "$cap_tt" \
    -s "$pub_date" \
    -t draft \
    --settings '{"privacy_level":"PUBLIC_TO_EVERYONE","content_posting_method":"DIRECT_POST","duet":true,"stitch":true,"comment":true,"brand_organic_toggle":false,"brand_content_toggle":false,"autoAddMusic":"no","isAigc":false,"title":""}' \
    -m "$video_url" \
    -i "$TIKTOK_ID" 2>&1) || true
  echo "$tt_out" | tee -a "$LOG"

  # Instagram draft (Reels go via post_type=post with video media; "reel" is not a valid post_type)
  echo "  -> Instagram draft..." | tee -a "$LOG"
  ig_out=$(postiz posts:create \
    -c "$cap_ig" \
    -s "$pub_date" \
    -t draft \
    --settings '{"post_type":"post"}' \
    -m "$video_url" \
    -i "$INSTAGRAM_ID" 2>&1) || true
  echo "$ig_out" | tee -a "$LOG"

  # Facebook Reel draft (working schema)
  echo "  -> Facebook Reel draft..." | tee -a "$LOG"
  fb_out=$(postiz posts:create \
    -c "$cap_fb" \
    -s "$pub_date" \
    -t draft \
    --settings '{"type":"reel"}' \
    -m "$video_url" \
    -i "$FACEBOOK_ID" 2>&1) || true
  echo "$fb_out" | tee -a "$LOG"

  echo "  done." | tee -a "$LOG"
done

echo -e "\nLog: $LOG"
echo "Drafts created. Review in Postiz UI, then promote each with:"
echo "  postiz posts:status <post-id> --status schedule"
