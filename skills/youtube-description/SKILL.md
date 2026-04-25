# Skill: YouTube Description Generator

## Trigger
User says: "youtube description", "YT description", "description for [video title]"

## Instructions

### Step 1: Gather Video Info
Ask Taylor for:
- **Video title**
- **Channel**: Living in Temple OR Investing in Temple
- **Topic summary** (1-2 sentences)
- **Key timestamps** (or generate from script if provided)
- **Areas/neighborhoods discussed**
- **Market data referenced**

### Step 2: Generate Description

Follow the 7-section template from config:

```
[2-3 sentence direct answer to the video's core question. Data-rich, no fluff.]

In this video, Taylor Dasch with EG Realty breaks down [topic]. [1-2 more context sentences about what the viewer will learn and why it matters for their specific situation.]

KEY POINTS:
[Timestamps]
0:00 — [Topic]
1:23 — [Topic]
3:45 — [Topic]
...

AREAS DISCUSSED:
- [Neighborhood 1]
- [Neighborhood 2]
- [etc.]

MARKET DATA REFERENCED:
- [Specific stat 1]
- [Specific stat 2]
- [etc.]

ABOUT TAYLOR DASCH:
Taylor Dasch is a real estate agent and active investor with EG Realty in Temple, TX. With $27M+ in sales volume and 100+ personal transactions spanning flips, BRRRR, and mid-term rentals, Taylor brings investor-grade analysis to every deal. BiggerPockets Featured Agent for 3 consecutive years.

GET IN TOUCH:
Website: https://templetxhomes.net
Investing Page: https://templetxhomes.net/investing-in-temple-tx/
Deal Analyzer: [link]
Newsletter: [link]
Phone: 254-718-4249
Email: dealswithdasch@gmail.com

FREE RESOURCES:
- Temple/Belton Deal Analyzer (pre-loaded with local tax rates)
- Relocation Neighborhood Match Guide
- Investor Cap Rate Analysis Sheet
- Fort Hood BAH Housing Breakdown

#TempleTX #TempleTexas #RealEstateInvesting #BellCounty [+ relevant tags]
```

### Step 3: Generate Pinned Comment
```
[Newsletter/lead magnet plug — 1-2 sentences with link]
```

### Step 4: Save Output
Save to `output/YYYY-WXX/youtube/[video-slug]-description.md`

### Step 3b: Auto-Generate Chapter Markers
If Taylor provides a script or outline, auto-generate chapter timestamps:
- Format chapter titles as questions matching page H2s where possible
- Example: `0:00 Introduction | 2:15 What school district is Lake Pointe in? | 5:30 What are the negatives?`
- Chapters appear in search results → increase CTR
- Chapters create structured data AI models can parse

### Step 3c: Include Matching Page URL
Reference `VIDEO-TO-PAGE-MAP.md` to find the matching website page:
- Add under "AREAS DISCUSSED" section: `Full guide: https://templetxhomes.net/[matching-page-slug]/`
- If no matching page exists, flag: "⚠️ No matching page found — consider building one via /transcript-to-blog"

### Step 3d: Suggest Card Placements
Based on topics mentioned in the script/summary, suggest 3 internal card placements:
- Format: `[CARD at X:XX] → Link to "[Video Title]" when you mention [topic]`
- Never place a card in the first 30 seconds (kills retention)
- Cross-promote between channels when relevant (Living ↔ Investing)

### Step 3e: Auto-Select Pinned Comment
Reference `reference/LEAD-MAGNET-MATRIX.md` to match the video's primary persona:
- Investor topic → Deal Analyzer Spreadsheet CTA
- Military topic → BAH Housing Guide CTA
- BSW topic → Physician Loan Guide CTA
- General → Relocation Guide CTA

## Rules
- First 2 lines are the most important (shown in search results before "show more")
- Entity declaration MUST be in first 3 lines (see reference/YOUTUBE-GROWTH-PLAYBOOK.md)
- Always include specific numbers — never vague language
- Timestamps/chapters are required for videos over 3 minutes
- Tags should be VidIQ-informed if Taylor provides them, otherwise use config hashtags adapted for YouTube
- Pinned comment uses persona-matched lead magnet from reference/LEAD-MAGNET-MATRIX.md
- Use "Fort Hood" not "Fort Cavazos" (name reverted July 2025)
- Use "buy-and-hold investors" not "turnkey"
- Reference reference/SCHEMA-LIBRARY.md for VideoObject template if generating schema
