# Command Center

Date: May 21, 2026.

Status: DRAFT. Taylor approval required before any real-world action.

## Current Read

- Best first move: build demand-led distribution around pages already getting Search Console impressions.
- Highest search opportunity: `/data-center-impact/` with 71 clicks and 7,654 impressions from February 20-May 20, 2026.
- Biggest immediate system debt: stuck registry items and missing related page links for published videos.
- Current week production gap: no counted Week 21 TikTok, GMB, community, long-form, Short, blog, newsletter, BP, or audit outputs beyond the existing content calendar.
- Fresh market proof exists in `market-monitor/`, especially May 14 and May 19 MLS pulls.

## First Action Queue

1. Build the Data Center Impact social proof cluster.
   - Platforms: LinkedIn, GBP, YouTube Short, Temple Insider or Investor Brief split, community post.
   - Page: `https://templetxhomes.net/data-center-impact/`
   - Goal: convert impressions into authority and lead conversations.

2. Build the Temple Market Report investor cluster.
   - Platforms: LinkedIn, BP, Investor Brief, YouTube refresh.
   - Page: `https://templetxhomes.net/investing/temple-tx-market-report/`
   - Gate: no TikTok.

3. Build the BSW Relocation medical buyer cluster.
   - Platforms: GBP, Temple Insider, LinkedIn, YouTube Short.
   - Pages: `/baylor-scott-white-relocation/`, `/match-day-2026-bsw-housing-timeline/`, `/bsw-temple-childcare-daycare-guide/`.

4. Build the Neighborhoods buyer/relocator cluster.
   - Platforms: TikTok property-tour prep only when listing facts exist, Instagram Reel, GBP, Temple Insider.
   - Page: `/neighborhoods/`.

5. Repair the registry/page bridge queue.
   - Map or decide on published videos with missing `related_page_slug`.
   - Fix invalid state decisions in a separate approval-safe queue.

## Use Today

Run:

```bash
python3 scripts/social-os-snapshot.py --out projects/real-estate-social-os-3x/snapshots/latest.md
```

Then pick one source and fill:

```text
templates/source-to-social-packet.md
```

## Stop Condition

Do not mark an asset ready unless the packet includes source proof, platform-native draft, lead path, UTM/source note, dedupe note, and approval gate.
