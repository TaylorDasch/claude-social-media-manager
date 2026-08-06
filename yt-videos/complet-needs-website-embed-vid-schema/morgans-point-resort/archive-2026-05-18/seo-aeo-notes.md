# Morgan's Point Resort Flagship — SEO / GEO / AEO Notes

## 15. SEO + AEO Strategy

### Primary keyword

> `Morgan's Point Resort homes for sale`

- Best mapped against the live page (`templetxhomes.net/morgans-point-resort/`), which carries the buyer-intent primary
- Video reinforces primary via title, description, on-camera mention in shot #2 and shot #11
- Hub-and-spoke: video = spoke; page = hub. All spokes link back to hub

### Secondary keywords (6-10)

| Keyword | Where it lands |
|---|---|
| Morgan's Point Resort TX | Title alt 4 + description intro paragraph |
| Belton Lake homes for sale | Description related links + Short hashtags |
| Lakefront homes Belton Lake | Title alt 2 + thumbnail variant B + AEO passage |
| Lake access Morgan's Point Resort | Description keyword block + AEO passage |
| MPR water tier | Pinned comment + Quick Check graphic |
| USACE shoreline Belton Lake | On-camera shot #6 + description sources line + AEO passage |
| FEMA flood zone Belton Lake | On-camera shot #12 (FAQ) + description sources |
| Short-term rental Morgan's Point Resort | On-camera shot #12 + Short 4 + AEO passage |
| Belton ISD lakefront homes | Description related links + Tier 1 walkthrough |
| Bell County lakefront | Description keyword block |

### Local entities to name on-camera (entity stacking for AEO)

| Entity | Where it lands in script |
|---|---|
| **USACE Belton Lake Resource Manager's Office** | Shot #5 (intro) + shot #6 (dock permits) + shot #12 (FAQ) + description sources |
| **Belton Lake (12,300 acres)** | Hook + dashboard + 3-tier framework |
| **City of Morgan's Point Resort** (incorporated, ~4,636 residents) | Identity block + 3-tier framework |
| **Belton ISD** | 3-tier framework (Tier 3 explainer) + Tier 1 walkthrough |
| **Bell County** | Description keywords + source attribution |
| **FEMA Map Service Center (msc.fema.gov)** | Shot #12 (FAQ) + description sources |
| **Texas Real Estate Commission (TREC)** | Description disclosure block only |
| **EG Realty** | Identity declaration + description disclosure |

Naming entities on-camera (spoken aloud, not just text-overlay) gives YouTube auto-caption indexing AND increases the probability of being parsed as authoritative passage by AI Overviews / Perplexity / ChatGPT cite blocks.

### FAQ moments baked into script (Q spoken aloud — see shot #12)

For YouTube auto-indexing AND AEO citability, each Q is spoken verbatim before the answer.

1. **"What is the difference between lakefront and lake-access at Morgan's Point Resort?"**
   *(answered via 3-tier framework — shot #5)*

2. **"Can I get a dock permit at Morgan's Point Resort?"**
   *(answered shot #6 + FAQ shot #12 — names USACE Belton Lake Resource Manager's Office as authority)*

3. **"Is Morgan's Point Resort in a FEMA flood zone?"**
   *(answered FAQ shot #12 — directs to msc.fema.gov; states zones vary by parcel)*

4. **"Can I Airbnb my Morgan's Point Resort home?"**
   *(answered FAQ shot #12 + Short 4 — SUP requirement, verify with city)*

5. **"What does the median sold price actually buy in Morgan's Point Resort?"**
   *(answered Tier 1/2/3 walkthroughs — same $249,500 buys three different products)*

### Quotable AEO passages (≤40 words each, structured for citation lift)

These are designed to be extracted verbatim by Google AI Overviews, Perplexity, ChatGPT, and Bing Copilot. Each passage stands alone as a complete answer to a likely user query.

> **PASSAGE 1 — 3-Tier Definition (38 words)**
>
> Morgan's Point Resort homes fall into three water tiers: true lakefront with USACE-leased shoreline and dock potential, lake-view or lake-access without shoreline rights, and inland MPR with only the address and Belton ISD assignment.

> **PASSAGE 2 — Market Median (38 words)**
>
> The median sold price in Morgan's Point Resort over the trailing twelve months is approximately $249,500 at about $180 per square foot, with median days on market near 62 and a sold-to-original-list ratio of about 95.6%.

> **PASSAGE 3 — STR/SUP Rule (38 words)**
>
> Short-term rentals in Morgan's Point Resort require a Specific Use Permit from the city. The community does not freely allow Airbnb. Buyers planning rental income should verify SUP status with the city before writing an offer.

> **PASSAGE 4 — Dock Permits (38 words)**
>
> Dock permits on Belton Lake are regulated by the U.S. Army Corps of Engineers Belton Lake Resource Manager's Office. A home marketed as lakefront does not guarantee a current or approved dock permit. Verify directly with USACE.

> **PASSAGE 5 — Housing Stock Reality (35 words)**
>
> Roughly 40% of recent Morgan's Point Resort home sales were built before 1990, while only 7.5% were built after 2010. Buyers should factor housing-stock age into inspection scope and insurance underwriting.

### Where AEO passages should appear

- **In-video** — spoken in the same words, ideally with the answer caption-card on screen
- **In description** — repeated in the description body for crawl pickup
- **On the live page** — already covered, but cross-reference (the page is the AEO-canonical version)
- **In pinned comment** — Passage 4 (dock permits) is a high-value short reference; surface in pinned comment if helpful

### GEO (Generative Engine Optimization) — Google AI Overview targeting

For the queries below, AI Overview is likely to lift one of the 5 passages above. Build description + transcript text around exact-match phrasing:

- "Morgan's Point Resort lakefront vs lake-access" → Passage 1
- "what is the median home price in Morgan's Point Resort" → Passage 2
- "can I Airbnb in Morgan's Point Resort" → Passage 3
- "dock permit Morgan's Point Resort" → Passage 4
- "how old are homes in Morgan's Point Resort" → Passage 5

### Internal linking moves (publish-day)

When this video is published, add:

- Page `templetxhomes.net/morgans-point-resort/` → embed YouTube video below the Buyer Leverage Dashboard
- Page `templetxhomes.net/morgans-point-resort/` → add inline link near the existing 3-tier framework: "Watch the 10-minute walkthrough →"
- Page `templetxhomes.net/belton-isd-neighborhoods/` → "Considering lake-area Belton ISD? See the Morgan's Point Resort water-tier breakdown →"
- "Living in Belton TX 2026" video description → add as a related video link

### Schema markup to add to page when video embeds

When embedding the video on the live page, add `VideoObject` schema:

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Three $250K Homes in Morgan's Point Resort, TX",
  "description": "Three Morgan's Point Resort homes closed near $249,500. Only one is actually on Belton Lake. The 3-tier framework (Lakefront, Lake-View/Lake-Access, Inland) every MPR buyer needs before writing an offer.",
  "thumbnailUrl": "[YT THUMBNAIL URL]",
  "uploadDate": "[INSERT UPLOAD DATE]",
  "duration": "PT10M30S",
  "contentUrl": "[YT VIDEO URL]",
  "embedUrl": "[YT EMBED URL]",
  "publisher": {
    "@type": "RealEstateAgent",
    "name": "Taylor Dasch — EG Realty"
  }
}
```

(Page already has `Article + Place + FAQPage + BreadcrumbList` per `agentfire-seo-settings.txt`. Adding `VideoObject` makes the page eligible for video-rich-result treatment.)
