#!/usr/bin/env node

/*
 * Applies the authenticated root-scope adjudication to collection inputs:
 * locally based creators keep full Videos/Shorts tabs; statewide, national,
 * or out-of-market channels keep only the directly discovered target-city
 * videos.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const scopePath = path.join(auditDir, "root-scope-adjudication.tsv");
const searchPath = path.join(auditDir, "search-results.json");
const rootManifestNames = [
  "authenticated-root-inputs-shard-1.txt",
  "authenticated-root-inputs-shard-2.txt",
  "authenticated-root-inputs-shard-3.txt",
];
const fullOutputPath = path.join(auditDir, "authenticated-root-local-channel-inputs.txt");
const directOutputPath = path.join(auditDir, "authenticated-root-direct-video-inputs.txt");
const excludedTaylorChannelIds = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);

function parseTsv(text) {
  const lines = text.replace(/\r/g, "").split(/\n/).filter(Boolean);
  const headers = lines.shift().split("\t");
  return lines.map((line) => {
    const fields = line.split("\t");
    if (fields.length !== headers.length) throw new Error(`Malformed scope TSV row: ${line}`);
    return Object.fromEntries(headers.map((header, index) => [header, fields[index]]));
  });
}

const scopeRows = parseTsv(await fs.readFile(scopePath, "utf8"));
if (scopeRows.length !== 47) throw new Error(`Expected 47 scope rows; got ${scopeRows.length}`);
const fullIds = new Set(
  scopeRows
    .filter((row) => row.recommended_lane === "full_channel_local_creator")
    .map((row) => row.channel_id),
);
const directIds = new Set(
  scopeRows
    .filter((row) => row.recommended_lane === "direct_target_videos_only")
    .map((row) => row.channel_id),
);
if (fullIds.size !== 42 || directIds.size !== 5) {
  throw new Error(`Unexpected lane totals: ${fullIds.size} full, ${directIds.size} direct`);
}
for (const channelId of [...fullIds, ...directIds]) {
  if (excludedTaylorChannelIds.has(channelId)) throw new Error(`Taylor channel survived scope: ${channelId}`);
}

const originalUrls = [];
for (const name of rootManifestNames) {
  originalUrls.push(
    ...(await fs.readFile(path.join(auditDir, name), "utf8"))
      .split(/\n/)
      .map((line) => line.trim())
      .filter(Boolean),
  );
}
const fullUrls = [...new Set(originalUrls.filter((url) => {
  const match = url.match(/\/channel\/(UC[A-Za-z0-9_-]{20,})\//);
  return match && fullIds.has(match[1]);
}))];
if (fullUrls.length !== fullIds.size * 2) {
  throw new Error(`Expected ${fullIds.size * 2} local full-channel tab URLs; got ${fullUrls.length}`);
}

const search = JSON.parse(await fs.readFile(searchPath, "utf8"));
if (!Array.isArray(search.unique_videos)) throw new Error("search-results.json is missing unique_videos");
const directVideos = search.unique_videos
  .filter((video) => directIds.has(String(video.channel_id ?? "")))
  .filter((video) => /^[A-Za-z0-9_-]{11}$/.test(String(video.id ?? "")));
const directUrls = [...new Set(directVideos.map((video) => `https://www.youtube.com/watch?v=${video.id}`))];
if (!directUrls.length) throw new Error("No direct target-city videos found for root scope overrides");

await Promise.all([
  fs.writeFile(fullOutputPath, `${fullUrls.join("\n")}\n`),
  fs.writeFile(directOutputPath, `${directUrls.join("\n")}\n`),
]);
process.stderr.write(
  `Root scope inputs: ${fullIds.size} local full channels (${fullUrls.length} tabs); `
  + `${directIds.size} direct-only channels (${directUrls.length} discovered videos).\n`,
);
