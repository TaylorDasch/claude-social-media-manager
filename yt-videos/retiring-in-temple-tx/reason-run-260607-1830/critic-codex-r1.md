Reading prompt from stdin...
2026-06-07T23:36:05.235978Z ERROR codex_core::session: failed to load skill /Users/taylordasch_1/.claude/skills/geo-query-finder/SKILL.md: missing YAML frontmatter delimited by ---
2026-06-07T23:36:05.235993Z ERROR codex_core::session: failed to load skill /Users/taylordasch_1/.agents/skills/repurpose-tree/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 99
OpenAI Codex v0.128.0 (research preview)
--------
workdir: /Users/taylordasch_1/claude-social-media-manager/yt-videos/retiring-in-temple-tx/reason-run-260607-1830
model: gpt-5.5
provider: openai
approval: never
sandbox: read-only
reasoning effort: xhigh
reasoning summaries: none
session id: 019ea471-8b76-7370-8cf7-a1ba5de14dd9
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
  - **Living in Temple channel:** BSW medical hires, military PCS-window buyers (Fort Cavazos), DFW/Austin relocators
  - **Investing in Temple channel:** investors only — NEVER mix
- Banned vocabulary: dream home, charming, nestled, turnkey, hidden gem, perfect (neighborhood/home), exclusive, stunning, gorgeous, paradise, oasis, picturesque, "you'll love," "won't last," "must see," boasts, "a true gem," "one-of-a-kind," sneak peek, white glove, "my expertise," insider, dream
- Lane discipline: NO investor framing on buyer content (no cap rates, no cash flow, no rental analysis on a Living in Temple piece); NO buyer framing on investor content
- BSW guardrails: lender channel only (Stark Law); never direct-to-physician outreach
- Format rules: identity declaration must appear in first 3 sentences but NOT in first 15 seconds of video; ONE creative element per video, not three; honest negatives included

TASK:

Attack this draft ruthlessly. Imagine the most informed hostile commenter on r/TempleTX, a BSW physician group chat, or a Fort Cavazos spouse Facebook group — what would they tear apart? What would an industry-savvy competitor agent quote out of context to discredit Taylor?

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

=== CANDIDATE TO CRITIQUE ===
# Candidate A — Round 1 (Author-A, cold start)
# "Retiring in Temple, TX" — Living in Temple

## 3 HOOK VARIANTS

**Hook 1 (Contrarian — Georgetown):**
"Every retirement guide in Texas points you to Georgetown's Sun City. I'm going to make the case for the city 30 minutes north that nobody markets to you — Temple — and then I'm going to tell you the one kind of person who should ignore everything I'm about to say and go to Georgetown anyway."

**Hook 2 (Healthcare-led):**
"If you're picking where to retire and you're being honest, the real question isn't the golf course or the granite countertops. It's: where's the nearest Level I trauma center when something goes wrong at 2 AM? In Temple, Texas, the answer is ten minutes away. In most retirement towns, it's an hour. That changes everything."

**Hook 3 (Money/contrarian):**
"You can buy the same house in Temple, Texas for about 60% of what it costs in Georgetown — and Temple has a Level I trauma center Georgetown doesn't. So why does everyone still tell retirees to go to Georgetown? Let me show you what's actually going on."

---

## FULL WORD-FOR-WORD SCRIPT (~1,350 words / ~8.5 min)

**[0:00-0:12 — HOOK. Talking head, no name yet.]**
Every retirement guide in Texas points you to Georgetown's Sun City. I'm going to make the case for the city 30 minutes north that nobody markets to you — Temple — and then I'm going to tell you the one kind of person who should ignore everything I'm about to say and go to Georgetown anyway.

**[0:12-0:30 — Identity + frame. B-roll: BSW campus exterior.]**
I'm Taylor Dasch with EG Realty. I've done over $28 million in transactions here in Temple and Belton, and I work with retirees and downsizers almost every week. So this isn't a brochure. This is the honest version — what's great, what's missing, and who this city is wrong for.

**[0:30-0:50 — The thesis. LOWER-THIRD: "Healthcare-first retirement."]**
Here's the thesis. Temple is the highest-healthcare, lowest-cost serious retirement option on the entire I-35 corridor. The reason you've never heard that is simple: Temple doesn't market itself like a retirement destination. It's a working medical city. But that's exactly why it works.

**[0:50-1:40 — HEALTHCARE. B-roll: BSW, VA hospital. GRAPHIC: "636-bed Level I trauma center."]**
Let's start with the thing that actually matters as you age — healthcare. Baylor Scott & White in Temple is a 636-bed Level I trauma center. That's the only Level I trauma center on I-35 between Dallas and Austin. Thirty-plus specialties. Eighty-eight hundred-plus employees. There's a reason for that: Temple is the regional medical hub — people drive *to* Temple for care.

And here's the counterintuitive part. Because Temple is the referral center, specialist wait times are often *shorter* than in Austin. A cardiology consult here books in about two to three weeks, versus four to six in Austin. Verify that for your own situation — but the pattern holds.

There's also a full VA hospital right in town — the Olin E. Teague Veterans' Medical Center. If you're a military retiree, that dual access — VA plus Baylor Scott & White — is rare in a city this size.

**[1:40-2:00 — Pull-quote moment. Talking head.]**
I'll put it the way I see it after years of doing this: most retirees who end up in Temple came for the hospital and stayed for the cost of living. The ones who leave came for the cost of living and left because of the boredom. Hold onto that — we'll come back to it.

**[2:00-3:00 — MONEY: taxes. GRAPHIC: "Over-65 school-tax freeze."]**
Now the money, because this is where Texas does something most states don't. First — no state income tax. Your Social Security, your pension, your 401(k) withdrawals — none of it gets taxed at the state level. If you're coming from a state with a 5% income tax drawing 60 grand a year, that's roughly three thousand dollars a year back in your pocket. From California, it can be over five.

Second — and almost nobody knows this until after they buy — the over-65 school-tax freeze. Once you turn 65 and file the over-65 homestead exemption, your school district taxes freeze at the dollar amount you owed that year. Not the rate — the dollar amount. Forever. Plus an extra ten-thousand-dollar exemption. On a 300-thousand-dollar home, the combined over-65 breaks save you somewhere around twenty-four hundred to thirty-two hundred a year.

Here's the part people miss: that freeze *transfers* if you move within Texas — but it's proportional, not dollar-for-dollar, and you have to file Form 50-132 with the new county within one year. Miss that deadline and you lose it. Mark your calendar.

**[3:00-3:45 — MONEY: cost of living + comparison. GRAPHIC: comparison card Temple vs Georgetown.]**
Put it together with the home prices and the gap gets loud. Median home in Temple is around 255 thousand. Georgetown's around 425. Fredericksburg's pushing 490 and up. So you're looking at the same house for roughly 60% of the Georgetown cost — call it 170 grand cheaper — and Temple has the Level I trauma center Georgetown doesn't. Georgetown drives to Austin for that.

A retired couple here runs about thirty-five hundred to forty-six hundred a month all in. These are ranges — verify current numbers when you're actually shopping, because medians move.

**[3:45-4:45 — HOUSING. B-roll: single-story drives in Bella Terra, Lake Pointe, Three Creeks.]**
So where do people actually buy? Let me tell you the pattern, because it's almost funny how consistent it is. Retirees come to me wanting a big lot — a ranch-style place with some acreage. And then, every single time, they end up buying a newer single-story in a community like Bella Terra or Three Creeks instead.

Why? Because on a fixed income, a fifteen-thousand-dollar foundation repair or a twelve-thousand-dollar roof is a budget-breaking event. Newer construction — 2018 and later — means builder warranties, modern HVAC, energy-efficient, single-story floor plans built for accessibility. Four areas I'd point you to: Bella Terra — newer, closest to the hospital, my top pick. Three Creeks — Belton Lake trails, best for active retirees. Canyon Creek — bigger lots, mature trees, best value. Lake Pointe — single-story, lower-maintenance, easier on the budget.

**[4:45-6:00 — THE HONEST NEGATIVE. Talking head, serious. LOWER-THIRD: "Who should NOT retire here."]**
Now the part most agents won't say out loud. Here's who should *not* retire in Temple.

Number one — and this is the big one — Temple does not have a Sun City. There is no large 55-plus, gated, golf-cart, activities-director community here. We've got exactly one 55-plus apartment community. If that resort lifestyle — the amenity center, the organized social calendar, the golf cart to your neighbor's — if that's the dealbreaker for you, then Georgetown is genuinely the better call. I'm not going to pretend otherwise.

Number two — the summers are brutal. Ninety-four to ninety-eight degrees, June through August, twenty to forty days over a hundred. Your summer electric bill runs two to three-fifty a month. Plan your outdoor life around October to May.

Number three — you need to be able to drive. Temple is car-dependent. The micro-transit is limited and there's no reliable rideshare like Austin. If you're at the stage where driving is ending, Temple is hard without family nearby.

And number four — there's no continuing-care retirement community, no CCRC, the kind where you buy into one campus that takes you from independent living all the way through memory care. The nearest ones are in the Austin metro. If you're retiring solo and planning for escalating care, that's a real gap.

**[6:00-7:00 — TAYLOR'S TAKE. Talking head, personal.]**
Let me make this real. My own parents are looking at retiring here, from Mansfield. What I tell them is the same thing I'll tell you: it's not as upscale as where they are now — but their money goes dramatically further. A 350-thousand-dollar home here buys what 550-plus gets you in Mansfield, and the healthcare is comparable or better, because Baylor Scott & White is a Level I trauma center. The tradeoff is dining and entertainment — you'll drive to Austin, about an hour, when you want a nice dinner or a show. That's the honest deal.

And the biggest real reason people land here? Family. A lot of folks come to be near kids and grandkids who already work at Baylor Scott & White or Fort Hood. Close enough to visit daily, affordable enough to buy outright or with a small mortgage, and the hospital's right there for peace of mind.

**[7:00-7:45 — VERDICT + CTA. Talking head.]**
So here's my verdict. Temple is the right retirement move for practical people who put healthcare, cost, and family first. It is the wrong move for people who want a resort lifestyle. Know which one you are before you start looking — that one decision saves you a year of regret.

If you're the practical type, I built a full written breakdown — the tax-freeze math, the neighborhoods, the healthcare detail — and it's linked in the description and pinned in the comments. And if you want to talk through whether Temple actually fits your situation, my number's down there too. I'm Taylor Dasch. I'll see you in the next one.

---

## TALKING-POINTS / TELEPROMPTER-LIGHT VERSION

- **HOOK:** Everyone says Georgetown's Sun City. Make the case for Temple 30 min north — then name the one person who should ignore me and go to Georgetown.
- **IDENTITY:** Taylor Dasch, EG Realty. $28M+ Temple/Belton. Work with retirees weekly. Honest version, not a brochure.
- **THESIS:** Highest-healthcare, lowest-cost serious retirement option on I-35. Doesn't market itself = working medical city = why it works.
- **HEALTHCARE:** BSW = 636-bed Level I trauma center, only one on I-35 Dallas↔Austin. 30+ specialties, 8,800+ staff. Regional hub → specialist waits SHORTER (cardiology ~2-3 wk vs 4-6 Austin — verify). VA hospital (Olin E. Teague) in town → dual access for military.
- **PULL-QUOTE:** Came for the hospital, stayed for the cost of living. The ones who leave came for cost, left from boredom.
- **TAXES:** No state income tax (SS/pension/401k). ~$3K/yr saved from a 5% state, $5K+ from CA. Over-65 school-tax FREEZE at dollar amount, forever + extra $10K exemption = ~$2,400-3,200/yr on $300K. Transfers but proportional + Form 50-132 within 1 year or lose it.
- **COST/COMPARISON:** Median ~$255K vs Georgetown ~$425K vs Fredericksburg ~$490K+. ~60% of Georgetown cost, ~$170K cheaper, WITH the Level I Georgetown lacks. Couple ~$3,530-4,580/mo. Ranges — verify.
- **HOUSING:** Pattern: want acreage, buy newer single-story every time. Fixed income → $15K foundation/$12K roof = budget-breaker. 2018+ = warranties, modern HVAC, accessible. Bella Terra (top pick, near hospital), Three Creeks (active/lake), Canyon Creek (value/lots), Lake Pointe (budget single-story).
- **WHO SHOULD NOT (mandatory):** (1) No Sun City — one 55+ apartment only; resort lifestyle dealbreaker → GO TO GEORGETOWN, say it. (2) Brutal summers 94-98°F, $200-350 electric. (3) Must be able to drive — car-dependent, no real rideshare. (4) No CCRC — nearest Austin metro; gap for solo progressive-care planners.
- **TAYLOR'S TAKE:** Parents from Mansfield. $350K here = $550K+ Mansfield, healthcare comparable/better. Tradeoff = dining/shows, drive to Austin ~1hr. Biggest driver = family near BSW/Fort Hood kids/grandkids.
- **VERDICT:** Right for practical/healthcare/cost/family. Wrong for resort lifestyle. Know which you are.
- **CTA:** Written breakdown in description + pinned comment. Phone in description.

---

## 3 YOUTUBE TITLES (≤60 chars)

1. `Retiring in Temple TX: The Honest Georgetown Alternative` (56)
2. `Why Retirees Quietly Pick Temple TX Over Georgetown` (51)
3. `Retiring in Temple, TX — Healthcare, Taxes & the Catch` (53)

---

## 3 THUMBNAIL CONCEPTS

1. **TEMPLE vs GEORGETOWN** — split screen, BSW hospital on Temple side, "$255K" vs "$425K" big numbers. Overlay: "TEMPLE vs GEORGETOWN."
2. **Healthcare-led** — Taylor pointing at BSW tower, red "LEVEL I" stamp. Overlay: "THE 10-MINUTE HOSPITAL."
3. **The catch** — Taylor, arms crossed, neutral face, big text. Overlay: "DON'T RETIRE HERE IF…"

---

## YOUTUBE DESCRIPTION

Thinking about retiring in Temple, TX? Here's the honest analysis most retirement guides won't give you — why people quietly choose Temple over Georgetown's Sun City, and the one reason you shouldn't.

I'm Taylor Dasch with EG Realty. I've closed $28M+ in Temple/Belton and work with retirees and downsizers every week. This is the real breakdown: healthcare, the over-65 tax freeze, cost of living, and who should NOT retire here.

📍 Full written retirement breakdown (tax-freeze math, neighborhoods, healthcare):
https://templetxhomes.net/retiring-in-temple-tx/?utm_source=youtube&utm_medium=description&utm_campaign=retiring-in-temple-tx

⏱️ CHAPTERS
0:00 The Georgetown problem
0:30 Why Temple works
0:50 Healthcare: the unfair advantage
2:00 Taxes: the over-65 freeze
3:00 Cost of living vs Georgetown
3:45 Where retirees actually buy
4:45 Who should NOT retire here
6:00 My honest take
7:00 The verdict

📞 Talk through your situation: 254-718-4249 | dealswithdasch@gmail.com

Taylor Dasch | EG Realty | Temple, TX
*Numbers are ranges — verify current figures before financial decisions.*

#TempleTX #RetireInTexas #CentralTexas

---

## PINNED COMMENT

The full written retirement breakdown — over-65 tax-freeze math, neighborhoods, and the healthcare detail — is here: https://templetxhomes.net/retiring-in-temple-tx/?utm_source=youtube&utm_medium=description&utm_campaign=retiring-in-temple-tx — and if you want to talk through whether Temple actually fits, call/text me at 254-718-4249. — Taylor

---

## B-ROLL SHOT LIST

1. BSW Medical Center campus exterior (tower, signage) — hook + healthcare
2. Olin E. Teague VA Medical Center exterior — military beat
3. Single-story home drives: Bella Terra, Lake Pointe, Three Creeks — housing
4. Downtown Temple street — "working city" frame
5. Belton Lake (trails, water) — Three Creeks/active retirees
6. GRAPHIC: over-65 tax-freeze number card
7. GRAPHIC: Temple vs Georgetown cost/healthcare comparison card
8. Amtrak TPL station — connectivity
9. H-E-B / everyday errand b-roll — cost of living

---

## SHORTS CUTS (vertical)

**Short 1 — "Temple vs Georgetown" (the money+healthcare beat):**
Micro-hook: "Same house, 60% of the price — and a trauma center Georgetown doesn't have."
[Comparison card] Median home: Temple ~$255K, Georgetown ~$425K. Temple has the only Level I trauma center on I-35 between Dallas and Austin. Georgetown drives to Austin. So why does everyone still say Georgetown? Because Georgetown markets itself. Temple doesn't. Full breakdown linked.

**Short 2 — "Who should NOT retire in Temple" (honesty beat):**
Micro-hook: "Don't retire in Temple, TX if you want this one thing."
If you want a Sun City — gated, golf carts, an activities director — Temple does not have that. One 55-plus apartment community, that's it. If that lifestyle is the dealbreaker, go to Georgetown, honestly. But if healthcare and cost come first, Temple wins. Here's why.

**Short 3 — "The over-65 tax freeze" (little-gem beat):**
Micro-hook: "The Texas retirement tax break nobody tells you about until it's too late."
At 65, file the over-65 homestead exemption and your school taxes freeze at that year's dollar amount — forever. Plus an extra $10K exemption. On a $300K home that's ~$2,400-3,200 a year. And it transfers if you move — but you have 1 year to file Form 50-132 or you lose it.

codex
I’ll treat this as a read-only critique and verify the factual/legal surfaces before grading the draft, because several claims touch taxes, healthcare status, and market data.
web search: 
web search: Baylor Scott & White Temple Level I trauma center 636 beds official
web search: 
web search: site:bswhealth.com Baylor Scott White Medical Center Temple 636 beds Level I trauma center
web search: 
web search: TREC IABS real estate advertising disclose broker name Texas YouTube description
web search: 
web search: Texas Comptroller age 65 older homestead exemption 100000 10000 school tax ceiling 2026
web search: 
web search: https://comptroller.texas.gov/taxes/property-tax/exemptions/
web search: 
web search: site:comptroller.texas.gov taxes property-tax residence homestead FAQ school tax ceiling transfer new homestead percentage
web search: 
web search: Georgetown TX housing market average home value April 2026 Zillow
web search: 
web search: Baylor Scott White Temple cardiology appointment wait time 2 weeks Austin 4 weeks
codex
FATAL WEAKNESSES (must fix or kill):
1. `I'm Taylor Dasch with EG Realty.` — Identity starts at `0:12`, but the spec requires the identity declaration in the first 3 sentences and not inside the first 15 seconds. — Rewrite timing to: `[0:00-0:15 — HOOK] ...` then `[0:15-0:33 — Identity] I'm Taylor Dasch with EG Realty...`

2. `Plus an extra ten-thousand-dollar exemption.` — Wrong as of current Texas Comptroller guidance: school homestead is `$140,000`, and age 65+/disabled adds `$60,000`, not `$10,000`. This is a tax/legal accuracy failure. Source: Texas Comptroller. — Rewrite: `Under current Texas law, the school-district homestead exemption is $140,000, and the age-65-or-older exemption adds another $60,000. Confirm with Bell CAD or your appraisal district before you build a budget around it.`

3. `On a 300-thousand-dollar home, the combined over-65 breaks save you somewhere around twenty-four hundred to thirty-two hundred a year.` — Unsupported tax math tied to a now-wrong exemption amount. A retired buyer could rely on this and make a financial decision. — Rewrite: `The savings depend on the school tax rate, local exemptions, prior ceiling, and appraised value. I would show the formula, then verify the actual bill with the appraisal district before treating it as spendable money.`

4. `you have to file Form 50-132 with the new county within one year. Miss that deadline and you lose it.` — Wrong form. Comptroller’s forms page lists `50-808` for Residence Homestead Exemption Transfer Certificate and `50-272` for School Tax Ceiling Certificate; `50-132` is a protest form. Source: Texas Comptroller forms list. — Rewrite: `To transfer the ceiling, request the proper tax-ceiling or homestead-transfer certificate through the appraisal district; do not rely on a YouTube video for the filing step.`

5. `Because Temple is the referral center, specialist wait times are often shorter than in Austin. A cardiology consult here books in about two to three weeks, versus four to six in Austin. Verify that for your own situation — but the pattern holds.` — Looks fabricated or anecdotal, and a BSW physician group chat would shred it. Public sources support BSW’s specialty depth, not this exact wait-time comparison. — Rewrite: `Temple has unusually deep specialty coverage for a city this size, but appointment timing depends on insurance, referral urgency, specialty, and provider availability. If healthcare access is the reason you’re moving, call your specific doctors before you buy.`

6. `Temple is the highest-healthcare, lowest-cost serious retirement option on the entire I-35 corridor.` — Unprovable superlative and potential misleading-advertising surface. — Rewrite: `Temple has one of the strongest healthcare-to-housing-cost combinations in Central Texas, especially if you are comparing it with Georgetown or Austin-adjacent retirement options.`

7. `Bella Terra — newer, closest to the hospital, my top pick. Three Creeks — Belton Lake trails, best for active retirees. Canyon Creek — bigger lots, mature trees, best value. Lake Pointe — single-story, lower-maintenance, easier on the budget.` — This reads like steering retirees into named neighborhoods by age/lifestyle. Fair-housing risk. — Rewrite: `The criteria I’d compare are hospital distance, single-story inventory, HOA costs, lot size, age of systems, trail access, and tax district. Then I’d match the property, not the buyer’s age, to those criteria.`

MAJOR WEAKNESSES (must fix to ship cleanly):
1. `I've done over $28 million in transactions here in Temple and Belton` — Context says `$30M+ closed volume`; this looks stale or inconsistent. — Rewrite: `I've closed $30M+ in Central Texas transactions, including Temple and Belton.`

2. `Baylor Scott & White in Temple is a 636-bed Level I trauma center.` — Level I is supported by Texas DSHS and BSW, but BSW currently describes Temple as a `640-bed` hospital in some official material. — Rewrite: `Baylor Scott & White Medical Center - Temple is a Level I trauma center, and BSW describes the Temple hospital as roughly 640 beds.`

3. `That's the only Level I trauma center on I-35 between Dallas and Austin.` — Supported by BSW, but it needs attribution on-screen or in description. — Rewrite: `BSW describes Temple as the only designated Level I trauma center between Dallas and Austin.`

4. `Georgetown drives to Austin for that.` — Oversimplified. Georgetown has emergency and trauma-adjacent regional options; the accurate distinction is Level I adult trauma. — Rewrite: `For Level I adult trauma care, Georgetown is tied into the Austin/Round Rock network; Temple has that Level I designation in town.`

5. `same house for roughly 60% of the Georgetown cost` — “Same house” is lazy and false-adjacent: age, lot, schools, tax districts, amenities, and condition differ. — Rewrite: `A comparable price band often buys more house in Temple than Georgetown, but the right comparison is age, condition, tax district, HOA, and commute, not just median price.`

6. `A retired couple here runs about thirty-five hundred to forty-six hundred a month all in.` — “All in” is undefined and financially dangerous. — Rewrite: `I would not use one universal monthly number. Build the budget from housing payment or cash purchase, taxes, insurance, HOA, utilities, healthcare, and transportation.`

7. `Retirees come to me wanting a big lot... And then, every single time, they end up buying...` — “Every single time” sounds fake. — Rewrite: `The pattern I see often: buyers start with acreage, then narrow toward newer single-story homes once roof, foundation, HVAC, and maintenance costs enter the math.`

8. `Now the part most agents won't say out loud.` — Competitor bait. It implies other agents hide negatives. — Rewrite: `Here’s the part that gets skipped when Temple is reduced to affordability.`

9. `Fort Hood` — The provided lane context uses Fort Cavazos. Military spouses will notice the outdated name. — Rewrite: `Fort Cavazos`.

10. `If you're at the stage where driving is ending, Temple is hard without family nearby.` — True concern, bad framing. It can sound like discouraging older or disabled buyers. — Rewrite: `If you expect to rely on transit, paratransit, or rideshare, test that before buying: doctor visits, groceries, church, airport trips, and late-night backup rides.`

11. `If you're the practical type, I built a full written breakdown...` — Operational commitment. If the page is not live, this fails. — Rewrite: `If the written breakdown is live, it’s linked below; if not, remove this CTA before publishing.`

12. YouTube description lacks IABS / Consumer Protection Notice links — TREC advertising guidance requires broker name in ads, and business web surfaces need IABS/CPN handling. Source: TREC advertising/IABS guidance. — Rewrite add: `Texas Real Estate Commission Information About Brokerage Services: [link]` and `TREC Consumer Protection Notice: [link]`.

MINOR WEAKNESSES (polish):
1. `the city 30 minutes north` — Temple is north of Georgetown, but “30 minutes” is optimistic depending on route and traffic. — Rewrite: `about 30 to 40 minutes north, depending on where you start.`

2. `you've never heard that` — Patronizing. — Rewrite: `Temple usually does not get described that way because it is a working medical city, not a purpose-built retirement brand.`

3. `the gap gets loud` — AI-ish phrasing. — Rewrite: `the price gap becomes hard to ignore.`

4. `Temple wins.` — Sales/pump tone in Short 2. — Rewrite: `Temple makes more sense for that buyer profile.`

5. `little-gem beat` — Not public-facing, but it drifts near banned “gem” language. — Rewrite: `tax-freeze beat`.

DOMAIN CHECKS:
- Identity timing: FAIL — identity starts at `0:12`; must land at `0:14` or later and outside first 15 seconds.
- Banned vocabulary: Clean in public copy; remove internal `little-gem beat`.
- Lane discipline: PASS — no investor framing leaks into the Living in Temple asset.
- Forecast surface: FAIL — `forever`, `pattern holds`, universal monthly-budget claims, and tax-savings claims overstate certainty.
- Data provenance: FAIL — tax exemption amount/form are wrong; wait times, monthly budget, utilities, neighborhood labels, and several medians need source labels.

VERDICT: REVISE

ONE-LINE REASON: The concept is usable, but the current draft cannot ship because tax guidance, identity timing, healthcare wait-time claims, and neighborhood steering language create avoidable compliance and credibility risk.
tokens used
94,835
FATAL WEAKNESSES (must fix or kill):
1. `I'm Taylor Dasch with EG Realty.` — Identity starts at `0:12`, but the spec requires the identity declaration in the first 3 sentences and not inside the first 15 seconds. — Rewrite timing to: `[0:00-0:15 — HOOK] ...` then `[0:15-0:33 — Identity] I'm Taylor Dasch with EG Realty...`

2. `Plus an extra ten-thousand-dollar exemption.` — Wrong as of current Texas Comptroller guidance: school homestead is `$140,000`, and age 65+/disabled adds `$60,000`, not `$10,000`. This is a tax/legal accuracy failure. Source: Texas Comptroller. — Rewrite: `Under current Texas law, the school-district homestead exemption is $140,000, and the age-65-or-older exemption adds another $60,000. Confirm with Bell CAD or your appraisal district before you build a budget around it.`

3. `On a 300-thousand-dollar home, the combined over-65 breaks save you somewhere around twenty-four hundred to thirty-two hundred a year.` — Unsupported tax math tied to a now-wrong exemption amount. A retired buyer could rely on this and make a financial decision. — Rewrite: `The savings depend on the school tax rate, local exemptions, prior ceiling, and appraised value. I would show the formula, then verify the actual bill with the appraisal district before treating it as spendable money.`

4. `you have to file Form 50-132 with the new county within one year. Miss that deadline and you lose it.` — Wrong form. Comptroller’s forms page lists `50-808` for Residence Homestead Exemption Transfer Certificate and `50-272` for School Tax Ceiling Certificate; `50-132` is a protest form. Source: Texas Comptroller forms list. — Rewrite: `To transfer the ceiling, request the proper tax-ceiling or homestead-transfer certificate through the appraisal district; do not rely on a YouTube video for the filing step.`

5. `Because Temple is the referral center, specialist wait times are often shorter than in Austin. A cardiology consult here books in about two to three weeks, versus four to six in Austin. Verify that for your own situation — but the pattern holds.` — Looks fabricated or anecdotal, and a BSW physician group chat would shred it. Public sources support BSW’s specialty depth, not this exact wait-time comparison. — Rewrite: `Temple has unusually deep specialty coverage for a city this size, but appointment timing depends on insurance, referral urgency, specialty, and provider availability. If healthcare access is the reason you’re moving, call your specific doctors before you buy.`

6. `Temple is the highest-healthcare, lowest-cost serious retirement option on the entire I-35 corridor.` — Unprovable superlative and potential misleading-advertising surface. — Rewrite: `Temple has one of the strongest healthcare-to-housing-cost combinations in Central Texas, especially if you are comparing it with Georgetown or Austin-adjacent retirement options.`

7. `Bella Terra — newer, closest to the hospital, my top pick. Three Creeks — Belton Lake trails, best for active retirees. Canyon Creek — bigger lots, mature trees, best value. Lake Pointe — single-story, lower-maintenance, easier on the budget.` — This reads like steering retirees into named neighborhoods by age/lifestyle. Fair-housing risk. — Rewrite: `The criteria I’d compare are hospital distance, single-story inventory, HOA costs, lot size, age of systems, trail access, and tax district. Then I’d match the property, not the buyer’s age, to those criteria.`

MAJOR WEAKNESSES (must fix to ship cleanly):
1. `I've done over $28 million in transactions here in Temple and Belton` — Context says `$30M+ closed volume`; this looks stale or inconsistent. — Rewrite: `I've closed $30M+ in Central Texas transactions, including Temple and Belton.`

2. `Baylor Scott & White in Temple is a 636-bed Level I trauma center.` — Level I is supported by Texas DSHS and BSW, but BSW currently describes Temple as a `640-bed` hospital in some official material. — Rewrite: `Baylor Scott & White Medical Center - Temple is a Level I trauma center, and BSW describes the Temple hospital as roughly 640 beds.`

3. `That's the only Level I trauma center on I-35 between Dallas and Austin.` — Supported by BSW, but it needs attribution on-screen or in description. — Rewrite: `BSW describes Temple as the only designated Level I trauma center between Dallas and Austin.`

4. `Georgetown drives to Austin for that.` — Oversimplified. Georgetown has emergency and trauma-adjacent regional options; the accurate distinction is Level I adult trauma. — Rewrite: `For Level I adult trauma care, Georgetown is tied into the Austin/Round Rock network; Temple has that Level I designation in town.`

5. `same house for roughly 60% of the Georgetown cost` — “Same house” is lazy and false-adjacent: age, lot, schools, tax districts, amenities, and condition differ. — Rewrite: `A comparable price band often buys more house in Temple than Georgetown, but the right comparison is age, condition, tax district, HOA, and commute, not just median price.`

6. `A retired couple here runs about thirty-five hundred to forty-six hundred a month all in.` — “All in” is undefined and financially dangerous. — Rewrite: `I would not use one universal monthly number. Build the budget from housing payment or cash purchase, taxes, insurance, HOA, utilities, healthcare, and transportation.`

7. `Retirees come to me wanting a big lot... And then, every single time, they end up buying...` — “Every single time” sounds fake. — Rewrite: `The pattern I see often: buyers start with acreage, then narrow toward newer single-story homes once roof, foundation, HVAC, and maintenance costs enter the math.`

8. `Now the part most agents won't say out loud.` — Competitor bait. It implies other agents hide negatives. — Rewrite: `Here’s the part that gets skipped when Temple is reduced to affordability.`

9. `Fort Hood` — The provided lane context uses Fort Cavazos. Military spouses will notice the outdated name. — Rewrite: `Fort Cavazos`.

10. `If you're at the stage where driving is ending, Temple is hard without family nearby.` — True concern, bad framing. It can sound like discouraging older or disabled buyers. — Rewrite: `If you expect to rely on transit, paratransit, or rideshare, test that before buying: doctor visits, groceries, church, airport trips, and late-night backup rides.`

11. `If you're the practical type, I built a full written breakdown...` — Operational commitment. If the page is not live, this fails. — Rewrite: `If the written breakdown is live, it’s linked below; if not, remove this CTA before publishing.`

12. YouTube description lacks IABS / Consumer Protection Notice links — TREC advertising guidance requires broker name in ads, and business web surfaces need IABS/CPN handling. Source: TREC advertising/IABS guidance. — Rewrite add: `Texas Real Estate Commission Information About Brokerage Services: [link]` and `TREC Consumer Protection Notice: [link]`.

MINOR WEAKNESSES (polish):
1. `the city 30 minutes north` — Temple is north of Georgetown, but “30 minutes” is optimistic depending on route and traffic. — Rewrite: `about 30 to 40 minutes north, depending on where you start.`

2. `you've never heard that` — Patronizing. — Rewrite: `Temple usually does not get described that way because it is a working medical city, not a purpose-built retirement brand.`

3. `the gap gets loud` — AI-ish phrasing. — Rewrite: `the price gap becomes hard to ignore.`

4. `Temple wins.` — Sales/pump tone in Short 2. — Rewrite: `Temple makes more sense for that buyer profile.`

5. `little-gem beat` — Not public-facing, but it drifts near banned “gem” language. — Rewrite: `tax-freeze beat`.

DOMAIN CHECKS:
- Identity timing: FAIL — identity starts at `0:12`; must land at `0:14` or later and outside first 15 seconds.
- Banned vocabulary: Clean in public copy; remove internal `little-gem beat`.
- Lane discipline: PASS — no investor framing leaks into the Living in Temple asset.
- Forecast surface: FAIL — `forever`, `pattern holds`, universal monthly-budget claims, and tax-savings claims overstate certainty.
- Data provenance: FAIL — tax exemption amount/form are wrong; wait times, monthly budget, utilities, neighborhood labels, and several medians need source labels.

VERDICT: REVISE

ONE-LINE REASON: The concept is usable, but the current draft cannot ship because tax guidance, identity timing, healthcare wait-time claims, and neighborhood steering language create avoidable compliance and credibility risk.
