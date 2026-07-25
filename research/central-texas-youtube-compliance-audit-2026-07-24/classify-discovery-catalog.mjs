#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const discovery = JSON.parse(
  await fs.readFile(path.join(auditDir, "discovery-video-catalog.json"), "utf8"),
);
const manifestLines = (
  await fs.readFile(path.join(auditDir, "root-full-catalog-channels.tsv"), "utf8")
).trim().split("\n").slice(1);
const candidateLines = (
  await fs.readFile(path.join(auditDir, "candidate-channels.tsv"), "utf8")
).trim().split("\n").slice(1);

const auditedChannelIds = new Set(manifestLines.map((line) => line.split("\t")[0]));
for (const line of candidateLines) {
  const [channelId, , , lane] = line.split("\t");
  if (lane?.startsWith("audit_")) auditedChannelIds.add(channelId);
}
const excludedTaylorChannels = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);
const targetPlacePattern = /\b(?:Temple|Belton|Killeen|Harker Heights|Copperas Cove|Nolanville|Fort (?:Hood|Cavazos)|Bell County)\b/i;
const housingPattern = /\b(?:real estate|realtor|home|house|housing|property|properties|apartment|rent|rental|listing|market|neighborhood|relocat|moving|builder|construction|duplex|mortgage|loan|land|acreage|invest)\w*/i;
const taylorFingerprintPattern = /\b(?:Taylor Dasch|Deals with Dasch|templetxhomes\.net)\b/i;

function csvCell(value) {
  const text = value == null ? "" : String(value);
  return `"${text.replaceAll('"', '""')}"`;
}

const classified = discovery.map((item) => {
  const text = `${item.title ?? ""}\n${item.description ?? ""}`;
  let classification;
  let reason;
  if (excludedTaylorChannels.has(item.channel_id) || taylorFingerprintPattern.test(text)) {
    classification = "excluded_taylor";
    reason = "Taylor-owned channel or Taylor-content fingerprint";
  } else if (auditedChannelIds.has(item.channel_id)) {
    classification = "full_channel_audit";
    reason = "Creator/channel included in the full local-channel audit";
  } else if (targetPlacePattern.test(text) && housingPattern.test(text)) {
    classification = "direct_video_extra";
    reason = "Target-place and housing/real-estate terms appear in the public title or description";
  } else {
    classification = "search_noise_or_unconfirmed";
    reason = "Search hit did not retain both a target-place and housing/real-estate signal in current metadata";
  }
  return { ...item, classification, classification_reason: reason };
});

await fs.writeFile(
  path.join(auditDir, "discovery-video-classification.json"),
  `${JSON.stringify(classified, null, 2)}\n`,
);
const header = [
  "classification",
  "classification_reason",
  "upload_date",
  "video_id",
  "channel_id",
  "channel",
  "title",
  "url",
  "query",
  "playability_status",
];
const rows = classified.map((item) => [
  item.classification,
  item.classification_reason,
  item.upload_date || item.publish_date,
  item.id,
  item.channel_id,
  item.channel,
  item.title,
  item.url,
  item.query,
  item.status,
]);
await fs.writeFile(
  path.join(auditDir, "discovery-video-classification.csv"),
  `${[header, ...rows].map((row) => row.map(csvCell).join(",")).join("\n")}\n`,
);
const counts = Object.fromEntries(
  Object.entries(Object.groupBy(classified, (item) => item.classification))
    .map(([key, rowsForKey]) => [key, rowsForKey.length]),
);
await fs.writeFile(
  path.join(auditDir, "discovery-video-classification-summary.json"),
  `${JSON.stringify({ total_in_window_search_hits: classified.length, ...counts }, null, 2)}\n`,
);
process.stdout.write(`${JSON.stringify({ total: classified.length, ...counts })}\n`);
