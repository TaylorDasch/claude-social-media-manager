# Evidence

## Primary sources

- `/Users/taylordasch_1/market-monitor/whole-market-with-status-2026-07-20.csv`
- `/Users/taylordasch_1/market-monitor/05-14-2026-mls-templebelton.csv`
- relevant April–July point-in-time exports in `/Users/taylordasch_1/market-monitor/`
- `/Users/taylordasch_1/market-monitor/temple-belton-historical-data/*.csv`
- May video transcript: `/Users/taylordasch_1/claude-video/mentor-memory/crawled-videos/pph_QEB7E-E/transcript.en-en.vtt`
- Studio export: `/Users/taylordasch_1/real-estate-youtube/cockpit/studio-drops/content-videos_2026-04-03_2026-07-02.csv`

## Reproducible artifact

`/Users/taylordasch_1/claude-social-media-manager/yt-videos/temple-belton-market-update-july-2026/analysis/analyze_market.py`

## Accepted facts

- Current Temple + Belton Residential sample with `Status = Active`: 870 rows / 869 unique addresses; $299,440 median ask; 69.5 median DOM.
- Current reduction share: 486/870 = 55.9%.
- DOM reduction staircase: 28/204 = 13.7% at 0–30, 84/185 = 45.4% at 31–60, 76/114 = 66.7% at 61–90, and 298/367 = 81.2% at 91+.
- Current-versus-May continuity evidence: count -2.1%, median active ask -3.4%, median DOM -2.1%, and reduction share +1.8 percentage points. May status was inferred, so this is not a precise apples-to-apples comparison.
- Latest qualifying closes, June 21–July 20: n=200 at or above $25,000; $278,670 median close; median DOM 50; 99.76% of final list; 97.01% of original list; 103/200 = 51.5% below final list.
- Builder-identified current active: 222/870 = 25.5%; median DOM 110 vs 64 non-builder.
- YTD 2026 vs 2025: sales -0.9%, median close -1.4%, DOM +3 days.

## Explicit-field Active audit

- The current source includes explicit `Status` and `PropertyType` fields.
- The analysis filters `PropertyType = Residential` and `Status = Active`, then post-filters the multi-city export to exact Temple and Belton rows.
- The resulting current sample is 870 rows / 869 unique addresses.
- The May source does not provide equally explicit status evidence; May comparisons are retained only as continuity evidence.
- Conclusion: the current Active/Residential filming gate is cleared. This does not convert the May comparison into a precise apples-to-apples trend.

## Rejected/limited sources

- Every blank-close-date row is not active; doing so blends status blocks.
- The earlier field-incomplete export is superseded for current Active claims by the explicit-field July 20 export.
- Generated W29 snapshot/public pulse counts and months supply are invalid for this video.
- June 13 open counts are unsafe near the Matrix row cap.
- `BuilderName` and `YearBuilt` are unsafe builder classifiers.
- Median price movement is not repeat-sales appreciation/depreciation.
- Close/list ratios do not include seller credits.

## Prior-video evidence

- May update public URL: `https://www.youtube.com/watch?v=pph_QEB7E-E`.
- Studio through 2026-07-02: 1,714 impressions, 4.32% CTR, about 5:01 AVD, 38.8% viewed, zero subscribers.
- Same export channel CTR: 5.27%.
- May opening structure was strong; packaging was crowded and the first likely retention leak came after the hook when the video paused for method/setup.
- May transcript used the wrong brokerage; corrected public identity is `Taylor Dasch with EG Realty`.
