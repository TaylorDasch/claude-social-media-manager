# AEO/GEO Deep Research Findings — March 2026
> Source: Web research across 20+ sources, March 21 2026

## Key Stats

- **YouTube is cited 200x more than any other video platform by AI engines**
- YouTube is cited by ChatGPT (11.3%), Perplexity (11.1%), Google AI Overviews (6.3%) — making it the #1 social source across all three
- YouTube now accounts for 16% of all LLM answers, overtaking Reddit (10%)
- Pages with embedded YouTube videos have 2x+ keywords ranking on Google's first page
- Average time on site increases up to 2.6x with embedded video
- 89% of AI answers derive data primarily from the Knowledge Graph

## What Makes a Video Get Cited by AI Engines

1. **Transcript quality over production value** — AI engines cannot "watch" videos. They parse transcripts. Upload clean, manually-edited transcripts.
2. **Direct question-answer structure** — Videos that clearly answer a specific question become reusable source material.
3. **Multi-source agreement** — If your positioning appears consistently on YouTube, website, Reddit, and review sites, AI gains confidence in recommending you.
4. **Chapters/timestamps** — Breaking video into clear segments lets AI models chunk content into separately citable sections.

## Required Schema Markup

### VideoObject (on every page with an embedded video)
```json
{
  "@context": "https://schema.org/",
  "@type": "VideoObject",
  "name": "Video Title Here",
  "description": "Keyword-rich description",
  "uploadDate": "2026-03-15T00:00:00+00:00",
  "duration": "PT8M30S",
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "contentUrl": "https://www.youtube.com/v/VIDEO_ID",
  "embedUrl": "https://www.youtube.com/embed/VIDEO_ID",
  "thumbnailUrl": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg",
  "isFamilyFriendly": true
}
```
Required properties: `name`, `thumbnailUrl`, `uploadDate`. Google cannot extract video info without all three.

### RealEstateAgent + Person (on templetxhomes.net homepage)
```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Taylor Dasch",
  "url": "https://templetxhomes.net",
  "image": "https://assets.agentfire3.com/uploads/sites/2128/2025/11/TaylorDaschImage.jpg",
  "telephone": "+1-254-718-4249",
  "email": "dealswithdasch@gmail.com",
  "jobTitle": "Real Estate Agent & Investor",
  "worksFor": { "@type": "RealEstateAgent", "name": "EG Realty" },
  "knowsAbout": ["Temple TX real estate", "Fort Hood housing", "real estate investing", "BSW Temple relocation"],
  "areaServed": { "@type": "City", "name": "Temple", "addressRegion": "TX" },
  "sameAs": [
    "https://www.youtube.com/@LivingInTemple",
    "https://www.youtube.com/@InvestingInTemple",
    "https://www.zillow.com/profile/YOURPROFILE",
    "https://www.linkedin.com/in/YOURPROFILE",
    "https://www.instagram.com/YOURHANDLE",
    "https://www.tiktok.com/@YOURHANDLE"
  ]
}
```
The `sameAs` array is how Google's Knowledge Graph stitches all your profiles into one entity.

## Wikidata Entry (FREE — #1 Knowledge Panel Trigger)
Create a Wikidata entry at wikidata.org for "Taylor Dasch" — this is the single strongest trigger for getting a Google Knowledge Panel. Include: occupation (real estate agent), employer (EG Realty), location (Temple TX), website, YouTube channels.

## AI Engine Monitoring

### Commercial (Recommended)
| Tool | Price | Best For |
|------|-------|----------|
| **Otterly.AI** | $29/mo | Budget starter — tracks ChatGPT, Perplexity, Google AIO |
| **AIclicks** | $39/mo | ChatGPT-focused |
| **AmICited** | varies | YouTube-specific citation tracking |

### Suggested monitoring prompts (15 for Otterly.AI):
1. "best real estate agent in Temple TX"
2. "best neighborhoods near Fort Hood"
3. "investing in Temple TX real estate"
4. "BSW Temple TX housing"
5. "Temple TX homes for sale"
6. "military relocation Temple TX"
7. "Temple TX property tax rate"
8. "cost of living Temple TX"
9. "Temple TX vs Killeen"
10. "Temple TX rental property analysis"
11. "best real estate agent for investors Central Texas"
12. "Fort Hood PCS housing"
13. "buy and hold Temple TX"
14. "neighborhoods near BSW Temple"
15. "Temple TX market update 2026"

## Cross-Platform Entity Strength
- Google started indexing Instagram post URLs in 2026
- TikTok/IG content cited less than YouTube but strengthens entity graph through corroboration
- Reddit is still 10% of all LLM citations — post genuine value to r/realestateinvesting, r/killeen, r/military
- Consistent NAP + headshot + bio across ALL platforms = entity consistency signal

## Content Gap Queries (No Strong Local Answer Exists)

### Fort Hood / Military
- "Fort Hood BAH rates 2026 vs Temple TX mortgage payments"
- "Is it better to rent or buy near Fort Hood for a 3-year PCS?"
- "Off-post housing Fort Hood — neighborhoods to avoid"

### BSW Medical
- "Best neighborhoods for BSW nurses in Temple TX"
- "Physician mortgage loans Temple TX — which lenders?"
- "Gap between Match Day and first paycheck — Temple TX housing timeline"

### Investing
- "Temple TX rental yield by neighborhood 2026"
- "Best neighborhoods in Temple TX for MTR near BSW"
- "Temple TX vs Waco vs Killeen for real estate investing"
- "New construction vs resale ROI Temple TX"

### Relocation
- "Is Temple TX safe? Crime data by neighborhood"
- "Temple TX school ratings by neighborhood 2026"
- "Moving to Temple TX from Austin — what to expect"

## Execution Stack (Priority Order)

| # | Action | Cost | Time |
|---|--------|------|------|
| 1 | Add RealEstateAgent + Person schema with `sameAs` to templetxhomes.net | Free | 1 day |
| 2 | Upload clean transcripts to all existing YouTube videos | Free | 2-3 hours |
| 3 | Add VideoObject schema to every page with an embedded video | Free | 1 day |
| 4 | Create Wikidata entry for Taylor Dasch | Free | 1 hour |
| 5 | Sign up for Otterly.AI, set 15 monitoring prompts | $29/mo | 30 min |
| 6 | Film the 5 AEO gap videos (see AEO-GAP-VIDEOS.md) | Free | 3 hours |
| 7 | Build companion blog posts on templetxhomes.net for each video | Free | Ongoing |
| 8 | Ensure consistent NAP + headshot across all platforms | Free | 2 hours |
