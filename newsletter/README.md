# Newsletter Desk

The Newsletter Desk makes Codex the working surface and keeps Beehiiv in the background as the delivery layer.

Taylor does not need to design a newsletter in Beehiiv. Taylor and Codex talk through each issue here, Codex builds a branded local preview, Taylor reviews it, and the approved issue is staged for Beehiiv delivery. Beehiiv remains responsible for unsubscribe links, bounce handling, suppression state, and analytics.

## Products and cadence

| Timing | Product | Audience | Publication |
|---|---|---|---|
| First Thursday monthly | Central Texas Market Update | Past clients, relocators, buyer leads, homeowners, and permissioned sphere contacts | Temple TX Insider |
| Second Thursday monthly | Investor Deal Analysis | Permissioned investors | Temple TX Investor Brief |
| Fourth Thursday monthly | Investor Deal Analysis | Permissioned investors | Temple TX Investor Brief |

The market update contains the honest market pulse, home of the month, best current deal, a quick tip, and one rotating feature. Each investor edition ranks the strongest multifamily, single-family rental, and specialty opportunity under stated assumptions. Never mix the two lists.

See `newsletter/NEWSLETTER-PROGRAM.md` for the module rotations, underwriting requirements, launch calendar, and evidence rules.

## Temple Insider approved design

- `newsletter/design/APPROVED-DESIGN.md` records the selected design and the production elements that must be preserved.
- `newsletter/design/temple-insider-market-update-v1-premium.html` is the approved working design for future Temple TX Insider market updates.
- `newsletter/design/temple-insider-design-options.html` is the comparison page for the design studies.
- `newsletter/design/temple-insider-market-update-v1.html` is the original high-contrast Market Field Report reference.
- `newsletter/design/temple-insider-market-report-upgrade-comparison.html` compares the original Market Field Report with the selected premium upgrade.
- `newsletter/design/temple-insider-market-update-v2-editorial.html` is the warm Editorial Elegance direction.
- `newsletter/design/temple-insider-market-update-v3-newspaper.html` is the sharper Modern Newspaper direction.
- `newsletter/design/temple-insider-monthly-input-sheet.md` separates MLS inputs, Taylor's field experience, and Codex verification work.

The colored source labels are internal planning aids. Remove them when the real issue is built for Beehiiv. Design approval does not authorize staging, publishing, or sending.

## Investor Brief approved design

- `newsletter/design/APPROVED-INVESTOR-DESIGN.md` records the selected investor design and the production elements that must be preserved.
- `newsletter/design/temple-investor-brief-v1-desk-tech.html` is the approved working design for future Temple TX Investor Brief editions: a dark underwriting desk with premium-tech hierarchy, tabular money figures, explicit assumptions, equal-weight risk treatment, and three asset-class deal cards.

Taylor approved this design on July 19, 2026. It remains separate from the Temple TX Insider market-update design and audience. Design approval does not authorize staging, publishing, or sending.

## Production workflow

1. **Monday — talk it out here.** Codex checks the calendar and last Beehiiv send, confirms which product is due, and proposes the issue angle from current videos, pages, and MLS-backed facts.
2. **Tuesday — draft.** Taylor reacts in plain language. Codex writes the issue and creates the preview. No Beehiiv design work is needed.
3. **Wednesday — approve.** Taylor reviews subject, preview text, body, links, and the recipient count. Approval to stage is separate from approval to send.
4. **Thursday — delivery.** The approved issue goes through Beehiiv so unsubscribes, bounces, and analytics work correctly. The delivery record is verified after the send.
5. **Friday — outcome check.** Codex logs replies, clicks, and deal conversations. A serious reply matters more than a vanity open rate.

## Contact list

Private contacts belong at:

`newsletter/private/contacts.csv`

That folder is gitignored because it contains personal information. Start from `newsletter/contacts.template.csv`.

To prepare a private review list from a Follow Up Boss export:

```bash
python3 scripts/newsletter_desk.py fub prepare \
  /Users/taylordasch_1/Downloads/all-people-2026-06-16.csv
```

This excludes missing emails, duplicate emails, bounced/DNC/no-outreach records, cold records without a permission signal, and seller-only contacts. Proposed buyers and investors remain `pending_review`; classification is not treated as newsletter consent.

Compare the private candidates against existing Beehiiv subscriptions without importing anything:

```bash
python3 scripts/newsletter_desk.py contacts reconcile \
  newsletter/private/fub-newsletter-candidates.csv --live
```

The reconciled file marks existing active, inactive, and invalid subscriptions. Inactive or invalid Beehiiv records are held out and never reactivated.

Create conservative, audience-specific review lists from the reconciled candidates:

```bash
python3 scripts/newsletter_desk.py fub filter \
  newsletter/private/fub-newsletter-candidates-reconciled.csv \
  /Users/taylordasch_1/Downloads/all-people-2026-06-16.csv \
  --recent-since 2025-07-18
```

This writes three private files under `newsletter/private/fub-filtered/`:

- `temple-insider-review.csv` — relationship, contacted-lead, and recent-inbound candidates for the monthly market update
- `investor-brief-review.csv` — the same review tiers for the investor analysis
- `held-out.csv` — existing active/inactive records, cold-source contacts, and older uncontacted leads

Relationship records rank first, then contacted leads, then recent inbound leads. Filtering never changes `pending_review` to `subscribed`; Taylor still approves the relationship/permission basis before a contact enters an importable file. A past client with a strong investor signal remains in one audience unless a separate second-audience permission record is confirmed.

Apply a Taylor-reviewed row decision file recoverably:

```bash
python3 scripts/newsletter_desk.py fub curate \
  newsletter/private/fub-filtered/temple-insider-review.csv \
  newsletter/private/fub-filtered/curation-2026-07-18.json \
  --held-out newsletter/private/fub-filtered/held-out.csv
```

The command dry-runs by default and verifies both the spreadsheet row and expected FUB ID so shifted row numbers cannot remove the wrong person. Applying requires `--apply --confirm APPLY_CONTACT_CURATION`. Before changing the private review file, it writes a full backup and a removal archive. Removed contacts move to `held-out.csv`; they are not deleted from the original FUB export or from the suppression history.

Required rules:

- Every active contact has one audience: `temple-insider` or `investor-brief`.
- Every active contact has a consent source and consent date.
- `pending_review` candidates are never importable until Taylor confirms the audience and permission record.
- `unsubscribed`, `bounced`, and `complained` contacts remain in the local suppression record but are never imported.
- The sync path sets `reactivate_existing=false`; an old unsubscribe is never silently overridden.
- A person may be on both audiences only when there is a separate opt-in record for each.

Validate without making any external change:

```bash
python3 scripts/newsletter_desk.py contacts validate newsletter/private/contacts.csv
```

Prepare a dry-run import for one audience:

```bash
python3 scripts/newsletter_desk.py contacts sync newsletter/private/contacts.csv \
  --audience temple-insider
```

Live import is a separate, explicit action after Taylor reviews the report. The tool never reactivates unsubscribed contacts.

## Issue build

Start from the template for the due product:

- `newsletter/issues/market-update.template.md`
- `newsletter/issues/investor-analysis.template.md`

Copy the template into the correct date, replace every placeholder, fill the frontmatter and body, then run:

```bash
python3 scripts/newsletter_desk.py issue build newsletter/issues/market-update.template.md
```

The default output is:

`output/YYYY-WXX/newsletter/<audience>-<subject>/`

It contains:

- `preview.html` — browser review surface
- `email.html` — email-safe HTML for Beehiiv staging
- `plain.txt` — plain-text fallback
- `manifest.json` — audience, subject, date, sources, and `NOT_SENT` state

The builder blocks missing entity information, missing source notes, missing page links, bad subject/preview lengths, banned language, unresolved `{{PLACEHOLDERS}}`, and an issue type paired with the wrong audience.

## Delivery boundary

Do not use Gmail BCC as the mass-newsletter engine. It has no reliable per-recipient unsubscribe/suppression workflow and creates avoidable deliverability risk.

Beehiiv's Create Post API is currently Enterprise-only. On the current account, Codex can still build and preview everything locally, import consented contacts through the supported subscription API, and stage the approved issue through the authenticated Beehiiv web editor. The final send remains a separate approval step under the repository's no-auto-send rule.

## Rollback

This system does not alter existing Beehiiv posts or contacts in dry-run mode. Before commit, place all Newsletter Desk changes into a recoverable stash with:

```bash
git stash push --include-untracked -m "rollback newsletter desk" -- \
  .gitignore skills/newsletter/SKILL.md newsletter scripts/newsletter_desk.py tests/test_newsletter_desk.py
```

The ignored private contact files are not included in that stash and remain untouched.
