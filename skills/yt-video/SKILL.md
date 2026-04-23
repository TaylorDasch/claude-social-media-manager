# Skill: /yt-video — YouTube Video Production Prep

## Trigger
"new video", "video about", "film this", "yt video", "video prep", "video idea", "/yt-video", any topic + "video"

## What It Does
Takes a video topic and generates the complete production package in one pass: deep research, script outline, shot list, filming notes, and post-production checklist. Everything Taylor needs to walk into film day prepared. Output goes to `yt-videos/[video-slug]/` so each video has its own workspace.

## Input
The user provides:
1. **Topic** — What the video is about (e.g., "Top 3 luxury neighborhoods Temple TX", "BSW relocation guide")
2. **Channel** — "Living in Temple" (relocation/lifestyle) or "Investing in Temple" (investor) — infer from topic if not stated
3. **Format** — Long-form (8-15 min), Short (< 60 sec), or Both — default to Long-form + Short clips

**Optional:**
- Target persona override (Military / Medical / Investor / Relocator)
- Specific properties or neighborhoods to feature
- Desk-filmable or on-location
- Matching website page URL (from VIDEO-TO-PAGE-MAP.md)

## Instructions

### Step 1: Load Context
- Read `reference/VIDEO-SCRIPT-FORMULAS.md` — pick the best script formula for this topic
- Read `reference/TEMPLE-TX-DATA-VAULT.md` — pull all relevant hard numbers
- Read `reference/YOUTUBE-GROWTH-PLAYBOOK.md` — title formulas, retention mechanics
- Read `reference/FILMING-STYLE-GUIDE.md` — production standards
- Read `VIDEO-TO-PAGE-MAP.md` — check if a matching page exists or needs building
- Read `data/living-in-temple-catalog.txt` and `data/investing-in-temple-catalog.txt` — check for existing videos on similar topics (avoid duplication, find linking opportunities)

### Step 2: Research & Competitive Analysis
Before writing the script, gather:
- **Search intent** — What would someone type into Google/YouTube/AI to find this content?
- **Top 3 search queries** this video should rank for
- **Existing YouTube competition** — Are other Temple TX agents covering this topic? What angle are they missing?
- **AEO angle** — What question could an AI engine answer by citing this video's transcript?
- **Data points needed** — Pull specific numbers from the data vault, MLS data, or flag what Taylor needs to look up

### Step 3: Generate Title Options
Provide 3 title options using proven formulas from `reference/YOUTUBE-GROWTH-PLAYBOOK.md`:
```
TITLE OPTIONS:
1. [Data-specific formula] — e.g., "$350K Gets You THIS in Temple TX (Full Neighborhood Tour)"
2. [Question formula] — e.g., "Is Legacy Ranch Worth the Premium? (BSW Doctor's Neighborhood)"
3. [Curiosity/contrast formula] — e.g., "Why Temple TX Doctors Are Leaving Austin for THIS Neighborhood"

RECOMMENDED: [#X] — [reason: search volume, CTR potential, differentiation]
```

### Step 4: Generate Script Outline
Use the matched formula from VIDEO-SCRIPT-FORMULAS.md:

```markdown
## Script Outline: [Title]

### HOOK (0:00-0:15) — First 15 seconds decide everything
- **Opening line:** [Exact words. Lead with the most surprising number or claim.]
- **Pattern interrupt at 3 sec:** [Visual or audio change]
- **Thesis preview:** [One sentence: what the viewer gets by staying]
- **On-screen text:** [What appears as text overlay]

### SETUP (0:15-2:00) — Context & credibility
- **Entity declaration:** "I'm Taylor Dasch with EG Realty..."
- **Why this matters:** [Connect to viewer's situation — relocating, investing, PCS]
- **Key context data:** [2-3 specific numbers that frame the topic]

### BODY — [3-5 segments, each 2-3 minutes]

#### Segment 1: [Topic]
- **Key data:** [specific numbers]
- **Visual:** [what's on screen — MLS screenshot, driving footage, property walk]
- **Pattern interrupt:** [transition between segments]
- **Scars & All moment:** [honest negative if applicable]

#### Segment 2: [Topic]
- [same structure]

#### Segment 3: [Topic]
- [same structure]

[Continue as needed]

### VERDICT / TAYLOR'S TAKE (near end)
- **Bottom line:** [Direct, honest assessment]
- **Who this is for:** [Persona match]
- **Who should skip it:** [Honest negative — builds trust]

### CTA (last 60 sec)
- **Primary:** [Newsletter / Deal Analyzer / Guide — matched from reference/LEAD-MAGNET-MATRIX.md]
- **Secondary:** "Subscribe" + end screen
- **DM keyword:** [from approved list: GUIDE/DEALS/TOUR/BAH/BSW/RELOCATE/TEMPLE]
```

### Step 5: Generate Shot List
```markdown
## Shot List

### Required A-Roll (Taylor on camera)
- [ ] Hook delivery (face-to-camera, high energy)
- [ ] Entity declaration (can be same take or separate)
- [ ] Verdict/Taylor's Take (face-to-camera, authentic)
- [ ] CTA (face-to-camera, direct)

### Required B-Roll
- [ ] [Specific shot 1 — e.g., "Driving into Legacy Ranch entrance on S 31st St"]
- [ ] [Specific shot 2 — e.g., "MLS listing screenshot of $521K active listing"]
- [ ] [Specific shot 3 — e.g., "Walking the community pool area"]
- [continue for all visual references in the script]

### Drone Shots (if on-location)
- [ ] [Neighborhood overview — fly-in from south]
- [ ] [Street-level fly-through — main boulevard]

### Screen Recordings (if desk-filmable)
- [ ] [Spreadsheet walkthrough — cap rate calculation]
- [ ] [Google Maps — commute visualization]
- [ ] [MLS screenshots — comp data]

### Setup Notes
- **Location(s):** [Where Taylor films this]
- **Time of day:** [Best light / traffic conditions]
- **Wardrobe:** [Change from last video if batch filming]
- **Equipment:** [Standard + any special needs — gimbal for walk-and-talk, lapel mic for outdoor]
```

### Step 6: Generate Short-Form Clips Plan
Identify the 2-3 strongest moments from the script that work as standalone TikTok/Shorts:

```markdown
## Short-Form Clips (cut from long-form or film separately)

### Clip 1: [Hook moment]
- **Timestamp range:** ~[X:XX-X:XX] in the long-form
- **Standalone hook:** [Rewritten as a 3-sec TikTok hook]
- **DM keyword:** [KEYWORD]
- **Can be cut from long-form?** Yes/No — [if No, needs separate vertical filming]

### Clip 2: [Data bomb moment]
- [same structure]

### Clip 3: [Scars & All moment]
- [same structure]
```

### Step 7: Generate Post-Production Checklist
Pull from `reference/CONTENT-PRODUCTION-CHECKLIST.md` and customize for this specific video:

```markdown
## Post-Production Checklist: [Title]

### Edit
- [ ] Visual change every 15-20 sec (long) or 7 sec (short)
- [ ] Captions added — watch for: [list proper nouns in this video that CapCut will misspell]
- [ ] Thumbnail: [specific concept — e.g., "Taylor pointing at Legacy Ranch sign, price overlay $521K"]
- [ ] Title: [recommended title from Step 3]

### Upload
- [ ] Channel: [Living in Temple / Investing in Temple]
- [ ] Description: Run /youtube-description with this script
- [ ] Tags: [10-15 suggested tags specific to this topic]
- [ ] Pinned comment: [persona-matched lead magnet]
- [ ] End screen: subscribe + [related video suggestion]
- [ ] Cards: [specific card placements based on cross-references]
- [ ] Chapters: [pre-formatted timestamp list from script outline]

### Deploy (48h after upload)
- [ ] Download auto-transcript from YouTube Studio
- [ ] Clean transcript (fix: [list proper nouns specific to this video])
- [ ] Run /transcript-to-blog on cleaned transcript
- [ ] Deploy blog page to AgentFire
- [ ] Add schema pack
- [ ] Matching page: [URL from VIDEO-TO-PAGE-MAP.md or "BUILD NEW: /[suggested-slug]/"]

### Repurpose
- [ ] Run /produce on finalized script for full asset generation
- [ ] Post TikTok clips 24-48h after long-form
- [ ] Schedule community post between this video and next
```

### Step 8: Save Output
Save all files to `yt-videos/[video-slug]/`:
```
yt-videos/[video-slug]/
  research.md          (Step 2 output)
  script-outline.md    (Steps 3-4 output)
  shot-list.md         (Step 5 output)
  short-form-clips.md  (Step 6 output)
  checklist.md         (Step 7 output)
```

## Quality Gate
Before delivering, verify:
- [ ] No banned words (turnkey, dream home, charming, nestled, white glove, Fort Cavazos)
- [ ] All data points are specific — no "approximately" or "around"
- [ ] Entity declaration included in script
- [ ] At least one Scars & All moment in the outline
- [ ] Hook contains a specific number or surprising claim
- [ ] Short-form clips have standalone hooks (don't rely on long-form context)
- [ ] Shot list is specific enough that Taylor knows exactly what to film
- [ ] Matching page identified (existing or flagged for building)

## Rules
- ALWAYS check the video catalogs first — don't prep a video Taylor already filmed
- Script outline, not full script. Taylor ad-libs on camera. Give him the structure and data, not a teleprompter.
- Shot list must be SPECIFIC. "Get B-roll" is useless. "Film the Legacy Ranch entrance sign from S 31st St at golden hour" is useful.
- If the topic requires data Taylor doesn't have yet, flag it clearly: "DATA NEEDED: [what to pull from MLS/CAD]"
- Default to on-location filming unless Taylor says desk-filmable or the topic is clearly a screen-share analysis
- Every video should have a matching page strategy — either link to existing or flag for building

## Dependencies
- Reads `reference/VIDEO-SCRIPT-FORMULAS.md`, `reference/TEMPLE-TX-DATA-VAULT.md`, `reference/YOUTUBE-GROWTH-PLAYBOOK.md`, `reference/FILMING-STYLE-GUIDE.md`, `reference/LEAD-MAGNET-MATRIX.md`
- Reads `VIDEO-TO-PAGE-MAP.md` for page matching
- Reads `data/living-in-temple-catalog.txt` and `data/investing-in-temple-catalog.txt` for duplication check
- Outputs to `yt-videos/[video-slug]/`
