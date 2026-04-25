# Skill: /transcript-to-blog — YouTube Transcript to AEO Blog Post

## Trigger
"transcript to blog", "yt to blog", "/transcript-to-blog", "/yt-to-blog", "turn this video into a blog", "blog from transcript", "blog from video"

## What It Does
Takes a YouTube video URL or pasted transcript and generates a complete, structured blog post optimized for AI Engine Optimization (AEO), ready to paste into AgentFire. This is the highest-ROI skill in the system — every YouTube video becomes a citable, indexable, lead-generating page.

## Input
The user provides ONE of:
1. A YouTube URL (Claude fetches/reads the transcript)
2. A pasted transcript (raw text from YouTube or Descript)
3. A video title + transcript file path

**Optional:**
- Target page URL on templetxhomes.net (for embedding the post)
- Specific internal links to prioritize

## Instructions

### Step 1: Load Context Files
Before generating anything, read these files:
- `VIDEO-TO-PAGE-MAP.md` — Match the video to its target page and find related videos/pages
- `reference/SCHEMA-LIBRARY.md` — Pull VideoObject, FAQPage, and Article schema templates
- `reference/LEAD-MAGNET-MATRIX.md` — Match the video's persona/topic to the right lead magnet for the pinned comment
- `research/AEO-DIRECTIVES.md` — Entity consistency rules, AI citation optimization
- `social-media-config.json` — Brand voice, personas, DM keywords
- `/Users/taylordasch_1/open-claw/feedback-log.md` — Content feedback patterns

### Step 2: Analyze the Transcript
Extract and catalog:
- **Core question** the video answers (becomes the H1)
- **Every specific number** — prices, percentages, counts, dates, distances, rates
- **Every neighborhood name** mentioned
- **Every negative/honest take** — foundation issues, flood zones, noise, drawbacks, deal-breakers
- **Target persona** — Military / Medical / Investor / Relocator / General
- **Content pillar** — Market Data / Investor Ed / Relocation / Neighborhoods / BTS / Myth-busting
- **Quotable moments** — Taylor's strongest one-liners and data drops

### Step 3: Generate the Blog Post

Output a single markdown file with all sections in this order:

---

#### Section 1: Meta Data Block
```
TITLE: [SEO title — under 60 chars, includes "Temple TX" + primary keyword]
SLUG: [url-friendly-slug]
META DESCRIPTION: [155 chars max — direct answer + data point + location]
TARGET PAGE: [templetxhomes.net URL if provided, or suggested page from VIDEO-TO-PAGE-MAP.md]
```

#### Section 2: BLUF (Bottom Line Up Front)
50 words max. Direct, factual summary answering the video's core question. Lead with the number or verdict. No throat-clearing. AI engines scrape this paragraph first — make it citable.

```html
<p class="bluf"><strong>Bottom Line:</strong> [50-word direct answer with specific data]</p>
```

#### Section 3: YouTube Embed Placeholder
```
[EMBED YOUTUBE VIDEO: "Video Title Here" — URL]
```
Place immediately after the BLUF. This is where Taylor pastes the iframe.

#### Section 4: Structured Body
Break the transcript into logical H2/H3 hierarchy following these rules:

- **H2s are questions** matching common search queries (how AI engines find content)
- **H3s are sub-answers** within each H2
- Retain ALL hard data — every number, every neighborhood name, every specific claim
- Remove verbal filler ("um", "you know", "so basically") but keep Taylor's natural phrasing
- Paragraphs stay short — 2-4 sentences max
- Bold key numbers and neighborhood names on first mention
- Add transitional context between sections that existed as visual cues in the video
- Target word count: 1,500-2,500 words (enough depth for AI citation, not so long readers bounce)

Example H2 structure:
```markdown
## How Much Does a House Cost in [Neighborhood], Temple TX?
### Entry-Level: $180K-$220K
### Mid-Range: $250K-$320K

## What Are the Biggest Drawbacks of Living in [Area]?
### Foundation Concerns on Expansive Clay
### Train Noise Along the Eastern Corridor
```

#### Section 5: "Scars & All" Callout
Extract the most brutally honest or negative statement from the transcript. This is Taylor's differentiator and triggers "Information Gain" scoring in AI engines.

```html
<blockquote class="scars-and-all">
  <strong>Scars & All:</strong> "[Exact quote or close paraphrase of the negative reality Taylor mentioned]"
</blockquote>
```

If the video contains multiple honest negatives, pick the one most likely to be unique information that competitors would never publish.

#### Section 6: FAQ Section
Extract 3-5 of the most important questions answered in the video. Write in clean Q&A format:

```markdown
## Frequently Asked Questions

### [Question 1 — written as a natural search query]
[2-3 sentence answer. Lead with the number or verdict.]

### [Question 2]
[Answer]

### [Question 3]
[Answer]
```

Rules:
- Questions must be phrased how a real person would ask Google or an AI engine
- Answers must start with the direct answer, then add context
- Include specific data in every answer — no vague responses
- These feed directly into FAQPage schema (Section 8)

#### Section 7: Internal Links
Suggest 3-5 links to other templetxhomes.net pages based on topics mentioned in the video.

```markdown
## Related Pages
- [Anchor text](https://templetxhomes.net/page-slug/) — Why this link is relevant
- [Anchor text](https://templetxhomes.net/page-slug/) — Why this link is relevant
```

Cross-reference `VIDEO-TO-PAGE-MAP.md` for matches. Prioritize:
1. Neighborhood pages mentioned in the video
2. The investing page (if investor content)
3. Relocation guide (if relocation content)
4. Other blog posts covering related topics

#### Section 8: Schema JSON-LD
Output clean, valid JSON-LD containing three schemas in a single `<script>` block:

**VideoObject** — Pull template from `reference/SCHEMA-LIBRARY.md`, fill in:
- name, description, thumbnailUrl, uploadDate, duration, contentUrl, embedUrl

**FAQPage** — Generated from Section 6 Q&As:
- Each Q&A becomes a Question/Answer entity

**Article** — With author entity:
- headline, datePublished, author (Taylor Dasch), publisher (EG Realty)
- Include `about` property with neighborhood/topic entities

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "VideoObject", ... },
    { "@type": "FAQPage", ... },
    { "@type": "Article", ... }
  ]
}
</script>
```

#### Section 9: Pinned Comment
Match the video's persona and topic to a lead magnet from `reference/LEAD-MAGNET-MATRIX.md`.

```markdown
## Pinned Comment Draft
[1-2 sentence lead magnet plug matching the video's audience. Include DM keyword if for YouTube, or newsletter link if for the blog.]
```

---

### Step 4: Quality Gate (Two-Pass System)

**Actor pass** — Generate the full blog post (Steps 1-3 above).

**Revisor pass** — Audit against this checklist before delivering:

| Check | Rule |
|-------|------|
| Banned words | No "turnkey", "dream home", "charming", "nestled", "white glove", "Fort Cavazos", "approximately", "around" (when exact data exists) |
| Fort Hood | Always "Fort Hood" never "Fort Cavazos" (name reverted July 2025) |
| Investor language | "Buy-and-hold investors" not "turnkey investors" |
| Specific numbers | Every data point is exact — no "approximately $250K" when "$247,500" was said |
| Entity consistency | "Taylor Dasch" + "EG Realty" + "Temple, TX" — same every time, matching research/AEO-DIRECTIVES.md |
| BLUF present | 50 words max, leads with data |
| Scars & All present | At least one honest negative callout |
| FAQ count | 3-5 Q&As minimum |
| Internal links | 3-5 links minimum, all to real templetxhomes.net pages |
| Schema valid | VideoObject + FAQPage + Article all present, valid JSON-LD |
| H2s are questions | Every H2 is phrased as a search query |
| Meta title length | Under 60 characters, includes "Temple TX" |
| Meta description length | Under 155 characters |
| No agent speak | Read every sentence — does it sound like a data analyst or a used car salesman? |
| Embed placeholder | YouTube embed placeholder present after BLUF |
| Pinned comment | Persona-matched lead magnet included |

If any check fails, fix it before delivering. Flag what was caught and corrected.

### Step 5: Save Output
Save to:
```
output/YYYY-WXX/blog/[video-slug]-blog.md
```

Also output a separate file for the schema block:
```
output/YYYY-WXX/blog/[video-slug]-schema.json
```

## Output Structure
```
output/YYYY-WXX/blog/[video-slug]-blog.md
├── Meta Data Block (title, slug, description, target page)
├── BLUF (50-word summary)
├── YouTube Embed Placeholder
├── Structured Body (H2/H3 hierarchy, all data preserved)
├── Scars & All Callout
├── FAQ Section (3-5 Q&As)
├── Internal Links (3-5 suggestions)
├── Schema JSON-LD (VideoObject + FAQPage + Article)
└── Pinned Comment Draft

output/YYYY-WXX/blog/[video-slug]-schema.json
└── Standalone schema for direct paste into page head
```

## Example Usage

```
User: /transcript-to-blog
Claude: Give me one of:
  1. YouTube URL
  2. Pasted transcript
  3. Video title + transcript file path

Optional: Target page URL on templetxhomes.net?

User: https://youtube.com/watch?v=xyz — it's my Canyon Creek neighborhood tour

Claude: [Fetches transcript, reads VIDEO-TO-PAGE-MAP.md, generates full blog post with
BLUF, structured body, Scars & All callout, 5 FAQs, internal links to /canyon-creek/
and /investing-in-temple-tx/, VideoObject + FAQPage + Article schema, meta data,
and a pinned comment pushing the Neighborhood Match Guide]

Revisor caught: "approximately 2,400 sq ft" → corrected to "2,387 sq ft" from transcript.
Revisor caught: "charming community" → corrected to "established neighborhood with
mature tree canopy."
```

## Dependencies
- `VIDEO-TO-PAGE-MAP.md` — Video-to-page matching and gap identification
- `reference/SCHEMA-LIBRARY.md` — Schema templates (VideoObject, FAQPage, Article)
- `reference/LEAD-MAGNET-MATRIX.md` — Persona-matched lead magnets for pinned comments
- `research/AEO-DIRECTIVES.md` — Entity consistency and AI citation optimization rules
- `social-media-config.json` — Brand voice, personas, DM keywords
- `/Users/taylordasch_1/open-claw/feedback-log.md` — Content feedback patterns
- Outputs to `output/YYYY-WXX/blog/[slug]/`

## Why This Skill Matters
Every YouTube video Taylor films contains 1,500-3,000 words of unique, data-rich content that currently lives only in video format. AI engines cannot watch videos — they read text. This skill converts every video into a citable, indexable blog post that:
- Gets scraped by ChatGPT, Gemini, Perplexity, and Claude when users ask about Temple TX real estate
- Adds FAQPage + VideoObject schema for rich results
- Creates internal linking opportunities across templetxhomes.net
- Generates a "Scars & All" section that no competitor will replicate (Information Gain)
- Produces a lead magnet hook matched to the video's audience

One video in, one full AEO-optimized blog post out. Every time.
