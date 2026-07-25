#!/usr/bin/env node

/*
 * Builds the user-facing adjudicated findings CSV from the normalized master
 * and any supplemental authenticated review CSVs in this audit directory.
 * This is an offline transform; it does not retrieve or reclassify evidence.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const masterName = "master-findings-adjudicated.csv";
const outputName = "final-findings.csv";
const summaryName = "final-findings-summary.json";
const coverageSummaryName = "authenticated-coverage-summary.json";
const authenticatedCatalogName = "authenticated-video-catalog.json";
const manualEligibilityName = "manual-finding-video-eligibility.tsv";
const startDate = "2024-07-24";
const endDate = "2026-07-24";
const excludedTaylorChannelIds = [
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
];
const outputHeaders = [
  "source_report",
  "finding_id",
  "creator_or_channel",
  "date",
  "video_title",
  "video_url",
  "video_id",
  "evidence_excerpt",
  "timestamp",
  "category_or_rule",
  "severity",
  "confidence",
  "classification",
  "missing_context",
  "required_follow_up",
  "adjudicated_priority",
  "adjudicated_label",
  "final_report_treatment",
];

function fail(message) {
  throw new Error(`FINAL FINDINGS BUILD FAILED: ${message}`);
}

function clean(value) {
  return value == null ? "" : String(value).trim();
}

function csvCell(value) {
  return `"${String(value ?? "").replaceAll('"', '""')}"`;
}

function parseCsv(text, label) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    if (quoted) {
      if (character === '"' && text[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else if (character === '"') {
        quoted = false;
      } else {
        cell += character;
      }
      continue;
    }
    if (character === '"') {
      quoted = true;
    } else if (character === ",") {
      row.push(cell);
      cell = "";
    } else if (character === "\n") {
      row.push(cell);
      if (row.some((value) => value !== "")) rows.push(row);
      row = [];
      cell = "";
    } else if (character !== "\r") {
      cell += character;
    }
  }
  if (quoted) fail(`${label} has an unterminated quoted field`);
  if (cell || row.length) {
    row.push(cell);
    if (row.some((value) => value !== "")) rows.push(row);
  }
  if (!rows.length) fail(`${label} is empty`);
  const headers = rows.shift().map(clean);
  if (headers.some((header) => !header) || new Set(headers).size !== headers.length) {
    fail(`${label} has invalid or duplicate headers`);
  }
  return rows.map((values, index) => {
    if (values.length !== headers.length) {
      fail(`${label} row ${index + 2} has ${values.length} fields; expected ${headers.length}`);
    }
    return Object.fromEntries(headers.map((header, fieldIndex) => [header, values[fieldIndex]]));
  });
}

function parseTsv(text, label) {
  const lines = text
    .split(/\n/)
    .map((line) => line.replaceAll("\r", ""))
    .filter((line) => line.trim());
  if (!lines.length) fail(`${label} is empty`);
  const headers = lines.shift().split("\t").map(clean);
  if (headers.some((header) => !header) || new Set(headers).size !== headers.length) {
    fail(`${label} has invalid or duplicate headers`);
  }
  return lines.map((line, index) => {
    const values = line.split("\t");
    if (values.length !== headers.length) {
      fail(`${label} row ${index + 2} has ${values.length} fields; expected ${headers.length}`);
    }
    return Object.fromEntries(headers.map((header, fieldIndex) => [header, clean(values[fieldIndex])]));
  });
}

function requireHeaders(rows, headers, label) {
  if (!rows.length) fail(`${label} has no data rows`);
  const available = new Set(Object.keys(rows[0]));
  for (const header of headers) {
    if (!available.has(header)) fail(`${label} is missing ${header}`);
  }
}

function treatmentFor(priority) {
  if (priority === "high") {
    return "Include in high-priority broker/compliance review as an apparent concern; no violation or liability is determined.";
  }
  if (priority === "medium") {
    return "Include in medium-priority source, substantiation, consistency, or disclosure review; no violation is determined.";
  }
  if (priority === "low") {
    return "Retain as low-priority copy cleanup or verification; do not characterize as a legal violation.";
  }
  if (priority === "verification_only") {
    return "Retain only in the verification/limitations ledger; required legal or factual elements were not established.";
  }
  if (priority === "resolved") {
    return "List as resolved/not escalated and do not report as a current missing-disclosure concern.";
  }
  fail(`unsupported adjudicated priority ${JSON.stringify(priority)}`);
}

function normalisePriority(value) {
  const priority = clean(value).toLowerCase().replaceAll("-", "_").replaceAll(" ", "_");
  if (["high", "medium", "low", "verification_only", "resolved"].includes(priority)) return priority;
  fail(`unsupported supplemental priority ${JSON.stringify(value)}`);
}

const entries = await fs.readdir(auditDir, { withFileTypes: true });
const supplementalNames = entries
  .filter((entry) => entry.isFile() && /^supplemental-.*review\.csv$/.test(entry.name))
  .map((entry) => entry.name)
  .sort();

const nonPublicVideoIds = new Set();
try {
  const coverage = JSON.parse(
    await fs.readFile(path.join(auditDir, coverageSummaryName), "utf8"),
  );
  for (const item of coverage.non_public_files ?? []) {
    const videoId = clean(item?.id);
    if (/^[A-Za-z0-9_-]{11}$/.test(videoId)) nonPublicVideoIds.add(videoId);
  }
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}

const publicEligibleVideos = new Map();
function addEligibleVideo({ videoId, channelId, uploadDate, source }) {
  if (!/^[A-Za-z0-9_-]{11}$/.test(videoId)) fail(`${source} has invalid video ID ${videoId}`);
  if (!/^UC[A-Za-z0-9_-]{20,}$/.test(channelId)) fail(`${source} has invalid channel ID ${channelId}`);
  if (excludedTaylorChannelIds.includes(channelId)) fail(`${source} contains excluded Taylor channel ${channelId}`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(uploadDate) || uploadDate < startDate || uploadDate > endDate) {
    fail(`${source} has out-of-window or invalid date ${uploadDate} for ${videoId}`);
  }
  const existing = publicEligibleVideos.get(videoId);
  if (existing && (existing.channel_id !== channelId || existing.upload_date !== uploadDate)) {
    fail(`${source} conflicts with eligibility record for ${videoId}`);
  }
  publicEligibleVideos.set(videoId, {
    channel_id: channelId,
    upload_date: uploadDate,
    source,
  });
}

const authenticatedCatalog = JSON.parse(
  await fs.readFile(path.join(auditDir, authenticatedCatalogName), "utf8"),
);
if (!Array.isArray(authenticatedCatalog)) fail(`${authenticatedCatalogName} must be an array`);
for (const [index, item] of authenticatedCatalog.entries()) {
  addEligibleVideo({
    videoId: clean(item?.id),
    channelId: clean(item?.channel_id),
    uploadDate: clean(item?.upload_date),
    source: `${authenticatedCatalogName} row ${index + 1}`,
  });
}

const manualEligibilityRows = parseTsv(
  await fs.readFile(path.join(auditDir, manualEligibilityName), "utf8"),
  manualEligibilityName,
);
requireHeaders(
  manualEligibilityRows,
  ["video_id", "channel_id", "upload_date", "availability", "verification_source"],
  manualEligibilityName,
);
const manualEligibilityIds = new Set();
for (const [index, row] of manualEligibilityRows.entries()) {
  if (manualEligibilityIds.has(row.video_id)) fail(`${manualEligibilityName} duplicates ${row.video_id}`);
  manualEligibilityIds.add(row.video_id);
  if (clean(row.availability).toLowerCase() !== "public") {
    fail(`${manualEligibilityName} row ${index + 2} is not verified public`);
  }
  addEligibleVideo({
    videoId: clean(row.video_id),
    channelId: clean(row.channel_id),
    uploadDate: clean(row.upload_date),
    source: `${manualEligibilityName} row ${index + 2}`,
  });
}

const master = parseCsv(await fs.readFile(path.join(auditDir, masterName), "utf8"), masterName);
requireHeaders(master, outputHeaders, masterName);
const classificationCorrections = new Map([
  ...["A-01", "A-02", "A-03", "A-04", "A-05", "A-07", "A-12"].map((findingId) => [
    findingId,
    "Apparent familial-status wording; copy-remediation priority, not a Fair Housing or TREC violation finding.",
  ]),
  ...["A-10", "A-11", "PF-09", "LB-05"].map((findingId) => [
    findingId,
    "Apparent familial-status wording plus school-source/consistency review; not a Fair Housing or steering violation finding.",
  ]),
  ...["A-06", "A-08", "A-09"].map((findingId) => [
    findingId,
    "Military-family wording: optional copy-remediation review of the family-suitability phrase only; military status is not treated as an FHA/TREC protected class or discrimination finding.",
  ]),
  ...["BG-03", "PF-01", "PF-05", "LB-02"].map((findingId) => [
    findingId,
    "Mixed age-oriented and familial-status wording review; age-oriented terms are inclusive-copy only, with no age/HOPA conclusion. Any direct family/child phrase remains a copy-remediation concern, not a violation finding.",
  ]),
  [
    "LB-07",
    "Mixed age-oriented and familial-status wording review; age-oriented terms are inclusive-copy only, with no age/HOPA conclusion. Direct family/child language and investment-outcome wording remain copy/substantiation concerns, not violation findings.",
  ],
]);
for (const row of master) {
  if (classificationCorrections.has(row.finding_id)) {
    row.classification = classificationCorrections.get(row.finding_id);
  }
  if (row.finding_id === "SH-02") {
    row.date = "2025-07-23; 2025-05-06; 2024-09-20; current About";
  }
  if (row.finding_id === "SH-04") {
    row.date = "2026-04-19; 2025-12-19; 2025-01-25; 2026-02-21; 2026-02-14";
  }
}

const supplemental = [];
const supplementalHeaders = [
  "finding_id",
  "creator_or_channel",
  "date",
  "video_title",
  "video_url",
  "video_id",
  "timestamp_or_location",
  "evidence_excerpt",
  "topic",
  "priority",
  "classification",
  "material_caveat",
  "recommended_follow_up",
];
for (const name of supplementalNames) {
  const rows = parseCsv(await fs.readFile(path.join(auditDir, name), "utf8"), name);
  requireHeaders(rows, supplementalHeaders, name);
  for (const row of rows) {
    const priority = normalisePriority(row.priority);
    supplemental.push({
      source_report: name,
      finding_id: clean(row.finding_id),
      creator_or_channel: clean(row.creator_or_channel),
      date: clean(row.date),
      video_title: clean(row.video_title),
      video_url: clean(row.video_url),
      video_id: clean(row.video_id),
      evidence_excerpt: clean(row.evidence_excerpt),
      timestamp: clean(row.timestamp_or_location),
      category_or_rule: clean(row.topic),
      severity: priority === "high" ? "High" : priority === "medium" ? "Moderate" : "Low",
      confidence: "Authenticated public-text evidence; ultimate legal conclusion not determined",
      classification: clean(row.classification),
      missing_context: clean(row.material_caveat),
      required_follow_up: clean(row.recommended_follow_up),
      adjudicated_priority: priority,
      adjudicated_label: clean(row.topic),
      final_report_treatment: treatmentFor(priority),
    });
  }
}

const candidateRows = [...master, ...supplemental];
const excludedNonPublicFindingIds = [];
const rows = candidateRows.filter((row) => {
  const videoIds = clean(row.video_id).split(";").map(clean).filter(Boolean);
  if (!videoIds.some((videoId) => nonPublicVideoIds.has(videoId))) return true;
  excludedNonPublicFindingIds.push(clean(row.finding_id));
  return false;
});
const priorityOrder = new Map([
  ["high", 0],
  ["medium", 1],
  ["low", 2],
  ["verification_only", 3],
  ["resolved", 4],
]);
rows.sort((left, right) => (
  priorityOrder.get(clean(left.adjudicated_priority)) - priorityOrder.get(clean(right.adjudicated_priority))
  || clean(left.creator_or_channel).localeCompare(clean(right.creator_or_channel))
  || clean(left.date).localeCompare(clean(right.date))
  || clean(left.finding_id).localeCompare(clean(right.finding_id))
));
const ids = new Set();
const referencedPublicVideoIds = new Set();
for (const [index, row] of rows.entries()) {
  for (const header of outputHeaders) {
    if (!(header in row)) fail(`row ${index + 1} is missing ${header}`);
  }
  const findingId = clean(row.finding_id);
  if (!findingId) fail(`row ${index + 1} has no finding_id`);
  if (ids.has(findingId)) fail(`duplicate finding_id ${findingId}`);
  ids.add(findingId);
  const allText = outputHeaders.map((header) => clean(row[header])).join(" ");
  for (const excluded of excludedTaylorChannelIds) {
    if (allText.includes(excluded)) fail(`finding ${findingId} contains excluded Taylor channel ${excluded}`);
  }
  const idParts = clean(row.video_id).split(";").map(clean).filter(Boolean);
  const urlParts = clean(row.video_url).split(";").map(clean).filter(Boolean);
  if (idParts.length !== urlParts.length) {
    fail(`finding ${findingId} has ${idParts.length} evidence IDs but ${urlParts.length} evidence URLs`);
  }
  const referencedVideoIds = [];
  for (const [evidenceIndex, evidenceId] of idParts.entries()) {
    if (!/^[A-Za-z0-9_-]{11}$/.test(evidenceId) && !/^UC[A-Za-z0-9_-]{20,}$/.test(evidenceId)) {
      fail(`finding ${findingId} has invalid video/channel ID ${evidenceId}`);
    }
    const url = urlParts[evidenceIndex];
    if (!/^https:\/\/www\.youtube\.com\//.test(url)) {
      fail(`finding ${findingId} has non-YouTube evidence URL ${url}`);
    }
    if (/^[A-Za-z0-9_-]{11}$/.test(evidenceId)) {
      const expectedUrl = `https://www.youtube.com/watch?v=${evidenceId}`;
      if (url !== expectedUrl) {
        fail(`finding ${findingId} URL/ID position ${evidenceIndex + 1} is ${url} / ${evidenceId}`);
      }
      const eligibility = publicEligibleVideos.get(evidenceId);
      if (!eligibility) fail(`finding ${findingId} cites video ${evidenceId} without public in-window eligibility evidence`);
      referencedVideoIds.push(evidenceId);
      referencedPublicVideoIds.add(evidenceId);
    }
  }
  const dateTokens = [...clean(row.date).matchAll(/\d{4}-\d{2}-\d{2}/g)].map((match) => match[0]);
  if (dateTokens.length < referencedVideoIds.length) {
    fail(`finding ${findingId} has ${referencedVideoIds.length} video IDs but only ${dateTokens.length} explicit dates`);
  }
  for (const [videoIndex, videoId] of referencedVideoIds.entries()) {
    const expectedDate = publicEligibleVideos.get(videoId).upload_date;
    if (dateTokens[videoIndex] !== expectedDate) {
      fail(`finding ${findingId} date/video position ${videoIndex + 1} is ${dateTokens[videoIndex]} / ${videoId}; expected ${expectedDate}`);
    }
  }
  treatmentFor(clean(row.adjudicated_priority));
}
for (const videoId of manualEligibilityIds) {
  if (!referencedPublicVideoIds.has(videoId)) {
    fail(`${manualEligibilityName} contains unused eligibility record ${videoId}`);
  }
}

const csv = [
  outputHeaders.map(csvCell).join(","),
  ...rows.map((row) => outputHeaders.map((header) => csvCell(row[header])).join(",")),
].join("\n");
const roundTrip = parseCsv(`${csv}\n`, outputName);
if (roundTrip.length !== rows.length) fail("generated CSV failed row-count round trip");
requireHeaders(roundTrip, outputHeaders, outputName);

const priorityCounts = Object.fromEntries(
  ["high", "medium", "low", "verification_only", "resolved"]
    .map((priority) => [priority, rows.filter((row) => clean(row.adjudicated_priority) === priority).length]),
);
const summary = {
  schema_version: 1,
  generated_at: new Date().toISOString(),
  master_source: masterName,
  supplemental_sources: supplementalNames,
  public_video_eligibility_sources: [authenticatedCatalogName, manualEligibilityName],
  total_finding_groups: rows.length,
  priority_counts: priorityCounts,
  legal_conclusion: "Issue-spotting and broker/counsel review priorities only; no legal violation or liability is determined.",
  corrections_applied: {
    "SH-02": "Authenticated current title/description recheck; date vector corrected to the video-ID order.",
    "SH-04": "Authenticated metadata recheck; complete date vector corrected to the video-ID order.",
    classification_harmonization: [...classificationCorrections.keys()],
  },
  validation: {
    duplicate_finding_ids: 0,
    malformed_rows: 0,
    taylor_channel_ids_absent: true,
    cited_video_ids_verified_public_and_in_window: referencedPublicVideoIds.size,
    positional_video_id_url_date_checks_passed: true,
    unused_manual_eligibility_records: 0,
    excluded_non_public_finding_ids: excludedNonPublicFindingIds,
  },
};

await Promise.all([
  fs.writeFile(path.join(auditDir, outputName), `${csv}\n`),
  fs.writeFile(path.join(auditDir, summaryName), `${JSON.stringify(summary, null, 2)}\n`),
]);

process.stderr.write(`Final findings: ${rows.length} groups (${priorityCounts.high} high, ${priorityCounts.medium} medium).\n`);
