# Content OS Quality Upgrade — Design Spec

**Goal:** Upgrade the social media content system for higher quality output: native TikTok property tours (not YT repurpose), clean registry hygiene, and tighter repurpose pathways.

**Context:** Taylor is switching TikTok from desk-scripted clips to iPhone+gimbal property tours with improv delivery and talking point prep sheets. The repurpose skill incorrectly treats TikTok as a YouTube derivative. The content registry has 63 entries all stuck at NEEDS_REVIEW.

---

## 1. TikTok Skill Rewrite

**Current state:** Generic desk-script format (talking head, green screen, walk-and-talk). Assumes fully scripted delivery.

**New state:** Property Tour Prep Sheet. Improv-first with talking points. iPhone + gimbal on-site tours with buyer value-add callouts per room.

### Output format:
- Tour route (room order with purpose for each stop)
- Talking points per stop (2-3 bullet points, data-backed buyer value-adds)
- Persona overlay (which persona this tour serves, what angle to emphasize)
- Hook concept (first 3 seconds — what stops the scroll, filmed on-site)
- Gimbal shot notes (movement style, transitions, drone if applicable)
- Caption + hashtags + DM keyword CTA
- Editing notes for post-production

### Key design decisions:
- NOT a full script — talking points only. Taylor improvises.
- Every stop must have a buyer value-add (not just "nice kitchen" — WHY it matters financially or lifestyle-wise)
- Persona-specific angles baked in (BSW commute, BAH affordability, school zone, investor skip)
- Property Tours and Relocation are the only TikTok pillars (no investor content per Taylor's rule)

## 2. Repurpose Skill Fix

**Current state:** "From YouTube Long-form → 60-Second Short/Reel Script" treats TikTok as derivative content.

**New state:** Remove YouTube → TikTok pathway. TikTok is its own original content lane. Keep all other repurpose paths.

### Changes:
- Remove "60-Second Short/Reel Script" from YouTube Long-form derivatives
- Remove "From TikTok → 3 Platforms" section (TikTok tours are original, not repurposed FROM other content)
- Add note: TikTok content is original property tours, not derivatives
- Keep: YouTube Shorts as its own thing (search-optimized, different from TikTok tours)

## 3. Registry Hygiene

**Current state:** 63 entries, every `last_reviewed` = NEEDS_REVIEW. No enforced freshness.

**Fix:**
- Set `last_reviewed` to actual review date (today) for all PUBLISHED entries
- Set proper `refresh_due_date` based on staleness rules from WORKFLOW-STATE-MACHINE.md
- Verify status accuracy for QUEUED/SCRIPTED entries
- Remove template entries (TPL-*) from content registry (they're not content)

## 4. Quality Gates Update

- Add Gate 14: TikTok Native Check — TikTok scripts must be property tour format, not repurposed clips
- Update DEFINITION-OF-DONE.md TikTok section to match new tour prep sheet format
