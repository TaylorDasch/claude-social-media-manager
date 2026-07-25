#!/usr/bin/env bash
set -euo pipefail

audit_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
query_file="${audit_dir}/search-queries.txt"
raw_dir="${audit_dir}/raw/search"
mkdir -p "${raw_dir}"

run_query() {
  local index="$1"
  local mode="$2"
  local query="$3"
  local output_file="${raw_dir}/${index}-${mode}.json"
  local temp_file="${output_file}.tmp"
  local search_term="${query}"

  if [[ "${mode}" == "current" ]]; then
    search_term="${query} 2025 2026"
  fi

  if [[ -s "${output_file}" ]] && jq -e '.entries | type == "array"' "${output_file}" >/dev/null 2>&1; then
    return 0
  fi

  local attempt
  for attempt in 1 2 3; do
    if yt-dlp \
      --no-update \
      --flat-playlist \
      --dump-single-json \
      --no-warnings \
      "ytsearch35:${search_term}" > "${temp_file}" \
      && jq -e '.entries | type == "array"' "${temp_file}" >/dev/null 2>&1; then
      mv "${temp_file}" "${output_file}"
      return 0
    fi
    rm -f "${temp_file}"
  done

  jq -n \
    --arg query "${query}" \
    --arg mode "${mode}" \
    '{entries: [], audit_collection_error: "yt-dlp search failed after three attempts", query: $query, mode: $mode}' \
    > "${output_file}"
}

export -f run_query
export raw_dir

work_file="$(mktemp)"
trap 'rm -f "${work_file}"' EXIT

index=0
while IFS= read -r query; do
  [[ -z "${query}" ]] && continue
  index=$((index + 1))
  printf '%04d\0%s\0%s\0' "${index}" "relevance" "${query}" >> "${work_file}"
  printf '%04d\0%s\0%s\0' "${index}" "current" "${query}" >> "${work_file}"
done < "${query_file}"

xargs -0 -P 2 -n 3 bash -c 'run_query "$@"' _ < "${work_file}"

jq -n \
  --arg audit_date "2026-07-24" \
  --arg window_start "2024-07-24" \
  --slurpfile entries <(
    for result_file in "${raw_dir}"/*.json; do
      stem="$(basename "${result_file}" .json)"
      index="${stem%%-*}"
      mode="${stem#*-}"
      query="$(sed -n "$((10#${index}))p" "${query_file}")"
      jq \
        --arg query "${query}" \
        --arg mode "${mode}" \
        '[.entries[]? | {
          id,
          url,
          title,
          channel,
          channel_id,
          channel_url,
          duration,
          view_count,
          query: $query,
          search_mode: $mode
        }]' "${result_file}"
    done
  ) \
  '{
    audit_date: $audit_date,
    window_start: $window_start,
    search_rows: ($entries | add),
    unique_videos: ($entries | add | unique_by(.id))
  }' > "${audit_dir}/search-results.json"

jq -r '
  ["video_id","title","channel","channel_id","url","duration_seconds","view_count"],
  (.unique_videos[] | [
    .id,
    .title,
    .channel,
    .channel_id,
    .url,
    .duration,
    .view_count
  ]) | @csv
' "${audit_dir}/search-results.json" > "${audit_dir}/search-results.csv"

printf 'queries=%s raw_searches=%s unique_videos=%s\n' \
  "$(grep -cve '^$' "${query_file}")" \
  "$(find "${raw_dir}" -type f -name '*.json' | wc -l | tr -d ' ')" \
  "$(jq '.unique_videos | length' "${audit_dir}/search-results.json")"
