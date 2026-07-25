#!/usr/bin/env node

/*
 * Offline, recall-first compliance text screen for authenticated yt-dlp exports.
 *
 * Input:  authenticated-video-catalog.json (from build-authenticated-catalog.mjs)
 * Output: authenticated-risk-screen.json and authenticated-risk-screen.md
 *
 * This script never opens YouTube, invokes yt-dlp, accesses a browser, or touches
 * credential stores. A match is a review cue only, not a compliance finding or a
 * legal conclusion. Review the actual video, visual overlays, disclosures, current
 * profile/direct links, and applicable rules before recording any finding.
 */

import fs from "node:fs/promises";
import path from "node:path";

const auditDir = path.dirname(new URL(import.meta.url).pathname);
const catalogPath = path.join(auditDir, "authenticated-video-catalog.json");
const jsonOutputPath = path.join(auditDir, "authenticated-risk-screen.json");
const markdownOutputPath = path.join(auditDir, "authenticated-risk-screen.md");
const rootFullChannelsPath = path.join(auditDir, "root-full-catalog-channels.tsv");
const rootScopePath = path.join(auditDir, "root-scope-adjudication.tsv");
const rootDirectInputsPath = path.join(auditDir, "authenticated-root-direct-video-inputs.txt");
const gapFullInputsPath = path.join(auditDir, "authenticated-gap-full-channel-inputs.txt");
const discoveryGapPath = path.join(auditDir, "discovery-gap-triage.tsv");
const searchResultsPath = path.join(auditDir, "search-results.json");

// Defense in depth: the upstream builder excludes these channels, but this screen
// independently rejects them before reading associated caption artifacts.
const excludedTaylorChannelIds = new Set([
  "UCqrLPGPR9eV7QUfK02dwtpQ", // Living in Temple
  "UCKuVz8ytHECKEAyRacDpm1g", // Invest Central Texas
]);
const excludedTaylorIdentity = /\b(?:taylor dasch|living in temple|invest central texas)\b/i;
const discoveryDirectOnlyOverrides = new Set([
  "UCVfUGN4gxcLeWzP5K_fPgnA", // national Palm Harbor channel
  "UCatgc79aqbQYQQkpNVXfb3A", // Austin-market identity
  "UC6YcqWxqAo3jNVxyyF2MZyA", // national real-estate/media identity
  "UCYsdJIrTd2vYmfqSNfUSYZA", // North Atlanta identity
  "UC_ijOhQ7aWRH6GqL1a-G5Dg", // Northwest Austin identity
]);
const manualAndZeroEligibleFullChannelIds = new Set([
  "UC1SKo4gUtYWElAGwZSguqpA",
  "UCqo6EaV9o6bFg4szBL8RYEw",
  "UCwoQakQVf2m8hfitYnymb5w",
  "UCeZysVNyhl-JqrqesQjcqPg",
  "UCijF1zTR7RluBFGicVZU4SA",
  "UCvyNP3_ZgVLciAIev5t2Gog",
  "UCWykQcBeQE_1yY2lk9m23YQ",
  "UC5v4flYtIbs8z1ZQ-d-nGXw",
]);

const reasonFamilies = [
  {
    family: "family_children_suitability",
    note: "Review whether housing is being described as suited to, preferred by, or excluding families/children.",
    regex: /\b(?:family[- ]friendly|family[- ]oriented|family[- ]first|family living|family home|for the whole family|busy family life|perfect for (?:a |the |any |military )?famil(?:y|ies)|ideal for (?:a |the |any |military )?(?:famil(?:y|ies)|dwelling for the whole family)|great for (?:a |the |any )?famil(?:y|ies)|best for (?:a |the |any )?famil(?:y|ies)|designed for (?:easy )?(?:a )?(?:growing )?family living|designed for (?:a )?growing famil(?:y|ies)|growing famil(?:y|ies)|parents?'? dream|space (?:your|the) family (?:has|have) been craving|your family(?:, children,? and pets)? will (?:love|approve)|families with (?:school[- ]age )?(?:children|kids)|(?:children|kids) (?:can|will) (?:play|love)|room for (?:your |the )?(?:children|kids) to play|backyard (?:that|where|is just right for) (?:your |the )?(?:children|kids)(?: can play)?|perfect for kids|monitor (?:your )?(?:children|kids)|no (?:kids|children)|adults? only|singles? only|married couples? only|empty nesters?)\b/giu,
  },
  {
    family: "schools_crime_safety_or_avoidance",
    note: "Review context and consistency; school/crime information alone is not a Fair Housing conclusion.",
    regex: /\b(?:(?:best|great|good|top[- ]rated|highly rated|higher[- ]ranking|highest[- ]rated) schools?|school district|low(?:er)? crime|crime[- ]free|safe(?:r|st)? (?:neighborhood|community|area|place)|dangerous (?:neighborhood|area)|avoid (?:this|these|the|those) (?:neighborhoods?|areas?|parts? of town)|places? (?:for you )?to avoid|bad neighborhood|sketchy (?:neighborhood|area)|too ghetto)\b/giu,
  },
  {
    family: "demographic_composition_or_steering",
    note: "Review for protected-class targeting, preference, limitation, or steering rather than treating generic demographics as conclusive.",
    regex: /\b(?:what kind of people (?:live|typically live)|who (?:lives|typically lives) (?:here|there)|young professionals|retirees and empty nesters|for retirees|retirement community|military families|families prefer|families prioritize|families (?:end up|are) (?:landing|moving)|more families means|predominantly (?:white|black|hispanic|latino|asian|christian|muslim|jewish)|(?:white|black|hispanic|latino|asian|christian|muslim|jewish) (?:neighborhood|community|area)|people like you)\b/giu,
  },
  {
    family: "loan_rate_apr_downpayment_or_incentive",
    note: "Review lending, rate, down-payment, rebate, closing-cost, and builder-incentive statements for terms/disclosures and factual support.",
    regex: /\b(?:\d+(?:\.\d+)?\s*%\s*(?:apr|interest|rate)|annual percentage rate|0\s*%\s*down|zero down|no money down|as low as \$?\d[\d,]* down|\$?\d[\d,]*(?:\s*(?:in )?)?(?:closing costs?|credit|rebate|cash back)|closing[- ]cost(?:s)? (?:paid|covered)|builder[- ]paid(?:\s+commission)?|rate buy[- ]?down|lower (?:your )?(?:rate|payment)|incentive(?:s)?|free (?:solar|appliances?)|no mortgage(?: payments?)?|mortgage[- ]free|no rent|free rent|owner financ(?:e|ed|ing)|all credit (?:ok|okay)|no credit check)\b/giu,
  },
  {
    family: "investment_return_equity_or_profit",
    note: "Review investment, appreciation, cash-flow, equity, return, and profit claims for qualification and support.",
    regex: /\b(?:instant equity|negative equity|below (?:market|apprais(?:al|ed)) value|guaranteed appreciation|steady appreciation|strong(?:er)? appreciation|outperform(?:s|ed|ing)? other neighborhoods|\d+(?:\s*(?:to|-)\s*\d+)?\s*%\s*(?:increase|appreciation|value gain)|prices? (?:will|are going to) go up|sure to (?:make|be) (?:a )?(?:good|great) investment|massive upside|hold(?:s)? (?:its|their) value|cash flow|cash[- ]flowing|cash flow like crazy|profit(?:able|s|ing)?|return on investment|maximi[sz]e (?:your )?(?:return on investment|\broi\b)|\broi\b|annual net profit|monthly net|year[- ]?one profit|rental income|investment return|passive income|built[- ]in demand|consistent revenue streams?|long[- ]term stability|income[- ]producing|strong rental demand|build (?:six[- ]figure )?wealth|million[- ]dollar (?:portfolio|wealth))\b/giu,
  },
  {
    family: "ranking_superlative_or_numeric_comparison",
    note: "Review rankings, superiority claims, comparisons, and numeric performance statements for substantiation and currentness.",
    regex: /\b(?:#\s*1|number one|top\s*1\s*%|top producer|top producing|top dollar|best (?:agent|realtor|brokerage|property management|rental company)|leading (?:agent|brokerage|company)|fastest growing|award[- ]winning|most (?:trusted|successful|experienced)|higher sale price|over \$?\d[\d,.]*\s*(?:million|m)\s*(?:sold|in sales)|(?:sold|sell(?:ing)?) (?:homes )?faster|sold in \d+ days?|sat (?:for )?(?:nearly |almost )?\d+ days?|(?:get|gets|getting|command(?:s|ing)?) more per square foot|faster for more money|most money in your pocket|more money in your pocket|net proceeds?(?: can be| of)? \$?\d[\d,.]*(?:\s*(?:to|-)\s*\$?\d[\d,.]*)?|netted (?:about )?\$?\d[\d,.]*|undervalu(?:ed|ing)(?: [^.!?]{0,50})? by \$?\d+(?:\.\d+)?\s*[km]?|maximize (?:your )?(?:profit|proceeds)|\$?\d[\d,.]*\s*(?:difference|saved|savings|year[- ]?one profit|annual net profit)|\d+(?:\.\d+)?\s*%\s*(?:more|less|higher|lower|faster|down|up))\b/giu,
  },
  {
    family: "license_identity_or_required_notice",
    note: "Review stated broker/NMLS/license identity and whether IABS/CPN references or direct links are complete and internally consistent.",
    regex: /\b(?:nmls(?:\s*(?:#|number|id))?\s*\d+|license(?:\s*(?:#|number|id))?\s*\d+|brokered by|information about brokerage services|consumer protection notice|\biabs\b|\bcpn\b|real estate broker|licensed (?:agent|realtor|broker))\b/giu,
  },
  {
    family: "stale_or_time_sensitive_status",
    note: "Review time-sensitive listing, market, loan, or incentive statements for currentness at the time of publication and continued availability.",
    regex: /\b(?:available now|just listed|still available|today(?: only)?|right now|current(?:ly)?|as of (?:today|this week|this month)|this (?:week|month|year)'?s market|limited time|expires? (?:today|soon)|last chance|act now|inventory is (?:low|high)|rates? (?:are|is) (?:at|down|up))\b/giu,
  },
  {
    family: "endorsement_referral_affiliate_or_compensation",
    note: "Review endorsements, preferred-provider recommendations, material connections, referral compensation, and disclosure placement.",
    regex: /\b(?:preferred (?:lender|title|inspector|vendor|partner)|sponsored by|paid partnership|affiliate link|affiliate(?:\s+commission)?|referral fee|we receive compensation|compensated(?:\s+link)?|promotion|partnered with|use my code|discount code|commission rebate)\b/giu,
  },
  {
    family: "guarantee_or_unqualified_outcome",
    note: "Review guarantees and unqualified outcome promises for complete terms, scope, support, and broker-approved qualification.",
    regex: /\b(?:your home sold guaranteed(?!\s+realty)|home sold guaranteed(?!\s+realty)|guaranteed (?:sale|offer|approval|savings|results?|rent|income|return)|we guarantee|100\s*%\s*(?:clean|satisfaction|approved|approval) guarantee|sell your home or (?:we|i)'?ll buy it|if we don'?t sell it,? (?:we|i)'?ll buy it)\b/giu,
  },
];

function asText(value) {
  return typeof value === "string" ? value : value == null ? "" : String(value);
}

function normaliseText(value) {
  return asText(value).replace(/\s+/g, " ").trim();
}

function timestamp(seconds) {
  const value = Number(seconds);
  if (!Number.isFinite(value) || value < 0) return "";
  const total = Math.floor(value);
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const remainder = total % 60;
  return hours > 0
    ? `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`
    : `${String(minutes).padStart(2, "0")}:${String(remainder).padStart(2, "0")}`;
}

function parseClock(value) {
  const match = asText(value).trim().replace(",", ".").match(/(?:(\d+):)?(\d{1,2}):(\d{2}(?:\.\d+)?)/);
  if (!match) return null;
  return Number(match[1] || 0) * 3600 + Number(match[2]) * 60 + Number(match[3]);
}

function stripMarkup(value) {
  return normaliseText(asText(value).replace(/<[^>]*>/g, " ").replace(/&nbsp;/gi, " ").replace(/&amp;/gi, "&"));
}

function parseJson3(raw) {
  const parsed = JSON.parse(raw);
  const events = Array.isArray(parsed?.events) ? parsed.events : Array.isArray(parsed) ? parsed : [];
  return events.flatMap((event) => {
    const text = normaliseText((event?.segs || []).map((seg) => seg?.utf8 || "").join(""));
    if (!text || /^\[.*\]$/.test(text)) return [];
    return [{ timestamp: timestamp(Number(event?.tStartMs) / 1000), text }];
  });
}

function parseTimedSubtitle(raw) {
  const lines = raw.replace(/\r/g, "").split("\n");
  const rows = [];
  let activeTime = "";
  let buffer = [];
  const flush = () => {
    const text = stripMarkup(buffer.join(" "));
    if (text) rows.push({ timestamp: activeTime, text });
    activeTime = "";
    buffer = [];
  };
  for (const line of lines) {
    if (/^\s*$/.test(line)) {
      flush();
      continue;
    }
    if (/^WEBVTT|^NOTE(?:\s|$)|^STYLE(?:\s|$)|^REGION(?:\s|$)|^\d+\s*$/i.test(line)) continue;
    if (line.includes("-->")) {
      flush();
      activeTime = timestamp(parseClock(line.split("-->")[0]));
      continue;
    }
    buffer.push(line);
  }
  flush();
  return rows;
}

function parsePlainText(raw) {
  return raw.replace(/\r/g, "").split("\n").flatMap((line) => {
    const match = line.match(/^\s*(\d{1,2}:\d{2}(?::\d{2})?(?:\.\d+)?)\s*(?:\t|[-–—]\s+)(.*)$/);
    const text = normaliseText(match ? match[2] : line);
    return text ? [{ timestamp: match ? timestamp(parseClock(match[1])) : "", text }] : [];
  });
}

function parseCaption(raw, filePath) {
  const extension = path.extname(filePath).toLowerCase();
  if (extension === ".json3") return parseJson3(raw);
  if ([".vtt", ".srt", ".ttml", ".srv1", ".srv2", ".srv3"].includes(extension)) return parseTimedSubtitle(raw);
  return parsePlainText(raw);
}

function excerpt(text, start, length, radius = 155) {
  return normaliseText(text.slice(Math.max(0, start - radius), Math.min(text.length, start + length + radius)));
}

function matchesForText(text, source, captionPath = "", at = "") {
  const matches = [];
  for (const { family, note, regex } of reasonFamilies) {
    regex.lastIndex = 0;
    for (const match of text.matchAll(regex)) {
      matches.push({
        reason_family: family,
        review_note: note,
        source,
        caption_path: captionPath,
        timestamp: at,
        match: match[0],
        excerpt: excerpt(text, match.index, match[0].length),
      });
    }
  }
  return matches;
}

function safeCaptionPath(linkedPath) {
  const candidate = path.resolve(auditDir, asText(linkedPath));
  return candidate === auditDir || candidate.startsWith(`${auditDir}${path.sep}`) ? candidate : "";
}

function markdownCell(value) {
  return asText(value).replaceAll("|", "\\|").replaceAll("\n", " ");
}

function parseTsv(raw) {
  const lines = asText(raw).replace(/\r/g, "").split("\n").filter(Boolean);
  if (!lines.length) return [];
  const headers = lines[0].split("\t");
  return lines.slice(1).map((line) => Object.fromEntries(
    line.split("\t").map((value, index) => [headers[index], value]),
  ));
}

function channelIdsFromGapInputs(raw) {
  return new Set([...asText(raw).matchAll(/\/channel\/(UC[A-Za-z0-9_-]{20,})\//g)].map((match) => match[1]));
}

function videoIdsFromInputs(raw) {
  return new Set([...asText(raw).matchAll(/[?&]v=([A-Za-z0-9_-]{11})(?:&|$)/g)].map((match) => match[1]));
}

let catalog;
try {
  catalog = JSON.parse(await fs.readFile(catalogPath, "utf8"));
} catch (error) {
  if (error?.code === "ENOENT") {
    throw new Error(`Missing authenticated catalog: ${catalogPath}. Run build-authenticated-catalog.mjs after placing local exports; this screen does not retrieve content.`);
  }
  throw error;
}
if (!Array.isArray(catalog)) throw new Error("authenticated-video-catalog.json must contain an array.");

const [rootFullRaw, rootScopeRaw, rootDirectRaw, gapFullRaw, discoveryGapRaw, searchResultsRaw] = await Promise.all([
  fs.readFile(rootFullChannelsPath, "utf8"),
  fs.readFile(rootScopePath, "utf8"),
  fs.readFile(rootDirectInputsPath, "utf8"),
  fs.readFile(gapFullInputsPath, "utf8"),
  fs.readFile(discoveryGapPath, "utf8"),
  fs.readFile(searchResultsPath, "utf8"),
]);
const rootFullRows = parseTsv(rootFullRaw);
const rootScopeRows = parseTsv(rootScopeRaw);
const rootScopeById = new Map(rootScopeRows.map((row) => [row.channel_id, row]));
for (const row of rootFullRows) {
  if (!rootScopeById.has(row.channel_id)) {
    throw new Error(`Root scope adjudication is missing ${row.channel_id}`);
  }
}
const rootLocalFullChannelIds = new Set(rootScopeRows
  .filter((row) => row.recommended_lane === "full_channel_local_creator")
  .map((row) => row.channel_id));
const rootDirectOnlyChannelIds = new Set(rootScopeRows
  .filter((row) => row.recommended_lane === "direct_target_videos_only")
  .map((row) => row.channel_id));
const fullChannelIds = new Set([
  ...manualAndZeroEligibleFullChannelIds,
  ...rootLocalFullChannelIds,
  ...channelIdsFromGapInputs(gapFullRaw),
]);
const discoveryGapRows = parseTsv(discoveryGapRaw);
const credibleDiscoveryChannelIds = new Set(discoveryGapRows.map((row) => row.channel_id));
const directOnlyChannelIds = new Set(discoveryGapRows
  .filter((row) => row.recommended_action === "direct_video_only" || discoveryDirectOnlyOverrides.has(row.channel_id))
  .map((row) => row.channel_id));
const searchResults = JSON.parse(searchResultsRaw);
const allowedDirectVideoIds = new Set([
  ...(searchResults.unique_videos ?? [])
  .filter((video) => directOnlyChannelIds.has(asText(video.channel_id)))
  .map((video) => asText(video.id)),
  ...videoIdsFromInputs(rootDirectRaw),
]);

const queue = [];
const readErrors = [];
let taylorExcluded = 0;
let outOfScopeExcluded = 0;
let captionFilesRead = 0;

for (const video of catalog) {
  const channelId = asText(video.channel_id).trim();
  const identity = `${asText(video.channel)} ${asText(video.title)}`;
  if (excludedTaylorChannelIds.has(channelId) || excludedTaylorIdentity.test(identity)) {
    taylorExcluded += 1;
    continue;
  }
  const isScopedFullChannel = fullChannelIds.has(channelId);
  const isScopedDirectVideo = allowedDirectVideoIds.has(asText(video.id))
    && (
      (credibleDiscoveryChannelIds.has(channelId) && directOnlyChannelIds.has(channelId))
      || rootDirectOnlyChannelIds.has(channelId)
    );
  if (!isScopedFullChannel && !isScopedDirectVideo) {
    outOfScopeExcluded += 1;
    continue;
  }

  const matches = [
    ...matchesForText(asText(video.title), "title"),
    ...matchesForText(asText(video.description), "description"),
  ];
  const captionPaths = Array.isArray(video.caption_file_paths) ? video.caption_file_paths : [];
  for (const linkedPath of captionPaths) {
    const resolved = safeCaptionPath(linkedPath);
    if (!resolved) {
      readErrors.push({ id: video.id, caption_path: linkedPath, error: "Skipped path outside audit directory" });
      continue;
    }
    try {
      const raw = await fs.readFile(resolved, "utf8");
      captionFilesRead += 1;
      for (const row of parseCaption(raw, resolved)) {
        matches.push(...matchesForText(row.text, "caption", linkedPath, row.timestamp));
      }
    } catch (error) {
      readErrors.push({ id: video.id, caption_path: linkedPath, error: asText(error?.message || error) });
    }
  }
  if (!matches.length) continue;

  const grouped = Object.groupBy(matches, (match) => match.reason_family);
  queue.push({
    id: video.id,
    url: video.url,
    title: video.title,
    upload_date: video.upload_date,
    channel: video.channel,
    channel_id: channelId,
    content_type: video.content_type,
    duration: video.duration,
    sources: video.sources ?? [],
    caption_file_paths: captionPaths,
    reason_families: Object.keys(grouped).sort(),
    evidence: Object.fromEntries(Object.entries(grouped)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([family, rows]) => [family, rows.slice(0, 12)])),
  });
}

queue.sort((a, b) => b.reason_families.length - a.reason_families.length
  || asText(a.channel).localeCompare(asText(b.channel))
  || asText(a.upload_date).localeCompare(asText(b.upload_date))
  || asText(a.id).localeCompare(asText(b.id)));

const output = {
  generated_at: new Date().toISOString(),
  banner: "RECALL-ONLY SCREEN: text matches are not compliance findings, violations, or legal conclusions. Confirm context in the actual video (including visual overlays), current profile/direct links, disclosures, and the applicable rule matrix before escalating.",
  input: "authenticated-video-catalog.json",
  videos_in_catalog: catalog.length,
  videos_excluded_as_taylor_defense_in_depth: taylorExcluded,
  videos_excluded_as_out_of_scope_discovery_or_channel_content: outOfScopeExcluded,
  videos_screened_in_scope: catalog.length - taylorExcluded - outOfScopeExcluded,
  caption_files_read: captionFilesRead,
  videos_with_one_or_more_matches: queue.length,
  caption_read_errors: readErrors,
  reason_families: reasonFamilies.map(({ family, note }) => ({ family, note })),
  queue,
};
await fs.writeFile(jsonOutputPath, `${JSON.stringify(output, null, 2)}\n`);

const markdown = [
  "# Authenticated-catalog compliance text review queue",
  "",
  "> **RECALL-ONLY SCREEN — NOT FINDINGS.** These automated text matches are not violations or legal conclusions. Confirm the actual video (including visual overlays), the current channel/profile and direct links, disclosures, factual support, timing, and the compliance matrix before escalating.",
  "",
  `- Catalog videos screened: **${catalog.length}**`,
  `- Defense-in-depth Taylor exclusions: **${taylorExcluded}**`,
  `- Out-of-scope discovery/channel-content exclusions: **${outOfScopeExcluded}**`,
  `- In-scope videos actually text-screened: **${catalog.length - taylorExcluded - outOfScopeExcluded}**`,
  `- Caption files read: **${captionFilesRead}**`,
  `- Videos with at least one review cue: **${queue.length}**`,
  `- Caption read/path errors: **${readErrors.length}**`,
  "",
  "| Date | Channel | Video | Review reason families | Caption files |",
  "|---|---|---|---|---|",
  ...queue.map((item) => `| ${markdownCell(item.upload_date)} | ${markdownCell(item.channel)} | [${markdownCell(item.title)}](${item.url}) | ${item.reason_families.join(", ")} | ${item.caption_file_paths.length} |`),
  "",
  "## Review notes by reason family",
  "",
  ...reasonFamilies.map(({ family, note }) => `- **${family}:** ${note}`),
  "",
  "## Caption read/path errors",
  "",
  ...(readErrors.length ? readErrors.map((row) => `- ${row.id}: \`${row.caption_path}\` — ${markdownCell(row.error)}`) : ["- None."]),
  "",
].join("\n");
await fs.writeFile(markdownOutputPath, markdown);
process.stdout.write(`authenticated_review_queue=${queue.length} caption_errors=${readErrors.length}\n`);
