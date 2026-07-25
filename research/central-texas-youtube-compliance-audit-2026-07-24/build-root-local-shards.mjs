#!/usr/bin/env node

/*
 * Splits the 42 adjudicated local full-channel inputs into two disjoint,
 * approximately balanced collection shards. Historical flat-playlist size is
 * used only as a scheduling weight; it does not change audit scope.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const inputPath = path.join(auditDir, "authenticated-root-local-channel-inputs.txt");
const flatNames = [
  "flat-root-shard-1.tsv",
  "flat-root-shard-2.tsv",
  "flat-root-shard-3.tsv",
];
const outputNames = [
  "authenticated-root-local-shard-a.txt",
  "authenticated-root-local-shard-b.txt",
];

const urls = (await fs.readFile(inputPath, "utf8")).split(/\n/).map((line) => line.trim()).filter(Boolean);
const urlsByChannel = new Map();
for (const url of urls) {
  const match = url.match(/\/channel\/(UC[A-Za-z0-9_-]{20,})\/(videos|shorts)$/);
  if (!match) throw new Error(`Malformed local channel input: ${url}`);
  if (!urlsByChannel.has(match[1])) urlsByChannel.set(match[1], []);
  urlsByChannel.get(match[1]).push(url);
}
if (urlsByChannel.size !== 42) throw new Error(`Expected 42 local channels; got ${urlsByChannel.size}`);
for (const [channelId, channelUrls] of urlsByChannel) {
  if (channelUrls.length !== 2) throw new Error(`${channelId} has ${channelUrls.length} tab URLs`);
}

const inventoryIdsByChannel = new Map();
for (const name of flatNames) {
  const raw = await fs.readFile(path.join(auditDir, name), "utf8");
  for (const match of raw.matchAll(/^(UC[A-Za-z0-9_-]{20,})\\t([A-Za-z0-9_-]{11})(?:\\t|$)/gm)) {
    if (!inventoryIdsByChannel.has(match[1])) inventoryIdsByChannel.set(match[1], new Set());
    inventoryIdsByChannel.get(match[1]).add(match[2]);
  }
}

const scheduled = [...urlsByChannel].map(([channelId, channelUrls]) => ({
  channelId,
  urls: channelUrls,
  weight: inventoryIdsByChannel.get(channelId)?.size ?? 1,
})).sort((left, right) => right.weight - left.weight || left.channelId.localeCompare(right.channelId));

const shards = [
  { weight: 0, channels: [] },
  { weight: 0, channels: [] },
];
for (const item of scheduled) {
  const target = shards[0].weight <= shards[1].weight ? shards[0] : shards[1];
  target.channels.push(item);
  target.weight += item.weight;
}

await Promise.all(shards.map((shard, index) => fs.writeFile(
  path.join(auditDir, outputNames[index]),
  `${shard.channels.flatMap((item) => item.urls).join("\n")}\n`,
)));
process.stderr.write(
  `Root local shards: A=${shards[0].channels.length} channels/weight ${shards[0].weight}; `
  + `B=${shards[1].channels.length} channels/weight ${shards[1].weight}.\n`,
);
