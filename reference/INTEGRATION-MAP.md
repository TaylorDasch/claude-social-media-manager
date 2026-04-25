# Cross-Project Integration Map

> How the Content OS connects to other ClawdBot projects.
> Skills should check these integration points when they need data from outside this project.

## MCP Tools Available

These MCP tools are registered at user scope and available in any Claude Code session:

### TC Module (Transaction Data)
- **`tc_person_full_context`** — Get everything about a person: contacts.db + FUB profile + texts + notes + active deals + DocuSign envelopes + deadlines. Use when DOTW, newsletter, or any skill references a specific buyer/seller/agent.
- **`tc_list_deals`** — List all active transactions. Use to find current deals for DOTW content.
- **`tc_get_deal`** — Full deal details (property, contacts, dates, tasks, docs). Use for deal-specific content.
- **`tc_briefing`** — Daily briefing with risk reports. Content calendar skill can reference this for timely topics.

### FUB (CRM Data)
- **`fub_search_leads`** — Search Follow Up Boss contacts. Use for audience research, lead attribution.
- **`fub_get_lead`** — Full contact details by FUB ID.
- **`fub_get_notes`** — Contact notes for conversation context.

### Router (Cross-Project Data)
- **`router_market_data`** — Market intelligence from real-estate-command-center/reports/: daily briefing, agent rankings, hot subdivisions, equity analysis, competitive landscape. Use for data-heavy content.
- **`router_listing_status`** — Active listings from listing-domination-os with checklists and data sheets. Use for listing content pipeline.
- **`router_page_status`** — Page build queue and shipped pages. Use for content-to-page alignment.
- **`router_video_ideas`** — Brand context + video formulas + data vault for generating video concepts.
- **`router_side_income_pipeline`** — AI side income status (not for RE content, but for Taylor's awareness).

### Omi (Conversation Context)
- **`omi_recent_conversations`** — What Taylor talked about recently. Use for content ideas grounded in real conversations.
- **`omi_get_action_items`** — Action items extracted from Omi conversations. Some may be content-related.
- **`omi_get_field_mode`** — Taylor's current mode (DESK/DRIVING/SHOWING/CLOSING/LISTING). Adjust content urgency accordingly.

### YouTube
- **`youtube_list_videos`** — Recent video catalog. Use for repurpose tracking, scorecard, video-to-page map.
- **`youtube_get_video_stats`** — View count, likes, comments. Use for performance ledger updates.

### Beehiiv (Newsletter)
- **`beehiiv_list_posts`** — Published newsletter issues. Use for avoiding topic duplication.
- **`beehiiv_newsletter_stats`** — Open rates, click rates. Use for weekly scorecard.

---

## Integration Patterns

### Deal of the Week (DOTW) — TC Integration
Instead of asking Taylor for all deal info manually:
1. Call `tc_list_deals` → find interesting active deals or recently closed deals
2. Call `tc_get_deal <id>` → pull address, price, beds/baths, financing, dates
3. Call `router_market_data --report hot` → pull comparable neighborhood data
4. Pre-populate the DOTW template, ask Taylor only for: condition, estimated rent, "would you buy it?"

### Listing Content — Listing Domination OS Integration
When a new listing goes active:
1. Call `router_listing_status --listing [name]` → get checklist + data sheet + MLS description
2. Use data sheet for: address, price, beds/baths, features, neighborhood context
3. Auto-generate: social media launch posts (per listing-domination-os content matrix), video prep sheet, thumbnail brief
4. Track in content-registry.csv with source: `listing-domination-os`

### Market Content — Command Center Integration
For any market data content (blog, newsletter, social):
1. Call `router_market_data --report briefing` → daily market summary
2. Call `router_market_data --report hot` → hot subdivisions for neighborhood content
3. Call `router_market_data --report rankings` → agent rankings for competitive content
4. Cross-reference with TEMPLE-TX-DATA-VAULT.md for historical context

### Content Calendar — Morning Briefing Integration
The Monday morning cron (`skills/clawdbot-content-flywheel/monday-calendar.py`) should:
1. Pull this week's content targets from `/content-calendar` output
2. Cross-reference with active listings (new listing = content trigger)
3. Cross-reference with deal deadlines (closing = Just Sold content trigger)
4. Surface in the morning briefing Telegram message

### Video-to-Page Pipeline
When a video is published:
1. Check `VIDEO-TO-PAGE-MAP.md` — does a matching page exist?
2. If yes → embed video into the page (call `router_page_status` to find the page)
3. If no → queue a blog post via `/transcript-to-blog`
4. Track in content-registry.csv

---

## Data Flow Summary

```
TC Module (deals) ──────→ DOTW / Newsletter / Social posts
                  ──────→ Calendar deadlines → content triggers

Listing Domination OS ──→ Social launch sequence
                     ──→ Video prep sheets
                     ──→ Thumbnail briefs

Command Center ─────────→ Market content (blog, newsletter, social)
                     ──→ Data vault refresh triggers

YouTube API ────────────→ Performance tracking
                     ──→ Repurpose pipeline (transcript → blog)
                     ──→ Video-to-page mapping

Omi Conversations ──────→ Content ideas from real conversations
                     ──→ Action items that become content tasks

FUB (CRM) ─────────────→ Lead attribution tracking
                     ──→ Audience research for persona targeting
```
