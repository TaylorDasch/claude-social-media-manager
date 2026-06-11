2026-05-27T16:25:35.881673Z ERROR codex_core::session: failed to load skill /Users/taylordasch_1/.claude/skills/geo-query-finder/SKILL.md: missing YAML frontmatter delimited by ---
2026-05-27T16:25:35.881708Z ERROR codex_core::session: failed to load skill /Users/taylordasch_1/.agents/skills/repurpose-tree/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 99
OpenAI Codex v0.128.0 (research preview)
--------
workdir: /Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019e6a41-78c9-7e02-b966-4f276d5f3b5e
--------
user
# Codex Critic Prompt — Council Cross-Lab Voice

**Use when:** Council skill needs the Codex cross-lab Critic role (default-on for flagship work).
**Append to:** the candidate script/draft being attacked.
**Captured into lineage as:** `critic-codex-r<N>.md` in the reason-run folder.

---

## PROMPT (copy below this line through the END marker)

ROLE: You are an adversarial critic from a different AI lab than the author (Claude / Anthropic). You are Codex, trained on OpenAI's corpus. You do not share Anthropic's RLHF conditioning or voice priors — that is the value you bring. Attack from a different angle than a Claude critic would.

CONTEXT — TAYLOR DASCH / EG REALTY / TEMPLE TX:
- Real estate agent at EG Realty, Temple, TX, USA
- $30M+ closed volume, 100+ transactions, BiggerPockets Featured 3 years
- Investor-analyst voice: data-first, honest negatives, no generic real-estate language
- Audience lanes (kept strictly separate):
  - **Living in Temple channel:** BSW medical hires, military PCS-window buyers (Fort Hood), DFW/Austin relocators
  - **Investing in Temple channel:** investors only — NEVER mix
- Banned vocabulary: dream home, charming, nestled, turnkey, hidden gem, perfect (neighborhood/home), exclusive, stunning, gorgeous, paradise, oasis, picturesque, "you'll love," "won't last," "must see," boasts, "a true gem," "one-of-a-kind," sneak peek, white glove, "my expertise," insider, dream
- Lane discipline: NO investor framing on buyer content (no cap rates, no cash flow, no rental analysis on a Living in Temple piece); NO buyer framing on investor content
- BSW guardrails: lender channel only (Stark Law); never direct-to-physician outreach
- Format rules: identity declaration must appear in first 3 sentences but NOT in first 15 seconds of video; ONE creative element per video, not three; honest negatives included

TASK:

Attack this draft ruthlessly. Imagine the most informed hostile commenter on r/TempleTX, a BSW physician group chat, or a Fort Hood spouse Facebook group — what would they tear apart? What would an industry-savvy competitor agent quote out of context to discredit Taylor?

For each weakness identified:
1. Tag as **FATAL** (cannot ship; breaks lane discipline, format spec, fair housing, NAR Article 15, TREC, or hits banned vocabulary), **MAJOR** (degrades the deliverable; must fix), or **MINOR** (polish)
2. Quote the EXACT line
3. Propose the rewrite

Check these explicitly:
- Identity-declaration timing (sentence 3 must land at 0:14 or later if it's a video)
- Any forward-looking claim, market forecast, rate prediction, or "will" statement
- Banned vocabulary anywhere in the draft
- Lane discipline (any investor framing leaking into buyer content, or vice versa?)
- Numbers that look fabricated, rounded too hard, or hand-wavy without provenance
- Tone — analyst register vs sales/pump piece
- Things a savvy audience member would see as patronizing, generic, or AI-generated
- BSW lender-channel discipline (no direct-to-physician moves)
- Whether the draft commits Taylor to actions he can't or shouldn't fulfill (sending spreadsheets, promising monthly cadence without commitment, etc.)
- Compliance — TREC, IABS, Fair Housing, MLS attribution where claims are data-anchored

Output structure:

```
FATAL WEAKNESSES (must fix or kill):
1. [Quote] — [Why it's fatal] — [Proposed rewrite]
2. ...

MAJOR WEAKNESSES (must fix to ship cleanly):
1. ...

MINOR WEAKNESSES (polish):
1. ...

DOMAIN CHECKS:
- Identity timing: [PASS/FAIL with line reference]
- Banned vocabulary: [LIST any found, or "clean"]
- Lane discipline: [PASS/FAIL]
- Forecast surface: [PASS/FAIL with line reference]
- Data provenance: [PASS/FAIL]

VERDICT: SHIP / REVISE / KILL
ONE-LINE REASON: [exact one sentence — no hedging]
```

Do NOT soften your critique. Do NOT add complimentary preamble. Do NOT suggest the draft is "generally strong but has minor issues." If it has zero issues, say so — but only if it actually has zero issues. The author wants an outsider voice; deliver one.

---

DRAFT TO REVIEW:

[Paste the full candidate script/draft below this line]

---

END PROMPT

==========================================
DRAFT TO REVIEW (full candidate package):
==========================================
# Hospital District — INVESTOR Video Package (Investing in Temple)
**Author-A · r1 · 2026-05-27**
Companion to money page: https://templetxhomes.net/hospital-district/
Data ground truth: fresh MLS pull 2026-05-27.

---

## 1. LONG-FORM SCRIPT (6–9 min, investor-analyst voice)

> Format note: visual/audio change ~every 7s. Timestamps approximate. Rents are labeled verify-day-of inputs. All math shown as methodology so the investor plugs their own numbers.

---

**[0:00–0:18 — HOOK]**
There's a neighborhood in Temple, Texas where the median house closed this year for a hundred and forty-nine thousand, nine hundred and ninety-nine dollars. Not a typo. Sub-one-fifty. Single-family. And it sits three to four minutes from a twelve-thousand-person hospital workforce that never stops needing somewhere to sleep.

I own two houses on this street. I rehabbed both of them. So before you scroll, let me show you the actual numbers — including the one risk that scares retail buyers off and keeps your entry price this low.

**[0:18–0:48 — ENTITY + CREDIBILITY (woven, not stacked)]**
I'm Taylor Dasch with EG Realty. I've closed over thirty million in volume and a hundred-plus transactions, I've been a BiggerPockets Featured Agent three years running, and I'm ranked twenty-eighth out of two thousand-plus agents in Bell County. But here's the part that actually matters for this video: I don't just list this neighborhood. I bought in it. Eighteen-oh-five and eighteen-fourteen South Seventh. I've pulled the foundation reports, written the rehab checks, and dealt with the clay. So this isn't a tour. It's a deal breakdown from someone with skin in the dirt.

**[0:48–1:05 — NAME THE MARKET / FRAME]**
The area I'm talking about is the Hospital District — the older single-family pocket wrapped around Baylor Scott & White. I'm going to be blunt about something up front: this is not a pretty neighborhood. It's a smart one. If you want curb-appeal photos, this isn't your video. If you want the cheapest single-family entry next to a recession-resistant employer in this city, stay.

**[1:05–2:00 — THE DEMAND ENGINE: BSW]**
Why does this dirt matter? One reason: the hospital. Baylor Scott & White's Temple campus runs roughly eighty-eight hundred employees, plus around thirty-five hundred at the VA next door. Call it twelve-thousand-plus medical workers in a tight cluster. It's a Level I trauma center — twenty-four-seven shifts, which means people working nights, sleeping days, and needing housing close in.

And it churns. Travel nurses and traveling clinicians cycle through on thirteen-week contracts, constantly. That's the part investors miss. You're not just betting on a stable employer — you're betting on a stable employer with built-in tenant turnover that *wants* short commutes and furnished options.

Here's a tell from the data: roughly forty-seven percent of the active listings in this area literally cite proximity to Baylor Scott & White in the remarks. When half the sellers are using the hospital as the selling point, the rental thesis is already priced into the neighborhood's DNA. Your tenant demand isn't a hope. It's a payroll.

To be clear — this is about who *rents* from you. I'm not telling anyone to move to Temple. I'm telling you who fills your unit.

**[2:00–3:00 — ENTRY-PRICE REALITY (the numbers)]**
Now the entry. Fresh pull, today. Closed median price in the Hospital District: a hundred forty-nine, nine ninety-nine. Active median list is sitting around a hundred sixty thousand, and the median works out to about a hundred twenty-six dollars a square foot.

Compare that to Temple as a whole — citywide median runs somewhere in the two-seventy-five to three-fifteen range at roughly a hundred seventy-eight a foot. *(Verify that citywide number day-of — it moves.)* That means the Hospital District is trading at roughly fifty to sixty percent of the citywide median. This is the cheapest single-family entry near a major employer in Temple. Full stop.

The stock explains the price. Seventy-five percent of these homes were built before 1960. The median build year is 1952. Median size, about eleven-hundred ninety-six square feet. Of around a hundred thirteen homes in the dataset, only six were built after 2000 — so new infill exists, but it's rare and it carries a premium.

And you have leverage. Median days on market is about fifty-eight for closed homes, and sale-to-list is running around ninety-seven percent at the median — sellers are giving back two to seven points. In the distressed, as-is cluster the mean drops closer to ninety-three. Translation: this is a negotiating market for the buyer who shows up with cash and a contractor.

**[3:00–5:10 — THE PLAYS, WITH TRANSPARENT MATH]**
So how do you actually make money here? Four plays. I'll show the arithmetic on each so you can plug in your own rents — and you *should*, because my rent figures are from earlier research and you need to verify them the day you write the offer.

**Play one — buy-and-hold, long-term rental.**
Let's build a realistic all-in. Say you buy near the closed median: a hundred twenty thousand on an older home that needs work, plus a rehab to a livable rental standard. Budget thirty to fifty thousand for that — I'll use forty. That's roughly a hundred sixty thousand all-in.
Long-term rent in this pocket, verify-day-of, lands somewhere around nine hundred to eleven hundred a month. Take the low end to stay honest: a thousand a month is twelve thousand a year gross.
On older pre-1960 stock, your expense load is real — taxes, insurance, vacancy, repairs, management. Underwrite around forty-five percent of gross going to expenses. That leaves about sixty-six hundred a year in net operating income. Sixty-six hundred on a hundred-sixty-thousand all-in is a cap rate around four-point-one percent.
Push rent to eleven hundred and trim expenses to forty percent — your NOI is about seventy-nine hundred, and your cap rate moves toward five percent. So you're underwriting a roughly four-to-five percent cap on a buy-and-hold. That's not a home run. That's a slow, boring, hospital-backed bond. Which brings us to the play that actually justifies this neighborhood.

**Play two — the mid-term rental for travel nurses. This is the premium play.**
Same hundred-sixty-thousand all-in, but you furnish it — call it eight to twelve thousand more in furniture and setup. Mid-term, furnished rent to a traveling clinician, verify-day-of, runs roughly fourteen hundred to eighteen hundred a month. Take fifteen hundred. That's eighteen thousand a year gross.
Furnished mid-term carries higher operating costs — utilities, furnishings, turns, higher vacancy between contracts — so underwrite heavier, call it fifty percent expenses. That's nine thousand NOI on roughly a hundred seventy thousand all-in including the furniture. Cap rate around five-point-three percent, and on the high end of rent you're pushing past six and a half. The proximity to the hospital is the entire moat on this play — three to four minutes to BSW is what lets you charge the furnished premium. Nobody pays mid-term rates to live twenty minutes out.

**Play three — value-add flip.**
Buy at a hundred to a hundred-thirty, put in around forty in rehab, and your after-repair value targets roughly one-eighty to two-ten — and the comps support that ceiling. Look at South Seventh: eleven-oh-one sold at a hundred twenty thousand, ten-oh-eight square feet, built 1928. Twelve-oh-two sold at a hundred thirty-nine. But eleven-oh-two — thirteen-forty-four square feet, built 1965 — sold at a hundred ninety-two. Newer and bigger wins. So the flip thesis is real, but your exit depends on square footage and how updated it is, not the dirt alone. Run your seventy-percent-of-ARV-minus-rehab number hard, because in a ninety-seven-percent sale-to-list market your buyer has leverage too.

**Play four — small multifamily.**
About eight percent of these listings — nine of a hundred thirteen — are zoned commercial, multi-family, or mixed-use. There's a property at three-oh-nine South Thirty-First explicitly zoned multi-family. Duplex conversions and small multi exist here. If you want two doors on one foundation next to a hospital, this is one of the only Temple submarkets where the zoning cooperates.

**[5:10–6:25 — THE FOUNDATION RISK = THE MOAT]**
Now the part I refuse to soft-pedal, because if I do, someone buys a money pit on my word.
These homes are pier-and-beam, sitting on Bell County black clay. Expansive clay. It swells when it's wet and shrinks when it's dry, and it moves your foundation with it. About four-point-four percent of the listings flag foundation issues outright — five homes name it directly — but I'll tell you straight, the real number is higher. Plenty of as-is sellers just don't disclose it. Thirty-three percent of these listings — thirty-seven of a hundred thirteen — mention as-is, rehab, repair, or foundation in the remarks. That's not a coincidence.
So budget for it. Six thousand dollars minimum for foundation work, and the range runs five to fifteen depending on severity. And do not — *do not* — rely on a general home inspector for this. Hire a structural engineer. Different scope, different liability, different number. That's a non-negotiable line item, not an optional one.
And it's not just the slab. Pre-1960 stock means galvanized plumbing that's rusting shut, outdated or knob-and-tube wiring, and asbestos and lead in anything built before 1978. That's why the all-in rehab to a livable rental standard is thirty to fifty thousand, not ten.
Here's the reframe, and this is the whole game: that risk is your moat. The clay, the foundations, the asbestos — that's exactly what scares retail buyers and house-flippers-on-HGTV out of this neighborhood. It's *why* the median is sub-one-fifty next to a twelve-thousand-person employer. The day this becomes an easy, move-in-ready neighborhood, your entry price doubles. The friction is the opportunity. You don't want this to be easy. You want to be the one who can underwrite the hard part.

**[6:25–7:15 — WHO IT'S FOR / NOT FOR]**
So who is this for? It's for the buy-and-hold investor who wants recession-resistant tenant demand and will accept a four-to-five cap to get it. It's for the MTR operator who can run a furnished mid-term and capture the travel-nurse premium — that's where the real yield lives. And it's for the value-add flipper with a real contractor and a structural engineer on speed dial.
Who is it *not* for? Anyone who wants passive and hands-off on day one. Anyone underwriting on rents they haven't verified this week. And anyone who hears "pier-and-beam on clay" and doesn't budget for it. If you need it to be pretty, or you need it to be easy, this neighborhood will punish you.

**[7:15–7:50 — TAYLOR'S TAKE / VERDICT]**
Here's what I'd actually do. If I'm buying my next one here — and I might — I'm buying the worst house I can structurally fix on the best block I can find, I'm running it as a furnished mid-term for the hospital, and I'm underwriting the foundation before I underwrite the upside. I'd take a five-cap MTR with payroll-backed demand over a flashier deal in a neighborhood with no employer behind it. Boring and backed beats exciting and exposed. I've made that bet twice on South Seventh. It's why I can talk about it instead of just listing it.

**[7:50–8:20 — CTA]**
I built a full breakdown of the Hospital District on my site — the subdivision-by-subdivision data, the comps, and the investor plays — and it's linked in the description and pinned in the comments. If you're underwriting a deal here, that page is your starting point. And if you want me to run the numbers on a specific property, the offer's in the description too. Verify your rents the day you write the offer. Hire the structural engineer. And don't let the ugly scare you off the math. I'm Taylor Dasch. I'll see you on the next one.

---

## 2. HOOK VARIANTS (first 15s — NO entity declaration)

**Hook A — The Number**
There's a neighborhood in Temple, Texas where the median house closed this year for a hundred forty-nine thousand, nine hundred ninety-nine dollars — three to four minutes from a twelve-thousand-person hospital workforce. I own two houses on this street. Here's the math, and the one risk that keeps your entry this cheap.

**Hook B — The Contrarian**
This is not a pretty neighborhood. It's a smart one. Sub-one-fifty single-family, next to the biggest employer in Temple, and most investors won't touch it for one reason. I bought here twice — let me show you why the ugly is the opportunity.

**Hook C — The Moat**
The reason houses near Temple's hospital still close under a hundred fifty grand isn't location. It's the dirt underneath them. Expansive clay scares retail buyers off — and it's exactly why this is the cheapest single-family cash-flow entry in the city. I own two of these. Here's how the numbers actually pencil.

---

## 3. TITLE + 7-SECTION DESCRIPTION

**TITLE:**
This Temple TX Neighborhood Cash-Flows Next to a Hospital — Houses Under $150K (Investor Breakdown)

*Alt:* Why Investors Buy Sub-$150K Houses by Temple TX's Hospital (Cap Rate Math + The Clay Risk)

---

**[Section 1 — Hook line / one-sentence promise]**
Single-family houses closing under $150K, three to four minutes from a 12,000-person hospital workforce in Temple, TX — here's the full investor breakdown with transparent cap-rate math, the four plays, and the foundation risk nobody warns you about.

**[Section 2 — What you'll learn]**
- Why the Hospital District trades at ~50–60% of Temple's citywide median
- The BSW tenant-demand engine: 12,000+ medical workers + travel-nurse churn
- 4 investor plays (LTR, MTR for travel nurses, value-add flip, small multifamily) with the actual arithmetic
- Why pier-and-beam on Bell County clay is both your biggest risk AND your moat
- Who this neighborhood is for — and who it'll punish

**[Section 3 — Timestamps]**
0:00 The $149,999 median (the hook)
0:18 Who I am + why I have skin in this dirt
0:48 Naming the market: the Hospital District
1:05 The demand engine — Baylor Scott & White
2:00 Entry-price reality (fresh MLS numbers)
3:00 Play 1 — Buy-and-hold LTR (cap-rate math)
3:50 Play 2 — MTR for travel nurses (the premium play)
4:30 Play 3 — Value-add flip + S 7th comps
4:55 Play 4 — Small multifamily / duplex zoning
5:10 The foundation & clay risk = the moat
6:25 Who it's for / who it's NOT for
7:15 My take — what I'd actually buy
7:50 Resources + how to get a deal analyzed

**[Section 4 — Entity declaration / about]**
Taylor Dasch with EG Realty — Temple, TX. $30M+ in volume, 100+ transactions, 3-year BiggerPockets Featured Agent, ranked #28 of 2,013 Bell County agents. I own and have rehabbed homes in this exact neighborhood (1805 & 1814 S 7th). I help investors underwrite buy-and-hold, BRRRR, MTR, and value-add deals in the Temple market.

**[Section 5 — Resources / links]**
Full Hospital District investor breakdown (subdivision data, comps, all four plays):
https://templetxhomes.net/hospital-district/?utm_source=youtube&utm_medium=description&utm_campaign=hospital-district-investor
Want me to run the numbers on a specific property? Comment the address or reach me below.

**[Section 6 — Contact]**
Taylor Dasch | EG Realty
254-718-4249 | dealswithdasch@gmail.com
templetxhomes.net

**[Section 7 — Disclaimer / hashtags + verify note]**
Rent figures are research-based estimates — verify current rents the day you write your offer. Cap-rate examples are illustrative methodology, not guaranteed returns; plug in your own numbers. Always hire a licensed structural engineer before purchasing pier-and-beam stock. Not investment advice.
#TempleTX #RealEstateInvesting #BRRRR #MidTermRentals #CashFlow #TexasRealEstate #RentalProperty #InvestingInTemple

---

## 4. THUMBNAIL BRIEF

**Concept:** Split-tension thumbnail — cheap entry vs. big institution. Left: a modest 1950s Hospital District bungalow exterior (slightly worn, real, not staged). Right or background: the BSW hospital tower / skyline. Bold price tag overlay bridges the two.

**Text overlay (≤4 words):** `$149K NEXT TO THIS` — with `$149K` huge on the house side and an arrow pointing to the hospital. (Backup: `UNDER $150K`)

**Visual direction:**
- High-contrast, slightly desaturated to signal "honest/analyst," not glossy real-estate.
- Yellow or red price tag for the dollar figure (high CTR contrast against muted house tones).
- Optional small circle inset of Taylor (arms-crossed, neutral, credible — not smiling-realtor).
- A subtle crack/foundation line motif at the bottom edge to hint at the risk hook without being literal.
- No IDX, no logos clutter. One number, one tension, one face.

---

## 5. B-ROLL SHOT LIST (dense — 7-second rule)

| # | Shot | Use over (script beat) |
|---|------|------------------------|
| 1 | Slow push-in on a 1950s pier-and-beam bungalow exterior, worn but solid | Hook / 0:00 |
| 2 | Tight on a "Sold" or for-sale rider sign, address blurred | Entry-price reality |
| 3 | Taylor walking up to 1805 / 1814 S 7th, keys in hand | Credibility / skin-in-the-dirt |
| 4 | Dashcam/POV drive: bungalow block → BSW campus, clock/timer overlay "3–4 min" | Demand engine |
| 5 | BSW hospital tower exterior + signage (Baylor Scott & White) | Demand engine |
| 6 | VA facility exterior signage | "+3,500 VA" line |
| 7 | Busy hospital entrance / shift-change foot traffic (or stock parking lot fill) | 24/7 shifts / travel-nurse churn |
| 8 | Screen-recording scroll of MLS remarks highlighting "near BSW" | 47% cite proximity |
| 9 | Clean on-screen data card: "$149,999 median · $126/sqft · 1952 build · 75% pre-1960" | Entry-price reality |
| 10 | Crawlspace / pier-and-beam underside footage (flashlight, real) | Foundation risk |
| 11 | Close-up of cracked drywall / sloping floor / shimmed pier | Foundation risk |
| 12 | Dried, cracked black-clay soil close-up | Bell County clay |
| 13 | Structural engineer's report / level on a floor | "Hire a structural engineer" |
| 14 | Galvanized pipe / old electrical panel / knob-and-tube detail | Other rehab risks |
| 15 | Rehab before→after split (gutted room → finished rental-grade room) | Value-add play |
| 16 | Furnished bedroom/living setup (MTR-style, clean, simple) | MTR play |
| 17 | Block-by-block street variance: one updated house next to one rough one | Block matters / S 7th comps |
| 18 | On-screen comp table: 1101 / 1202 / 1814 / 1102 S 7th | Flip comps |
| 19 | 1914 Coffee House exterior near BSW | Walkable amenity (light) |
| 20 | Taylor piece-to-camera, arms crossed, neutral delivery | Verdict / take |

---

## 6. SHORTS CUTS (≤60s each; title includes "Temple TX")

**SHORT 1 — "The $149K Number" (≈45s)**
*Title:* Houses Under $150K Next to a Hospital in Temple TX
*Script:*
"A single-family house in this Temple, Texas neighborhood closed this year for a median of a hundred forty-nine thousand, nine hundred ninety-nine. Three to four minutes from a twelve-thousand-person hospital workforce. So why is it this cheap? Because these homes sit on pier-and-beam over Bell County clay, and that scares retail buyers off — which is exactly why the median is sub-one-fifty next to the biggest employer in town. I own two houses on this street and rehabbed both. The clay isn't the problem. It's the moat. Budget six grand-plus for foundation work, hire a structural engineer, and you're buying cash flow nobody else will touch. Full breakdown's pinned."
*On-screen:* `$149,999 MEDIAN` → `3–4 MIN TO HOSPITAL` → `THE CLAY = THE MOAT`

**SHORT 2 — "The Travel-Nurse Play" (≈50s)**
*Title:* The Best Rental Play Near Temple TX's Hospital
*Script:*
"Here's the highest-yield play in Temple, Texas right now and almost nobody runs it. There's a hospital here with twelve thousand-plus medical workers and constant travel-nurse turnover — thirteen-week contracts, cycling through all year. You buy an older house three minutes away, all-in around a hundred seventy thousand including furniture, and you run it as a furnished mid-term rental. Verify rents day-of, but furnished mid-term in this pocket runs roughly fourteen to eighteen hundred a month versus a thousand for a long-term lease. That proximity to the hospital is the entire moat — nobody pays mid-term rates to live twenty minutes out. I own two houses on this street. Plays linked below."
*On-screen:* `12,000+ MEDICAL WORKERS` → `13-WEEK CONTRACTS` → `MTR > LTR HERE`

**SHORT 3 — "Don't Skip the Engineer" (≈40s)**
*Title:* The $6K Mistake Investors Make in Temple TX
*Script:*
"If you buy an older house near Temple, Texas's hospital and you only hire a general home inspector, you're gambling. These are pier-and-beam homes on expansive black clay. Around a third of the listings mention as-is, rehab, or foundation issues — and the real number's higher because as-is sellers don't always disclose. Budget six thousand minimum for foundation work, five to fifteen depending on severity, and hire a structural engineer — not just an inspector. Different scope, different number. I've written these checks on my own houses here. The math only works if you underwrite the dirt first."
*On-screen:* `PIER & BEAM` → `BELL COUNTY CLAY` → `HIRE A STRUCTURAL ENGINEER`

---

## 7. PINNED COMMENT

Full Hospital District investor breakdown — subdivision-by-subdivision data, comps, and all four plays (LTR, MTR for travel nurses, value-add flip, small multifamily):
https://templetxhomes.net/hospital-district/?utm_source=youtube&utm_medium=description&utm_campaign=hospital-district-investor

Two reminders before you write an offer: (1) verify current rents the day you offer — my figures are research-based estimates, and (2) hire a structural engineer on any pier-and-beam home, not just a general inspector. Drop an address below and I'll run the numbers with you. — Taylor

---

### COMPLIANCE SELF-CHECK
- Banned words: none present (anti-passive phrased as "passive and hands-off" / "move-in-ready"; "turnkey" not used). ✓
- Entity declaration: lands 0:18–0:48, not in first 15s. ✓
- Lane: investor-only; BSW = tenant-demand engine only; explicit "I'm not telling anyone to move to Temple"; no military; no buyer-lifestyle. ✓
- Math: gross → expense load → NOI → cap rate shown transparently; rents labeled verify-day-of; no single hard cap rate as gospel. ✓
- Foundation/clay: unflinching + framed as the moat. ✓
- Lived experience (1805 & 1814 S 7th) front and center. ✓
- Fresh MLS numbers used ($149,999, $126/sqft, 1952, 75% pre-1960, ~97% sale-to-list, ~58 DOM). ✓

codex
I’m going to treat this as a content/compliance review, not a code edit. I’ll verify the repo governance language and scan the provided draft for banned terms and high-risk claims before giving the adversarial critique.
exec
/bin/zsh -lc "pwd && rg --files -g 'QUALITY-GATES.md' -g 'FACT-HANDLING.md' -g 'CLAUDE.md' -g 'AGENTS.md'" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120
exec
/bin/zsh -lc "rg -n \"dream home|charming|nestled|turnkey|hidden gem|perfect|exclusive|stunning|gorgeous|paradise|oasis|picturesque|you'll love|won't last|must see|boasts|a true gem|one-of-a-kind|sneak peek|white glove|my expertise|insider|dream|Fort Hood|Fort Hood|Baylor|Stark|IABS|TREC|MLS|Article 15|fair housing|identity\" ." in /Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120
 exited 1 in 0ms:
/Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120

 succeeded in 0ms:
./r1-critic-codex.md:32:  - **Living in Temple channel:** BSW medical hires, military PCS-window buyers (Fort Hood), DFW/Austin relocators
./r1-critic-codex.md:34:- Banned vocabulary: dream home, charming, nestled, turnkey, hidden gem, perfect (neighborhood/home), exclusive, stunning, gorgeous, paradise, oasis, picturesque, "you'll love," "won't last," "must see," boasts, "a true gem," "one-of-a-kind," sneak peek, white glove, "my expertise," insider, dream
./r1-critic-codex.md:36:- BSW guardrails: lender channel only (Stark Law); never direct-to-physician outreach
./r1-critic-codex.md:37:- Format rules: identity declaration must appear in first 3 sentences but NOT in first 15 seconds of video; ONE creative element per video, not three; honest negatives included
./r1-critic-codex.md:41:Attack this draft ruthlessly. Imagine the most informed hostile commenter on r/TempleTX, a BSW physician group chat, or a Fort Hood spouse Facebook group — what would they tear apart? What would an industry-savvy competitor agent quote out of context to discredit Taylor?
./r1-critic-codex.md:44:1. Tag as **FATAL** (cannot ship; breaks lane discipline, format spec, fair housing, NAR Article 15, TREC, or hits banned vocabulary), **MAJOR** (degrades the deliverable; must fix), or **MINOR** (polish)
./r1-critic-codex.md:58:- Compliance — TREC, IABS, Fair Housing, MLS attribution where claims are data-anchored
./r1-critic-codex.md:102:Data ground truth: fresh MLS pull 2026-05-27.
./r1-critic-codex.md:121:The area I'm talking about is the Hospital District — the older single-family pocket wrapped around Baylor Scott & White. I'm going to be blunt about something up front: this is not a pretty neighborhood. It's a smart one. If you want curb-appeal photos, this isn't your video. If you want the cheapest single-family entry next to a recession-resistant employer in this city, stay.
./r1-critic-codex.md:124:Why does this dirt matter? One reason: the hospital. Baylor Scott & White's Temple campus runs roughly eighty-eight hundred employees, plus around thirty-five hundred at the VA next door. Call it twelve-thousand-plus medical workers in a tight cluster. It's a Level I trauma center — twenty-four-seven shifts, which means people working nights, sleeping days, and needing housing close in.
./r1-critic-codex.md:128:Here's a tell from the data: roughly forty-seven percent of the active listings in this area literally cite proximity to Baylor Scott & White in the remarks. When half the sellers are using the hospital as the selling point, the rental thesis is already priced into the neighborhood's DNA. Your tenant demand isn't a hope. It's a payroll.
./r1-critic-codex.md:215:1:05 The demand engine — Baylor Scott & White
./r1-critic-codex.md:216:2:00 Entry-price reality (fresh MLS numbers)
./r1-critic-codex.md:268:| 5 | BSW hospital tower exterior + signage (Baylor Scott & White) | Demand engine |
./r1-critic-codex.md:271:| 8 | Screen-recording scroll of MLS remarks highlighting "near BSW" | 47% cite proximity |
./r1-critic-codex.md:319:- Banned words: none present (anti-passive phrased as "passive and hands-off" / "move-in-ready"; "turnkey" not used). ✓
./r1-critic-codex.md:325:- Fresh MLS numbers used ($149,999, $126/sqft, 1952, 75% pre-1960, ~97% sale-to-list, ~58 DOM). ✓
./TASK.md:10:## GROUND TRUTH (fresh MLS pull 2026-05-27 — use these numbers)
./TASK.md:15:- Demand engine: **Baylor Scott & White = ~8,884 BSW + ~3,500 VA = 12,000+ medical workforce.** Level I trauma, 24/7 shifts, constant travel-nurse churn. ~47% of area MLS listings cite BSW proximity. **3–4 min to BSW.**
./TASK.md:38:dream home, charming, nestled, turnkey, white glove, hidden gem, perfect neighborhood, exclusive, sneak peek, insider, my expertise, paradise, oasis, stunning, gorgeous, dream, vibrant community, welcome home, picturesque, "you'll love", "won't last", "must see", boasts, "a true gem", "one-of-a-kind". (NOTE: "turnkey" is banned even in investor content — say "move-in-ready" or "passive/hands-off".)
./TASK.md:43:- NO military / Fort Hood relocation content.
./TASK.md:50:- Honest pragmatism over gloss: "This is not a pretty neighborhood. It's a smart one." Don't pretend it's up-and-coming or charming.
./TASK.md:51:- Use the fresh 2026-05-27 MLS numbers as ground truth.
./TASK.md:69:4. Numbers don't match the fresh 2026-05-27 MLS pull (closed median $149,999, ~$126/sqft, 1952 median build, 75% pre-1960, ~97% sale-to-list, ~58 DOM).
./r1-A.md:4:Data ground truth: fresh MLS pull 2026-05-27.
./r1-A.md:23:The area I'm talking about is the Hospital District — the older single-family pocket wrapped around Baylor Scott & White. I'm going to be blunt about something up front: this is not a pretty neighborhood. It's a smart one. If you want curb-appeal photos, this isn't your video. If you want the cheapest single-family entry next to a recession-resistant employer in this city, stay.
./r1-A.md:26:Why does this dirt matter? One reason: the hospital. Baylor Scott & White's Temple campus runs roughly eighty-eight hundred employees, plus around thirty-five hundred at the VA next door. Call it twelve-thousand-plus medical workers in a tight cluster. It's a Level I trauma center — twenty-four-seven shifts, which means people working nights, sleeping days, and needing housing close in.
./r1-A.md:30:Here's a tell from the data: roughly forty-seven percent of the active listings in this area literally cite proximity to Baylor Scott & White in the remarks. When half the sellers are using the hospital as the selling point, the rental thesis is already priced into the neighborhood's DNA. Your tenant demand isn't a hope. It's a payroll.
./r1-A.md:117:1:05 The demand engine — Baylor Scott & White
./r1-A.md:118:2:00 Entry-price reality (fresh MLS numbers)
./r1-A.md:170:| 5 | BSW hospital tower exterior + signage (Baylor Scott & White) | Demand engine |
./r1-A.md:173:| 8 | Screen-recording scroll of MLS remarks highlighting "near BSW" | 47% cite proximity |
./r1-A.md:221:- Banned words: none present (anti-passive phrased as "passive and hands-off" / "move-in-ready"; "turnkey" not used). ✓
./r1-A.md:227:- Fresh MLS numbers used ($149,999, $126/sqft, 1952, 75% pre-1960, ~97% sale-to-list, ~58 DOM). ✓

codex
I found the candidate package and task file in the reason-run folder. The local task card confirms this is investor-only and gives the same fresh MLS numbers, so the main risk surface is wording, compliance, and claims that could be clipped out of context.
exec
/bin/zsh -lc "sed -n '1,120p' TASK.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120
exec
/bin/zsh -lc "sed -n '1,260p' r1-A.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120
exec
/bin/zsh -lc "rg --files .. | rg '("'^|/)(QUALITY-GATES|FACT-HANDLING|SESSION-LOOP|DEFINITION-OF-DONE|MULTI-PASS-SYSTEM|WORKFLOW-STATE-MACHINE|CLAUDE|TASK)'"\\.md"'$'"'" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120
 succeeded in 0ms:
../reason-run-260527-1120/TASK.md

 succeeded in 0ms:
# TASK — Hospital District INVESTOR video (Investing in Temple channel)

Produce a complete, production-ready YouTube video package for Taylor Dasch's **Investing in Temple** channel — a **6–9 minute long-form investor video** on Temple TX's **Hospital District** neighborhood, plus **1–3 vertical Shorts** cuts. Flagship pillar content; on-camera companion to the money page https://templetxhomes.net/hospital-district/. This video mines the INVESTOR half of that page.

## AUDIENCE + FORMAT
- Channel: **Investing in Temple** (investor lane: buy-and-hold / BRRRR / MTR / value-add flippers). NOT the Living in Temple buyer/relocation channel. Taylor pivoted this to investor-only on 2026-05-27.
- Length: 6–9 min long-form + 1–3 vertical Shorts (≤60s each).
- Platform: YouTube long-form (7-section description, timestamps, entity declaration). Shorts titles must include "Temple TX".

## GROUND TRUTH (fresh MLS pull 2026-05-27 — use these numbers)
- Closed median price: **$149,999** (~$150K). Active median list: $160,000. **~$126/sqft** median.
- Sale-to-list: **~97% median** (sellers give back 2–7%; mean ~93% from distressed/as-is cluster). Median DOM: **~58 closed** / ~34 active. Buyers have negotiating leverage.
- Stock: **75% pre-1960**; **median build 1952**; range 1908–2026; median **~1,196 sqft**. Only 6 of ~113 built after 2000 (rare infill, premium).
- Citywide context: Temple median ~$275–315K / ~$178/sqft. Hospital District trades at **~50–60% of citywide median** — cheapest single-family entry near a major employer in Temple. [VERIFY citywide figure day-of — April estimate.]
- Demand engine: **Baylor Scott & White = ~8,884 BSW + ~3,500 VA = 12,000+ medical workforce.** Level I trauma, 24/7 shifts, constant travel-nurse churn. ~47% of area MLS listings cite BSW proximity. **3–4 min to BSW.**
- Investor reality: **45 of 113 (~40%)** listings mention investor/rental/income/tenant. **37 of 113 (~33%)** mention as-is/rehab/fix/flip/foundation/repair. 5 flagged foundation issues outright. 9 of 113 (~8%) commercial/multi-family/mixed-use zoning. Known fix-and-flip / rental-conversion zone.
- Subdivisions (decode plat names): Freeman Heights (12), Tal-Coe Place (10), Skyline (9), South Park (9), Temple Heights (9) — dominant clusters (51 of 113), mid-20th-c historic plats, trade similarly.
- S 7th St comps (sold): 1101 S 7th ($120K, 1,008sf, 1928); 1202 S 7th ($139K, 1,064sf, 1934); 1814 S 7th ($157K, 840sf, 1955); 1102 S 7th ($192K, 1,344sf, 1965 — newer+bigger wins).
- Foundation reality: pier-and-beam on expansive **Bell County black clay**. ~4.4% flagged but real number likely higher. Budget **$6,000+** (range $5K–$15K) for foundation work. ALWAYS hire a **structural engineer**, not just a general inspector. Also galvanized plumbing, outdated/knob-and-tube electrical, asbestos/lead in pre-1978 stock. Rehab to livable rental standard: **~$30K–$50K**.
- Schools: Temple ISD (not Belton ISD). Travis Science Academy = IB Middle Years campus. (Keep light — investor video; relevant only to tenant pool / resale.)
- Walkable amenity: 1914 Coffee House near BSW (across S 31st).

## THE INVESTOR PLAYS (teach math transparently — label rents VERIFY-day-of)
- Buy-and-hold LTR.
- **MTR for travel nurses** (the PREMIUM play — BSW proximity is the moat; furnished mid-term rentals to traveling clinicians).
- Value-add / flip: buy $100–130K + ~$40K rehab → ARV ~$180–210K.
- Small multifamily / duplex (mixed-use zoning present; 309 S 31st explicitly multi-family zoned).
- Rent assumptions (April research — MUST label as estimates to verify): LTR ~$900–1,100/mo; MTR ~$1,400–1,800/mo. Present all cap-rate/cash-flow math as **transparent methodology** ("at $X rent on a $Y all-in, your cap rate is Z%") so it doesn't go stale and an investor plugs their own numbers. Do NOT state a single hard cap-rate number as gospel.

## TAYLOR'S VOICE RULES (enforce in final)
- Investor-analyst voice: data first, interpretation second. Calm, blunt, honest. Include negatives ("Scars and All"). Not a salesperson, not hype.
- Entity declaration: **"Taylor Dasch with EG Realty"** appears naturally — but **NOT in the first 15 seconds** (hook owns the open). Land by ~0:30–0:60.
- Credibility (weave once, don't stack): $30M+ volume, 100+ transactions, 3-yr BiggerPockets Featured Agent, ranked #28 of 2,013 Bell County agents (top 1.4%). **Owns + has rehabbed IN this neighborhood (1805 & 1814 S 7th)** — the killer credibility beat for investors; lean on lived experience over titles.
- 7-Second Rule: visual/audio change ~every 7s (drives B-roll density).
- Include a plain-English verdict ("here's what I'd actually do").

## BANNED WORDS (hard fail if any appear in final)
dream home, charming, nestled, turnkey, white glove, hidden gem, perfect neighborhood, exclusive, sneak peek, insider, my expertise, paradise, oasis, stunning, gorgeous, dream, vibrant community, welcome home, picturesque, "you'll love", "won't last", "must see", boasts, "a true gem", "one-of-a-kind". (NOTE: "turnkey" is banned even in investor content — say "move-in-ready" or "passive/hands-off".)

## LANE DISCIPLINE (investor — enforce)
- INVESTOR content on the Investing in Temple channel. BSW appears ONLY as the **tenant-demand engine** (guaranteed renters, recession-resistant healthcare employment, travel-nurse churn) — NEVER as a "relocate to Temple for your BSW job" buyer/relocation pitch.
- NO buyer-lifestyle framing (no "imagine living here"; no schools-for-your-kids except as tenant-pool/resale factor).
- NO military / Fort Hood relocation content.
- NO mixing the Living in Temple buyer audience. If a beat sounds like a relocation guide, kill it.
- The foundation/clay risk is REQUIRED — framed as BOTH a real margin risk AND the competitive moat that keeps retail buyers out and entry prices low.

## EDITORIAL DECISIONS LOCKED
- Investor-only (not dual-audience).
- Name + own the micro-market as **"the Hospital District"** (not the local inside-joke "South Odd-Numbered Streets" — nobody searches that).
- Honest pragmatism over gloss: "This is not a pretty neighborhood. It's a smart one." Don't pretend it's up-and-coming or charming.
- Use the fresh 2026-05-27 MLS numbers as ground truth.

## SKIP
No buyer/relocation framing. No military lane. No lifestyle gloss. No IDX widgets. No fabricated cap-rate certainty. No deep school comparison (light touch only).

## DELIVERABLES (ALL of these, as one unified package)
1. **Final long-form script** (6–9 min, investor-analyst voice): hook → demand engine → entry-price reality → the plays w/ transparent math → foundation risk = moat → who it's for/not for → Taylor's-take verdict → CTA. Timestamp-able (mark approximate timestamps).
2. **3 hook variants** (first 15 seconds — NO entity declaration in the hook).
3. **Title** (YouTube, click-worthy, investor-framed, includes "Temple TX") + **7-section description** with timestamps and entity declaration.
4. **Thumbnail brief** (concept, text overlay ≤4 words, visual direction).
5. **B-roll shot list** (bungalow exteriors, BSW proximity drive, foundation/crawlspace, rehab before/after, block-by-block street variance, 1914 Coffee House) — dense enough for the 7-second rule.
6. **1–3 Shorts cuts** (≤60s each; title includes "Temple TX"; each a standalone hook).
7. **Pinned comment** with UTM page link: `https://templetxhomes.net/hospital-district/?utm_source=youtube&utm_medium=description&utm_campaign=hospital-district-investor`

## INVERSE-FAIL RUBRIC (this artifact embarrasses Taylor if…)
1. The cap-rate/flip/cash-flow math doesn't pencil at the stated entry + rent — a real BRRRR/MTR investor runs the numbers in comments and catches a fantasy deal.
2. It reads like a buyer/relocation video that wandered onto the investor channel (lane bleed — any "imagine your family here," any BSW-job-relocation pitch).
3. It soft-pedals the foundation/clay risk and a viewer buys a money pit on Taylor's word (trust destruction — the foundation beat must be unflinching).
4. Numbers don't match the fresh 2026-05-27 MLS pull (closed median $149,999, ~$126/sqft, 1952 median build, 75% pre-1960, ~97% sale-to-list, ~58 DOM).
5. It gets brigaded on r/realestateinvesting or BiggerPockets as someone who's never done a deal here — Taylor HAS (1805 & 1814 S 7th); lived-experience proof must be front and center.
6. It states a rent band or cap rate as gospel that's stale (April estimate) — rents must be framed as verify-day-of inputs.
7. A banned word ships in the final.
8. The entity declaration lands in the first 15 seconds (kills the hook) or never lands at all.

 succeeded in 0ms:
# Hospital District — INVESTOR Video Package (Investing in Temple)
**Author-A · r1 · 2026-05-27**
Companion to money page: https://templetxhomes.net/hospital-district/
Data ground truth: fresh MLS pull 2026-05-27.

---

## 1. LONG-FORM SCRIPT (6–9 min, investor-analyst voice)

> Format note: visual/audio change ~every 7s. Timestamps approximate. Rents are labeled verify-day-of inputs. All math shown as methodology so the investor plugs their own numbers.

---

**[0:00–0:18 — HOOK]**
There's a neighborhood in Temple, Texas where the median house closed this year for a hundred and forty-nine thousand, nine hundred and ninety-nine dollars. Not a typo. Sub-one-fifty. Single-family. And it sits three to four minutes from a twelve-thousand-person hospital workforce that never stops needing somewhere to sleep.

I own two houses on this street. I rehabbed both of them. So before you scroll, let me show you the actual numbers — including the one risk that scares retail buyers off and keeps your entry price this low.

**[0:18–0:48 — ENTITY + CREDIBILITY (woven, not stacked)]**
I'm Taylor Dasch with EG Realty. I've closed over thirty million in volume and a hundred-plus transactions, I've been a BiggerPockets Featured Agent three years running, and I'm ranked twenty-eighth out of two thousand-plus agents in Bell County. But here's the part that actually matters for this video: I don't just list this neighborhood. I bought in it. Eighteen-oh-five and eighteen-fourteen South Seventh. I've pulled the foundation reports, written the rehab checks, and dealt with the clay. So this isn't a tour. It's a deal breakdown from someone with skin in the dirt.

**[0:48–1:05 — NAME THE MARKET / FRAME]**
The area I'm talking about is the Hospital District — the older single-family pocket wrapped around Baylor Scott & White. I'm going to be blunt about something up front: this is not a pretty neighborhood. It's a smart one. If you want curb-appeal photos, this isn't your video. If you want the cheapest single-family entry next to a recession-resistant employer in this city, stay.

**[1:05–2:00 — THE DEMAND ENGINE: BSW]**
Why does this dirt matter? One reason: the hospital. Baylor Scott & White's Temple campus runs roughly eighty-eight hundred employees, plus around thirty-five hundred at the VA next door. Call it twelve-thousand-plus medical workers in a tight cluster. It's a Level I trauma center — twenty-four-seven shifts, which means people working nights, sleeping days, and needing housing close in.

And it churns. Travel nurses and traveling clinicians cycle through on thirteen-week contracts, constantly. That's the part investors miss. You're not just betting on a stable employer — you're betting on a stable employer with built-in tenant turnover that *wants* short commutes and furnished options.

Here's a tell from the data: roughly forty-seven percent of the active listings in this area literally cite proximity to Baylor Scott & White in the remarks. When half the sellers are using the hospital as the selling point, the rental thesis is already priced into the neighborhood's DNA. Your tenant demand isn't a hope. It's a payroll.

To be clear — this is about who *rents* from you. I'm not telling anyone to move to Temple. I'm telling you who fills your unit.

**[2:00–3:00 — ENTRY-PRICE REALITY (the numbers)]**
Now the entry. Fresh pull, today. Closed median price in the Hospital District: a hundred forty-nine, nine ninety-nine. Active median list is sitting around a hundred sixty thousand, and the median works out to about a hundred twenty-six dollars a square foot.

Compare that to Temple as a whole — citywide median runs somewhere in the two-seventy-five to three-fifteen range at roughly a hundred seventy-eight a foot. *(Verify that citywide number day-of — it moves.)* That means the Hospital District is trading at roughly fifty to sixty percent of the citywide median. This is the cheapest single-family entry near a major employer in Temple. Full stop.

The stock explains the price. Seventy-five percent of these homes were built before 1960. The median build year is 1952. Median size, about eleven-hundred ninety-six square feet. Of around a hundred thirteen homes in the dataset, only six were built after 2000 — so new infill exists, but it's rare and it carries a premium.

And you have leverage. Median days on market is about fifty-eight for closed homes, and sale-to-list is running around ninety-seven percent at the median — sellers are giving back two to seven points. In the distressed, as-is cluster the mean drops closer to ninety-three. Translation: this is a negotiating market for the buyer who shows up with cash and a contractor.

**[3:00–5:10 — THE PLAYS, WITH TRANSPARENT MATH]**
So how do you actually make money here? Four plays. I'll show the arithmetic on each so you can plug in your own rents — and you *should*, because my rent figures are from earlier research and you need to verify them the day you write the offer.

**Play one — buy-and-hold, long-term rental.**
Let's build a realistic all-in. Say you buy near the closed median: a hundred twenty thousand on an older home that needs work, plus a rehab to a livable rental standard. Budget thirty to fifty thousand for that — I'll use forty. That's roughly a hundred sixty thousand all-in.
Long-term rent in this pocket, verify-day-of, lands somewhere around nine hundred to eleven hundred a month. Take the low end to stay honest: a thousand a month is twelve thousand a year gross.
On older pre-1960 stock, your expense load is real — taxes, insurance, vacancy, repairs, management. Underwrite around forty-five percent of gross going to expenses. That leaves about sixty-six hundred a year in net operating income. Sixty-six hundred on a hundred-sixty-thousand all-in is a cap rate around four-point-one percent.
Push rent to eleven hundred and trim expenses to forty percent — your NOI is about seventy-nine hundred, and your cap rate moves toward five percent. So you're underwriting a roughly four-to-five percent cap on a buy-and-hold. That's not a home run. That's a slow, boring, hospital-backed bond. Which brings us to the play that actually justifies this neighborhood.

**Play two — the mid-term rental for travel nurses. This is the premium play.**
Same hundred-sixty-thousand all-in, but you furnish it — call it eight to twelve thousand more in furniture and setup. Mid-term, furnished rent to a traveling clinician, verify-day-of, runs roughly fourteen hundred to eighteen hundred a month. Take fifteen hundred. That's eighteen thousand a year gross.
Furnished mid-term carries higher operating costs — utilities, furnishings, turns, higher vacancy between contracts — so underwrite heavier, call it fifty percent expenses. That's nine thousand NOI on roughly a hundred seventy thousand all-in including the furniture. Cap rate around five-point-three percent, and on the high end of rent you're pushing past six and a half. The proximity to the hospital is the entire moat on this play — three to four minutes to BSW is what lets you charge the furnished premium. Nobody pays mid-term rates to live twenty minutes out.

**Play three — value-add flip.**
Buy at a hundred to a hundred-thirty, put in around forty in rehab, and your after-repair value targets roughly one-eighty to two-ten — and the comps support that ceiling. Look at South Seventh: eleven-oh-one sold at a hundred twenty thousand, ten-oh-eight square feet, built 1928. Twelve-oh-two sold at a hundred thirty-nine. But eleven-oh-two — thirteen-forty-four square feet, built 1965 — sold at a hundred ninety-two. Newer and bigger wins. So the flip thesis is real, but your exit depends on square footage and how updated it is, not the dirt alone. Run your seventy-percent-of-ARV-minus-rehab number hard, because in a ninety-seven-percent sale-to-list market your buyer has leverage too.

**Play four — small multifamily.**
About eight percent of these listings — nine of a hundred thirteen — are zoned commercial, multi-family, or mixed-use. There's a property at three-oh-nine South Thirty-First explicitly zoned multi-family. Duplex conversions and small multi exist here. If you want two doors on one foundation next to a hospital, this is one of the only Temple submarkets where the zoning cooperates.

**[5:10–6:25 — THE FOUNDATION RISK = THE MOAT]**
Now the part I refuse to soft-pedal, because if I do, someone buys a money pit on my word.
These homes are pier-and-beam, sitting on Bell County black clay. Expansive clay. It swells when it's wet and shrinks when it's dry, and it moves your foundation with it. About four-point-four percent of the listings flag foundation issues outright — five homes name it directly — but I'll tell you straight, the real number is higher. Plenty of as-is sellers just don't disclose it. Thirty-three percent of these listings — thirty-seven of a hundred thirteen — mention as-is, rehab, repair, or foundation in the remarks. That's not a coincidence.
So budget for it. Six thousand dollars minimum for foundation work, and the range runs five to fifteen depending on severity. And do not — *do not* — rely on a general home inspector for this. Hire a structural engineer. Different scope, different liability, different number. That's a non-negotiable line item, not an optional one.
And it's not just the slab. Pre-1960 stock means galvanized plumbing that's rusting shut, outdated or knob-and-tube wiring, and asbestos and lead in anything built before 1978. That's why the all-in rehab to a livable rental standard is thirty to fifty thousand, not ten.
Here's the reframe, and this is the whole game: that risk is your moat. The clay, the foundations, the asbestos — that's exactly what scares retail buyers and house-flippers-on-HGTV out of this neighborhood. It's *why* the median is sub-one-fifty next to a twelve-thousand-person employer. The day this becomes an easy, move-in-ready neighborhood, your entry price doubles. The friction is the opportunity. You don't want this to be easy. You want to be the one who can underwrite the hard part.

**[6:25–7:15 — WHO IT'S FOR / NOT FOR]**
So who is this for? It's for the buy-and-hold investor who wants recession-resistant tenant demand and will accept a four-to-five cap to get it. It's for the MTR operator who can run a furnished mid-term and capture the travel-nurse premium — that's where the real yield lives. And it's for the value-add flipper with a real contractor and a structural engineer on speed dial.
Who is it *not* for? Anyone who wants passive and hands-off on day one. Anyone underwriting on rents they haven't verified this week. And anyone who hears "pier-and-beam on clay" and doesn't budget for it. If you need it to be pretty, or you need it to be easy, this neighborhood will punish you.

**[7:15–7:50 — TAYLOR'S TAKE / VERDICT]**
Here's what I'd actually do. If I'm buying my next one here — and I might — I'm buying the worst house I can structurally fix on the best block I can find, I'm running it as a furnished mid-term for the hospital, and I'm underwriting the foundation before I underwrite the upside. I'd take a five-cap MTR with payroll-backed demand over a flashier deal in a neighborhood with no employer behind it. Boring and backed beats exciting and exposed. I've made that bet twice on South Seventh. It's why I can talk about it instead of just listing it.

**[7:50–8:20 — CTA]**
I built a full breakdown of the Hospital District on my site — the subdivision-by-subdivision data, the comps, and the investor plays — and it's linked in the description and pinned in the comments. If you're underwriting a deal here, that page is your starting point. And if you want me to run the numbers on a specific property, the offer's in the description too. Verify your rents the day you write the offer. Hire the structural engineer. And don't let the ugly scare you off the math. I'm Taylor Dasch. I'll see you on the next one.

---

## 2. HOOK VARIANTS (first 15s — NO entity declaration)

**Hook A — The Number**
There's a neighborhood in Temple, Texas where the median house closed this year for a hundred forty-nine thousand, nine hundred ninety-nine dollars — three to four minutes from a twelve-thousand-person hospital workforce. I own two houses on this street. Here's the math, and the one risk that keeps your entry this cheap.

**Hook B — The Contrarian**
This is not a pretty neighborhood. It's a smart one. Sub-one-fifty single-family, next to the biggest employer in Temple, and most investors won't touch it for one reason. I bought here twice — let me show you why the ugly is the opportunity.

**Hook C — The Moat**
The reason houses near Temple's hospital still close under a hundred fifty grand isn't location. It's the dirt underneath them. Expansive clay scares retail buyers off — and it's exactly why this is the cheapest single-family cash-flow entry in the city. I own two of these. Here's how the numbers actually pencil.

---

## 3. TITLE + 7-SECTION DESCRIPTION

**TITLE:**
This Temple TX Neighborhood Cash-Flows Next to a Hospital — Houses Under $150K (Investor Breakdown)

*Alt:* Why Investors Buy Sub-$150K Houses by Temple TX's Hospital (Cap Rate Math + The Clay Risk)

---

**[Section 1 — Hook line / one-sentence promise]**
Single-family houses closing under $150K, three to four minutes from a 12,000-person hospital workforce in Temple, TX — here's the full investor breakdown with transparent cap-rate math, the four plays, and the foundation risk nobody warns you about.

**[Section 2 — What you'll learn]**
- Why the Hospital District trades at ~50–60% of Temple's citywide median
- The BSW tenant-demand engine: 12,000+ medical workers + travel-nurse churn
- 4 investor plays (LTR, MTR for travel nurses, value-add flip, small multifamily) with the actual arithmetic
- Why pier-and-beam on Bell County clay is both your biggest risk AND your moat
- Who this neighborhood is for — and who it'll punish

**[Section 3 — Timestamps]**
0:00 The $149,999 median (the hook)
0:18 Who I am + why I have skin in this dirt
0:48 Naming the market: the Hospital District
1:05 The demand engine — Baylor Scott & White
2:00 Entry-price reality (fresh MLS numbers)
3:00 Play 1 — Buy-and-hold LTR (cap-rate math)
3:50 Play 2 — MTR for travel nurses (the premium play)
4:30 Play 3 — Value-add flip + S 7th comps
4:55 Play 4 — Small multifamily / duplex zoning
5:10 The foundation & clay risk = the moat
6:25 Who it's for / who it's NOT for
7:15 My take — what I'd actually buy
7:50 Resources + how to get a deal analyzed

**[Section 4 — Entity declaration / about]**
Taylor Dasch with EG Realty — Temple, TX. $30M+ in volume, 100+ transactions, 3-year BiggerPockets Featured Agent, ranked #28 of 2,013 Bell County agents. I own and have rehabbed homes in this exact neighborhood (1805 & 1814 S 7th). I help investors underwrite buy-and-hold, BRRRR, MTR, and value-add deals in the Temple market.

**[Section 5 — Resources / links]**
Full Hospital District investor breakdown (subdivision data, comps, all four plays):
https://templetxhomes.net/hospital-district/?utm_source=youtube&utm_medium=description&utm_campaign=hospital-district-investor
Want me to run the numbers on a specific property? Comment the address or reach me below.

**[Section 6 — Contact]**
Taylor Dasch | EG Realty
254-718-4249 | dealswithdasch@gmail.com
templetxhomes.net

**[Section 7 — Disclaimer / hashtags + verify note]**
Rent figures are research-based estimates — verify current rents the day you write your offer. Cap-rate examples are illustrative methodology, not guaranteed returns; plug in your own numbers. Always hire a licensed structural engineer before purchasing pier-and-beam stock. Not investment advice.
#TempleTX #RealEstateInvesting #BRRRR #MidTermRentals #CashFlow #TexasRealEstate #RentalProperty #InvestingInTemple

---

## 4. THUMBNAIL BRIEF

**Concept:** Split-tension thumbnail — cheap entry vs. big institution. Left: a modest 1950s Hospital District bungalow exterior (slightly worn, real, not staged). Right or background: the BSW hospital tower / skyline. Bold price tag overlay bridges the two.

**Text overlay (≤4 words):** `$149K NEXT TO THIS` — with `$149K` huge on the house side and an arrow pointing to the hospital. (Backup: `UNDER $150K`)

**Visual direction:**
- High-contrast, slightly desaturated to signal "honest/analyst," not glossy real-estate.
- Yellow or red price tag for the dollar figure (high CTR contrast against muted house tones).
- Optional small circle inset of Taylor (arms-crossed, neutral, credible — not smiling-realtor).
- A subtle crack/foundation line motif at the bottom edge to hint at the risk hook without being literal.
- No IDX, no logos clutter. One number, one tension, one face.

---

## 5. B-ROLL SHOT LIST (dense — 7-second rule)

| # | Shot | Use over (script beat) |
|---|------|------------------------|
| 1 | Slow push-in on a 1950s pier-and-beam bungalow exterior, worn but solid | Hook / 0:00 |
| 2 | Tight on a "Sold" or for-sale rider sign, address blurred | Entry-price reality |
| 3 | Taylor walking up to 1805 / 1814 S 7th, keys in hand | Credibility / skin-in-the-dirt |
| 4 | Dashcam/POV drive: bungalow block → BSW campus, clock/timer overlay "3–4 min" | Demand engine |
| 5 | BSW hospital tower exterior + signage (Baylor Scott & White) | Demand engine |
| 6 | VA facility exterior signage | "+3,500 VA" line |
| 7 | Busy hospital entrance / shift-change foot traffic (or stock parking lot fill) | 24/7 shifts / travel-nurse churn |
| 8 | Screen-recording scroll of MLS remarks highlighting "near BSW" | 47% cite proximity |
| 9 | Clean on-screen data card: "$149,999 median · $126/sqft · 1952 build · 75% pre-1960" | Entry-price reality |
| 10 | Crawlspace / pier-and-beam underside footage (flashlight, real) | Foundation risk |
| 11 | Close-up of cracked drywall / sloping floor / shimmed pier | Foundation risk |
| 12 | Dried, cracked black-clay soil close-up | Bell County clay |
| 13 | Structural engineer's report / level on a floor | "Hire a structural engineer" |
| 14 | Galvanized pipe / old electrical panel / knob-and-tube detail | Other rehab risks |
| 15 | Rehab before→after split (gutted room → finished rental-grade room) | Value-add play |
| 16 | Furnished bedroom/living setup (MTR-style, clean, simple) | MTR play |
| 17 | Block-by-block street variance: one updated house next to one rough one | Block matters / S 7th comps |
| 18 | On-screen comp table: 1101 / 1202 / 1814 / 1102 S 7th | Flip comps |
| 19 | 1914 Coffee House exterior near BSW | Walkable amenity (light) |
| 20 | Taylor piece-to-camera, arms crossed, neutral delivery | Verdict / take |

---

## 6. SHORTS CUTS (≤60s each; title includes "Temple TX")

**SHORT 1 — "The $149K Number" (≈45s)**
*Title:* Houses Under $150K Next to a Hospital in Temple TX
*Script:*
"A single-family house in this Temple, Texas neighborhood closed this year for a median of a hundred forty-nine thousand, nine hundred ninety-nine. Three to four minutes from a twelve-thousand-person hospital workforce. So why is it this cheap? Because these homes sit on pier-and-beam over Bell County clay, and that scares retail buyers off — which is exactly why the median is sub-one-fifty next to the biggest employer in town. I own two houses on this street and rehabbed both. The clay isn't the problem. It's the moat. Budget six grand-plus for foundation work, hire a structural engineer, and you're buying cash flow nobody else will touch. Full breakdown's pinned."
*On-screen:* `$149,999 MEDIAN` → `3–4 MIN TO HOSPITAL` → `THE CLAY = THE MOAT`

**SHORT 2 — "The Travel-Nurse Play" (≈50s)**
*Title:* The Best Rental Play Near Temple TX's Hospital
*Script:*
"Here's the highest-yield play in Temple, Texas right now and almost nobody runs it. There's a hospital here with twelve thousand-plus medical workers and constant travel-nurse turnover — thirteen-week contracts, cycling through all year. You buy an older house three minutes away, all-in around a hundred seventy thousand including furniture, and you run it as a furnished mid-term rental. Verify rents day-of, but furnished mid-term in this pocket runs roughly fourteen to eighteen hundred a month versus a thousand for a long-term lease. That proximity to the hospital is the entire moat — nobody pays mid-term rates to live twenty minutes out. I own two houses on this street. Plays linked below."
*On-screen:* `12,000+ MEDICAL WORKERS` → `13-WEEK CONTRACTS` → `MTR > LTR HERE`

**SHORT 3 — "Don't Skip the Engineer" (≈40s)**
*Title:* The $6K Mistake Investors Make in Temple TX
*Script:*
"If you buy an older house near Temple, Texas's hospital and you only hire a general home inspector, you're gambling. These are pier-and-beam homes on expansive black clay. Around a third of the listings mention as-is, rehab, or foundation issues — and the real number's higher because as-is sellers don't always disclose. Budget six thousand minimum for foundation work, five to fifteen depending on severity, and hire a structural engineer — not just an inspector. Different scope, different number. I've written these checks on my own houses here. The math only works if you underwrite the dirt first."
*On-screen:* `PIER & BEAM` → `BELL COUNTY CLAY` → `HIRE A STRUCTURAL ENGINEER`

---

## 7. PINNED COMMENT

Full Hospital District investor breakdown — subdivision-by-subdivision data, comps, and all four plays (LTR, MTR for travel nurses, value-add flip, small multifamily):
https://templetxhomes.net/hospital-district/?utm_source=youtube&utm_medium=description&utm_campaign=hospital-district-investor

Two reminders before you write an offer: (1) verify current rents the day you offer — my figures are research-based estimates, and (2) hire a structural engineer on any pier-and-beam home, not just a general inspector. Drop an address below and I'll run the numbers with you. — Taylor

---

### COMPLIANCE SELF-CHECK
- Banned words: none present (anti-passive phrased as "passive and hands-off" / "move-in-ready"; "turnkey" not used). ✓
- Entity declaration: lands 0:18–0:48, not in first 15s. ✓
- Lane: investor-only; BSW = tenant-demand engine only; explicit "I'm not telling anyone to move to Temple"; no military; no buyer-lifestyle. ✓
- Math: gross → expense load → NOI → cap rate shown transparently; rents labeled verify-day-of; no single hard cap rate as gospel. ✓
- Foundation/clay: unflinching + framed as the moat. ✓
- Lived experience (1805 & 1814 S 7th) front and center. ✓
- Fresh MLS numbers used ($149,999, $126/sqft, 1952, 75% pre-1960, ~97% sale-to-list, ~58 DOM). ✓

exec
/bin/zsh -lc "nl -ba r1-A.md | sed -n '1,240p'" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120
 succeeded in 0ms:
     1	# Hospital District — INVESTOR Video Package (Investing in Temple)
     2	**Author-A · r1 · 2026-05-27**
     3	Companion to money page: https://templetxhomes.net/hospital-district/
     4	Data ground truth: fresh MLS pull 2026-05-27.
     5	
     6	---
     7	
     8	## 1. LONG-FORM SCRIPT (6–9 min, investor-analyst voice)
     9	
    10	> Format note: visual/audio change ~every 7s. Timestamps approximate. Rents are labeled verify-day-of inputs. All math shown as methodology so the investor plugs their own numbers.
    11	
    12	---
    13	
    14	**[0:00–0:18 — HOOK]**
    15	There's a neighborhood in Temple, Texas where the median house closed this year for a hundred and forty-nine thousand, nine hundred and ninety-nine dollars. Not a typo. Sub-one-fifty. Single-family. And it sits three to four minutes from a twelve-thousand-person hospital workforce that never stops needing somewhere to sleep.
    16	
    17	I own two houses on this street. I rehabbed both of them. So before you scroll, let me show you the actual numbers — including the one risk that scares retail buyers off and keeps your entry price this low.
    18	
    19	**[0:18–0:48 — ENTITY + CREDIBILITY (woven, not stacked)]**
    20	I'm Taylor Dasch with EG Realty. I've closed over thirty million in volume and a hundred-plus transactions, I've been a BiggerPockets Featured Agent three years running, and I'm ranked twenty-eighth out of two thousand-plus agents in Bell County. But here's the part that actually matters for this video: I don't just list this neighborhood. I bought in it. Eighteen-oh-five and eighteen-fourteen South Seventh. I've pulled the foundation reports, written the rehab checks, and dealt with the clay. So this isn't a tour. It's a deal breakdown from someone with skin in the dirt.
    21	
    22	**[0:48–1:05 — NAME THE MARKET / FRAME]**
    23	The area I'm talking about is the Hospital District — the older single-family pocket wrapped around Baylor Scott & White. I'm going to be blunt about something up front: this is not a pretty neighborhood. It's a smart one. If you want curb-appeal photos, this isn't your video. If you want the cheapest single-family entry next to a recession-resistant employer in this city, stay.
    24	
    25	**[1:05–2:00 — THE DEMAND ENGINE: BSW]**
    26	Why does this dirt matter? One reason: the hospital. Baylor Scott & White's Temple campus runs roughly eighty-eight hundred employees, plus around thirty-five hundred at the VA next door. Call it twelve-thousand-plus medical workers in a tight cluster. It's a Level I trauma center — twenty-four-seven shifts, which means people working nights, sleeping days, and needing housing close in.
    27	
    28	And it churns. Travel nurses and traveling clinicians cycle through on thirteen-week contracts, constantly. That's the part investors miss. You're not just betting on a stable employer — you're betting on a stable employer with built-in tenant turnover that *wants* short commutes and furnished options.
    29	
    30	Here's a tell from the data: roughly forty-seven percent of the active listings in this area literally cite proximity to Baylor Scott & White in the remarks. When half the sellers are using the hospital as the selling point, the rental thesis is already priced into the neighborhood's DNA. Your tenant demand isn't a hope. It's a payroll.
    31	
    32	To be clear — this is about who *rents* from you. I'm not telling anyone to move to Temple. I'm telling you who fills your unit.
    33	
    34	**[2:00–3:00 — ENTRY-PRICE REALITY (the numbers)]**
    35	Now the entry. Fresh pull, today. Closed median price in the Hospital District: a hundred forty-nine, nine ninety-nine. Active median list is sitting around a hundred sixty thousand, and the median works out to about a hundred twenty-six dollars a square foot.
    36	
    37	Compare that to Temple as a whole — citywide median runs somewhere in the two-seventy-five to three-fifteen range at roughly a hundred seventy-eight a foot. *(Verify that citywide number day-of — it moves.)* That means the Hospital District is trading at roughly fifty to sixty percent of the citywide median. This is the cheapest single-family entry near a major employer in Temple. Full stop.
    38	
    39	The stock explains the price. Seventy-five percent of these homes were built before 1960. The median build year is 1952. Median size, about eleven-hundred ninety-six square feet. Of around a hundred thirteen homes in the dataset, only six were built after 2000 — so new infill exists, but it's rare and it carries a premium.
    40	
    41	And you have leverage. Median days on market is about fifty-eight for closed homes, and sale-to-list is running around ninety-seven percent at the median — sellers are giving back two to seven points. In the distressed, as-is cluster the mean drops closer to ninety-three. Translation: this is a negotiating market for the buyer who shows up with cash and a contractor.
    42	
    43	**[3:00–5:10 — THE PLAYS, WITH TRANSPARENT MATH]**
    44	So how do you actually make money here? Four plays. I'll show the arithmetic on each so you can plug in your own rents — and you *should*, because my rent figures are from earlier research and you need to verify them the day you write the offer.
    45	
    46	**Play one — buy-and-hold, long-term rental.**
    47	Let's build a realistic all-in. Say you buy near the closed median: a hundred twenty thousand on an older home that needs work, plus a rehab to a livable rental standard. Budget thirty to fifty thousand for that — I'll use forty. That's roughly a hundred sixty thousand all-in.
    48	Long-term rent in this pocket, verify-day-of, lands somewhere around nine hundred to eleven hundred a month. Take the low end to stay honest: a thousand a month is twelve thousand a year gross.
    49	On older pre-1960 stock, your expense load is real — taxes, insurance, vacancy, repairs, management. Underwrite around forty-five percent of gross going to expenses. That leaves about sixty-six hundred a year in net operating income. Sixty-six hundred on a hundred-sixty-thousand all-in is a cap rate around four-point-one percent.
    50	Push rent to eleven hundred and trim expenses to forty percent — your NOI is about seventy-nine hundred, and your cap rate moves toward five percent. So you're underwriting a roughly four-to-five percent cap on a buy-and-hold. That's not a home run. That's a slow, boring, hospital-backed bond. Which brings us to the play that actually justifies this neighborhood.
    51	
    52	**Play two — the mid-term rental for travel nurses. This is the premium play.**
    53	Same hundred-sixty-thousand all-in, but you furnish it — call it eight to twelve thousand more in furniture and setup. Mid-term, furnished rent to a traveling clinician, verify-day-of, runs roughly fourteen hundred to eighteen hundred a month. Take fifteen hundred. That's eighteen thousand a year gross.
    54	Furnished mid-term carries higher operating costs — utilities, furnishings, turns, higher vacancy between contracts — so underwrite heavier, call it fifty percent expenses. That's nine thousand NOI on roughly a hundred seventy thousand all-in including the furniture. Cap rate around five-point-three percent, and on the high end of rent you're pushing past six and a half. The proximity to the hospital is the entire moat on this play — three to four minutes to BSW is what lets you charge the furnished premium. Nobody pays mid-term rates to live twenty minutes out.
    55	
    56	**Play three — value-add flip.**
    57	Buy at a hundred to a hundred-thirty, put in around forty in rehab, and your after-repair value targets roughly one-eighty to two-ten — and the comps support that ceiling. Look at South Seventh: eleven-oh-one sold at a hundred twenty thousand, ten-oh-eight square feet, built 1928. Twelve-oh-two sold at a hundred thirty-nine. But eleven-oh-two — thirteen-forty-four square feet, built 1965 — sold at a hundred ninety-two. Newer and bigger wins. So the flip thesis is real, but your exit depends on square footage and how updated it is, not the dirt alone. Run your seventy-percent-of-ARV-minus-rehab number hard, because in a ninety-seven-percent sale-to-list market your buyer has leverage too.
    58	
    59	**Play four — small multifamily.**
    60	About eight percent of these listings — nine of a hundred thirteen — are zoned commercial, multi-family, or mixed-use. There's a property at three-oh-nine South Thirty-First explicitly zoned multi-family. Duplex conversions and small multi exist here. If you want two doors on one foundation next to a hospital, this is one of the only Temple submarkets where the zoning cooperates.
    61	
    62	**[5:10–6:25 — THE FOUNDATION RISK = THE MOAT]**
    63	Now the part I refuse to soft-pedal, because if I do, someone buys a money pit on my word.
    64	These homes are pier-and-beam, sitting on Bell County black clay. Expansive clay. It swells when it's wet and shrinks when it's dry, and it moves your foundation with it. About four-point-four percent of the listings flag foundation issues outright — five homes name it directly — but I'll tell you straight, the real number is higher. Plenty of as-is sellers just don't disclose it. Thirty-three percent of these listings — thirty-seven of a hundred thirteen — mention as-is, rehab, repair, or foundation in the remarks. That's not a coincidence.
    65	So budget for it. Six thousand dollars minimum for foundation work, and the range runs five to fifteen depending on severity. And do not — *do not* — rely on a general home inspector for this. Hire a structural engineer. Different scope, different liability, different number. That's a non-negotiable line item, not an optional one.
    66	And it's not just the slab. Pre-1960 stock means galvanized plumbing that's rusting shut, outdated or knob-and-tube wiring, and asbestos and lead in anything built before 1978. That's why the all-in rehab to a livable rental standard is thirty to fifty thousand, not ten.
    67	Here's the reframe, and this is the whole game: that risk is your moat. The clay, the foundations, the asbestos — that's exactly what scares retail buyers and house-flippers-on-HGTV out of this neighborhood. It's *why* the median is sub-one-fifty next to a twelve-thousand-person employer. The day this becomes an easy, move-in-ready neighborhood, your entry price doubles. The friction is the opportunity. You don't want this to be easy. You want to be the one who can underwrite the hard part.
    68	
    69	**[6:25–7:15 — WHO IT'S FOR / NOT FOR]**
    70	So who is this for? It's for the buy-and-hold investor who wants recession-resistant tenant demand and will accept a four-to-five cap to get it. It's for the MTR operator who can run a furnished mid-term and capture the travel-nurse premium — that's where the real yield lives. And it's for the value-add flipper with a real contractor and a structural engineer on speed dial.
    71	Who is it *not* for? Anyone who wants passive and hands-off on day one. Anyone underwriting on rents they haven't verified this week. And anyone who hears "pier-and-beam on clay" and doesn't budget for it. If you need it to be pretty, or you need it to be easy, this neighborhood will punish you.
    72	
    73	**[7:15–7:50 — TAYLOR'S TAKE / VERDICT]**
    74	Here's what I'd actually do. If I'm buying my next one here — and I might — I'm buying the worst house I can structurally fix on the best block I can find, I'm running it as a furnished mid-term for the hospital, and I'm underwriting the foundation before I underwrite the upside. I'd take a five-cap MTR with payroll-backed demand over a flashier deal in a neighborhood with no employer behind it. Boring and backed beats exciting and exposed. I've made that bet twice on South Seventh. It's why I can talk about it instead of just listing it.
    75	
    76	**[7:50–8:20 — CTA]**
    77	I built a full breakdown of the Hospital District on my site — the subdivision-by-subdivision data, the comps, and the investor plays — and it's linked in the description and pinned in the comments. If you're underwriting a deal here, that page is your starting point. And if you want me to run the numbers on a specific property, the offer's in the description too. Verify your rents the day you write the offer. Hire the structural engineer. And don't let the ugly scare you off the math. I'm Taylor Dasch. I'll see you on the next one.
    78	
    79	---
    80	
    81	## 2. HOOK VARIANTS (first 15s — NO entity declaration)
    82	
    83	**Hook A — The Number**
    84	There's a neighborhood in Temple, Texas where the median house closed this year for a hundred forty-nine thousand, nine hundred ninety-nine dollars — three to four minutes from a twelve-thousand-person hospital workforce. I own two houses on this street. Here's the math, and the one risk that keeps your entry this cheap.
    85	
    86	**Hook B — The Contrarian**
    87	This is not a pretty neighborhood. It's a smart one. Sub-one-fifty single-family, next to the biggest employer in Temple, and most investors won't touch it for one reason. I bought here twice — let me show you why the ugly is the opportunity.
    88	
    89	**Hook C — The Moat**
    90	The reason houses near Temple's hospital still close under a hundred fifty grand isn't location. It's the dirt underneath them. Expansive clay scares retail buyers off — and it's exactly why this is the cheapest single-family cash-flow entry in the city. I own two of these. Here's how the numbers actually pencil.
    91	
    92	---
    93	
    94	## 3. TITLE + 7-SECTION DESCRIPTION
    95	
    96	**TITLE:**
    97	This Temple TX Neighborhood Cash-Flows Next to a Hospital — Houses Under $150K (Investor Breakdown)
    98	
    99	*Alt:* Why Investors Buy Sub-$150K Houses by Temple TX's Hospital (Cap Rate Math + The Clay Risk)
   100	
   101	---
   102	
   103	**[Section 1 — Hook line / one-sentence promise]**
   104	Single-family houses closing under $150K, three to four minutes from a 12,000-person hospital workforce in Temple, TX — here's the full investor breakdown with transparent cap-rate math, the four plays, and the foundation risk nobody warns you about.
   105	
   106	**[Section 2 — What you'll learn]**
   107	- Why the Hospital District trades at ~50–60% of Temple's citywide median
   108	- The BSW tenant-demand engine: 12,000+ medical workers + travel-nurse churn
   109	- 4 investor plays (LTR, MTR for travel nurses, value-add flip, small multifamily) with the actual arithmetic
   110	- Why pier-and-beam on Bell County clay is both your biggest risk AND your moat
   111	- Who this neighborhood is for — and who it'll punish
   112	
   113	**[Section 3 — Timestamps]**
   114	0:00 The $149,999 median (the hook)
   115	0:18 Who I am + why I have skin in this dirt
   116	0:48 Naming the market: the Hospital District
   117	1:05 The demand engine — Baylor Scott & White
   118	2:00 Entry-price reality (fresh MLS numbers)
   119	3:00 Play 1 — Buy-and-hold LTR (cap-rate math)
   120	3:50 Play 2 — MTR for travel nurses (the premium play)
   121	4:30 Play 3 — Value-add flip + S 7th comps
   122	4:55 Play 4 — Small multifamily / duplex zoning
   123	5:10 The foundation & clay risk = the moat
   124	6:25 Who it's for / who it's NOT for
   125	7:15 My take — what I'd actually buy
   126	7:50 Resources + how to get a deal analyzed
   127	
   128	**[Section 4 — Entity declaration / about]**
   129	Taylor Dasch with EG Realty — Temple, TX. $30M+ in volume, 100+ transactions, 3-year BiggerPockets Featured Agent, ranked #28 of 2,013 Bell County agents. I own and have rehabbed homes in this exact neighborhood (1805 & 1814 S 7th). I help investors underwrite buy-and-hold, BRRRR, MTR, and value-add deals in the Temple market.
   130	
   131	**[Section 5 — Resources / links]**
   132	Full Hospital District investor breakdown (subdivision data, comps, all four plays):
   133	https://templetxhomes.net/hospital-district/?utm_source=youtube&utm_medium=description&utm_campaign=hospital-district-investor
   134	Want me to run the numbers on a specific property? Comment the address or reach me below.
   135	
   136	**[Section 6 — Contact]**
   137	Taylor Dasch | EG Realty
   138	254-718-4249 | dealswithdasch@gmail.com
   139	templetxhomes.net
   140	
   141	**[Section 7 — Disclaimer / hashtags + verify note]**
   142	Rent figures are research-based estimates — verify current rents the day you write your offer. Cap-rate examples are illustrative methodology, not guaranteed returns; plug in your own numbers. Always hire a licensed structural engineer before purchasing pier-and-beam stock. Not investment advice.
   143	#TempleTX #RealEstateInvesting #BRRRR #MidTermRentals #CashFlow #TexasRealEstate #RentalProperty #InvestingInTemple
   144	
   145	---
   146	
   147	## 4. THUMBNAIL BRIEF
   148	
   149	**Concept:** Split-tension thumbnail — cheap entry vs. big institution. Left: a modest 1950s Hospital District bungalow exterior (slightly worn, real, not staged). Right or background: the BSW hospital tower / skyline. Bold price tag overlay bridges the two.
   150	
   151	**Text overlay (≤4 words):** `$149K NEXT TO THIS` — with `$149K` huge on the house side and an arrow pointing to the hospital. (Backup: `UNDER $150K`)
   152	
   153	**Visual direction:**
   154	- High-contrast, slightly desaturated to signal "honest/analyst," not glossy real-estate.
   155	- Yellow or red price tag for the dollar figure (high CTR contrast against muted house tones).
   156	- Optional small circle inset of Taylor (arms-crossed, neutral, credible — not smiling-realtor).
   157	- A subtle crack/foundation line motif at the bottom edge to hint at the risk hook without being literal.
   158	- No IDX, no logos clutter. One number, one tension, one face.
   159	
   160	---
   161	
   162	## 5. B-ROLL SHOT LIST (dense — 7-second rule)
   163	
   164	| # | Shot | Use over (script beat) |
   165	|---|------|------------------------|
   166	| 1 | Slow push-in on a 1950s pier-and-beam bungalow exterior, worn but solid | Hook / 0:00 |
   167	| 2 | Tight on a "Sold" or for-sale rider sign, address blurred | Entry-price reality |
   168	| 3 | Taylor walking up to 1805 / 1814 S 7th, keys in hand | Credibility / skin-in-the-dirt |
   169	| 4 | Dashcam/POV drive: bungalow block → BSW campus, clock/timer overlay "3–4 min" | Demand engine |
   170	| 5 | BSW hospital tower exterior + signage (Baylor Scott & White) | Demand engine |
   171	| 6 | VA facility exterior signage | "+3,500 VA" line |
   172	| 7 | Busy hospital entrance / shift-change foot traffic (or stock parking lot fill) | 24/7 shifts / travel-nurse churn |
   173	| 8 | Screen-recording scroll of MLS remarks highlighting "near BSW" | 47% cite proximity |
   174	| 9 | Clean on-screen data card: "$149,999 median · $126/sqft · 1952 build · 75% pre-1960" | Entry-price reality |
   175	| 10 | Crawlspace / pier-and-beam underside footage (flashlight, real) | Foundation risk |
   176	| 11 | Close-up of cracked drywall / sloping floor / shimmed pier | Foundation risk |
   177	| 12 | Dried, cracked black-clay soil close-up | Bell County clay |
   178	| 13 | Structural engineer's report / level on a floor | "Hire a structural engineer" |
   179	| 14 | Galvanized pipe / old electrical panel / knob-and-tube detail | Other rehab risks |
   180	| 15 | Rehab before→after split (gutted room → finished rental-grade room) | Value-add play |
   181	| 16 | Furnished bedroom/living setup (MTR-style, clean, simple) | MTR play |
   182	| 17 | Block-by-block street variance: one updated house next to one rough one | Block matters / S 7th comps |
   183	| 18 | On-screen comp table: 1101 / 1202 / 1814 / 1102 S 7th | Flip comps |
   184	| 19 | 1914 Coffee House exterior near BSW | Walkable amenity (light) |
   185	| 20 | Taylor piece-to-camera, arms crossed, neutral delivery | Verdict / take |
   186	
   187	---
   188	
   189	## 6. SHORTS CUTS (≤60s each; title includes "Temple TX")
   190	
   191	**SHORT 1 — "The $149K Number" (≈45s)**
   192	*Title:* Houses Under $150K Next to a Hospital in Temple TX
   193	*Script:*
   194	"A single-family house in this Temple, Texas neighborhood closed this year for a median of a hundred forty-nine thousand, nine hundred ninety-nine. Three to four minutes from a twelve-thousand-person hospital workforce. So why is it this cheap? Because these homes sit on pier-and-beam over Bell County clay, and that scares retail buyers off — which is exactly why the median is sub-one-fifty next to the biggest employer in town. I own two houses on this street and rehabbed both. The clay isn't the problem. It's the moat. Budget six grand-plus for foundation work, hire a structural engineer, and you're buying cash flow nobody else will touch. Full breakdown's pinned."
   195	*On-screen:* `$149,999 MEDIAN` → `3–4 MIN TO HOSPITAL` → `THE CLAY = THE MOAT`
   196	
   197	**SHORT 2 — "The Travel-Nurse Play" (≈50s)**
   198	*Title:* The Best Rental Play Near Temple TX's Hospital
   199	*Script:*
   200	"Here's the highest-yield play in Temple, Texas right now and almost nobody runs it. There's a hospital here with twelve thousand-plus medical workers and constant travel-nurse turnover — thirteen-week contracts, cycling through all year. You buy an older house three minutes away, all-in around a hundred seventy thousand including furniture, and you run it as a furnished mid-term rental. Verify rents day-of, but furnished mid-term in this pocket runs roughly fourteen to eighteen hundred a month versus a thousand for a long-term lease. That proximity to the hospital is the entire moat — nobody pays mid-term rates to live twenty minutes out. I own two houses on this street. Plays linked below."
   201	*On-screen:* `12,000+ MEDICAL WORKERS` → `13-WEEK CONTRACTS` → `MTR > LTR HERE`
   202	
   203	**SHORT 3 — "Don't Skip the Engineer" (≈40s)**
   204	*Title:* The $6K Mistake Investors Make in Temple TX
   205	*Script:*
   206	"If you buy an older house near Temple, Texas's hospital and you only hire a general home inspector, you're gambling. These are pier-and-beam homes on expansive black clay. Around a third of the listings mention as-is, rehab, or foundation issues — and the real number's higher because as-is sellers don't always disclose. Budget six thousand minimum for foundation work, five to fifteen depending on severity, and hire a structural engineer — not just an inspector. Different scope, different number. I've written these checks on my own houses here. The math only works if you underwrite the dirt first."
   207	*On-screen:* `PIER & BEAM` → `BELL COUNTY CLAY` → `HIRE A STRUCTURAL ENGINEER`
   208	
   209	---
   210	
   211	## 7. PINNED COMMENT
   212	
   213	Full Hospital District investor breakdown — subdivision-by-subdivision data, comps, and all four plays (LTR, MTR for travel nurses, value-add flip, small multifamily):
   214	https://templetxhomes.net/hospital-district/?utm_source=youtube&utm_medium=description&utm_campaign=hospital-district-investor
   215	
   216	Two reminders before you write an offer: (1) verify current rents the day you offer — my figures are research-based estimates, and (2) hire a structural engineer on any pier-and-beam home, not just a general inspector. Drop an address below and I'll run the numbers with you. — Taylor
   217	
   218	---
   219	
   220	### COMPLIANCE SELF-CHECK
   221	- Banned words: none present (anti-passive phrased as "passive and hands-off" / "move-in-ready"; "turnkey" not used). ✓
   222	- Entity declaration: lands 0:18–0:48, not in first 15s. ✓
   223	- Lane: investor-only; BSW = tenant-demand engine only; explicit "I'm not telling anyone to move to Temple"; no military; no buyer-lifestyle. ✓
   224	- Math: gross → expense load → NOI → cap rate shown transparently; rents labeled verify-day-of; no single hard cap rate as gospel. ✓
   225	- Foundation/clay: unflinching + framed as the moat. ✓
   226	- Lived experience (1805 & 1814 S 7th) front and center. ✓
   227	- Fresh MLS numbers used ($149,999, $126/sqft, 1952, 75% pre-1960, ~97% sale-to-list, ~58 DOM). ✓

exec
/bin/zsh -lc "nl -ba r1-A.md | sed -n '240,340p'" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/hospital-district/reason-run-260527-1120
 succeeded in 0ms:
codex
FATAL WEAKNESSES (must fix or kill):
1. “I'm Taylor Dasch with EG Realty.” — Identity lands after 0:15, which is good, but it is not in the first 3 sentences. The hook burns eight sentence breaks before the entity declaration, so it fails the stated format spec. — Rewrite the open so sentence 3 starts at ~0:14: “A $149,999 closed median three to four minutes from Baylor Scott & White sounds like a typo. It is not, and the reason is old pier-and-beam housing on Bell County clay. I’m Taylor Dasch with EG Realty, and I own two houses on this street, so here’s the underwriting case before you call it a deal.”

2. Shorts 1–3 contain no “Taylor Dasch with EG Realty” entity declaration. — Public-facing video assets fail the identity rule, and Shorts are not exempt. — Add the entity line after the hook but inside the first 3 spoken sentences, paced after 0:15 if required.

3. “Say you buy near the closed median: a hundred twenty thousand…” — $120K is not near the stated $149,999 closed median; the cap-rate math depends on a below-median distressed purchase while the title/packaging sells “under $150K” cash flow. A real investor will call this bait-and-switch. — Rewrite: “At a $120K distressed purchase plus $40K rehab, you’re at $160K before closing costs. At the actual $149,999 median plus $40K rehab, the same $1,000 rent is closer to a 3.5% cap before debt, so this only works if you buy below median, control rehab, or capture the MTR premium.”

4. “Screen-recording scroll of MLS remarks highlighting ‘near BSW’” — Publicly showing MLS remarks/UI can create MLS copyright/display-rule problems unless explicitly permitted. Cannot ship as a production instruction. — Rewrite: “Recreated data graphic from permitted MLS-derived aggregate: ‘47% of sampled listings referenced BSW proximity,’ with source/date note. Do not show MLS UI or verbatim agent remarks.”

MAJOR WEAKNESSES (must fix to ship cleanly):
1. “Your tenant demand isn't a hope. It's a payroll.” — Dehumanizing and easy for a BSW group chat to quote as “agent treats hospital workers like income units.” — Rewrite: “The rental thesis is tied to a large, shift-based employment center, not a vague hope that tenants appear.”

2. “And it churns.” — Describing nurses/clinicians as churn is ugly in the wrong way. — Rewrite: “Staffing cycles create recurring furnished-rental demand, especially from clinicians on 13-week contracts.”

3. “The day this becomes an easy, move-in-ready neighborhood, your entry price doubles.” — Unsupported forward-looking price forecast. — Rewrite: “If the condition risk were already solved, the discount would probably be much thinner.”

4. “That’s a slow, boring, hospital-backed bond.” — Implies durable/secure investment behavior and invites securities-style criticism. — Rewrite: “That is a lower-yield, condition-sensitive rental play tied to a durable employment base.”

5. “Cap rate around five-point-three percent, and on the high end of rent you're pushing past six and a half.” — At $1,800 rent, 50% expense load, and $170K all-in, NOI is $10,800 and cap is ~6.35%, not past 6.5%. — Rewrite: “On the high end, you’re around the low-to-mid sixes before debt, depending on expense load.”

6. “The clay isn't the problem. It's the moat.” — Clippable and false; the clay absolutely is the problem. — Rewrite: “The clay is the problem, and the discount only works if you price that problem correctly.”

7. “Here’s the highest-yield play in Temple, Texas right now…” — Overbroad market claim with no proof across all Temple rental strategies. — Rewrite: “In this pocket, the MTR case is the yield angle I’d test first.”

8. “Drop an address below and I'll run the numbers with you.” — Commits Taylor to public deal analysis and creates operational/compliance expectations. — Rewrite: “For property-specific underwriting, use the contact link and send the address privately.”

9. “Plenty of as-is sellers just don't disclose it.” — Broad accusation against sellers; unnecessary liability surface. — Rewrite: “Foundation issues do not always show up in listing remarks, so absence of the phrase is not clearance.”

10. “BSW hospital tower exterior + signage” / “VA facility exterior signage” / “busy hospital entrance / shift-change foot traffic” — Risks implying institutional affiliation and showing identifiable staff/patients. — Rewrite: “Use public exterior/context footage only, avoid identifiable people/badges, avoid logo-heavy thumbnail treatment, and add no-affiliation language if BSW/VA are visually prominent.”

MINOR WEAKNESSES (polish):
1. “skin in the dirt” — Forced metaphor. — Rewrite: “actual money in the neighborhood.”
2. “Full stop.” — Internet-comment cadence, not analyst register. — Cut it.
3. “Who it'll punish” — Reads performative in the description. — Rewrite: “Who should avoid it.”
4. “This Temple TX Neighborhood Cash-Flows…” — Too absolute given the base LTR math. — Rewrite: “Temple TX Hospital District Investor Breakdown: Under-$150K Houses, MTR Math, Clay Risk.”

DOMAIN CHECKS:
- Identity timing: FAIL. Long-form timing is after 0:15, but not in first 3 sentences; Shorts have no entity declaration.
- Banned vocabulary: clean in the draft itself.
- Lane discipline: PASS. Investor lane holds; no buyer/relocation framing leaks in.
- Forecast surface: FAIL. “entry price doubles,” “highest-yield play right now,” “cash-flows,” and “nobody pays mid-term rates…” are overclaims.
- Data provenance: FAIL. Local task data supports the MLS numbers, but the public package lacks source/date/boundary notes for MLS-derived stats, citywide median, employment counts, ranking, and rent estimates.

VERDICT: REVISE

ONE-LINE REASON: The concept is usable, but the current draft fails identity-format rules, overstates the math, and gives hostile viewers too many easy clips to frame Taylor as hype-first instead of analyst-first.
tokens used
119,090
FATAL WEAKNESSES (must fix or kill):
1. “I'm Taylor Dasch with EG Realty.” — Identity lands after 0:15, which is good, but it is not in the first 3 sentences. The hook burns eight sentence breaks before the entity declaration, so it fails the stated format spec. — Rewrite the open so sentence 3 starts at ~0:14: “A $149,999 closed median three to four minutes from Baylor Scott & White sounds like a typo. It is not, and the reason is old pier-and-beam housing on Bell County clay. I’m Taylor Dasch with EG Realty, and I own two houses on this street, so here’s the underwriting case before you call it a deal.”

2. Shorts 1–3 contain no “Taylor Dasch with EG Realty” entity declaration. — Public-facing video assets fail the identity rule, and Shorts are not exempt. — Add the entity line after the hook but inside the first 3 spoken sentences, paced after 0:15 if required.

3. “Say you buy near the closed median: a hundred twenty thousand…” — $120K is not near the stated $149,999 closed median; the cap-rate math depends on a below-median distressed purchase while the title/packaging sells “under $150K” cash flow. A real investor will call this bait-and-switch. — Rewrite: “At a $120K distressed purchase plus $40K rehab, you’re at $160K before closing costs. At the actual $149,999 median plus $40K rehab, the same $1,000 rent is closer to a 3.5% cap before debt, so this only works if you buy below median, control rehab, or capture the MTR premium.”

4. “Screen-recording scroll of MLS remarks highlighting ‘near BSW’” — Publicly showing MLS remarks/UI can create MLS copyright/display-rule problems unless explicitly permitted. Cannot ship as a production instruction. — Rewrite: “Recreated data graphic from permitted MLS-derived aggregate: ‘47% of sampled listings referenced BSW proximity,’ with source/date note. Do not show MLS UI or verbatim agent remarks.”

MAJOR WEAKNESSES (must fix to ship cleanly):
1. “Your tenant demand isn't a hope. It's a payroll.” — Dehumanizing and easy for a BSW group chat to quote as “agent treats hospital workers like income units.” — Rewrite: “The rental thesis is tied to a large, shift-based employment center, not a vague hope that tenants appear.”

2. “And it churns.” — Describing nurses/clinicians as churn is ugly in the wrong way. — Rewrite: “Staffing cycles create recurring furnished-rental demand, especially from clinicians on 13-week contracts.”

3. “The day this becomes an easy, move-in-ready neighborhood, your entry price doubles.” — Unsupported forward-looking price forecast. — Rewrite: “If the condition risk were already solved, the discount would probably be much thinner.”

4. “That’s a slow, boring, hospital-backed bond.” — Implies durable/secure investment behavior and invites securities-style criticism. — Rewrite: “That is a lower-yield, condition-sensitive rental play tied to a durable employment base.”

5. “Cap rate around five-point-three percent, and on the high end of rent you're pushing past six and a half.” — At $1,800 rent, 50% expense load, and $170K all-in, NOI is $10,800 and cap is ~6.35%, not past 6.5%. — Rewrite: “On the high end, you’re around the low-to-mid sixes before debt, depending on expense load.”

6. “The clay isn't the problem. It's the moat.” — Clippable and false; the clay absolutely is the problem. — Rewrite: “The clay is the problem, and the discount only works if you price that problem correctly.”

7. “Here’s the highest-yield play in Temple, Texas right now…” — Overbroad market claim with no proof across all Temple rental strategies. — Rewrite: “In this pocket, the MTR case is the yield angle I’d test first.”

8. “Drop an address below and I'll run the numbers with you.” — Commits Taylor to public deal analysis and creates operational/compliance expectations. — Rewrite: “For property-specific underwriting, use the contact link and send the address privately.”

9. “Plenty of as-is sellers just don't disclose it.” — Broad accusation against sellers; unnecessary liability surface. — Rewrite: “Foundation issues do not always show up in listing remarks, so absence of the phrase is not clearance.”

10. “BSW hospital tower exterior + signage” / “VA facility exterior signage” / “busy hospital entrance / shift-change foot traffic” — Risks implying institutional affiliation and showing identifiable staff/patients. — Rewrite: “Use public exterior/context footage only, avoid identifiable people/badges, avoid logo-heavy thumbnail treatment, and add no-affiliation language if BSW/VA are visually prominent.”

MINOR WEAKNESSES (polish):
1. “skin in the dirt” — Forced metaphor. — Rewrite: “actual money in the neighborhood.”
2. “Full stop.” — Internet-comment cadence, not analyst register. — Cut it.
3. “Who it'll punish” — Reads performative in the description. — Rewrite: “Who should avoid it.”
4. “This Temple TX Neighborhood Cash-Flows…” — Too absolute given the base LTR math. — Rewrite: “Temple TX Hospital District Investor Breakdown: Under-$150K Houses, MTR Math, Clay Risk.”

DOMAIN CHECKS:
- Identity timing: FAIL. Long-form timing is after 0:15, but not in first 3 sentences; Shorts have no entity declaration.
- Banned vocabulary: clean in the draft itself.
- Lane discipline: PASS. Investor lane holds; no buyer/relocation framing leaks in.
- Forecast surface: FAIL. “entry price doubles,” “highest-yield play right now,” “cash-flows,” and “nobody pays mid-term rates…” are overclaims.
- Data provenance: FAIL. Local task data supports the MLS numbers, but the public package lacks source/date/boundary notes for MLS-derived stats, citywide median, employment counts, ranking, and rent estimates.

VERDICT: REVISE

ONE-LINE REASON: The concept is usable, but the current draft fails identity-format rules, overstates the math, and gives hostile viewers too many easy clips to frame Taylor as hype-first instead of analyst-first.
