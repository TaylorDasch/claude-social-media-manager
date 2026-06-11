# Skill: /clip-grader — Rank Short Clips Against Taylor's Own Winners

## Trigger
"clip grader", "score my clips", "rank these shorts", "/clip-grader", "grade the clips", "pick keepers", "which shorts to post"

## What It Does
Walks `~/claude-social-media-manager/shorts/inbox/`, transcribes every clip with Whisper, scores each against Taylor's actual historical TikTok winners (not generic "viral video" tips), writes a dated ranked report, copies keepers to `shorts/keepers/`, and stages each keeper as DRAFT posts in Postiz on TikTok + Instagram + Facebook for Taylor to review.

Honest framing: this is selection-from-a-batch, not point-estimate view prediction. Goal is "out of 10 clips dropped in, the keepers it picks should reliably beat the rejects on average."

## Inputs
- `~/claude-social-media-manager/shorts/inbox/*.{mp4,mov,mkv,webm,m4v}` — Taylor drops compressed shorts here (from VidIQ, Opus Clip, manual exports, etc.)

## Outputs
- `~/claude-social-media-manager/shorts/reports/batch-YYYY-MM-DD-HHMM.json` — raw transcription + metadata
- `~/claude-social-media-manager/shorts/reports/grader-YYYY-MM-DD-HHMM.md` — ranked report with reasoning per clip
- `~/claude-social-media-manager/shorts/keepers/` — copies of keeper clips
- `~/claude-social-media-manager/shorts/reports/keepers-YYYY-MM-DD-HHMM.json` — manifest of keepers + suggested captions per platform + suggested publish_date
- Postiz drafts on TikTok + Instagram + Facebook for each keeper (DRAFT state, not auto-published)

## Workflow

### Step 1: Transcribe + extract metadata
```bash
bash -lc "cd ~/claude-social-media-manager && python3 scripts/clip-grader/transcribe-batch.py --whisper-model tiny.en"
```
The script returns the path to `batch-*.json` on stdout. Read it.

### Step 2: Score each clip per the rubric below
For each clip in `batch.json["clips"]`, compute a total score (0-100) using the rubric. Apply hard rejections FIRST.

### Step 3: Write the markdown report
Save to `~/claude-social-media-manager/shorts/reports/grader-YYYY-MM-DD-HHMM.md`. Structure per Output Format below.

### Step 4: Copy keepers + build manifest
- Copy every keeper clip from `inbox/` to `keepers/` (don't move — keep originals in inbox until Taylor confirms)
- Write `keepers-YYYY-MM-DD-HHMM.json` manifest with suggested captions per platform and a placeholder `publish_date` (next available 23:00 UTC = 6 PM CDT slot that doesn't conflict with existing Postiz queue — default to 7 days out if uncertain)

### Step 5: Stage drafts in Postiz
```bash
bash -lc "set -a; source ~/shared-keys.env; set +a; bash ~/claude-social-media-manager/scripts/clip-grader/stage-to-postiz.sh ~/claude-social-media-manager/shorts/reports/keepers-YYYY-MM-DD-HHMM.json"
```

### Step 6: Report back to Taylor
Show him:
- N clips graded, N keepers staged, N rejected (with reasons summary)
- Path to the markdown report
- "Review drafts in Postiz UI, then promote to scheduled with `postiz posts:status <id> --status schedule`"
- Surface anything blocking (banned words found, hard rejections, errored uploads)

---

## Scoring Rubric (0-100, grounded in Taylor's actual top performers)

**Hard rejections (auto-reject regardless of score):**
- Investor content on TikTok (cap rate, cash-on-cash, "great investment", "MTR", "underwriting", multi-family pitches) → violates Taylor's lane discipline
- Banned words anywhere in transcript or suggested caption: "turnkey", "dream home", "perfect neighborhood", "nestled", "broker" (use "agent")
- Duration < 10s or > 90s
- Transcript empty or whisper errored
- Audio sounds like a robotic voiceover (transcript has no contractions, all sentences too clean) — flag for review, not auto-reject

**Section A: Hook Strength (0-30 pts) — based on first 5-10 seconds of transcript**
- A1 (0-10): Opens with a contrarian/pattern-interrupt line? (e.g. "Most X do Y. This is Z." or "What no one tells you about...")
- A2 (0-10): First spoken line names a specific audience (BSW resident, Fort Hood family, first-time buyer) OR a universal moving-to-Texas hook?
- A3 (0-10): Novel hook — NOT "Hey guys, today we're looking at...", "What's up everyone", or generic "Welcome to Temple". Penalize if first 5s contains: "today", "in this video", "welcome", "hey guys", "what's up".

**Section B: Angle Quality (0-30 pts)**
- B1 (0-15): Contrarian / honest-cons / "what no one tells you" framing? This is Taylor's proven 10x winner (May 5 = 10.5K views).
- B2 (0-10): Specific local insight a generic relocation video wouldn't have (named street, named neighborhood, BSW district sub-zone, specific commute math, named builder)?
- B3 (0-5): Concrete dollar amount, percentage, or specific named neighborhood in the first 15 seconds?

**Section C: Audience Fit (0-15 pts)**
- C1 (0-10): Clearly aimed at one of: BSW physician/resident, Fort Hood military relocator, out-of-state buyer relocating to TX, first-time buyer, local lifestyle viewer (parents/families/UMHB)? Specificity > generic.
- C2 (0-5): Universal-appeal opener that works for non-Temple viewers too? (broad pull)

**Section D: Arc + Payoff (0-15 pts)**
- D1 (0-10): Complete thought with a payoff inside the clip — not a tease without delivery? Whisper transcript should resolve, not cut off mid-sentence.
- D2 (0-5): Duration in 25-75s sweet spot? (Outside that range = -2 per 10s deviation, capped at 0.)

**Section E: CTA Strength (0-10 pts)**
- E1 (0-10): Has a comment-keyword or DM-trigger CTA naturally embedded? (e.g. "Comment TOUR for the walkthrough", "DM MAP for the BSW commute map"). No CTA = 0.

**Bucket from total score:**
- **80+ : VIRAL CANDIDATE** — KEEPER, stage to Postiz
- **60-79: MID** — KEEPER, stage to Postiz
- **40-59: WEAK** — REJECT, leave in inbox, suggest 1 specific rewrite (new hook OR new CTA OR cut to under 60s)
- **<40: SKIP** — REJECT, leave in inbox, brief reason only

---

## Caption Generation (per keeper)

For each keeper, draft platform-appropriate captions following Taylor's voice rules:
- TikTok: ≤150 words, 3-5 hashtags (1 broad like `#templetx`, 2 niche like `#bswtemple` or `#firsttimehomebuyer`, 1 local like `#76502` or `#bellcountytx`), DM keyword CTA, NO investor framing
- Instagram: ≤150 words, "Save this if you're..." hook is fine on IG, 5-10 hashtags, same DM keyword
- Facebook: ≤200 words, can be slightly longer-form / explanatory, link to templetxhomes.net OK, fewer hashtags (2-3)

Voice rules (from `governance/QUALITY-GATES.md`):
- Lead with the data/insight, not a sales pitch
- Honest negatives where applicable (it's Taylor's brand)
- "Taylor Dasch with EG Realty" entity declaration only required for long-form content, not every short
- 254-718-4249 / dealswithdasch@gmail.com — only include in 1 of 3 platform captions, not all three (avoid spam pattern)
- Use "Fort Hood" not "Fort Hood"
- Use "agent" not "broker"

---

## Output Format (markdown report)

```markdown
# Clip Grader Report — YYYY-MM-DD HHMM

**Inbox:** {path}
**Clips processed:** N
**Keepers:** K
**Rejected:** N-K
**Whisper model:** tiny.en

## Keepers (staged to Postiz drafts)

### 1. {filename} — Score: {score}/100 ({bucket})
- **Hook (first 5s):** "{transcript first 5s}"
- **Why kept:** {1-2 sentence reasoning citing rubric sections}
- **Predicted bucket:** {Viral candidate | Mid}
- **TikTok caption (drafted):**
  > {caption}
- **IG caption (drafted):**
  > {caption}
- **FB caption (drafted):**
  > {caption}
- **Postiz status:** {staged to TT/IG/FB as drafts | upload failed: reason}

(repeat per keeper)

## Rejected

### {filename} — Score: {score}/100 ({bucket})
- **Hook (first 5s):** "{transcript first 5s}"
- **Why rejected:** {1 sentence}
- **Fix to consider:** {one specific rewrite — new hook, new CTA, or cut to <60s}

(brief — one block per reject)

## Hard Rejections (banned content)

- {filename}: reason

## Notes
- Whisper errors: N (list filenames)
- ffprobe errors: N
- Postiz upload errors: N (list)
```

---

## Rules

- NEVER auto-publish. Always create as DRAFT state in Postiz. Taylor reviews and promotes manually.
- NEVER skip the transcription step — scoring on filename alone is a fail.
- If the inbox is empty, exit gracefully with a one-line message — do not invent clips.
- If Whisper errors on a clip, note it in the report but do NOT score it as 0 — flag for re-encode/manual review.
- If a keeper's Postiz upload fails, surface it loudly in the report — Taylor needs to know which clips need re-staging.
- The scoring rubric is grounded in Taylor's OWN data. Do NOT pull in generic "TikTok virality" advice from training data. If a rubric criterion isn't in this file, don't apply it.
- The publish_date in keepers manifest is a placeholder — drafts don't publish until Taylor promotes them. Pick something 5-10 days out at 23:00 UTC (6 PM CDT) so it doesn't conflict with the existing Postiz queue.

## Dependencies
- `whisper` CLI (openai-whisper) on PATH — `tiny.en` model auto-downloads on first use
- `ffprobe` + `ffmpeg` on PATH
- `python3` with stdlib only (no extra packages required)
- `jq` for the staging shell script
- `postiz` CLI authenticated (API key in `~/shared-keys.env`)
- Reads:
  - `~/claude-social-media-manager/shorts/inbox/*.mp4`
  - `~/claude-social-media-manager/governance/QUALITY-GATES.md` (banned words, voice rules)
- Writes:
  - `~/claude-social-media-manager/shorts/reports/batch-*.json`
  - `~/claude-social-media-manager/shorts/reports/grader-*.md`
  - `~/claude-social-media-manager/shorts/reports/keepers-*.json`
  - `~/claude-social-media-manager/shorts/keepers/*.{mp4,mov,…}`

## Tuning Notes
- The rubric weights are based on Taylor's data through 2026-05-23. If a viral hit emerges that doesn't fit the current weights (e.g. a property tour breaks 5K views), update Section B weights to reflect.
- After every batch, log the predicted bucket → actual views (7-day) into `data/clip-grader-calibration.csv` so the rubric can be tuned over time.
