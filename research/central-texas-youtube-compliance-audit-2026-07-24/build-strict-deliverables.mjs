#!/usr/bin/env node

/*
 * Converts the issue-spotting ledger into a strict, proven-violations-only
 * publication set. The broader audit remains preserved as an internal
 * remediation/verification workpaper.
 */

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const auditDir = path.dirname(fileURLToPath(import.meta.url));
const projectDir = path.resolve(auditDir, "..", "..");
const reportsDir = path.join(projectDir, "reports");

const inputs = {
  findings: path.join(auditDir, "final-findings.csv"),
  findingsSummary: path.join(auditDir, "final-findings-summary.json"),
  coverageSummary: path.join(auditDir, "final-coverage-summary.json"),
};

const outputs = {
  report: path.join(reportsDir, "central-texas-youtube-compliance-proven-violations-2026-07-24.md"),
  provenCsv: path.join(reportsDir, "central-texas-youtube-compliance-proven-violations-2026-07-24.csv"),
  factualCsv: path.join(reportsDir, "central-texas-youtube-compliance-confirmed-factual-corrections-2026-07-24.csv"),
  dispositionCsv: path.join(auditDir, "strict-disposition-ledger.csv"),
  summaryJson: path.join(auditDir, "strict-findings-summary.json"),
};

const excludedTaylorChannelIds = [
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
];

const buckets = {
  unresolved_financial_mortgage_or_substantiation: [
    "BG-01", "C-04", "S-AUTH-02", "PF-11", "PF-03", "D-AUTH-03", "GDI-03", "J-02",
    "RL-02", "RL-01", "ROOTB-R-07", "ROOTB-R-09", "D-AUTH-04", "ROOT-AUTH-04", "SH-01",
    "LB-21", "LB-20", "LB-16", "LB-15", "DL-05", "ROOTA-R-01", "D-AUTH-07", "C-02",
    "C-03", "ROOTB-C21-01", "ROOT-AUTH-07", "BPM-06", "ROOTA-H-05", "ROOTA-H-04",
    "ROOTA-H-06", "D-AUTH-08", "J-01", "STREAMS-INC-01", "ROOTB-R-06", "BPM-08",
    "LB-01", "LB-08", "LB-09", "ROOTB-W-02", "ROOTB-R-08", "P-01", "ROOTB-RHEA-01",
    "RL-03", "ROOTA-SS-10", "ROOT-AUTH-06", "ROOTA-H-01", "ROOTA-H-02", "S-AUTH-04",
    "SH-05", "SH-03", "S-AUTH-03", "ROOT-AUTH-05", "ROOTA-SS-02", "ROOTA-SS-03",
    "ROOTA-SS-04", "ROOTA-SS-07", "ROOTA-SS-06", "ROOTA-SS-05", "D-AUTH-06", "LB-17",
    "GDI-04", "BPM-07", "V-01", "LB-03",
  ],
  unresolved_school_crime_steering_or_demographic_context: [
    "A-11", "A-10", "PF-09", "ROOTA-H-03", "LB-14", "LB-07", "LB-05", "SH-04",
    "LB-18", "D-AUTH-09", "BG-02", "PF-10", "PF-04", "PF-02", "LB-11", "LB-13",
    "LB-12", "LB-04", "LB-06", "ROOTB-SH-01", "ROOTA-SS-09", "LB-19",
  ],
  unresolved_disclosure_or_status_path: [
    "LB-10", "PF-08", "PF-06", "BPM-05", "PF-12", "DL-04", "DL-01", "RL-04", "DL-02",
    "DL-06",
  ],
  no_proven_violation_family_age_or_military_wording: [
    "GAP-AUTH-01", "A-12", "A-07", "A-01", "A-04", "A-02", "A-03", "A-05", "BG-03",
    "PF-05", "BPM-01", "ROOT-AUTH-01", "S-AUTH-01", "BPM-02", "BPM-03", "ROOT-AUTH-02",
    "GDI-01", "ROOTB-R-02", "PF-01", "D-AUTH-02", "LB-02", "PF-07", "ROOTB-W-01",
    "ROOTB-R-04", "ROOTB-R-01", "ROOTB-R-03", "ROOTA-SS-08", "ROOT-AUTH-03",
    "ROOTA-SS-01", "D-AUTH-01", "GDI-02", "ROOTB-R-05", "A-09", "A-08", "A-06",
    "BPM-04", "DL-03",
  ],
  no_proven_violation_other: [
    "C-01", "J-03", "RL-05", "V-03", "V-02", "P-02",
  ],
  confirmed_factual_inaccuracy_not_violation: [
    "SH-02",
  ],
};

const basisByBucket = {
  unresolved_financial_mortgage_or_substantiation:
    "Excluded from the violations output: one or more required facts remain unproven, such as regulated role, complete final-ad context, source methodology, falsity, material terms, eligibility, compensation, or an applicable exception.",
  unresolved_school_crime_steering_or_demographic_context:
    "Excluded from the violations output: the public record does not prove discriminatory intent, differential treatment, protected-class tailoring, or another required steering/discrimination element.",
  unresolved_disclosure_or_status_path:
    "Excluded from the violations output: the full disclosure path, visual asset, direct-link destination, listing history, authorization, or date-matched status was not completely established.",
  no_proven_violation_family_age_or_military_wording:
    "No proven violation: the cited wording is not an express exclusion or limitation, and the complete context does not establish an unlawful protected-class preference. Relocation and military status are not treated as FHA protected classes.",
  no_proven_violation_other:
    "No proven violation: the public evidence is puffery, a resolved path, ordinary geographic information, or an item that never established a required legal element.",
  confirmed_factual_inaccuracy_not_violation:
    "Confirmed factual inaccuracy only: an official NMLS identity record conflicts with the public identifier attribution. No final enforcement disposition or complete proof of a separate advertising-law violation was found.",
};

function fail(message) {
  throw new Error(`STRICT DELIVERABLE BUILD FAILED: ${message}`);
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

function csvCell(value) {
  return `"${String(value ?? "").replaceAll('"', '""')}"`;
}

function renderCsv(headers, rows) {
  return [
    headers.map(csvCell).join(","),
    ...rows.map((row) => headers.map((header) => csvCell(row[header])).join(",")),
    "",
  ].join("\n");
}

const [findingsText, findingsSummaryText, coverageSummaryText] = await Promise.all([
  fs.readFile(inputs.findings, "utf8"),
  fs.readFile(inputs.findingsSummary, "utf8"),
  fs.readFile(inputs.coverageSummary, "utf8"),
]);

const findings = parseCsv(findingsText, path.basename(inputs.findings));
const findingsSummary = JSON.parse(findingsSummaryText);
const coverageSummary = JSON.parse(coverageSummaryText);

if (findings.length !== 140 || Number(findingsSummary.total_finding_groups) !== 140) {
  fail(`expected 140 source groups; found ${findings.length}`);
}

const sourceById = new Map(findings.map((row) => [row.finding_id, row]));
if (sourceById.size !== findings.length) fail("source findings contain duplicate IDs");

const bucketById = new Map();
for (const [bucket, ids] of Object.entries(buckets)) {
  for (const id of ids) {
    if (bucketById.has(id)) fail(`finding ${id} appears in more than one strict bucket`);
    bucketById.set(id, bucket);
  }
}

const sourceIds = new Set(sourceById.keys());
const missingFromBuckets = [...sourceIds].filter((id) => !bucketById.has(id));
const unknownBucketIds = [...bucketById.keys()].filter((id) => !sourceIds.has(id));
if (missingFromBuckets.length) fail(`unclassified source IDs: ${missingFromBuckets.join(", ")}`);
if (unknownBucketIds.length) fail(`bucket IDs absent from source: ${unknownBucketIds.join(", ")}`);

const strictDispositionFor = (bucket) => {
  if (bucket === "confirmed_factual_inaccuracy_not_violation") {
    return "confirmed_factual_inaccuracy_not_a_proven_violation";
  }
  if (bucket.startsWith("no_proven_violation")) return "no_proven_violation";
  return "unresolved_missing_evidence_not_publishable_as_violation";
};

const dispositionRows = findings
  .map((row) => {
    const bucket = bucketById.get(row.finding_id);
    return {
      finding_id: row.finding_id,
      creator_or_channel: row.creator_or_channel,
      video_url: row.video_url,
      original_adjudicated_priority: row.adjudicated_priority,
      strict_bucket: bucket,
      strict_disposition: strictDispositionFor(bucket),
      strict_basis: basisByBucket[bucket],
      published_as_proven_violation: "no",
    };
  })
  .sort((left, right) => left.finding_id.localeCompare(right.finding_id));

const dispositionCounts = dispositionRows.reduce((counts, row) => {
  counts[row.strict_disposition] = (counts[row.strict_disposition] ?? 0) + 1;
  return counts;
}, {});

const expectedCounts = {
  adjudicated_or_objectively_established_violation: 0,
  confirmed_factual_inaccuracy_not_a_proven_violation: 1,
  unresolved_missing_evidence_not_publishable_as_violation: 96,
  no_proven_violation: 43,
};

for (const [label, expected] of Object.entries(expectedCounts)) {
  const actual = label === "adjudicated_or_objectively_established_violation"
    ? 0
    : Number(dispositionCounts[label] ?? 0);
  if (actual !== expected) fail(`${label} count ${actual}; expected ${expected}`);
}

for (const channelId of excludedTaylorChannelIds) {
  if (findingsText.includes(channelId)) fail(`source findings contain excluded Taylor channel ${channelId}`);
}

const provenHeaders = [
  "strict_finding_id",
  "disposition",
  "creator_or_channel",
  "publication_date",
  "asset_url",
  "evidence",
  "violated_law_or_rule",
  "official_final_disposition_url",
  "proof_basis",
];
const provenRows = [];

const sh02 = sourceById.get("SH-02");
if (!sh02) fail("SH-02 source row is missing");

const factualHeaders = [
  "correction_id",
  "classification",
  "creator_or_channel",
  "dates",
  "video_urls",
  "confirmed_public_error",
  "official_record",
  "why_not_in_violations_file",
  "verification_date",
];
const factualRows = [{
  correction_id: "FC-01",
  classification: "Confirmed factual inaccuracy — not a proven legal or regulatory violation",
  creator_or_channel: sh02.creator_or_channel,
  dates: sh02.date,
  video_urls: sh02.video_url,
  confirmed_public_error:
    "The cited public YouTube descriptions attribute NMLS ID 2453024 to Stephen Harris. The September 20, 2024 description later also lists Personal NMLS 2563024.",
  official_record:
    "NMLS Consumer Access identifies 2453024 as Emma A. Krivak and 2563024 as Stephen Jerrell Harris.",
  why_not_in_violations_file:
    "No final agency/court disposition was found, and the retained evidence does not prove every element and exception of a separate advertising-law violation. In the September 20, 2024 description, the correct personal ID also appears later in the same asset.",
  verification_date: "2026-07-24",
}];

const report = `# Central Texas YouTube proven-violations report

**Report date:** July 24, 2026  
**Review window:** July 24, 2024 through July 24, 2026, inclusive  
**Scope:** ${Number(coverageSummary.totals.channels).toLocaleString("en-US")} scoped public YouTube channel identities, ${Number(coverageSummary.totals.total_in_window_public_uploads_cataloged).toLocaleString("en-US")} recovered in-window public uploads, and ${Number(findingsSummary.total_finding_groups).toLocaleString("en-US")} previously identified issue-spotting groups. Taylor's two identified channels remained excluded.

## Result

**No adjudicated or objectively established legal or regulatory violations were identified from the public evidence reviewed.**

The proven-violations CSV therefore contains its schema and **zero finding rows**. This does not certify that every reviewed asset was compliant. It means the available public evidence did not meet the deliberately strict proof threshold below.

| Strict disposition | Groups |
|---|---:|
| Adjudicated violation | 0 |
| Objectively established rule/statutory violation | 0 |
| Confirmed factual inaccuracy, reported separately | 1 |
| Unresolved because a material legal or factual element is missing | 96 |
| No proven violation on the cited public evidence | 43 |
| **Total re-adjudicated** | **140** |

## Strict publication standard

A matter is published as a violation only if one of these tests is satisfied:

1. **Adjudicated violation:** a final court judgment, final agency order, or consent order identifies the respondent, conduct, and violated law or rule; or
2. **Objectively established violation:** complete, authenticated, date-matched evidence proves every element of an applicable self-executing requirement and eliminates every material exception or alternative compliance path.

The second test requires the rule to have been effective on the relevant date; the actor's regulated role and status to be confirmed; the complete final asset and permitted disclosure path to be reviewed; and no unresolved issue concerning context, materiality, falsity, compensation, eligibility, intent, or an exception. Automatic captions alone do not satisfy it.

Anything less is excluded from the proven-violations CSV. The broader 140-row ledger remains an internal issue-spotting and remediation workpaper, not a violations list.

## Confirmed factual correction — not a violation finding

The only item that survives as a verified factual correction is the NMLS attribution in finding group \`SH-02\`:

- Public descriptions for [You Won't Believe What $340K Buys in Belton, TX!](https://www.youtube.com/watch?v=-CpNohOpgaw), [Texas Home Sales CRASH 20%](https://www.youtube.com/watch?v=18WLFA46NT4), and [Mortgage Payment Went From $2500 to $7500 A MONTH](https://www.youtube.com/watch?v=z7GOddPjiio) display \`NMLS 2453024\` with Stephen Harris's identity.
- Official NMLS Consumer Access identifies [2453024](https://www.nmlsconsumeraccess.org/EntityDetails.aspx/INDIVIDUAL/2453024) as **Emma A. Krivak** and [2563024](https://www.nmlsconsumeraccess.org/EntityDetails.aspx/INDIVIDUAL/2563024) as **Stephen Jerrell Harris**.
- The September 20, 2024 viral video's same description later states \`Personal NMLS2563024\` and \`Company NMLS3029\`. It therefore contains both an incorrect attribution and Stephen's correct personal identifier.

The incorrect attribution is proven as a factual matter. It is **not published as a proven legal violation** because no final enforcement disposition was found and the record does not eliminate every remaining question about the governing advertisement rule, covered communication, responsible actor, complete asset, and applicable exception. The correct identifier's later appearance in the 2024 description also prevents treating that asset as a simple proven omission of the personal identifier.

Stephen's current NMLS status is not used retroactively. The official record reviewed on July 24, 2026 showed Approved–Inactive effective July 22, 2026, but that does not prove that a September 2024 publication was unlawful, and a legacy video's continued availability alone does not prove present unlicensed origination activity.

## Items removed from the violations output

- **“Family,” “family-friendly,” children, military-family, and relocator wording:** none of the cited items proves an express protected-class exclusion or limitation such as “no children,” “adults only,” or “families preferred.” “Relocators” is not a Fair Housing protected class. These phrases may still be edited as conservative copy practice, but they are not violation findings here.
- **Rates, APR, down payments, incentives, rebates, rankings, performance, ROI, valuation, schools, crime, safety, and listing status:** the retained evidence lacks at least one required fact such as the complete final asset, regulated role, terms, source methodology, falsity, materiality, authorization, or an applicable exception.
- **Broker, CPN, IABS, affiliate, RESPA, and referral items:** the complete permitted disclosure path or the necessary relationship, compensation, referral, and transaction elements were not proven.

## Primary authorities used for the strict screen

- [Fair Housing Act, 42 U.S.C. §3604(c)](https://uscode.house.gov/view.xhtml?req=%28title%3A42+section%3A3604%28c%29+edition%3Aprelim%29)
- [Texas Property Code Chapter 301](https://statutes.capitol.texas.gov/docs/PR/pdf/PR.301.pdf)
- [TREC Rules, including §535.155](https://www.trec.texas.gov/node/634)
- [Texas Finance Code §180.151](https://statutes.capitol.texas.gov/Docs/FI/pdf/FI.180.pdf)
- [Texas Department of Savings and Mortgage Lending advertising FAQ](https://www.sml.texas.gov/mortgage-origination/faqs/)
- [CFPB Regulation Z §1026.24](https://www.consumerfinance.gov/rules-policy/regulations/1026/2026-04-08/24/)
- [CFPB RESPA §8 FAQs](https://www.consumerfinance.gov/compliance/compliance-resources/mortgage-resources/real-estate-settlement-procedures-act/real-estate-settlement-procedures-act-faqs/)
- [FTC Disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)

## Limit

This is a public-evidence review, not legal advice, an agency determination, or a compliance certification. A zero-row proven-violations file means no item met this report's proof standard; it does not prove that unseen frames, deleted content, private communications, transaction records, or regulator-held evidence contain no issue.
`;

const summary = {
  schema_version: 1,
  generated_at: new Date().toISOString(),
  source_finding_groups: findings.length,
  strict_standard:
    "Final official disposition, or complete authenticated date-matched evidence proving every element of an applicable self-executing requirement and eliminating material exceptions.",
  counts: expectedCounts,
  published_proven_violation_ids: [],
  confirmed_factual_correction_ids: ["SH-02"],
  taylor_channel_ids_excluded: true,
  source_ledger_preserved: true,
};

await fs.mkdir(reportsDir, { recursive: true });
await Promise.all([
  fs.writeFile(outputs.report, report),
  fs.writeFile(outputs.provenCsv, renderCsv(provenHeaders, provenRows)),
  fs.writeFile(outputs.factualCsv, renderCsv(factualHeaders, factualRows)),
  fs.writeFile(
    outputs.dispositionCsv,
    renderCsv([
      "finding_id",
      "creator_or_channel",
      "video_url",
      "original_adjudicated_priority",
      "strict_bucket",
      "strict_disposition",
      "strict_basis",
      "published_as_proven_violation",
    ], dispositionRows),
  ),
  fs.writeFile(outputs.summaryJson, `${JSON.stringify(summary, null, 2)}\n`),
]);

process.stderr.write(
  `Built strict deliverables: ${findings.length} groups re-adjudicated; `
  + "0 proven violations; 1 confirmed factual correction; "
  + "96 unresolved; 43 no-proven-violation.\n",
);
