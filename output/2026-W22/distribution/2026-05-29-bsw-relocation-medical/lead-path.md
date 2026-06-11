# Lead Path — BSW Medical Relocation Cluster

Status: DRAFT. No CRM write, send, or automation goes live without Taylor's explicit approval. No auto-FUB push.

---

## Primary Offer

- Lead magnet: **BSW Temple Relocation Guide (PDF)** — physician-loan overview, Match-Day-to-closing timeline, neighborhoods by commute to BSW.
- Hosted: `https://assets.agentfire3.com/uploads/sites/2128/2026/04/BSW-Temple-Relocation-Guide.pdf`
- Primary DM/reply keywords: **MATCHED · BSW · DOCTOR · RESIDENT**
- Secondary keyword: **COMMUTE** → points to the live commute page `https://templetxhomes.net/neighborhoods-near-bsw-by-commute/`. Note: a dedicated downloadable "BSW Commute Map" PDF is **not confirmed built** (LEAD-MAGNET-MATRIX lists status unknown) — COMMUTE resolves to the page, not a separate PDF. Flag as a missing asset to build.
- Business goal: convert BSW relocation search demand into named buyer/relocator conversations during the live close-and-move window (orientation June 22).

## Keyword → Asset → Page map

| Keyword | Triggers on | Send | Target page |
| --- | --- | --- | --- |
| MATCHED | LinkedIn 1, Short 1, Newsletter | Relocation Guide PDF + Match Day timeline link | /match-day-2026-bsw-housing-timeline/ |
| BSW | Short 2, IG Reel | Relocation Guide PDF + commute link | /baylor-scott-white-relocation/ (hub) |
| DOCTOR / RESIDENT | reserved replies (inbound) | Relocation Guide PDF | /match-day-2026-bsw-housing-timeline/ |
| COMMUTE | Short 2, IG Reel (secondary) | Commute-by-role page link | /neighborhoods-near-bsw-by-commute/ |

## UTM Links (by platform)

```text
# Match Day page
https://templetxhomes.net/match-day-2026-bsw-housing-timeline/?utm_source=gbp&utm_medium=local&utm_campaign=2026-05-bsw-relocation
https://templetxhomes.net/match-day-2026-bsw-housing-timeline/?utm_source=linkedin&utm_medium=social&utm_campaign=2026-05-bsw-relocation
https://templetxhomes.net/match-day-2026-bsw-housing-timeline/?utm_source=youtube&utm_medium=short&utm_campaign=2026-05-bsw-relocation
https://templetxhomes.net/match-day-2026-bsw-housing-timeline/?utm_source=newsletter&utm_medium=email&utm_campaign=2026-05-bsw-relocation

# Commute page
https://templetxhomes.net/neighborhoods-near-bsw-by-commute/?utm_source=gbp&utm_medium=local&utm_campaign=2026-05-bsw-relocation
https://templetxhomes.net/neighborhoods-near-bsw-by-commute/?utm_source=youtube&utm_medium=short&utm_campaign=2026-05-bsw-relocation
https://templetxhomes.net/neighborhoods-near-bsw-by-commute/?utm_source=instagram&utm_medium=social&utm_campaign=2026-05-bsw-relocation

# Relocation hub (BSW keyword default)
https://templetxhomes.net/baylor-scott-white-relocation/?utm_source=linkedin&utm_medium=social&utm_campaign=2026-05-bsw-relocation
```

## FUB Source Note (spec — NO write without approval)

When a lead converts from this cluster, log (manually, on approval) a note in this exact shape:

```text
Source: Social OS | Lane: BSW medical relocator | Campaign: 2026-05-bsw-relocation | Platform: [gbp|linkedin|youtube|instagram|newsletter] | Keyword: [MATCHED|BSW|DOCTOR|RESIDENT|COMMUTE] | Page: [target URL] | Captured: [date]
```

Suggested FUB tags (apply on approval): `BSW`, `BSW_Relocator`, plus role if known (`BSW_Resident`, `BSW_Nurse`, `BSW_Attending`, `BSW_CRNA`). These mirror the commute-page form's role tags so on-site and social leads land in one segment. No auto-enrollment in an action plan without Taylor's go.

## DM / Reply Scripts (persona-fit, draft)

**Opening reply (any keyword):**
> Thanks for reaching out. Quick context so I send the right thing: are you a resident/fellow, an attending, or a nurse/tech — and roughly when's your start date? I'll send the relocation guide plus a shortlist that fits your commute and shift. (I'm an independent agent — not affiliated with or endorsed by BSW.)

**Resident / fellow (MATCHED / RESIDENT):**
> Here's the 94-day Match-Day-to-keys timeline: [Match Day UTM link]. Two honest notes: on a 1–2 year prelim, renting usually beats buying once you count selling costs; on a 3+ year track the math often flips. And book movers early — May/June is the squeeze. Want me to run your specific rent-vs-buy number?

**Attending / CRNA (DOCTOR / BSW):**
> Sending the relocation guide: [hub UTM link]. At your stage the questions are usually school district, premium-build inventory, and separation from work. I can pull a by-role shortlist and verify ISD zoning by address before you tour. Buying or also weighing rent for year one?

**Nurse / tech / family (BSW / COMMUTE):**
> Sending the commute-by-role map: [commute UTM]. Day shift or nights? That changes which neighborhoods I'd point you to, especially around rail noise, parking time, and school-zone tradeoffs.

## Persona-fit CTA per platform (summary)

| Platform | CTA | Keyword | UTM source |
| --- | --- | --- | --- |
| GBP (Match Day) | "Call or text 254-718-4249 for a personalized timeline" | — (call) | gbp |
| GBP (Commute) | "Call or text for a 3-neighborhood shortlist for your role" | — (call) | gbp |
| LinkedIn 1 | "Comment MATCHED" + first-comment link | MATCHED | linkedin |
| YouTube Short 1 | "Comment MATCHED" + pinned link | MATCHED | youtube |
| YouTube Short 2 | "Comment BSW / COMMUTE" + pinned link | BSW / COMMUTE | youtube |
| Instagram Reel | "Comment BSW / COMMUTE + link in bio" | BSW / COMMUTE | instagram |
| Newsletter | "Reply BSW" | BSW | newsletter |

## Next Action by Persona

| Persona | Next question | Follow-up |
| --- | --- | --- |
| Incoming resident | "Residency length and start date?" | Run rent-vs-buy on their number; send timeline |
| Attending / CRNA | "School district priority and budget band?" | By-role shortlist; verify ISD by address |
| Nurse / tech (shift) | "Day shift or nights?" | Commute + night-noise screen |
| Relocating family | "School district, commute, or rent-vs-buy first?" | Route to commute map, Match Day timeline, or relocation guide |
| Out-of-area / sight-unseen | "Can you travel to tour, or need video?" | Offer video-walkthrough process; timeline |

## Attribution close-the-loop note

GBP posts drive calls (no UTM on a phone call) — to attribute, the opening reply asks "where did you find me." LinkedIn/YouTube/IG/newsletter all carry UTMs + keyword, so a converted lead can be traced to platform + asset. Review GBP "calls" and GSC page clicks weekly against new BSW conversations to read which asset is actually producing.
