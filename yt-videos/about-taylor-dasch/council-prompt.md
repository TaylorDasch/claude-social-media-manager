# Council Prompt — About-Taylor Companion Video

**Use this for:** `/council` skill (autoresearch:reason or council workflow).
**Inputs required before running:** `deepmode-output.md` in this folder (produced by `deepmode-prompt.md`).
**Output target:** A single shipping packet at `~/claude-social-media-manager/yt-videos/about-taylor-dasch/SCRIPT.md` plus supporting files (see Output Contract).

---

## Goal in one sentence

Converge on a 4–6 minute YouTube script that lives on the **Living in Temple, TX** channel, embeds on **templetxhomes.net/about/**, doubles as legitimate relocation-buyer content (so the algorithm doesn't relegate it as brand fluff), and tells viewers exactly who Taylor Dasch is and which three lanes he serves — **without depending on dollar figures in the spoken script**.

---

## Required reading before any author writes

1. The full `deepmode-output.md` in this folder (mandatory).
2. The brand voice rules below (mandatory).
3. The `/about/` page content at `~/real-estate-redefined/page-build-queue/about-taylor-dasch/agentfire-code-block.txt` for tone consistency (the video should sound like the same person who wrote that page).
4. Taylor's CLAUDE.md production rules at `~/CLAUDE.md` "Shot List & Script Production Rules" — Toma/contratoma alternating, 7–12s blocks, A/B notation, pattern interrupts, solo backup plans.

---

## Hard constraints (any violation = automatic critic veto)

| Rule | Hard constraint |
|---|---|
| Spoken hook | Must NOT depend on saying "$30M", "100 deals", or any dollar figure. Numbers may appear in lower-third graphics only. |
| Voice | Analyst-first, investor-second, agent-third. Direct, data-grounded, opinion-confident. No warm/charismatic mode. |
| Banned words | turnkey, dream home, charming, nestled, vibrant community, hidden gem, welcome home. |
| Title | "agent" not "broker". EG Realty is the brokerage; Taylor is the agent. |
| Channel | Living in Temple (Lane 01 — relocation/buyer). Investor-only material may appear briefly but cannot dominate. |
| Lane mix | Three lanes must be named: Investor, BSW Medical, Military PCS. The "three lanes" framing is the spine of the contradiction. |
| Length | 4–6 minutes long-form. Plus 3 vertical Shorts (45–60s each) pulled from the same shoot. |
| Block size | YouTube long-form script written in **7–12 second blocks**, each tagged (A) or (B). A/B must alternate — no three-in-a-row of the same letter. |
| Solo backup | Every shot in the shot list must have a solo backup plan (locked-off tripod, handheld stabilized, or static frame) in case Taylor's wife is unavailable for gimbal. |
| Local moat | At least 2 shots only a Temple-based agent could capture (BSW campus, Belton ISD neighborhood, specific Temple landmark). |
| Pattern interrupt | One pattern interrupt every 60–90 seconds in the middle third of the long-form. Type called out (location change, prop, graphic, energy shift). |
| TikTok cuts | Shorts repurposed to TikTok must be buyer/relocator content only. NO investor-only Shorts on TikTok. |
| Conversion | Pinned comment with UTM-tagged link: `https://templetxhomes.net/about/?utm_source=youtube&utm_medium=description&utm_campaign=about-taylor`. End-screen CTA points to the same. |

---

## Council rounds

### Round 1 — Authors (3 parallel drafts)

Spawn **3 author agents** with distinct personas. Each writes a full 4–6 minute script independently using the deepmode synthesis as their brief.

- **Author A — The Contrarian.** Lead with the "three lanes" contradiction. Sharp, direct, slightly aggressive. The hook is a refusal: "I turn down most of the people who call me."
- **Author B — The Operator.** Lead with the operator/analyst framing. The hook is a method claim: "I underwrite my own portfolio before I underwrite yours."
- **Author C — The Insider.** Lead with the "what nobody tells you about Temple real estate" framing. The hook is a local-intelligence promise that delivers in act 2.

Each author MUST produce:
- Full script in 7–12 second (A)/(B) blocks
- 3 alternate hook openers
- Title and description
- Thumbnail brief (3 sentences describing image)
- Shot list with solo backups
- 3 Shorts cuts (timestamp range + standalone hook + standalone CTA)

### Round 2 — Critic attack

Spawn **3 critic agents**, each with a specific lens. Each critic attacks all three Round-1 drafts and outputs a list of weaknesses with timestamps:

- **Critic 1 — Retention Doctor.** Identifies every spot the viewer would close the tab. Hook strength, the 30-second cliff, mid-video sag, end-screen drop. Targets minimum 12 weaknesses per draft.
- **Critic 2 — Brand Compliance Auditor.** Cross-checks against the hard constraints table above + the banned-word list + the voice rules. Flags every breach. Also flags any line that reads as generic real-estate agent (the warm/charismatic mode Taylor refuses).
- **Critic 3 — Lane Disciplinarian.** Checks each script for lane discipline. Are the three lanes genuinely named? Is one over-weighted? Does the BSW lane have enough hook-specific language? Does the investor lane name BRRRR/MTR/buy-and-hold concretely? Does the military lane survive (or is it cut for runtime)?

### Round 3 — Candidate B (synthesis)

A synthesis agent reads all 3 author drafts + all 3 critic attacks. It produces **Candidate B** — a single revised script that:
- Picks the strongest hook across the 3 drafts (must be a non-dollar contradiction)
- Repairs every Round-2 weakness
- Honors all hard constraints
- Keeps Taylor's voice (analyst-first, no warm-charismatic drift)

Candidate B is the production candidate.

### Round 4 — Judge verdict

Spawn **5 judge agents**. Each scores Candidate B on a 1–5 scale across 7 dimensions and writes a 1-paragraph verdict.

- **Judge 1 — YouTube Algorithm:** hook strength, retention curve, channel-fit on Living in Temple, predicted 7-day view performance vs the channel's average
- **Judge 2 — BSW Physician Audience:** does this make a BSW resident or attending feel "yes, this agent gets me"?
- **Judge 3 — Out-of-State Investor:** does this make a buy-and-hold investor in Austin/Dallas/Houston feel "yes, I'd call this guy"?
- **Judge 4 — AEO/GEO Citation:** would ChatGPT/Perplexity preferentially cite the YouTube video (via transcript) or the /about/ page when someone asks "who is the best agent near BSW Temple"?
- **Judge 5 — Conversion Engineer:** does the pinned comment + UTM + end-screen actually drive measurable contact-page traffic, or is the CTA architecture too soft?

Each judge issues one of three verdicts: **APPROVE**, **APPROVE-WITH-CAVEAT**, or **REJECT**. If any judge says REJECT, go back to Round 3 with that judge's notes as the patch list. Otherwise, ship.

Convergence target: **4 of 5 judges APPROVE or APPROVE-WITH-CAVEAT**, with REJECT count = 0.

---

## Output contract (what ships when the council converges)

Save these files in `~/claude-social-media-manager/yt-videos/about-taylor-dasch/`:

| File | Contents |
|---|---|
| `SCRIPT.md` | Full final script in (A)/(B) blocks, each block timestamped, with overlay/lower-third callouts where stats appear visually |
| `HOOK-VARIANTS.md` | The 5 strongest hook openers from the council, ranked, in case Taylor wants to A/B test |
| `SHOT-LIST.md` | A-roll and B-roll grouped by filming day. Every shot has a solo backup. Local-moat shots flagged. Pattern interrupts marked with timestamp + type. |
| `TITLE-DESCRIPTION.md` | Final title + description + tags + end-screen + pinned comment (with UTM link) |
| `THUMBNAIL-BRIEF.md` | Final thumbnail concept in concrete visual terms — subject placement, text overlay, color palette |
| `SHORTS.md` | 3 vertical Shorts: each with hook, script, timestamp range from long-form, standalone CTA, platform list (YT Shorts + IG Reels + TikTok — buyer-only on TT) |
| `LINEAGE.md` | Round-by-round summary: which author the winning hook came from, which critic notes were repaired, which judge said what. Useful for post-mortem and next video. |

---

## Convergence rationale (load-bearing)

The video is doing two jobs that usually conflict: it must serve the Living-in-Temple channel's relocation-buyer audience AND act as a citation surface for AI assistants answering "who is this agent." The council exists to make sure those two jobs don't break each other. Authors generate divergent drafts; critics force discipline; the synthesizer picks the move that solves both jobs; judges verify the move actually works for both audiences plus the channel + the conversion path.

If the council can't converge after Round 4 → patch → Round 4-again, **do not ship the video**. Re-run `deepmode-prompt.md` with a tighter brief and start over. A weak about-me video on the channel is worse than no video — the algorithm punishes brand fluff hard.

---

## After convergence — handoff to filming

The shipped packet feeds directly into Taylor's filming workflow:
1. Taylor reviews SCRIPT.md, picks HOOK-VARIANTS.md alternate if desired
2. Films per SHOT-LIST.md in one session (long-form + 3 Shorts)
3. Editor cuts to SHOT-LIST + adds overlays per SCRIPT.md
4. Upload package: TITLE-DESCRIPTION.md values + THUMBNAIL-BRIEF.md image
5. Pinned comment fires per TITLE-DESCRIPTION.md
6. After publish: embed iframe in /about/ between Chapter II and Chapter III; add VideoObject schema node to the @graph
7. Shorts queued via Postiz across YT Shorts / IG Reels / TikTok (TT = buyer cuts only)
