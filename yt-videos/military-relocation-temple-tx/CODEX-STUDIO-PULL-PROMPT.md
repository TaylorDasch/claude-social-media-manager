# Codex Computer prompt — YouTube Studio analytics pull (video 39Y6UpSFqu0)

Paste the block below into Codex (Computer/browser mode). Run it once NOW with `START_DATE = 2026-07-14, END_DATE = 2026-07-16` (pre-reset baseline), and again on **July 25** with `START_DATE = 2026-07-17, END_DATE = 2026-07-23` (day-9 decision pull).

---

Use the browser. I'm already logged into YouTube Studio as the Living in Temple, TX channel.

1. Go to https://studio.youtube.com → Content → find the video "PCS to Fort Hood (2026): 6 Towns Compared by BAH & Commute" (ID 39Y6UpSFqu0) → click its Analytics icon.
2. Set the date range picker (top right) to Custom: START_DATE through END_DATE.
3. Open the **Reach** tab and record exactly these numbers:
   - Impressions
   - Impressions click-through rate (%)
   - Views
   - Unique viewers
   - In "Impressions and how they led to watch time" note total impressions and watch time from impressions.
4. Still in Reach, open the **Traffic source types** card → "See more" → record the table rows for: Browse features, Suggested videos, YouTube search, Channel pages, External, Direct/unknown — with Impressions, Impressions CTR, Views, and Average view duration per row (some sources show no impressions; record what's shown).
5. In the same expanded report, switch the traffic source dimension to **YouTube search terms** and record every search term with its views.
6. Open the **Engagement** tab and record: End screen element click rate (%), end screen clicks, and card teaser click rate/clicks if shown.
7. Open the **Audience** tab and record: Returning viewers, New viewers, and Subscribers vs non-subscribers split if shown.
8. Do NOT change anything — read-only. Do not touch the video details, thumbnail, or comments.
9. Output everything as one markdown table block titled with the date range, and save it to a file named `studio-pull-<START_DATE>-to-<END_DATE>.md` in `~/claude-social-media-manager/yt-videos/military-relocation-temple-tx/` (or paste it back in chat if you can't write files).

---

## What the numbers feed (decision gates from the growth brief)
- Day-9 gate (pull on Jul 25): ≥1,000 impressions AND CTR <4% → title switch (challenger picked by impression mix: Browse+Suggested ≥60% → "PCS to Fort Hood? The $1,695 Mistake Most Soldiers Make in 2026"; Search ≥40% → "Fort Hood Housing 2026: What $1,695 BAH Buys in All 6 Towns"). CTR 4–6% → hold. >6% → lock. <1,000 impressions → don't touch the title; feed Suggested instead.
- Day-14 gate: if the 0:24–1:22 retention drop persists ≥25 pts at ≥150 views → Studio trim of 0:24–1:22.
