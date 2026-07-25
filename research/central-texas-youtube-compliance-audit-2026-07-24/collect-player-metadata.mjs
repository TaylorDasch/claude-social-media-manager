#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const rawDir = path.join(auditDir, "raw", "flat-catalogs");
const cacheDir = path.join(auditDir, "raw", "player-metadata");
const catalogPath = path.join(auditDir, "root-channel-catalog.json");
const csvPath = path.join(auditDir, "root-channel-catalog.csv");
const failuresPath = path.join(auditDir, "root-channel-catalog-failures.json");
const scanPath = path.join(auditDir, "root-channel-catalog-scan.json");
const discoveryPath = path.join(auditDir, "discovery-video-catalog.json");
const discoveryCsvPath = path.join(auditDir, "discovery-video-catalog.csv");
const searchResultsPath = path.join(auditDir, "search-results.json");
const startDate = "2024-07-24";
const endDate = "2026-07-24";
const concurrency = Number(process.env.AUDIT_CONCURRENCY ?? 3);
const requestDelayMs = Number(process.env.AUDIT_REQUEST_DELAY_MS ?? 500);

await fs.mkdir(cacheDir, { recursive: true });

function csvCell(value) {
  const text = value == null ? "" : String(value);
  return `"${text.replaceAll('"', '""')}"`;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getInnertubeConfig() {
  if (process.env.YOUTUBE_PUBLIC_API_KEY && process.env.YOUTUBE_WEB_CLIENT_VERSION) {
    return {
      apiKey: process.env.YOUTUBE_PUBLIC_API_KEY,
      clientVersion: process.env.YOUTUBE_WEB_CLIENT_VERSION,
    };
  }
  const response = await fetch("https://www.youtube.com/watch?v=dQw4w9WgXcQ&hl=en&gl=US", {
    headers: { "accept-language": "en-US,en;q=0.9" },
  });
  if (!response.ok) {
    throw new Error(`Unable to load YouTube configuration: HTTP ${response.status}`);
  }
  const html = await response.text();
  const apiKey = html.match(/"INNERTUBE_API_KEY":"([^"]+)"/)?.[1];
  const clientVersion = html.match(/"INNERTUBE_CLIENT_VERSION":"([^"]+)"/)?.[1];
  if (!apiKey || !clientVersion) {
    throw new Error("Unable to parse YouTube public client configuration");
  }
  return { apiKey, clientVersion };
}

async function readFlatGroups() {
  const files = (await fs.readdir(rawDir))
    .filter((name) => name.endsWith(".jsonl"))
    .sort();
  const groups = [];

  for (const file of files) {
    const match = file.match(/^(UC.+)-(videos|shorts)\.jsonl$/);
    if (!match) continue;
    const [, manifestChannelId, tab] = match;
    const body = await fs.readFile(path.join(rawDir, file), "utf8");
    const entries = [];
    for (const line of body.split("\n")) {
      if (!line.trim()) continue;
      const item = JSON.parse(line);
      if (!item.id) continue;
      entries.push({
        id: item.id,
        flat_title: item.title ?? "",
        flat_duration_seconds: item.duration ?? null,
        manifest_channel_id: manifestChannelId,
        source_tabs: [tab],
        playlist_index: item.playlist_index ?? item.playlist_autonumber ?? entries.length + 1,
      });
    }
    entries.sort((a, b) => a.playlist_index - b.playlist_index);
    groups.push({ file, manifest_channel_id: manifestChannelId, tab, entries });
  }
  return groups;
}

async function fetchPlayer(entry, config) {
  const cachePath = path.join(cacheDir, `${entry.id}.json`);
  try {
    return JSON.parse(await fs.readFile(cachePath, "utf8"));
  } catch {
    // Cache miss.
  }

  let lastError;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      await sleep(requestDelayMs);
      const response = await fetch(
        `https://www.youtube.com/youtubei/v1/player?key=${encodeURIComponent(config.apiKey)}`,
        {
          method: "POST",
          headers: {
            "content-type": "application/json",
            "accept-language": "en-US,en;q=0.9",
          },
          body: JSON.stringify({
            context: {
              client: {
                clientName: "WEB",
                clientVersion: config.clientVersion,
                hl: "en",
                gl: "US",
              },
            },
            videoId: entry.id,
          }),
        },
      );
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      const details = data.videoDetails ?? {};
      const microformat = data.microformat?.playerMicroformatRenderer ?? {};
      const selected = {
        id: entry.id,
        status: data.playabilityStatus?.status ?? "UNKNOWN",
        status_reason: data.playabilityStatus?.reason ?? "",
        title: details.title ?? entry.flat_title,
        description: details.shortDescription ?? "",
        channel_id: details.channelId ?? entry.manifest_channel_id,
        channel: microformat.ownerChannelName ?? "",
        duration_seconds: Number(details.lengthSeconds ?? entry.flat_duration_seconds) || null,
        upload_date: (microformat.uploadDate ?? "").slice(0, 10),
        publish_date: (microformat.publishDate ?? "").slice(0, 10),
      };
      await fs.writeFile(cachePath, `${JSON.stringify(selected, null, 2)}\n`);
      return selected;
    } catch (error) {
      lastError = error;
      await sleep([400, 1200, 3000][attempt]);
    }
  }
  return {
    id: entry.id,
    status: "FETCH_FAILED",
    status_reason: String(lastError),
    title: entry.flat_title,
    description: "",
    channel_id: entry.manifest_channel_id,
    channel: "",
    duration_seconds: entry.flat_duration_seconds,
    upload_date: "",
    publish_date: "",
  };
}

async function mapConcurrent(items, worker, limit) {
  const results = new Array(items.length);
  let nextIndex = 0;
  async function run() {
    while (true) {
      const index = nextIndex;
      nextIndex += 1;
      if (index >= items.length) return;
      results[index] = await worker(items[index], index);
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, run));
  return results;
}

const config = await getInnertubeConfig();
const flatGroups = await readFlatGroups();
const totalFlatIds = flatGroups.reduce((sum, group) => sum + group.entries.length, 0);
process.stderr.write(`player metadata: ${flatGroups.length} channel tabs / ${totalFlatIds} flat rows\n`);
let processedRootRows = 0;
const groupScans = await mapConcurrent(
  flatGroups,
  async (group) => {
    const metadata = [];
    let consecutiveOld = 0;
    let consecutiveMissing = 0;
    let stopReason = "end_of_tab";
    let boundaryDate = "";
    for (const entry of group.entries) {
      const player = await fetchPlayer(entry, config);
      processedRootRows += 1;
      if (processedRootRows % 100 === 0) {
        process.stderr.write(`player metadata: ${processedRootRows}/${totalFlatIds} rows sampled\n`);
      }
      const date = player.upload_date || player.publish_date;
      metadata.push({
        ...player,
        source_tabs: entry.source_tabs,
        url: `https://www.youtube.com/watch?v=${entry.id}`,
        in_window: date >= startDate && date <= endDate,
      });
      if (!date) {
        consecutiveMissing += 1;
        consecutiveOld = 0;
      } else if (date < startDate) {
        consecutiveOld += 1;
        consecutiveMissing = 0;
        boundaryDate = date;
      } else {
        consecutiveOld = 0;
        consecutiveMissing = 0;
      }
      if (consecutiveOld >= 3) {
        stopReason = "three_consecutive_pre_window_uploads";
        break;
      }
      if (consecutiveMissing >= 10) {
        stopReason = "ten_consecutive_missing_dates";
        break;
      }
    }
    if (metadata.length === 1000 && !metadata.some((item) => {
      const date = item.upload_date || item.publish_date;
      return date && date < startDate;
    })) {
      stopReason = "playlist_cap_reached_without_old_boundary";
    }
    return {
      scan: {
        file: group.file,
        channel_id: group.manifest_channel_id,
        tab: group.tab,
        flat_rows: group.entries.length,
        sampled_rows: metadata.length,
        stop_reason: stopReason,
        boundary_date: boundaryDate,
      },
      metadata,
    };
  },
  concurrency,
);
const byRootId = new Map();
for (const group of groupScans) {
  for (const item of group.metadata) {
    const current = byRootId.get(item.id);
    if (!current) {
      byRootId.set(item.id, item);
      continue;
    }
    current.source_tabs = [...new Set([...current.source_tabs, ...item.source_tabs])].sort();
  }
}
const metadata = [...byRootId.values()];
await fs.writeFile(
  scanPath,
  `${JSON.stringify(groupScans.map((group) => group.scan), null, 2)}\n`,
);

const catalog = metadata
  .filter((item) => item.in_window)
  .sort((a, b) =>
    (a.upload_date || a.publish_date).localeCompare(b.upload_date || b.publish_date)
    || a.channel.localeCompare(b.channel)
    || a.id.localeCompare(b.id),
  );
const failures = metadata
  .filter((item) => !item.upload_date && !item.publish_date)
  .sort((a, b) => a.channel_id.localeCompare(b.channel_id) || a.id.localeCompare(b.id));

await fs.writeFile(catalogPath, `${JSON.stringify(catalog, null, 2)}\n`);
await fs.writeFile(failuresPath, `${JSON.stringify(failures, null, 2)}\n`);

const header = [
  "upload_date",
  "publish_date",
  "video_id",
  "channel_id",
  "channel",
  "content_type",
  "duration_seconds",
  "title",
  "url",
  "description",
  "playability_status",
];
const rows = catalog.map((item) => [
  item.upload_date,
  item.publish_date,
  item.id,
  item.channel_id,
  item.channel,
  item.source_tabs.includes("shorts") ? "short" : "video",
  item.duration_seconds,
  item.title,
  item.url,
  item.description,
  item.status,
]);
await fs.writeFile(
  csvPath,
  `${[header, ...rows].map((row) => row.map(csvCell).join(",")).join("\n")}\n`,
);

const searchPayload = JSON.parse(await fs.readFile(searchResultsPath, "utf8"));
const discoveryEntries = searchPayload.unique_videos.map((item) => ({
  id: item.id,
  flat_title: item.title ?? "",
  flat_duration_seconds: item.duration ?? null,
  manifest_channel_id: item.channel_id ?? "",
  source_tabs: ["search"],
  search_channel: item.channel ?? "",
  query: item.query ?? "",
  search_mode: item.search_mode ?? "",
}));
process.stderr.write(`discovery metadata: ${discoveryEntries.length} unique search IDs\n`);
const rootIds = new Set(catalog.map((item) => item.id));
const discoveryMetadata = await mapConcurrent(
  discoveryEntries,
  async (entry, index) => {
    if ((index + 1) % 100 === 0) {
      process.stderr.write(`discovery metadata: ${index + 1}/${discoveryEntries.length}\n`);
    }
    const player = await fetchPlayer(entry, config);
    const date = player.upload_date || player.publish_date;
    return {
      ...player,
      channel: player.channel || entry.search_channel,
      query: entry.query,
      search_mode: entry.search_mode,
      url: `https://www.youtube.com/watch?v=${entry.id}`,
      in_root_channel_catalog: rootIds.has(entry.id),
      in_window: date >= startDate && date <= endDate,
    };
  },
  concurrency,
);
const discoveryCatalog = discoveryMetadata
  .filter((item) => item.in_window)
  .sort((a, b) =>
    (a.upload_date || a.publish_date).localeCompare(b.upload_date || b.publish_date)
    || a.channel.localeCompare(b.channel)
    || a.id.localeCompare(b.id),
  );
await fs.writeFile(discoveryPath, `${JSON.stringify(discoveryCatalog, null, 2)}\n`);
const discoveryHeader = [
  "upload_date",
  "video_id",
  "channel_id",
  "channel",
  "duration_seconds",
  "title",
  "url",
  "query",
  "search_mode",
  "in_root_channel_catalog",
  "description",
  "playability_status",
];
const discoveryRows = discoveryCatalog.map((item) => [
  item.upload_date || item.publish_date,
  item.id,
  item.channel_id,
  item.channel,
  item.duration_seconds,
  item.title,
  item.url,
  item.query,
  item.search_mode,
  item.in_root_channel_catalog,
  item.description,
  item.status,
]);
await fs.writeFile(
  discoveryCsvPath,
  `${[discoveryHeader, ...discoveryRows].map((row) => row.map(csvCell).join(",")).join("\n")}\n`,
);

process.stdout.write(
  `flat_rows=${totalFlatIds} sampled_root_ids=${metadata.length} in_window=${catalog.length} missing_dates=${failures.length} discovery_in_window=${discoveryCatalog.length}\n`,
);
