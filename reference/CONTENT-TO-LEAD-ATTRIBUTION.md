# CONTENT-TO-LEAD ATTRIBUTION FRAMEWORK
## Standardizes how leads are tracked back to the content that generated them
## Reference for all skills that build CTAs, forms, or tracking links

---

## FUB SOURCE TAGS (Use These Consistently)

Every lead entering Follow Up Boss gets ONE primary source tag:

| Tag | Source |
|-----|--------|
| `youtube_living` | Living in Temple channel |
| `youtube_investing` | Investing in Temple channel |
| `youtube_short` | YouTube Shorts (either channel) |
| `website_organic` | Found via Google/AI search (no specific page identified) |
| `website_[page-slug]` | Specific page (e.g., `website_lake-pointe`, `website_investing-playbook`) |
| `biggerpockets` | BiggerPockets forum or profile |
| `tiktok` | TikTok (DM, comment, or profile link) |
| `newsletter` | Email newsletter click-through |
| `gmb` | Google Business Profile |
| `reddit` | Reddit thread or DM |
| `referral_[name]` | Personal referral (e.g., `referral_john-smith`) |
| `podcast_[show]` | Podcast guest appearance |
| `linkedin` | LinkedIn post or article |
| `direct` | Phone call, walk-in, or text with no digital trail |
| `ai_engine` | Lead says they found you via ChatGPT, Perplexity, or Google AI Overview |

---

## UTM PARAMETER STRUCTURE

Every outbound link from content should include UTMs:

```
?utm_source=[platform]&utm_medium=[format]&utm_campaign=[topic]&utm_content=[specific-piece]
```

**Examples:**
- YouTube description link: `?utm_source=youtube&utm_medium=video&utm_campaign=deal-of-the-week&utm_content=dotw-2026-03-21`
- TikTok bio link: `?utm_source=tiktok&utm_medium=bio&utm_campaign=general`
- Newsletter CTA: `?utm_source=newsletter&utm_medium=email&utm_campaign=weekly-digest&utm_content=2026-w12`
- BP forum reply: `?utm_source=biggerpockets&utm_medium=forum&utm_campaign=investor-content`

---

## HIDDEN FORM FIELDS (Every Lead Capture Form)

Every form on templetxhomes.net should include these hidden fields:

| Field | Value | Purpose |
|-------|-------|---------|
| `source_url` | Auto-populate with current page URL | Know which page converted |
| `asset_name` | Name of the lead magnet that triggered the form | Track which magnets convert |
| `persona_rail` | investor / bsw / military / luxury / general | Route to correct FUB action plan |
| `capture_date` | Auto-populate with current date | Attribution timing |

---

## WEEKLY TRACKING QUESTIONS (Every Friday During Pipeline Review)

1. How many leads entered FUB this week by source tag?
2. Which page/video generated the most form fills this week?
3. Which YouTube video had the highest "link in description" clicks? (Check YouTube Studio)
4. Any leads mention a specific video or page during intake call?
5. What's the source breakdown of deals currently in pipeline?
6. Did any AI engine monitoring alerts fire this week? (Otterly.AI)

---

## MONTHLY METRICS TO TRACK

| Metric | Where to Find It |
|--------|-----------------|
| YouTube subscribers (both channels) | YouTube Studio |
| YouTube views by video (top 10) | YouTube Studio → Analytics |
| Website sessions by page (top 10) | GA4 |
| Form fills by source_url | FUB + GA4 Events |
| FUB lead count by source tag | FUB Smart Lists |
| Deals closed by original source | FUB → Closed tag |
| Revenue by content source | Manual calculation from FUB |
| AEO citation rate | Otterly.AI weekly report |
| Non-branded search queries | Google Search Console |

---

## ATTRIBUTION RULES

- If a lead mentions a video → tag with the specific video name
- If a lead came through a page form → tag with page slug
- If a lead found you on BP but also watched YouTube → primary: `biggerpockets`, secondary: `youtube_investing`
- If a lead says "AI recommended you" or "ChatGPT told me about you" → tag: `ai_engine` (this is gold — track every one)
- **Always ask during first call:** "How did you find me?" and log the exact answer in FUB notes
- If they can't remember → tag: `direct`

---

## CONTENT ROI FORMULA

```
Content ROI = (Revenue from content-sourced deals) / (Time spent creating content + Tool costs)
```

**Current baseline (March 2026):** 35%+ of revenue from content sources
**Target (June 2026):** 50%+ of revenue from content sources

Track the 35% → 50% progression monthly. This is the number that proves the system works.
