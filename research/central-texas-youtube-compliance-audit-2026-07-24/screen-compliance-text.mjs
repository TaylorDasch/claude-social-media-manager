#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const captionDir = path.join(auditDir, "raw", "captions");
const rootCatalog = JSON.parse(
  await fs.readFile(path.join(auditDir, "root-channel-catalog.json"), "utf8"),
);
const discoveryCatalog = JSON.parse(
  await fs.readFile(path.join(auditDir, "discovery-video-catalog.json"), "utf8"),
);
const coverage = JSON.parse(
  await fs.readFile(path.join(auditDir, "caption-coverage.json"), "utf8"),
);

const excludedTaylorChannels = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ",
  "UCKuVz8ytHECKEAyRacDpm1g",
]);
const targetPlacePattern = /\b(?:Temple|Belton|Killeen|Harker Heights|Copperas Cove|Nolanville|Fort (?:Hood|Cavazos)|Bell County)\b/i;
const housingPattern = /\b(?:real estate|realtor|home|house|housing|property|properties|apartment|rent|rental|listing|market|neighborhood|relocat|moving|builder|construction|duplex|mortgage|loan|land|acreage|invest)\w*/i;
const patterns = [
  {
    category: "familial_status_preference",
    regex: /\b(?:family[- ]friendly|family[- ]oriented|perfect for (?:military )?famil(?:y|ies)|ideal for (?:military )?famil(?:y|ies)|best for famil(?:y|ies)|great for famil(?:y|ies)|top choice for famil(?:y|ies)|excellent (?:choice|option) for famil(?:y|ies)|families and retirees|families with (?:school[- ]age )?children|growing famil(?:y|ies)|affordable family homes)\b/giu,
  },
  {
    category: "explicit_household_limitation",
    regex: /\b(?:adults only|no children|no kids|singles only|married couples only|christians? only|muslims? only|jewish only|no wheelchairs?|able[- ]bodied only)\b/giu,
  },
  {
    category: "spanish_preference",
    regex: /\b(?:ideal para familias|perfect[oa] para familias|solo adultos|sin niñ[oa]s|solo cristian[oa]s|barrio seguro|mejores escuelas|buenas escuelas)\b/giu,
  },
  {
    category: "schools_safety_context",
    regex: /\b(?:best schools?|great schools?|good schools?|top[- ]rated schools?|highly rated schools?|safe(?:r|st)? neighborhood|safe(?:r|st)? communit(?:y|ies)|low crime|crime[- ]free|avoid (?:this|these|the) neighborhoods?|bad neighborhood)\b/giu,
  },
  {
    category: "demographic_or_steering_context",
    regex: /\b(?:what kind of people (?:live|typically live)|young professionals|retirees and empty nesters|for retirees|retirement community|school[- ]age children|military families|families prefer|families prioritize|more families means)\b/giu,
  },
  {
    category: "ranking_or_superiority_claim",
    regex: /\b(?:#\s*1|number one|top producer|top producing|top\s*1\s*%|best (?:agent|realtor|brokerage|property management|rental company)|leading rental compan(?:y|ies)|fastest growing|consistently ranked|award[- ]winning)\b/giu,
  },
  {
    category: "valuation_or_return_claim",
    regex: /\b(?:instant equity|below apprais(?:al|ed value)|guaranteed appreciation|steady appreciation|stronger appreciation|massive upside|hold their value|holds? (?:its|their) value|year 1 profit|annual net profit|monthly cash flow|cash flow starts|reliable retirement strategy|million[- ]dollar portfolios?|six[- ]figure wealth|pay your kids|pay itself forward|profitable move)\b/giu,
  },
  {
    category: "financial_or_lending_claim",
    regex: /\b(?:\d+(?:\.\d+)?\s*%\s*(?:apr|annual percentage rate)|0\s*%\s*down|zero down|free solar|cash rebate|cash back|builder[- ]paid commission|lower interest rate|no money down|save you \$?\d[\d,]*|more likely over (?:the )?million)\b/giu,
  },
  {
    category: "guarantee_or_performance_claim",
    regex: /\b(?:guaranteed|sell your home faster|for more money|commanding more per square foot|sell(?:ing)? homes fast|most stress[- ]free move|perfect home|seamless transition)\b/giu,
  },
  {
    category: "referral_or_material_connection",
    regex: /\b(?:preferred lender|preferred title|preferred inspector|sponsored by|paid partnership|affiliate link|referral fee|builder[- ]paid|commission rebate|we receive compensation|promotion)\b/giu,
  },
];

function snippet(text, index, length, radius = 140) {
  const start = Math.max(0, index - radius);
  const end = Math.min(text.length, index + length + radius);
  return text.slice(start, end).replace(/\s+/g, " ").trim();
}

function findMatches(text, source, timestamp = "") {
  const found = [];
  for (const { category, regex } of patterns) {
    regex.lastIndex = 0;
    for (const match of text.matchAll(regex)) {
      found.push({
        category,
        source,
        timestamp,
        match: match[0],
        excerpt: snippet(text, match.index, match[0].length),
      });
    }
  }
  return found;
}

const byId = new Map();
const rootIds = new Set(rootCatalog.map((item) => item.id));
for (const item of [...rootCatalog, ...discoveryCatalog]) {
  if (excludedTaylorChannels.has(item.channel_id)) continue;
  const text = `${item.title ?? ""}\n${item.description ?? ""}`;
  if (!rootIds.has(item.id) && !(targetPlacePattern.test(text) && housingPattern.test(text))) {
    continue;
  }
  const current = byId.get(item.id) ?? item;
  byId.set(item.id, {
    ...current,
    in_root_channel_catalog:
      Boolean(current.in_root_channel_catalog) || rootIds.has(item.id),
  });
}
const coverageById = new Map(coverage.map((item) => [item.id, item]));
const queue = [];

for (const item of byId.values()) {
  const matches = [
    ...findMatches(item.title ?? "", "title"),
    ...findMatches(item.description ?? "", "description"),
  ];
  const caption = coverageById.get(item.id);
  if (caption?.transcript_path) {
    try {
      const body = await fs.readFile(path.join(auditDir, caption.transcript_path), "utf8");
      for (const line of body.split("\n")) {
        if (!line) continue;
        const [time, ...parts] = line.split("\t");
        matches.push(...findMatches(parts.join("\t"), "caption", time));
      }
    } catch {
      // Coverage file remains the source of truth for retrieval gaps.
    }
  }
  if (!matches.length) continue;
  const grouped = Object.groupBy(matches, (match) => match.category);
  queue.push({
    id: item.id,
    upload_date: item.upload_date || item.publish_date,
    channel_id: item.channel_id,
    channel: item.channel,
    title: item.title,
    url: item.url,
    in_root_channel_catalog: Boolean(item.in_root_channel_catalog),
    caption_status: caption?.status ?? "not_collected_independent_lane",
    categories: Object.keys(grouped).sort(),
    evidence: Object.fromEntries(
      Object.entries(grouped)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([category, rows]) => [category, rows.slice(0, 8)]),
    ),
  });
}

queue.sort((a, b) =>
  b.categories.length - a.categories.length
  || a.channel.localeCompare(b.channel)
  || a.upload_date.localeCompare(b.upload_date)
  || a.id.localeCompare(b.id),
);
await fs.writeFile(
  path.join(auditDir, "automated-risk-screen.json"),
  `${JSON.stringify(queue, null, 2)}\n`,
);

const markdown = [
  "# Automated compliance-text review queue",
  "",
  "This is a recall-oriented text screen, not a finding or legal conclusion. Every item requires context review against the linked video, current profile/direct links, and the rule matrix.",
  "",
  `Videos with one or more text matches: **${queue.length}**`,
  "",
  "| Date | Channel | Video | Categories | Caption status |",
  "|---|---|---|---|---|",
  ...queue.map((item) =>
    `| ${item.upload_date} | ${item.channel.replaceAll("|", "\\|")} | [${item.title.replaceAll("|", "\\|")}](${item.url}) | ${item.categories.join(", ")} | ${item.caption_status} |`,
  ),
  "",
].join("\n");
await fs.writeFile(path.join(auditDir, "automated-risk-screen.md"), markdown);
process.stdout.write(`review_queue=${queue.length}\n`);
