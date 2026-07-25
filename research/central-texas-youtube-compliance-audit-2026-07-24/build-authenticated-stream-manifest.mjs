#!/usr/bin/env node

/*
 * Builds the archived-livestream tab manifest for every adjudicated
 * full-channel identity. Videos and Shorts are collected separately; the
 * /streams pass closes the remaining public-upload tab.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const rootScopePath = path.join(auditDir, "root-scope-adjudication.tsv");
const gapFullPath = path.join(auditDir, "authenticated-gap-full-channel-inputs.txt");
const outputPath = path.join(auditDir, "authenticated-full-channel-stream-inputs.txt");
const manualAndZeroEligibleIds = [
  "UC1SKo4gUtYWElAGwZSguqpA",
  "UCqo6EaV9o6bFg4szBL8RYEw",
  "UCwoQakQVf2m8hfitYnymb5w",
  "UCeZysVNyhl-JqrqesQjcqPg",
  "UCijF1zTR7RluBFGicVZU4SA",
  "UCvyNP3_ZgVLciAIev5t2Gog",
  "UCWykQcBeQE_1yY2lk9m23YQ",
  "UC5v4flYtIbs8z1ZQ-d-nGXw",
];
const excludedTaylorIds = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);

function fail(message) {
  throw new Error(`STREAM MANIFEST BUILD FAILED: ${message}`);
}

function parseTsv(text) {
  const lines = text.replaceAll("\r", "").split("\n").filter(Boolean);
  const headers = lines.shift().split("\t");
  return lines.map((line, rowIndex) => {
    const values = line.split("\t");
    if (values.length !== headers.length) fail(`root scope row ${rowIndex + 2} has the wrong column count`);
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

const [rootScopeText, gapFullText] = await Promise.all([
  fs.readFile(rootScopePath, "utf8"),
  fs.readFile(gapFullPath, "utf8"),
]);
const rootFullIds = parseTsv(rootScopeText)
  .filter((row) => row.recommended_lane === "full_channel_local_creator")
  .map((row) => row.channel_id);
const gapFullIds = [...gapFullText.matchAll(/\/channel\/(UC[A-Za-z0-9_-]{20,})\//g)]
  .map((match) => match[1]);
const channelIds = [...new Set([...manualAndZeroEligibleIds, ...rootFullIds, ...gapFullIds])].sort();

if (rootFullIds.length !== 42) fail(`expected 42 root full-channel IDs, got ${rootFullIds.length}`);
if (new Set(gapFullIds).size !== 24) fail(`expected 24 discovery-gap full-channel IDs, got ${new Set(gapFullIds).size}`);
if (channelIds.length !== 74) fail(`expected 74 adjudicated full-channel identities, got ${channelIds.length}`);
for (const channelId of channelIds) {
  if (excludedTaylorIds.has(channelId)) fail(`excluded Taylor channel survived: ${channelId}`);
  if (!/^UC[A-Za-z0-9_-]{20,}$/.test(channelId)) fail(`malformed channel ID: ${channelId}`);
}

const urls = channelIds.map((channelId) => `https://www.youtube.com/channel/${channelId}/streams`);
await fs.writeFile(outputPath, `${urls.join("\n")}\n`);
process.stderr.write(`Stream manifest: ${urls.length} unique full-channel URLs.\n`);
