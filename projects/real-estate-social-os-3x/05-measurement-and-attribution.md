# Measurement And Attribution

The system measures whether social creates discovery, trust, and lead movement.

## Required Tracking Fields

Every packet should name:

- `source_asset`
- `audience_lane`
- `platform`
- `campaign_slug`
- `cta_keyword`
- `lead_magnet`
- `target_url`
- `utm_source`
- `utm_medium`
- `utm_campaign`
- `fub_source_note`
- `approval_status`

## UTM Format

```text
https://templetxhomes.net/[page]/?utm_source=[platform]&utm_medium=social&utm_campaign=[campaign-slug]
```

Examples:

```text
https://templetxhomes.net/data-center-impact/?utm_source=linkedin&utm_medium=social&utm_campaign=2026-05-data-center-impact
https://templetxhomes.net/baylor-scott-white-relocation/?utm_source=gbp&utm_medium=local&utm_campaign=2026-05-bsw-relocation
```

## FUB Source Notes

Use short, copy-pasteable notes:

```text
Source: Social OS | Platform: [platform] | Campaign: [campaign_slug] | CTA: [keyword] | Page: [target_url]
```

No FUB write happens without approval. These notes are draft handoff material.

## Performance Tiers

| Tier | Signal | Action |
| --- | --- | --- |
| CRUSH | Produces lead conversation, booked call, strong saves/shares, or meaningful page traffic. | Build 3 derivatives and consider page refresh. |
| SOLID | Gets engagement or improves discovery but no lead movement yet. | Keep in rotation and test a stronger hook. |
| MEH | Low engagement and no lead movement. | Rewrite hook or change platform. |
| MISS | Wrong audience, unsupported claims, or poor channel fit. | Archive or rebuild from source. |

## Weekly Scorecard

Each Friday:

1. Run local snapshot.
2. Pull Search Console top pages and query/page pairs.
3. Pull platform metrics where available.
4. Update `data/performance-ledger.csv` if Taylor has ratings or platform metrics.
5. Decide: double down, refresh, merge, archive, or leave alone.

## Lead Attribution Questions

Ask these for each asset:

- Did the asset point to a specific page?
- Did it have a DM keyword or reply path?
- Did the lead source survive into FUB?
- Did it strengthen a page that already has search demand?
- Did it create a reusable proof point for AI/local search?

## What Not To Measure Alone

- Views without retention.
- Followers without qualified conversation.
- Posts published without lead path.
- Clicks without landing page fit.
- Volume without registry hygiene.
