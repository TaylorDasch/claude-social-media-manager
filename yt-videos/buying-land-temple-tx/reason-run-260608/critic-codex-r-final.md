Reading prompt from stdin...
2026-06-08T14:17:48.078963Z ERROR codex_core::session: failed to load skill /Users/taylordasch_1/.claude/skills/geo-query-finder/SKILL.md: missing YAML frontmatter delimited by ---
2026-06-08T14:17:48.079293Z ERROR codex_core::session: failed to load skill /Users/taylordasch_1/.agents/skills/repurpose-tree/SKILL.md: invalid YAML: mapping values are not allowed in this context at line 2 column 99
OpenAI Codex v0.128.0 (research preview)
--------
workdir: /Users/taylordasch_1/claude-social-media-manager/yt-videos/buying-land-temple-tx
model: gpt-5.5
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, /Users/taylordasch_1/.codex/memories]
reasoning effort: xhigh
reasoning summaries: none
session id: 019ea798-c8ed-7c42-9ac5-02046d9202f9
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

=== END TEMPLATE — FOCUS ADDENDUM FOR THIS RUN ===
CORRECTION: Use "Fort Hood" (the base reverted from Fort Cavazos). Do NOT flag "Fort Hood" as an error.

This is a Living-in-Temple BUYER video that drives to a LIVE page (/buying-land-temple-tx/). The video MUST stay consistent with that page. Three decisive adjudications (pick ONE answer each + give the exact replacement line):

1) AG ROLLBACK WORDING. The live page says, in visible HTML + FAQ schema: "recovering several years of the tax savings, plus interest" and hedges "confirm the current rollback period with the Bell County Appraisal District and a tax pro." Texas cut the ag-rollback lookback from 5 years to 3 (~2019-2021). The script speaks "several years ... plus interest" then the same hedge. Is "several years" safe to SPEAK on an evergreen video, or should BOTH page and video change to count-free wording (e.g., "back taxes plus interest")? Decide; give the exact line.

2) ENTITY-LINE TIMING. Rule: the "Taylor Dasch with EG Realty" line must NOT be in the first ~15 seconds (hook first). The script places it at 0:12. Acceptable, or move to 0:14+? Give the exact fix.

3) Any FATAL/MAJOR: banned vocabulary, an unhedged engineering/lending claim, a fabricated or geographically-mislabeled number, or lane drift (buyer lane — no investor/cap-rate framing).

Be concise: list only FATAL and MAJOR items (skip minor polish). Each: severity, exact quoted line, one-line rewrite. End with a one-line OVERALL VERDICT: ship-ready as-is / ship-ready with your fixes / not ship-ready.

=== SCRIPT TO ATTACK ===
# Companion Video — Buying Land Near Temple, TX (Council-converged)
**Channel:** Living in Temple (relocation/buyer lane) · **Pairs with:** /buying-land-temple-tx/
**Produced via:** /council -> autoresearch:reason (5 blind judges, 3 rounds, converged AB @2 consecutive wins, 2026-06-08)

> This is the winning creative core (title + 3 hooks + full word-for-word script + talking-points + Shorts seeds + a compliance self-check). Derived deliverables (description+UTM, thumbnail brief, shot list, Shorts, pinned comment) are in the sibling files.

---

# CREATIVE CORE — CANDIDATE AB · "Buying Land Near Temple, TX: 7 Checks Before You Offer"

## 1) RECOMMENDED TITLE (54 chars)

**Buying Land Near Temple, TX? 7 Checks Before You Offer**

*Backups: `7 Checks Before You Buy Land Near Temple, TX` (45 chars, keyword-cleanest) · `Don't Buy Land Near Temple, TX Until You Run These 7` (51 chars, higher curiosity).*

---

## 2) THREE 15-SECOND HOOK VARIANTS

> Rules enforced on all three: the surprise lands by ~6s (concrete payoff in the first beat, not deferred to a setup clause); no spoken stat is geographically narrower than its source — the MLS figure is kept OUT of every cold open and spoken only in the body as "Temple-area" (four-city corridor); every buildability claim stays conditional (can / might / sometimes) — never a flat verdict on the tract on screen; the payoff is information, not a tease; the "7" promise lands before 0:13; no name/entity and no dated dollar figure in any cold open.

**HOOK A — "The cheapest acre" (★ RECOMMENDED)**
> [B-ROLL: drone push over an open Bell County tract — FOR SALE sign in the grass, a dirt two-track running to a far tree line] **[CUT @0:03]**
> "The cheapest ten acres on the listing site can cost you more than the most expensive one."
> [ON-SCREEN: **"CHEAP DIRT ≠ CHEAP TO BUILD ON"**] **[CUT @0:06]**
> "Because the price tag is just the dirt. It doesn't include the septic, the water tap, or whether you can legally even drive onto the lot."
> [ON-SCREEN: **"7 checks · before you offer"**] **[CUT @0:11]**
> "Run these seven before you write the offer — or that bargain becomes the most expensive lesson in Bell County."

*Why recommended:* The payoff is a real, counterintuitive operator claim that lands at ~0:04 — "the cheapest can cost more than the most expensive" — and it's defensible because it compares *build-ready cost*, not sticker price ("can cost you more," conditional, never "always does"). It names three of the actual checks (septic / water tap / legal access) as concrete content inside the first beat, so the hook teaches instead of teases. It carries zero stat in the cold open, which sidesteps the geographic-precision trap entirely: the only safe spoken version of the MLS number is a mouthful ("793 of 4,270 listings across four cities"), and any compressed spoken version silently narrows a four-city figure into a Temple-only claim — so the number moves to Taylor's Take where it's said correctly. Closes on the page's load-bearing stakes line ("the most expensive lesson in Bell County"), so video and destination page reinforce each other. This is the council's flagged winning angle (the build-cost surprise) delivered as the hook, not buried at Check 7.

**HOOK B — "The arithmetic" (Taylor's locked voice, story-led)**
> [B-ROLL: a dirt two-track curving across an open field toward a gate] **[CUT @0:03]**
> "Somebody finds ten acres priced under the neighbors and writes the offer that same weekend. Feels like a steal — for about a month."
> [ON-SCREEN: **"LAND PRICE ≠ ALL-IN COST"**] **[CUT @0:07]**
> "Then the soil won't pass a septic test, and the 'water' turns out to be a co-op line down the road — not a tap at the pad."
> [CUT @0:11]
> "The land was never the problem. Nobody priced the build-ready budget."

*Why strong:* Taylor's locked take as three clipped beats; "for about a month" supplies the turn. Leads in his analyst voice instead of a claim. Use if Taylor wants voice-first over claim-first — marginally slower information-gain because the payoff (what went wrong) arrives at ~0:08 rather than ~0:04, and it opens on a generic "somebody."

**HOOK C — "The driveway that isn't access" (single-fact shock — assign to Short #2)**
> [B-ROLL: a clean gravel driveway curving off a county road onto an empty lot] **[CUT @0:03]**
> "This driveway might be worth nothing."
> [ON-SCREEN: **"'There's a driveway' ≠ legal access"**] **[CUT @0:06]**
> "If it crosses a neighbor's land with nothing recorded, the lot can be legally landlocked — and your lender walks."
> [CUT @0:11]
> "It's one of seven checks Temple land buyers skip. Here they are."

*Why strong:* The single most screenshot-worthy fact and the fastest "wait, what." But it narrows the topic promise to Check 4 — a thinner long-form signal, since a long-form hook should promise the breadth of all seven, not one check. Holding it back from the cold open is deliberate: it's the **Short #2** hook (§5), not the opener.

---

## 3) FULL WORD-FOR-WORD SCRIPT (~1,295 words spoken | ~7:45 at conversational pace)

> Visual/audio change roughly every ~7s; cut points marked **[CUT]**. Timestamps approximate. Lower-thirds over full-frame cutaways; full-frame reserved for the cost-stack build, the map graphic, and Taylor's Take card. The video promises **7 on-camera checks** and explicitly points to the page for the full diligence set (it names minerals, financing, and the survey as "on the printable list"), so the count is honest, not amputated.

---

**[0:00–0:12] COLD OPEN — HOOK A**
[B-ROLL: drone push over an open tract — FOR SALE sign, dirt two-track to a far tree line] **[CUT]**

The cheapest ten acres on the listing site can cost you more than the most expensive one.

[ON-SCREEN: **"CHEAP DIRT ≠ CHEAP TO BUILD ON"**] **[CUT]**

Because the price tag is just the dirt. It doesn't include the septic, the water tap, or whether you can legally even drive onto the lot.

[ON-SCREEN: **"7 checks · before you offer"**] **[CUT]**

Run these seven before you write the offer — or that bargain becomes the most expensive lesson in Bell County.

---

**[0:12–0:42] BODY OPEN + ENTITY LINE**
[ON-CAMERA: Taylor, outdoors, open tract or truck behind him] **[CUT]**

I'm Taylor Dasch with EG Realty, and I walk these tracts for a living — Temple, Belton, Salado, Harker Heights, out into the county.

[ON-SCREEN: lower-third **"Taylor Dasch · EG Realty · Temple, TX"**] **[CUT]**

Here's the pattern I see. The land mistakes that cost people aren't emotional — they're arithmetic. Somebody buys good-looking dirt and never prices what it takes to make it usable.

[B-ROLL: quick 3-shot — well cap / aerobic septic spray head / culvert pipe set under a driveway] **[CUT]**

And almost none of what you're about to check shows up in the listing. It lives in the survey, the appraisal district file, the FEMA map, and the county septic records. I'm giving you the seven that quietly kill the most deals — the page linked below has the full checklist, minerals and financing included. Let's go get them.

---

**[0:42–1:14] WHY CHEAP LAND IS SOMETIMES CHEAP**
[ON-CAMERA] **[CUT]**

Start with one question on any tract priced under its neighbors: why? Sometimes it's just a seller who needs out — that's the good kind of cheap. A real deal.

[B-ROLL: slow drone reveal of standing water at the back of a lot] **[CUT]**

The other kind is cheap for something you can't see from the road. A floodplain line through the back. Soil that won't perc. No legal way in.

[ON-SCREEN: **"A house has comps. Raw dirt has a punch list."**] **[CUT]**

A finished house has a roof, a slab, comps you can pull. Raw dirt has a punch list — and the sticker price only tells you the first number on it. These seven checks find the second number: what it costs to make the land buildable.

---

**[1:14–1:58] CHECK 1 — WATER**
[ON-SCREEN: **"CHECK 1 · WATER"** | three icons: well / co-op / city] **[CUT]**

Check one: water — and there are three very different answers. [B-ROLL: well pump head and pressure tank] **[CUT]** A private well: no monthly bill, but you own the pump and the water quality, and drilling a new one can run well into five figures. A rural Water Supply Corporation tap. Or a city line.

[ON-SCREEN: **"'Water available' ≠ a paid tap at your pad"**] **[CUT]**

Here's the trap. "Water available" on a listing can just mean a co-op line runs somewhere down the road. That is not a tap that's already paid for and sitting at your house pad — and those two can be thousands of dollars, sometimes a waiting list, apart.

[ON-CAMERA] **[CUT]**

So the question isn't "is there water." It's: is the tap bought, and where exactly is it? On a city line, confirm it actually reaches your buildable spot. Pin that down — because check two is where I watch the most deals quietly fall apart.

---

**[1:58–2:50] CHECK 2 — SEPTIC / OSSF**
[ON-SCREEN: **"CHECK 2 · SEPTIC / OSSF"**] **[CUT]**

Check two: septic. Outside city limits you're almost certainly on an on-site sewage facility — OSSF — permitted through the county. Two things drive the cost: the soil, and the system type. [B-ROLL: soil auger pulling a core / open perc-test pit] **[CUT]**

A soil and perc evaluation tells you whether the ground will support a system at all, and which kind. Heavy clay or rock — common in parts of Bell County — can force a pricier engineered or aerobic system. Or shrink where on the lot you're even allowed to build.

[ON-SCREEN: **"Conventional = cheaper · Aerobic = spray field + annual contract"**] **[CUT]**

Conventional is the cheaper system. Aerobic means a spray field and a maintenance contract you carry every single year. [ON-CAMERA, leaning in] **[CUT]** And that "unbuildable land" you hear horror stories about? The unbuildable surprise is almost always a septic surprise.

[ON-SCREEN: **"Write the option period long enough for a soil eval."**] **[CUT]**

So write your option period long enough to actually get a soil evaluation done — while you can still walk, not after your money's committed. Check three is the one you'll fall for from the road, and the one I check the hardest.

---

**[2:50–3:28] CHECK 3 — FLOODPLAIN**
[ON-SCREEN: **"CHECK 3 · FLOODPLAIN"**] **[CUT]**

Check three: floodplain. Pull the FEMA flood map, then read the survey. [B-ROLL: creek-adjacent land, moving water along a tree line] **[CUT]** A corner in the floodplain isn't automatically a dealbreaker — but it moves three things: your insurance, where you're allowed to build, and what a lender will sign off on.

[ON-SCREEN: **"Live water = verify before you fall for the view"**] **[CUT]**

And around here, creek-adjacent land near Temple, Belton, and Salado is exactly where this bites. The lot with the live water — the one that sells itself from the road — is the one to verify before the view does your thinking for you. [ON-CAMERA] **[CUT]** Check four is the quiet one almost nobody warns you about — the one that can stop a deal cold.

---

**[3:28–4:14] CHECK 4 — LEGAL RECORDED ACCESS**
[ON-SCREEN: **"CHECK 4 · LEGAL ACCESS"**] **[CUT]**

Check four: legal, recorded access. [B-ROLL: dirt two-track crossing an open field toward a gate] **[CUT]** If the only way onto the land is driving across a neighbor's field, and nothing's recorded, that land can be legally landlocked.

[ON-SCREEN: **"'There's a driveway' ≠ there's access"**] **[CUT]**

"There's a driveway" is not "there's legal access." You need public road frontage, or a recorded easement that runs with the land — meaning it stays attached to the property no matter who buys that neighboring field next. [ON-CAMERA, flat] **[CUT]** A handshake with today's neighbor is worth nothing the day he sells. If it's not in the title records, it isn't real — confirm it in the title commitment before you offer. Check five is about what you're actually allowed to do out here.

---

**[4:14–5:00] CHECK 5 — "NO ZONING ≠ NO RULES"**
[ON-SCREEN: **"CHECK 5 · NO ZONING ≠ NO RULES"**] **[CUT]**

Check five is a mindset fix. People hear Texas counties have limited zoning and assume rural land is anything-goes. [B-ROLL: a pipeline right-of-way marker and a power-line easement cutting across a field] **[CUT]** It isn't. Inside a city's ETJ, platting rules can apply if you split the tract. And private deed restrictions written against the property can still tell you no — on a barn, on livestock, on a manufactured home.

[ON-SCREEN: **"Two kinds of 'easement': your way IN vs. a strip you can't build ON"**] **[CUT]**

And one quick word so this doesn't get confusing: back in check four, an easement was a good thing — your recorded right to get in. Here it's the other kind — a pipeline or power-line easement crossing the tract that limits what you can build on that strip. Same word, opposite jobs. [ON-CAMERA] **[CUT]** So your freedom out here is in how you live in the home once it's built — not a free pass on the land. Read the deed restrictions and the survey before you picture the shop. Check six is pure money, and it surprises people a year after they close.

---

**[5:00–5:48] CHECK 6 — AG VALUATION + ROLLBACK**
[ON-SCREEN: **"CHECK 6 · AG VALUATION + ROLLBACK"**] **[CUT]**

Check six: agricultural valuation, and the rollback attached to it. A lot of rural tracts near Temple carry an ag valuation — people call it an "ag exemption." [B-ROLL: cattle or round hay bales on an open tract] **[CUT]** It taxes qualifying land on its productive use instead of full market value, which can cut the annual tax bill a lot. That part's real — a genuine win.

[ON-SCREEN: **"Change the use → possible rollback (back taxes + interest)"**] **[CUT]**

Here's the catch. Take the land out of that ag use — stop running cattle, build a non-qualifying homesite — and the county can hit you with a rollback that recovers several years of those savings, plus interest. [ON-CAMERA, direct] **[CUT]** Rollback rules change, so before you touch how the land's used, confirm the current rollback period for your specific parcel with the Bell County Appraisal District and a tax pro. Just know it exists, and price in the possibility. Check seven ties the other six together.

---

**[5:48–6:38] CHECK 7 — TRUE BUILD-READY COST**
[ON-SCREEN: **"CHECK 7 · TRUE BUILD-READY COST"**] **[CUT]**

Check seven, and it's the whole point: the land price is not your all-in cost. [B-ROLL: montage — excavator moving dirt / septic tank set in a trench / culvert in a road cut / propane tank / utility trench] **[CUT]** On top of the dirt, you're budgeting site work and a pad. Septic install. The well, or the co-op tap. A driveway and the culvert the county requires. Utility runs — electric, propane, internet. Plus survey and permits.

[ON-SCREEN: stacked list builds line-by-line — **Dirt → +Site work/pad → +Septic → +Well/tap → +Driveway/culvert → +Utilities → +Survey/permits**] **[CUT]**

Stack all of that onto the sticker, and the gap between raw land and build-ready can be bigger than you'd ever guess from the listing — especially on rocky or sloped ground. [ON-CAMERA] **[CUT]** That's not a reason to fear land — it's the reason to price the project, not just the parcel, before your option period runs out. The dirt is the down payment on the build. It is not the whole bill.

---

**[6:38–7:14] TAYLOR'S TAKE + MARKET CONTEXT**
[ON-CAMERA, calm, direct — let it breathe] **[CUT]**

So here's my take, after walking a lot of these.

[ON-SCREEN, full-frame, held ~3s: **"The land mistakes I see aren't emotional — they're arithmetic."**] **[CUT]**

Somebody finds ten acres under the neighbors, writes the fast offer, then prices the septic the clay won't pass and the well they assumed was a co-op tap — after they're already committed. The land was never the problem. The build-ready budget was, and nobody added it up in time.

[B-ROLL: clean map graphic — soft pins on Temple ETJ, Belton, Salado, Harker Heights; pins only, NO price or percentage text on the card] **[CUT]**

If you're shopping acreage in the Temple area, the pockets are the Temple ETJ, Belton, Salado, and Harker Heights — and Salado punches above its size. But acreage runs from a half-acre homesite to a working ranch, so any "average price" you see tells you almost nothing about *your* parcel. [ON-CAMERA] **[CUT]** What matters isn't the headline number. It's whether this specific tract pencils. Buy the dirt for what it can become, priced for what it'll cost to get there. Usable dirt beats pretty dirt.

---

**[7:14–7:45] CTA — ONE ASK: THE CHECKLIST**
[ON-CAMERA] **[CUT]**

So — one thing to do next. There's a free checklist for all of this on the page linked below, and the part that genuinely saves you a week of phone tag is right on it: the actual Bell County offices that answer each question. [ON-SCREEN: **"Free land checklist + who-to-call → link below"**] **[CUT]** The appraisal district for the ag and rollback question. The county health district for septic. The county engineer for floodplain and for the driveway and culvert. I'm not going to read phone numbers at you on camera — they're printed on the checklist, and you can save the whole thing as a PDF and take it to the property.

[ON-SCREEN: page mock — readiness check · who-to-call directory · "Print / save as PDF"] **[CUT]**

Work it top to bottom before your option period ends, and you'll know exactly what you're buying. [ON-CAMERA, low-key] **[CUT]** Grab the checklist. Confirm before you commit. That's the whole game.

---
*(Optional VA/USDA one-liner — insert at [4:14] only if pacing allows; buyer-safe, mirrors the page: "And much of the rural belt around Temple is USDA-eligible, and a VA loan can work on the right rural property if you qualify — confirm it for your situation, it's not a promise.")*

---

## 4) TALKING-POINTS VERSION (shoot-from-the-hip outline)

**COLD OPEN (no name, ≤12s) — HOOK A**
- Counterintuitive payoff FIRST: "The cheapest ten acres on the listing site can cost you more than the most expensive one." (conditional — "can," never "always")
- Why: the price tag is just the dirt — doesn't include septic, water tap, or legal access.
- Promise + stakes: run these 7 before you offer, or the bargain = the most expensive lesson in Bell County.
- (No stat in the hook — the MLS number lands in the body, stated correctly.)

**BODY OPEN (entity line lands HERE, not in hook)**
- "Taylor Dasch with EG Realty — I walk these tracts." Lower-third.
- Thesis: "Land mistakes aren't emotional, they're arithmetic. People buy good-looking dirt and never price making it usable."
- Honest scope line: "I'm giving you the 7 that quietly kill the most deals — the page below has the FULL list, minerals and financing included." (keeps the 7-vs-full-list honest — don't pretend 7 is the whole map)
- Sources = survey · appraisal district · FEMA map · county septic file. NOT the listing.

**WHY CHEAP IS SOMETIMES CHEAP**
- Good cheap: motivated seller (real deal). Bad cheap: hidden flood line / bad soil / no legal access.
- House has comps; raw dirt has a punch list. Sticker = first number; these 7 find the second (cost-to-build).

**CHECK 1 — WATER**
- 3 answers, different money: private well (own pump + quality, new drill = well into 5 figures) · rural WSC tap · city line.
- Trap: "water available" = line down the road ≠ a tap PAID FOR and AT THE PAD. Can be thousands + sometimes a waitlist apart.
- City line? Confirm it reaches the buildable spot.
- Ask: tap bought? where exactly? → hand to septic as "where deals quietly fall apart."

**CHECK 2 — SEPTIC / OSSF** *(slow down — the big one, this is the winning Short)*
- Outside city = OSSF, county-permitted. Cost = soil + system type.
- Soil/perc eval = if and what. Clay or rock (Bell County) → pricier engineered/aerobic OR shrinks buildable area.
- Conventional (cheap) vs aerobic (spray field + annual contract every year).
- "Unbuildable surprise = almost always a septic surprise."
- ACTION: option period long enough to get the soil eval BEFORE money's committed. → tee up Check 3 as "the one you fall for from the road = check hardest."

**CHECK 3 — FLOODPLAIN**
- Pull FEMA map + read survey. Moves insurance, buildable area, lender sign-off.
- Creek-adjacent Temple/Belton/Salado = where it bites. Live-water lot = verify before the view does your thinking. → Check 4 = "quiet one that can stop a deal cold."

**CHECK 4 — LEGAL RECORDED ACCESS** *(the quiet deal-killer — keep the superlative HERE only, not on floodplain)*
- Driving across neighbor's field, nothing recorded = can be legally landlocked.
- Need public road frontage OR recorded easement that RUNS WITH THE LAND.
- "There's a driveway" ≠ "there's access." Handshake dies the day the neighbor sells. Not in title records = not real → confirm in the title commitment. → Check 5 = "what's actually allowed out here."

**CHECK 5 — NO ZONING ≠ NO RULES** *(ETJ + deed restrictions, THEN the easement-word callout)*
- Limited county zoning ≠ anything-goes. Still real: ETJ platting (if you split), private deed restrictions (barn / livestock / manufactured home).
- EXPLICIT easement signpost: "In check 4 an easement was GOOD (your right to get in). Here it's the other kind — pipeline/power-line easement that limits the strip you can build ON. Same word, opposite jobs." (kills the blur)
- "Freedom is in how you LIVE in the home — not a free pass on the land." Read deed restrictions + survey before picturing the shop. → Check 6 = "pure money, surprises you a year after closing."

**CHECK 6 — AG VALUATION + ROLLBACK**
- Ag valuation ("ag exemption") = taxed on productive use → big annual savings (real win).
- Change the use (stop ag / build non-qualifying homesite) → possible ROLLBACK = several years of savings recovered + interest.
- Say "several years" (do NOT pin an exact year count), then hedge: "rollback rules change — confirm the current period for your parcel with Bell County Appraisal District + a tax pro." Price in the possibility. NO "I won't say a number" theater — just say "several" and move.

**CHECK 7 — TRUE BUILD-READY COST** *(the payoff)*
- Land price ≠ all-in. Add: dirt/site work + pad · septic install · well/co-op tap · driveway + culvert · utilities (electric/propane/internet) · survey/permits.
- "The gap between raw land and build-ready can be bigger than you'd guess from the listing — especially on rocky or sloped ground." (directional — matches the page; do NOT say "costs more than a finished house" as a flat fact)
- Price the PROJECT, not the parcel. "Dirt is the down payment on the build, not the whole bill."
- *(Optional VA/USDA one-liner — qualify it: confirm for your situation, not a promise.)*

**TAYLOR'S TAKE + MARKET CONTEXT**
- Land it clean, let it breathe (full-frame card): "The land mistakes I see aren't emotional — they're arithmetic."
- Re-tell the fast-offer-then-the-bills story in one breath. Land was never the problem; the build-ready budget was.
- Pockets = Temple ETJ / Belton / Salado / Harker Heights (say "in the Temple area"); Salado punches above its size.
- Reframe over any average: acreage spans half-acre homesite → working ranch, so an "average" tells you nothing about YOUR parcel. (Keep the dated $ figure on the PAGE, not on camera.)
- "Buy the dirt for what it can become, priced for what it'll cost to get there. Usable dirt beats pretty dirt."

**CTA — ONE ASK: THE CHECKLIST**
- Free checklist on the page below; the real value = the actual Bell County offices (appraisal district = ag/rollback · county health district = septic · county engineer = floodplain + driveway/culvert).
- Don't read numbers on camera → "they're on the checklist, save it to PDF, take it to the property."
- Close: "Grab the checklist. Confirm before you commit. That's the whole game."
- (Booking link lives on the page; do NOT add a second spoken call-CTA — the on-screen page mock shows it, the voice stays on the checklist only. One ask.)

---

## 5) THREE SHORTS HOOKS (derivation seeds — brief asks to set up 1–3 Shorts)
*(Seeds only, mapped to long-form beats + the council prompt's three named Shorts.)*
- **Short #1 (Check 2 · "the septic" — the council's flagged likely-winner):** "When people say land near Temple is 'unbuildable,' they almost always mean one thing — septic." → ~25s: clay or rock won't perc → forces a pricier engineered/aerobic system + an annual maintenance contract → "get a soil evaluation done inside your option period, before you're committed." → "full 7-check guide + free Bell County checklist, link below." *(= council Short #1, "why cheap Texas land is sometimes cheap — the septic.")*
- **Short #2 (Check 4 · "landlocked"):** Use **HOOK C** verbatim — "This driveway might be worth nothing." → recorded easement that runs with the land vs a handshake → lender walks → confirm it in the title commitment → checklist CTA. *(= council Short #2, "legal access vs a driveway — the landlocked trap.")*
- **Short #3 (Check 6 · "the rollback"):** "That ag exemption dropping your tax bill? It can come back to bite you." → ag valuation = real annual savings → change the use → rollback recovers several years + interest → "confirm the current period with the Bell County Appraisal District before you change anything." → checklist CTA. *(= council Short #3, "ag exemption looks great until the rollback tax.")*

*(If Taylor wants a 4th: a Check 1 "water available ≠ a tap at the pad" Short is the strongest alternate — swap it for whichever of #1–#3 has weaker B-roll on filming day.)*

---

## COMPLIANCE / VOICE / INVERSE-FAIL SELF-CHECK
- **Hook-first:** entity line ("Taylor Dasch with EG Realty") lands at 0:12 in the body open; never in any cold-open variant. ✓ (Inverse-fail #5 cleared.)
- **No geographically-false stat spoken:** the cold open carries ZERO MLS stat. The sourced number (793 of 4,270 across four cities ≈ ~1 in 4 Temple-area) appears only in Taylor's Take, spoken as **"in the Temple area"** with the four named cities — never "around Temple" as a Temple-only fact. The dated ~$469K median is NOT spoken and NOT burned on screen (the market card is pins-only); Taylor's Take reframes "an average tells you nothing about your parcel." Matches the council prompt's own "~1 in 4 Temple-area listings" phrasing and respects the Sage Meadows / Bella Terra MLS-discipline rule. ✓
- **Hook = information, not a tease + no unhedged engineering verdict:** Hook A names three real checks (septic / water tap / legal access) and its build-cost claim is conditional ("can cost you more," not "will"). Every buildability beat across the script stays conditional — "can run well into five figures," "can force a pricier system," "can be legally landlocked," "can be bigger than you'd guess" — never a flat "you can't build here" on the tract on screen. ✓ (Inverse-fail #4 cleared.)
- **Page↔video AGREE on the rollback:** script speaks "several years of those savings, plus interest" — substance-matching the live page ("recovering several years of the tax savings, plus interest") — then hedges as the page does ("confirm the current rollback period … with the Bell County Appraisal District and a tax pro"). The "I won't say a number on camera" theater is removed; the line is "Rollback rules change, so before you touch how the land's used, confirm the current rollback period." NO specific year count anywhere; on-screen card reads "back taxes + interest," no number. ✓ (Inverse-fail #3 cleared.)
- **7-vs-full-list is honest, not amputated:** body open explicitly says "I'm giving you the seven that quietly kill the most deals — the page linked below has the full checklist, **minerals and financing included.**" The script never claims the 7 are the complete diligence set; it routes minerals, financing, and survey to the page. The 7 = highest-leverage on-camera beats, page = full reference (the page→video flywheel's intended division of labor). VA/USDA stays an optional one-liner because financing is fully on the page. ✓
- **Check 7 makes no invented price-inversion verdict:** payoff is the page's hedged, directional version — "the gap between raw land and build-ready can be bigger than you'd guess from the listing — especially on rocky or sloped ground" — NOT "pencils out higher than the move-in-ready place." No quantitative comparative claim asserted as fact; the only dollar reference in the whole script is "well into five figures" for a new well (as briefed + on the page). ✓
- **Cold open lands by ~6s:** Hook A's payoff sentence completes by **[CUT @0:06]**; the three named checks arrive inside that same first beat (0:03–0:06). No deferred-to-0:09 surprise. ✓
- **7 checks stay distinct + no superlative collision + easement collision SOLVED:** "check it the hardest" lives only on floodplain (Check 3); access (Check 4) is "the quiet one that can **stop a deal cold**" — a distinct idea (a binary deal-killer), not a second "scary one." Check 5 explicitly flags the two meanings of "easement" ("in check four an easement was good… here it's the other kind… same word, opposite jobs"), so 4 and 5 don't blur on the load-bearing vocabulary. Floodplain (3) = insurance/buildable/lender; access (4) = your right to get IN; encumbrance-easement (5) = a strip you can't build ON. Each check ends on a forward hook to a *different* idea. ✓ (Inverse-fail #7 cleared.)
- **CTA = genuinely one spoken ask, no humble-brag:** the voice asks for exactly one thing — the checklist — start to finish; the booking link and readiness tool appear only in the on-screen page mock, never voiced as a second CTA; closes on the checklist, not a sell. Office names match the page's actual directory: appraisal district (ag/rollback) · **county health district** for septic (the page routes OSSF to the Bell County Public Health District) · county engineer for floodplain + driveway/culvert. ✓ (Inverse-fail #8 cleared.)
- **Banned words:** none present (no dream/dream home/charming/nestled/turnkey/white glove/hidden gem/exclusive/sneak peek/insider/paradise/oasis/stunning/gorgeous/vibrant community/welcome home/perfect neighborhood). ✓ (Inverse-fail #2 cleared.)
- **"Agent" not "broker"; "Fort Hood" not "Cavazos":** "agent" used; no "broker"; no "Cavazos" (Fort Hood appears only as an area-served reference on the page, not on camera). ✓
- **No invented numbers; no lender endorsement; no IDX/listings/off-market claims:** only "well into five figures" for a new well. No private lender named. ✓ (Inverse-fail #3 cleared.)
- **Buyer-safe hedging throughout:** confirm / verify / depends on the parcel / for your situation / "rollback rules change"; no legal, lending, tax, engineering, or survey guarantees. ✓
- **Lane discipline:** buyer/relocator + build-your-homesite only; zero investor/cap-rate/rental/flip framing; VA/USDA kept to one optional qualified line. ✓ (Inverse-fail #6 cleared.)
- **Operator voice, not city-guide blogger:** opens on a walked-tract operator's counterintuitive judgment, every check carries a "buyers miss this" operator detail (tap at the pad / clay won't perc / handshake dies when the neighbor sells / easement same-word-opposite-jobs / rollback timing), closes on price-the-project arithmetic — not a listicle. ✓ (Inverse-fail #1 cleared.)
- **Length:** ~1,295 spoken words ≈ ~7:45, inside the 7–10 min / 1,100–1,500-word target. ✓
- **Cut cadence:** a marked [CUT] / on-screen change roughly every ~7s throughout. ✓

**How AB beats BOTH inputs:**
1. **Safest defensible hook of the three candidates** — takes B's build-cost-inversion cold open (zero spoken stat, lands at ~0:04) over A's spoken-stat open, because A's own ground-truth note proves the only compressed spoken version of the four-city MLS figure silently narrows it to a Temple-only claim. The stat moves to Taylor's Take, said correctly as "Temple-area, four cities."
2. **Keeps A's sharpest craft** — the same-word-opposite-jobs easement callout, the floodplain-only superlative, the granular ~7s [CUT]/on-screen cadence, and the forward-hook chaining that A executed most cleanly.
3. **Resolves the rollback contradiction once** — "several years" (brief instruction + page's exact words) with the page's hedge, and deletes the "I won't say a number on camera" theater both prior rounds flirted with.
4. **Honest scope** — adopts B's "7 that kill the most deals; full list incl. minerals + financing on the page" framing, so the 7-check video and the live page (which carries more checks) don't contradict.
5. **One spoken ask** — booking link and readiness tool live only in the on-screen mock; the voice stays on the checklist start to finish, with office names matching the page's real who-to-call directory.

**Files referenced (for the derivation step):**
- Live page source: `/Users/taylordasch_1/real-estate-redefined/page-build-queue/buying-land-temple-tx/buying-land-temple-tx.html`
- Companion video council prompt: `/Users/taylordasch_1/claude-social-media-manager/yt-videos/buying-land-temple-tx/council-prompt.md`
- Cluster strategy packet: `/Users/taylordasch_1/real-estate-redefined/page-build-queue/_land-acreage-cluster/CLUSTER-STRATEGY-PACKET.md`
- UTM page link (for description / pinned comment): `https://templetxhomes.net/buying-land-temple-tx/?utm_source=youtube&utm_medium=description&utm_campaign=buying-land-temple-tx`

codex
I’ll treat this as a content/compliance review, not a file-edit turn. I’m loading the repo voice gates and the real-estate YouTube skill so the critique is grounded in the local rules, then I’ll give only fatal/major findings as requested.
exec
/bin/zsh -lc "sed -n '1,260p' CLAUDE.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/buying-land-temple-tx
exec
/bin/zsh -lc "sed -n '1,260p' governance/QUALITY-GATES.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/buying-land-temple-tx
exec
/bin/zsh -lc "sed -n '1,220p' /Users/taylordasch_1/.agents/skills/real-estate-youtube/SKILL.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/buying-land-temple-tx
 exited 1 in 0ms:
sed: CLAUDE.md: No such file or directory

 exited 1 in 0ms:
sed: governance/QUALITY-GATES.md: No such file or directory

 succeeded in 0ms:
---
name: real-estate-youtube
description: Use when planning, scripting, researching, shooting, or packaging YouTube videos for Taylor's real estate business, including Temple TX, Belton, Central Texas, MLS market updates, listings, neighborhood tours, relocation videos, buyer education, seller education, new construction, builder incentives, affordability, and local real estate content. Uses /Users/taylordasch_1/market-monitor/ as the source of truth for MLS pulls before asking Taylor for new MLS data.
metadata:
  version: 1.0.0
---

# Real Estate YouTube

You are Taylor's real estate YouTube strategist. Your job is to create accurate, useful, locally relevant videos that help buyers, sellers, relocators, and homeowners make better decisions while moving viewers toward a natural next step with Taylor.

## Source of Truth

All MLS data lives in:

`/Users/taylordasch_1/market-monitor/`

Before asking Taylor for MLS data, inspect that folder for existing pulls, scripts, reports, or exports. Use local data first. When using market data, state the data date or file basis when possible. Distinguish confirmed facts from interpretation.

Do not invent market stats, days on market, pricing, builder incentives, inventory levels, or sales claims.

## Public Context Check

For local-area, city, neighborhood, relocation, market, or buyer-education videos, check public context when it could help the viewer understand the area. Prioritize official and neutral sources:

- City or municipality official website for location, services, planning, utilities, parks, local government, and community context.
- Relevant school district website for official district/campus information and zoning-verification language.
- Census Reporter, Census QuickFacts, or ACS sources for population, housing, commute, and demographic context.
- County appraisal district, county GIS, TxDOT, or official transportation sources when taxes, parcels, roads, growth, or commute routes matter.
- Chamber, economic development, or official tourism/community pages when local amenities or business context matter.

Use this context to add useful grounding, not filler. Cite or name the source when using a specific fact. Keep Fair Housing guardrails in mind: do not use demographic data to steer, rank, or imply who belongs in an area.

## When to Use This Skill

Use this for:
- Temple TX, Belton, Bell County, Central Texas, and local market videos.
- Buyer, seller, homeowner, investor, relocation, and PCS-style education.
- New construction, builder incentives, community tours, and model home videos.
- Listing walkthroughs and coming-soon content.
- MLS-backed market updates and neighborhood comparisons.
- YouTube topics meant to generate leads for Taylor's real estate business.

Pair with:
- `youtube-video-planner` for full packaging and script plan.
- `youtube-retention-scriptwriter` for hook, pacing, and script rewrites.
- `youtube-shot-director` for filming plans.
- Pikzels-ready thumbnail briefs by default. Use the local `thumbnail` skill only if Taylor explicitly asks for local thumbnail generation.

## Audience Defaults

Unless Taylor says otherwise, assume the audience is one of:
- People moving to Temple/Belton/Central Texas.
- Local homeowners deciding whether to sell.
- Buyers comparing resale vs. new construction.
- People trying to understand monthly market conditions.
- Prospects who want a trustworthy local advisor, not generic real estate hype.

## Taylor Channel Lanes

Taylor has two separate YouTube lanes. Keep them separate and do not recommend combining them unless Taylor explicitly asks for a consolidation strategy.

- `Living in Temple TX`: primary lead-generation channel for buyers, relocators, neighborhood comparisons, BSW medical relocations, Fort Hood/PCS lifestyle questions, local amenities, affordability, resale vs. new construction, and practical moving decisions. Avoid investor-first language on this channel.
- `Investing in Temple TX`: investor channel for deal analysis, cash flow, house hacking, wealth-building, rentals, flips, wholesaling, investor market reads, and military house-hack content.
- Military relocation/lifestyle belongs on `Living in Temple TX`; military house hacking and investing belong on `Investing in Temple TX`.
- BSW is a primary `Living in Temple TX` audience. Frame this as honest local advisory for medical professionals and relocators, not obvious targeting or hype.

## Taylor Coaching Rule

Use the `1-1-1` rule for every real estate video: one viewer, one decision, one proof. If the video starts drifting into multiple audiences or decisions, narrow it before writing.

Taylor's default hook formula:

`[Specific number or contradiction] + [who this is for] + [delayed payoff]`

- Seconds 0-3: lead with a real number, price, stat, contradiction, or local tradeoff.
- Seconds 3-6: name the exact viewer and decision.
- Seconds 6-10: open a payoff that resolves around the 50-60% mark.
- Never start with "Hey guys," a generic welcome, or Taylor's credentials before the viewer has a reason to care.
- Do not invent numbers. If the number is not confirmed, use a non-numeric contradiction or inspect `/Users/taylordasch_1/market-monitor/`.

## High-Leverage Video Formats

### Monthly Market Update

Structure:
1. Hook with the most decision-relevant change.
2. Quick data context: inventory, median price, days on market, sold/list activity, or other available metrics.
3. What it means for buyers.
4. What it means for sellers.
5. One local example or scenario.
6. CTA to schedule a strategy call or request a neighborhood-specific readout.

### Neighborhood or Area Tour

Structure:
1. Who this area may fit based on lifestyle/logistics, not protected-class assumptions.
2. Map context and commute anchors.
3. Housing types and price ranges if data is available.
4. Amenities, parks, shopping, medical, military/base access, or downtown access.
5. Tradeoffs.
6. CTA for a custom area shortlist.

### New Construction / Builder Incentives

Structure:
1. Hook around the real buyer decision: payment, closing costs, rate buydown, inventory, timeline.
2. Explain incentive mechanics in plain English.
3. Show what to verify in writing.
4. Compare against resale tradeoffs.
5. CTA to review current builder options with Taylor.

### Listing Walkthrough

Structure:
1. Hook: the strongest specific reason this listing is worth seeing.
2. Exterior and location context.
3. Main living/kitchen.
4. Primary suite and key rooms.
5. Outdoor space or standout feature.
6. Who should book a showing and why.

### Buyer/Seller Education

Structure:
1. Common mistake or costly assumption.
2. Real local example.
3. Explain the decision framework.
4. Show next step or checklist.
5. CTA to get personalized advice.

## Compliance and Trust Guardrails

- Follow Fair Housing principles. Do not steer based on protected classes.
- Avoid phrases like "safe neighborhood," "family-friendly," "good schools," or demographic claims.
- For schools, use neutral phrasing and official sources: "This address is currently zoned to..." or "Check district boundaries directly."
- Avoid crime claims unless citing a specific public source and advising viewers to verify.
- Do not guarantee appreciation, savings, investment returns, or negotiation outcomes.
- Treat builder incentives as time-sensitive and subject to terms; tell viewers to verify current availability.
- Do not imply legal, tax, lending, or financial advice.
- If data is stale or incomplete, say so plainly.

## Taylor Voice

Default tone:
- Plainspoken, specific, and practical.
- Local advisor, not hype machine.
- Calm confidence.
- Helpful enough that even a non-client gets value.

Avoid:
- Generic agent slogans.
- Overpromising.
- Fear-based manipulation.
- Filler intros.

## CTA Bank

Use CTAs that fit the video:
- "If you want the current numbers for your exact neighborhood, send me the address and I'll pull a custom readout."
- "If you're comparing resale and new construction, I can help you map the real monthly-payment difference."
- "If you're relocating to Central Texas, I can build you a shortlist based on commute, budget, and timeline."
- "If you're thinking about selling, let's look at what buyers are actually choosing right now."

## Output Expectations

For real-estate YouTube requests, include:
- Target viewer.
- Local decision being helped.
- Data needed or data used.
- Public context sources checked or recommended when useful.
- Compliance-sensitive wording notes.
- Script or outline.
- Shot plan if filming is involved.
- CTA.
- Repurposing ideas for Shorts/social when useful.

codex
The local YouTube skill confirms this should stay in the Living-in-Temple buyer lane with no invented stats or legal/tax/lending guarantees. The governance files are at the repo root rather than the video subfolder, so I’m reading those root paths now.
exec
/bin/zsh -lc "sed -n '1,260p' /Users/taylordasch_1/claude-social-media-manager/governance/QUALITY-GATES.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/buying-land-temple-tx
 succeeded in 0ms:
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
| Fort Hood | Fort Hood |
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
| Fort Hood | Fort Hood (NOT Fort Hood) |

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

Never run 2 of the same content pillar in a row (per platform). Check the last 3 entries in content-registry.csv for the relevant platform before generating.

### Short-form pillars (TikTok / Reels / YouTube Shorts):
1. Property Tours
2. Relocation / Military / Medical
3. Market Data
4. Lifestyle / Only in Texas
5. BTS

### Long-form YouTube pillars (Sherrard 5 — see reference/YOUTUBE-GROWTH-PLAYBOOK.md §5 Pillars):
1. Relocation
2. Market Updates
3. Neighborhood Deep Dives
4. Home Tours
5. Lifestyle & Community

Long-form pillar tag is required on every long-form YouTube script + registry entry so pillar-level lead performance can be read (which pillars actually close deals in Bell County). Short-form pillar tag is required on TikTok / Reel / Short registry entries.

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

exec
/bin/zsh -lc "sed -n '1,260p' /Users/taylordasch_1/claude-social-media-manager/CLAUDE.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/buying-land-temple-tx
 succeeded in 0ms:
# Content OS — Taylor Dasch | EG Realty

> This is a governed content operating system, not a prompt library.
> Claude operates as a content operations supervisor, not just a content generator.

## Mission

Produce, validate, track, refresh, and learn from every piece of content across all platforms. Every session should leave the system in a better state than it started.

## Architecture

```
governance/          ← Rules that every skill inherits (read first)
  QUALITY-GATES.md   ← Banned words, data rules, CTA fit, schema — ENFORCED globally
  WORKFLOW-STATE-MACHINE.md  ← Content lifecycle states and transitions
  FACT-HANDLING.md   ← Source provenance, confidence levels, conflict resolution
  SESSION-LOOP.md    ← Default operating procedure for every session
  DEFINITION-OF-DONE.md  ← When is each content type "done"
  MULTI-PASS-SYSTEM.md   ← 5-pass system: Strategist → Producer → Validator → Integrator → Optimizer

data/                ← System state
  content-registry.csv    ← Master index of ALL content assets and their lifecycle state
  performance-ledger.csv  ← Engagement/outcome data (manual update)
  hook-bank.json          ← Rotating hook bank with status tracking
  living-in-temple-catalog.txt / investing-in-temple-catalog.txt  ← Video catalogs

scripts/             ← Automation
  freshness-scanner.py      ← Page freshness + schema + video audit
  output-integrity-check.py ← Catch partial runs, missing files, placeholders, banned words
  dedupe-checker.py         ← Detect title/hook/angle cannibalization
  next-best-action.py       ← Prioritization engine

skills/              ← 15 production skills (see below)
reference/           ← 14 auto-pulled reference docs (data vault, formulas, playbooks)
output/              ← Weekly organized outputs (YYYY-WXX/)
yt-videos/           ← Video prep workspaces
research/            ← AEO research, strategy docs
```

## Inheritance Rules

1. `governance/QUALITY-GATES.md` overrides any quality check in any SKILL.md
2. `governance/FACT-HANDLING.md` overrides any data handling in any skill
3. Individual SKILL.md files define format and structure for their content type
4. `social-media-config.json` is the single source of truth for brand, personas, platforms
5. `reference/TEMPLE-TX-DATA-VAULT.md` is the single source for recurring data points

If a skill contradicts governance, governance wins.

## Session Start (Mandatory — see governance/SESSION-LOOP.md)

Every session:
1. **Ingest** — date, day, quality gates, registry state (silent)
2. **Inspect** — incomplete pipelines, blocked assets, freshness debt, production gaps (report if issues)
3. **Prioritize** — recommend #1 action + top 5 queue
4. **Execute** — on Taylor's direction, using multi-pass system
5. **Validate** — quality gates (silent if pass)
6. **Update** — registry, state machine, downstream task creation
7. **Log** — feedback, stale data notes, learnings

If Taylor has a direct request, skip to step 4 but still run 5-7 after.

## "If Unclear, Do This" Rules

| Situation | Default Action |
|-----------|---------------|
| Taylor asks for content without specifying persona | Check the topic — investor topics default to investor persona, neighborhood topics default to relocator |
| Taylor asks for content without specifying platform | Produce for the highest-leverage platform first (YouTube > Blog > TikTok > Newsletter) |
| Unsure if data is fresh enough | Mark it `[VERIFY — last confirmed YYYY-MM-DD]` and flag |
| Two skills could handle the request | Pick the one that produces more downstream value |
| Taylor says "do whatever needs doing" | Run next-best-action prioritizer |
| Not sure whether to create new or refresh existing | Check registry first — if similar asset exists and is >60 days old, refresh it |
| A number is missing or conflicting | Mark BLOCKED, explain what's needed, continue with rest of output |

## When to Create vs Audit vs Refresh vs Repurpose

| Signal | Action |
|--------|--------|
| Topic has no registry entry | CREATE (new content) |
| Registry entry exists, status = REFRESH_DUE | REFRESH (update existing) |
| Registry entry exists, status = PUBLISHED, no derivatives | REPURPOSE |
| Registry entry exists, low performance score | AUDIT (diagnose why) |
| Page has video mapped but not embedded | EMBED (complete pipeline) |
| Hook bank < 5 fresh hooks per pillar | REFILL (run /hook-bank) |
| Weekly target not met by Thursday | CATCH UP (produce missing types) |

## Quality Hierarchy

When trade-offs are necessary:
1. **Data accuracy** — Never compromise. Wrong numbers erode everything.
2. **Voice authenticity** — Taylor's brand IS the differentiation.
3. **Completeness** — An incomplete pipeline leaks value at every gap.
4. **Timeliness** — Fresh beats perfect. Ship and iterate.
5. **Volume** — Last priority. One CRUSH asset > five MEH assets.

## Email Rules (CRITICAL)
- NEVER use send_email or send_message. ALWAYS use create_draft.
- Taylor reviews and sends all drafts manually.

## Content Voice Rules
1. Analytical, data-driven, honest. Investor-analyst, not salesperson.
2. See `governance/QUALITY-GATES.md` for banned words (Gate 1)
3. Scars and All: honest negatives in applicable content (Gate 4)
4. Question Hook → Answer First
5. Entity declaration: "Taylor Dasch with EG Realty" in first 3 sentences (Gate 2)
6. Pillar rotation: never 2 of same pillar in a row (Gate 12)
7. 7-Second Rule: visual/audio change every 7 seconds in video
8. DM funnels: never fully answer — push to DM for expanded value
9. Key data: $27M+ volume, 100+ transactions, 3yr BP Featured Agent, 76502 Power Zip

## Skills (22)

| Skill | Trigger | Passes |
|-------|---------|--------|
| `/content-calendar` | "plan week", "content calendar" | 1,2,3L,4 |
| `/tiktok-script` | "tiktok script", "tiktok about" | 1L,2,3,4 |
| `/tiktok-performance` | "tiktok trends", "tiktok performance" | 2,5 |
| `/clip-grader` | "clip grader", "score my clips", "rank these shorts", "pick keepers" | 2,3,4 |
| `/instagram-reel` | "instagram reel", "IG reel", "reel about" | 1L,2,3,4 |
| `/youtube-description` | "youtube description" | 2,3,4 |
| `/newsletter` | "newsletter", "investor brief" | 1,2,3,4,5O |
| `/gmb-post` | "gmb post", "gbp post", "monthly gbp" | 2,3L,4 |
| `/deal-of-the-week` | "DOTW", "deal of the week" | 1,2,3,4,5 |
| `/produce` | "produce", "run pipeline" | 1,2,3,4,5 |
| `/repurpose` | "repurpose", "cross-post" | 1,2,3,4,5 |
| `/yt-video` | "new video", "film this" | 1,2,3,4,5 |
| `/weekly-scorecard` | "scorecard", "weekly review" | 2,5 |
| `/weekly-analytics-pull` | "analytics pull", "weekly data", "platform stats" | 2,5 |
| `/hook-bank` | "hooks", "hook bank" | 1L,2,3,4 |
| `/transcript-to-blog` | "yt to blog", "transcript to blog" | 1,2,3,4,5 |
| `/community-post` | "community post", "community tab" | 2,3L,4 |
| `/linkedin-carousel` | "linkedin", "carousel" | 1L,2,3,4 |
| `/reddit-bp` | "reddit post", "BP post", "forum post" | 1L,2,3,4 |
| `/thumbnail-brief` | "thumbnail", "cover image", "CTR image" | 2,3L,4 |
| `/unique-listings` | "unique listings", "FB group listings", "pull listings" | 2,3L,4 |
| `/audit` | "audit", "score this page" | 2,5 |

L = Lite pass. O = Optional pass.

## Reference Docs (auto-pulled by skills)

| Doc | Purpose |
|-----|---------|
| `reference/TEMPLE-TX-DATA-VAULT.md` | Single source for recurring data |
| `reference/VIDEO-SCRIPT-FORMULAS.md` | 6 proven script structures |
| `reference/SCHEMA-LIBRARY.md` | JSON-LD templates |
| `reference/LEAD-MAGNET-MATRIX.md` | Persona → CTA mapping |
| `reference/CONTENT-TO-LEAD-ATTRIBUTION.md` | FUB source tags, UTM structure |
| `reference/YOUTUBE-GROWTH-PLAYBOOK.md` | Algorithm, titles, retention |
| `reference/FILMING-STYLE-GUIDE.md` | Camera, production standards |
| `reference/CONTENT-PRODUCTION-CHECKLIST.md` | Per-video checklist |
| `reference/WEEKLY-CONTENT-BATCH-SOP.md` | Mon-Sun rhythm |
| `reference/OPPORTUNITY-SCANNER-PROMPTS.md` | Gap audit prompts |
| `reference/INTEGRATION-MAP.md` | Cross-project MCP tools + data flow patterns |

## Platform Formatting (summary — full rules in QUALITY-GATES.md Gate 8)
- **TikTok**: ≤60s, 3-5 hashtags (3-tier), DM keyword CTA
- **YouTube Long**: 7-section description, timestamps, entity declaration
- **YouTube Short**: Title must include "Temple TX" + keyword
- **Blog**: BLUF ≤50w, H2s as questions, meta title <60, meta desc <155
- **GMB/GBP**: 4-week rotation (Market Update / Listing Spotlight / Neighborhood Guide / Expertise Tip), ≤300 words, entity declaration required, 2+ citable data points, specific page link (no homepage), AI citation optimized
- **BP**: Data-heavy, NO video links, personal experience
- **Newsletter**: Investor Brief = investors only. Temple Insider = buyers only.

## Automation Triggers

| Event | Auto-Action |
|-------|-------------|
| `/produce` completes | Create registry entries for all outputs + expected downstream (blog at 48h) |
| `/transcript-to-blog` completes | Set refresh_due_date, verify schema sidecar |
| `/yt-video` completes | Register as READY_TO_FILM, add to filming day queue |
| `/audit` finds critical issues | Add fix tasks to action queue |
| Video published >48h without blog | Flag in next session |
| Video exists in VIDEO-TO-PAGE-MAP but page lacks embed | Flag in next session |
| Hook/title matches recent content >70% | Warn and suggest alternative |
| Stat older than freshness window | Flag before reuse |
| CRUSH-rated content | Suggest 3 derivatives + 1 page update |

## Taylor's Info
- Taylor Dasch, EG Realty | 254-718-4249 | dealswithdasch@gmail.com
- templetxhomes.net | Headshot: `https://assets.agentfire3.com/uploads/sites/2128/2025/11/TaylorDaschImage.jpg`

---

## Proactive Business Improvement Rule

**Claude is always watching for what Taylor would miss.**

At the end of any session — or any time something is spotted mid-build — surface:

- Automation opportunities (cron, FUB action plans, Hermes scripts, n8n)
- Revenue levers (listing acquisition gaps, follow-up timing, lead source ROI)
- SEO/AEO/GEO gaps (missing pages, unoptimized content, AI citation misses)
- Customer service improvements (response time, chatbot coverage, review velocity)
- Risk or dead weight (silently failing crons, stale data, abandoned workflows)

Format: one sentence observation + one concrete next action. Don't pitch a project — name the specific thing. Taylor can say yes or no in one word.

<!-- proactive-business-improvement-rule:v1 -->

exec
/bin/zsh -lc "sed -n '1,220p' /Users/taylordasch_1/claude-social-media-manager/governance/FACT-HANDLING.md" in /Users/taylordasch_1/claude-social-media-manager/yt-videos/buying-land-temple-tx
 succeeded in 0ms:
# Fact Handling — Source Provenance & Certainty

> Every important number in output should be traceable.
> This file defines how Claude handles data certainty.

---

## Confidence Levels

| Level | Label | Meaning | Usage Rule |
|-------|-------|---------|-----------|
| 1 | VERIFIED | From authoritative source, confirmed within freshness window | Use freely, no annotation needed |
| 2 | DATED | From authoritative source, but older than freshness window | Use with date stamp: "(MLS, Jan 2026)" |
| 3 | ESTIMATED | Calculated or interpolated from verified data | Mark `[ESTIMATED]` in output |
| 4 | UNKNOWN | No source available | Mark `[NEEDS VERIFICATION]` — do not present as fact |
| 5 | BLOCKED | Required data missing, cannot proceed | Mark `[BLOCKED — need X]` — halt that section |

---

## Source Hierarchy

When multiple sources give different numbers, use this precedence:

1. **MLS pull** (date-stamped) — most authoritative for price/DOM/inventory
2. **Bell County CAD** — most authoritative for tax/assessed values
3. **TEMPLE-TX-DATA-VAULT.md** — canonical reference, use if source date within freshness window
4. **social-media-config.json** — business/performance data, Taylor-confirmed
5. **PropStream** — for equity/owner data
6. **Census/ACS** — for population/demographics
7. **DoD/VA** — for BAH rates, military population
8. **Claude's training data** — NEVER use as source. If no other source exists, mark UNKNOWN.

---

## Freshness Windows

| Data Type | Window | Primary Source |
|-----------|--------|---------------|
| Median home price | 90 days | MLS pull → TEMPLE-TX-DATA-VAULT.md |
| Active inventory count | 30 days | MLS pull |
| Days on market (avg) | 30 days | MLS pull |
| Rental rates | 90 days | MLS/Rentometer |
| BAH rates | Jan 1 annual update | DoD BAH calculator |
| Property tax rates | Annual (set by Oct) | Bell County CAD |
| BSW employee count | 180 days | BSW official / news |
| Fort Hood personnel | 180 days | DoD / AUSA |
| Population figures | 365 days | Census/ACS estimate |
| Builder incentives | 30 days | Direct verification only |
| Interest rates | 7 days | Freddie Mac PMMS |
| Taylor's deal count | Updated by Taylor | social-media-config.json |

---

## Conflict Resolution

When a stat appears differently in two sources:

1. **Check dates.** The more recent verified source wins.
2. **Check specificity.** "Temple 76502 median" beats "Temple median" beats "Bell County median."
3. **Check source authority.** MLS > Zillow > Redfin > training data.
4. **If still unclear:** Use the more conservative number and flag: `[Sourced from X — verify against Y]`.
5. **Never average two conflicting sources.** Pick one and cite it.

---

## Qualitative Claims

For non-numeric claims (e.g., "Temple has a small-town feel"):
- Acceptable if Taylor has said it in recorded content (BP posts, YT transcripts)
- Acceptable if it describes firsthand observation
- NOT acceptable if it's a generic descriptor that could apply to any town
- Must be specific: "Temple still has that 'wave at strangers' energy" > "Temple is a great place to live"

---

## How to Handle Missing Data

| Situation | Action |
|-----------|--------|
| Stat needed but not in TEMPLE-TX-DATA-VAULT.md | Check MLS CSVs in data/. If not there, mark [NEEDS VERIFICATION] |
| Number exists but is older than freshness window | Use it with date annotation: "($247K median, MLS Dec 2025)" |
| Number exists in config but contradicts MLS data | MLS wins. Flag conflict for Taylor. |
| Financial calculation needed | Compute it. Show formula. Never estimate cap rates or cash flow. |
| Competitor data needed | Mark [NEEDS LOOKUP] — do not fabricate competitor stats |
| National comparison needed | Only use if from verifiable source with date. No "national average" without citation. |
| Year-over-year change needed | Both endpoints must be verified. Never compute YoY from one data point. |

---

## Data Vault Update Protocol

When TEMPLE-TX-DATA-VAULT.md is refreshed:
1. Update the `last_verified` date at the top of the file
2. Note which sections were updated
3. Flag any number that changed by >10% — these need downstream content updates
4. Run freshness scanner to identify content using the old numbers

codex
FATAL WEAKNESSES:
1. “I'm Taylor Dasch with EG Realty...” — lands at `0:12`, inside the no-entity first ~15 seconds window. — Rewrite timing/line: `[0:15] I'm Taylor Dasch with EG Realty, and I walk these tracts with buyers across Temple, Belton, Salado, Harker Heights, and the county.`

MAJOR WEAKNESSES:
1. “...the county can hit you with a rollback that recovers several years of those savings, plus interest.” — “Several years” is legally plausible but unnecessarily count-based for evergreen tax content; change both page and video. — Rewrite: `...the county can hit you with a rollback for back taxes plus interest.`

2. “Conventional is the cheaper system.” — too absolute for an engineering/cost claim. — Rewrite: `Conventional is usually the lower-cost system when the soil supports it.`

3. “A handshake with today's neighbor is worth nothing the day he sells. If it's not in the title records, it isn't real...” — overstates a legal/title issue. — Rewrite: `A handshake with today's neighbor may not survive the next sale. If access is not recorded or confirmed in title, treat it as unproven before you offer.`

4. “...the lot can be legally landlocked — and your lender walks.” — unhedged lending outcome. — Rewrite: `...the lot can be legally landlocked, and a lender may refuse to finance it until recorded access is confirmed.`

5. “...what a lender will sign off on.” — unhedged lending claim. — Rewrite: `...what a lender may sign off on.`

6. “...the part that genuinely saves you a week of phone tag...” — unsupported time-savings claim. — Rewrite: `...the part that cuts down the phone tag...`

7. “Work it top to bottom before your option period ends, and you'll know exactly what you're buying.” — overpromises certainty. — Rewrite: `Work it top to bottom before your option period ends, and you'll know what still needs verification before you commit.`

OVERALL VERDICT: ship-ready with your fixes.
tokens used
55,559
FATAL WEAKNESSES:
1. “I'm Taylor Dasch with EG Realty...” — lands at `0:12`, inside the no-entity first ~15 seconds window. — Rewrite timing/line: `[0:15] I'm Taylor Dasch with EG Realty, and I walk these tracts with buyers across Temple, Belton, Salado, Harker Heights, and the county.`

MAJOR WEAKNESSES:
1. “...the county can hit you with a rollback that recovers several years of those savings, plus interest.” — “Several years” is legally plausible but unnecessarily count-based for evergreen tax content; change both page and video. — Rewrite: `...the county can hit you with a rollback for back taxes plus interest.`

2. “Conventional is the cheaper system.” — too absolute for an engineering/cost claim. — Rewrite: `Conventional is usually the lower-cost system when the soil supports it.`

3. “A handshake with today's neighbor is worth nothing the day he sells. If it's not in the title records, it isn't real...” — overstates a legal/title issue. — Rewrite: `A handshake with today's neighbor may not survive the next sale. If access is not recorded or confirmed in title, treat it as unproven before you offer.`

4. “...the lot can be legally landlocked — and your lender walks.” — unhedged lending outcome. — Rewrite: `...the lot can be legally landlocked, and a lender may refuse to finance it until recorded access is confirmed.`

5. “...what a lender will sign off on.” — unhedged lending claim. — Rewrite: `...what a lender may sign off on.`

6. “...the part that genuinely saves you a week of phone tag...” — unsupported time-savings claim. — Rewrite: `...the part that cuts down the phone tag...`

7. “Work it top to bottom before your option period ends, and you'll know exactly what you're buying.” — overpromises certainty. — Rewrite: `Work it top to bottom before your option period ends, and you'll know what still needs verification before you commit.`

OVERALL VERDICT: ship-ready with your fixes.
