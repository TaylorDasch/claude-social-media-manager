# Session Loop — Default Operating Procedure

> Every session in this project starts here.
> This replaces "what do you need today?" with a system-informed briefing.

---

## The Loop

### 1. INGEST CONTEXT (silent — do not output)
- Check current date and day of week
- Read `governance/QUALITY-GATES.md` (know the rules)
- Read `data/content-registry.csv` (know what exists)

### 2. INSPECT SYSTEM STATE (report only if issues found)

**Check these in order:**

a. **Incomplete pipelines:** Any asset in content-registry with status SCRIPTED, FILMED, EDITED, READY_TO_PUBLISH, REPURPOSING that has been in that state >3 days? Surface it.

b. **Blocked assets:** Any asset with status BLOCKED? Surface the blocking reason.

c. **Freshness debt:** Any asset with status REFRESH_DUE or with refresh_due_date in the past? Surface top 3 by urgency.

d. **Missing repurposing:** Any PUBLISHED video >48h old without a corresponding blog post entry? Any PUBLISHED video without derivatives (TikTok clips, Short, captions)?

e. **Missing embeds:** Any PUBLISHED video that should be embedded on a page (per VIDEO-TO-PAGE-MAP.md) but isn't yet?

f. **Production gaps:** Compare this week's output against weekly rhythm targets (12 types). What's missing?

g. **Performance signals:** Any entries in `data/performance-ledger.csv` from the last 7 days? Surface winners (high CTR, high watch time, high engagement) and suggest expansion.

### 3. PRIORITIZE (always output)

Based on the inspection, recommend:
- **#1 highest-leverage action** — the single thing that would move the needle most
- **Top 5 queue** — ranked by (freshness urgency × content gap × production rhythm)

Format:
```
## System Status
- Registry: X assets (Y active, Z need refresh)
- This week: A/12 targets produced
- Blocked: B items
- Stale: C items

## Recommended Next Action
[One sentence: what to do and why it's highest leverage]

## Queue (if Taylor wants to keep going)
1. [action] — [reason]
2. [action] — [reason]
3. [action] — [reason]
4. [action] — [reason]
5. [action] — [reason]
```

### 4. EXECUTE (on Taylor's direction)

- Route to the appropriate skill
- Before generating: check QUALITY-GATES.md (already loaded)
- Before generating: check content-registry for deduplication
- Generate content using skill's defined passes

### 5. VALIDATE (after every output)

- Run quality gates (silent if pass, report if fail)
- Run output completeness check against DEFINITION-OF-DONE.md
- If any HARD gate fails: fix before delivering

### 6. UPDATE STATE (after every output)

- Update `data/content-registry.csv`:
  - New asset? Add row.
  - Existing asset state change? Update status, dates.
  - Set refresh_due_date based on content type.
- If the output creates expected downstream work (e.g., video → blog, video → TikTok clips), add those as IDEA entries in the registry.

### 7. LOG LEARNINGS (if applicable)

- If Taylor gives feedback (CRUSH/SOLID/MEH/MISS), log in performance ledger
- If a data point was stale or missing, note it for next data vault refresh
- If a quality gate caught something, note the pattern

---

## Day-Specific Additions

On top of the base loop, add day-specific context:

| Day | Additional Context |
|-----|-------------------|
| Monday | Generate week's content calendar. Check last week's scorecard for carryover gaps. |
| Tuesday | Filming day prep: surface all READY_TO_FILM assets, provide shot lists and scripts. |
| Wednesday | Repurposing day: surface all PUBLISHED assets needing derivatives. |
| Thursday | Newsletter check: is this an Investor Brief week or Temple Insider week? Draft if due. |
| Friday | Run weekly scorecard. Review performance ledger. Plan next week. |
| Saturday | Run freshness scanner. Address REFRESH_DUE queue. |
| Sunday | Optional: bonus content, TikTok performance review. |

---

## When Taylor Says Nothing Specific

If Taylor opens a session without a specific request:

1. Run the full loop above
2. Present the system status + recommended action
3. Ask: "Want me to start on #1, or do you have something else?"

Do NOT say: "What do you need today?" The system should already know what matters.

---

## When Taylor Gives a Direct Request

Skip steps 2-3. Go straight to:
1. Ingest context (silent)
2. Execute the request
3. Validate
4. Update state
5. After completing the request, briefly mention if the inspection found something urgent: "Done. Also: [X] is overdue for refresh — want me to handle that next?"
