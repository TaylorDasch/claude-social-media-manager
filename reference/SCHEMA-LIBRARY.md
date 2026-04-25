# SCHEMA-LIBRARY — Pre-Built JSON-LD Templates
## Fill-in-the-blank schema for every page type on templetxhomes.net
## Reference: Any skill generating pages or content should pull from here

---

## TEMPLATE 1: VideoObject (Every Page With an Embedded Video)

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "[VIDEO_TITLE]",
  "description": "[2-3 sentence data-rich description]",
  "thumbnailUrl": "[YOUTUBE_THUMB_URL]",
  "uploadDate": "[YYYY-MM-DD]",
  "duration": "[PT#M#S]",
  "contentUrl": "[YOUTUBE_URL]",
  "embedUrl": "https://www.youtube.com/embed/[VIDEO_ID]",
  "publisher": {
    "@type": "RealEstateAgent",
    "name": "Taylor Dasch",
    "url": "https://templetxhomes.net"
  },
  "about": {
    "@type": "Place",
    "name": "[NEIGHBORHOOD or CITY]",
    "address": {
      "@type": "PostalAddress",
      "addressLocality": "[Temple/Belton/Killeen]",
      "addressRegion": "TX",
      "postalCode": "[ZIP]"
    }
  }
}
```

---

## TEMPLATE 2: FAQPage (Every Content Page — Extract Q&As from H2s)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[H2 QUESTION TEXT]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[FIRST 2-3 SENTENCES AFTER H2 — data-rich answer]"
      }
    }
  ]
}
```

**Note:** Add one Question object per H2 that's phrased as a question. Use for machine readability and AI parsing — Google restricts FAQ rich results to gov/health sites, but AI engines still parse FAQ schema heavily.

---

## TEMPLATE 3: RealEstateAgent + Person (Homepage + About Page)

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Taylor Dasch",
  "alternateName": "Deals with Dasch",
  "url": "https://templetxhomes.net",
  "telephone": "+1-254-718-4249",
  "email": "dealswithdasch@gmail.com",
  "image": "https://assets.agentfire3.com/uploads/sites/2128/2025/11/TaylorDaschImage.jpg",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Temple",
    "addressRegion": "TX",
    "postalCode": "76502",
    "addressCountry": "US"
  },
  "areaServed": [
    {"@type": "City", "name": "Temple", "sameAs": "https://en.wikipedia.org/wiki/Temple,_Texas"},
    {"@type": "City", "name": "Belton", "sameAs": "https://en.wikipedia.org/wiki/Belton,_Texas"},
    {"@type": "City", "name": "Killeen"},
    {"@type": "City", "name": "Harker Heights"},
    {"@type": "City", "name": "Salado"}
  ],
  "knowsAbout": [
    "Buy-and-hold rental property investing",
    "Baylor Scott & White medical professional relocation",
    "Fort Hood military relocation",
    "Physician home loans",
    "BRRRR strategy",
    "Mid-term rentals",
    "Bell County property tax protest",
    "1031 exchange",
    "DSCR loans"
  ],
  "sameAs": [
    "[WIKIDATA_URL]",
    "[YOUTUBE_LIVING_IN_TEMPLE_URL]",
    "[YOUTUBE_INVESTING_IN_TEMPLE_URL]",
    "[BIGGERPOCKETS_PROFILE_URL]",
    "[LINKEDIN_URL]",
    "[ZILLOW_PROFILE_URL]",
    "[TIKTOK_URL]"
  ],
  "memberOf": {
    "@type": "Organization",
    "name": "EG Realty"
  },
  "hasCredential": {
    "@type": "EducationalOccupationalCredential",
    "credentialCategory": "license",
    "recognizedBy": {
      "@type": "Organization",
      "name": "Texas Real Estate Commission"
    }
  }
}
```

**Action required:** Replace [WIKIDATA_URL] after creating the Wikidata entry. Fill in all sameAs profile URLs.

---

## TEMPLATE 4: Article (Blog Posts / Deal of the Week / Transcript Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[H1 TITLE]",
  "author": {
    "@type": "Person",
    "name": "Taylor Dasch",
    "url": "https://templetxhomes.net",
    "jobTitle": "REALTOR & Real Estate Investor",
    "worksFor": {"@type": "Organization", "name": "EG Realty"}
  },
  "publisher": {
    "@type": "Organization",
    "name": "Temple TX Homes",
    "url": "https://templetxhomes.net"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "about": {
    "@type": "Place",
    "name": "[TOPIC LOCATION]"
  }
}
```

---

## TEMPLATE 5: HowTo (Calculator Pages, Guide Pages, Step-by-Step)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[HOW TO TITLE]",
  "step": [
    {
      "@type": "HowToStep",
      "name": "[STEP NAME]",
      "text": "[STEP DESCRIPTION]"
    }
  ]
}
```

---

## TEMPLATE 6: LocalBusiness + AggregateRating (Pillar Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "RealEstateAgent",
  "name": "Taylor Dasch - EG Realty",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "[CURRENT_REVIEW_COUNT]",
    "bestRating": "5"
  }
}
```

---

## TEMPLATE 7: BreadcrumbList (All Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://templetxhomes.net"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "[SECTION]",
      "item": "https://templetxhomes.net/[SECTION-SLUG]/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[PAGE TITLE]",
      "item": "https://templetxhomes.net/[PAGE-SLUG]/"
    }
  ]
}
```

---

## STACKING MULTIPLE SCHEMAS (Use @graph)

When a page needs 3+ schema types (e.g., Article + VideoObject + FAQPage):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Article", ... },
    { "@type": "VideoObject", ... },
    { "@type": "FAQPage", ... }
  ]
}
```

---

## DEPLOYMENT RULES

1. Every page gets AT LEAST FAQPage schema (if it has Q&A content)
2. Every page with a video embed gets FAQPage + VideoObject
3. Homepage and about page get RealEstateAgent (Template 3)
4. Blog posts and transcript pages get Article + FAQPage
5. All schema goes in AgentFire Spark/Coder blocks — NEVER paste into text editor blocks
6. Validate at validator.schema.org before publishing
7. Stack multiple schema types using @graph when a page needs 3+
8. Update dateModified whenever page content is refreshed
9. `viewbox` not `viewBox` in any SVG elements (AgentFire quirk)
