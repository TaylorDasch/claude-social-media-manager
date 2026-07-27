import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { basename, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const outputDir = fileURLToPath(new URL(".", import.meta.url));
const transcriptJsonPath = resolve(
  process.argv[2] || join(outputDir, "stylecraft-capcut-timeline-final-base-en.json"),
);
const transcript = JSON.parse(readFileSync(transcriptJsonPath, "utf8"));
const timelineSnapshot = JSON.parse(
  readFileSync(join(outputDir, "timeline-segments.json"), "utf8"),
);

const transcriptSha256 = createHash("sha256")
  .update(readFileSync(transcriptJsonPath))
  .digest("hex");

const normalizeTimestamp = (value) => value.replace(",", ".");
const segmentConfidence = (segment) => {
  const probabilities = (segment.tokens ?? [])
    .filter((token) => Number.isFinite(token.p) && !token.text.startsWith("[_"))
    .map((token) => token.p);
  if (!probabilities.length) return null;
  return probabilities.reduce((sum, value) => sum + value, 0) / probabilities.length;
};

const transcriptLines = transcript.transcription.map((segment) => {
  const from = normalizeTimestamp(segment.timestamps.from);
  const to = normalizeTimestamp(segment.timestamps.to);
  return `**[${from} → ${to}]** ${segment.text.trim()}`;
});

const confidenceValues = transcript.transcription
  .map(segmentConfidence)
  .filter((value) => value !== null);
const meanConfidence =
  confidenceValues.reduce((sum, value) => sum + value, 0) / confidenceValues.length;
const lowConfidenceCount = confidenceValues.filter((value) => value < 0.5).length;

const markdown = `# Timestamped CapCut Timeline Transcript

- Timeline snapshot SHA-256: \`${timelineSnapshot.snapshot.snapshot_sha256}\`
- Timeline duration: ${timelineSnapshot.snapshot.timeline_duration_seconds.toFixed(6)} seconds
- Timeline fps setting: ${timelineSnapshot.snapshot.timeline_fps}
- Transcription engine: whisper.cpp \`whisper-cli\`, local \`ggml-base.en.bin\`
- Transcript JSON: \`${basename(transcriptJsonPath)}\`
- Transcript JSON SHA-256: \`${transcriptSha256}\`
- Status: machine transcript; timestamps are aligned to the rendered CapCut timeline, but wording has not been human-proofread.

${transcriptLines.join("\n\n")}
`;
writeFileSync(join(outputDir, "TIMESTAMPED-TRANSCRIPT.md"), markdown);

const manifest = `# Transcription Manifest

## Source lock

- CapCut project: \`/Users/taylordasch_1/Movies/CapCut/User Data/Projects/com.lveditor.draft/0726 (1)\`
- Frozen timeline snapshot: \`draft_info.snapshot.json\`
- Snapshot SHA-256: \`${timelineSnapshot.snapshot.snapshot_sha256}\`
- Timeline ID: \`${timelineSnapshot.snapshot.timeline_id}\`
- Timeline duration: ${timelineSnapshot.snapshot.timeline_duration_seconds.toFixed(6)} seconds
- Timeline fps setting: ${timelineSnapshot.snapshot.timeline_fps}
- Main segments: ${timelineSnapshot.segments.filter((segment) => segment.trackIndex === 0).length}
- Overlay segments: ${timelineSnapshot.segments.filter((segment) => segment.trackIndex !== 0).length}

## Audio reconstruction

- Lossless timeline mix: \`timeline-audio-48k-stereo.flac\`
- Whisper input: \`timeline-whisper-16k-mono.wav\`
- Source trims use CapCut's microsecond source ranges.
- Timeline placement uses CapCut's microsecond target ranges.
- Segment volume values are applied before the tracks are mixed.
- Video segments without an audio stream are represented by silence of the exact target duration.
- Each segment is padded only when source packet/sample rounding would otherwise make it shorter than CapCut's target duration.

## Whisper run

- Binary: \`/opt/homebrew/bin/whisper-cli\`
- Model: \`/Users/taylordasch_1/.cache/whisper/ggml-base.en.bin\`
- Model SHA-256: \`a03779c86df3323075f5e796cb2ce5029f00ec8869eee3fdfb897afe36c6d002\`
- Language: English
- Decode: beam size 5, best-of 5, word-aware splitting
- Prompt supplied with Taylor/Stylecraft/Central Texas proper nouns.
- Machine segments: ${transcript.transcription.length}
- Mean token probability: ${meanConfidence.toFixed(4)}
- Segments with mean token probability below 0.50: ${lowConfidenceCount}

## Timing uncertainty

- Clip map: exact CapCut values, displayed to the nearest millisecond (rounding uncertainty ±0.5 ms).
- 48 kHz audio render: sample-aligned; boundary uncertainty is at most one 48 kHz sample after conversion.
- 16 kHz Whisper input: sample-aligned; boundary uncertainty is at most one 16 kHz sample after conversion.
- Whisper text segment boundaries are model estimates, not edit points. Treat them as approximately ±0.5–1.5 seconds, with larger uncertainty around silence, wind, music, overlapping audio, or cut-off words.
- Proper nouns, numbers, and builder/product terms require human review before publication.
`;
writeFileSync(join(outputDir, "TRANSCRIPTION-MANIFEST.md"), manifest);

console.log(
  JSON.stringify(
    {
      transcriptJsonPath,
      transcriptSha256,
      segmentCount: transcript.transcription.length,
      meanConfidence,
      lowConfidenceCount,
    },
    null,
    2,
  ),
);
