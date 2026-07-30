# TikTok Saturday Slot Test — opened 2026-07-29

**Hypothesis:** Saturday 6:00 PM CT outperforms the current Monday 6:00 PM default.

**Baseline (n=74, 2025–26, median plays):** Sat **752** · Fri 613 · Tue 575 · Sun 486 · Wed 418 ·
Thu 400 · **Mon 350**. All-day median 447.

**Cadence:** every other Saturday, 6:00 PM CT (23:00Z).

| Date | Clip | Post ID | Status | Plays @14d |
|---|---|---|---|---|
| 2026-08-01 | T2 · Day 365 warranty | `cms666xek03x5p50yhybnyh7i` | QUEUE | |
| 2026-08-15 | T3 · the tax trap *(planned)* | | open | |
| 2026-08-29 | T4 or T5 | | open | |
| 2026-09-12 | | | open | |
| 2026-09-26 | | | open | |

**Control group** — Mondays already queued, same window:

| Date | Clip | Plays @14d |
|---|---|---|
| 2026-08-03 | Belton home sales | |
| 2026-08-10 | Morgan's Point | |
| 2026-08-17 | Three Creeks | |
| 2026-08-24 | Dawson Ranch | |

**Read the result ~2026-09-26**, after 4 Saturday cycles. Compare Saturday median vs the Monday
control median over the same period. Re-scrape with:

```
apify clockworks/tiktok-profile-scraper → profiles:["taylordasch"], resultsPerPage:110
```

**Do not call it early.** Four data points against a 350-median baseline is thin; a single viral
outlier on either side would swamp it. Judge on median, never mean.

**Confound to watch:** the Saturday slots are all Stylecraft clips and the Monday control is all
Belton neighborhood content. If Saturday wins, topic is a live alternative explanation — the
clean follow-up test is a Belton clip on a Saturday.
