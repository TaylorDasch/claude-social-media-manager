# Multi-Pass System — Universal Quality Architecture

> Every skill runs through defined passes.
> Not every skill needs all 5 passes.
> This file defines the passes and which skills use which.

---

## The Five Passes

### PASS 1: STRATEGIST
**Purpose:** Define what we're making and why before making it.

- What is the goal of this asset?
- Who is the target persona?
- What platform is it for?
- What data is required? Is it available and fresh?
- Does this asset already exist? (check content-registry.csv)
- Does this angle duplicate recent content? (check last 30 days)
- What related assets should exist alongside it?
- What's the expected state transition? (IDEA → what end state?)

**Output:** Go/no-go decision + brief spec (persona, platform, angle, data sources, expected files)

### PASS 2: PRODUCER
**Purpose:** Generate the actual content.

- Follow the skill's SKILL.md for format and structure
- Use voice rules from `skills/voice-learning/SKILL.md`
- Pull data from canonical sources per FACT-HANDLING.md
- Apply platform formatting per QUALITY-GATES.md Gate 8
- Include Scars & All where applicable (Gate 4)

**Output:** Draft content in the skill's specified format

### PASS 3: VALIDATOR
**Purpose:** Check against global quality gates before delivery.

Run these checks (from QUALITY-GATES.md):
- [ ] Gate 1: No banned language
- [ ] Gate 2: Entity consistency
- [ ] Gate 3: Data integrity (all numbers sourced, no hallucinated math)
- [ ] Gate 4: Scars & All present (if applicable)
- [ ] Gate 5: CTA matches persona + platform
- [ ] Gate 6: Schema present (if applicable)
- [ ] Gate 7: Internal links present (if applicable)
- [ ] Gate 8: Platform formatting correct
- [ ] Gate 9: No stale data
- [ ] Gate 10: Output completeness (all required files exist per DEFINITION-OF-DONE.md)
- [ ] Gate 12: Pillar rotation (no repeat)
- [ ] Gate 13: No duplicate hooks/titles

**If HARD gate fails:** Fix before proceeding.
**If SOFT gate fails:** Note warning, proceed.
**If all pass:** Proceed silently (don't list checks to Taylor).

**Output:** Validated content OR fix + re-validate

### PASS 4: INTEGRATOR
**Purpose:** Update system state after delivery.

- Add/update entry in `data/content-registry.csv`
- Set appropriate status in state machine
- Set refresh_due_date
- Create entries for expected downstream assets (status: IDEA)
- Update VIDEO-TO-PAGE-MAP.md if new video-page relationship created
- Update `data/hook-bank.json` if hooks were used or generated

**Output:** Updated registry + state

### PASS 5: OPTIMIZER
**Purpose:** Identify what to do next with this asset.

- Should this be repurposed? For which platforms?
- Is there a page that should embed this?
- Is there a related topic that would strengthen this cluster?
- Did a recent performance signal suggest expanding this topic?
- Should this trigger a refresh of related content?

**Output:** 1-3 concrete next actions added to queue

---

## Pass Requirements by Skill

| Skill | Pass 1 | Pass 2 | Pass 3 | Pass 4 | Pass 5 |
|-------|--------|--------|--------|--------|--------|
| /produce | YES | YES | YES | YES | YES |
| /transcript-to-blog | YES | YES | YES | YES | YES |
| /yt-video | YES | YES | YES | YES | YES |
| /deal-of-the-week | YES | YES | YES | YES | YES |
| /newsletter | YES | YES | YES | YES | Optional |
| /content-calendar | YES | YES | Lite* | YES | No |
| /tiktok-script | YES | YES | YES | YES | No |
| /youtube-description | No | YES | YES | YES | No |
| /gmb-post | No | YES | Lite* | YES | No |
| /community-post | No | YES | Lite* | YES | No |
| /repurpose | YES | YES | YES | YES | YES |
| /hook-bank | Lite* | YES | YES | YES | No |
| /linkedin-carousel | Lite* | YES | YES | YES | No |
| /instagram-reel | Lite* | YES | YES | YES | No |
| /audit | No | YES | No | No | YES |
| /weekly-scorecard | No | YES | No | No | YES |
| /weekly-analytics-pull | No | YES | No | No | YES |
| /tiktok-performance | No | YES | No | No | YES |
| /thumbnail-brief | No | YES | Lite* | YES | No |

**Lite Pass 1** = Check dedup + persona fit only, skip full strategy.
**Lite Pass 3** = Check banned words + entity consistency only, skip schema/linking.

---

## Implementation

Skills don't need to explicitly call each pass. Claude runs them internally as part of content generation. The passes are a mental model and a checklist — not separate API calls or scripts.

When a session runs any skill:
1. Claude internally runs the applicable passes
2. Only surfaces issues to Taylor (silent when clean)
3. Updates registry and state (Pass 4) automatically
4. Mentions optimization opportunities (Pass 5) briefly at the end

The validator (Pass 3) is the non-negotiable gate. Everything else can be compressed for speed on simple tasks.
