# Production Bible Generator

## Trigger
"production bible", "full production plan", "video production bible", "bible for [topic]"

## Required Inputs
- Video topic/concept
- Target channel: "Living in Temple" (relocation) or "Investing in Temple" (investor)
- Video type: Neighborhood Tour, Market Update, Deal Analysis, Comparison, How-To, Listing Showcase

## Step-by-Step Execution

### Step 1 — Research & Deduplication
1. Read `data/living-in-temple-catalog.txt` and `data/investing-in-temple-catalog.txt`
2. Check for existing coverage — if similar video exists, frame as "update" or find a differentiated angle
3. Read `reference/VIDEO-SCRIPT-FORMULAS.md` for script structure options
4. Read `reference/YOUTUBE-GROWTH-PLAYBOOK.md` for algorithm optimization
5. Read `reference/FILMING-STYLE-GUIDE.md` for production standards
6. Read `reference/CONTENT-PRODUCTION-CHECKLIST.md` for checklist items
7. If neighborhood-related, check `real-estate-redefined/` for existing page data

### Step 2 — Hook Development (3 Options)

Each hook must be ≤ 8 seconds and follow one of these formulas:

**Hook A (Primary — highest conviction):**
Format: [Contrarian claim or surprising number] + [why it matters to viewer]

**Hook B (Alternative — emotional angle):**
Format: [Personal experience or confession] + [what you'll learn]

**Hook C (Safety — proven formula):**
Format: [Question nobody asks] + [promise of answer]

Rules:
- Hook must work WITHOUT context (viewer decides in 1-3 seconds)
- Never start with "Hey guys" or "Welcome back"
- Include a visual direction for each hook (what's on screen)

### Step 3 — Full Script Outline

Structure (8-15 minutes for long-form):

```
SECTION 1 — HOOK (0:00-0:08)
[Hook text + on-screen visual]

SECTION 2 — SETUP (0:08-1:00)
- Who is this for? (persona callout)
- What will you learn? (episode promise — specific, not vague)
- Entity declaration: "Taylor Dasch with EG Realty"

SECTION 3 — BODY SEGMENT 1 (1:00-3:00)
- Topic: [specific subtopic]
- Key data point: [number + source]
- On-screen overlay: [what to show]
- B-roll note: [what to film]

SECTION 4 — BODY SEGMENT 2 (3:00-5:00)
[same structure]

SECTION 5 — BODY SEGMENT 3 (5:00-7:00)
[same structure]

SECTION 6 — BODY SEGMENT 4 (7:00-9:00)
[same structure — include "Scars and All" negative here]

SECTION 7 — VERDICT/SUMMARY (9:00-10:30)
- Bottom line: who should care and why
- Surprise insight or personal take
- "Here's what I'd do if I were you..."

SECTION 8 — CTA (10:30-11:00)
- Primary CTA: subscribe / call / DM keyword
- Secondary CTA: related video link
- Phone number on screen: 254-718-4249
```

### Step 4 — Shot List

```markdown
## A-Roll (Taylor on camera)
| Segment | Location | Setup | Notes |
|---------|----------|-------|-------|
| Hook | [location] | Gimbal, eye-level | High energy, direct to camera |
| Setup | [location] | Tripod, medium | Calm, authoritative |
| Verdict | [location] | Tripod, close-up | Honest, direct |
| CTA | [location] | Tripod, medium | Friendly, inviting |

## B-Roll
| Segment | Shots Needed | Equipment | Duration |
|---------|-------------|-----------|----------|
| [topic] | Drone flyover | Mavic 3 | 15-20s |
| [topic] | Street driving POV | GoPro on dash | 30s |
| [topic] | Walking tour | Gimbal + A7SIII | 60s |
| [topic] | Screen recording | OBS | 20s |

## Solo Backup Shots
(For segments where Taylor can't be on location — film against solid wall)
| Segment | Talking Points | Duration |
|---------|---------------|----------|
| [topic] | [key points to cover] | 30-45s |
```

### Step 5 — On-Screen Overlays
List every data overlay, lower third, text callout, and graphic needed during edit.
Reference: brand colors Midnight #1e293b, Emerald #059669, Snow #f8fafc.

```markdown
## Overlays
| Timecode | Type | Content | Duration |
|----------|------|---------|----------|
| 0:05 | Lower Third | "Taylor Dasch | EG Realty" | 5s |
| 1:30 | Data Card | "[stat + source]" | 4s |
| 3:00 | Map Graphic | "[location visual]" | 6s |
| 6:00 | Pros/Cons | Split screen card | 8s |
| 8:00 | Price Chart | "[price data]" | 5s |
```

### Step 6 — YouTube Metadata
Generate using the youtube-metadata skill format:
- 3 title options
- Full 7-section description
- 30 tags
- Pinned comment with lead magnet
- Card placement suggestions

### Step 7 — Shorts/TikTok Extraction Plan
Identify 2-3 clips from the script for short-form:

```markdown
## Short-Form Clips
| Clip | Timecode Range | Hook | Platform | Duration |
|------|---------------|------|----------|----------|
| Clip 1 | 2:15-3:00 | "[hook]" | TikTok | 45s |
| Clip 2 | 5:30-6:15 | "[hook]" | YT Shorts | 40s |
| Clip 3 | 8:00-8:45 | "[hook]" | IG Reels | 35s |
```

Each clip gets: hook (≤3s), value payload, DM keyword CTA.

### Step 8 — CTA Placement Map

```
0:00-0:10   — NO CTA (earn attention first)
2:00        — Soft verbal: "If you're moving to Temple..."
5:00        — Card: related video
7:00        — Verbal: lead magnet mention
9:00        — Card: website link
10:30-11:00 — Hard CTA: subscribe + phone + DM keyword
End Screen  — Subscribe + best related video
```

## Output Format
Save all sections to `yt-videos/[slug]/` as:
- `production-bible.md` (master document with all sections)
- `shot-list.md` (extracted for filming day)
- `overlays-list.md` (extracted for edit day)

## Quality Checks
- [ ] Hook A/B/C all ≤ 8 seconds
- [ ] Entity declaration in first 60 seconds of script
- [ ] "Scars and All" negative included in body
- [ ] At least 3 data points with sources
- [ ] Solo backup shots listed for all A-roll segments
- [ ] 2-3 short-form clips identified
- [ ] No title duplication with existing catalogs
- [ ] CTA placement follows the CTA map (no CTA before 2:00)
- [ ] Every overlay uses brand colors
- [ ] Fort Hood (not Fort Cavazos), buy-and-hold (not turnkey)

## Brand Rules
- 7-second rule: visual or audio change every 7 seconds minimum
- Never start with "Hey guys" or "Welcome back"
- Data-first: every claim backed by a number
- Honest negatives mandatory (Scars and All)
- No FOMO, no urgency pressure, no salesy language
