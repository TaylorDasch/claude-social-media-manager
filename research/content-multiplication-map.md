# Content Multiplication Map — 1 Video = 15 Assets
## Integrated with ClawdBot Automation (April 2026)
## Source: Perplexity Research + ClawdBot workflow mapping

---

## The Framework

Every long-form YouTube video generates 15 assets. Estimated time with automation: 60-90 minutes per video batch.

```
MASTER ASSET: Long-form YouTube Video (10-20 min)
|
+-- IMMEDIATE (Day of publish)
|   +-- 1. YouTube Short #1 — Hook clip (best 30-45 sec moment)
|   +-- 2. YouTube Short #2 — Money moment / data reveal
|   +-- 3. TikTok — Same Short, native upload (NO watermark cross-post)
|   +-- 4. Instagram Reel — Same Short, text overlay for silent viewing
|
+-- TEXT DERIVATIVES (Same day or next day)
|   +-- 5. Newsletter section — 150-word summary for Investor Brief or Temple Insider
|   +-- 6. BiggerPockets forum post — Key investor insight, link to blog (NOT video)
|   +-- 7. GMB post — 1 paragraph + thumbnail image + video link
|   +-- 8. Blog post — 800-1,200 word AEO-formatted transcript post on templetxhomes.net
|
+-- SOCIAL MICRO-CONTENT (Days 2-3)
|   +-- 9. YouTube Community post — Poll or stat graphic from video
|   +-- 10. Facebook group post — Bell County / Temple local groups
|   +-- 11. LinkedIn post — Professional network, investor angle if applicable
|
+-- LONG-TAIL (Week 2)
    +-- 12. YouTube Short #3 — "Still getting questions about this" follow-up
    +-- 13. Newsletter deep-dive — Expanded version in next biweekly send
    +-- 14. Website FAQ update — Add 2 Q&As from video comments to matching page
    +-- 15. YouTube Community post #2 — Behind-the-scenes or follow-up data
```

---

## Weekly Workflow (Mapped to Existing Automation)

### TUESDAY (Sacred Film Day)
- Film video
- Upload to YouTube (schedule for Wednesday 8am CT publish)
- Feed video to Opus Clip for auto-clipping overnight
- ClawdBot cron: Content Flywheel Monday calendar already queues the week

### WEDNESDAY (Publish + Distribute)
- Video goes live at 8am CT
- Review Opus Clip output, select best 2-3 Shorts
- Upload Short #1 to YouTube Shorts + TikTok (native) + IG Reel
- Post GMB post with video thumbnail (ClawdBot can draft via /gmb-post)
- Write BP forum teaser if investor topic (5 min, ClawdBot drafts)
- Newsletter section written (ClawdBot /newsletter skill)

### THURSDAY (Text Derivatives)
- Upload Short #2 to YouTube Shorts + TikTok
- Blog post generated from transcript (ClawdBot /transcript-to-blog)
- Blog post published to templetxhomes.net
- YouTube Community post with poll or stat

### FRIDAY (Social + Queue)
- LinkedIn post if applicable
- Facebook group post
- Schedule remaining Shorts for following Mon-Tue
- ClawdBot cron: Friday Scorecard runs at 5pm, auto-tallies week's output

### FOLLOWING WEEK
- Short #3 posted Monday/Tuesday
- Newsletter deep-dive in next biweekly send
- FAQ updates added to matching page
- Community post #2

---

## ClawdBot Skills That Handle Each Asset

| Asset | Skill | Automation Level |
|-------|-------|-----------------|
| Blog post from transcript | /transcript-to-blog | Full draft (Taylor reviews) |
| Newsletter section | /newsletter | Full draft |
| GMB post | /gmb-post | Full draft |
| Community post | /community-post | Full draft |
| YouTube description | /youtube-description | Full draft |
| TikTok script (if filming original) | /tiktok-script | Full draft |
| Short clips | Opus Clip (external) | Auto-generated, Taylor selects |
| Content registry update | /produce pipeline | Auto-registers all assets |
| Weekly scorecard | /weekly-scorecard | Auto-tallies Friday 5pm |

---

## Key Rules

1. **Shorts go up 24-48 hours AFTER long-form** — gives long-form a head start in algorithm
2. **TikTok is ALWAYS native upload** — never cross-post with YouTube watermark
3. **BP posts link to BLOG, not video** — BP penalizes video links
4. **GMB posts include newsletter link, not homepage** — per Quality Gate 8
5. **Every asset gets registered in content-registry.csv** — /produce handles this
6. **Investor content stays on Investing channel + Investor Brief** — never mix into buyer content
7. **TikTok is buyers/relocators ONLY** — no investor content on TikTok (Taylor's rule)
