# Quality Gates — Global Enforcement Layer

> **Every skill inherits these gates.** No skill may override or skip them.
> If a skill's SKILL.md contradicts this file, this file wins.
> Last updated: 2026-04-13

## How This Works

Before delivering ANY output to Taylor, Claude runs these checks silently. If all pass, output ships. If any HARD gate fails, output is blocked and the failure is reported. If a SOFT gate fails, output ships with a warning.

---

## GATE 1: Banned Language (HARD)

**Never use these words/phrases in any output:**

| Banned | Replacement |
|--------|-------------|
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
| turnkey investors | buy-and-hold investors |
| welcome home | (remove entirely) |

**Also banned in hooks/openers:**
- "Let me tell you about..."
- "Hidden gem"
- "In this article we'll explore..."
- "In conclusion..."

**Check method:** Case-insensitive string scan of full output. Zero tolerance.

---

## GATE 2: Entity Consistency (HARD)

Every piece of content that represents Taylor must use these exact strings:

| Field | Exact Value |
|-------|-------------|
| Name | Taylor Dasch |
| Brokerage | EG Realty |
| Title | Real Estate Agent (NOT broker) |
| Phone | 254-718-4249 |
| Email | dealswithdasch@gmail.com |
| Website | templetxhomes.net |
| Headshot URL | `https://assets.agentfire3.com/uploads/sites/2128/2025/11/TaylorDaschImage.jpg` |
| Location | Temple, TX (NOT Temple, Texas in entity declarations) |
| Fort Hood | Fort Hood (NOT Fort Cavazos) |

**Entity declaration** (required in YouTube scripts, blog posts, and page content):
> "Taylor Dasch with EG Realty" — must appear in first 3 sentences of scripts, first paragraph of blogs.

---

## GATE 3: Data Integrity (HARD)

1. **Every number must have a source.** If the source is TEMPLE-TX-DATA-VAULT.md, acceptable. If calculated, show the math. If estimated, mark `[ESTIMATED]` explicitly.
2. **Never hallucinate math.** Financial calculations (cap rate, cash-on-cash, DSCR, PITI) must be computed, not guessed.
3. **No rounded approximations when exact data exists.** "$96,000" not "about $100K." "$247,500 median" not "around $250K."
4. **Date-stamp volatile data.** Any stat that changes quarterly or faster must include the source date: "Bell County median $247K (MLS, March 2026)."
5. **Minimum data density:** 3+ specific data points per content piece. Blog posts: 5+. Deal breakdowns: 10+.

---

## GATE 4: Scars and All (HARD for applicable types)

**Applicable to:** Deal of the Week, neighborhood tours, blog posts, newsletter deal autopsy, page builds, video scripts.

**Not applicable to:** GMB posts, community posts, TikTok scripts under 30s, social captions.

**Rule:** Every applicable piece must include at least ONE honest negative. Foundation risk, noise, crime stats, boring nightlife, HOA issues, drainage, old pipes — whatever is real.

**Pattern:** State negative plainly → Don't minimize → Pivot to upside or alternative.

**Check method:** Scan for a section/sentence that contains a genuine downside. Generic "no investment is risk-free" does NOT count.

---

## GATE 5: CTA Fit (HARD)

Every content piece must end with a call to action that matches the **persona** and **platform**.

**Persona → Lead Magnet mapping** (from LEAD-MAGNET-MATRIX.md):

| Persona | Lead Magnet | DM Keywords |
|---------|-------------|-------------|
| Investor | Deal Analyzer Spreadsheet | SPREADSHEET, DEALS, ANALYZER |
| Military | BAH Housing Guide | BAH, PCS, RELOCATE, GUIDE |
| BSW Medical | Zero-Down Physician Loan Guide | MATCHED, BSW, DOCTOR, RESIDENT |
| Luxury | Luxury Acreage Due Diligence Checklist | ACREAGE, LUXURY |
| General | Temple TX Relocation Guide | TEMPLE, RELOCATE, GUIDE, TOUR |

**Platform → CTA format:**

| Platform | CTA Format |
|----------|-----------|
| TikTok | DM keyword (never fully answer in video) |
| YouTube Long | Verbal CTA at ~70% + description links + pinned comment |
| YouTube Short | "Comment [KEYWORD]" or "Link in bio" |
| Blog | Inline CTA + bottom CTA with lead magnet |
| Newsletter | Reply CTA or specific next action |
| GMB | Newsletter link or specific page link (never homepage) |
| BP/Reddit | Soft — no direct pitch, offer help via DM |
| LinkedIn | Comment + profile link |

---

## GATE 6: Schema Requirements (SOFT — warn if missing)

| Content Type | Required Schema |
|-------------|----------------|
| Blog post | Article + FAQPage |
| Deal of the Week | Article + FAQPage + VideoObject (if video) |
| Page build | RealEstateAgent + FAQPage + Article + BreadcrumbList |
| Video transcript blog | VideoObject + FAQPage + Article |

Schema must be valid JSON-LD. `dateModified` must be present and current. Templates in `reference/SCHEMA-LIBRARY.md`.

---

## GATE 7: Internal Linking (SOFT — warn if missing)

- Blog posts: 3-5 internal links to templetxhomes.net pages minimum
- Page builds: 5+ internal links + 5 hidden link slots
- Newsletter: 1+ link to specific page (not homepage)
- YouTube description: matching page URL from VIDEO-TO-PAGE-MAP.md

---

## GATE 8: Platform Formatting (HARD)

| Platform | Rule |
|----------|------|
| TikTok | Hook ≤3 seconds verbal, total ≤60 seconds, 3-5 hashtags (3-tier), DM keyword CTA |
| YouTube Long | 7-section description, entity declaration, timestamps if >3 min |
| YouTube Short | Title includes "Temple TX" + keyword |
| GMB/GBP | 4-week rotation (Market Update / Listing Spotlight / Neighborhood Guide / Expertise Tip), ≤300 words, entity declaration (Taylor Dasch + EG Realty + Temple Texas), 2+ citable data points, specific page link (NO homepage), AI query target documented, weekday 8-10 AM |
| BP | NO video links (blog links only), data-heavy, personal experience |
| Reddit | 200-400 words, no self-promotion in Month 1-2 |
| Instagram Reels | Keyword-dense caption (150-300 words micro-blog), 3-5 hashtags max, no TikTok watermarks, DM keyword + link-in-bio CTA |
| Blog | BLUF ≤50 words, H2s as questions, meta title <60 chars, meta desc <155 chars |
| Newsletter | INVESTOR ONLY for Investor Brief, BUYER ONLY for Temple Insider |

---

## GATE 9: Freshness Check (SOFT — warn if stale)

Before using any data point, check its age:

| Data Type | Max Age | Source |
|-----------|---------|--------|
| Median home price | 90 days | TEMPLE-TX-DATA-VAULT.md |
| BAH rates | 365 days (updates Jan 1) | TEMPLE-TX-DATA-VAULT.md |
| Tax rates | 365 days | TEMPLE-TX-DATA-VAULT.md |
| Active inventory | 30 days | MLS pull |
| DOM average | 30 days | MLS pull |
| BSW employee count | 180 days | TEMPLE-TX-DATA-VAULT.md |
| Fort Hood personnel | 180 days | TEMPLE-TX-DATA-VAULT.md |
| Population | 365 days | Census/estimate |
| Builder incentives | 30 days | Direct verification required |
| Rental rates | 90 days | MLS/Rentometer |

If data exceeds max age, mark it `[VERIFY — last confirmed YYYY-MM-DD]` in output.

---

## GATE 10: Output Completeness (HARD)

Every skill defines its required output files in DEFINITION-OF-DONE.md. If a skill run produces fewer files than required, the run is marked INCOMPLETE and a warning is generated.

**Check method:** Compare actual output files against the expected manifest for that skill.

---

## GATE 11: No Auto-Send (HARD)

- Emails: DRAFT only (gmail_create_draft, never send)
- Social posts: Saved to files, never posted
- Nothing external without Taylor's explicit approval

---

## GATE 12: Pillar Rotation (SOFT — warn on violation)

TikTok/Reels: Never 2 of the same content pillar in a row. Check the last 3 entries in content-registry.csv before generating.

Five pillars: Property Tours, Relocation/Military/Medical, Market Data, Lifestyle/Only in Texas, BTS.

---

## GATE 13: Deduplication (SOFT — warn on match)

Before generating any hook, title, or H1:
1. Check `data/content-registry.csv` for similar titles (same target query or >70% word overlap)
2. Check `data/hook-bank.json` for similar hooks
3. If match found within 30 days, warn and suggest alternative angle

---

## GATE 14: TikTok Native Content (HARD)

**TikTok content must be original property tours filmed on-site with iPhone + gimbal.**

- Never repurpose YouTube content into TikTok
- Never generate desk/green-screen TikTok scripts
- TikTok output format = Tour Prep Sheet (talking points, not full scripts)
- No investor content on TikTok — buyers/relocators only
- Every tour stop must include a buyer value-add (financial or lifestyle benefit)

**Check method:** If content_type is TikTok, verify it uses the property tour prep sheet format and does NOT reference a YouTube source as canonical_parent_id.

---

## GATE 15: GBP as AI Citation Source (SOFT — opportunity missed warning)

Google's Gemini AI now pulls from GBP posts, reviews, and business description to answer local queries. Every GMB post is an AI citation opportunity.

- GMB posts should include entity-rich, data-specific language that an AI engine can extract
- Reviews mentioning specific neighborhoods or transaction types become AI signals
- Prompt Taylor to coach satisfied clients to mention specific neighborhoods in Google reviews
- GMB business description should contain key entity declarations (Taylor Dasch, EG Realty, Temple TX)

---

## GATE 16: Best Posting Times (SOFT — warn if outside window)

Reference `social-media-config.json` platform sections for current best times. When generating content with a posting recommendation, verify timing aligns with the 2026 data:

| Platform | Best Days | Best Times (Central) |
|----------|-----------|---------------------|
| TikTok | Tue-Fri | 2-6 PM |
| Instagram | Tue-Wed | 10 AM-2 PM, 5-9 PM |
| YouTube Long | Thu-Sat | 2-4 PM (publish 2hrs early) |
| YouTube Shorts | Any day | Less time-sensitive |
| GMB | Weekdays | 8-10 AM |
| LinkedIn | Tue-Thu | 7-9 AM |
| BP/Reddit | Tue-Wed | 10 AM-12 PM |

If content is being scheduled outside these windows, warn but do not block.

---

## Enforcement

- HARD gates: Output blocked. Fix required before delivery.
- SOFT gates: Output delivered with explicit warning. Taylor decides.
- Silent pass: If all gates pass, deliver output without listing checks (don't waste Taylor's time).
