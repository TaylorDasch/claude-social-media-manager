# Shorts/TikTok/Reels Extraction

## Trigger
"extract shorts", "find clips", "shorts from transcript", "tiktok clips", "reels clips", "best 60 seconds"

## Required Inputs
- Full transcript (.SRT or plain text) of a long-form video
- Video title and topic for context
- Optional: timestamps of key moments Taylor wants to highlight

## Step-by-Step Execution

### Step 1 — Analyze Transcript
1. Read the full transcript
2. Identify high-energy moments: strong opinions, surprising data, funny moments, personal stories
3. Flag segments with natural hooks (questions, contrarian claims, specific numbers)
4. Note the "Mac Moments" — physical comedy, genuine reactions, spontaneous humor

### Step 2 — Score Potential Clips
Rate each candidate on 5 criteria (1-5 scale):

| Criteria | What to Look For |
|----------|-----------------|
| **Hook Strength** | Does the first 3 seconds grab attention without context? |
| **Standalone Value** | Does this clip make sense without watching the full video? |
| **Emotional Peak** | Surprise, humor, outrage, excitement — any strong emotion? |
| **Data Density** | Does it contain a specific number or fact viewers can screenshot? |
| **CTA Natural Fit** | Can a DM keyword CTA flow naturally at the end? |

Minimum score to extract: 18/25

### Step 3 — Extract 3-5 Clips

For each extracted clip:

```markdown
## Clip [N]: "[Working Title]"
**Score:** [X]/25
**Source timecode:** [start] → [end]
**Duration:** [30-60 seconds]
**Target platform:** [TikTok / YT Shorts / IG Reels / all]

### Hook (first 3 seconds)
[Exact text — this is what stops the scroll]

### Body (value payload)
[Core content of the clip — may need minor re-editing for flow]

### CTA (last 5 seconds)
"DM me '[KEYWORD]' for [specific value offer]"
OR
"Link in bio for [resource]"

### Edit Notes
- Trim: [what to cut for pacing]
- Text overlay needed: [key stat or quote to put on screen]
- Music suggestion: [trending sound or mood]
- Caption style: [word-by-word auto-captions recommended]

### Platform-Specific Adjustments
**TikTok:** [any TikTok-specific notes — trending format, duet potential]
**YT Shorts:** [title suggestion, must include "Temple TX"]
**IG Reels:** [cover image suggestion, hashtag set]
```

### Step 4 — Rank by Platform Priority
- **TikTok:** Highest energy, most casual, hook-dependent. Best for: opinions, reactions, quick data.
- **YT Shorts:** Can be slightly longer, searchable titles matter. Best for: mini-tours, data breakdowns.
- **IG Reels:** Visual-first, cover image important. Best for: property showcases, lifestyle content.

### Step 5 — Generate Captions for Each Platform

**TikTok caption format:**
```
[Hook question or bold claim]
.
.
.
[1-2 lines of context]
DM me "[KEYWORD]" for [offer] 📲

#TempleTexas #TempleRealEstate #[topic tag] #[3 trending tags]
```

**YT Shorts title format:**
```
[Title with "Temple TX" + primary keyword, under 60 chars]
```

**IG Reels caption format:**
```
[Value-first opening line]

[2-3 lines of context with line breaks]

Save this for later 📌
DM me "[KEYWORD]" for [offer]

#TempleTexas #TempleRealEstate #[5-8 niche tags]
```

## Output Format
Save to `output/YYYY-WXX/shorts/[video-slug]/`:
- `clips-extraction.md` (all clips with scores and details)
- `tiktok-captions.md` (ready-to-post captions)
- `shorts-titles.md` (YT Shorts titles)
- `reels-captions.md` (IG Reels captions)

## Quality Checks
- [ ] Each clip works standalone (no "as I was saying" openings)
- [ ] Each clip ≤ 60 seconds
- [ ] Each hook ≤ 3 seconds
- [ ] No clip starts with "Hey guys" or "So..."
- [ ] DM keyword CTA on every clip
- [ ] No investor content on TikTok (TikTok = buyers/relocators ONLY)
- [ ] Fort Hood (not Fort Cavazos)
- [ ] No banned words from QUALITY-GATES.md
- [ ] Each clip score ≥ 18/25

## Brand Rules
- TikTok audience = buyers and relocators ONLY. No investor content on TikTok.
- Investor clips → YouTube Shorts and IG Reels only
- Every clip needs a DM keyword CTA (never "link in bio" alone)
- Keep Taylor's casual energy — don't over-polish casual moments
- Mac Moments (physical comedy) are gold — always extract if present
