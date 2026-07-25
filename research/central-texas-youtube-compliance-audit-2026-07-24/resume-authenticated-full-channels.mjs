#!/usr/bin/env node

/*
 * Sequential, paced resumption for an approved full-channel URL manifest.
 *
 * The existing yt-dlp archive skips completed records. Each Videos/Shorts tab
 * is run separately so the expected first out-of-window item can stop that tab
 * without aborting the rest of the manifest. A status ledger makes rate-limit
 * or authentication failures explicit instead of silently treating them as
 * zero eligible uploads.
 */

import fs from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const args = process.argv.slice(2);
const manifestIndex = args.indexOf("--manifest");
if (manifestIndex < 0 || !args[manifestIndex + 1]) {
  throw new Error("Usage: resume-authenticated-full-channels.mjs --manifest <audit-relative manifest.txt>");
}

const manifestName = args[manifestIndex + 1];
if (!/^[A-Za-z0-9._-]+\.txt$/.test(manifestName)) {
  throw new Error(`Unsafe manifest name: ${manifestName}`);
}
const archiveIndex = args.indexOf("--archive");
const archiveName = archiveIndex >= 0 && args[archiveIndex + 1]
  ? args[archiveIndex + 1]
  : "authenticated-existing-video.archive";
if (!/^[A-Za-z0-9._-]+\.archive$/.test(archiveName)) {
  throw new Error(`Unsafe archive name: ${archiveName}`);
}

const manifestPath = path.join(auditDir, manifestName);
const archivePath = path.join(auditDir, archiveName);
const statusPath = path.join(auditDir, `${manifestName.replace(/\.txt$/, "")}-collection-status.tsv`);
const logPath = path.join(auditDir, `${manifestName.replace(/\.txt$/, "")}-collection.log`);
const outputTemplate = path.join(
  auditDir,
  "raw",
  "authenticated-root",
  "%(channel_id)s",
  "%(upload_date)s_%(id)s.%(ext)s",
);
const excludedTaylorChannelIds = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);
const completedStatuses = new Set(["complete", "cutoff_complete", "no_tab"]);
const statusHeaders = [
  "channel_id",
  "tab",
  "url",
  "status",
  "exit_code",
  "new_archive_ids",
  "completed_at",
];

function clean(value) {
  return value == null ? "" : String(value).replaceAll(/\s+/g, " ").trim();
}

function parseUrl(url) {
  const match = url.match(/^https:\/\/www\.youtube\.com\/channel\/(UC[A-Za-z0-9_-]{20,})\/(videos|shorts|streams)$/);
  if (!match) throw new Error(`Unsupported channel-tab URL in ${manifestName}: ${url}`);
  return { channelId: match[1], tab: match[2] };
}

function archiveCount(text) {
  return text.split(/\n/).filter(Boolean).length;
}

async function readArchiveCount() {
  try {
    return archiveCount(await fs.readFile(archivePath, "utf8"));
  } catch (error) {
    if (error?.code === "ENOENT") return 0;
    throw error;
  }
}

function runYtDlp(url) {
  const ytDlpArgs = [
    "--no-update",
    "--ignore-errors",
    "--ignore-no-formats-error",
    "--break-on-reject",
    "--dateafter", "20240723",
    "--datebefore", "20260725",
    "--skip-download",
    "--write-info-json",
    "--write-subs",
    "--write-auto-subs",
    "--sub-langs", "en",
    "--sub-format", "json3",
    "--download-archive", archivePath,
    "--force-write-archive",
    "--sleep-requests", "0.75",
    "--retry-sleep", "http:exp=1:10",
    "--no-overwrites",
    "--no-write-playlist-metafiles",
    "--quiet",
    "--no-warnings",
    "--output", outputTemplate,
    url,
  ];
  return new Promise((resolve) => {
    const child = spawn("yt-dlp", ytDlpArgs, {
      cwd: path.dirname(auditDir),
      stdio: ["ignore", "pipe", "pipe"],
    });
    let output = "";
    child.stdout.on("data", (chunk) => { output += chunk; });
    child.stderr.on("data", (chunk) => { output += chunk; });
    child.on("error", (error) => resolve({ exitCode: 127, output: `${output}\n${error.message}` }));
    child.on("close", (exitCode) => resolve({ exitCode: exitCode ?? 1, output }));
  });
}

const manifestText = await fs.readFile(manifestPath, "utf8");
const urls = [...new Set(manifestText.split(/\n/).map((line) => line.trim()).filter(Boolean))];
if (!urls.length) throw new Error(`${manifestName} contains no URLs`);

const priorRows = new Map();
try {
  const statusText = await fs.readFile(statusPath, "utf8");
  for (const line of statusText.split(/\n/).slice(1).filter(Boolean)) {
    const fields = line.split("\t");
    if (fields.length !== statusHeaders.length) continue;
    const row = Object.fromEntries(statusHeaders.map((header, index) => [header, fields[index]]));
    priorRows.set(row.url, row);
  }
} catch (error) {
  if (error?.code !== "ENOENT") throw error;
}

const rows = [];
let shouldStop = false;
for (const url of urls) {
  const { channelId, tab } = parseUrl(url);
  if (excludedTaylorChannelIds.has(channelId)) {
    throw new Error(`Excluded Taylor channel survived manifest validation: ${channelId}`);
  }
  const prior = priorRows.get(url);
  if (prior && completedStatuses.has(prior.status)) {
    rows.push(prior);
    continue;
  }

  const before = await readArchiveCount();
  const result = await runYtDlp(url);
  const after = await readArchiveCount();
  const normalizedOutput = clean(result.output);
  let status = "error";
  if (/rate-limited|too many requests|HTTP Error 429/i.test(normalizedOutput)) {
    status = "rate_limited";
    shouldStop = true;
  } else if (/sign in to confirm|LOGIN_REQUIRED|cookies are no longer valid/i.test(normalizedOutput)) {
    status = "authentication_blocked";
  } else if (/does not have a (?:shorts|streams|live) tab/i.test(normalizedOutput)) {
    status = "no_tab";
  } else if (
    result.exitCode === 101
    || /did not match filter|break-match-filter|not in range/i.test(normalizedOutput)
  ) {
    status = "cutoff_complete";
  } else if (result.exitCode === 0) {
    status = "complete";
  } else if (/video unavailable|private video|members-only|removed by the uploader/i.test(normalizedOutput)) {
    status = "error_with_unavailable_items";
  }

  const row = {
    channel_id: channelId,
    tab,
    url,
    status,
    exit_code: result.exitCode,
    new_archive_ids: Math.max(0, after - before),
    completed_at: new Date().toISOString(),
  };
  rows.push(row);
  priorRows.set(url, row);
  await fs.appendFile(
    logPath,
    `\n===== ${row.completed_at} ${url} status=${status} exit=${result.exitCode} new=${row.new_archive_ids} =====\n${result.output}`,
  );
  process.stderr.write(`${channelId}/${tab}: ${status}; ${row.new_archive_ids} new records\n`);
  if (shouldStop) break;
}

for (const [url, prior] of priorRows) {
  if (!rows.some((row) => row.url === url)) rows.push(prior);
}
rows.sort((left, right) => urls.indexOf(left.url) - urls.indexOf(right.url));
const tsv = [
  statusHeaders.join("\t"),
  ...rows.map((row) => statusHeaders.map((header) => String(row[header] ?? "").replaceAll(/[\t\r\n]+/g, " ")).join("\t")),
].join("\n");
await fs.writeFile(statusPath, `${tsv}\n`);

const counts = {};
for (const row of rows) counts[row.status] = (counts[row.status] ?? 0) + 1;
process.stderr.write(`${manifestName}: ${JSON.stringify(counts)}\n`);
if (shouldStop) process.exitCode = 75;
