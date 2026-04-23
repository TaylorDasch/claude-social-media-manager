---
name: voice-guardian
description: Score any social media, email, blog, or video script draft against Taylor Dasch's voice rules using Claude Haiku. Returns 0-100 score + specific issues + rewrite suggestion. Run before shipping any public-facing content to prevent voice drift, banned phrases, wrong-audience mistakes, and generic real estate language. Threshold — ship at 85+, strict mode requires 90+.
---

## Governance

Read `governance/QUALITY-GATES.md` before generating content. QUALITY-GATES overrides any quality check in this skill. Also consult:
- `governance/FACT-HANDLING.md` — source provenance + conflict resolution
- `governance/DEFINITION-OF-DONE.md` — when each content type is done
- `governance/MULTI-PASS-SYSTEM.md` — 5-pass pipeline integration points

# Voice Guardian Skill

## When to invoke

**Before shipping any public-facing content.** No exceptions. Voice Guardian is the gatekeeper between draft and publish.

Required invocations:
- After generating a TikTok script, YouTube description, Instagram caption, LinkedIn post, GMB post, Facebook post, newsletter copy, blog post, email draft
- Before any Engagement Queue reply goes out
- Before any ad creative
- On any AI-generated content that mentions Taylor or EG Realty

## Architecture

- **Script:** `~/.hermes/scripts/voice-check.py`
- **Rubric:** `~/claude-social-media-manager/data/voice-rubric.json` (editable; reloaded per run)
- **Exemplars:** `~/claude-social-media-manager/data/hook-bank.json` (auto-loaded, filtered by platform)
- **Model:** `claude-haiku-4-5-20251001` (fast, cheap, accurate)
- **Threshold:** 85+ passes by default. `--strict` raises to 90+.

## Commands

```bash
# Pipe draft via stdin (most common)
echo "draft" | python3 ~/.hermes/scripts/voice-check.py --platform tiktok --audience buyer

# Pass draft as argument
python3 ~/.hermes/scripts/voice-check.py --draft "text" --platform youtube_living

# Strict mode (require >=90)
cat script.txt | python3 ~/.hermes/scripts/voice-check.py --strict --platform instagram

# Raw JSON (for piping into other skills)
cat draft.md | python3 ~/.hermes/scripts/voice-check.py --json --platform temple_insider

# Just the rewrite (auto-replace workflows)
cat bad-draft.txt | python3 ~/.hermes/scripts/voice-check.py --rewrite-only --platform tiktok
```

## Platform values

`tiktok, youtube_living, youtube_investing, temple_insider, investor_brief, instagram, linkedin, gmb, facebook, email`

## Audience values

`buyer, investor, military, bsw, seller, relocator`

## What it catches (validated)

Tested against a banned-phrase-loaded draft, scored 12/100 FAIL with:
- All 8 banned phrases flagged (dream home, charming, premier, immaculate, boasts, stunning views, luxurious touches, don't miss, opportunity of a lifetime)
- Wrong-audience violation (TikTok=buyers only, draft pivoted to investors)
- No-creative-element flag
- Generic tone detection
- Mixed-audience confusion
- Returned on-brand rewrite (MLS data anchor, BSW/BAH hook, native-TikTok cue)

Good drafts pass 85+ with `creative_element` named explicitly.

## Exit codes

- `0` = passes threshold
- `1` = fails (use in shell: `|| echo "draft rejected"`)
- `2` = error (missing key, API failure, malformed response)

## Integration with other skills

- **Community Memory → draft reply → Voice Guardian** — score every reply before it ships
- **tiktok-script, yt-video, newsletter, gmb-post** — pipe outputs through voice-check before Taylor review
- **Engagement Queue** — batch-score drafts before Telegram approval push
- **Two-pass system (governance)** — voice-guardian IS pass #2

Example chain:
```bash
python3 generate-tiktok-hook.py --topic "BSW area" \
  | python3 ~/.hermes/scripts/voice-check.py --strict --platform tiktok --audience buyer --rewrite-only
```

## Editing the rubric

Edit `~/claude-social-media-manager/data/voice-rubric.json` freely; script reloads each run. Sections:
- `voice` — core rules
- `banned_phrases` — add/remove
- `platform_rules` — per-platform audience/pillar constraints
- `broker_rule`, `ads_rule`, `bsw_rule` — enforceables
- `numerical` — MLS/Node math/citation rules
- `first_of_month_rule`, `heagerty_rule` — calendar + client constraints

## Cost estimate

Claude Haiku 4.5: ~$0.003/score (1-2K input + 500 output). 100 scores/day ≈ $0.30/day, $9/month. Negligible vs the damage one off-voice piece does.

## Rollback

`rm ~/.hermes/scripts/voice-check.py ~/claude-social-media-manager/data/voice-rubric.json` — removes the guardian. Publishing falls back to human-only review (current state before this build).
