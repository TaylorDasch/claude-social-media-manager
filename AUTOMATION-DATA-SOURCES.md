# Automation Data Sources

This branch is the current data bridge for content reporting. Only specifically reviewed bridge files are updated; the rest of the branch is historical repository context, not current operational truth.

## Sources and coverage

- `data/content-registry.csv` comes from the active content workspace on its canonical host. Its daily bridge first reconciles recent public uploads for the primary YouTube channel using immutable video IDs and publication timestamps. Ambiguous existing prep matches are held for reconciliation rather than guessed.
- `data/performance-ledger.csv` is a public projection of the separate active clean-main worktree ledger. Observation keys are retained; only explicitly sourced public YouTube view, comment and labeled like counters cross this bridge. Owner-only watch time, retention, engaged views, thumbnail impressions/CTR, business metrics and arbitrary notes are withheld. Blank fields marked withheld are not zero and do not mean the local connector is disconnected. Private metrics require a separately accessible private report or authenticated source. These rows are measurement observations, not publication receipts. Some content IDs collide across old registry copies; join YouTube records by verified platform/video identity, not a prep ID alone.
- The old cloud Content Registry Sync routine used a different repository and is paused. Its bootstrapped CSVs/PRs are not this source of truth.
- This bridge does not establish complete TikTok, GBP, Facebook/Instagram, community, newsletter, blog, private YouTube Analytics or CRM coverage. Use current connectors and dated receipts for those sections. Missing coverage means UNKNOWN/PARTIAL, not zero output or a missed target.
- Do not derive publishes from channel video-count differences. Enumerate unique platform release IDs and convert timestamps to America/Chicago for production counts. Preserve the API timezone and processed-through date separately for analytics.

## Freshness and current intent

Record retrieval/transfer time, publication/measurement cutoff and coverage separately. The newest draft row and Git checkout timestamps do not verify the rest of the registry. A successful transfer only proves those bytes were transferred. If data is missing, old, inconsistent or incomplete, label the affected claim accordingly.

Read row notes/status before making recommendations. Filmed, published, archived and explicitly retired milestones must not reappear as filming work. Approval, scheduling and release are separate facts. An absent parent pointer does not prove an absent derivative: inspect the actual published/scheduled inventory before recommending another Short. A bookkeeping correction must never trigger posting.

A past refresh due date triggers a review, not an automatic conclusion that a live page is stale. Historical videos and newsletter issues may remain dated archives. Check current page text, the exact embed and underlying dated evidence. Publication-identity verification is not fact-checking of the video's claims. Never advance a public verification date merely because an automated check ran.

## Reporting accuracy

- Compare compatible YouTube metrics from the same date range, dimensions, filters and denominators. Public lifetime starts, engaged views, watch time and AVD cannot be mixed. Label missing private data UNKNOWN and incompatible scopes NOT COMPARABLE. Respect the existing public-view measurement break before drawing lift conclusions.
- Subscriber snapshot changes are not verified weekly subscribers gained minus lost. Small samples do not establish a retention winner.
- A weekly-delivered transaction summary can contain cumulative totals. Require actual closing/appointment dates before attributing them to the reporting week. AFRAME totals are snapshots unless their period is explicit; they are not a live CRM query.
- Do not use historical CRM configuration, obsolete integration sources or hard-coded deal lists. Current dated evidence and explicit completion corrections take precedence.

## Publication boundary

This repository is public. Do not copy email bodies, client records, credentials, private analytics exports, raw automation logs, unpublished operational reports or local evidence bundles into it. New bridge changes must be reviewed for public suitability; reporting output stays in its private run/draft destination. The existing daily sync stages only its two allowlisted CSVs, never an entire working tree or report folder.
