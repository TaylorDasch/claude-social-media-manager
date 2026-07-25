#!/usr/bin/env node

/*
 * Offline catalog builder for authenticated yt-dlp exports.
 *
 * This deliberately does not invoke yt-dlp, a browser, or any credential store.
 * Place yt-dlp --write-info-json / subtitle artifacts beneath either:
 *   raw/authenticated-root/
 *   raw/authenticated-discovery/
 * then run this file from any working directory.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const sourceRoots = [
  { source: "root", directory: path.join(auditDir, "raw", "authenticated-root") },
  { source: "discovery", directory: path.join(auditDir, "raw", "authenticated-discovery") },
];
const catalogPath = path.join(auditDir, "authenticated-video-catalog.json");
const catalogCsvPath = path.join(auditDir, "authenticated-video-catalog.csv");
const summaryPath = path.join(auditDir, "authenticated-coverage-summary.json");
const startDate = "2024-07-24";
const endDate = "2026-07-24";
const excludedTaylorChannels = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);
const captionExtensions = new Set([".srt", ".vtt", ".ttml", ".srv1", ".srv2", ".srv3", ".json3", ".lrc"]);

function toPosix(relativePath) {
  return relativePath.split(path.sep).join("/");
}

function csvCell(value) {
  const text = Array.isArray(value) ? value.join(";") : value == null ? "" : String(value);
  return `"${text.replaceAll('"', '""')}"`;
}

function cleanText(value) {
  return typeof value === "string" ? value : value == null ? "" : String(value);
}

function normaliseDate(value) {
  const raw = cleanText(value).trim();
  if (/^\d{8}$/.test(raw)) return `${raw.slice(0, 4)}-${raw.slice(4, 6)}-${raw.slice(6, 8)}`;
  const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})/);
  return match ? `${match[1]}-${match[2]}-${match[3]}` : "";
}

function videoIdFromFilename(filename) {
  // yt-dlp's default %(title)s [%(id)s].%(ext)s template is the most reliable
  // filename signal. The dated fallback supports this audit's
  // %(upload_date)s_%(id)s.%(ext)s template, including IDs that begin with "_".
  const bracketed = filename.match(/\[([A-Za-z0-9_-]{6,})\](?:\.[^.]+)+$/)?.[1];
  if (bracketed) return bracketed;
  const dated = filename.match(/^\d{8}_([A-Za-z0-9_-]{11})(?=(?:\.[^.]+)+$)/)?.[1];
  if (dated) return dated;
  return filename.match(/(?:^|[^A-Za-z0-9_-])([A-Za-z0-9_-]{11})(?=[^A-Za-z0-9_-]|$)/)?.[1] ?? "";
}

function sourceForPath(filePath) {
  for (const root of sourceRoots) {
    if (filePath === root.directory || filePath.startsWith(`${root.directory}${path.sep}`)) return root.source;
  }
  return "";
}

function resolveChannelId(info, filePath) {
  const channelIdPattern = /^UC[A-Za-z0-9_-]{20,}$/;
  const pathChannelId = filePath
    .split(path.sep)
    .find((segment) => channelIdPattern.test(segment));
  const urlChannelId = [
    info.channel_url,
    info.uploader_url,
    info.playlist_webpage_url,
  ]
    .map((value) => cleanText(value).match(/\/channel\/(UC[A-Za-z0-9_-]{20,})/)?.[1] ?? "")
    .find(Boolean);
  const candidates = [
    info.channel_id,
    info.playlist_channel_id,
    info.playlist_uploader_id,
    info.playlist_id,
    pathChannelId,
    urlChannelId,
    info.uploader_id,
  ].map((value) => cleanText(value).trim());
  return candidates.find((value) => channelIdPattern.test(value)) ?? "";
}

async function walk(directory) {
  const files = [];
  try {
    const entries = await fs.readdir(directory, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(directory, entry.name);
      if (entry.isDirectory()) files.push(...await walk(fullPath));
      else if (entry.isFile()) files.push(fullPath);
    }
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
  return files;
}

function isCaptionFile(filePath) {
  const name = path.basename(filePath).toLowerCase();
  return !name.endsWith(".info.json") && captionExtensions.has(path.extname(name));
}

function classifyContentType(info, duration) {
  const liveStatus = cleanText(info.live_status).toLowerCase();
  if (["was_live", "is_live", "post_live"].includes(liveStatus)) return "live";
  const direct = cleanText(info.content_type || info._type || info.media_type).toLowerCase();
  if (direct.includes("short")) return "short";
  if (direct.includes("livestream") || direct.includes("live")) return "live";
  if (Number.isFinite(duration) && duration > 0 && duration <= 60) return "short";
  return "video";
}

function chooseValue(existing, candidate) {
  return existing || candidate || "";
}

const allFiles = (await Promise.all(sourceRoots.map((root) => walk(root.directory)))).flat().sort();
const captionsById = new Map();
for (const filePath of allFiles) {
  if (!isCaptionFile(filePath)) continue;
  const id = videoIdFromFilename(path.basename(filePath));
  if (!id) continue;
  const files = captionsById.get(id) ?? [];
  files.push(toPosix(path.relative(auditDir, filePath)));
  captionsById.set(id, files);
}
for (const paths of captionsById.values()) paths.sort();

const unreadableFiles = [];
const outOfWindowFiles = [];
const excludedFiles = [];
const nonPublicFiles = [];
const byId = new Map();
let infoFilesSeen = 0;

for (const filePath of allFiles.filter((file) => file.endsWith(".info.json"))) {
  infoFilesSeen += 1;
  let info;
  try {
    info = JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    unreadableFiles.push({
      path: toPosix(path.relative(auditDir, filePath)),
      error: cleanText(error?.message || error),
    });
    continue;
  }

  const id = cleanText(info.id || videoIdFromFilename(path.basename(filePath))).trim();
  if (!id) {
    unreadableFiles.push({
      path: toPosix(path.relative(auditDir, filePath)),
      error: "Missing video ID in info JSON and filename",
    });
    continue;
  }
  const channelId = resolveChannelId(info, filePath);
  if (!channelId) {
    unreadableFiles.push({
      path: toPosix(path.relative(auditDir, filePath)),
      error: "Missing canonical UC channel ID",
    });
    continue;
  }
  if (excludedTaylorChannels.has(channelId)) {
    excludedFiles.push(toPosix(path.relative(auditDir, filePath)));
    continue;
  }
  const availability = cleanText(info.availability).trim().toLowerCase();
  if (availability !== "public") {
    nonPublicFiles.push({
      path: toPosix(path.relative(auditDir, filePath)),
      id,
      availability: availability || "unknown_or_unverified",
    });
    continue;
  }
  const uploadDate = normaliseDate(info.upload_date || info.release_date || info.timestamp && new Date(info.timestamp * 1000).toISOString());
  if (!uploadDate || uploadDate < startDate || uploadDate > endDate) {
    outOfWindowFiles.push({
      path: toPosix(path.relative(auditDir, filePath)),
      id,
      upload_date: uploadDate,
    });
    continue;
  }

  const source = sourceForPath(filePath);
  const durationValue = Number(info.duration);
  const duration = Number.isFinite(durationValue) ? durationValue : null;
  const candidate = {
    id,
    url: cleanText(info.webpage_url || info.original_url || `https://www.youtube.com/watch?v=${id}`),
    title: cleanText(info.title || info.fulltitle),
    description: cleanText(info.description),
    upload_date: uploadDate,
    channel: cleanText(info.channel || info.uploader),
    channel_id: channelId,
    duration,
    content_type: classifyContentType(info, duration),
    caption_file_paths: captionsById.get(id) ?? [],
    sources: [source],
    info_file_paths: [toPosix(path.relative(auditDir, filePath))],
  };
  const existing = byId.get(id);
  if (!existing) {
    byId.set(id, candidate);
    continue;
  }
  existing.url = chooseValue(existing.url, candidate.url);
  existing.title = chooseValue(existing.title, candidate.title);
  existing.description = chooseValue(existing.description, candidate.description);
  existing.upload_date = chooseValue(existing.upload_date, candidate.upload_date);
  existing.channel = chooseValue(existing.channel, candidate.channel);
  existing.channel_id = chooseValue(existing.channel_id, candidate.channel_id);
  existing.duration ??= candidate.duration;
  if (existing.content_type === "video" && candidate.content_type !== "video") existing.content_type = candidate.content_type;
  existing.sources = [...new Set([...existing.sources, ...candidate.sources])].sort();
  existing.info_file_paths = [...new Set([...existing.info_file_paths, ...candidate.info_file_paths])].sort();
  existing.caption_file_paths = [...new Set([...existing.caption_file_paths, ...candidate.caption_file_paths])].sort();
}

// A small number of otherwise valid video records can omit the channel name
// even though sibling records from the same channel ID contain it. Canonicalize
// names by channel ID before producing the catalog so one incomplete metadata
// object cannot split a channel into duplicate coverage rows. The most frequent
// non-empty public name wins; ties are deterministic.
const channelNameCounts = new Map();
for (const item of byId.values()) {
  item.channel = cleanText(item.channel).trim();
  item.channel_id = cleanText(item.channel_id).trim();
  if (!item.channel_id || !item.channel) continue;
  const counts = channelNameCounts.get(item.channel_id) ?? new Map();
  counts.set(item.channel, (counts.get(item.channel) ?? 0) + 1);
  channelNameCounts.set(item.channel_id, counts);
}
const canonicalChannelNames = new Map(
  [...channelNameCounts].map(([channelId, counts]) => [
    channelId,
    [...counts]
      .sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0]))[0][0],
  ]),
);
for (const item of byId.values()) {
  const canonicalName = canonicalChannelNames.get(item.channel_id);
  if (canonicalName) item.channel = canonicalName;
}

const catalog = [...byId.values()]
  .map((item) => ({ ...item, has_captions: item.caption_file_paths.length > 0 }))
  .sort((a, b) => a.channel.localeCompare(b.channel) || a.upload_date.localeCompare(b.upload_date) || a.id.localeCompare(b.id));

const channels = new Map();
for (const item of catalog) {
  const key = `${item.channel_id}\u0000${item.channel}`;
  const row = channels.get(key) ?? {
    channel: item.channel,
    channel_id: item.channel_id,
    videos: 0,
    shorts: 0,
    live: 0,
    total: 0,
    with_captions: 0,
    without_captions: 0,
    caption_file_count: 0,
    root: 0,
    discovery: 0,
    both_sources: 0,
  };
  row.total += 1;
  if (item.content_type === "short") row.shorts += 1;
  else if (item.content_type === "live") row.live += 1;
  else row.videos += 1;
  if (item.has_captions) row.with_captions += 1;
  else row.without_captions += 1;
  row.caption_file_count += item.caption_file_paths.length;
  if (item.sources.includes("root")) row.root += 1;
  if (item.sources.includes("discovery")) row.discovery += 1;
  if (item.sources.length > 1) row.both_sources += 1;
  channels.set(key, row);
}

const coverage = {
  generated_at: new Date().toISOString(),
  audit_window: { start: startDate, end: endDate, inclusive: true },
  inputs: Object.fromEntries(sourceRoots.map((root) => [root.source, toPosix(path.relative(auditDir, root.directory))])),
  counts: {
    files_scanned: allFiles.length,
    info_files_seen: infoFilesSeen,
    catalog_videos: catalog.length,
    videos_with_captions: catalog.filter((item) => item.has_captions).length,
    caption_files_linked: catalog.reduce((sum, item) => sum + item.caption_file_paths.length, 0),
    unreadable_info_files: unreadableFiles.length,
    excluded_taylor_info_files: excludedFiles.length,
    non_public_info_files: nonPublicFiles.length,
    out_of_window_info_files: outOfWindowFiles.length,
  },
  channels: [...channels.values()].sort((a, b) => a.channel.localeCompare(b.channel) || a.channel_id.localeCompare(b.channel_id)),
  unreadable_files: unreadableFiles,
  excluded_taylor_files: excludedFiles.sort(),
  non_public_files: nonPublicFiles.sort((a, b) => a.path.localeCompare(b.path)),
  out_of_window_files: outOfWindowFiles.sort((a, b) => a.path.localeCompare(b.path)),
};

const csvHeaders = [
  "id", "url", "title", "description", "upload_date", "channel", "channel_id",
  "duration", "content_type", "has_captions", "caption_file_paths", "sources", "info_file_paths",
];
const csv = [
  csvHeaders.map(csvCell).join(","),
  ...catalog.map((item) => csvHeaders.map((header) => csvCell(item[header])).join(",")),
].join("\n");

await Promise.all([
  fs.writeFile(catalogPath, `${JSON.stringify(catalog, null, 2)}\n`),
  fs.writeFile(catalogCsvPath, `${csv}\n`),
  fs.writeFile(summaryPath, `${JSON.stringify(coverage, null, 2)}\n`),
]);

process.stderr.write(`Authenticated catalog: ${catalog.length} in-window videos from ${infoFilesSeen} info files; ${coverage.counts.videos_with_captions} with caption files.\n`);
