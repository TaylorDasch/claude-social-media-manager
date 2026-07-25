#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const captionDir = path.join(auditDir, "raw", "captions");
const coveragePath = path.join(auditDir, "caption-coverage.json");
const rootCatalogPath = path.join(auditDir, "root-channel-catalog.json");
const discoveryCatalogPath = path.join(auditDir, "discovery-video-catalog.json");
const concurrency = Number(process.env.AUDIT_CONCURRENCY ?? 2);
const requestDelayMs = Number(process.env.AUDIT_REQUEST_DELAY_MS ?? 700);
const apiKey = process.env.YOUTUBE_PUBLIC_API_KEY;
const clientVersion = process.env.YOUTUBE_ANDROID_CLIENT_VERSION ?? "20.10.38";

if (!apiKey) {
  throw new Error("YOUTUBE_PUBLIC_API_KEY is required; use the public key parsed from the current YouTube page");
}

const excludedTaylorChannels = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);
const independentlyAuditedChannels = new Set([
  "UCqo6EaV9o6bFg4szBL8RYEw",
  "UCwoQakQVf2m8hfitYnymb5w",
  "UCeZysVNyhl-JqrqesQjcqPg",
  "UCijF1zTR7RluBFGicVZU4SA",
  "UCvyNP3_ZgVLciAIev5t2Gog",
  "UCWykQcBeQE_1yY2lk9m23YQ",
  "UCrN5LHFTL2qwkmd9z-90RgA",
  "UCw9DgzcPb_rhdp3VHFFo_8Q",
  "UCQIRCIpmSGFVbRXK6OYg6zA",
  "UCApMznnU70goY-0ucOaQNXA",
  "UCKC2Qfjps_rzW0-lUQIP7KA",
  "UCfDOrNekvd28MKc_S897MsQ",
  "UCm-ak6OuI6VnRU7xJbfndMw",
]);
const skipIndependent = process.env.SKIP_INDEPENDENTLY_AUDITED !== "0";
const targetPlacePattern = /\b(?:Temple|Belton|Killeen|Harker Heights|Copperas Cove|Nolanville|Fort (?:Hood|Cavazos)|Bell County)\b/i;
const housingPattern = /\b(?:real estate|realtor|home|house|housing|property|properties|apartment|rent|rental|listing|market|neighborhood|relocat|moving|builder|construction|duplex|mortgage|loan|land|acreage|invest)\w*/i;

await fs.mkdir(captionDir, { recursive: true });

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function timestamp(ms) {
  const total = Math.max(0, Math.floor(Number(ms || 0) / 1000));
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const seconds = total % 60;
  return [hours, minutes, seconds].map((part) => String(part).padStart(2, "0")).join(":");
}

async function fetchWithRetry(url, options = {}) {
  let lastError;
  for (let attempt = 0; attempt < 4; attempt += 1) {
    try {
      await sleep(requestDelayMs);
      const response = await fetch(url, options);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response;
    } catch (error) {
      lastError = error;
      await sleep([600, 1800, 5000, 12000][attempt]);
    }
  }
  throw lastError;
}

async function loadCatalog() {
  const [root, discovery] = await Promise.all([
    fs.readFile(rootCatalogPath, "utf8").then(JSON.parse),
    fs.readFile(discoveryCatalogPath, "utf8").then(JSON.parse),
  ]);
  const rootIds = new Set(root.map((item) => item.id));
  const byId = new Map();
  for (const item of [...root, ...discovery]) {
    if (excludedTaylorChannels.has(item.channel_id)) continue;
    if (skipIndependent && independentlyAuditedChannels.has(item.channel_id)) continue;
    const text = `${item.title ?? ""}\n${item.description ?? ""}`;
    if (!rootIds.has(item.id) && !(targetPlacePattern.test(text) && housingPattern.test(text))) {
      continue;
    }
    const current = byId.get(item.id) ?? item;
    byId.set(item.id, {
      ...current,
      in_root_channel_catalog:
        Boolean(current.in_root_channel_catalog) || rootIds.has(item.id),
    });
  }
  return [...byId.values()].sort((a, b) =>
    a.channel.localeCompare(b.channel) || a.id.localeCompare(b.id),
  );
}

function chooseCaptionTrack(tracks) {
  const scored = tracks.map((track) => {
    const language = track.languageCode ?? "";
    const languageScore = language.startsWith("en") ? 30 : language.startsWith("es") ? 20 : 10;
    const manualScore = track.kind === "asr" ? 0 : 5;
    return { track, score: languageScore + manualScore };
  });
  scored.sort((a, b) => b.score - a.score);
  return scored[0]?.track ?? null;
}

async function collectCaption(item) {
  const rawPath = path.join(captionDir, `${item.id}.json3`);
  const textPath = path.join(captionDir, `${item.id}.txt`);
  try {
    const text = await fs.readFile(textPath, "utf8");
    return {
      id: item.id,
      channel_id: item.channel_id,
      channel: item.channel,
      title: item.title,
      url: item.url,
      status: "available_cached",
      line_count: text.split("\n").filter(Boolean).length,
      transcript_path: path.relative(auditDir, textPath),
    };
  } catch {
    // Cache miss.
  }

  try {
    const playerResponse = await fetchWithRetry(
      `https://www.youtube.com/youtubei/v1/player?key=${encodeURIComponent(apiKey)}`,
      {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "accept-language": "en-US,en;q=0.9",
          "X-Youtube-Client-Name": "3",
          "X-Youtube-Client-Version": clientVersion,
        },
        body: JSON.stringify({
          context: {
            client: {
              clientName: "ANDROID",
              clientVersion,
              hl: "en",
              gl: "US",
            },
          },
          videoId: item.id,
        }),
      },
    );
    const player = await playerResponse.json();
    const tracks = player.captions?.playerCaptionsTracklistRenderer?.captionTracks ?? [];
    const track = chooseCaptionTrack(tracks);
    if (!track?.baseUrl) {
      return {
        id: item.id,
        channel_id: item.channel_id,
        channel: item.channel,
        title: item.title,
        url: item.url,
        status: "unavailable",
        language: "",
        kind: "",
        player_status: player.playabilityStatus?.status ?? "UNKNOWN",
      };
    }
    const captionUrl = new URL(track.baseUrl);
    captionUrl.searchParams.set("fmt", "json3");
    const captionResponse = await fetchWithRetry(captionUrl);
    const caption = await captionResponse.json();
    const lines = (caption.events ?? [])
      .filter((event) => Array.isArray(event.segs))
      .map((event) => ({
        start_ms: Number(event.tStartMs ?? 0),
        duration_ms: Number(event.dDurationMs ?? 0),
        text: event.segs.map((segment) => segment.utf8 ?? "").join("").replace(/\s+/g, " ").trim(),
      }))
      .filter((line) => line.text);
    await fs.writeFile(rawPath, `${JSON.stringify(caption, null, 2)}\n`);
    await fs.writeFile(
      textPath,
      `${lines.map((line) => `${timestamp(line.start_ms)}\t${line.text}`).join("\n")}\n`,
    );
    return {
      id: item.id,
      channel_id: item.channel_id,
      channel: item.channel,
      title: item.title,
      url: item.url,
      status: "available",
      language: track.languageCode ?? "",
      kind: track.kind === "asr" ? "automatic" : "manual",
      line_count: lines.length,
      transcript_path: path.relative(auditDir, textPath),
    };
  } catch (error) {
    return {
      id: item.id,
      channel_id: item.channel_id,
      channel: item.channel,
      title: item.title,
      url: item.url,
      status: "fetch_failed",
      error: String(error),
    };
  }
}

async function mapConcurrent(items, worker, limit) {
  const results = new Array(items.length);
  let nextIndex = 0;
  async function run() {
    while (true) {
      const index = nextIndex;
      nextIndex += 1;
      if (index >= items.length) return;
      results[index] = await worker(items[index]);
      if ((index + 1) % 100 === 0) {
        process.stderr.write(`captions: ${index + 1}/${items.length}\n`);
      }
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, run));
  return results;
}

const items = await loadCatalog();
process.stderr.write(`captions: ${items.length} videos after exclusions\n`);
const coverage = await mapConcurrent(items, collectCaption, concurrency);
coverage.sort((a, b) => a.channel.localeCompare(b.channel) || a.id.localeCompare(b.id));
await fs.writeFile(coveragePath, `${JSON.stringify(coverage, null, 2)}\n`);
const statusCounts = Object.fromEntries(
  Object.entries(Object.groupBy(coverage, (item) => item.status))
    .map(([status, rows]) => [status, rows.length]),
);
process.stdout.write(`${JSON.stringify({ total: coverage.length, ...statusCounts })}\n`);
