#!/usr/bin/env bash
# social-preflight.sh — validate and normalize a CapCut/Resolve export before it goes to Postiz.
#
#   social-preflight.sh check <file|dir>      # non-destructive report
#   social-preflight.sh fix   <file> [outfile] # normalize -> platform-safe MP4, then re-verify
#
# Exit 0 = safe to publish. Exit 1 = do NOT publish.
# Built 2026-09-03 after a zero-length CapCut export published to IG + FB as a dead video.

set -uo pipefail
FFPROBE=$(command -v ffprobe) || { echo "ffprobe not found (brew install ffmpeg)"; exit 2; }
FFMPEG=$(command -v ffmpeg)   || { echo "ffmpeg not found (brew install ffmpeg)";  exit 2; }

R=$'\e[31m'; G=$'\e[32m'; Y=$'\e[33m'; B=$'\e[1m'; N=$'\e[0m'
probe(){ "$FFPROBE" -v error -select_streams "$1" -show_entries "$2" -of default=nw=1:nk=1 "$3" 2>/dev/null | head -1; }

check_one(){
  local f="$1" fail=0 warn=0
  echo "${B}$(basename "$f")${N}"

  local bytes; bytes=$(stat -f%z "$f" 2>/dev/null || echo 0)
  if [ "$bytes" -lt 1024 ]; then echo "  ${R}FAIL${N} file is ${bytes} bytes"; return 1; fi

  if ! "$FFPROBE" -v error -show_format "$f" >/dev/null 2>&1; then
    echo "  ${R}FAIL${N} unreadable / no moov atom — export was interrupted"; return 1; fi

  local dur vcodec w h fps acodec pixfmt trc
  dur=$(probe v:0 format=duration "$f"); [ -z "$dur" ] && dur=$("$FFPROBE" -v error -show_entries format=duration -of default=nw=1:nk=1 "$f" 2>/dev/null)
  vcodec=$(probe v:0 stream=codec_name "$f")
  w=$(probe v:0 stream=width "$f"); h=$(probe v:0 stream=height "$f")
  fps=$(probe v:0 stream=r_frame_rate "$f")
  acodec=$(probe a:0 stream=codec_name "$f")
  pixfmt=$(probe v:0 stream=pix_fmt "$f")
  trc=$(probe v:0 stream=color_transfer "$f")

  # --- hard gates -------------------------------------------------------
  if [ -z "$vcodec" ]; then echo "  ${R}FAIL${N} no video stream"; fail=1; fi
  local dsec; dsec=$(awk -v d="${dur:-0}" 'BEGIN{printf "%.2f", d+0}')
  if awk -v d="$dsec" 'BEGIN{exit !(d < 0.5)}'; then
    echo "  ${R}FAIL${N} duration ${dsec}s — this is the zero-length failure. Do not upload."; fail=1
  fi

  [ "$fail" -eq 0 ] && echo "  ${G}ok${N}   ${dsec}s  ${w}x${h}  ${vcodec}/${acodec:-NO-AUDIO}  ${pixfmt}  ${fps} fps"

  # --- warnings ---------------------------------------------------------
  local nfps; nfps=$(awk -F/ -v r="${fps:-0/1}" 'BEGIN{split(r,a,"/"); if(a[2]>0) printf "%.2f", a[1]/a[2]; else print 0}')
  awk -v f="$nfps" 'BEGIN{exit !(f>0 && f<29.9)}' && { echo "  ${Y}warn${N} ${nfps} fps — Meta wants Reels at 30+"; warn=1; }
  [ -z "$acodec" ] && { echo "  ${Y}warn${N} no audio track — TikTok/Reels can reject silent uploads"; warn=1; }
  [ "$pixfmt" != "yuv420p" ] && [ -n "$pixfmt" ] && { echo "  ${Y}warn${N} pix_fmt=$pixfmt (want yuv420p)"; warn=1; }
  case "$trc" in arib-std-b67|smpte2084) echo "  ${Y}warn${N} HDR ($trc) — will look washed out; re-export SDR"; warn=1;; esac
  [ -n "$w" ] && [ $((w % 2)) -ne 0 ] && { echo "  ${Y}warn${N} odd width $w"; warn=1; }
  [ -n "$h" ] && [ $((h % 2)) -ne 0 ] && { echo "  ${Y}warn${N} odd height $h"; warn=1; }
  if [ -n "$w" ] && [ -n "$h" ] && [ "$h" -gt 0 ]; then
    awk -v w="$w" -v h="$h" 'BEGIN{exit !(w/h > 0.60)}' && { echo "  ${Y}warn${N} ${w}x${h} is not 9:16 vertical"; warn=1; }
  fi

  [ "$fail" -ne 0 ] && return 1
  [ "$warn" -ne 0 ] && { echo "  ${Y}-> run: social-preflight.sh fix '$f'${N}"; return 0; }
  echo "  ${G}-> safe to publish${N}"; return 0
}

fix_one(){
  local in="$1" out="${2:-}"
  [ -z "$out" ] && out="${in%.*}-READY.mp4"

  if ! "$FFPROBE" -v error -show_format "$in" >/dev/null 2>&1; then
    echo "${R}Cannot fix:${N} $in is unreadable. Re-export from CapCut — there is no file here to repair."; return 1; fi
  local dur; dur=$("$FFPROBE" -v error -show_entries format=duration -of default=nw=1:nk=1 "$in" 2>/dev/null)
  if awk -v d="${dur:-0}" 'BEGIN{exit !(d+0 < 0.5)}'; then
    echo "${R}Cannot fix:${N} duration is ${dur:-0}s. The export contains no frames. Re-export from CapCut."; return 1; fi

  local fps nfps target; fps=$(probe v:0 stream=r_frame_rate "$in")
  nfps=$(awk -F/ -v r="${fps:-30/1}" 'BEGIN{split(r,a,"/"); if(a[2]>0) printf "%.2f", a[1]/a[2]; else print 30}')
  target=30; awk -v f="$nfps" 'BEGIN{exit !(f>=59)}' && target=60

  echo "${B}normalizing${N} $(basename "$in") -> $(basename "$out")  (${nfps} -> ${target} fps CFR)"
  local hasaudio; hasaudio=$(probe a:0 stream=codec_name "$in")
  local -a VF=(-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos,format=yuv420p"
               -fps_mode cfr -r "$target"
               -c:v libx264 -profile:v high -level 4.2 -preset slow -crf 19 -pix_fmt yuv420p
               -colorspace bt709 -color_primaries bt709 -color_trc bt709)

  if [ -n "$hasaudio" ]; then
    "$FFMPEG" -y -v error -i "$in" "${VF[@]}" \
      -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$out"
  else
    echo "  adding silent audio track"
    "$FFMPEG" -y -v error -i "$in" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
      -map 0:v:0 -map 1:a:0 "${VF[@]}" \
      -c:a aac -b:a 128k -shortest -movflags +faststart "$out"
  fi

  local rc=$?
  [ $rc -ne 0 ] && { echo "${R}encode failed${N} (rc=$rc)"; return 1; }
  echo "${B}re-verifying output:${N}"
  check_one "$out" || { echo "${R}output failed verification — do not publish${N}"; return 1; }
}

cmd="${1:-}"; shift 2>/dev/null
case "$cmd" in
  check)
    t="${1:-}"; [ -z "$t" ] && { echo "usage: social-preflight.sh check <file|dir>"; exit 2; }
    rc=0
    if [ -d "$t" ]; then
      while IFS= read -r f; do check_one "$f" || rc=1; echo; done < <(find "$t" -maxdepth 1 -type f \( -iname '*.mp4' -o -iname '*.mov' \) | sort)
    else check_one "$t" || rc=1; fi
    exit $rc;;
  fix)
    [ -z "${1:-}" ] && { echo "usage: social-preflight.sh fix <file> [outfile]"; exit 2; }
    fix_one "$1" "${2:-}";;
  *) sed -n '2,10p' "$0"; exit 2;;
esac
