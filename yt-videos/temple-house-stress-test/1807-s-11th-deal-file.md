# PILOT PROPERTY — 1807 S 11th St, Temple, TX 76504 (LOCKED 2026-07-28)

Buyer client: **Nelson [confirm full name + best contact from deal file]** · Taylor = buyer's agent (CDA: "BUYER AGENT Signed CDA | 1807 S. 11th St." — Jun 2) · **Closed June 9, 2026** (EG/trfit "Transaction closed" notice) · Listing agent: Derek Smith, Deal Smith Realty · Title: First Community Title (Betty Mena) · TC: Boykin Group · Zip note: CDA says 76504, TC notice said 76502 — resolve from the contract.

## The negotiation story (documented, from Taylor's own sent mail)
- **May 18, 3:30 PM — the ask** (email to Derek Smith): three inspection findings converted to a **$5,000 seller credit in lieu of repairs** —
  1. Electrical subpanel: multiple neutrals under one screw — separate onto individual lugs by a licensed electrician
  2. Crawlspace: no insulation observed under the floor — install
  3. Attic: insulation compressed, below standard — upgrade to ≥ R-30
- **May 18, 5:54 PM — the counter** (Derek): seller "literally cannot afford" further discount; will handle the electrical; hesitant on insulation; Derek offered to handle insulation himself to save the deal.
- **Final outcome: PULL FROM FILE** — the executed amendment / final CD shows what actually settled (credit amount vs. repairs performed vs. Derek's out-of-pocket). This is THE RECEIPTS beat and the open-loop decider: if one finding is isolated in the amendment → "moved the price" loop; if it settled as a bundle → "biggest one" loop.

## Where the documents already are
| Doc | Location | Status |
|---|---|---|
| Inspection report (likely) | "trec (4).pdf" (2.6 MB) attached to Taylor's May 18 email to Derek (msg 19e3cc85bdeefbb3) | ✅ in inbox — verify it's the report, count findings |
| Repair ask + counter | Gmail thread "Inspection Report W Requested Repairs / Credit" (thread 19e3cc6da1907fb3) | ✅ quoted above |
| Signed CDA | Thread "BUYER AGENT Signed CDA \| 1807 S. 11th St." (Jun 2, Betty Mena/FCT + Boykin Group) | ✅ in inbox |
| Executed amendment, contract, CD, appraisal | Boykin Group TC file / Brokermint / FCT | ⬜ Taylor pulls |
| Tour-day notes/photos, option period dates | Taylor's calendar + phone | ⬜ Taylor pulls |

## Gate status
- **Gate 0 (closed buyer-side ≤9mo):** ✅ closed Jun 9 — 7 weeks.
- **Gate 1 (consent):** ⬜ THE BLOCKER — Nelson's ask + signed release (draft below).
- **Gate 2 (per-finding documents):** partial ✅ — 3 findings named with inspector language; dollar sourcing = amendment/CD/quotes (electrician invoice if seller repaired; Derek's insulation receipt if that happened — a receipt from the *listing agent* fixing insulation is a first-of-its-kind receipt beat). Any unpriced report finding → severity-only lane or `[current quote — MM/YYYY]`.
- **Gate 3 (≥4 findings, ≥3 categories):** likely ✅ — 3 named already span Electrical (Big-Ticket), and two insulation/envelope items; a 2.6MB report on an older crawlspace house will have more. Count on doc pull.
- **Gate 4 (findings moved ≥1% of price):** probable ✅ — $5K ask vs. central-Temple price point (if price ≈ $150–220K, $5K = 2.3–3.3%). CONFIRM the executed outcome ≥ ~1%.
- **Gate 5 (landmines):** ✅ resale (crawlspace-era), no builder, closed+funded. Confirm no post-close disputes. 76504: house-only rule absolute — zero neighborhood/safety/demographic commentary.
- **Gate 6 (scout):** ⬜ after release — crawlspace + subpanel + attic are permanent-visual findings (panel interior shot with flashlight = the thumbnail-grade macro); repaired items run the repaired-finding recipe with the report photos as "before."
- **OPEN QUESTION (framing + access, not eligibility):** is Nelson an owner-occupant living there, or an investor/tenant situation? Owner-occupant = clean access + on-lane. Investor-owned = episode still works (the stress test is about the HOUSE; zero rent/return talk permitted per lane rule) but access needs tenant cooperation and the CTA framing softens. Tenant-occupied filming needs the tenant's written acknowledgment too.

## ⚠️ Nelson consent — Spanish required (added 07-28)
Nelson doesn't speak English. The ask and the release happen in Spanish or they don't count as informed consent. Use `consent-kit-es.md` — call script + short text version + bilingual release. Lead with: **no camera, no name — la casa cuenta la historia.** Identity election will likely be "sin nombre / no cámara," which the format fully supports (the owner never needs to appear). Broker blesses the bilingual release once before signing.

## Consent ask — filled draft, English reference (Spanish version in consent-kit-es.md is the one to use)
> "Nelson — got a minute? I'm starting a YouTube series that shows buyers what I check before they offer on a house, and I want your place on 11th to be the first episode: the flags I caught on our walkthrough, what the inspector confirmed, and how we used them at the table. Full honesty about what that means: the video is permanent and public, the repair story uses the real dollar figures, and the math points at what you paid — we can round the price story, but we can't hide it. If you ever sell, a future buyer's agent could find it — and it'll also show everything was inspected, negotiated, and handled with receipts, which cuts both ways. You approve anything that identifies you, you see the full cut before it publishes, you can pull the plug any time before it goes up, and if you ever list the house I'll unlist the episode while it's on the market. The analysis itself stays mine. Want me to send over the one-page release?"

## Prep-week sequence (from the field card, now property-specific)
1. Confirm Nelson's occupancy + warmth → make the ask → send release (broker skims it once first) → signed, price tier elected (Tier E vs. Rounded Band — run `stress-test-calc.py` zone check once price is in hand).
2. Pull: executed amendment, contract + option dates, CD, appraisal (if financed), electrician invoice / insulation receipt. Open "trec (4).pdf" — count findings, mark S1/S2/S3, note which are photographed in the report.
3. Inspector license check: read the inspection agreement; ask the inspector for excerpt permission (offer the credit).
4. Scout at the house (30–45 min): filmability map — panel, crawlspace access, attic hatch, plus every other report finding still visible. Tier-B zone-preservation check.
5. Run the file through `stress-test-calc.py` → real TRE, real %, computed verdict. Fill the fact & source log (property-intake-checklist.md). Then packaging slots: hooks/title/thumbnail update together (slot coherence).
6. Broker call: date + footage ownership + 23.976p + pre-review framing ("nothing in this series touches a city or public figure — you see every cut").
7. Solo pre-validation hour at Taylor's own house. Then book the videographer.
