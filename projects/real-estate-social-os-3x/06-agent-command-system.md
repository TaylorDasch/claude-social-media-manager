# Agent Command System

This is the role layer for running the social OS with AI help while keeping real-world actions gated.

## Roles

| Role | Job | Inputs | Output |
| --- | --- | --- | --- |
| Strategist | Pick the source asset and lane. | GSC, registry, market-monitor, current business priority. | Source brief and go/no-go. |
| Proof Analyst | Verify numbers and claims. | MLS files, source page, GSC, config, local references. | Proof notes with dates and caveats. |
| Platform Producer | Create native drafts. | Source brief, proof notes, platform template. | Drafts by platform. |
| Lead Path Integrator | Add CTA, UTM, FUB/source note, and approval status. | Lead magnet matrix and attribution rules. | Lead path packet. |
| Gatekeeper | Run quality gates and mark blockers. | Draft packet and governance docs. | Pass/block report. |
| Optimizer | Decide what to do next. | Performance, registry, source portfolio. | Queue updates and next action. |

## Default Chain

1. Strategist.
2. Proof Analyst.
3. Platform Producer.
4. Lead Path Integrator.
5. Gatekeeper.
6. Optimizer.

For fast drafts, combine Strategist + Producer, but do not skip Proof Analyst or Gatekeeper when numbers, medical, military, seller, or investor claims are involved.

## Approval Gates

The system can draft:

- Social posts.
- Captions.
- Scripts.
- GBP posts.
- Emails.
- FUB/source notes.
- Site update tasks.
- Calendar recommendations.

The system cannot do without Taylor approval:

- Post or schedule.
- Send email or text.
- Update FUB/CRM.
- Change live pages.
- Spend money.
- Make external commitments.

## Operator Prompts

Use these in order:

- `prompts/daily-operator-prompt.md`
- `prompts/distribution-packet-prompt.md`
- `prompts/campaign-council-prompt.md`
- `prompts/opus-review-prompt.md`

## Decision Rules

- If GSC shows demand and the page has weak CTR, build social that sharpens the title promise and sends traffic back to the page.
- If MLS proof is fresh but the page/video is stale, refresh the public claim before distributing.
- If the asset is investor-focused, route to YouTube, LinkedIn, BP, and Investor Brief.
- If the asset is buyer/relocator-focused, route to TikTok only when there is native property footage or listing facts.
- If the output cannot name a lead path, it is not ready.
