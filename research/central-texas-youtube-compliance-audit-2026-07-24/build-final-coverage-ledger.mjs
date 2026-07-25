#!/usr/bin/env node

/*
 * Offline final coverage ledger builder.
 *
 * Run this only after build-authenticated-catalog.mjs has completed. It reads
 * local artifacts only; it never invokes yt-dlp, a browser, or a credential
 * store. The ledger intentionally distinguishes a full-channel inventory from
 * a discovery video: discovery evidence is never silently promoted to a
 * complete channel pass.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const inputNames = {
  authenticatedCatalog: "authenticated-video-catalog.json",
  authenticatedSummary: "authenticated-coverage-summary.json",
  rootChannels: "root-full-catalog-channels.tsv",
  rootScope: "root-scope-adjudication.tsv",
  rootLocalInputs: "authenticated-root-local-channel-inputs.txt",
  rootDirectInputs: "authenticated-root-direct-video-inputs.txt",
  discoveryDirectInputs: "authenticated-credible-direct-caption-inputs.txt",
  rootLocalStatusA: "authenticated-root-local-shard-a-collection-status.tsv",
  rootLocalStatusB: "authenticated-root-local-shard-b-collection-status.tsv",
  gapFullInputs: "authenticated-gap-full-channel-inputs.txt",
  gapFullStatus: "authenticated-gap-full-channel-inputs-collection-status.tsv",
  streamInputs: "authenticated-full-channel-stream-inputs.txt",
  streamStatus: "authenticated-full-channel-stream-inputs-collection-status.tsv",
  discoveryTriage: "discovery-gap-triage.tsv",
  candidates: "candidate-channels.tsv",
  manualCoverage: "agent-findings-normalized-coverage.csv",
  discoveryAdjudication: "discovery-gap-adjudication.md",
};
const outputNames = {
  ledger: "final-coverage-ledger.csv",
  summary: "final-coverage-summary.json",
};
const excludedTaylorChannelIds = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);

const manualAudits = [
  {
    channel_id: "UC1SKo4gUtYWElAGwZSguqpA",
    channel_name: "Moving to Killeen Texas - Brina Gordon",
    total: 191,
    with_captions: 188,
    evidence_mode: "manual full-channel audit: metadata/descriptions and available English automatic-caption tracks",
    limitations: "Two standard videos lacked English auto captions; two Shorts lacked descriptions; visual layer was not completed.",
    source_report: "agent-findings-brina.md",
  },
  {
    channel_id: "UCqo6EaV9o6bFg4szBL8RYEw",
    channel_name: "Living in Central Texas - Aundrea Dudik",
    total: 62,
    with_captions: 62,
    evidence_mode: "manual full-channel audit: metadata/descriptions and available English automatic-caption tracks",
    limitations: "One same-day scheduled premiere was unavailable and not counted; text/caption review does not verify visuals.",
    source_report: "agent-findings-aundrea.md",
  },
  {
    channel_id: "UCwoQakQVf2m8hfitYnymb5w",
    channel_name: "Mallory Anthony",
    total: 53,
    with_captions: 48,
    evidence_mode: "manual full-channel audit: available English caption tracks",
    limitations: "Five uploads without captions remain in the caption/visual review queue; absent captions were not treated as violations.",
    source_report: "agent-findings-local-batch.md",
  },
  {
    channel_id: "UCeZysVNyhl-JqrqesQjcqPg",
    channel_name: "John Hayes",
    total: 28,
    with_captions: 24,
    evidence_mode: "manual full-channel audit: available English caption tracks",
    limitations: "Four uploads without captions remain in the caption/visual review queue; absent captions were not treated as violations.",
    source_report: "agent-findings-local-batch.md",
  },
  {
    channel_id: "UCijF1zTR7RluBFGicVZU4SA",
    channel_name: "Military Living in Central Texas - Mathew Dick",
    total: 46,
    with_captions: 33,
    evidence_mode: "manual full-channel audit: available English caption tracks",
    limitations: "Thirteen uploads without captions remain in the caption/visual review queue; absent captions were not treated as violations.",
    source_report: "agent-findings-local-batch.md",
  },
  {
    channel_id: "UCvyNP3_ZgVLciAIev5t2Gog",
    channel_name: "LIVING IN CENTRAL TEXAS - Jacob Martinez",
    total: 40,
    with_captions: 37,
    evidence_mode: "manual full-channel audit: available English caption tracks",
    limitations: "Three uploads without captions remain in the caption/visual review queue; absent captions were not treated as violations.",
    source_report: "agent-findings-local-batch.md",
  },
  {
    channel_id: "UCWykQcBeQE_1yY2lk9m23YQ",
    channel_name: "Trent Babb - Central Texas Land and Commercial",
    total: 105,
    with_captions: 34,
    evidence_mode: "manual full-channel audit: available English caption tracks",
    limitations: "Seventy-one uploads without captions remain in the caption/visual review queue; absent captions were not treated as violations.",
    source_report: "agent-findings-local-batch.md",
  },
];

const georgeCass = {
  channel_id: "UC5v4flYtIbs8z1ZQ-d-nGXw",
  channel_name: "George Cass - Texas Realtor",
};

// These five channels were initially triaged as full-channel candidates, then
// narrowed after authenticated profile review. Keep the triage action in the
// ledger, but let the adjudication control the final coverage lane.
const discoveryDirectOnlyOverrides = new Set([
  "UCVfUGN4gxcLeWzP5K_fPgnA",
  "UCatgc79aqbQYQQkpNVXfb3A",
  "UC6YcqWxqAo3jNVxyyF2MZyA",
  "UCYsdJIrTd2vYmfqSNfUSYZA",
  "UC_ijOhQ7aWRH6GqL1a-G5Dg",
]);

function fail(message) {
  throw new Error(`FINAL COVERAGE LEDGER FAILED: ${message}`);
}

function clean(value) {
  return value == null ? "" : String(value).replaceAll("\r", "").trim();
}

function normaliseName(value) {
  return clean(value).replaceAll(/\s+/g, " ");
}

function asNonNegativeInteger(value, context) {
  const number = Number(value);
  if (!Number.isInteger(number) || number < 0) fail(`${context} must be a non-negative integer; got ${JSON.stringify(value)}`);
  return number;
}

function csvCell(value) {
  return `"${String(value ?? "").replaceAll('"', '""')}"`;
}

function parseDelimitedLine(line, delimiter) {
  const cells = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const character = line[index];
    if (quoted) {
      if (character === '"' && line[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else if (character === '"') {
        quoted = false;
      } else {
        cell += character;
      }
    } else if (character === '"') {
      quoted = true;
    } else if (character === delimiter) {
      cells.push(cell);
      cell = "";
    } else {
      cell += character;
    }
  }
  if (quoted) fail("Unterminated quote in delimited input");
  cells.push(cell);
  return cells;
}

function parseDelimited(text, delimiter, label) {
  const lines = text.replace(/^\uFEFF/, "").split(/\n/).filter((line) => line !== "");
  if (lines.length < 1) fail(`${label} is empty`);
  const headers = parseDelimitedLine(lines[0], delimiter).map(clean);
  if (headers.some((header) => !header)) fail(`${label} has an empty header`);
  if (new Set(headers).size !== headers.length) fail(`${label} has duplicate headers`);
  return lines.slice(1).map((line, rowIndex) => {
    const values = parseDelimitedLine(line, delimiter);
    if (values.length !== headers.length) {
      fail(`${label} row ${rowIndex + 2} has ${values.length} columns; expected ${headers.length}`);
    }
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

async function readText(name) {
  const filePath = path.join(auditDir, name);
  try {
    return await fs.readFile(filePath, "utf8");
  } catch (error) {
    fail(`required input ${name} is not readable (${clean(error?.message || error)})`);
  }
}

async function readJson(name) {
  const text = await readText(name);
  try {
    return JSON.parse(text);
  } catch (error) {
    fail(`${name} is not valid JSON (${clean(error?.message || error)})`);
  }
}

function requireColumns(rows, columns, label) {
  if (!rows.length) fail(`${label} has no data rows`);
  const available = new Set(Object.keys(rows[0]));
  for (const column of columns) {
    if (!available.has(column)) fail(`${label} is missing required column ${column}`);
  }
}

function toUniqueMap(rows, keyName, label) {
  const output = new Map();
  for (const [index, row] of rows.entries()) {
    const key = clean(row[keyName]);
    if (!key) fail(`${label} row ${index + 2} has no ${keyName}`);
    if (output.has(key)) fail(`${label} has duplicate ${keyName} ${key}`);
    output.set(key, row);
  }
  return output;
}

function assertNoTaylor(channelId, context) {
  if (excludedTaylorChannelIds.has(channelId)) fail(`${context} contains excluded Taylor channel ${channelId}`);
}

function channelIdsFromInputUrls(text, label) {
  const ids = [...text.matchAll(/\/channel\/(UC[A-Za-z0-9_-]{20,})\//g)].map((match) => match[1]);
  if (!ids.length) fail(`${label} contains no channel URLs`);
  return new Set(ids);
}

function videoIdsFromInputUrls(text, label) {
  const ids = [...text.matchAll(/[?&]v=([A-Za-z0-9_-]{11})(?=&|\s|$)/g)].map((match) => match[1]);
  if (!ids.length) fail(`${label} contains no video URLs`);
  return new Set(ids);
}

function urlsFromInput(text, label) {
  const urls = text.split(/\n/).map(clean).filter(Boolean);
  if (!urls.length) fail(`${label} contains no URLs`);
  if (new Set(urls).size !== urls.length) fail(`${label} contains duplicate URLs`);
  return urls;
}

function parseChannelTabUrl(url, label) {
  const match = clean(url).match(
    /^https:\/\/www\.youtube\.com\/channel\/(UC[A-Za-z0-9_-]{20,})\/(videos|shorts|streams)$/,
  );
  if (!match) fail(`${label} contains a malformed channel-tab URL: ${url}`);
  return { channelId: match[1], tab: match[2] };
}

function validateChannelTabManifest(urls, expectedChannelIds, expectedTabs, label) {
  const expectedTabSet = new Set(expectedTabs);
  if (urls.length !== expectedChannelIds.size * expectedTabSet.size) {
    fail(`${label} has ${urls.length} URLs; expected ${expectedChannelIds.size * expectedTabSet.size}`);
  }
  const tabsByChannel = new Map();
  for (const url of urls) {
    const { channelId, tab } = parseChannelTabUrl(url, label);
    if (!expectedChannelIds.has(channelId)) fail(`${label} contains unexpected channel ${channelId}`);
    if (!expectedTabSet.has(tab)) fail(`${label} contains unexpected tab ${tab} for ${channelId}`);
    const tabs = tabsByChannel.get(channelId) ?? new Set();
    if (tabs.has(tab)) fail(`${label} duplicates ${tab} for ${channelId}`);
    tabs.add(tab);
    tabsByChannel.set(channelId, tabs);
  }
  for (const channelId of expectedChannelIds) {
    const tabs = tabsByChannel.get(channelId);
    if (!tabs || tabs.size !== expectedTabSet.size || [...expectedTabSet].some((tab) => !tabs.has(tab))) {
      fail(`${label} does not contain every required tab for ${channelId}`);
    }
  }
}

function aggregateCatalog(catalog) {
  if (!Array.isArray(catalog)) fail(`${inputNames.authenticatedCatalog} must be an array`);
  const videoIds = new Set();
  const channels = new Map();
  for (const [index, item] of catalog.entries()) {
    if (!item || typeof item !== "object") fail(`catalog item ${index + 1} is not an object`);
    const videoId = clean(item.id);
    const channelId = clean(item.channel_id);
    const channelName = normaliseName(item.channel);
    if (!videoId || !channelId || !channelName) fail(`catalog item ${index + 1} is missing id, channel_id, or channel`);
    if (videoIds.has(videoId)) fail(`catalog has duplicate video ID ${videoId}`);
    videoIds.add(videoId);
    assertNoTaylor(channelId, `catalog item ${videoId}`);
    if (!Array.isArray(item.sources) || !item.sources.length || item.sources.some((source) => !["root", "discovery"].includes(source))) {
      fail(`catalog item ${videoId} has invalid sources`);
    }
    const hasCaptions = item.has_captions === true || (Array.isArray(item.caption_file_paths) && item.caption_file_paths.length > 0);
    const row = channels.get(channelId) ?? {
      channel_id: channelId,
      channel_name: channelName,
      total: 0,
      with_captions: 0,
      source_categories: new Set(),
      source_totals: { root: 0, discovery: 0 },
      source_with_captions: { root: 0, discovery: 0 },
    };
    if (row.channel_name !== channelName) fail(`catalog has conflicting names for channel ${channelId}`);
    row.total += 1;
    row.with_captions += hasCaptions ? 1 : 0;
    for (const source of item.sources) {
      row.source_categories.add(source);
      row.source_totals[source] += 1;
      row.source_with_captions[source] += hasCaptions ? 1 : 0;
    }
    channels.set(channelId, row);
  }
  return channels;
}

function aggregateAllowedDirectCatalog(catalog, allowedVideoIds, allowedChannelIds) {
  const channels = new Map();
  for (const item of catalog) {
    const videoId = clean(item?.id);
    const channelId = clean(item?.channel_id);
    if (!allowedVideoIds.has(videoId) || !allowedChannelIds.has(channelId)) continue;
    const channelName = normaliseName(item?.channel);
    const hasCaptions = item.has_captions === true
      || (Array.isArray(item.caption_file_paths) && item.caption_file_paths.length > 0);
    const row = channels.get(channelId) ?? {
      channel_id: channelId,
      channel_name: channelName,
      total: 0,
      with_captions: 0,
      source_categories: new Set(),
    };
    row.total += 1;
    row.with_captions += hasCaptions ? 1 : 0;
    for (const source of item.sources ?? []) row.source_categories.add(source);
    channels.set(channelId, row);
  }
  return channels;
}

function aggregateSummary(summary) {
  if (!summary || typeof summary !== "object" || !Array.isArray(summary.channels)) {
    fail(`${inputNames.authenticatedSummary} must contain a channels array`);
  }
  const channels = new Map();
  for (const [index, item] of summary.channels.entries()) {
    const channelId = clean(item?.channel_id);
    const channelName = normaliseName(item?.channel);
    if (!channelId || !channelName) fail(`authenticated summary channel ${index + 1} is missing channel_id or channel`);
    assertNoTaylor(channelId, `authenticated summary channel ${index + 1}`);
    if (channels.has(channelId)) fail(`authenticated summary has duplicate channel ID ${channelId}`);
    const total = asNonNegativeInteger(item.total, `authenticated summary ${channelId}.total`);
    const withCaptions = asNonNegativeInteger(item.with_captions, `authenticated summary ${channelId}.with_captions`);
    const withoutCaptions = asNonNegativeInteger(item.without_captions, `authenticated summary ${channelId}.without_captions`);
    if (withCaptions + withoutCaptions !== total) fail(`authenticated summary ${channelId} caption counts do not equal total`);
    channels.set(channelId, { channel_id: channelId, channel_name: channelName, total, with_captions: withCaptions });
  }
  return channels;
}

function compareAuthenticatedSources(catalogChannels, summaryChannels) {
  if (catalogChannels.size !== summaryChannels.size) {
    fail(`authenticated catalog has ${catalogChannels.size} channels but summary has ${summaryChannels.size}`);
  }
  for (const [channelId, catalog] of catalogChannels) {
    const summary = summaryChannels.get(channelId);
    if (!summary) fail(`authenticated summary is missing catalog channel ${channelId}`);
    if (catalog.total !== summary.total || catalog.with_captions !== summary.with_captions) {
      fail(`authenticated totals disagree for ${channelId}: catalog ${catalog.total}/${catalog.with_captions}, summary ${summary.total}/${summary.with_captions}`);
    }
  }
}

const [
  catalog,
  authenticatedSummary,
  rootRows,
  rootScopeRows,
  rootLocalInputs,
  rootDirectInputs,
  discoveryDirectInputs,
  rootLocalStatusRowsA,
  rootLocalStatusRowsB,
  gapFullInputs,
  gapFullStatusRows,
  streamInputs,
  streamStatusRows,
  discoveryRows,
  candidateRows,
  manualCoverageRows,
  discoveryAdjudication,
] = await Promise.all([
  readJson(inputNames.authenticatedCatalog),
  readJson(inputNames.authenticatedSummary),
  readText(inputNames.rootChannels).then((text) => parseDelimited(text, "\t", inputNames.rootChannels)),
  readText(inputNames.rootScope).then((text) => parseDelimited(text, "\t", inputNames.rootScope)),
  readText(inputNames.rootLocalInputs),
  readText(inputNames.rootDirectInputs),
  readText(inputNames.discoveryDirectInputs),
  readText(inputNames.rootLocalStatusA).then((text) => parseDelimited(text, "\t", inputNames.rootLocalStatusA)),
  readText(inputNames.rootLocalStatusB).then((text) => parseDelimited(text, "\t", inputNames.rootLocalStatusB)),
  readText(inputNames.gapFullInputs),
  readText(inputNames.gapFullStatus).then((text) => parseDelimited(text, "\t", inputNames.gapFullStatus)),
  readText(inputNames.streamInputs),
  readText(inputNames.streamStatus).then((text) => parseDelimited(text, "\t", inputNames.streamStatus)),
  readText(inputNames.discoveryTriage).then((text) => parseDelimited(text, "\t", inputNames.discoveryTriage)),
  readText(inputNames.candidates).then((text) => parseDelimited(text, "\t", inputNames.candidates)),
  readText(inputNames.manualCoverage).then((text) => parseDelimited(text, ",", inputNames.manualCoverage)),
  readText(inputNames.discoveryAdjudication),
]);

requireColumns(rootRows, ["channel_id", "channel_name", "inclusion_basis"], inputNames.rootChannels);
requireColumns(rootScopeRows, ["channel_id", "channel_name", "recommended_lane"], inputNames.rootScope);
requireColumns(rootLocalStatusRowsA, ["channel_id", "tab", "url", "status"], inputNames.rootLocalStatusA);
requireColumns(rootLocalStatusRowsB, ["channel_id", "tab", "url", "status"], inputNames.rootLocalStatusB);
requireColumns(gapFullStatusRows, ["channel_id", "tab", "url", "status"], inputNames.gapFullStatus);
requireColumns(streamStatusRows, ["channel_id", "tab", "url", "status"], inputNames.streamStatus);
requireColumns(discoveryRows, ["channel_id", "channel_name", "recommended_action"], inputNames.discoveryTriage);
requireColumns(candidateRows, ["channel_id", "channel_name", "audit_lane"], inputNames.candidates);
requireColumns(manualCoverageRows, ["source_report", "channels_or_scope", "in_window_uploads_or_inventory"], inputNames.manualCoverage);

const rootById = toUniqueMap(rootRows, "channel_id", inputNames.rootChannels);
const rootScopeById = toUniqueMap(rootScopeRows, "channel_id", inputNames.rootScope);
if (rootScopeById.size !== rootById.size) {
  fail(`${inputNames.rootScope} has ${rootScopeById.size} channels but root manifest has ${rootById.size}`);
}
const rootLocalChannelIds = new Set();
const rootDirectOnlyChannelIds = new Set();
for (const [channelId, root] of rootById) {
  const scope = rootScopeById.get(channelId);
  if (!scope) fail(`${inputNames.rootScope} is missing root channel ${channelId}`);
  if (normaliseName(scope.channel_name) !== normaliseName(root.channel_name)) {
    fail(`${inputNames.rootScope} channel name disagrees for ${channelId}`);
  }
  if (scope.recommended_lane === "full_channel_local_creator") rootLocalChannelIds.add(channelId);
  else if (scope.recommended_lane === "direct_target_videos_only") rootDirectOnlyChannelIds.add(channelId);
  else fail(`${inputNames.rootScope} has unsupported lane ${scope.recommended_lane} for ${channelId}`);
}
if (rootLocalChannelIds.size !== 42 || rootDirectOnlyChannelIds.size !== 5) {
  fail(`root scope expected 42 full and 5 direct-only channels; got ${rootLocalChannelIds.size}/${rootDirectOnlyChannelIds.size}`);
}
const rootLocalInputUrls = urlsFromInput(rootLocalInputs, inputNames.rootLocalInputs);
const rootLocalInputChannelIds = channelIdsFromInputUrls(rootLocalInputs, inputNames.rootLocalInputs);
if (
  rootLocalInputUrls.length !== rootLocalChannelIds.size * 2
  || rootLocalInputChannelIds.size !== rootLocalChannelIds.size
  || [...rootLocalInputChannelIds].some((channelId) => !rootLocalChannelIds.has(channelId))
) {
  fail(`${inputNames.rootLocalInputs} does not exactly match the 42 local full-channel scope rows`);
}
validateChannelTabManifest(
  rootLocalInputUrls,
  rootLocalChannelIds,
  ["videos", "shorts"],
  inputNames.rootLocalInputs,
);
const rootDirectAllowedVideoIds = videoIdsFromInputUrls(rootDirectInputs, inputNames.rootDirectInputs);
const discoveryDirectAllowedVideoIds = videoIdsFromInputUrls(
  discoveryDirectInputs,
  inputNames.discoveryDirectInputs,
);
const gapFullChannelIds = channelIdsFromInputUrls(gapFullInputs, inputNames.gapFullInputs);
const gapFullInputUrls = urlsFromInput(gapFullInputs, inputNames.gapFullInputs);
validateChannelTabManifest(
  gapFullInputUrls,
  gapFullChannelIds,
  ["videos", "shorts"],
  inputNames.gapFullInputs,
);
const streamInputUrls = urlsFromInput(streamInputs, inputNames.streamInputs);
const streamInputChannelIds = channelIdsFromInputUrls(streamInputs, inputNames.streamInputs);
const expectedStreamChannelIds = new Set([
  ...manualAudits.map((audit) => audit.channel_id),
  georgeCass.channel_id,
  ...rootLocalChannelIds,
  ...gapFullChannelIds,
]);
if (
  expectedStreamChannelIds.size !== 74
  || streamInputUrls.length !== 74
  || streamInputChannelIds.size !== 74
  || [...expectedStreamChannelIds].some((channelId) => !streamInputChannelIds.has(channelId))
  || [...streamInputChannelIds].some((channelId) => !expectedStreamChannelIds.has(channelId))
) {
  fail(`${inputNames.streamInputs} does not exactly match the 74 adjudicated full-channel identities`);
}
validateChannelTabManifest(
  streamInputUrls,
  expectedStreamChannelIds,
  ["streams"],
  inputNames.streamInputs,
);
const completedCollectionStatuses = new Set(["complete", "cutoff_complete", "no_tab"]);
function validateCollectionStatuses(expectedUrls, statusRows, label) {
  const byUrl = toUniqueMap(statusRows, "url", label);
  if (byUrl.size !== expectedUrls.length) {
    fail(`${label} has ${byUrl.size} URL rows; expected ${expectedUrls.length}`);
  }
  for (const url of expectedUrls) {
    const row = byUrl.get(url);
    if (!row) fail(`${label} is missing ${url}`);
    const expected = parseChannelTabUrl(url, label);
    if (clean(row.channel_id) !== expected.channelId) {
      fail(`${label} channel_id ${row.channel_id} disagrees with ${url}`);
    }
    if (clean(row.tab) !== expected.tab) {
      fail(`${label} tab ${row.tab} disagrees with ${url}`);
    }
    if (!completedCollectionStatuses.has(clean(row.status))) {
      fail(`${label} has incomplete status ${row.status} for ${url}`);
    }
  }
  for (const url of byUrl.keys()) {
    if (!expectedUrls.includes(url)) fail(`${label} contains unexpected URL ${url}`);
  }
}
validateCollectionStatuses(
  rootLocalInputUrls,
  [...rootLocalStatusRowsA, ...rootLocalStatusRowsB],
  `${inputNames.rootLocalStatusA}+${inputNames.rootLocalStatusB}`,
);
validateCollectionStatuses(
  gapFullInputUrls,
  gapFullStatusRows,
  inputNames.gapFullStatus,
);
validateCollectionStatuses(
  streamInputUrls,
  streamStatusRows,
  inputNames.streamStatus,
);
const discoveryById = toUniqueMap(discoveryRows, "channel_id", inputNames.discoveryTriage);
const candidatesById = toUniqueMap(candidateRows, "channel_id", inputNames.candidates);
// The candidate registry deliberately retains Taylor's channels for discovery
// bookkeeping. They may be present in an input manifest, but can never become
// a ledger row. Root and triage manifests must not treat them as audit scope.
for (const channelId of [...rootById.keys(), ...discoveryById.keys()]) assertNoTaylor(channelId, "audit-scope manifest");
for (const channelId of discoveryDirectOnlyOverrides) {
  const triage = discoveryById.get(channelId);
  if (!triage || triage.recommended_action !== "full_channel_audit") {
    fail(`discovery scope override ${channelId} is missing or no longer matches the original full-channel triage`);
  }
  if (!discoveryAdjudication.includes(`\`${channelId}\``)) {
    fail(`discovery scope override ${channelId} is absent from ${inputNames.discoveryAdjudication}`);
  }
}
for (const channelId of gapFullChannelIds) {
  const triage = discoveryById.get(channelId);
  if (!triage || triage.recommended_action !== "full_channel_audit" || discoveryDirectOnlyOverrides.has(channelId)) {
    fail(`curated full-channel input ${channelId} is not an eligible full-channel discovery row`);
  }
}

const catalogChannels = aggregateCatalog(catalog);
const rootDirectCatalogChannels = aggregateAllowedDirectCatalog(
  catalog,
  rootDirectAllowedVideoIds,
  rootDirectOnlyChannelIds,
);
const discoveryDirectOnlyChannelIds = new Set(
  discoveryRows
    .filter((row) => (
      row.recommended_action === "direct_video_only"
      || discoveryDirectOnlyOverrides.has(row.channel_id)
    ))
    .map((row) => row.channel_id),
);
const discoveryDirectCatalogChannels = aggregateAllowedDirectCatalog(
  catalog,
  discoveryDirectAllowedVideoIds,
  discoveryDirectOnlyChannelIds,
);
const summaryChannels = aggregateSummary(authenticatedSummary);
compareAuthenticatedSources(catalogChannels, summaryChannels);

const manualById = new Map();
for (const audit of manualAudits) {
  assertNoTaylor(audit.channel_id, "manual audit definition");
  if (manualById.has(audit.channel_id)) fail(`manual audit definition has duplicate channel ID ${audit.channel_id}`);
  const candidate = candidatesById.get(audit.channel_id);
  if (!candidate) fail(`manual audited channel ${audit.channel_id} is absent from ${inputNames.candidates}`);
  if (normaliseName(candidate.channel_name) !== audit.channel_name) {
    fail(`manual audited channel name disagrees with candidate registry for ${audit.channel_id}`);
  }
  if (!String(candidate.audit_lane).startsWith("audit_")) fail(`manual audited channel ${audit.channel_id} lacks an audit lane`);
  if (audit.with_captions > audit.total) fail(`manual audit has impossible caption total for ${audit.channel_id}`);
  const sourceCoverage = manualCoverageRows.filter((row) => clean(row.source_report) === audit.source_report);
  if (!sourceCoverage.length) fail(`manual source report ${audit.source_report} is absent from ${inputNames.manualCoverage}`);
  const coverageToken = audit.channel_name.includes("Mathew Dick") ? "Mathew Dick"
    : audit.channel_name.includes("Jacob Martinez") ? "Jacob Martinez"
      : audit.channel_name.includes("Trent Babb") ? "Trent Babb"
        : audit.channel_name.includes("Brina Gordon") ? "Brina Gordon"
          : audit.channel_name.includes("Aundrea Dudik") ? "Aundrea Dudik"
            : audit.channel_name;
  if (!sourceCoverage.some((row) => clean(row.channels_or_scope).includes(coverageToken))) {
    fail(`manual source report ${audit.source_report} does not identify ${audit.channel_name}`);
  }
  manualById.set(audit.channel_id, audit);
}

const georgeCandidate = candidatesById.get(georgeCass.channel_id);
if (!georgeCandidate || normaliseName(georgeCandidate.channel_name) !== georgeCass.channel_name || georgeCandidate.preliminary_scope !== "high_local_zero_eligible") {
  fail("George Cass zero-eligible channel is missing or changed in candidate registry");
}

const rowsById = new Map();
const directVideoRetrievalGapRows = [];
function addRow(row) {
  assertNoTaylor(row.channel_id, "final ledger");
  if (rowsById.has(row.channel_id)) fail(`final ledger would contain duplicate channel ID ${row.channel_id}`);
  if (row.uploads_with_caption_files + row.uploads_without_caption_files !== row.total_in_window_public_uploads_cataloged) {
    fail(`final ledger caption counts do not equal total for ${row.channel_id}`);
  }
  rowsById.set(row.channel_id, row);
}

function addDirectVideoRetrievalGap(triage, directOnlyOverride = false) {
  if (rowsById.has(triage.channel_id)) return;
  addRow({
    channel_id: triage.channel_id,
    channel_name: normaliseName(triage.channel_name),
    scope_lane: "discovery_direct_video_only",
    total_in_window_public_uploads_cataloged: 0,
    uploads_with_caption_files: 0,
    uploads_without_caption_files: 0,
    evidence_mode: "offline discovery hit followed by authenticated direct-video retrieval attempt",
    triage_recommended_action: triage.recommended_action,
    scope_adjudication: directOnlyOverride
      ? "discovery-gap-adjudication override: direct_video_only"
      : "triage recommendation: direct_video_only",
    source_categories: "discovery",
    limitations: "No eligible authenticated artifact was retained for the direct-video lane. The discovered video may be outside the audit window, unavailable, removed, private, or an extraction gap; this is not a finding and not a complete channel inventory.",
    source_report_or_input: `${inputNames.discoveryTriage}; ${directOnlyOverride ? inputNames.discoveryAdjudication : inputNames.authenticatedCatalog}`.replace(/;\s*$/, ""),
  });
  directVideoRetrievalGapRows.push({
    channel_id: triage.channel_id,
    channel_name: normaliseName(triage.channel_name),
  });
}

function addRootDirectVideoRow(channelId) {
  if (rowsById.has(channelId)) return;
  const root = rootById.get(channelId);
  const scoped = rootDirectCatalogChannels.get(channelId);
  if (!scoped) {
    addRow({
      channel_id: channelId,
      channel_name: normaliseName(root.channel_name),
      scope_lane: "discovery_direct_video_only",
      total_in_window_public_uploads_cataloged: 0,
      uploads_with_caption_files: 0,
      uploads_without_caption_files: 0,
      evidence_mode: "root-scope direct target-video discovery followed by public metadata/caption retrieval attempt",
      triage_recommended_action: "",
      scope_adjudication: "root-scope-adjudication override: direct_target_videos_only",
      source_categories: "discovery",
      limitations: "No eligible public in-window artifact was retained for the directly discovered target-city videos. The videos may be outside the audit window, unavailable, removed, private, unlisted, or retrieval-limited; this is not a finding or a complete channel inventory.",
      source_report_or_input: `${inputNames.rootScope}; ${inputNames.rootDirectInputs}`,
    });
    directVideoRetrievalGapRows.push({
      channel_id: channelId,
      channel_name: normaliseName(root.channel_name),
    });
    return;
  }
  addRow({
    channel_id: channelId,
    channel_name: normaliseName(root.channel_name),
    scope_lane: "discovery_direct_video_only",
    total_in_window_public_uploads_cataloged: scoped.total,
    uploads_with_caption_files: scoped.with_captions,
    uploads_without_caption_files: scoped.total - scoped.with_captions,
    evidence_mode: "public direct target-video metadata and available caption artifacts",
    triage_recommended_action: "",
    scope_adjudication: "root-scope-adjudication override: direct_target_videos_only",
    source_categories: [...scoped.source_categories].sort().join(";"),
    limitations: "Direct-target-video-only row for an out-of-market, statewide, or syndication channel; unrelated uploads were not promoted into the six-city full-channel scope.",
    source_report_or_input: `${inputNames.rootScope}; ${inputNames.rootDirectInputs}; ${inputNames.authenticatedCatalog}`,
  });
}

for (const audit of manualAudits) {
  const authenticated = catalogChannels.get(audit.channel_id);
  const authenticatedItems = catalog.filter((item) => clean(item?.channel_id) === audit.channel_id);
  if (authenticated) {
    if (
      authenticatedItems.length !== authenticated.total
      || authenticatedItems.some((item) => item.content_type !== "live")
    ) {
      fail(`manual channel ${audit.channel_id} has authenticated non-stream inventory that would overlap its reported Videos/Shorts pass`);
    }
    // The manual full-channel pass covered Videos and Shorts. The separately
    // authenticated /streams pass is additive and closes the archived-live tab.
    catalogChannels.delete(audit.channel_id);
  }
  const additionalStreams = authenticated?.total ?? 0;
  const additionalStreamCaptions = authenticated?.with_captions ?? 0;
  addRow({
    channel_id: audit.channel_id,
    channel_name: audit.channel_name,
    scope_lane: "manual_full_channel",
    total_in_window_public_uploads_cataloged: audit.total + additionalStreams,
    uploads_with_caption_files: audit.with_captions + additionalStreamCaptions,
    uploads_without_caption_files: (audit.total - audit.with_captions) + (additionalStreams - additionalStreamCaptions),
    evidence_mode: authenticated
      ? `${audit.evidence_mode}; authenticated archived-livestream metadata and available caption artifacts`
      : audit.evidence_mode,
    triage_recommended_action: "",
    scope_adjudication: "manual audited full-channel scope",
    source_categories: authenticated ? [...authenticated.source_categories].sort().join(";") : "manual",
    limitations: `${audit.limitations} Archived-livestream coverage was probed separately through the completed /streams manifest.`,
    source_report_or_input: authenticated
      ? `${audit.source_report}; ${inputNames.streamInputs}; ${inputNames.authenticatedCatalog}`
      : `${audit.source_report}; ${inputNames.streamInputs}`,
  });
}

let discoveryChannelsExcludedNotInTriage = 0;
let discoveryVideosExcludedNotInTriage = 0;
for (const [channelId, authenticated] of catalogChannels) {
  const triage = discoveryById.get(channelId);
  const root = rootById.get(channelId);
  if (rootDirectOnlyChannelIds.has(channelId)) {
    addRootDirectVideoRow(channelId);
    continue;
  }
  const directOnlyOverride = discoveryDirectOnlyOverrides.has(channelId);
  const discoveryDirectOnly = triage && (triage.recommended_action === "direct_video_only" || directOnlyOverride);
  const discoveryFullChannel = triage && triage.recommended_action === "full_channel_audit" && !directOnlyOverride;
  const hasRootEvidence = authenticated.source_categories.has("root");
  if (!hasRootEvidence && !triage) {
    discoveryChannelsExcludedNotInTriage += 1;
    discoveryVideosExcludedNotInTriage += authenticated.total;
    continue;
  }
  if (discoveryDirectOnly) {
    if (!["full_channel_audit", "direct_video_only"].includes(triage.recommended_action)) {
      fail(`discovery triage ${channelId} has an unsupported recommended action ${triage.recommended_action}`);
    }
    const scopedDirect = discoveryDirectCatalogChannels.get(channelId);
    const directTotal = scopedDirect?.total ?? 0;
    const directWithCaptions = scopedDirect?.with_captions ?? 0;
    if (directTotal === 0) {
      addDirectVideoRetrievalGap(triage, directOnlyOverride);
      continue;
    }
    addRow({
      channel_id: channelId,
      channel_name: normaliseName(triage.channel_name),
      scope_lane: "discovery_direct_video_only",
      total_in_window_public_uploads_cataloged: directTotal,
      uploads_with_caption_files: directWithCaptions,
      uploads_without_caption_files: directTotal - directWithCaptions,
      evidence_mode: "authenticated discovery-video artifacts restricted to the approved direct-video ID manifest",
      triage_recommended_action: triage.recommended_action,
      scope_adjudication: directOnlyOverride
        ? "discovery-gap-adjudication override: direct_video_only"
        : "triage recommendation: direct_video_only",
      source_categories: [...scopedDirect.source_categories].sort().join(";"),
      limitations: `Direct-video-only ledger row; this is not a complete channel inventory. Triage recommends ${triage.recommended_action}${directOnlyOverride ? "; authenticated adjudication narrowed it to direct-video-only" : ""}.`,
      source_report_or_input: `${inputNames.authenticatedCatalog}; ${inputNames.discoveryDirectInputs}; ${inputNames.discoveryTriage}; ${directOnlyOverride ? inputNames.discoveryAdjudication : ""}`.replace(/;\s*$/, ""),
    });
    continue;
  }
  if (discoveryFullChannel && !hasRootEvidence) {
    fail(`full-channel discovery candidate ${channelId} has no authenticated root inventory; rerun the curated full-channel collector before building the final ledger`);
  }
  if (hasRootEvidence && ((root && rootLocalChannelIds.has(channelId)) || discoveryFullChannel)) {
    if (triage && !["full_channel_audit", "direct_video_only"].includes(triage.recommended_action)) {
      fail(`discovery triage ${channelId} has an unsupported recommended action ${triage.recommended_action}`);
    }
    const source = root ? "root scope adjudication: full_channel_local_creator" : "discovery-gap triage full_channel_audit recommendation";
    const channelName = root ? normaliseName(root.channel_name) : authenticated.channel_name;
    addRow({
      channel_id: channelId,
      channel_name: channelName,
      scope_lane: "authenticated_full_channel",
      total_in_window_public_uploads_cataloged: authenticated.total,
      uploads_with_caption_files: authenticated.with_captions,
      uploads_without_caption_files: authenticated.total - authenticated.with_captions,
      evidence_mode: "authenticated yt-dlp full-channel catalog plus local caption-file artifacts",
      triage_recommended_action: triage ? triage.recommended_action : "",
      scope_adjudication: source,
      source_categories: [...authenticated.source_categories].sort().join(";"),
      limitations: "Authenticated inventory is a full-channel lane. Caption-file presence is an artifact-availability signal; visual-layer review is outside this ledger.",
      source_report_or_input: `${inputNames.authenticatedCatalog}; ${inputNames.authenticatedSummary}`,
    });
    continue;
  }
  fail(`catalog channel ${channelId} has no eligible ledger scope`);
}

for (const triage of discoveryRows) {
  const directOnlyOverride = discoveryDirectOnlyOverrides.has(triage.channel_id);
  if (triage.recommended_action === "direct_video_only" || directOnlyOverride) {
    addDirectVideoRetrievalGap(triage, directOnlyOverride);
  }
}
for (const channelId of rootDirectOnlyChannelIds) addRootDirectVideoRow(channelId);

const zeroEligibleRows = [];
function addZeroEligibleRow({ channel_id, channel_name, scope_adjudication, source_report_or_input }) {
  if (rowsById.has(channel_id)) return;
  addRow({
    channel_id,
    channel_name,
    scope_lane: "authenticated_full_channel",
    total_in_window_public_uploads_cataloged: 0,
    uploads_with_caption_files: 0,
    uploads_without_caption_files: 0,
    evidence_mode: "zero-eligible full-channel inventory",
    triage_recommended_action: "",
    scope_adjudication,
    source_categories: "root",
    limitations: "Zero eligible in-window uploads were returned by the completed full-channel collector; retained explicitly to distinguish zero eligible uploads from omitted coverage.",
    source_report_or_input,
  });
  zeroEligibleRows.push({ channel_id, channel_name, total_in_window_public_uploads_cataloged: 0 });
}

for (const [channel_id, root] of rootById) {
  if (!rootLocalChannelIds.has(channel_id)) continue;
  addZeroEligibleRow({
    channel_id,
    channel_name: normaliseName(root.channel_name),
    scope_adjudication: "root full-channel manifest: zero eligible in-window uploads",
    source_report_or_input: inputNames.rootChannels,
  });
}
for (const channel_id of gapFullChannelIds) {
  const triage = discoveryById.get(channel_id);
  addZeroEligibleRow({
    channel_id,
    channel_name: normaliseName(triage.channel_name),
    scope_adjudication: "curated discovery-gap full-channel input: zero eligible in-window uploads",
    source_report_or_input: `${inputNames.gapFullInputs}; ${inputNames.discoveryTriage}`,
  });
}
if (!rowsById.has(georgeCass.channel_id)) {
  addRow({
    channel_id: georgeCass.channel_id,
    channel_name: georgeCass.channel_name,
    scope_lane: "authenticated_full_channel",
    total_in_window_public_uploads_cataloged: 0,
    uploads_with_caption_files: 0,
    uploads_without_caption_files: 0,
    evidence_mode: "zero-eligible channel recorded from candidate registry",
    triage_recommended_action: "",
    scope_adjudication: "explicit zero-eligible root candidate",
    source_categories: "root",
    limitations: "Zero eligible in-window uploads were reported for this root candidate; retained explicitly to distinguish zero eligible uploads from omitted coverage.",
    source_report_or_input: inputNames.candidates,
  });
  zeroEligibleRows.push({ ...georgeCass, total_in_window_public_uploads_cataloged: 0 });
}

const expectedScopedChannelIds = new Set([
  ...manualAudits.map((audit) => audit.channel_id),
  georgeCass.channel_id,
  ...rootById.keys(),
  ...discoveryById.keys(),
]);
if (expectedScopedChannelIds.size !== 119) {
  fail(`frozen adjudicated scope expected 119 unique channel identities; got ${expectedScopedChannelIds.size}`);
}
for (const channelId of expectedScopedChannelIds) {
  if (!rowsById.has(channelId)) fail(`final ledger is missing scoped channel ${channelId}`);
}
for (const channelId of rowsById.keys()) {
  if (!expectedScopedChannelIds.has(channelId)) fail(`final ledger contains unexpected channel ${channelId}`);
}

const ledgerRows = [...rowsById.values()].sort((left, right) => (
  left.scope_lane.localeCompare(right.scope_lane)
  || left.channel_name.localeCompare(right.channel_name)
  || left.channel_id.localeCompare(right.channel_id)
));
const ledgerHeaders = [
  "channel_id",
  "channel_name",
  "scope_lane",
  "total_in_window_public_uploads_cataloged",
  "uploads_with_caption_files",
  "uploads_without_caption_files",
  "evidence_mode",
  "triage_recommended_action",
  "scope_adjudication",
  "source_categories",
  "limitations",
  "source_report_or_input",
];
for (const row of ledgerRows) {
  const width = ledgerHeaders.map((header) => row[header]).length;
  if (width !== ledgerHeaders.length) fail(`output row for ${row.channel_id} has ${width} columns; expected ${ledgerHeaders.length}`);
  for (const header of ledgerHeaders) {
    if (!(header in row)) fail(`output row for ${row.channel_id} is missing ${header}`);
  }
}

const byScope = Object.fromEntries(
  ["manual_full_channel", "authenticated_full_channel", "discovery_direct_video_only"].map((scopeLane) => {
    const scopedRows = ledgerRows.filter((row) => row.scope_lane === scopeLane);
    return [scopeLane, {
      channels: scopedRows.length,
      total_in_window_public_uploads_cataloged: scopedRows.reduce((sum, row) => sum + row.total_in_window_public_uploads_cataloged, 0),
      uploads_with_caption_files: scopedRows.reduce((sum, row) => sum + row.uploads_with_caption_files, 0),
      uploads_without_caption_files: scopedRows.reduce((sum, row) => sum + row.uploads_without_caption_files, 0),
    }];
  }),
);
const totals = ledgerRows.reduce((aggregate, row) => ({
  channels: aggregate.channels + 1,
  total_in_window_public_uploads_cataloged: aggregate.total_in_window_public_uploads_cataloged + row.total_in_window_public_uploads_cataloged,
  uploads_with_caption_files: aggregate.uploads_with_caption_files + row.uploads_with_caption_files,
  uploads_without_caption_files: aggregate.uploads_without_caption_files + row.uploads_without_caption_files,
}), { channels: 0, total_in_window_public_uploads_cataloged: 0, uploads_with_caption_files: 0, uploads_without_caption_files: 0 });

if (totals.uploads_with_caption_files + totals.uploads_without_caption_files !== totals.total_in_window_public_uploads_cataloged) {
  fail("global caption counts do not equal global upload total");
}
if (ledgerRows.some((row) => excludedTaylorChannelIds.has(row.channel_id))) fail("Taylor channel survived final ledger validation");

const discoveryNoiseDocument = await readText("discovery-gap-triage.md");
const noiseMatch = discoveryNoiseDocument.match(/remaining\s+(\d+)\s+channels\s+were classified as noise/i);
const discoveryNoiseOrUnconfirmedChannels = noiseMatch ? Number(noiseMatch[1]) : null;
if (discoveryNoiseOrUnconfirmedChannels == null) fail("Could not read discovery noise count from discovery-gap-triage.md");
if (!authenticatedSummary.counts || typeof authenticatedSummary.counts !== "object") {
  fail(`${inputNames.authenticatedSummary} is missing counts`);
}
const authenticatedCollectorExcludedTaylorInfoFiles = asNonNegativeInteger(
  authenticatedSummary.counts.excluded_taylor_info_files,
  "authenticated summary excluded_taylor_info_files",
);

const outputSummary = {
  schema_version: 1,
  generated_at: new Date().toISOString(),
  audit_window: authenticatedSummary.audit_window ?? null,
  inputs: inputNames,
  totals,
  totals_by_scope_lane: byScope,
  zero_eligible_channels: {
    count: zeroEligibleRows.length,
    channels: zeroEligibleRows.sort((left, right) => left.channel_name.localeCompare(right.channel_name)),
  },
  excluded_or_noise_counts: {
    taylor_channel_ids_excluded_defensively: [...excludedTaylorChannelIds].sort(),
    authenticated_collector_excluded_taylor_info_files: authenticatedCollectorExcludedTaylorInfoFiles,
    authenticated_discovery_channels_excluded_not_in_triage: discoveryChannelsExcludedNotInTriage,
    authenticated_discovery_videos_excluded_not_in_triage: discoveryVideosExcludedNotInTriage,
    offline_discovery_noise_or_unconfirmed_channels: discoveryNoiseOrUnconfirmedChannels,
  },
  discovery_scope_adjudication_overrides: [...discoveryDirectOnlyOverrides].map((channel_id) => ({
    channel_id,
    channel_name: discoveryById.get(channel_id).channel_name,
    final_scope_lane: "discovery_direct_video_only",
    source: inputNames.discoveryAdjudication,
  })),
  root_scope_adjudication: {
    full_channel_local_creator: rootLocalChannelIds.size,
    direct_target_videos_only: rootDirectOnlyChannelIds.size,
    source: inputNames.rootScope,
  },
  discovery_direct_video_retrieval_gaps: {
    count: directVideoRetrievalGapRows.length,
    channels: directVideoRetrievalGapRows.sort((left, right) => left.channel_name.localeCompare(right.channel_name)),
  },
  validation: {
    required_inputs_read: true,
    authenticated_catalog_matches_summary: true,
    duplicate_channel_ids_in_final_ledger: 0,
    duplicate_video_ids_in_authenticated_catalog: 0,
    final_ledger_column_count: ledgerHeaders.length,
    expected_scoped_channel_ids: expectedScopedChannelIds.size,
    taylor_channel_ids_absent_from_final_ledger: true,
  },
};

const csv = [
  ledgerHeaders.map(csvCell).join(","),
  ...ledgerRows.map((row) => ledgerHeaders.map((header) => csvCell(row[header])).join(",")),
].join("\n");
const outputCsvRows = parseDelimited(csv, ",", outputNames.ledger);
if (outputCsvRows.length !== ledgerRows.length) fail("generated CSV row count does not match in-memory ledger");
requireColumns(outputCsvRows, ledgerHeaders, outputNames.ledger);
const outputCsvIds = toUniqueMap(outputCsvRows, "channel_id", outputNames.ledger);
if (outputCsvIds.size !== ledgerRows.length) fail("generated CSV has duplicate channel IDs");
for (const channelId of outputCsvIds.keys()) assertNoTaylor(channelId, "generated CSV");

await Promise.all([
  fs.writeFile(path.join(auditDir, outputNames.ledger), `${csv}\n`),
  fs.writeFile(path.join(auditDir, outputNames.summary), `${JSON.stringify(outputSummary, null, 2)}\n`),
]);

process.stderr.write(
  `Final coverage ledger: ${totals.channels} channels, ${totals.total_in_window_public_uploads_cataloged} uploads, `
  + `${totals.uploads_with_caption_files} with caption files/tracks.\n`,
);
