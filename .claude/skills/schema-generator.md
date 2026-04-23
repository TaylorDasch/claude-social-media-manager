# Schema Markup Generator

## Trigger
"generate schema", "schema for", "json-ld", "structured data", "schema markup"

## Required Inputs
- URL or page content (HTML file path or URL)
- Page type: Neighborhood, Blog Post, Listing, Video Page, About, FAQ, or Home

## Step-by-Step Execution

### Step 1 — Read Page Content
1. Read the HTML file or fetch the URL
2. Identify: title, description, headings, FAQs, video embeds, images, author, dates, breadcrumbs
3. Read `reference/SCHEMA-LIBRARY.md` for template patterns

### Step 2 — Determine Required Schema Types

| Page Type | Required Schema |
|-----------|----------------|
| Any page | `LocalBusiness` (RealEstateAgent) + `BreadcrumbList` |
| Blog post | + `Article` + `FAQPage` (if FAQ section exists) |
| Video page | + `VideoObject` |
| Blog with video | + `Article` + `VideoObject` + `FAQPage` |
| Neighborhood page | + `Article` + `FAQPage` + `Place` |
| Listing page | + `RealEstateListing` + `FAQPage` |
| About page | + `Person` + `Organization` |

### Step 3 — Generate JSON-LD

**LocalBusiness / RealEstateAgent (every page):**
```json
{
  "@context": "https://schema.org",
  "@type": ["RealEstateAgent", "LocalBusiness"],
  "name": "Taylor Dasch - EG Realty",
  "image": "https://assets.agentfire3.com/uploads/sites/2128/2025/11/TaylorDaschImage.jpg",
  "url": "https://templetxhomes.net",
  "telephone": "+1-254-718-4249",
  "email": "dealswithdasch@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Temple",
    "addressRegion": "TX",
    "postalCode": "76502",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 31.0982,
    "longitude": -97.3428
  },
  "areaServed": [
    {"@type": "City", "name": "Temple, TX"},
    {"@type": "City", "name": "Belton, TX"},
    {"@type": "City", "name": "Killeen, TX"}
  ],
  "knowsAbout": ["Temple TX Real Estate", "Fort Hood Housing", "BSW Physician Relocation", "Buy-and-Hold Investing"],
  "sameAs": [
    "https://www.youtube.com/@LivinginTemple",
    "https://www.youtube.com/@InvestinginTemple",
    "https://www.biggerpockets.com/users/taylordasch",
    "https://www.tiktok.com/@taylordasch"
  ]
}
```

**Article:**
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[H1 text]",
  "description": "[meta description]",
  "author": {
    "@type": "Person",
    "name": "Taylor Dasch",
    "jobTitle": "Real Estate Agent",
    "worksFor": {"@type": "Organization", "name": "EG Realty"}
  },
  "publisher": {
    "@type": "Organization",
    "name": "EG Realty",
    "url": "https://templetxhomes.net"
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "mainEntityOfPage": "[canonical URL]",
  "image": "[hero image URL]"
}
```

**VideoObject:**
```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "[video title]",
  "description": "[video description — first 200 chars]",
  "thumbnailUrl": "[thumbnail URL]",
  "uploadDate": "[YYYY-MM-DD]",
  "duration": "[PT#M#S format]",
  "contentUrl": "[YouTube URL]",
  "embedUrl": "https://www.youtube.com/embed/[video_id]",
  "author": {
    "@type": "Person",
    "name": "Taylor Dasch"
  }
}
```

**FAQPage:**
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[question from H2 or FAQ section]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[answer text — concise, factual]"
      }
    }
  ]
}
```

**BreadcrumbList:**
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://templetxhomes.net"},
    {"@type": "ListItem", "position": 2, "name": "[parent]", "item": "[parent URL]"},
    {"@type": "ListItem", "position": 3, "name": "[current page]", "item": "[current URL]"}
  ]
}
```

### Step 4 — Combine and Validate
1. Merge all schema types into a single `<script type="application/ld+json">` block using `@graph`
2. Validate: no empty required fields, dates in ISO 8601, URLs are absolute
3. Check against existing schema on the page — don't duplicate

## Output Format
- `[slug]-schema.json` — Complete JSON-LD ready to paste into page head
- `[slug]-schema-instructions.md` — Where to place it, what it replaces

## Quality Checks
- [ ] Valid JSON (no trailing commas, proper escaping)
- [ ] All required fields populated (no empty strings)
- [ ] Dates in YYYY-MM-DD format
- [ ] URLs are absolute (start with https://)
- [ ] Phone number: +1-254-718-4249
- [ ] Entity name exact: "Taylor Dasch - EG Realty"
- [ ] No schema type missing for the page type (see table above)
- [ ] FAQPage has minimum 3 questions
- [ ] VideoObject duration in PT format (e.g., PT12M30S)

## Brand Rules
- Author is always "Taylor Dasch" with jobTitle "Real Estate Agent" (not broker)
- Organization is always "EG Realty"
- sameAs links must be real, verified profiles
- knowsAbout uses "Fort Hood" not "Fort Cavazos"
