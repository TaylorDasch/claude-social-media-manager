# Asset Factory

The factory turns one source into a draft distribution packet without mixing lanes or inventing facts.

## Source Intake

Every source asset starts with:

- Source type: page, video, listing, MLS pull, newsletter, client question, or market brief.
- Source path or URL.
- Primary audience lane.
- Business outcome.
- Proof needed.
- Lead path.
- Approval gate.

## Derivative Map

| Source | Required drafts | Optional drafts | Blocked paths |
| --- | --- | --- | --- |
| SEO page | GBP, LinkedIn or community, newsletter block, Short idea | YouTube long-form brief, email draft | TikTok unless there is a native property tour source. |
| YouTube long-form | Description, Short, blog outline, LinkedIn/GBP/newsletter/community | BP post, FUB note | TikTok clips. |
| Listing/property | TikTok tour prep, Reel prep, photo/cover notes, Facebook/IG caption | GBP listing spotlight | Investor framing unless Taylor asks and proof exists. |
| MLS market pull | Market-read post, newsletter block, YouTube outline, GBP | LinkedIn carousel | Raw private MLS details. |
| Client question | Community post, Short, FAQ/page update | Email draft | Unsupported legal, tax, lending claims. |

## File Manifest

For each packet, save under:

```text
output/YYYY-WXX/distribution/[slug]/
```

Minimum files:

- `source-brief.md`
- `platform-drafts.md`
- `lead-path.md`
- `proof-notes.md`
- `quality-check.md`

When the packet is page-led, add:

- `seo-geo-aeo-amplification.md`
- `internal-link-opportunities.md`

When the packet is video-led, add:

- `shorts-plan.md`
- `description-cta.md`
- `page-bridge.md`

When the packet is listing-led, add:

- `tiktok-tour-prep.md`
- `reel-prep.md`
- `photo-shot-list.md`

## Quality Checklist

Before a packet is considered ready for Taylor review:

- Source and audience lane are named.
- Registry/dedupe check is recorded.
- Every number has source and date.
- CTA matches persona and platform.
- UTM/source note exists.
- FUB/source note exists where useful.
- GBP links to a specific page, not the homepage.
- TikTok is native buyer/relocator property-tour prep only.
- Draft-only approval gate is explicit.

## Output Naming

Slug format:

```text
YYYY-MM-DD-[source-topic]-[lane]
```

Examples:

- `2026-05-22-data-center-impact-relocator`
- `2026-05-22-market-report-investor`
- `2026-05-24-bsw-relocation-medical`

## No-Waste Rule

If a source cannot produce at least three strong derivatives, it stays as a single draft. Do not force every platform.
