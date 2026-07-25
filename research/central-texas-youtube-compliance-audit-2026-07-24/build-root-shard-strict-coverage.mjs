#!/usr/bin/env node

/*
 * Reconciles the two authenticated root-channel shards against the exact audit
 * window. This is an offline check: it reads completed yt-dlp artifacts and
 * writes a per-channel ledger plus a machine-readable summary.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const rawRoot = path.join(auditDir, "raw", "authenticated-root");
const startDate = "2024-07-24";
const endDate = "2026-07-24";
const manifests = [
  "authenticated-root-local-shard-a.txt",
  "authenticated-root-local-shard-b.txt",
];
const statusFiles = [
  "authenticated-root-local-shard-a-collection-status.tsv",
  "authenticated-root-local-shard-b-collection-status.tsv",
];
const streamStatusFile = "authenticated-full-channel-stream-inputs-collection-status.tsv";
const rootManifest = "root-full-catalog-channels.tsv";
const outputTsv = path.join(auditDir, "root-shards-strict-coverage.tsv");
const outputJson = path.join(auditDir, "root-shards-strict-coverage.json");
const terminalStatuses = new Set(["complete", "cutoff_complete", "no_tab"]);
const captionExtensions = new Set([".srt", ".vtt", ".ttml", ".srv1", ".srv2", ".srv3", ".json3", ".lrc"]);

function fail(message) {
  throw new Error(`ROOT SHARD COVERAGE FAILED: ${message}`);
}

function clean(value) {
  return value == null ? "" : String(value).replaceAll("\r", "").trim();
}

function normalizeDate(value) {
  const raw = clean(value);
  if (/^\d{8}$/.test(raw)) return `${raw.slice(0, 4)}-${raw.slice(4, 6)}-${raw.slice(6, 8)}`;
  const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})/);
  return match ? `${match[1]}-${match[2]}-${match[3]}` : "";
}

function videoIdFromFilename(filename) {
  const dated = filename.match(/^\d{8}_([A-Za-z0-9_-]{11})(?=(?:\.[^.]+)+$)/)?.[1];
  if (dated) return dated;
  return filename.match(/(?:^|[^A-Za-z0-9_-])([A-Za-z0-9_-]{11})(?=[^A-Za-z0-9_-]|$)/)?.[1] ?? "";
}

async function walk(directory) {
  const files = [];
  let entries;
  try {
    entries = await fs.readdir(directory, { withFileTypes: true });
  } catch (error) {
    if (error?.code === "ENOENT") return files;
    throw error;
  }
  for (const entry of entries) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) files.push(...await walk(fullPath));
    else if (entry.isFile()) files.push(fullPath);
  }
  return files;
}

function parseTsv(text, label) {
  const lines = text.split(/\n/).filter((line) => clean(line));
  if (!lines.length) fail(`${label} is empty`);
  const headers = lines.shift().split("\t").map(clean);
  return lines.map((line, index) => {
    const values = line.split("\t");
    if (values.length !== headers.length) fail(`${label} row ${index + 2} has the wrong column count`);
    return Object.fromEntries(headers.map((header, fieldIndex) => [header, clean(values[fieldIndex])]));
  });
}

const manifestTexts = await Promise.all(
  manifests.map((name) => fs.readFile(path.join(auditDir, name), "utf8")),
);
const manifestUrls = manifestTexts.flatMap((text) => text.split(/\n/).map(clean).filter(Boolean));
if (manifestUrls.length !== 84 || new Set(manifestUrls).size !== 84) {
  fail(`expected 84 unique root-shard URLs, got ${manifestUrls.length}/${new Set(manifestUrls).size}`);
}
const channelIds = [...new Set(manifestUrls.map((url) => {
  const id = url.match(/\/channel\/(UC[A-Za-z0-9_-]{20,})\//)?.[1];
  if (!id) fail(`cannot parse channel ID from ${url}`);
  return id;
}))].sort();
if (channelIds.length !== 42) fail(`expected 42 unique root-shard channels, got ${channelIds.length}`);
const rootRows = parseTsv(await fs.readFile(path.join(auditDir, rootManifest), "utf8"), rootManifest);
const rootNames = new Map(rootRows.map((row) => [row.channel_id, row.channel_name]));
for (const channelId of channelIds) {
  if (!rootNames.get(channelId)) fail(`${rootManifest} is missing ${channelId}`);
}

const statusTexts = await Promise.all(statusFiles.map(async (name) => {
  try {
    return await fs.readFile(path.join(auditDir, name), "utf8");
  } catch (error) {
    fail(`${name} is unavailable; run this check only after both collectors finish (${clean(error?.message || error)})`);
  }
}));
const statusRows = statusTexts.flatMap((text, index) => parseTsv(text, statusFiles[index]));
if (statusRows.length !== 84) fail(`expected 84 status rows, got ${statusRows.length}`);
const statusByUrl = new Map();
for (const row of statusRows) {
  if (statusByUrl.has(row.url)) fail(`duplicate status URL ${row.url}`);
  statusByUrl.set(row.url, row);
}
for (const url of manifestUrls) {
  const row = statusByUrl.get(url);
  if (!row) fail(`missing status row for ${url}`);
  if (!terminalStatuses.has(row.status)) fail(`non-terminal status ${row.status} for ${url}`);
}
for (const url of statusByUrl.keys()) {
  if (!manifestUrls.includes(url)) fail(`unexpected status URL ${url}`);
}
const streamStatusRows = parseTsv(
  await fs.readFile(path.join(auditDir, streamStatusFile), "utf8"),
  streamStatusFile,
).filter((row) => channelIds.includes(row.channel_id));
if (streamStatusRows.length !== 42) fail(`expected 42 root-channel stream status rows, got ${streamStatusRows.length}`);
const streamStatusByChannel = new Map();
for (const row of streamStatusRows) {
  if (streamStatusByChannel.has(row.channel_id)) fail(`duplicate stream status for ${row.channel_id}`);
  if (row.tab !== "streams") fail(`unexpected stream tab label ${row.tab} for ${row.channel_id}`);
  if (!terminalStatuses.has(row.status)) fail(`non-terminal stream status ${row.status} for ${row.channel_id}`);
  streamStatusByChannel.set(row.channel_id, row);
}
for (const channelId of channelIds) {
  if (!streamStatusByChannel.has(channelId)) fail(`missing stream status for ${channelId}`);
}

const rows = [];
const exclusions = {
  out_of_window: [],
  non_public: [],
  no_date_or_profile: [],
  unreadable: [],
};
for (const channelId of channelIds) {
  const directory = path.join(rawRoot, channelId);
  const files = await walk(directory);
  const captionIds = new Set(
    files
      .filter((file) => !file.endsWith(".info.json") && captionExtensions.has(path.extname(file).toLowerCase()))
      .map((file) => videoIdFromFilename(path.basename(file)))
      .filter(Boolean),
  );
  const publicIds = new Set();
  let recoveredChannelName = "";
  let infoFiles = 0;
  let outOfWindow = 0;
  let nonPublic = 0;
  let noDate = 0;
  for (const file of files.filter((candidate) => candidate.endsWith(".info.json")).sort()) {
    infoFiles += 1;
    let info;
    try {
      info = JSON.parse(await fs.readFile(file, "utf8"));
    } catch (error) {
      exclusions.unreadable.push({ path: path.relative(auditDir, file), error: clean(error?.message || error) });
      continue;
    }
    recoveredChannelName ||= clean(info.channel || info.uploader);
    const id = clean(info.id || videoIdFromFilename(path.basename(file)));
    const date = normalizeDate(
      info.upload_date
      || info.release_date
      || (info.timestamp ? new Date(Number(info.timestamp) * 1000).toISOString() : ""),
    );
    const availability = clean(info.availability).toLowerCase();
    const relativePath = path.relative(auditDir, file).split(path.sep).join("/");
    if (availability !== "public") {
      nonPublic += 1;
      exclusions.non_public.push({
        channel_id: channelId,
        id,
        availability: availability || "unknown_or_unverified",
        path: relativePath,
      });
      continue;
    }
    if (!date) {
      noDate += 1;
      exclusions.no_date_or_profile.push({ channel_id: channelId, id, path: relativePath });
      continue;
    }
    if (date < startDate || date > endDate) {
      outOfWindow += 1;
      exclusions.out_of_window.push({ channel_id: channelId, id, upload_date: date, path: relativePath });
      continue;
    }
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) fail(`eligible record has malformed video ID ${id} in ${relativePath}`);
    publicIds.add(id);
  }
  const withCaptions = [...publicIds].filter((id) => captionIds.has(id)).length;
  rows.push({
    channel_id: channelId,
    channel_name: rootNames.get(channelId),
    recovered_channel_name: recoveredChannelName,
    info_files_seen: infoFiles,
    public_in_window_uploads: publicIds.size,
    uploads_with_caption_artifacts: withCaptions,
    uploads_without_caption_artifacts: publicIds.size - withCaptions,
    out_of_window_info_files: outOfWindow,
    non_public_info_files: nonPublic,
    no_date_or_profile_info_files: noDate,
  });
}

const totals = rows.reduce((aggregate, row) => ({
  channels: aggregate.channels + 1,
  info_files_seen: aggregate.info_files_seen + row.info_files_seen,
  public_in_window_uploads: aggregate.public_in_window_uploads + row.public_in_window_uploads,
  uploads_with_caption_artifacts: aggregate.uploads_with_caption_artifacts + row.uploads_with_caption_artifacts,
  uploads_without_caption_artifacts: aggregate.uploads_without_caption_artifacts + row.uploads_without_caption_artifacts,
  out_of_window_info_files: aggregate.out_of_window_info_files + row.out_of_window_info_files,
  non_public_info_files: aggregate.non_public_info_files + row.non_public_info_files,
  no_date_or_profile_info_files: aggregate.no_date_or_profile_info_files + row.no_date_or_profile_info_files,
}), {
  channels: 0,
  info_files_seen: 0,
  public_in_window_uploads: 0,
  uploads_with_caption_artifacts: 0,
  uploads_without_caption_artifacts: 0,
  out_of_window_info_files: 0,
  non_public_info_files: 0,
  no_date_or_profile_info_files: 0,
});

const headers = Object.keys(rows[0]);
const tsv = [
  headers.join("\t"),
  ...rows.map((row) => headers.map((header) => String(row[header] ?? "").replaceAll("\t", " ")).join("\t")),
].join("\n");
const summary = {
  generated_at: new Date().toISOString(),
  audit_window: { start: startDate, end: endDate, inclusive: true },
  manifests,
  root_manifest: rootManifest,
  status_files: statusFiles,
  stream_status_file: streamStatusFile,
  terminal_statuses: [...terminalStatuses].sort(),
  totals,
  channels: rows,
  exclusions,
  validation: {
    input_urls: manifestUrls.length,
    unique_input_urls: new Set(manifestUrls).size,
    unique_channel_ids: channelIds.length,
    terminal_status_rows: statusRows.length,
    terminal_root_stream_status_rows: streamStatusRows.length,
    all_statuses_terminal: true,
  },
};

await Promise.all([
  fs.writeFile(outputTsv, `${tsv}\n`),
  fs.writeFile(outputJson, `${JSON.stringify(summary, null, 2)}\n`),
]);
process.stderr.write(
  `Root shard coverage: ${totals.channels} channels, ${totals.public_in_window_uploads} public in-window uploads, `
  + `${totals.uploads_with_caption_artifacts} with caption artifacts.\n`,
);
