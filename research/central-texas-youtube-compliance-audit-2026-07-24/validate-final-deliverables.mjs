#!/usr/bin/env node

/*
 * Offline integrity checks for the three user-facing audit deliverables.
 * This validates internal consistency only; it does not make legal judgments.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const projectDir = path.resolve(auditDir, "..", "..");
const reportsDir = path.join(projectDir, "reports");
const files = {
  coverageSummary: path.join(auditDir, "final-coverage-summary.json"),
  findingsSummary: path.join(auditDir, "final-findings-summary.json"),
  sourceCoverage: path.join(auditDir, "final-coverage-ledger.csv"),
  sourceFindings: path.join(auditDir, "final-findings.csv"),
  report: path.join(reportsDir, "central-texas-youtube-compliance-audit-2026-07-24.md"),
  coverage: path.join(reportsDir, "central-texas-youtube-compliance-coverage-2026-07-24.csv"),
  findings: path.join(reportsDir, "central-texas-youtube-compliance-findings-2026-07-24.csv"),
};
const excludedTaylorChannelIds = [
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
];

function fail(message) {
  throw new Error(`FINAL DELIVERABLE VALIDATION FAILED: ${message}`);
}

function parseCsv(text, label) {
  const rawRows = [];
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
    } else if (character === '"') {
      quoted = true;
    } else if (character === ",") {
      row.push(cell);
      cell = "";
    } else if (character === "\n") {
      row.push(cell);
      if (row.some((value) => value !== "")) rawRows.push(row);
      row = [];
      cell = "";
    } else if (character !== "\r") {
      cell += character;
    }
  }
  if (quoted) fail(`${label} has an unterminated quoted field`);
  if (cell || row.length) {
    row.push(cell);
    if (row.some((value) => value !== "")) rawRows.push(row);
  }
  if (!rawRows.length) fail(`${label} is empty`);
  const headers = rawRows.shift();
  if (headers.some((header) => !header) || new Set(headers).size !== headers.length) {
    fail(`${label} has blank or duplicate headers`);
  }
  return rawRows.map((values, rowIndex) => {
    if (values.length !== headers.length) {
      fail(`${label} row ${rowIndex + 2} has ${values.length} columns; expected ${headers.length}`);
    }
    return Object.fromEntries(headers.map((header, fieldIndex) => [header, values[fieldIndex]]));
  });
}

const [
  coverageSummaryText,
  findingsSummaryText,
  sourceCoverage,
  sourceFindings,
  report,
  deliveredCoverage,
  deliveredFindings,
] = await Promise.all([
  fs.readFile(files.coverageSummary, "utf8"),
  fs.readFile(files.findingsSummary, "utf8"),
  fs.readFile(files.sourceCoverage, "utf8"),
  fs.readFile(files.sourceFindings, "utf8"),
  fs.readFile(files.report, "utf8"),
  fs.readFile(files.coverage, "utf8"),
  fs.readFile(files.findings, "utf8"),
]);

const coverageSummary = JSON.parse(coverageSummaryText);
const findingsSummary = JSON.parse(findingsSummaryText);
const coverageRows = parseCsv(deliveredCoverage, path.basename(files.coverage));
const findingRows = parseCsv(deliveredFindings, path.basename(files.findings));

if (sourceCoverage !== deliveredCoverage) fail("delivered coverage CSV differs from the validated source ledger");
if (sourceFindings !== deliveredFindings) fail("delivered findings CSV differs from the validated source findings");

const coverageIds = coverageRows.map((row) => row.channel_id);
if (new Set(coverageIds).size !== coverageIds.length) fail("coverage CSV has duplicate channel IDs");
if (coverageIds.length !== coverageSummary.totals.channels) {
  fail(`coverage row count ${coverageIds.length} disagrees with summary ${coverageSummary.totals.channels}`);
}
if (coverageSummary.validation?.expected_scoped_channel_ids !== coverageSummary.totals.channels) {
  fail("coverage summary expected-scope total disagrees with final channel total");
}

const coverageTotals = coverageRows.reduce((aggregate, row) => ({
  uploads: aggregate.uploads + Number(row.total_in_window_public_uploads_cataloged),
  captions: aggregate.captions + Number(row.uploads_with_caption_files),
  withoutCaptions: aggregate.withoutCaptions + Number(row.uploads_without_caption_files),
}), { uploads: 0, captions: 0, withoutCaptions: 0 });
if (
  coverageTotals.uploads !== coverageSummary.totals.total_in_window_public_uploads_cataloged
  || coverageTotals.captions !== coverageSummary.totals.uploads_with_caption_files
  || coverageTotals.withoutCaptions !== coverageSummary.totals.uploads_without_caption_files
) {
  fail("coverage CSV totals disagree with the coverage summary");
}

const findingIds = findingRows.map((row) => row.finding_id);
if (new Set(findingIds).size !== findingIds.length) fail("findings CSV has duplicate finding IDs");
if (findingRows.length !== findingsSummary.total_finding_groups) {
  fail(`findings row count ${findingRows.length} disagrees with summary ${findingsSummary.total_finding_groups}`);
}
const allowedPriorities = ["high", "medium", "low", "verification_only", "resolved"];
const deliveredPriorityCounts = Object.fromEntries(
  allowedPriorities.map((priority) => [
    priority,
    findingRows.filter((row) => row.adjudicated_priority === priority).length,
  ]),
);
for (const priority of allowedPriorities) {
  if (deliveredPriorityCounts[priority] !== Number(findingsSummary.priority_counts?.[priority])) {
    fail(`findings priority count disagrees for ${priority}`);
  }
}
if (
  findingsSummary.validation?.positional_video_id_url_date_checks_passed !== true
  || Number(findingsSummary.validation?.unused_manual_eligibility_records) !== 0
) {
  fail("findings summary does not attest to complete public-eligibility and positional validation");
}

const deliveredVideoIds = new Set();
for (const row of findingRows) {
  const evidenceIds = row.video_id.split(";").map((value) => value.trim()).filter(Boolean);
  const evidenceUrls = row.video_url.split(";").map((value) => value.trim()).filter(Boolean);
  if (evidenceIds.length !== evidenceUrls.length) {
    fail(`finding ${row.finding_id} has mismatched evidence ID/URL counts`);
  }
  const videoIds = [];
  for (const [index, evidenceId] of evidenceIds.entries()) {
    if (!/^[A-Za-z0-9_-]{11}$/.test(evidenceId) && !/^UC[A-Za-z0-9_-]{20,}$/.test(evidenceId)) {
      fail(`finding ${row.finding_id} has malformed evidence ID ${evidenceId}`);
    }
    if (!/^https:\/\/www\.youtube\.com\//.test(evidenceUrls[index])) {
      fail(`finding ${row.finding_id} has a non-YouTube evidence URL`);
    }
    if (/^[A-Za-z0-9_-]{11}$/.test(evidenceId)) {
      if (evidenceUrls[index] !== `https://www.youtube.com/watch?v=${evidenceId}`) {
        fail(`finding ${row.finding_id} has a non-positional video ID/URL mapping`);
      }
      deliveredVideoIds.add(evidenceId);
      videoIds.push(evidenceId);
    }
  }
  const dateTokens = [...row.date.matchAll(/\d{4}-\d{2}-\d{2}/g)].map((match) => match[0]);
  if (dateTokens.length < videoIds.length) {
    fail(`finding ${row.finding_id} has fewer explicit dates than cited videos`);
  }
  for (const date of dateTokens.slice(0, videoIds.length)) {
    if (date < "2024-07-24" || date > "2026-07-24") {
      fail(`finding ${row.finding_id} has an out-of-window cited-video date ${date}`);
    }
  }
}
if (deliveredVideoIds.size !== Number(findingsSummary.validation?.cited_video_ids_verified_public_and_in_window)) {
  fail("delivered unique video-ID count disagrees with public-eligibility validation summary");
}

for (const channelId of excludedTaylorChannelIds) {
  if (deliveredCoverage.includes(channelId)) fail(`coverage CSV contains excluded Taylor channel ${channelId}`);
  if (deliveredFindings.includes(channelId)) fail(`findings CSV contains excluded Taylor channel ${channelId}`);
}

if (/\{\{[^}]+\}\}|(?:^|\W)(?:TODO|INTERIM)(?:\W|$)/i.test(report)) {
  fail("report contains an unresolved replacement token or draft marker");
}
for (const forbidden of ["violation confirmed", "committed a violation", "illegal conduct established"]) {
  if (report.toLowerCase().includes(forbidden)) fail(`report contains forbidden conclusory phrase: ${forbidden}`);
}

const expectedReportStrings = [
  `| Scoped channel identities | ${Number(coverageSummary.totals.channels).toLocaleString("en-US")} |`,
  `| In-window upload count | ${Number(coverageSummary.totals.total_in_window_public_uploads_cataloged).toLocaleString("en-US")} |`,
  `| Uploads with an available caption artifact | ${Number(coverageSummary.totals.uploads_with_caption_files).toLocaleString("en-US")} |`,
  `${Number(findingsSummary.total_finding_groups).toLocaleString("en-US")} finding groups:`,
];
for (const value of expectedReportStrings) {
  if (!report.includes(value)) fail(`report does not contain expected final count ${value}`);
}

const malformedVideoLinks = [...report.matchAll(/https:\/\/www\.youtube\.com\/watch\?v=([^\s)\];]+)/g)]
  .map((match) => match[1])
  .filter((videoId) => !/^[A-Za-z0-9_-]{11}$/.test(videoId));
if (malformedVideoLinks.length) fail(`report has malformed YouTube video IDs: ${malformedVideoLinks.join(", ")}`);

process.stderr.write(
  `Validated ${coverageRows.length} coverage rows, ${coverageTotals.uploads} uploads, `
  + `${coverageTotals.captions} caption-bearing records, and ${findingRows.length} finding groups.\n`,
);
