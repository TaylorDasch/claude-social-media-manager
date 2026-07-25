#!/usr/bin/env bash
set -euo pipefail

audit_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
manifest="${audit_dir}/root-full-catalog-channels.tsv"
raw_dir="${audit_dir}/raw/flat-catalogs"
log_dir="${audit_dir}/raw/catalog-logs"
mkdir -p "${raw_dir}" "${log_dir}"

collect_tab() {
  local channel_id="$1"
  local tab_name="$2"
  local output_file="${raw_dir}/${channel_id}-${tab_name}.jsonl"
  local temp_file="${output_file}.tmp"
  local log_file="${log_dir}/${channel_id}-${tab_name}.log"

  if [[ -s "${output_file}" ]] && jq -s -e 'all(.[]; .id)' "${output_file}" >/dev/null 2>&1; then
    return 0
  fi

  : > "${log_file}"
  if yt-dlp \
    --no-update \
    --flat-playlist \
    --playlist-end 1000 \
    --skip-download \
    --dump-json \
    --no-warnings \
    "https://www.youtube.com/channel/${channel_id}/${tab_name}" \
    > "${temp_file}" 2> "${log_file}"; then
    if [[ ! -s "${temp_file}" ]] || jq -s -e 'all(.[]; .id)' "${temp_file}" >/dev/null 2>&1; then
      mv "${temp_file}" "${output_file}"
      return 0
    fi
  fi

  if [[ -s "${temp_file}" ]] && jq -s -e 'all(.[]; .id)' "${temp_file}" >/dev/null 2>&1; then
    mv "${temp_file}" "${output_file}"
    printf 'partial\n' > "${output_file}.status"
    return 0
  fi

  rm -f "${temp_file}"
  printf 'failed\n' > "${output_file}.status"
}

collect_channel() {
  local channel_id="$1"
  collect_tab "${channel_id}" "videos"
  collect_tab "${channel_id}" "shorts"
}

while IFS=$'\t' read -r channel_id channel_name inclusion_basis; do
  [[ "${channel_id}" == "channel_id" ]] && continue
  collect_channel "${channel_id}"
done < "${manifest}"

node "${audit_dir}/collect-player-metadata.mjs"

printf 'channels=%s videos=%s failed_tabs=%s partial_tabs=%s\\n' \
  "$(tail -n +2 "${manifest}" | cut -f1 | sort -u | wc -l | tr -d ' ')" \
  "$(jq 'length' "${audit_dir}/root-channel-catalog.json")" \
  "$(find "${raw_dir}" -name '*.status' -exec grep -l '^failed$' {} + 2>/dev/null | wc -l | tr -d ' ')" \
  "$(find "${raw_dir}" -name '*.status' -exec grep -l '^partial$' {} + 2>/dev/null | wc -l | tr -d ' ')"
