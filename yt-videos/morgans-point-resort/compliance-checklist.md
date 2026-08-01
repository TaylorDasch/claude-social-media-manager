# Morgan's Point Resort — Compliance Checklist

> Current package basis: `GROUND-TRUTH-2026-07-30.md`
> Review date: 2026-07-31

## 1. Data integrity

- [ ] Every volatile MLS number is date-stamped `July 30, 2026`.
- [ ] Active count is **13**, not 15.
- [ ] Total filtered universe is **26**, not 29.
- [ ] Active range is **$205,000–$869,000**.
- [ ] Active size range is **1,001–2,804 sqft**.
- [ ] Active build-year range is **1966–2026**.
- [ ] Active $/sqft range is shown as **$152–$310**, rounded from the source.
- [ ] Septic is phrased as **mentioned in 4 of 26 listing-remark records**, not `4 homes definitely have septic`.
- [ ] HOA is phrased as an MLS field pattern: **24 None · 2 Mandatory**, verify the property.
- [ ] The active median is not used to value an individual property.
- [ ] No subset median is presented as a city-label price effect.

## 2. Comparable-sales language

- [ ] The script says similar market area, site, size, age, condition, style, and property rights.
- [ ] The script does not promise an appraisal result.
- [ ] The script does not say a particular active is overpriced or a bargain.
- [ ] Current listings are not described as closed-sale proof of value.
- [ ] The MLS city label is not used as a value adjustment, market tier, or comp selector.

**Approved line:**

> "When I run comps here, I start with nearby closed sales that compete for the same buyer—similar site, size, age, condition, style, and property rights. If I need to expand outside that immediate set, I explain why and adjust for the real differences."

## 3. Retired city-field thesis

The following must return zero hits in all public package files and exported captions:

- [ ] `$315,000 apparent floor`
- [ ] `$110,000 gap`
- [ ] `50.8% premium`
- [ ] `price illusion`
- [ ] `different market` based on city field
- [ ] `city field sorts by age`
- [ ] `all cheap homes are filed under Belton`
- [ ] `a name search prices the town too high`

Internal historical files may retain the old argument for audit history. They are not production sources.

## 4. Water, shoreline, and dock claims

- [ ] Say CTXMLS **does** have waterfront and water-access fields.
- [ ] `WaterfrontYN = False` is stated as **26 of 26**.
- [ ] `WaterAccessYN` is stated as **True 2 · False 4 · blank 20**.
- [ ] Belton Lake view mentions are stated as **4 of 26**.
- [ ] Private docks and piers are described as prohibited lake-wide under the USACE master-plan rule.
- [ ] Public/commercial/courtesy docks are not conflated with privately owned residential docks.
- [ ] A lake view is not described as shoreline ownership.
- [ ] GIS is labeled as not a survey.
- [ ] `Many`, `most`, or `generally` is used for the federal shoreline belt; never `every lot`.
- [ ] Exact property boundary is deferred to a survey or Corps boundary record.

**Primary source:** USACE Belton Lake Master Plan, December 2018.

## 5. Property-condition language

- [ ] No identifiable home is said to have foundation, roof, HVAC, electrical, plumbing, septic, or insurance problems without property-specific evidence.
- [ ] Inspection footage is permissioned, licensed, or generic.
- [ ] The property-specific disclaimer remains to camera.
- [ ] Insurance guidance is procedural, not a promise of coverage or premium.
- [ ] Septic guidance is procedural, not an engineering opinion.

**Required line:**

> "I'm not telling you any specific home here has any of those issues. I'm telling you the active inventory runs from 1966 to 2026, so the due diligence can't be one-size-fits-all."

## 6. Fair housing and steering

- [ ] Discuss physical property types, land-use rules, zoning, and recorded restrictions only.
- [ ] Do not characterize residents by income, class, family status, race, religion, national origin, disability, sex, or any other protected characteristic.
- [ ] Do not say or imply manufactured homes reduce surrounding values.
- [ ] Do not film an identifiable manufactured home as an illustration of a downside.
- [ ] Do not rank or steer buyers toward or away from a street.
- [ ] Give the variable and the verification method; the buyer decides.
- [ ] School language says all 26 MLS records show Belton ISD and the exact address must be verified with the district.

## 7. Filming and privacy

- [ ] Public access or written property permission confirmed.
- [ ] No trespass.
- [ ] Drone launch/landing permission and FAA rules confirmed.
- [ ] No readable house numbers, active-listing signs, occupants, faces, or license plates.
- [ ] Current lake footage is used; no old shot is implied to show current pool level.
- [ ] Any parcel-line overlay says `ILLUSTRATION — NOT A SURVEY`.

## 8. Voice and entity

- [ ] `Taylor Dasch with EG Realty` appears in the first three sentences.
- [ ] Taylor is identified as a Real Estate Agent, not a broker.
- [ ] At least one honest negative remains.
- [ ] At least one recommend-against line remains.
- [ ] Hook, title, thumbnail, script, description, Shorts, and CTA share the same three-check promise.
- [ ] Banned-language scan passes.

## 9. Final export search

Run against the production package and caption file:

```bash
rg -n -i '\$315|\$110|50\.8|price illusion|city field sorts|different market|no waterfront field|private dock permit' \
  concept.md script.md talking-points.md description-block.md on-screen-graphics.md \
  shorts-cutdowns.md shot-list.md thumbnail-brief.md seo-aeo-notes.md
```

Any hit must be reviewed. A hit inside an explicit `do not say` or retired-claim audit block is acceptable; a hit in public copy is not.

## 10. Final go/no-go

- [ ] Hook recorded cleanly.
- [ ] Three checks signposted and paid.
- [ ] USACE rule sourced in description.
- [ ] Chapters corrected to final export.
- [ ] Thumbnail contains no old price-label story.
- [ ] Pinned comment contains no old price-label story.
- [ ] Taylor approves before publication.
