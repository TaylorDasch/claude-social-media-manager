# Skill: /produce — Omni-Channel Content Pipeline

## Trigger
"produce", "produce this", "/produce", "run the pipeline", "generate all assets"

## What It Does
Takes a finalized YouTube script (or any master content piece) and generates ALL downstream assets in one pass. One input → full content ecosystem.

## Input
The user provides ONE of:
1. A file path to a finished script (e.g., `output/2026-W12/youtube/market-update-script.md`)
2. A video title + topic summary (Claude drafts the master script first)
3. A Deal of the Week address + numbers (triggers deal-specific pipeline)

## Pipeline Steps

### Step 1: Analyze the Master Content
Read the source script/content. Extract:
- **Core topic** and pillar (Market Data / Investor Ed / Relocation / Neighborhoods / BTS / Myth-busting)
- **Key data points** (every specific number, stat, price, percentage)
- **Target personas** (Military / Medical / Investor / General — from social-media-config.json)
- **Neighborhoods mentioned**
- **Controversial/surprising claims** (these become short-form hooks)

### Step 2: Generate YouTube Assets
Reference `skills/youtube-description/SKILL.md` for format.

**Output: `youtube-description.md`**
- 7-section description (direct answer, context, timestamps, areas, data, about, contact)
- SEO tags (include "Temple TX" + primary keyword)
- Pinned comment draft (newsletter plug or lead magnet)

**Output: `youtube-tags.md`**
- 15-20 tags ordered by relevance
- Include long-tail keywords from the content

### Step 3: Generate TikTok / Reels Scripts (2-3 clips)
Reference `skills/tiktok-script/SKILL.md` for format.

For each clip, identify the strongest data point or argument from the master script and build a property tour format around it:

**Output: `tiktok-clip-1.md`, `tiktok-clip-2.md`, etc.**
Each contains:
- Hook (0-3 sec) with text overlay
- Body (3-25 sec) — property tour format: walk through a house while delivering the data point
- CTA with DM keyword (GUIDE/DEALS/TOUR/BAH/BSW/RELOCATE/TEMPLE)
- Caption (1-3 sentences)
- Hashtags (three-tier system from config)
- Filming notes (what property to film at, what to show)
- Posting window (from config schedule)

**Key rule:** Every TikTok is a PROPERTY TOUR with data, not a talking head lecture. The house is the visual. The number is the value.

### Step 4: Generate YouTube Short Script
Reference YouTube Shorts format — heavy text overlays, hook in first 2 seconds.

**Output: `youtube-short.md`**
- Hook text (first 2 sec, ALL CAPS + emoji)
- 30-60 sec condensed version of strongest argument
- Search-optimized title (MUST include "Temple TX" + keyword)

### Step 5: Generate Blog Post Outline
**Output: `blog-outline.md`**
- H1 in question format
- 5-7 H2 sections (also questions where possible)
- Key data points to include under each section
- FAQ schema section (5+ Q&As derived from the video content)
- Internal link targets (neighborhood pages, investing page, other blog posts)
- CTA placement notes (newsletter, Deal Analyzer, contact)
- Word count target: 2,000+
- Note: This is an OUTLINE, not the full post. Taylor or Claude writes the full post separately.

### Step 6: Generate Social Captions
Apply the Framing Effect — every data point becomes TWO posts.

**Output: `social-captions.md`**
Contains all of:

**BiggerPockets Forum Post:**
- Data-heavy, specific numbers
- NO video links (blog links only)
- Reference investor experience ($27M+, 100+ transactions)
- 200-400 words

**LinkedIn Post:**
- Professional tone, still data-driven
- 500 words max
- Tag relevant topics

**Relocator Frame (Instagram/Facebook):**
- Frame the content for someone moving to Temple
- Story-style caption
- Soft CTA

**Investor Frame (Instagram/Facebook):**
- Frame the SAME content for an investor
- Numbers-forward
- DM keyword CTA

### Step 7: Generate Newsletter Segment
Reference `skills/newsletter/SKILL.md` for format.

**Output: `newsletter-segment.md`**
- "Deep Dive" section extract (400 words, answer-first)
- Or "Deal Autopsy" if content is deal-specific
- Bell County Bulletin bullet (1 sentence + data point from the video)
- Subject line options (3, using formula bank)

### Step 8: Generate GBP Post
Reference `skills/gmb-post/SKILL.md` for format (4-week rotation).

**Output: `gbp-post.md`**
- Match the video's topic to the appropriate post type (Market Update if data-heavy, Listing Spotlight if property-focused, Neighborhood Guide if area-focused, Expertise Tip if advice-driven)
- Entity declaration: "Taylor Dasch, real estate agent at EG Realty in Temple, Texas"
- 2+ citable data points from the video content
- Target AI query documented (what Gemini question this answers)
- Link to the blog post or specific templetxhomes.net page (not homepage)
- Under 300 words
- Geotagged photo reminder

## Output Structure
All files saved to:
```
output/YYYY-WXX/produced/[content-slug]/
├── source-script.md          (copy of or link to the master content)
├── youtube-description.md
├── youtube-tags.md
├── tiktok-clip-1.md
├── tiktok-clip-2.md
├── tiktok-clip-3.md          (if enough material)
├── youtube-short.md
├── blog-outline.md
├── social-captions.md
├── newsletter-segment.md
├── gbp-post.md
└── PRODUCTION-CHECKLIST.md   (see below)
```

## Production Checklist
Auto-generated at the end of every pipeline run:

```markdown
# Production Checklist: [Content Title]

## Pre-Film
- [ ] YouTube script finalized
- [ ] TikTok filming locations identified (which properties?)
- [ ] B-roll shot list reviewed
- [ ] Outfit/jacket selected (different from last video)

## Film Day
- [ ] YouTube long-form recorded
- [ ] TikTok clips filmed at properties
- [ ] YouTube Short filmed (or clipped from long-form)

## Post-Production
- [ ] YouTube uploaded + description pasted
- [ ] YouTube tags added
- [ ] Thumbnail created
- [ ] TikTok clips edited + posted (check posting windows)
- [ ] YouTube Short uploaded
- [ ] Instagram Reels cross-posted

## Distribution
- [ ] Blog outline sent to writer / written
- [ ] BiggerPockets post published
- [ ] LinkedIn post published
- [ ] Newsletter segment added to next issue
- [ ] GBP post published (AI citation optimized, entity declaration, specific page link)
- [ ] Social captions posted (both frames)

## Engagement (24h post-publish)
- [ ] Respond to all YouTube comments
- [ ] Respond to all TikTok comments (push to DM)
- [ ] Check DM keyword triggers
- [ ] Pin top comment on YouTube
```

## Quality Gate
Before delivering, run the two-pass check:
1. **Actor pass** — Generate all assets
2. **Revisor pass** — Check against:
   - No banned words (turnkey, dream home, charming, nestled, white glove, Fort Cavazos)
   - All numbers are specific (no "approximately" or ranges where exact data exists)
   - Every CTA uses a DM keyword from the approved list
   - Hashtags follow three-tier system
   - YouTube description has all 7 sections
   - Blog outline has FAQ schema section
   - Framing Effect applied (relocator + investor versions exist)
   - Entity declaration present in YouTube script ("Hi, I'm Taylor Dasch with EG Realty...")

## Example Usage

```
User: /produce
Claude: What's the master content? Give me either:
  1. A file path to a finished script
  2. A video title + topic summary
  3. A Deal of the Week address + numbers

User: The market update script I just wrote — it's about Temple inventory hitting 500+ homes

Claude: [Reads script, runs full pipeline, outputs all assets to output/2026-W12/produced/temple-market-update/]
```

## Step 9: Generate YouTube Community Post
Reference `skills/community-post/SKILL.md` for format.

**Output: `community-post.md`**
- 3 variations (Data Poll, Scars & All Post, Pop Quiz)
- Schedule between this video upload and the next
- Include templetxhomes.net link in at least one variation

## Step 10: Generate Schema Pack
Reference `reference/SCHEMA-LIBRARY.md` for templates.

**Output: `schema-pack.json`**
- VideoObject schema (pre-filled with video title, description, upload date)
- FAQPage schema (pre-filled from blog outline Q&As)
- Article schema (pre-filled with headline, author, dates)
- Ready to paste into AgentFire Spark/Coder block

## Step 11: Auto-Select Pinned Comment
Reference `reference/LEAD-MAGNET-MATRIX.md` for persona matching.

**Output: included in `youtube-description.md`**
- Identify primary persona from the video topic
- Pull matching lead magnet and CTA from the matrix
- Generate pinned comment with specific asset offer + link placeholder

### Post-Publish: Pin Comment via YouTube MCP
Only execute this after Taylor confirms the video is uploaded.
1. Call `youtube_list_videos` to find the newly uploaded video (match by title)
2. Call `youtube_post_comment` with the generated pinned comment text on that video
3. Call `youtube_pin_comment` to pin the posted comment

## Step 12.5: Pull Video Performance Baseline
If this video is part of a series (e.g., Market Update, Deal of the Week, Neighborhood Tour):
1. Call `youtube_get_video_stats` on the previous video in this series to pull views, watch time, CTR, and engagement
2. Record baseline metrics in `PRODUCTION-CHECKLIST.md` under a new "Performance Baseline" section:
   - Previous video title, views at 48h/7d (if available), like ratio, comment count
   - Target: beat the previous video on at least one key metric
3. If no previous video exists in the series, note "First in series — no baseline" and skip

## Step 12: Transcript Deployment Checklist
**Output: appended to `PRODUCTION-CHECKLIST.md`**
```
## Transcript Pipeline (48h after upload)
- [ ] Download auto-transcript from YouTube Studio
- [ ] Clean transcript (fix: BSW, Fort Hood, neighborhood names, numbers)
- [ ] Run /transcript-to-blog on cleaned transcript
- [ ] Deploy blog page to AgentFire with video embedded
- [ ] Add schema pack (schema-pack.json) to page
- [ ] Clear AgentFire cache
- [ ] Request indexing in Google Search Console
```

## Dependencies
- Reads `social-media-config.json` for hashtags, DM keywords, posting schedule, personas
- Reads `reference/SCHEMA-LIBRARY.md` for JSON-LD templates
- Reads `reference/LEAD-MAGNET-MATRIX.md` for persona-matched CTAs
- Reads `reference/VIDEO-SCRIPT-FORMULAS.md` for script structure reference
- References other skill formats (tiktok-script, youtube-description, newsletter, gmb-post, community-post)
- YouTube MCP tools: `youtube_list_videos`, `youtube_post_comment`, `youtube_pin_comment`, `youtube_get_video_stats`
- Outputs to `output/YYYY-WXX/produced/[slug]/`
