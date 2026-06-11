export const meta = {
  name: 'land-video-council',
  description: 'Adversarial reason loop (5 blind judges, up to 3 rounds, converge@2) for the buying-land Temple TX companion YouTube video script',
  phases: [
    { title: 'Round 1' },
    { title: 'Round 2' },
    { title: 'Round 3' },
  ],
}

const TASK = `PRODUCE: the CREATIVE CORE of a 7-10 min long-form YouTube video for Taylor Dasch's "Living in Temple" channel (relocation/buyer lane).
WORKING TITLE: "Buying Land Near Temple, TX? Do These 7 Checks Before You Offer."
GOAL: make a buyer trust Taylor as THE local land guide, drive them to the page /buying-land-temple-tx/ (which has an interactive readiness check + a Bell County who-to-call directory + a free printable checklist), and set up 1-3 Shorts.

WHAT EACH CANDIDATE MUST CONTAIN (creative core only — NOT thumbnail/shotlist/shorts/description; those are derived later):
1) FULL word-for-word script, 7-10 min (~1100-1500 words spoken), with rough timestamps and inline [ON-SCREEN: ...] / [B-ROLL: ...] cues. Cold-open HOOK first (<15s) BEFORE any name/intro.
2) A TALKING-POINTS version (bullet outline Taylor can shoot from without a teleprompter) covering the same beats.
3) THREE distinct 15-second HOOK variants; flag the recommended one.
4) ONE recommended video TITLE (<=60 chars, includes "Temple" or "Central Texas").

STRUCTURE (locked): cold-open hook -> "why cheap land is sometimes cheap" -> the 7 checks (each a crisp, screenshottable on-camera beat that ends with a reason to keep watching) -> Taylor's Take -> CTA to the free checklist + a 15-min call. End on the checklist CTA, not a hard sell. Aim for a visual/audio change roughly every 7 seconds (mark cut points).

THE 7 CHECKS (do not invent beyond this):
1 WATER — private well (you own + maintain pump/quality; a new well runs well into 5 figures) vs rural Water Supply Corporation tap (confirm a tap is PAID FOR and physically at the pad, not just a line down the road — thousands of $ and sometimes a waitlist apart) vs city line (confirm it reaches the buildable spot).
2 SEPTIC/OSSF — will the soil perc? Heavy clay or rock (common in parts of Bell County) can force a pricier engineered/aerobic system or shrink where you can build. Conventional (cheaper) vs aerobic (spray field + annual maintenance contract). The "unbuildable" surprise is usually a septic surprise. Make the option period long enough to get a soil evaluation.
3 FLOODPLAIN — pull the FEMA map + read the survey. Creek-adjacent land near Temple/Belton/Salado is where it matters. Changes insurance, buildable area, and what a lender allows.
4 LEGAL RECORDED ACCESS — the quiet deal-killer. Reaching land by driving across a neighbor's field with no recorded easement = legally landlocked. Must be public road frontage or a recorded easement that runs with the land. "There's a driveway" is NOT "there's legal access."
5 DEED RESTRICTIONS / "no zoning is not no rules" — TX counties have limited zoning, but floodplain rules, OSSF permitting, city ETJ platting, utility easements, and private deed restrictions still apply. Freedom is in how you use the home, not a free pass on the land.
6 AG VALUATION + ROLLBACK — ag valuation taxes qualifying land on productive use (big annual savings). Take it out of ag use and the county can assess a ROLLBACK tax recovering several years of savings + interest. NEVER state a specific year count — say "several years"; tell viewers to confirm the current rollback period with the Bell County Appraisal District + a tax pro.
7 TRUE BUILD-READY COST — "Land price is not all-in cost." Budget dirt/site work + pad, septic install, well or co-op tap, driveway + culvert, utility runs (electric, propane, internet), survey/permits. The dirt is the down payment on the project, not the whole bill.

FREE CHECKLIST TEASE (the page now has it): "I put the actual Bell County phone numbers for each of these — the appraisal district, the county septic office, the engineer for floodplain and driveways — in a free checklist linked below." (Do NOT read long phone numbers on camera; point to the checklist.)

GROUND-TRUTH MLS SIGNAL (label as dated, June 1 2026 export, "verify current"): ~1 in 4 Temple-area listings reference acreage; the median of acreage-referencing listings is ~$469K; Salado punches above its size; the pockets are Temple ETJ / Belton / Salado / Harker Heights.

TAYLOR'S LOCKED TAKE (keep voice consistent): "The land mistakes I see aren't emotional — they're arithmetic." Someone finds 10 acres priced under the neighbors, writes a fast offer, then prices the septic the clay won't pass, the well they assumed was a co-op tap, and the driveway + culvert the county requires. The land was never the problem; the BUILD-READY BUDGET was, and nobody added it up before the option period ran out. "Buy the dirt for what it can become, priced for what it'll cost to get there." Usable dirt beats pretty dirt.

VOICE (enforce): analyst / active-operator / calm-but-blunt guide. Data first, interpretation second. Honest negatives. Entity line "Taylor Dasch with EG Realty" inside the first ~3 sentences of the BODY but NOT in the first ~15 seconds (hook first). Say "agent" NOT "broker." Say "Fort Hood" NOT "Cavazos." Buyer-safe hedging throughout: verify / confirm / depends on the property / ask before you offer. NO legal, lending, tax, engineering, or survey guarantees. Optional credibility (use at most lightly): $30M+ volume, 100+ transactions, ranked #28 of 2,013 Bell County agents.

BANNED WORDS (zero tolerance): dream home, charming, nestled, turnkey, white glove, hidden gem, perfect neighborhood, exclusive, sneak peek, insider, paradise, oasis, stunning, gorgeous, dream, vibrant community, welcome home.

LANE DISCIPLINE: buyer/relocator + build-your-homesite. NO investor pivots, NO cap rates, NO rental/cash-flow analysis, NO "great flip." Light optional one-liner OK: VA/USDA financing exists for those who qualify (no deep military lane).

DO NOT: state a specific ag rollback year count; invent prices beyond "~$469K median" + "5 figures for a well"; name a specific private lender as an endorsement; promise IDX/listings; make "off-market" claims; use real/fabricated client names (anonymize any story).

INVERSE-FAIL (avoid): (1) reads like a generic city-guide blogger or a Zillow listicle instead of an operator who walks tracts; (2) any banned word or "broker"/"Cavazos"; (3) a specific rollback year or invented number; (4) a legal/lending/engineering guarantee instead of verify/confirm/depends; (5) the name/entity line in the first 15s killing the hook; (6) investor/cap-rate drift; (7) the 7 checks blur together instead of each a distinct beat; (8) a CTA that over-sells instead of pointing to the genuinely useful free checklist.`

const JUDGE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['winner', 'runnerUp', 'reasoning', 'winningStrength', 'runnerUpGap'],
  properties: {
    winner: { type: 'string', enum: ['X', 'Y', 'Z'] },
    runnerUp: { type: 'string', enum: ['X', 'Y', 'Z'] },
    reasoning: { type: 'string', description: '2-4 sentences citing specific text from the candidates' },
    winningStrength: { type: 'string', description: 'the single strongest element of the winner' },
    runnerUpGap: { type: 'string', description: 'the specific gap that kept the runner-up from winning' },
  },
}

// Deterministic per-round label permutations (no RNG — keeps the synthesis from always hiding behind the same letter)
const PERMS = {
  1: { X: 'AB', Y: 'A', Z: 'B' },
  2: { X: 'A', Y: 'B', Z: 'AB' },
  3: { X: 'B', Y: 'AB', Z: 'A' },
}

const JUDGES = [
  { id: 'Retention', persona: 'YouTube Retention Engineer', lens: 'Does the cold open hook in under 15s? Is there a pattern/visual change roughly every 7s? Does each of the 7 checks END with a reason to keep watching? Would the first 30s survive a swipe-away?' },
  { id: 'Contrarian', persona: 'Contrarian editor', lens: 'Is the "cheap land is cheap for a reason" frame honest and non-obvious, or does it soften into a brochure? Are the negatives real and specific, not hedged into mush?' },
  { id: 'Viewer', persona: 'Real Temple-area land shopper (the actual viewer)', lens: 'Would I trust this person to walk my tract? After watching, do I know exactly what to DO Monday morning? Is anything confusing or condescending?' },
  { id: 'Analyst', persona: 'Fact/compliance analyst', lens: 'Are all numbers defensible and dated? Is every hedge present (verify/confirm/depends)? Zero invented facts, zero banned words, zero "broker"/"Cavazos", no specific rollback year, no legal/lending guarantee? Entity line placed AFTER the 15s hook?' },
  { id: 'Scout', persona: 'Content-strategy Scout', lens: 'Does it cleanly set up the 3 Shorts + the page/checklist CTA + future cluster videos (Belton, Salado, unrestricted land) WITHOUT cannibalizing them? Is the title click-worthy and honest?' },
]

function block(label, text) { return `\n---\nCANDIDATE ${label}:\n${text}\n---\n` }

let incumbentText = null
let incumbentRole = null
let consec = 0
const rounds = []

for (let r = 1; r <= 3; r++) {
  phase('Round ' + r)

  // --- Phase 2: Author-A ---
  const aPrompt = incumbentText
    ? `${TASK}\n\nYOUR ROLE: Author-A, round ${r}. Here is the current best candidate. IMPROVE it — restructure, prune, sharpen the hook, tighten each of the 7 beats; do NOT reproduce it verbatim and do NOT just paraphrase. Produce a genuinely better creative-core package.\n${block('(current best)', incumbentText)}`
    : `${TASK}\n\nYOUR ROLE: Author-A, round 1, cold start. No prior candidates. Produce your single best creative-core package. Don't hold back.`
  const A = await agent(aPrompt, { label: `r${r}:author-A`, phase: 'Round ' + r })

  // --- Phase 3: Critic (sees ONLY A) ---
  const critique = await agent(
    `You are an adversarial critic of a YouTube video SCRIPT PACKAGE for a real-estate channel. ATTACK it ruthlessly — your job is to find what's weak, NOT to praise or fix.\nRULES: find a MINIMUM of 3 distinct, SUBSTANTIVE weaknesses; each must quote/reference the exact line or beat it attacks; rate each [FATAL|MAJOR|MINOR]; do NOT offer fixes; end with one "VERDICT:" line naming the single weakest point.\nWatch especially for: a hook that doesn't land in 15s; the 7 checks blurring together; brochure-softening of honest negatives; any banned word (dream home, charming, nestled, turnkey, hidden gem, etc.) or the word "broker" or "Cavazos"; a specific ag-rollback year count; invented prices; a legal/lending/engineering guarantee; the entity/name line landing inside the first 15 seconds; investor/cap-rate drift on a buyer video; a CTA that over-sells.\n${block('TO ATTACK', A)}`,
    { label: `r${r}:critic`, phase: 'Round ' + r })

  // --- Phase 4: Author-B (task + A + critique) ---
  const B = await agent(
    `${TASK}\n\nYOUR ROLE: Author-B. Below is a previous attempt (Candidate A) and an adversarial critique of it. Produce a BETTER creative-core package that fixes at least the FATAL and MAJOR weaknesses while preserving what A did well. Rethink structure where the critique reveals a deeper issue — don't just patch. Do NOT reference the critique explicitly. Do NOT reproduce A verbatim.\n${block('A', A)}\n---\nADVERSARIAL CRITIQUE OF A:\n${critique}\n---`,
    { label: `r${r}:author-B`, phase: 'Round ' + r })

  // --- Phase 5: Synthesizer (task + A + B only, NOT the critique) ---
  const AB = await agent(
    `${TASK}\n\nYOUR ROLE: Synthesizer. You have two candidate creative-core packages. Produce CANDIDATE AB that is superior to BOTH: take the strongest hook, the crispest 7-check beats, the best Taylor's-Take and CTA from each. Combine strengths — do NOT average into mediocrity, do NOT invent claims neither supports, do NOT hedge contradictions. It must read as ONE coherent package. Begin with a 2-3 sentence note in [brackets] on what you took from each, then the full package.\n${block('A', A)}${block('B', B)}`,
    { label: `r${r}:synth`, phase: 'Round ' + r })

  // --- Phase 6: blind judge panel ---
  const byRole = { A, B, AB }
  const perm = PERMS[r]
  const labeled = { X: byRole[perm.X], Y: byRole[perm.Y], Z: byRole[perm.Z] }

  const votes = await parallel(JUDGES.map((j) => () =>
    agent(
      `You are an expert evaluator: ${j.persona}. Domain: content (YouTube real-estate video for a Temple, TX buyer audience). Here is the task the candidates were written for:\n${TASK}\n\nThree candidate packages follow under arbitrary labels X/Y/Z — label order implies NOTHING about quality. You MUST pick one winner (no ties — force-rank if close) and one runner-up. Evaluate on accuracy, completeness, reasoning, and practical applicability, THROUGH YOUR PERSONA LENS: ${j.lens}\nCite SPECIFIC text. Do NOT pick on length or surface style — substance, frame, voice-fit, and retention win.\n${block('X', labeled.X)}${block('Y', labeled.Y)}${block('Z', labeled.Z)}`,
      { label: `r${r}:judge:${j.id}`, phase: 'Round ' + r, schema: JUDGE_SCHEMA })
      .then((v) => ({ judge: j.id, ...v }))
  ))

  // --- tally (decode labels -> roles) ---
  const tally = { A: 0, B: 0, AB: 0 }
  const runner = { A: 0, B: 0, AB: 0 }
  const decoded = []
  votes.filter(Boolean).forEach((v) => {
    const wRole = perm[v.winner]
    const rRole = perm[v.runnerUp]
    tally[wRole]++
    runner[rRole]++
    decoded.push({ judge: v.judge, winnerRole: wRole, runnerUpRole: rRole, reasoning: v.reasoning, winningStrength: v.winningStrength, runnerUpGap: v.runnerUpGap })
  })

  // plurality, with tiebreak: runner-up votes, then incumbent (status-quo), then AB>A>B
  const maxVotes = Math.max(tally.A, tally.B, tally.AB)
  const top = ['AB', 'A', 'B'].filter((k) => tally[k] === maxVotes)
  let winnerRole
  if (top.length === 1) {
    winnerRole = top[0]
  } else {
    const byRunner = top.slice().sort((a, b) => runner[b] - runner[a])
    if (runner[byRunner[0]] !== runner[byRunner[1]]) winnerRole = byRunner[0]
    else if (incumbentRole && top.includes(incumbentRole)) winnerRole = incumbentRole
    else winnerRole = top.includes('AB') ? 'AB' : top[0]
  }

  if (winnerRole === incumbentRole) consec++
  else { consec = 1; incumbentRole = winnerRole }
  incumbentText = byRole[winnerRole]

  rounds.push({
    round: r,
    labelMap: perm,
    tally,
    winnerRole,
    consec,
    critiqueHead: critique.split('\n').filter((l) => /FATAL|MAJOR|VERDICT/i.test(l)).slice(0, 6),
    judgeNotes: decoded.map((d) => ({ judge: d.judge, winnerRole: d.winnerRole, winningStrength: d.winningStrength, runnerUpGap: d.runnerUpGap })),
    wordcounts: { A: A.split(/\s+/).length, B: B.split(/\s+/).length, AB: AB.split(/\s+/).length },
  })

  log(`Round ${r}: tally A=${tally.A} B=${tally.B} AB=${tally.AB} -> winner ${winnerRole} (consec ${consec})`)
  if (consec >= 2) { log(`Converged: ${winnerRole} won ${consec} consecutive rounds.`); break }
}

return {
  converged: consec >= 2,
  finalWinnerRole: incumbentRole,
  roundsRun: rounds.length,
  finalWinnerText: incumbentText,
  lineage: rounds,
}
