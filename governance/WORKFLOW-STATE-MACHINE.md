# Workflow State Machine — Content Lifecycle

> Every content asset moves through defined states.
> No asset should exist without a state.
> State transitions are logged in `data/content-registry.csv`.

---

## States

### IDEA
- **Entry:** Taylor mentions a topic, system identifies a gap, or next-best-action suggests it
- **Exit:** Research started OR explicitly killed
- **Allowed next:** RESEARCHING, ARCHIVED
- **Auto-action:** Add row to content-registry.csv with status=IDEA
- **Blocking:** None

### RESEARCHING
- **Entry:** Research has begun (data pull, competitor check, angle selection)
- **Exit:** Research complete, angle locked, data confirmed
- **Allowed next:** READY_TO_SCRIPT, BLOCKED, ARCHIVED
- **Auto-action:** None
- **Blocking:** Missing data source, conflicting numbers, no clear angle

### READY_TO_SCRIPT
- **Entry:** Research done, angle selected, data verified
- **Exit:** Script/outline/draft exists
- **Allowed next:** SCRIPTED, BLOCKED
- **Auto-action:** Flag if in this state >7 days
- **Blocking:** Missing data, unclear persona target

### SCRIPTED
- **Entry:** Draft/script/outline written and passed quality gates
- **Exit:** Ready for filming (video) or ready for publishing (text)
- **Allowed next:** READY_TO_FILM (video), READY_TO_PUBLISH (text), BLOCKED
- **Auto-action:** For video: add to filming day queue. For text: add to publish queue.
- **Blocking:** Quality gate failure, missing approval

### READY_TO_FILM
- **Entry:** Script approved, shot list exists, filming day identified
- **Exit:** Filmed
- **Allowed next:** FILMED, BLOCKED
- **Auto-action:** Include in next Tuesday/Friday filming day prep
- **Blocking:** Weather, location access, equipment issue

### FILMED
- **Entry:** Raw footage captured
- **Exit:** Edit complete, ready for upload
- **Allowed next:** EDITED, BLOCKED
- **Auto-action:** Flag if in this state >3 days
- **Blocking:** Missing B-roll, audio issues

### EDITED
- **Entry:** Final edit complete (CapCut), captions added, thumbnail created
- **Exit:** Uploaded to platform
- **Allowed next:** PUBLISHED, BLOCKED
- **Auto-action:** Trigger /produce pipeline prep
- **Blocking:** Missing thumbnail, missing description

### READY_TO_PUBLISH
- **Entry:** Text content (blog, newsletter, page) passed quality gates
- **Exit:** Published to platform
- **Allowed next:** PUBLISHED, BLOCKED
- **Auto-action:** None
- **Blocking:** Quality gate failure, missing schema

### PUBLISHED
- **Entry:** Live on platform (YouTube, TikTok, blog, newsletter, GMB)
- **Exit:** Repurposing started OR 48h elapsed (auto-flag for repurpose)
- **Allowed next:** REPURPOSING, REFRESH_DUE
- **Auto-action:** 
  - Create expected downstream assets checklist
  - Set refresh_due_date (90 days for pages, 180 days for evergreen, 30 days for market data)
  - If video: flag for /transcript-to-blog at 48h
  - Update content-registry.csv with publish_date and platform
- **Blocking:** None

### REPURPOSING
- **Entry:** /repurpose or /produce started generating derivative assets
- **Exit:** All expected derivatives exist
- **Allowed next:** REPURPOSED, BLOCKED
- **Auto-action:** Check derivative manifest against actual files
- **Blocking:** Missing source transcript, missing approval

### REPURPOSED
- **Entry:** All planned derivative assets created
- **Exit:** Embeds placed, schema updated, internal links added
- **Allowed next:** EMBEDDED, REFRESH_DUE
- **Auto-action:** Check for missing page embeds (VIDEO-TO-PAGE-MAP.md)
- **Blocking:** None

### EMBEDDED
- **Entry:** Video embedded on target page, schema includes VideoObject, internal links point to it
- **Exit:** Periodic freshness check
- **Allowed next:** SCHEMA_COMPLETE, REFRESH_DUE
- **Auto-action:** Verify embed + schema via freshness scanner
- **Blocking:** None

### SCHEMA_COMPLETE
- **Entry:** All applicable schema types added and validated
- **Exit:** Content is fully deployed and integrated
- **Allowed next:** REFRESH_DUE, ARCHIVED
- **Auto-action:** Set next freshness check date
- **Blocking:** None

### REFRESH_DUE
- **Entry:** Content age exceeds freshness threshold OR data it contains is stale
- **Exit:** Content refreshed with current data
- **Allowed next:** PUBLISHED (re-publish), ARCHIVED
- **Auto-action:** Add to freshness fix queue, include in next session's priority list
- **Blocking:** Missing current data

### BLOCKED
- **Entry:** Any state where a required input is missing
- **Exit:** Blocking condition resolved
- **Allowed next:** (return to previous state)
- **Auto-action:** Log blocking reason, include in morning briefing
- **Required fields:** blocked_reason, blocked_date, what_is_needed
- **Blocking:** The blocking condition itself

### ARCHIVED
- **Entry:** Content is no longer relevant, superseded, or explicitly killed
- **Exit:** None (terminal state)
- **Allowed next:** IDEA (if revived with new angle)
- **Auto-action:** Remove from active queues
- **Blocking:** None

---

## State Transition Diagram

```
IDEA → RESEARCHING → READY_TO_SCRIPT → SCRIPTED
                                            ↓
                              ┌──────────────┴──────────────┐
                              ↓                              ↓
                        READY_TO_FILM                  READY_TO_PUBLISH
                              ↓                              ↓
                           FILMED                        PUBLISHED
                              ↓                              ↓
                           EDITED                       REPURPOSING
                              ↓                              ↓
                         PUBLISHED ──────────────→    REPURPOSED
                              ↓                              ↓
                         REPURPOSING                    EMBEDDED
                              ↓                              ↓
                         REPURPOSED                 SCHEMA_COMPLETE
                              ↓                              ↓
                          EMBEDDED                    REFRESH_DUE
                              ↓                              ↓
                      SCHEMA_COMPLETE               PUBLISHED (loop)
                              ↓                         or ARCHIVED
                         REFRESH_DUE
                              ↓
                    PUBLISHED or ARCHIVED

Any state → BLOCKED (with return path)
Any state → ARCHIVED (terminal)
```

---

## Auto-Generated Actions by State Transition

| Transition | Auto-Action |
|-----------|-------------|
| → PUBLISHED (video) | Create /produce checklist: YT desc, 3 TikToks, Short, blog outline, captions, newsletter, GMB, community post, schema, pinned comment |
| → PUBLISHED (video, +48h) | Flag for /transcript-to-blog |
| → PUBLISHED (blog) | Check for matching video in VIDEO-TO-PAGE-MAP.md, verify schema |
| → PUBLISHED (newsletter) | Log issue number, set next issue reminder |
| → REPURPOSED | Verify all derivative assets exist per manifest |
| → EMBEDDED | Verify VideoObject schema on target page |
| → REFRESH_DUE | Add to freshness queue, include in session priority |
| → BLOCKED | Log reason, surface in morning briefing, include in session priority |

---

## Staleness Rules (Auto-transition to REFRESH_DUE)

| Content Type | Staleness Threshold |
|-------------|-------------------|
| Neighborhood page | 90 days |
| Market data page | 60 days |
| Blog post (evergreen) | 180 days |
| Blog post (market data) | 90 days |
| Deal of the Week | Never (archival) |
| Newsletter issue | Never (archival) |
| Video | Never (but page embed may go stale) |
| GMB post | Never (daily, ephemeral) |
| Schema markup | When dateModified > 90 days old |
