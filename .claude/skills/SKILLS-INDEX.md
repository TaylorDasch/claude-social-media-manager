# Skills Index — Content Production Engine

## Quick Reference

### Production Skills (in `skills/` — project root)

| Skill | Trigger | Inputs | Primary Output |
|-------|---------|--------|----------------|
| `/content-calendar` | "plan week", "content calendar" | Week number, priorities | `output/YYYY-WXX/content-calendar.md` |
| `/tiktok-script` | "tiktok script", "tiktok about" | Topic, persona | TikTok script with hooks + DM CTA |
| `/youtube-description` | "youtube description" | Video title, topic | 7-section description + tags |
| `/newsletter` | "newsletter", "investor brief" | Week's content, audience | Beehiiv newsletter draft |
| `/gmb-post` | "gmb post", "daily post" | Day of week, latest content | GBP post with Bible verse |
| `/deal-of-the-week` | "DOTW", "deal of the week" | Property address, MLS data | Full DOTW package (8+ files) |
| `/produce` | "produce", "run pipeline" | Master content piece | 12+ derivative files |
| `/repurpose` | "repurpose", "cross-post" | Published content | Platform-adapted versions |
| `/yt-video` | "new video", "film this" | Topic, channel | Production prep (5 files) |
| `/weekly-scorecard` | "scorecard", "weekly review" | None (auto-scans) | Scorecard with gaps + wins |
| `/hook-bank` | "hooks", "hook bank" | Pillar, count | 10-15 hooks per pillar |
| `/transcript-to-blog` | "yt to blog", "transcript" | .SRT file, video URL | AEO blog + schema JSON |
| `/community-post` | "community post" | Topic | 3 post variations |
| `/linkedin-carousel` | "linkedin", "carousel" | Topic (investor/BSW only) | 5-7 slide carousel outline |
| `/audit` | "audit", "score this page" | URL or page slug | 100-point AEO audit |

### New Skills (in `.claude/skills/`)

| Skill | Trigger | Inputs | Primary Output |
|-------|---------|--------|----------------|
| `srt-corrector` | "fix srt", "correct srt" | .SRT file path | Corrected .SRT + corrections log |
| `youtube-metadata` | "youtube metadata", "yt metadata" | Topic, pillar, persona | 3 titles + description + tags + pinned comment |
| `thumbnail-brief` | "thumbnail brief", "thumb idea" | Video title, emotion | Composition brief + color spec |
| `production-bible` | "production bible", "full production plan" | Topic, channel, video type | Master doc + shot list + overlays list |
| `shorts-extraction` | "extract shorts", "find clips" | Transcript, video title | 3-5 clip extractions with hooks + captions |
| `schema-generator` | "generate schema", "json-ld" | Page content/URL, page type | Complete JSON-LD package |
| `deal-analysis` | "deal analysis", "run the numbers" | Address, price, rent | PITI + cash flow + cap rate + verdict |
| `rent-vs-buy` | "rent vs buy", "true cost" | Home price, rent, zip | 2/3/5-year comparison table |
| `video-overlay-generator` | "video overlay", "create graphic" | Graphic type, data | 1920x1080 branded PNG |
| `keyword-audit` | "keyword audit", "transcript keywords" | .SRT file, target keywords | Density report + gap analysis |
| `content-freshness-check` | "freshness check", "stale pages" | None or specific URL | Freshness report with update queue |
| `competitor-gap` | "competitor gap", "content gap" | Competitor list (optional) | Gap-fill ideas ranked by impact |
| `internal-link-audit` | "internal link audit", "orphan pages" | None (auto-scans) | Link graph report + recommendations |
| `spark-ads-tracker` | "spark ads", "ads review" | Weekly ad data from Taylor | Performance report + boost recommendations |

## Weekly Workflow Mapping

| Day | Primary Skills Used |
|-----|-------------------|
| **Monday** | `/content-calendar`, `content-freshness-check` |
| **Tuesday (Film Day)** | `production-bible`, `video-overlay-generator` |
| **Wednesday** | `/repurpose`, `shorts-extraction` |
| **Thursday (Edit Day)** | `srt-corrector` → `/transcript-to-blog`, `youtube-metadata`, `thumbnail-brief` |
| **Friday (Publish)** | `schema-generator`, `/gmb-post` |
| **Saturday (YouTube Publishes)** | `keyword-audit`, `/community-post` |
| **Sunday (Measurement)** | `spark-ads-tracker`, `/weekly-scorecard`, `competitor-gap` (monthly) |

## Skill Chain (Common Sequences)

```
Film Day:       production-bible → [film] → srt-corrector
Edit Day:       srt-corrector → transcript-to-blog → schema-generator → youtube-metadata → thumbnail-brief
Publish Day:    shorts-extraction → /tiktok-script → /gmb-post
Measurement:    spark-ads-tracker → /weekly-scorecard
Monthly Audit:  content-freshness-check → internal-link-audit → competitor-gap
```

## Skills Requiring External Data

| Skill | What's Needed | Where to Get It |
|-------|--------------|----------------|
| `deal-analysis` | Current interest rates | Mortgage rate sites (verify weekly) |
| `rent-vs-buy` | Current BAH rates | DoD BAH calculator |
| `spark-ads-tracker` | Ad performance data | TikTok Ads Manager (Taylor provides) |
| `competitor-gap` | Competitor channel/site list | Taylor provides initial list |
| `content-freshness-check` | Current MLS stats | MLS pull (Taylor provides) |
| `keyword-audit` | Target keyword list | Auto-generated per pillar or Taylor provides |
