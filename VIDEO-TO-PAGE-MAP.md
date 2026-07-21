# Video-to-Page Mapping — AEO/GEO Optimization
> Generated: 2026-03-21
> Audited: 2026-07-19
> Goal: Embed the right YouTube video on each website page to create bidirectional authority signals that AI engines cite

## Strategy
Every website page should have at least ONE relevant YouTube video embedded. Every YouTube video should link back to its matching page. This creates a citation loop: AI engines see structured page content + video transcript + cross-links = strong topical authority.

## Priority: Pages That NEED a Video Embedded (High AEO Impact)

### Tier 1 — These pages exist, matching videos exist, EMBED NOW

| Website Page | YouTube Video to Embed | Channel |
|---|---|---|
| `/best-neighborhoods-temple-tx/` | "Don't Invest in Temple TX Without Watching This Neighborhood Breakdown" | Investing |
| `/fort-hood-relocation/` | "Where to Live Near Fort Hood: 6 Cities Compared (2026)" - published as `39Y6UpSFqu0`; packaging refresh pending | Living |
| `/fort-hood-off-post-housing/` | "Where to Live Near Fort Hood: 6 Cities Compared (2026)" - published as `39Y6UpSFqu0`; primary embed target | Living |
| `/neighborhoods-near-bsw-by-commute/` | "Baylor Scott & White Temple TX — Where Doctors & Nurses Actually Live" | Living |
| `/cost-of-living-temple-tx/` | "Living in Temple TX: The Unfiltered Guide (Cost of Living, Pros & Cons, & Tour)" | Living |
| `/investing-in-temple-tx-2026-playbook/` | "Step-by-Step: How to Invest in Real Estate in Temple, TX (2025 Guide)" | Investing |
| `/investing/out-of-state-investor-execution-playbook/` | "Investing in Temple TX from Out of State: Why This Market (Part 1 of 5)" | Investing |
| `/investing/property-management-guide/` | "Don't Hire a Property Manager in Temple TX Until You Watch This" | Investing |
| `/temple-vs-killeen/` | "Killeen vs Temple TX: What $350K Buys You in 2026" - published as `30qMJW6SRBw`; replace primary embed when the July pillar publishes | Living |
| `/temple-vs-belton/` | Temple vs Belton pillar - publish and video ID pending | Living |
| `/living-in-belton-tx/` | "Is Three Creeks the Best Neighborhood in Belton TX?" | Living |
| `/investing/tax-strategy/` | FILM: "Bell County Property Taxes: The Formula to Calculate Your Payment" | Living |
| `/bell-county-tax-protest-guide/` | FILM: "Bell County Tax Protest" (TikTok script exists, expand to long-form) | Living |
| `/mud-vs-pid-taxes-temple-belton-tx/` | "Windmill Farms Deep Dive: Calculating MUD Taxes and HOAs" (FILM THIS) | Living |
| `/sell-house-by-owner-temple-tx/` | "The FSBO Strategy That Actually Works in 2026" | Living |
| `/temple-tx-market-update/` | "Temple, Texas Market Forecast: The Numbers Don’t Lie" (`pph_QEB7E-E`); replace primary embed with the July Day-60 update after it publishes | Living |
| `/best-areas-long-term-rentals-temple-belton/` | "Temple TX Long Term Rental — $150K — Buy & Hold Strategy Breakdown" | Investing |
| `/assumable-loans-temple-tx/` | "No Credit Check, No Banks, 2.5% Interest Rate Belton, TX" | Living |
| `/deal-analyzer/` | FILM: "How to Analyze a Temple TX Buy-and-Hold (Live Spreadsheet)" | Investing |
| `/retiring-in-temple-tx/` | FILM: "Cost of Living Breakdown: Temple TX vs Austin (Line-Item Data)" | Living |

### Tier 2 — Page exists, additional matching video needed (FILM THESE)

| Website Page | Video Needed | Priority |
|---|---|---|
| `/bell-county-homestead-exemption-guide/` | "How to File Your Bell County Homestead Exemption (Step-by-Step)" | HIGH — desk filmable, screen share |
| `/how-to-choose-a-real-estate-agent-temple-tx/` | "5 Questions to Ask Before Hiring a Temple TX Agent" | MEDIUM |
| `/best-restaurants-temple-tx/` | "Best Places to Eat in Temple TX (Local's Guide)" | LOW — needs b-roll |
| `/things-to-do-temple-tx/` | "Is Temple TX Boring? Here's What There Actually Is to Do" | LOW — needs b-roll |
| `/temple-vs-waco/` | "Temple vs Waco: Cost of Living Data Compared" | HIGH — desk filmable |
| `/temple-vs-round-rock/` | "Temple vs Round Rock: Where Your Dollar Goes Further" | HIGH — desk filmable |
| `/investing/neighborhoods/` | "Top 3 Neighborhoods for Investors in Temple TX (2026 Data)" | HIGH — desk filmable |
| `/buy-before-first-day-of-residency-bsw/` | "BSW Residents: You Can Buy a House Before Your First Day" | HIGH — desk filmable |
| `/fort-hood-off-post-housing/` | "What $300K-$350K Buys Near Fort Hood: 4 Cities Compared" | HIGH — production bible ready |

### Tier 3 — Video exists, NO matching page yet (BUILD THESE PAGES)

| YouTube Video | Page to Build | Why |
|---|---|---|
| "5 Fatal Mistakes Out-of-State Investors Make in Temple TX" | `/investing/out-of-state-mistakes/` | High search intent, strong AEO query |
| "Are Foreclosure Auctions REALLY a Good Deal in Temple TX?" | `/investing/foreclosure-auctions-temple-tx/` | Niche investor query AI engines get asked |
| "I Analyzed Both Markets So You Don't Have To: Temple or Killeen?" | `/temple-vs-killeen-investing/` | Investor comparison; keep separate from the relocation page |
| "Buying a House for $75k! Full BRRRR Breakdown" | `/investing/brrrr-strategy-temple-tx/` | BiggerPockets audience search term |
| "Austin vs Temple: Where the REAL Cash Flow Is" | `/temple-vs-austin-investing/` | Major geo-arbitrage search query |
| "$45k Instant Equity! Temple TX Pre-Foreclosure Tour" | `/investing/pre-foreclosures-temple-tx/` | High intent investor query |

### Planned pairing — companion page built locally; neither asset is public yet

| Planned YouTube Video | Planned Page | Release gate |
|---|---|---|
| "What Makes a Good House Hack? 5 Tests Before You Buy" | `/house-hacking-temple-tx/` | `Investing in Temple` evergreen five-test package for a first-investment viewer. The canonical page packet exists locally; keep the pair outside live embed/health checks until the page resolves publicly and the video has a public ID. |
| "Temple & Belton Housing Market: The 60-Day Listing Test" | `/temple-tx-market-update/` | `Living in Temple` buyer/relocation update. Package is `READY_TO_FILM`; the July 20 explicit Status/Property-Type gate is cleared. Refresh the stale page data, then add the public video ID and complete VideoObject schema only after Taylor approves, the video is filmed, and it is published. |

## Implementation Notes
- Every embedded video should use VideoObject schema markup
- YouTube description for each video should link back to the matching page
- Each page with a video should have a FAQ section derived from the video's key questions (FAQPage schema)
- Update `AEO-DIRECTIVES.md` with this mapping as the canonical reference
