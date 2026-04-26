# WORKFLOW.md — Social Media Manager Daily + Weekly Rhythm

> Operational playbook for using the SMM CLI + existing Content OS skills. This doc is the "how" — voice and governance rules live in `BRAND_VOICE.md` + `governance/`.

---

## Daily Workflow (~20 min)

**1. Capture ideas as intake (2 min)**

Anywhere you spot a content opportunity — client call, showing, email, comment, market news — drop it into the queue:

```bash
python3 cli.py intake add --source-type comment --audience investor \
  --title "Investor asked why BSW commute matters for rental demand" \
  --body "Recurring question in DMs — worth a short explanation video"
```

Use stdin for longer input:

```bash
cat client-question.txt | python3 cli.py intake add --source-type buyer_question --audience bsw_relocation --title "PGY-1 rent vs buy timing"
```

**2. Generate drafts from ONE core asset (10 min)**

Pick one source (a YouTube upload, a blog, a market update) and run the relevant Claude Code skill:

- YouTube video → `/repurpose` or `/transcript-to-blog`
- Listing → `/deal-of-the-week`
- Market data → `/gmb-post` + `/newsletter`
- Local trend → `/news-hijack`

Skill output lands in `output/YYYY-WXX/...`. Import it as a draft:

```bash
python3 cli.py draft import output/2026-W17/gmb/investor-cash-flow-math-2026-04-20.md \
  --platform gmb \
  --intake intk_xxx
```

**3. Review the approval queue (3 min)**

```bash
python3 cli.py draft list --status needs_review
```

For each draft: read it, check compliance flags, edit if needed, then approve / reject / revise:

```bash
python3 cli.py draft show drft_xxx                                # full detail
python3 cli.py draft edit drft_xxx --cta "DM for the analyzer"    # tweak
python3 cli.py draft approve drft_xxx --note "ship Tuesday AM"    # approve
python3 cli.py draft reject drft_xxx --note "wrong audience"      # reject
python3 cli.py draft revise drft_xxx --note "add 1-rule math"     # back to drafting
```

HARD compliance flags block approve. Fix the copy or pass `--force` if you genuinely want to override (every override is logged in `approval_events`).

**4. Export or schedule approved posts (3 min)**

```bash
python3 cli.py export approved --target csv --platform linkedin
# → exports/2026-04-24-approved-linkedin.csv
```

Then either upload to Meta Business Suite / Postiz / Ayrshare / Buffer, or paste into the platform. Mark posted:

```bash
python3 cli.py draft scheduled drft_xxx --note "queued in Postiz 10am CT"
python3 cli.py draft posted drft_xxx --note "live at https://..."
```

**5. Log insights back into memory (2 min)**

Anything you learned from calls, showings, emails, or market activity → add back as intake:

```bash
python3 cli.py intake add --source-type comment \
  --audience bsw_relocation \
  --title "Ad creative idea from a PGY-2 DM" \
  --body "PGY-2 told me the commute-to-BSW calculator was the thing that got her to book. Build a dedicated tool page."
```

---

## Weekly Workflow (Sunday, ~45 min)

Full rhythm: lives in `governance/SESSION-LOOP.md` + `skills/weekly-retro/` + `skills/weekly-scorecard/`. Summary:

**1. Session Step 0 — inline health checks**

```bash
python3 scripts/freshness-scanner-v2.py
python3 scripts/output-integrity-check.py
python3 scripts/dedupe-checker.py
python3 scripts/next-best-action.py
```

Fix anything red before planning next week.

**2. Pull last week's performance**

Invoke the Claude Code skill:
```
/weekly-analytics-pull
```

Updates `data/performance-ledger.csv` with YouTube + Beehiiv + GSC + FUB pulls. Then rate each piece CRUSH / SOLID / MEH / MISS in the `taylor_rating` column.

**3. Pick next week's core assets (one per lane)**

- 1 investor education topic (→ `/yt-video` for Investing channel, or `/reddit-bp` / `/linkedin-carousel`)
- 1 relocation / local lifestyle topic (→ `/yt-video` for Living channel, or `/tiktok-script`)
- 1 market authority topic (→ `/newsletter` or `/gmb-post`)
- Repurpose ONE prior YouTube video or blog across platforms (→ `/repurpose`)

Each core asset = one `intake` row. Drafts are then generated per platform from that intake.

**4. Check calendar + gaps**

```bash
python3 cli.py calendar week     # this week's draft state + output files
python3 cli.py calendar gaps     # IDEA / DRAFT / REFRESH_DUE from content-registry.csv
python3 cli.py calendar mix      # audience/platform mix vs target
```

Build next week's queue to close gaps. Registry rows in `IDEA` state → create intake + generate drafts. `REFRESH_DUE` pages → schedule an update.

**5. Run weekly retro skill**

```
/weekly-retro
```

Scores the 7 days, computes narrative-arc velocity, flags kill/expand decisions for the coming week.

---

## Ideal Weekly Content Mix (configurable)

Default targets (from user spec; adjust in `smm/calendar.py:DEFAULT_WEEKLY_MIX`):

| Category | Share |
|---|---|
| Investor education | 40% |
| Relocation / local lifestyle | 30% |
| Market authority | 15% |
| Listings / property examples | 10% |
| Personal / BTS | 5% |

Existing Content OS pillar rules (from `social-media-config.json`):
- TikTok: Property Tours, Relocation, Market Data, Only in Texas, BTS, Temple Trap, Deal of the Week
- Newsletter split: Temple Insider (buyers, biweekly Tuesdays) + Investor Brief (investors, biweekly Thursdays)
- **Rotation rule:** Never 2 of the same pillar back-to-back. Algorithm flattens repetitive content.

---

## Platform Cadence Reference

From `social-media-config.json` + SMM-IMPROVEMENT-PLAN.md:

| Platform | Frequency | Best Time (Central) | Notes |
|---|---|---|---|
| TikTok | 5/week | Tue–Fri 2–6 PM | Native filming only, no YT repurposing |
| Instagram Reels | 3–5/week | Tue–Wed 10 AM–2 PM, 5–9 PM | 3-sec hold rate >60% = viral signal. Caption keywords > hashtags in 2026 |
| YouTube Long | 1–2/wk/channel | Thu–Sat 2–4 PM | Publish 2 hrs early |
| YouTube Shorts | As filmed | Flexible | Native Shorts beat TikTok reposts |
| YouTube Community | Weekly per channel | — | Polls, teasers, BTS |
| GMB | Weekly (4/mo) | Weekdays 8–10 AM | Rotation: Market Update / Listing Spotlight / Neighborhood Guide / Expertise Tip |
| LinkedIn | 2–3/wk | Tue–Thu 7–9 AM | Professional relocators + BSW referral partners + out-of-state agents |
| BiggerPockets / Reddit | 3–5/wk | Tue–Wed 10 AM–12 PM | Helpful-answer style, not promo |
| Temple Insider newsletter | Biweekly Tue | — | Buyers, relocators |
| Investor Brief newsletter | Biweekly Thu | — | Investors |
| Facebook (Unique Listings) | Saturday batch | — | 5 listings, scheduled M–F |

---

## Never Publish Without Approval

Hard rule from `AGENTS.md`:

> "No `send_email` or `send_message`. Always `create_draft`. Taylor sends manually. No live API calls without a `--live` flag. Default mode is dry-run or draft."

The CLI enforces this at the boundary: `export` writes a file. Posting is always a deliberate human action.

---

## When to Use What

| You want to… | Use |
|---|---|
| Capture a rough idea | `cli.py intake add` |
| Generate platform copy | Claude Code skill (`/tiktok-script`, `/gmb-post`, …) |
| Stage skill output for approval | `cli.py draft import <path> --platform X` |
| Create a draft from scratch | `cli.py draft new --platform X --body "…"` |
| Check voice/compliance | `cli.py compliance check --path X.md --platform tiktok` |
| See what's waiting for you | `cli.py draft list --status needs_review` |
| Approve a draft | `cli.py draft approve <id>` |
| Export approved posts | `cli.py export approved --target csv` |
| See weekly state | `cli.py calendar week` |
| Find gaps | `cli.py calendar gaps` |
| Pull pending work | Read `TODO.md` (auto-populated by Hermes writer) |
| Weekly retro | `/weekly-retro` Claude skill |
| Refresh hook bank | `/hook-bank` Claude skill |

---

## Stop-the-Line Triggers

Abort a draft and re-plan if you hit any of these:

- **HARD compliance flag** — copy goes back to drafting, not `--force`.
- **Lane mix-up** — investor content on TikTok / lifestyle on Investor Brief.
- **Number you can't cite** — pull from `market_data.json` / `reference/TEMPLE-TX-DATA-VAULT.md` or mark `[needs verification]`.
- **Fort Cavazos slip** — rename to Fort Hood everywhere before shipping.
- **Broker mention** — Taylor is an AGENT.
