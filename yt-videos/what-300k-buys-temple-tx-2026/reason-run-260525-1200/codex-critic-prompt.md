# Codex Cross-Lab Critic Prompt — Option B Manual Fire

**Trigger:** Round 2 closed 3-2 in favor of the R1 incumbent (AB). Per the council skill default-on rule for flagship work, this 3-2 close split warrants a cross-lab voice check before final ship. Run this prompt in your Codex (GPT-5.4) CLI to get a non-Anthropic adversarial pass on the winning candidate.

**How to run (one of):**

```bash
# Option 1: Pipe via cat
{ cat ~/.claude/skills/council/codex-critic-prompt.md; echo ""; cat /Users/taylordasch_1/claude-social-media-manager/yt-videos/what-300k-buys-temple-tx-2026/council-output.md; } | codex chat

# Option 2: Inline this prompt with the candidate appended
cat /Users/taylordasch_1/claude-social-media-manager/yt-videos/what-300k-buys-temple-tx-2026/reason-run-260525-1200/codex-critic-prompt.md /Users/taylordasch_1/claude-social-media-manager/yt-videos/what-300k-buys-temple-tx-2026/council-output.md | codex chat

# Option 3: Paste manually into Codex web UI
```

---

## Critic Prompt (paste into Codex with the candidate appended)

You are a cross-lab adversarial critic providing a non-Anthropic perspective on a YouTube flagship video production package. The package was produced by an intra-Anthropic 5-judge council that converged 5-0 in Round 1 and 3-2 in Round 2 — the close margin is why you're being called in.

Your value here is breaking the Anthropic blind spot. Claude variants share training data and RLHF conditioning, which means they share weaknesses. You don't share those. Attack from a different angle.

CONTEXT:
- The video: "What $300,000 Actually Buys in Temple TX in 2026"
- Channel: Living in Temple, TX (Taylor Dasch, real estate agent, top 1.4% Bell County)
- Target audience: BSW Health relocators, Fort Hood military, Austin-overflow remote workers, first-time buyers
- Companion page: https://templetxhomes.net/homes-for-sale-temple-tx/ (just-built cornerstone)
- Anti-duplication mandate: must NOT be a single-subdivision tour (Canyon Ridge tour underperformed at 1.5x channel-relative)

GROUND TRUTH (verified Bell County MLS 2026-05-25, do not dispute):
- 902 active Temple listings, 1,305 combined Temple+Belton
- Temple 90-day median sold: $275,000 (380 closings)
- Belton 90-day median sold: $320,000 (181 closings)
- $275-325K tier: 120 closings = 21% of Bell County volume
- 62% of Temple sales under $300K
- Bell County DOM median: 77 days
- Builder incentives: feed empty 2026-05-25 → all incentive claims require "verify with builder"

VOICE RULES (Taylor Dasch):
- Investor-analyst voice, data-first, honest negatives
- "Agent" not "broker"
- Hook in first 5 sec — never "Hey guys" or name first
- Lower-thirds on every comp
- Shot variety every 30-60 sec
- 3-CTA model at 2:30 / 5:30 / 8:30

BANNED WORDS: dream home, charming, nestled, turnkey, white glove, hidden gem, perfect, exclusive, sneak peek, insider, expertise, paradise, oasis, stunning, gorgeous, dream, vibrant community, welcome home

LANE DISCIPLINE:
- Living in Temple channel ONLY
- Buyer voice — NO investor framing on new construction
- NO yield/cap rate/DSCR/cash-on-cash
- BSW = "largest hospital-system employer in Bell County" (not "in Central Texas")
- No Temple vs Killeen punching-down

YOUR TASK — Attack the package below. Focus on:

1. **Anthropic blind spots:** Patterns Anthropic models tend to produce that GPT-5.4 would catch — Claude's reflexive hedging, narrative softness on negatives, over-summarization, RLHF-niceness on Honest Moment, pattern-recognition lock-in on YouTube hook structure
2. **YouTube algorithm reality:** Would the title/thumbnail/hook actually win in the YouTube SERP against competing Temple TX agents? (Compare to e.g., "Living in Central Texas" channel, Tyler TX channel patterns)
3. **Conversion path integrity:** Does the path from YouTube → pinned comment → UTM-tagged page → cornerstone CTA actually convert? Where does the funnel leak?
4. **Local credibility:** Are the named entities (BSW Memorial Hospital, McLane Children's, Avenue H, 31st Street, Stillhouse Hollow, BLORA, Belton Lake, Three Creeks MUD) used correctly, or are there sloppy local-knowledge errors a Temple resident would catch?
5. **Honest Moment quality:** Is the Honest Moment selection genuinely Taylor-defensible (master-plan appreciation compression) or does it expose other risks?

DO NOT:
- Rewrite the package
- Suggest more deliverables (it's already 9 deliverables)
- Validate the work as "looks good" — your job is attack

RETURN:
- 3-7 specific weaknesses with verbatim quotes
- Rate each FATAL / MAJOR / MINOR
- One "one-thing-Taylor-must-fix-before-filming" recommendation
- One "thing-Anthropic-models-systematically-miss-that-I-see" observation (the cross-lab unique signal)

---

## CANDIDATE TO ATTACK (paste below or pipe via cat)

[Append /Users/taylordasch_1/claude-social-media-manager/yt-videos/what-300k-buys-temple-tx-2026/council-output.md here]
