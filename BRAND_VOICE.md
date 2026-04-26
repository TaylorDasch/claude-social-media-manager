# BRAND_VOICE.md — Taylor Dasch / EG Realty

> Canonical human-readable voice doc. Source of truth for banned / approved language. Compliance module (`smm/compliance.py`) reads `data/voice-rubric.json` at runtime so updates propagate automatically.

## Voice Principles

- **Data-first.** Lead with numbers, not narratives. Specific beats generic.
- **Honest.** Include real negatives (foundation, noise, drainage, traffic) when they exist — that builds trust.
- **Short.** No disclaimers, no reverse-confirmations, no hedging, no fluff.
- **Analyst, not salesperson.** Taylor has $27M+ in transactions and 100+ personal investment transactions — sounds like an investor-analyst, not an order-taker.
- **One creative/unexpected element per piece** (a data angle, a contrarian take, a surprising comparison, a niche hook). Playing it safe is the mistake.
- **Email voice**: lead with attachment or data, one insight, easy CTA.
- **No generic RE language** — never "dream home," "perfect neighborhood," "nestled," "premier," "coveted," "charming."

## Entity Rules (HARD)

| Field | Exact Value |
|---|---|
| Name | Taylor Dasch |
| Brokerage | EG Realty |
| Title | Real Estate Agent (NOT broker) |
| Phone | 254-718-4249 |
| Email | dealswithdasch@gmail.com |
| Website | templetxhomes.net |
| Location | Temple, TX |
| Military base | Fort Hood (NEVER "Fort Cavazos") |

Every public-facing long-form asset (YouTube script, blog, page) must include the declaration "Taylor Dasch with EG Realty" in the first 3 sentences (script) or first paragraph (blog). SMS and DMs are exempt.

## Banned Phrases (HARD — blocks approval)

From `data/voice-rubric.json` + `governance/QUALITY-GATES.md`:

| Banned | Use Instead |
|---|---|
| turnkey | buy-and-hold |
| dream home | the right property |
| white glove | (remove entirely) |
| nestled | (name the actual location) |
| charming | cute / old home charm |
| stunning | beautiful / very nice |
| sought-after | desirable / where everybody wants to be |
| boasts | has / you get |
| utilize | use |
| comprehensive | full / complete / in-depth |
| furthermore / moreover | and / the other thing is / so |
| leverage (as verb) | use |
| unparalleled | (state actual comparative) |
| amenities (generic) | (name actual things) |
| in today's market | (name month/year) |
| vibrant community | (name what makes it vibrant) |
| hidden gem | (describe what's actually there) |
| Fort Cavazos | Fort Hood |
| welcome home | (remove entirely) |
| perfect home / perfect neighborhood | (name specifics instead) |
| coveted / premier | (concrete comparative) |
| inviting / welcoming | (concrete detail) |
| luxurious touches | (name the touches) |
| immaculate | (measurable condition) |
| stunning views | (what do you see from the window) |
| don't miss / act now / hurry / opportunity of a lifetime | (remove) |
| must see / must-see | (remove) |
| entertainer's delight | (remove) |
| move-in ready paradise | (remove) |

**Banned hooks/openers (HARD):**
- "Let me tell you about…"
- "In this article we'll explore…"
- "In conclusion…"

## Guaranteed-Return Language (HARD — compliance risk)

Rephrase or remove:
- "guaranteed return" → "based on current comps, the projected return is…"
- "guaranteed appreciation" → "historically Temple has averaged…"
- "risk-free" → (remove — no such thing)
- "can't lose" / "always appreciates" → (remove)

## Fair-Housing + Steering (SOFT — review context)

Flagged patterns that should be rephrased with data, not demographic fit:
- "perfect for families / kids / professionals / young [anything]"
- "best neighborhood for [demographic]"
- "family-friendly neighborhood"
- "safest part of town"

Prefer: "Walkable to [specific school X], [specific park Y], [specific employer Z]." Let the buyer self-select.

## School + Tax Claims (SOFT — need verification language)

- School quality claims → must include **"verify by address"** or **"check boundaries"**.
- Tax rate mentions → must include **"verify current rate"** or **"varies by …"**.

Why: Texas school boundaries and tax rates change. Stating "great schools" without the disclaimer creates liability and erodes trust when a buyer finds the boundary moved.

## Platform Audience Rules

| Platform | Audience | Never |
|---|---|---|
| **TikTok** | Buyers / relocators ONLY | Investor content, YouTube repurposes, desk scripts |
| **YouTube — Living in Temple** | Buyers, relocators, military PCS | Investor ROI analysis |
| **YouTube — Investing in Temple** | Investors (in-state + out-of-state) | Generic lifestyle / relocation |
| **Temple Insider newsletter** (biweekly Tue) | Buyers, relocators | Investor ROI — that's Investor Brief's lane |
| **Investor Brief newsletter** (biweekly Thu) | Investors | Generic lifestyle |
| **Instagram** | 70% buyers / 30% investors | Salesy hype, "act now" |
| **LinkedIn** | Professional relocators, BSW referral partners (via Matt Levant lender channel), out-of-state agents for referrals | Generic agent posts ("Just Listed!" without data) |
| **GMB** | Local searchers (Temple + Bell County) | Generic lifestyle language — always real data |
| **Facebook (Unique Listings group)** | Broad local | Saturday 5-listing batch |
| **Email** | 1:1 or segment | Reverse-confirmations, disclaimers, over-explanation |

**Ad rule:** Ad spend targets BSW medical (#1) and military (#2) ONLY. **No investor ads.**

**BSW rule:** Outreach goes ONLY via the lender channel (Matt Levant, Acre Mortgage). Stark Law blocks direct gatekeeper outreach. Peggy Peters + all BSW-employed staff cannot distribute outside resources.

**First-of-month rule:** 1st of every month = dedicated expired-listings lead-gen block. Do not schedule competing outreach.

## Hook Library

Canonical hook formula (source: `feedback_youtube_hook_formula`):

> **[Specific number or contradiction] + [Who this is for] + [Delayed payoff]**

Templates that work:

- "If [specific audience] is looking at [specific market], here's what I'd look at first."
- "The mistake I keep seeing [audience] make in [market]…"
- "Most people look at [metric]. I'd look at [better metric]."
- "If [character/persona] lived in [city], this would be their [home/neighborhood/strategy]."
- "Before you buy in [city/neighborhood], look at this first."
- "What does [$PRICE] get you as a rental investor in Temple, TX?"
- "[Contradiction]: this neighborhood scores X but is priced like Y."

Rotate hooks via `data/hook-bank.json`. `/hook-bank` skill refreshes any pillar with <5 fresh entries.

## CTA Library

| Audience | CTA |
|---|---|
| Investor | "DM if you want the Temple deal-analyzer template." / "Reply with the zip and I'll send the rent-comp pull." |
| BSW relocation | "If you're PGY-1–PGY-5, Matt Levant at Acre Mortgage handles physician-loan terms — I'll intro." |
| Fort Hood | "If you're PCS-ing to Fort Hood and want a BAH-matched rental or househack plan, reply and I'll send the map." |
| Local buyer | "templetxhomes.net/[neighborhood-slug] has the full neighborhood breakdown." |
| Seller | "Reply with address and I'll pull a 3-comp CMA today." |
| Agent referral | "25% referral fee on closed. Happy to return the favor." |

**Chatbot rule:** Soft-offer booking / email capture when user signals uncertainty. Don't wait 6 messages deep.

## Data Points (Cite When Relevant)

Always prefer `market_data.json` + `reference/TEMPLE-TX-DATA-VAULT.md` over memory. If the number isn't verified there, flag it `[needs verification]` rather than inventing.

Hot stats with source dates:

| Metric | Current Value | Source | Date |
|---|---|---|---|
| Temple median home price | $247,450–$288,000 | MLS | see data vault |
| Bell County effective tax (non-homestead) | ~2.366% | BCAD | 2026 |
| City of Temple tax rate | $0.6999 / $100 valuation | City | 2025 |
| BSW Temple employment base | 8,800+ | BSW HR | 2025 |
| Fort Hood BAH E-6 w/ dep | $1,920 / month tax-free | DFAS | verify current |
| 76502 Power Zip rank | 753/1000 (top 5%) | Niche/NAR data | 2025 |
| Active MLS inventory (Bell Co) | 500+ listings, ~6-month supply | MLS | Apr 2026 |
| Average DOM | 83 days | MLS | Apr 2026 |
| BSW PGY-1 stipend | $70,993 / year | BSW public posting | 2025 |

## Examples

### Good (ship this)

> "Temple's affordability is real, but the tax rate can kill a lazy rental analysis. A $255K house at 2.18% effective property tax needs stronger rent support than most out-of-state buyers expect. Before I'd call it a good buy-and-hold, I'd want rent comps, insurance quotes, HOA rules, and tenant demand by zip code. Verify current rate — Bell County reassesses annually. — Taylor Dasch with EG Realty."

Why it works: real numbers, honest negative, investor-audience language, entity declaration, tax disclaimer, no banned phrases.

### Bad (blocks on compliance)

> "Discover your dream home in the vibrant community of Temple, Texas! This charming property is nestled in a desirable neighborhood and offers something for everyone. Don't miss it!"

Why it fails: 6 HARD banned phrases (dream home, vibrant community, charming, nestled, don't miss, desirable), no data, no entity declaration, generic audience.

### Good (LinkedIn, professional relocator)

> "Temple's Power Zip (76502) has a 5,101-unit housing deficit and 24.1% population growth. Median is $247K–$288K; 3-bed rents are $1,650. If you're moving for the BSW system, the 76502–76504 corridor sits inside the 8-minute commute radius. Verify commute, zoning, and neighborhood fit before deciding. Taylor Dasch with EG Realty."

### Good (GMB post, data-forward)

> "Bell County active inventory: 500+ listings, ~6-month supply, 83-day DOM (MLS, April 2026). Temple itself is tighter — 76502/76504 absorb faster. Buyers: the seasonal inflection is mid-summer; sellers: price calibration matters more than marketing right now. — Taylor Dasch with EG Realty."

## What the Compliance Module Actually Checks

Implemented in `smm/compliance.py`:

| Rule | Severity | What it catches |
|---|---|---|
| `banned_phrase` | HARD | Any phrase from the banned list + voice-rubric |
| `guaranteed_return` | HARD | Explicit guarantee language |
| `broker_rule` | HARD | "Taylor is a broker" etc. |
| `tiktok_investor_leak` | HARD (platform=tiktok) | DSCR, cap rate, cash-on-cash, rental comp, BRRRR, etc. |
| `fair_housing_steering` | SOFT | Demographic-targeting phrasing |
| `school_claim_unverified` | SOFT | "great schools" without verify-by-address cue |
| `tax_claim_unverified` | SOFT | Tax rate mention without verify-current cue |
| `entity_missing` | SOFT | Long-form public asset without "Taylor Dasch with EG Realty" |

**HARD = blocks approval** unless `draft approve --force`. **SOFT = warns, ships.**

Run manually: `python3 cli.py compliance check --platform linkedin --path some-draft.md`
