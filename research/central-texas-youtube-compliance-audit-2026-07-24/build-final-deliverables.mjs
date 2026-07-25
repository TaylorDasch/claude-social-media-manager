#!/usr/bin/env node

/*
 * Renders the final Markdown report from the reconciled draft and copies the
 * two validated CSV ledgers into the project reports directory.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const projectDir = path.resolve(auditDir, "..", "..");
const reportsDir = path.join(projectDir, "reports");
const inputs = {
  draft: path.join(auditDir, "final-report-reconciled-draft.md"),
  coverageSummary: path.join(auditDir, "final-coverage-summary.json"),
  findingsSummary: path.join(auditDir, "final-findings-summary.json"),
  coverageCsv: path.join(auditDir, "final-coverage-ledger.csv"),
  findingsCsv: path.join(auditDir, "final-findings.csv"),
};
const outputs = {
  report: path.join(reportsDir, "central-texas-youtube-compliance-audit-2026-07-24.md"),
  coverageCsv: path.join(reportsDir, "central-texas-youtube-compliance-coverage-2026-07-24.csv"),
  findingsCsv: path.join(reportsDir, "central-texas-youtube-compliance-findings-2026-07-24.csv"),
};

function fail(message) {
  throw new Error(`FINAL DELIVERABLE BUILD FAILED: ${message}`);
}

function formatCount(value, label) {
  const number = Number(value);
  if (!Number.isInteger(number) || number < 0) fail(`${label} is not a non-negative integer`);
  return number.toLocaleString("en-US");
}

const [draft, coverageSummaryText, findingsSummaryText] = await Promise.all([
  fs.readFile(inputs.draft, "utf8"),
  fs.readFile(inputs.coverageSummary, "utf8"),
  fs.readFile(inputs.findingsSummary, "utf8"),
]);
const coverage = JSON.parse(coverageSummaryText);
const findings = JSON.parse(findingsSummaryText);

const priorities = ["high", "medium", "low", "verification_only", "resolved"];
const priorityCounts = Object.fromEntries(priorities.map((priority) => {
  const count = Number(findings.priority_counts?.[priority]);
  if (!Number.isInteger(count) || count < 0) fail(`invalid findings priority count for ${priority}`);
  return [priority, count];
}));
const priorityTotal = Object.values(priorityCounts).reduce((sum, count) => sum + count, 0);
if (priorityTotal !== Number(findings.total_finding_groups)) {
  fail(`priority counts sum to ${priorityTotal}, not ${findings.total_finding_groups}`);
}
if (Number(coverage.validation?.expected_scoped_channel_ids) !== Number(coverage.totals?.channels)) {
  fail("coverage expected-scope count disagrees with final channel total");
}

const findingCountPhrase = [
  `${formatCount(findings.total_finding_groups, "total finding groups")} finding groups:`,
  `${formatCount(priorityCounts.high, "high findings")} high,`,
  `${formatCount(priorityCounts.medium, "medium findings")} medium,`,
  `${formatCount(priorityCounts.low, "low findings")} low,`,
  `${formatCount(priorityCounts.verification_only, "verification findings")} verification-only,`,
  `and ${formatCount(priorityCounts.resolved, "resolved findings")} resolved`,
].join(" ");

const replacements = new Map([
  ["{{FINAL_CHANNELS}}", formatCount(coverage.totals?.channels, "coverage channels")],
  ["{{FINAL_UPLOADS}}", formatCount(coverage.totals?.total_in_window_public_uploads_cataloged, "coverage uploads")],
  ["{{FINAL_CAPTIONS}}", formatCount(coverage.totals?.uploads_with_caption_files, "coverage captions")],
  ["{{FINAL_FINDINGS_COUNTS}}", findingCountPhrase],
]);

let report = draft;
for (const [token, value] of replacements) {
  if (!report.includes(token)) fail(`draft is missing token ${token}`);
  report = report.replaceAll(token, value);
}
if (/\{\{[^}]+\}\}|(?:^|\W)(?:TODO|INTERIM)(?:\W|$)/i.test(report)) {
  fail("rendered report still contains a replacement token or draft marker");
}

await fs.mkdir(reportsDir, { recursive: true });
await Promise.all([
  fs.writeFile(outputs.report, report),
  fs.copyFile(inputs.coverageCsv, outputs.coverageCsv),
  fs.copyFile(inputs.findingsCsv, outputs.findingsCsv),
]);

process.stderr.write(
  `Built report and CSV deliverables: ${coverage.totals.channels} channels, `
  + `${coverage.totals.total_in_window_public_uploads_cataloged} uploads, `
  + `${findings.total_finding_groups} finding groups.\n`,
);
