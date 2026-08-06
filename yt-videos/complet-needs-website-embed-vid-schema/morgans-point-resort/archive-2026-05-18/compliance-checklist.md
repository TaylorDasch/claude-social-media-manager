# Morgan's Point Resort Flagship — Compliance Checklist

## 16. COMPLIANCE RISKS + SAFE PHRASING

| # | Risk | Banned / risky phrasing | Safe alternative |
|---|---|---|---|
| 1 | Fair Housing — familial steering | "great for families", "family-friendly", "kid-friendly community" | "if your buyer profile prioritizes ISD assignment and lower-maintenance lifestyle" |
| 2 | Fair Housing — age steering | "perfect for retirees", "55+ feel" | "if you want lower-maintenance with the lake address" |
| 3 | Fair Housing — race / ethnicity / national origin steering | any neighborhood quality descriptors implying demographics | strictly use property and infrastructure facts |
| 4 | "Safe neighborhood" claim | "safe", "low-crime", "secure neighborhood" | Use only verifiable public-record stats with citation, or omit entirely |
| 5 | "Best / top agent" self-claim | "top Temple agent", "best Bell County agent", "leading lakefront expert" | "data-driven neighborhood guides at templetxhomes.net" + "I separate every MPR active and recent sold by water tier" — describe work, not status |
| 6 | USACE shoreline accuracy | "you can definitely get a dock permit" | "dock permits are regulated by the USACE Belton Lake Resource Manager's Office — verify the specific parcel before writing an offer" |
| 7 | FEMA flood-zone accuracy | "this lot is NOT in a flood zone" | "the current FEMA map at msc.fema.gov shows [zone] as of [date] — verify before close; FEMA maps update annually" |
| 8 | Septic accuracy | "the septic is fine" | "the septic permit and last-pump date should be requested in the option period; many MPR systems are 25+ years old" |
| 9 | STR / Airbnb claim | "you can Airbnb this" | "MPR requires a Specific Use Permit for short-term rentals; the community does not freely allow them — verify SUP status before writing an offer if rental income is part of your math" |
| 10 | Tier-implied price advice | "this $249K listing is overpriced" | "this $249K listing prices as if it were Tier 1, but my read of the parcel and dock-permit status is Tier 2 — that's a comp gap worth verifying" |
| 11 | Investor pivot temptation | "great rental property", "good cap rate", "buy this for the cash flow" | HARD STOP — buyer lane only. Do not mention rental yield, cap rate, or buy-and-hold |
| 12 | Trespass | filming on private property without permission | filmed exclusively at USACE Owl Creek Park (public access). All home shots are drive-by from public road or drone over public airspace |
| 13 | Drone airspace | flying over restricted USACE or FAA area | FAA Part 107 compliance — Taylor verifies pilot status + airspace before flight. If uncertain, omit drone and use stock |
| 14 | Drone over private parcels | flying over occupied residences | drive-by from public road only; drone is for lake/shoreline B-roll, not directly over residential parcels |
| 15 | MLS attribution | omitting source | every on-screen stat block includes footer: "Source: Bell County MLS pull May 14, 2026" |
| 16 | License + disclosure | omitting Texas Real Estate License # and brokerage | description disclosure block includes license #, brokerage, TREC IABS/CPN reference. **Verify all values BEFORE upload** |
| 17 | Identifying specific homes | naming address or owner on-camera | address-blur drive-bys in post. No street numbers visible. No owners' vehicles in driveway. No identifying landscaping closeups. |
| 18 | MLS data redistribution | publishing protected MLS fields | use only aggregate stats (medians, ranges) and publicly-derivable info. Do NOT publish MLS#, full address, or copyright-protected listing photos |
| 19 | Comparison-page Fair Housing | "Lake Pointe is better/worse than MPR" → demographic implication | compare by property facts only — HOA presence, lot sizes, ISD assignment, infrastructure |
| 20 | "Guarantee" or "promise" language | "I guarantee you'll get this comp", "I promise this is the best deal" | "this is the framework I use" / "this is what the data shows" — never guarantee outcomes |

---

## Pre-publish gate (Taylor runs before clicking Publish)

- [ ] License # inserted in description
- [ ] Brokerage office address inserted in description
- [ ] TREC IABS/CPN reference present in description
- [ ] All on-screen address signs blurred or cropped
- [ ] No banned words in final script, title, thumbnail text, description, chapters, pinned comment, or burned-in captions
- [ ] Banned-word grep run on `script.md` returns no matches
- [ ] All 3 comp tier assignments verified against same-day MLS + USACE + FEMA
- [ ] USACE Belton Lake Resource Manager's Office name confirmed current
- [ ] FEMA map version date overlay matches msc.fema.gov as of upload day
- [ ] SUP rule for STRs in MPR confirmed current with city
- [ ] No "best/top" agent claim anywhere
- [ ] No Fair Housing-implied phrasing in script, captions, or thumbnail
- [ ] No investor pivot anywhere
- [ ] No address numbers visible in drive-by or drone B-roll
- [ ] Owner vehicles cropped/blurred where visible
- [ ] Source attribution footer present on all data graphics
- [ ] Pinned comment ready to post immediately after publish

## Banned-word grep (run before recording AND before publish)

```bash
cd ~/claude-social-media-manager/yt-videos/morgans-point-resort/
grep -Ei "dream|charming|nestled|turnkey|white glove|hidden gem|perfect neighborhood|exclusive|sneak peek|insider|my expertise|paradise|oasis|stunning|gorgeous|safe neighborhood|family-friendly|kid-friendly|perfect for|best agent|top agent|award-winning" *.md
```

Expected output: zero matches.

If matches appear in this compliance-checklist.md itself (the rows above list the banned phrases for clarity), that's fine — they live in the risk column, not as creative language. Run the grep on `script.md`, `description-block.md`, `thumbnail-brief.md`, and `shorts-cutdowns.md` specifically.
