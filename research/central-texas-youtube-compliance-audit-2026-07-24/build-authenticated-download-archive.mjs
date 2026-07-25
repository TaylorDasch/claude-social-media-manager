#!/usr/bin/env node

/*
 * Builds a yt-dlp archive from video metadata already retained in the two
 * authenticated evidence roots. This lets a paced channel-tab resumption skip
 * completed public records while continuing through any holes in the
 * two-year inventory.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const roots = [
  path.join(auditDir, "raw", "authenticated-root"),
  path.join(auditDir, "raw", "authenticated-discovery"),
];
const outputPath = path.join(auditDir, "authenticated-existing-video.archive");
const videoIdPattern = /^[A-Za-z0-9_-]{11}$/;
const channelIdPattern = /^UC[A-Za-z0-9_-]{20,}$/;
const startDate = "2024-07-24";
const endDate = "2026-07-24";
const excludedTaylorChannelIds = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);

async function walk(directory) {
  const output = [];
  for (const entry of await fs.readdir(directory, { withFileTypes: true })) {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) output.push(...await walk(entryPath));
    else if (entry.isFile() && entry.name.endsWith(".info.json")) output.push(entryPath);
  }
  return output;
}

function clean(value) {
  return value == null ? "" : String(value).trim();
}

function normaliseDate(value) {
  const raw = clean(value);
  if (/^\d{8}$/.test(raw)) return `${raw.slice(0, 4)}-${raw.slice(4, 6)}-${raw.slice(6, 8)}`;
  const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})/);
  return match ? `${match[1]}-${match[2]}-${match[3]}` : "";
}

function resolveChannelId(item, filePath) {
  const pathChannelId = filePath
    .split(path.sep)
    .find((segment) => channelIdPattern.test(segment));
  const candidates = [
    item?.channel_id,
    item?.playlist_channel_id,
    item?.playlist_uploader_id,
    item?.playlist_id,
    pathChannelId,
    item?.uploader_id,
  ].map(clean);
  return candidates.find((value) => channelIdPattern.test(value)) ?? "";
}

const ids = new Set();
let skippedPlaylistRecords = 0;
let skippedTaylorRecords = 0;
let skippedNonPublicRecords = 0;
let skippedOutOfWindowRecords = 0;
for (const root of roots) {
  for (const filePath of await walk(root)) {
    const item = JSON.parse(await fs.readFile(filePath, "utf8"));
    const id = clean(item?.id);
    const channelId = resolveChannelId(item, filePath);
    if (excludedTaylorChannelIds.has(channelId)) {
      skippedTaylorRecords += 1;
      continue;
    }
    if (!videoIdPattern.test(id)) {
      skippedPlaylistRecords += 1;
      continue;
    }
    if (clean(item?.availability).toLowerCase() !== "public") {
      skippedNonPublicRecords += 1;
      continue;
    }
    const uploadDate = normaliseDate(
      item?.upload_date
      || item?.release_date
      || (item?.timestamp ? new Date(Number(item.timestamp) * 1000).toISOString() : ""),
    );
    if (!uploadDate || uploadDate < startDate || uploadDate > endDate) {
      skippedOutOfWindowRecords += 1;
      continue;
    }
    ids.add(id);
  }
}

const lines = [...ids].sort().map((id) => `youtube ${id}`);
await fs.writeFile(outputPath, `${lines.join("\n")}\n`);
process.stderr.write(
  `yt-dlp archive: ${lines.length} video IDs; `
  + `${skippedPlaylistRecords} playlist/channel records skipped; `
  + `${skippedTaylorRecords} Taylor records skipped; `
  + `${skippedNonPublicRecords} nonpublic/unverified records skipped; `
  + `${skippedOutOfWindowRecords} out-of-window records skipped.\n`,
);
