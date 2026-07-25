#!/usr/bin/env bash
set -euo pipefail

audit_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
manifest="${audit_dir}/candidate-channels.tsv"
raw_dir="${audit_dir}/raw/channels"
mkdir -p "${raw_dir}"

fetch_channel() {
  local channel_id="$1"
  local output_file="${raw_dir}/${channel_id}.json"
  local temp_file="${output_file}.tmp"

  if [[ -s "${output_file}" ]] && jq -e '.id and .title' "${output_file}" >/dev/null 2>&1; then
    return 0
  fi

  if yt-dlp \
    --no-update \
    --flat-playlist \
    --playlist-end 1 \
    --dump-single-json \
    --no-warnings \
    "https://www.youtube.com/channel/${channel_id}/videos" > "${temp_file}" \
    && jq -e '.id and .title' "${temp_file}" >/dev/null 2>&1; then
    mv "${temp_file}" "${output_file}"
    return 0
  fi

  rm -f "${temp_file}"
  jq -n \
    --arg channel_id "${channel_id}" \
    '{id: $channel_id, audit_collection_error: "channel metadata unavailable"}' \
    > "${output_file}"
}

export -f fetch_channel
export raw_dir

tail -n +2 "${manifest}" | cut -f1 | xargs -P 2 -n 1 bash -c 'fetch_channel "$1"' _

jq -s '
  map({
    channel_id: .id,
    title,
    channel,
    uploader,
    uploader_id,
    uploader_url,
    description,
    collection_error: .audit_collection_error
  })
' "${raw_dir}"/*.json > "${audit_dir}/channel-descriptions.json"

jq -r '
  ["channel_id","channel","uploader_id","uploader_url","description","collection_error"],
  (.[] | [
    .channel_id,
    (.channel // .title),
    .uploader_id,
    .uploader_url,
    .description,
    .collection_error
  ]) | @csv
' "${audit_dir}/channel-descriptions.json" > "${audit_dir}/channel-descriptions.csv"

printf 'channels=%s metadata_ok=%s errors=%s\n' \
  "$(tail -n +2 "${manifest}" | wc -l | tr -d ' ')" \
  "$(jq '[.[] | select(.collection_error == null)] | length' "${audit_dir}/channel-descriptions.json")" \
  "$(jq '[.[] | select(.collection_error != null)] | length' "${audit_dir}/channel-descriptions.json")"
