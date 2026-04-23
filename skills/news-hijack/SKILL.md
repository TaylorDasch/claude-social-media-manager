---
name: news-hijack
description: News-Hijack Event Loop. Polls curated RSS feeds every 15 min, scores headlines against Temple/BSW/rates/military/real-estate keywords, drafts YouTube topic + TikTok hook + newsletter teaser per qualifying item, runs each draft through voice-check.py, pushes top 3 to Taylor's Telegram inside the 30-min hijack window. Use when Taylor says "news hijack", "hijack queue", "what can I hijack today", "claim hijack", "run news poll". Component #4 of Hermes SM MVP.
---

## Governance

Read `governance/QUALITY-GATES.md` before generating content. QUALITY-GATES overrides any quality check in this skill. Also consult:
- `governance/FACT-HANDLING.md` — source provenance + conflict resolution
- `governance/DEFINITION-OF-DONE.md` — when each content type is done
- `governance/MULTI-PASS-SYSTEM.md` — 5-pass pipeline integration points

# News-Hijack Event Loop

Trigger: Taylor asks for hijack angles, claims/skips items, or checks the pending queue.

## Architecture

Stdlib-only Python script. No pip installs.

```
~/.hermes/scripts/news-hijack.py          # engine
~/claude-social-media-manager/data/
  hijack-feeds.json                       # feed config + keyword weights (Taylor-editable)
  hijack-queue.json                       # scored items + drafts + status
  hijack-claimed.csv                      # Taylor-claimed log
~/.hermes/data/news-hijack-seen.json      # URL-hash dedup cache
~/.hermes/logs/news-hijack.log            # cron output
```

Data flow: poll -> score -> enqueue (if score >= threshold AND age < max_age_hours)
-> draft (Claude Sonnet 4.6) -> voice-check.py subprocess -> push-telegram -> claim/skip.

## Commands

| Command | Purpose |
|---------|---------|
| `news-hijack.py poll [--dry-run]` | Fetch all feeds, parse RSS, dedupe, score new items, enqueue |
| `news-hijack.py draft [--limit N]` | Draft top N un-drafted items (sort score desc). LLM + voice-check |
| `news-hijack.py push-telegram [--dry-run] [--top N]` | Send top N drafted items to Telegram |
| `news-hijack.py claim --id N [--platform yt\|tiktok\|newsletter]` | Log claimed to CSV |
| `news-hijack.py skip --id N` | Mark skipped |
| `news-hijack.py status` | Queue counts + oldest pending age |
| `news-hijack.py clean [--older-than-days 7]` | Drop stale claimed/skipped items |

## Feed editing (Taylor)

`~/claude-social-media-manager/data/hijack-feeds.json` is the single source of truth.
Edit freely — script reloads every run.

Fields:
- `feeds[]` — `{name, url, pillar, weight}`. `pillar` = one of
  `bsw | rates | local_re | local_news | military`. `weight` (float) multiplies the score.
- `scoring_keywords{}` — lowercase key -> integer weight. A keyword match adds its
  weight to the pre-multiplier score.
- `threshold` — minimum final score to enqueue (default 3.0).
- `max_age_hours` — drop items older than this (default 12h).
- `pillar_to_newsletter{}` — routes to `investor_brief` or `temple_insider`.
- `pillar_to_tiktok_audience{}` — always `buyer` (TikTok = buyers-only rule).

Use Google News RSS (`https://news.google.com/rss/search?q=<URL-encoded query>`)
for any source without a native feed.

## Scoring formula

```
score = sum(keyword_weight for each matched keyword in title) * feed_weight
```

Scoring runs on the cleaned title ONLY (Google News descriptions are source-attribution HTML
which poisons matching — e.g. "Temple Daily Telegram" would match every "temple" keyword).
The `" - <Source>"` suffix Google News appends to titles is stripped before matching.

Enqueue if `score >= threshold` AND `(now - pub_date) < max_age_hours`.

## Integration with Voice Guardian

Every draft is piped through `~/.hermes/scripts/voice-check.py --json --platform ... --audience ...`
(Haiku-backed, reads `voice-rubric.json`). Per-platform audiences:

- YT: `youtube_investing` for `bsw|rates` pillars (audience=investor), else `youtube_living` (audience=buyer)
- TikTok: `tiktok` + audience=buyer (TikTok-buyers-only rule enforced)
- Newsletter: `investor_brief` (audience=investor) for bsw/rates; `temple_insider` (audience=buyer) otherwise

Any draft scoring `< 70` on any platform sets `needs_rewrite: true` on the item. Telegram push
still includes the item but prepends `[NEEDS REWRITE]` so Taylor sees the voice debt upfront.

Issue details (`voice_issues.{yt,tiktok,newsletter}`) are stored on the queue item so Taylor
(or Claude on ask) can see exactly WHY a draft failed — banned phrases, hallucinated numbers, no creative element, wrong audience, etc.

## Cost estimate

- Draft: Claude Sonnet 4.6 ~$3/M input + $15/M output. A drafted item = ~800 input tokens + ~250 output tokens = ~$0.006/item.
- Voice-check: Claude Haiku 4.5 ~$1/M input + $5/M output. 3 calls per item @ ~600 in + ~200 out each = ~$0.004/item.
- Total: ~$0.01 per drafted item.
- Cadence: 3 drafted pushes/day x 3 platforms = $0.03/day = **~$1/mo** draft cost.
  (Original estimate of $3/mo was conservative; real runs at current feed volume land lower.)
- Poll cost: $0 (RSS only, no LLM).

## Cron (document only — do NOT install)

```
# Poll every 15 min
*/15 * * * * cd ~ && python3 ~/.hermes/scripts/news-hijack.py poll >> ~/.hermes/logs/news-hijack.log 2>&1

# Draft + push three times daily (8am, noon, 5pm)
0 8,12,17 * * * cd ~ && python3 ~/.hermes/scripts/news-hijack.py draft --limit 3 && python3 ~/.hermes/scripts/news-hijack.py push-telegram >> ~/.hermes/logs/news-hijack.log 2>&1

# Weekly cleanup Sunday 11pm
0 23 * * 0 cd ~ && python3 ~/.hermes/scripts/news-hijack.py clean --older-than-days 7 >> ~/.hermes/logs/news-hijack.log 2>&1
```

## Voice / content rules honored

- TikTok audience forced to `buyer` (CLAUDE.md rule — TikTok = buyers/relocators ONLY).
- Newsletter routing enforces Investor Brief vs Temple Insider split per pillar.
- YouTube channel split: "Investing in Temple" for BSW/rates; "Living in Temple" for local/military/relocation.
- Drafter system prompt bans generic RE language and broker terminology.
- No investor-targeted paid ad content — the hijack pipeline drafts organic content only.

## Rollback

```
rm -rf ~/.hermes/scripts/news-hijack.py \
       ~/.hermes/data/news-hijack-seen.json \
       ~/claude-social-media-manager/skills/news-hijack \
       ~/claude-social-media-manager/data/hijack-feeds.json \
       ~/claude-social-media-manager/data/hijack-queue.json \
       ~/claude-social-media-manager/data/hijack-claimed.csv
```

(Remove the cron lines above from crontab if installed.)

## Known limitations

- Google News RSS occasionally shifts its URL scheme or adds redirects. If `poll` returns zero items across every feed, check a feed URL manually.
- `pub_date` parsing falls back to "undated" for unusual date formats — undated items always pass the age filter.
- Voice-check is blocking (60s timeout per call x 3 per item). Drafting 3 items takes ~30-90s.
- Rate limiting: 0.3s sleep between Telegram sends. Bot token is shared with other Hermes tools — coordinate if you add a lot of pushers.
