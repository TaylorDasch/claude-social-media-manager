(function () {
  const physicianUrl = "https://templetxhomes.net/physician-mortgage-loans-central-texas/";
  const report = {
    startedAt: new Date().toISOString(),
    editorSaves: [],
    metaSaves: [],
    changes: [],
    skipped: [],
    errors: []
  };

  function xhr(method, url, body, headers) {
    const req = new XMLHttpRequest();
    req.open(method, url, false);
    if (headers) Object.keys(headers).forEach((key) => req.setRequestHeader(key, headers[key]));
    req.send(body || null);
    return { status: req.status, url: req.responseURL || url, text: req.responseText || "" };
  }

  function count(text, needle) {
    return text.split(needle).length - 1;
  }

  function replaceAll(page, field, text, before, after) {
    const found = count(text, before);
    if (!found) {
      report.skipped.push({ page, field, before, reason: "target text not found" });
      return text;
    }
    report.changes.push({ page, field, before, after, count: found });
    return text.split(before).join(after);
  }

  function replaceFirst(page, field, text, before, after) {
    const idx = text.indexOf(before);
    if (idx < 0) {
      report.skipped.push({ page, field, before, reason: "target text not found" });
      return text;
    }
    report.changes.push({ page, field, before, after, count: 1 });
    return text.slice(0, idx) + after + text.slice(idx + before.length);
  }

  function fixMojibake(page, field, text) {
    const pairs = [
      ["\u201a\u00c4\u00ec", "\u2013"],
      ["\u201a\u00c4\u00ee", "\u2014"],
      ["\u201a\u00c4\u00f4", "\u2019"],
      ["\u201a\u00c4\u00fa", "\u201c"],
      ["\u201a\u00c4\u00f9", "\u201d"]
    ];
    pairs.forEach(([before, after]) => {
      text = replaceAll(page, field + " encoding", text, before, after);
    });
    return text;
  }

  function extractJsonVar(html, name) {
    const marker = "var " + name + " = ";
    const start = html.indexOf(marker);
    if (start < 0) throw new Error("Missing " + name);
    let i = start + marker.length;
    while (/\s/.test(html[i])) i++;
    if (html[i] !== "{") throw new Error("Expected object for " + name);
    let depth = 0;
    let inString = false;
    let escape = false;
    for (; i < html.length; i++) {
      const ch = html[i];
      if (inString) {
        if (escape) escape = false;
        else if (ch === "\\") escape = true;
        else if (ch === '"') inString = false;
        continue;
      }
      if (ch === '"') inString = true;
      if (ch === "{") depth++;
      if (ch === "}") {
        depth--;
        if (depth === 0) return JSON.parse(html.slice(start + marker.length, i + 1));
      }
    }
    throw new Error("Unclosed object for " + name);
  }

  function extractNonce(html) {
    const match = html.match(/var afe_wp_nonce = '([^']+)'/);
    if (!match) throw new Error("Missing afe_wp_nonce");
    return match[1];
  }

  function getRaw(values) {
    const item = (values.items || []).find((candidate) => {
      return candidate && candidate.id === "raw_content" && candidate.values && candidate.values.code && candidate.values.code.twig;
    });
    if (!item) throw new Error("Missing raw_content twig");
    return item;
  }

  function saveEditor(page, postId, mutate) {
    const editor = xhr("GET", "/wp-admin/admin.php?page=agentfire-editor&post_id=" + postId);
    if (editor.status !== 200) throw new Error(page + " editor GET failed: " + editor.status);
    const values = extractJsonVar(editor.text, "afe_values");
    const nonce = extractNonce(editor.text);
    const rawItem = getRaw(values);
    const before = rawItem.values.code.twig;
    const after = mutate(before);
    if (after === before) {
      report.editorSaves.push({ page, postId, status: "unchanged" });
      return;
    }
    rawItem.values.code.twig = after;
    const saved = xhr("POST", "/wp-json/agentfire/v1/spark-editor/page/" + postId, JSON.stringify({ element_id: "spark_page", values }), {
      "Content-Type": "application/json",
      "X-WP-Nonce": nonce
    });
    if (saved.status < 200 || saved.status >= 300) throw new Error(page + " editor save failed: " + saved.status + " " + saved.text.slice(0, 300));
    report.editorSaves.push({ page, postId, status: saved.status });
  }

  function submitMeta(page, postId, title, description) {
    const edit = xhr("GET", "/wp-admin/post.php?post=" + postId + "&action=edit");
    if (edit.status !== 200) throw new Error(page + " post edit GET failed: " + edit.status);
    const doc = new DOMParser().parseFromString(edit.text, "text/html");
    const form = doc.querySelector("form#post");
    if (!form) throw new Error(page + " form#post missing");
    const titleEl = form.querySelector("[name='yoast_wpseo_title']");
    const descEl = form.querySelector("[name='yoast_wpseo_metadesc']");
    if (!titleEl || !descEl) throw new Error(page + " Yoast fields missing");
    const cleanDesc = fixMojibake(page, "meta description", description);
    report.changes.push({ page, field: "meta title", before: titleEl.value, after: title, count: 1 });
    report.changes.push({ page, field: "meta description", before: descEl.value, after: cleanDesc, count: 1 });
    titleEl.value = title;
    descEl.value = cleanDesc;
    const data = new FormData(form);
    data.set("yoast_wpseo_title", title);
    data.set("yoast_wpseo_metadesc", cleanDesc);
    data.set("action", "editpost");
    data.set("originalaction", "editpost");
    data.set("post_ID", String(postId));
    const saved = xhr("POST", "/wp-admin/post.php", data);
    if (saved.status < 200 || saved.status >= 400) throw new Error(page + " meta save failed: " + saved.status);
    report.metaSaves.push({ page, postId, status: saved.status, url: saved.url });
  }

  function mutateMatchDay(text) {
    const page = "/match-day-2026-bsw-housing-timeline/";
    text = fixMojibake(page, "body", text);
    text = replaceAll(page, "body", text, "Temple\u2019s median home price of $255K", "Temple\u2019s median home price of ~$274K (median, MLS May 2026)");
    text = replaceAll(page, "body", text, "if your program is 3+ years, buy. If it\u2019s a preliminary year, rent the cheapest apartment you can tolerate and save your cash.", "if your program is 1\u20132 years, rent. If it is 3 years, run the numbers carefully. If it is 4\u20137 years or a fellowship-to-attending path, buying usually wins.");
    text = replaceAll(page, "body", text, "Yes, if your training program is 3+ years. Temple\u2019s median home price is $255K.", "Often, if your training program is 4\u20137 years. A 3-year program is a toss-up, and a 1\u20132 year prelim usually points to renting. Temple\u2019s median home price is ~$274K (median, MLS May 2026).");
    text = replaceAll(page, "body", text, "Bell County\u2019s effective rate is 2.18%. On a $300K home, that\u2019s $6,540/year ($545/month) in your escrow payment.", "A rough planning number is about 2% of value, but the actual bill varies by parcel, district, exemptions, and appraisal. Verify the address at Bell CAD before you trust a calculator.");
    text = replaceAll(page, "body", text, "Bell County\u2019s effective property tax rate averages 2.18%, ranging from 1.74% to 2.4% depending on location and district. On a $255K home, expect $5,559/year ($463/month in escrow). On a $350K home: $7,630/year ($636/month).", "Use roughly 2% of assessed value as a planning number, then verify the parcel at Bell CAD because city, ISD, county, college district, exemptions, and appraisal all change the bill.");
    text = replaceAll(page, "body", text, "Only profitable if you\u2019ve owned 3+ years.", "Usually strongest if you have owned 4+ years; a 3-year hold is a toss-up.");
    text = replaceAll(page, "body", text, "$15,000\u2013$23,000 in exit costs on a $255K home", "$15,000\u2013$23,000+ in exit costs on a ~$274K home");
    text = replaceAll(page, "body", text, "Rent if your training program is under 3 years. Period.", "Rent for 1\u20132 year prelims; treat 3-year programs as a toss-up.");
    text = replaceAll(page, "body", text, "31 GME programs", "30+ accredited programs");
    return text;
  }

  function mutateHub(text) {
    const page = "/baylor-scott-white-relocation/";
    text = fixMojibake(page, "body", text);
    text = replaceAll(page, "body", text, "Property tax rate: 2.2\u20132.5% (Bell County)", "Property tax: roughly 2% of value (verify your parcel at Bell CAD)");
    text = replaceAll(page, "body", text, "Temple's median home price is $250,000\u2013$300,000, compared to $500,000\u2013$600,000+ in Austin for comparable homes.", "Temple's median home price is about ~$274,000 (MLS May 2026), compared to $500,000\u2013$600,000+ in Austin for comparable homes.");
    return text;
  }

  function mutateChildcare(text) {
    const page = "/bsw-temple-childcare-daycare-guide/";
    const scopedClaim = "At the Temple campus, BSW does not run a dedicated on-site employee daycare (its on-site/Bright Horizons childcare is at the Fort Worth campus); BSW does offer childcare benefits system-wide \u2014 confirm Temple specifics with HR.";
    text = fixMojibake(page, "body", text);
    text = replaceAll(page, "body", text, "BSW does not operate an on-site daycare facility at the Temple campus. However, BSW provides a Dependent Care Flexible Spending Account (DC-FSA) through Optum Bank with a 2026 limit of $7,500 per household \u2014 a 50% increase from the prior $5,000 cap. This allows employees to pay for eligible childcare expenses with pre-tax dollars, saving up to $2,400/year at the 32% tax bracket.", scopedClaim);
    text = replaceAll(page, "body", text, "The infant care waitlist in Temple is 3\u201315 months at most centers", "The estimated infant care waitlist in Temple is 3\u201315 months at most centers");
    return text;
  }

  function mutatePhysician(text) {
    const page = "/physician-mortgage-loans-central-texas/";
    text = fixMojibake(page, "body", text);
    text = replaceAll(page, "body", text, "With Temple's median home price at $255\u2013$260K", "With Temple's median home price at ~$274K (MLS May 2026)");
    text = replaceAll(page, "body", text, "At Temple\u2019s $255K median", "At Temple\u2019s ~$274K (MLS May 2026) median");
    text = replaceAll(page, "body", text, "Physician mortgage loans are specialized products that let medical professionals buy homes with 0% down and no private mortgage insurance (PMI), saving $200\u2013$350/month compared to conventional loans.", "Physician mortgage loans are specialized products some lenders offer to qualifying medical professionals, sometimes with 0% down and no private mortgage insurance (PMI); terms, savings, and eligibility vary by lender and borrower profile.");
    text = replaceAll(page, "body", text, "BSW PGY-1 stipend ($70,993) qualifies for $250K\u2013$300K at 0% down in Temple", "A BSW PGY-1 stipend ($70,993) may qualify for $250K\u2013$300K at 0% down in Temple, depending on lender terms");
    text = replaceAll(page, "body", text, "That\u2019s 106 days to secure financing", "That\u2019s 103 days to secure financing");
    text = replaceAll(page, "body", text, "March 17 \u2014 Day 0", "March 20 \u2014 Day 0");
    text = replaceAll(page, "body", text, "March 20\u201325 \u2014 Days 3\u20138", "March 20\u201325 \u2014 Days 0\u20135");
    text = replaceAll(page, "body", text, "March 25 \u2013 April 5 \u2014 Days 8\u201319", "March 25 \u2013 April 5 \u2014 Days 5\u201316");
    text = replaceAll(page, "body", text, "April 5\u2013May 10 \u2014 Days 19\u201354", "April 5\u2013May 10 \u2014 Days 16\u201351");
    text = replaceAll(page, "body", text, "May 10\u2013June 20 \u2014 Days 54\u201395", "May 10\u2013June 20 \u2014 Days 51\u201392");
    text = replaceAll(page, "body", text, "June 25\u201330 \u2014 Days 100\u2013106", "June 25\u201330 \u2014 Days 97\u2013102");
    text = replaceAll(page, "body", text, "Effective rate: ~2.18%. On a $300K home, that\u2019s $6,540/year ($545/month).", "Use roughly 2% of assessed value as a planning number, then verify the parcel at Bell CAD because city, ISD, county, college district, exemptions, and appraisal all change the bill.");
    text = replaceFirst(page, "body", text, "<li>Temple median ~$274K (MLS May 2026) vs Austin $525K+: physician loan purchasing power is 2x greater here</li></ul>", "<li>Temple median ~$274K (MLS May 2026) vs Austin $525K+: physician loan purchasing power is 2x greater here</li></ul><p style=\"font-size:.78rem;color:var(--pm-slate);margin-top:1rem\">Program terms, eligibility, loan availability, and savings vary by lender and borrower profile. Equal Housing Opportunity.</p>");
    return text;
  }

  try {
    saveEditor("/match-day-2026-bsw-housing-timeline/", 2271, mutateMatchDay);
    saveEditor("/baylor-scott-white-relocation/", 2223, mutateHub);
    saveEditor("/bsw-temple-childcare-daycare-guide/", 3131, mutateChildcare);
    saveEditor("/physician-mortgage-loans-central-texas/", 2230, mutatePhysician);
    submitMeta(
      "/baylor-scott-white-relocation/",
      2223,
      "Baylor Scott & White Temple Relocation Guide (2026)",
      "Relocating to Temple, TX for Baylor Scott & White? Neighborhoods by commute, the buying timeline, and honest tradeoffs from agent Taylor Dasch, EG Realty."
    );
    submitMeta(
      "/bsw-temple-childcare-daycare-guide/",
      3131,
      "BSW Temple Childcare: Shift Hours, Waitlists & Cost (2026)",
      "Why medical families should start the Temple childcare search before housing: 6\u20136 daycare hours, waitlists, and shift-friendly options near BSW."
    );
    submitMeta(
      "/physician-mortgage-loans-central-texas/",
      2230,
      "Physician Mortgage Loans in Central Texas | Temple TX",
      "How physician mortgage loans work in Central Texas \u2014 the 0%-down, no-PMI options some lenders offer doctors and residents. By Temple agent Taylor Dasch."
    );
  } catch (error) {
    report.errors.push({ message: error.message, stack: error.stack });
  }

  report.finishedAt = new Date().toISOString();
  return JSON.stringify(report);
})();
