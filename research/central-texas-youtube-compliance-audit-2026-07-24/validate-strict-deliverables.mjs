#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const auditDir = path.dirname(fileURLToPath(import.meta.url));
const projectDir = path.resolve(auditDir, "..", "..");
const reportsDir = path.join(projectDir, "reports");

const files = {
  sourceFindings: path.join(auditDir, "final-findings.csv"),
  disposition: path.join(auditDir, "strict-disposition-ledger.csv"),
  summary: path.join(auditDir, "strict-findings-summary.json"),
  report: path.join(reportsDir, "central-texas-youtube-compliance-proven-violations-2026-07-24.md"),
  proven: path.join(reportsDir, "central-texas-youtube-compliance-proven-violations-2026-07-24.csv"),
  factual: path.join(reportsDir, "central-texas-youtube-compliance-confirmed-factual-corrections-2026-07-24.csv"),
};

const excludedTaylorChannelIds = [
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
];

function fail(message) {
  throw new Error(`STRICT DELIVERABLE VALIDATION FAILED: ${message}`);
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

  return {
    headers,
    rows: rawRows.map((values, rowIndex) => {
      if (values.length !== headers.length) {
        fail(`${label} row ${rowIndex + 2} has ${values.length} columns; expected ${headers.length}`);
      }
      return Object.fromEntries(headers.map((header, fieldIndex) => [header, values[fieldIndex]]));
    }),
  };
}

const [sourceText, dispositionText, summaryText, report, provenText, factualText] = await Promise.all([
  fs.readFile(files.sourceFindings, "utf8"),
  fs.readFile(files.disposition, "utf8"),
  fs.readFile(files.summary, "utf8"),
  fs.readFile(files.report, "utf8"),
  fs.readFile(files.proven, "utf8"),
  fs.readFile(files.factual, "utf8"),
]);

const source = parseCsv(sourceText, path.basename(files.sourceFindings));
const disposition = parseCsv(dispositionText, path.basename(files.disposition));
const proven = parseCsv(provenText, path.basename(files.proven));
const factual = parseCsv(factualText, path.basename(files.factual));
const summary = JSON.parse(summaryText);

if (source.rows.length !== 140) fail(`source has ${source.rows.length} rows; expected 140`);
if (disposition.rows.length !== 140) fail(`disposition has ${disposition.rows.length} rows; expected 140`);
if (proven.rows.length !== 0) fail(`proven-violations CSV has ${proven.rows.length} rows; expected 0`);
if (factual.rows.length !== 1) fail(`factual-corrections CSV has ${factual.rows.length} rows; expected 1`);
if (!factual.rows[0].classification.toLowerCase().includes("not a proven legal or regulatory violation")) {
  fail("factual correction lacks the required non-violation label");
}

const sourceIds = new Set(source.rows.map((row) => row.finding_id));
const dispositionIds = disposition.rows.map((row) => row.finding_id);
if (new Set(dispositionIds).size !== dispositionIds.length) fail("disposition ledger has duplicate IDs");
for (const id of sourceIds) {
  if (!dispositionIds.includes(id)) fail(`source finding ${id} is absent from strict disposition ledger`);
}

const counts = disposition.rows.reduce((result, row) => {
  result[row.strict_disposition] = (result[row.strict_disposition] ?? 0) + 1;
  if (row.published_as_proven_violation !== "no") {
    fail(`finding ${row.finding_id} was unexpectedly published as a proven violation`);
  }
  return result;
}, {});

const expected = {
  confirmed_factual_inaccuracy_not_a_proven_violation: 1,
  unresolved_missing_evidence_not_publishable_as_violation: 96,
  no_proven_violation: 43,
};
for (const [label, expectedCount] of Object.entries(expected)) {
  if (Number(counts[label] ?? 0) !== expectedCount) {
    fail(`${label} count ${counts[label] ?? 0}; expected ${expectedCount}`);
  }
}

if (summary.counts.adjudicated_or_objectively_established_violation !== 0) {
  fail("summary reports a nonzero proven-violation count");
}
if (summary.published_proven_violation_ids.length !== 0) {
  fail("summary contains a published proven-violation ID");
}
if (summary.confirmed_factual_correction_ids.join(",") !== "SH-02") {
  fail("summary factual-correction IDs are not exactly SH-02");
}

const requiredReportPhrases = [
  "No adjudicated or objectively established legal or regulatory violations were identified",
  "zero finding rows",
  "Confirmed factual correction — not a violation finding",
  "Relocators",
  "families preferred",
  "Personal NMLS2563024",
  "not legal advice",
];
for (const phrase of requiredReportPhrases) {
  if (!report.includes(phrase)) fail(`report is missing required phrase: ${phrase}`);
}
if (/\{\{[^}]+\}\}|(?:^|\W)(?:TODO|INTERIM)(?:\W|$)/i.test(report)) {
  fail("report contains a draft marker");
}

for (const channelId of excludedTaylorChannelIds) {
  for (const [label, text] of Object.entries({
    report,
    provenText,
    factualText,
    dispositionText,
  })) {
    if (text.includes(channelId)) fail(`${label} contains excluded Taylor channel ${channelId}`);
  }
}

process.stderr.write(
  "Validated strict deliverables: 140/140 groups classified, "
  + "0 proven violations, 1 factual correction, Taylor channels absent.\n",
);
