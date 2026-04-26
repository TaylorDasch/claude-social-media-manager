# SKILL.md Descriptions — Applied 2026-04-24

**21 skills** were missing YAML frontmatter entirely (not just blank `description:`). Claude Code's Skill tool could not auto-surface them. All 21 were fixed this session; all 30 now have a `name:` + `description:` frontmatter.

## What Was Applied

Each of the 21 files below was prepended with:
```yaml
---
name: <slug>
description: <see list>
---
```

Body content was not modified. Rollback: `cd ~/claude-social-media-manager && git checkout -- skills/`.

## Descriptions Written

| Skill | Description (trimmed) |
|---|---|
| audit | Score any page, post, blog, or video script against Taylor's AEO + voice + data-integrity rules. Use when user says 'audit this page', 'score this', 'AEO check', 'how optimized is this?' |
| community-post | Draft YouTube Community-tab posts (polls, teasers, BTS, CTA) for the Living in Temple and Investing in Temple channels. Use when user says 'community post', 'YT community tab', 'poll for my channel'. |
| content-calendar | Build next week's content calendar (Mon-Fri + optional weekend) from the registry, freshness scanner, filming day queue, and gap analysis. Use when user says 'content calendar', 'plan the week'. |
| deal-of-the-week | Turn a Temple/Bell County property into a full Deal of the Week package — AgentFire page, short-form script, social captions, community post, schema markup. Use when user says 'deal of the week', 'DOTW', 'this week's deal'. |
| gmb-post | Draft Google Business Profile posts using the 4-week rotation (Market Update / Listing Spotlight / Neighborhood Guide / Expertise Tip) with local keywords. Use when user says 'GMB post', 'GBP rotation'. |
| hook-bank | Generate fresh hooks for any pillar where the hook-bank.json pool is stale or under 5 entries. Follows Taylor's canonical formula. Use when user says 'hooks', 'hook bank', 'opening lines'. |
| instagram-reel | Write an Instagram Reel script optimized for 2026 algorithm — 3-second hold rate over 60 percent, caption keywords over hashtags, DM-shareability. Use when user says 'Reel', 'IG Reel', 'Instagram script'. |
| linkedin-carousel | Draft LinkedIn carousel posts (8-10 slides) for professional relocators, BSW referral partners (via Matt Levant lender channel), and out-of-state agents. Use when user says 'LinkedIn carousel', 'carousel post'. |
| newsletter | Draft biweekly Temple Insider (buyers, Tue) or Investor Brief (investors, Thu) newsletter issues for Beehiiv — never mix audiences. Use when user says 'newsletter', 'Temple Insider', 'Investor Brief'. |
| produce | Post-production orchestrator for a filmed YouTube video — title, description, tags, community post, pinned comment, Shorts clip angles, thumbnail brief, blog derivative. Use when user says 'produce video'. |
| reddit-bp | Draft Reddit + BiggerPockets forum replies in helpful-answer style (not promo). Follows Reddit Responsible Builder Policy — no cross-posting. Use when user says 'Reddit reply', 'BP forum reply'. |
| repurpose | Turn one YouTube video, blog, listing, or market update into a multi-platform content pack — LinkedIn, FB, IG, Reels, Shorts, Community, GBP, quote cards, email. Use when user says 'repurpose', 'content multiplication'. |
| thumbnail-brief | Generate a thumbnail brief (or an actual Canva design via Canva MCP) for a YouTube video — text overlay, expression asset, contrast check, A/B pair. Use when user says 'thumbnail', 'thumb brief'. |
| tiktok-performance | Pull TikTok performance signals and trending local hashtags (via TrendsMCP when connected) and cross-reference against content-registry.csv for gaps. Use when user says 'TikTok performance', 'TikTok trends'. |
| tiktok-script | Generate an on-site prep sheet for filming a TikTok — buyer/relocator lane only, native vertical, 7-second visual-change rhythm, 3-act hook/tour/CTA. Use when user says 'TikTok script', 'TikTok prep'. |
| transcript-to-blog | Convert a YouTube or Omi transcript into an AEO-formatted blog post — Question-Hook → Answer-First H2 structure, FAQPage schema, embedded video, Yoast SEO block. |
| unique-listings | Build the Saturday 5-listing batch for the Unique Listings Facebook group — scheduled M-F, broad local audience. Use when user says 'unique listings', 'Saturday batch'. |
| weekly-analytics-pull | Sunday auto-consolidation skill — pulls YouTube + Beehiiv + GSC + FUB + Google Maps rank data into a single weekly performance snapshot. Use when user says 'weekly analytics', 'Sunday pull'. |
| weekly-scorecard | Friday 5pm weekly content scorecard — rates the week CRUSH / SOLID / MEH / MISS against YouTube, Beehiiv, GSC, FUB, and GMB signals. |
| youtube-description | Write a YouTube video description using the 7-section template — hook, value promise, timestamps, CTAs, links, social handles, credits. |
| yt-video | Full YouTube video workflow — script (hook + 3-act + 7-segment tour), filming prep, description, tags, community post, thumbnail brief. Use when user says 'YT video', 'full video'. |

## Taylor Review

These descriptions were written from knowledge of each skill's body + Taylor's voice/lane rules. They are **starter text** — if any description doesn't trigger the right way in practice, edit the frontmatter directly. The `name:` field matches the folder slug in all 21 cases.

Nothing else in any SKILL.md was modified. Bodies, triggers sections, and prose are all untouched.
