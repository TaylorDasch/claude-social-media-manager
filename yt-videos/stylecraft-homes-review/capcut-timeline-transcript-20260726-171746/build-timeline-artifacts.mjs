import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";
import { fileURLToPath } from "node:url";

const outputDir = fileURLToPath(new URL(".", import.meta.url));
const snapshotPath = join(outputDir, "draft_info.snapshot.json");
const draftBytes = readFileSync(snapshotPath);
const draft = JSON.parse(draftBytes);
const snapshotSha256 = createHash("sha256").update(draftBytes).digest("hex");
const audioPresenceCache = new Map();

const MICROS_PER_SECOND = 1_000_000;
const toSeconds = (micros) => Number(micros ?? 0) / MICROS_PER_SECOND;
const fixedSeconds = (seconds) => Number(seconds).toFixed(6);

function timecode(seconds) {
  const millis = Math.round(Number(seconds) * 1000);
  const hours = Math.floor(millis / 3_600_000);
  const minutes = Math.floor((millis % 3_600_000) / 60_000);
  const secs = Math.floor((millis % 60_000) / 1000);
  const ms = millis % 1000;
  return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(secs).padStart(2, "0")}.${String(ms).padStart(3, "0")}`;
}

function shellQuote(value) {
  return `'${String(value).replaceAll("'", `'\\''`)}'`;
}

function atempoChain(speed) {
  let remaining = Number(speed);
  const filters = [];
  while (remaining > 2) {
    filters.push("atempo=2");
    remaining /= 2;
  }
  while (remaining < 0.5) {
    filters.push("atempo=0.5");
    remaining /= 0.5;
  }
  if (Math.abs(remaining - 1) > 1e-9) {
    filters.push(`atempo=${remaining.toFixed(9)}`);
  }
  return filters;
}

function sourceHasAudio(sourcePath) {
  if (audioPresenceCache.has(sourcePath)) {
    return audioPresenceCache.get(sourcePath);
  }
  let hasAudio = false;
  try {
    const result = execFileSync(
      "/opt/homebrew/bin/ffprobe",
      [
        "-v",
        "error",
        "-select_streams",
        "a:0",
        "-show_entries",
        "stream=index",
        "-of",
        "csv=p=0",
        sourcePath,
      ],
      { encoding: "utf8" },
    );
    hasAudio = result.trim().length > 0;
  } catch {
    hasAudio = false;
  }
  audioPresenceCache.set(sourcePath, hasAudio);
  return hasAudio;
}

const videosById = new Map(
  (draft.materials?.videos ?? []).map((video) => [
    video.id,
    {
      path: video.path,
      name: video.material_name || basename(video.path || ""),
      duration: toSeconds(video.duration),
    },
  ]),
);

const rows = [];
for (const [trackIndex, track] of (draft.tracks ?? []).entries()) {
  const segments = [...(track.segments ?? [])].sort(
    (a, b) => a.target_timerange.start - b.target_timerange.start,
  );
  for (const [trackSegmentIndex, segment] of segments.entries()) {
    const material = videosById.get(segment.material_id) ?? {
      path: "",
      name: segment.material_id,
      duration: 0,
    };
    const timelineIn = toSeconds(segment.target_timerange.start);
    const timelineDuration = toSeconds(segment.target_timerange.duration);
    const sourceIn = toSeconds(segment.source_timerange.start);
    const sourceDuration = toSeconds(segment.source_timerange.duration);
    rows.push({
      trackIndex,
      trackId: track.id,
      trackType: track.type,
      lane: trackIndex === 0 ? "MAIN" : `OVERLAY-${trackIndex}`,
      trackSegmentIndex: trackSegmentIndex + 1,
      segmentId: segment.id,
      sourcePath: material.path,
      sourceClip: material.name,
      timelineIn,
      timelineOut: timelineIn + timelineDuration,
      timelineDuration,
      sourceIn,
      sourceOut: sourceIn + sourceDuration,
      sourceDuration,
      speed: Number(segment.speed ?? 1),
      volume: Number(segment.volume ?? 1),
      hasAudio: sourceHasAudio(material.path),
      visible: segment.visible !== false,
      reverse: Boolean(segment.reverse),
    });
  }
}

const mainRows = rows.filter((row) => row.trackIndex === 0);
const overlayRows = rows.filter((row) => row.trackIndex !== 0);
const timelineDuration = toSeconds(draft.duration);

writeFileSync(
  join(outputDir, "timeline-segments.json"),
  `${JSON.stringify(
    {
      snapshot: {
        source_project:
          "/Users/taylordasch_1/Movies/CapCut/User Data/Projects/com.lveditor.draft/0726 (1)",
        source_file: "draft_info.json",
        snapshot_sha256: snapshotSha256,
        timeline_id: draft.id,
        timeline_duration_seconds: timelineDuration,
        timeline_fps: draft.fps,
      },
      segments: rows,
    },
    null,
    2,
  )}\n`,
);

const tsvHeader = [
  "lane",
  "lane_segment",
  "timeline_in",
  "timeline_out",
  "timeline_duration_seconds",
  "source_clip",
  "source_in",
  "source_out",
  "source_duration_seconds",
  "speed",
  "volume",
  "has_audio",
  "source_path",
  "segment_id",
].join("\t");
const tsvRows = rows.map((row) =>
  [
    row.lane,
    row.trackSegmentIndex,
    timecode(row.timelineIn),
    timecode(row.timelineOut),
    fixedSeconds(row.timelineDuration),
    row.sourceClip,
    timecode(row.sourceIn),
    timecode(row.sourceOut),
    fixedSeconds(row.sourceDuration),
    row.speed,
    row.volume,
    row.hasAudio,
    row.sourcePath,
    row.segmentId,
  ].join("\t"),
);
writeFileSync(join(outputDir, "timeline-clip-map.tsv"), `${tsvHeader}\n${tsvRows.join("\n")}\n`);

const markdownRows = rows.map(
  (row) =>
    `| ${row.lane} | ${row.trackSegmentIndex} | ${timecode(row.timelineIn)}–${timecode(row.timelineOut)} | ${row.sourceClip} | ${timecode(row.sourceIn)}–${timecode(row.sourceOut)} | ${fixedSeconds(row.timelineDuration)} | ${row.volume.toFixed(6)} | ${row.hasAudio ? "yes" : "no"} |`,
);
const mapMarkdown = `# CapCut Timeline Clip Map

- Project snapshot: \`draft_info.snapshot.json\`
- Snapshot SHA-256: \`${snapshotSha256}\`
- Timeline ID: \`${draft.id}\`
- Timeline duration: \`${timecode(timelineDuration)}\` (${fixedSeconds(timelineDuration)} seconds)
- Timeline setting: ${draft.fps} fps
- Main-track edits: ${mainRows.length}
- Overlay edits: ${overlayRows.length}
- Time basis: CapCut microsecond target/source ranges converted directly to \`HH:MM:SS.mmm\`.
- Audio rule used for the render: every visible video segment's source audio is trimmed to its source range, scaled by its CapCut segment volume, positioned at its target time, and mixed without normalization.

| Lane | # | Timeline in–out | Source clip | Source in–out | Duration (s) | Volume | Audio |
|---|---:|---|---|---|---:|---:|---|
${markdownRows.join("\n")}
`;
writeFileSync(join(outputDir, "TIMELINE-CLIP-MAP.md"), mapMarkdown);

const concatLines = ["ffconcat version 1.0"];
for (const row of mainRows) {
  concatLines.push(`file ${shellQuote(row.sourcePath)}`);
  concatLines.push(`inpoint ${fixedSeconds(row.sourceIn)}`);
  concatLines.push(`outpoint ${fixedSeconds(row.sourceOut)}`);
}
writeFileSync(join(outputDir, "main-track.ffconcat"), `${concatLines.join("\n")}\n`);

const orderedRows = [...mainRows, ...overlayRows];
const ffmpegInputs = [];
const filterParts = [];
for (const [inputIndex, row] of orderedRows.entries()) {
  if (row.hasAudio) {
    ffmpegInputs.push(
      `  -ss ${fixedSeconds(row.sourceIn)} -t ${fixedSeconds(row.sourceDuration)} -i ${shellQuote(row.sourcePath)} \\`,
    );
  } else {
    ffmpegInputs.push(
      `  -f lavfi -t ${fixedSeconds(row.timelineDuration)} -i ${shellQuote("anullsrc=r=48000:cl=stereo")} \\`,
    );
  }
  const audioFilters = [
    `atrim=duration=${fixedSeconds(row.sourceDuration)}`,
    "asetpts=PTS-STARTPTS",
    ...atempoChain(row.speed),
    `apad=whole_dur=${fixedSeconds(row.timelineDuration)}`,
    `atrim=duration=${fixedSeconds(row.timelineDuration)}`,
    "aformat=sample_rates=48000:channel_layouts=stereo",
    `volume=${row.volume.toFixed(12)}`,
  ];
  if (row.trackIndex !== 0) {
    const delayMs = Math.round(row.timelineIn * 1000);
    audioFilters.push(`adelay=${delayMs}|${delayMs}`);
  }
  const label = row.trackIndex === 0 ? `m${row.trackSegmentIndex - 1}` : `o${inputIndex - mainRows.length}`;
  filterParts.push(`[${inputIndex}:a:0]${audioFilters.join(",")}[${label}]`);
}

const mainLabels = mainRows.map((row) => `[m${row.trackSegmentIndex - 1}]`).join("");
filterParts.push(`${mainLabels}concat=n=${mainRows.length}:v=0:a=1[main]`);
const overlayLabels = overlayRows.map((_, index) => `[o${index}]`).join("");
const mixInputCount = 1 + overlayRows.length;
filterParts.push(
  `[main]${overlayLabels}amix=inputs=${mixInputCount}:duration=longest:dropout_transition=0:normalize=0,atrim=duration=${fixedSeconds(timelineDuration)},asetpts=PTS-STARTPTS[mix]`,
);
filterParts.push(
  "[mix]asplit=2[lossless][whisperbase]",
  "[lossless]aformat=sample_rates=48000:channel_layouts=stereo[archive]",
  "[whisperbase]pan=mono|c0=0.5*c0+0.5*c1,aresample=16000[whisper]",
);

const renderScript = `#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=\${0:A:h}

/opt/homebrew/bin/ffmpeg -hide_banner -loglevel warning -stats -y \\
${ffmpegInputs.join("\n")}
  -filter_complex ${shellQuote(filterParts.join(";"))} \\
  -map '[archive]' -c:a flac -compression_level 8 "\${SCRIPT_DIR}/timeline-audio-48k-stereo.flac" \\
  -map '[whisper]' -c:a pcm_s16le "\${SCRIPT_DIR}/timeline-whisper-16k-mono.wav"
`;
writeFileSync(join(outputDir, "render-timeline-audio.zsh"), renderScript, { mode: 0o755 });

console.log(
  JSON.stringify(
    {
      outputDir,
      snapshotSha256,
      timelineDuration,
      mainSegments: mainRows.length,
      overlaySegments: overlayRows.length,
      renderInputs: orderedRows.length,
    },
    null,
    2,
  ),
);
