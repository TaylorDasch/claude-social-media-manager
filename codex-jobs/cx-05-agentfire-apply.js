(function () {
  const commuteUrl = "https://templetxhomes.net/neighborhoods-near-bsw-by-commute/";
  const physicianUrl = "https://templetxhomes.net/physician-mortgage-loans-central-texas/";

  const report = {
    startedAt: new Date().toISOString(),
    editorSaves: [],
    metaSaves: [],
    redirectSaves: [],
    changes: [],
    skipped: [],
    errors: []
  };

  function xhr(method, url, body, headers) {
    const req = new XMLHttpRequest();
    req.open(method, url, false);
    if (headers) {
      Object.keys(headers).forEach((key) => req.setRequestHeader(key, headers[key]));
    }
    req.send(body || null);
    return {
      status: req.status,
      url: req.responseURL || url,
      text: req.responseText || ""
    };
  }

  function count(text, needle) {
    if (!needle) return 0;
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

  function extractJsonVar(html, name) {
    const marker = "var " + name + " = ";
    const start = html.indexOf(marker);
    if (start < 0) throw new Error("Missing " + name);
    let i = start + marker.length;
    while (/\s/.test(html[i])) i++;
    const first = html[i];
    if (first !== "{") throw new Error("Expected object for " + name);
    let depth = 0;
    let inString = false;
    let escape = false;
    for (; i < html.length; i++) {
      const ch = html[i];
      if (inString) {
        if (escape) {
          escape = false;
        } else if (ch === "\\") {
          escape = true;
        } else if (ch === '"') {
          inString = false;
        }
        continue;
      }
      if (ch === '"') inString = true;
      if (ch === "{") depth++;
      if (ch === "}") {
        depth--;
        if (depth === 0) {
          return JSON.parse(html.slice(start + marker.length, i + 1));
        }
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
    const body = JSON.stringify({ element_id: "spark_page", values });
    const saved = xhr("POST", "/wp-json/agentfire/v1/spark-editor/page/" + postId, body, {
      "Content-Type": "application/json",
      "X-WP-Nonce": nonce
    });
    if (saved.status < 200 || saved.status >= 300) {
      throw new Error(page + " editor save failed: " + saved.status + " " + saved.text.slice(0, 300));
    }
    report.editorSaves.push({ page, postId, status: saved.status, response: saved.text.slice(0, 300) });
  }

  function submitMeta(page, postId, title, description) {
    const edit = xhr("GET", "/wp-admin/post.php?post=" + postId + "&action=edit");
    if (edit.status !== 200) throw new Error(page + " post edit GET failed: " + edit.status);
    const doc = new DOMParser().parseFromString(edit.text, "text/html");
    const form = doc.querySelector("form#post");
    if (!form) throw new Error(page + " form#post missing");
    const oldTitle = form.querySelector("[name='yoast_wpseo_title']");
    const oldDesc = form.querySelector("[name='yoast_wpseo_metadesc']");
    if (!oldTitle || !oldDesc) throw new Error(page + " Yoast fields missing");
    report.changes.push({
      page,
      field: "meta title",
      before: oldTitle.value,
      after: title,
      count: 1
    });
    report.changes.push({
      page,
      field: "meta description",
      before: oldDesc.value,
      after: description,
      count: 1
    });
    oldTitle.value = title;
    oldDesc.value = description;
    const data = new FormData(form);
    data.set("yoast_wpseo_title", title);
    data.set("yoast_wpseo_metadesc", description);
    data.set("action", "editpost");
    data.set("originalaction", "editpost");
    data.set("post_ID", String(postId));
    const saved = xhr("POST", "/wp-admin/post.php", data);
    if (saved.status < 200 || saved.status >= 400) {
      throw new Error(page + " meta save failed: " + saved.status + " " + saved.text.slice(0, 300));
    }
    report.metaSaves.push({ page, postId, status: saved.status, url: saved.url });
  }

  function submitRedirect(action, id, from, to, title) {
    const url = "/wp-admin/admin.php?page=redirect-manager&action=" + action + (id ? "&id=" + id : "") + "&category=default";
    const edit = xhr("GET", url);
    if (edit.status !== 200) throw new Error("redirect " + action + " GET failed: " + edit.status);
    const doc = new DOMParser().parseFromString(edit.text, "text/html");
    const form = Array.from(doc.querySelectorAll("form")).find((candidate) => candidate.querySelector("[name='from']") && candidate.querySelector("[name='to']"));
    if (!form) throw new Error("redirect " + action + " form missing");
    const data = new FormData(form);
    const beforeFrom = data.get("from") || "";
    const beforeTo = data.get("to") || "";
    data.set("type", "301");
    data.set("from", from);
    data.set("to", to);
    data.set("title", title || "");
    data.set("category", "default");
    data.set("action", action);
    if (id) data.set("id", String(id));
    report.changes.push({
      page: "Redirect Manager",
      field: action === "add" ? "add 301" : "update 301",
      before: (beforeFrom || from) + " -> " + beforeTo,
      after: from + " -> " + to,
      count: 1
    });
    const saved = xhr("POST", url, data);
    if (saved.status < 200 || saved.status >= 400) {
      throw new Error("redirect " + action + " save failed: " + saved.status + " " + saved.text.slice(0, 300));
    }
    report.redirectSaves.push({ action, id: id || null, from, to, status: saved.status, url: saved.url });
  }

  function repointRetiredLinks(page, text) {
    const replacements = [
      ["https://templetxhomes.net/best-neighborhoods-bsw/", commuteUrl],
      ["/best-neighborhoods-bsw/", "/neighborhoods-near-bsw-by-commute/"],
      ["https://templetxhomes.net/best-neighborhoods-baylor-scott-white-temple-tx/", commuteUrl],
      ["/best-neighborhoods-baylor-scott-white-temple-tx/", "/neighborhoods-near-bsw-by-commute/"],
      ["https://templetxhomes.net/best-neighborhoods-baylor-scott-white/", commuteUrl],
      ["/best-neighborhoods-baylor-scott-white/", "/neighborhoods-near-bsw-by-commute/"]
    ];
    replacements.forEach(([before, after]) => {
      text = replaceAll(page, "internal links", text, before, after);
    });
    return text;
  }

  function mutateMatchDay(text) {
    const page = "/match-day-2026-bsw-housing-timeline/";
    text = replaceAll(page, "body", text, "Match Day is March 17, 2026.", "Match Day is March 20, 2026.");
    text = replaceAll(page, "body", text, '<div class="md-hero__count-num">$255K</div>', '<div class="md-hero__count-num">~$274K</div>');
    text = replaceAll(page, "body", text, "Temple’s median home price of $255K", "Temple’s median home price of ~$274K (median, MLS May 2026)");
    text = replaceAll(page, "body", text, "Temple median home: $255K vs Austin $525K+", "Temple median home: ~$274K (median, MLS May 2026) vs Austin $525K+");
    text = replaceAll(page, "body", text, "Buy ($255K, 0% Down)", "Buy (~$274K, 0% Down)");
    text = replaceAll(page, "body", text, "3+ year categorical residency", "4–7 year residency or fellowship-to-attending path");
    text = replaceAll(page, "body", text, "Buying makes more sense for a 3+ year program or a household likely to stay in Central Texas.", "Buying usually makes more sense for a 4–7 year program or a household likely to stay in Central Texas. A 3-year program is a genuine toss-up; run the numbers against your cash reserve and exit plan.");
    text = replaceAll(page, "body", text, "if your program is 3+ years, buy. If it’s a preliminary year, rent the cheapest apartment you can tolerate and save your cash.", "if your program is 1–2 years, rent. If it is 3 years, run the numbers carefully. If it is 4–7 years or a fellowship-to-attending path, buying usually wins.");
    text = replaceAll(page, "body", text, "Yes, if your training program is 3+ years. Temple’s median home price is $255K.", "Often, if your training program is 4–7 years. A 3-year program is a toss-up, and a 1–2 year prelim usually points to renting. Temple’s median home price is ~$274K (median, MLS May 2026).");
    text = replaceAll(page, "body", text, "A physician loan at 0% down, 6.5% rate on a $255K home runs approximately $2,100/month", "A physician loan at 0% down, using a May 2026 rate estimate on a ~$274K home, runs approximately $2,100+/month");
    text = replaceAll(page, "body", text, "Physician loans let you close with 0% down using only your signed BSW contract.", '<a href="' + physicianUrl + '">Physician mortgage loans</a> may let eligible borrowers close with 0% down using a signed BSW contract, depending on lender terms.');
    text = replaceAll(page, "body", text, "Bell County’s effective rate is 2.18%. On a $300K home, that’s $6,540/year ($545/month) in your escrow payment.", "A rough planning number is about 2% of value, but the actual bill varies by parcel, district, exemptions, and appraisal. Verify the address at Bell CAD before you trust a calculator.");
    text = replaceAll(page, "body", text, "Bell County’s effective property tax rate averages 2.18%, ranging from 1.74% to 2.4% depending on location and district. On a $255K home, expect $5,559/year ($463/month in escrow). On a $350K home: $7,630/year ($636/month).", "Use roughly 2% of assessed value as a planning number, then verify the parcel at Bell CAD because city, ISD, county, college district, exemptions, and appraisal all change the bill.");
    text = replaceAll(page, "body", text, "Only profitable if you’ve owned 3+ years.", "Usually strongest if you have owned 4+ years; a 3-year hold is a toss-up.");
    text = repointRetiredLinks(page, text);
    return text;
  }

  function mutateHub(text) {
    const page = "/baylor-scott-white-relocation/";
    text = replaceAll(page, "body", text, "how physician loans work", 'how <a href="' + physicianUrl + '">physician mortgage loans</a> work');
    text = replaceAll(page, "body", text, '<div class="bh-glance-item-value">~$250K</div>', '<div class="bh-glance-item-value">~$274K</div>');
    text = replaceAll(page, "body", text, "Median home prices sit around <strong>$250,000</strong>", "Median home prices sit around <strong>~$274,000 (MLS May 2026)</strong>");
    text = replaceAll(page, "body", text, "Median home price: ~$250,000 (Q1 2026)", "Median home price: ~$274,000 (MLS May 2026)");
    text = replaceAll(page, "body", text, "median home price around $250,000", "median home price around ~$274,000 (MLS May 2026)");
    text = replaceAll(page, "body", text, "Property tax rate: 2.2–2.5% (Bell County)", "Property tax: roughly 2% of value (verify your parcel at Bell CAD)");
    text = replaceAll(page, "body", text, "property taxes run <strong>2.2% to 2.5%</strong> in Bell County", "use roughly 2% of value as a planning number in Bell County");
    text = replaceAll(page, "body", text, "Temple's median home price is $250,000–$300,000, compared to $500,000–$600,000+ in Austin for comparable homes.", "Temple's median home price is about ~$274,000 (MLS May 2026), compared to $500,000–$600,000+ in Austin for comparable homes.");
    text = replaceAll(page, "body", text, "turn-key", "move-in ready");
    text = repointRetiredLinks(page, text);
    return text;
  }

  function mutateChildcare(text) {
    const page = "/bsw-temple-childcare-daycare-guide/";
    const scopedClaim = "At the Temple campus, BSW does not run a dedicated on-site employee daycare (its on-site/Bright Horizons childcare is at the Fort Worth campus); BSW does offer childcare benefits system-wide — confirm Temple specifics with HR.";
    text = replaceAll(page, "body", text, "BSW does not operate an on-site daycare facility at the Temple campus. However, BSW provides a Dependent Care Flexible Spending Account (DC-FSA) through Optum Bank with a 2026 limit of $7,500 per household — a 50% increase from the prior $5,000 cap. This allows employees to pay for eligible childcare expenses with pre-tax dollars, saving up to $2,400/year at the 32% tax bracket.", scopedClaim);
    text = replaceAll(page, "body", text, "BSW does not operate an on-site daycare. However, BSW provides a Dependent Care FSA through Optum Bank with a 2026 limit of $7,500 per household, allowing employees to pay childcare expenses with pre-tax dollars and save up to $2,400/year.", scopedClaim);
    text = replaceAll(page, "body", text, "The infant care waitlist in Temple is 3–15 months at most centers", "The estimated infant care waitlist in Temple is 3–15 months at most centers");
    text = replaceAll(page, "body", text, "Standard infant waitlists in Temple range from 3 to 15 months.", "Estimated standard infant waitlists in Temple range from 3 to 15 months.");
    text = repointRetiredLinks(page, text);
    return text;
  }

  function mutatePhysician(text) {
    const page = "/physician-mortgage-loans-central-texas/";
    text = replaceAll(page, "body", text, '<div class="pm-hero__stat-num">$260K</div>', '<div class="pm-hero__stat-num">~$274K</div>');
    text = replaceAll(page, "body", text, "With Temple's median home price at $255–$260K", "With Temple's median home price at ~$274K (MLS May 2026)");
    text = replaceAll(page, "body", text, "Temple median $255K vs Austin $525K+", "Temple median ~$274K (MLS May 2026) vs Austin $525K+");
    text = replaceAll(page, "body", text, "At Temple’s $255K median", "At Temple’s ~$274K (MLS May 2026) median");
    text = replaceAll(page, "body", text, '<div class="pm-savings__col-num">$255K</div>', '<div class="pm-savings__col-num">~$274K</div>');
    text = replaceAll(page, "body", text, "where median home prices are $255K", "where median home prices are around ~$274K (MLS May 2026)");
    text = replaceAll(page, "body", text, "A $255K home with 0% down at 6.75%", "A ~$274K home with 0% down using a May 2026 rate estimate");
    text = replaceAll(page, "body", text, "Physician mortgage loans are specialized products that let medical professionals buy homes with 0% down and no private mortgage insurance (PMI), saving $200–$350/month compared to conventional loans.", "Physician mortgage loans are specialized products some lenders offer to qualifying medical professionals, sometimes with 0% down and no private mortgage insurance (PMI); terms, savings, and eligibility vary by lender and borrower profile.");
    text = replaceAll(page, "body", text, "Residents and fellows qualify using their signed employment contract, even before their start date.", "Some residents and fellows may qualify using their signed employment contract before their start date.");
    text = replaceAll(page, "body", text, "BSW PGY-1 stipend ($70,993) qualifies for $250K–$300K at 0% down in Temple", "A BSW PGY-1 stipend ($70,993) may qualify for $250K–$300K at 0% down in Temple, depending on lender terms");
    text = replaceAll(page, "body", text, "can qualify for 0% down homeownership on a single resident stipend", "may be able to qualify for 0% down homeownership on a single resident stipend, depending on lender terms");
    text = replaceAll(page, "body", text, "Match Day is March 17, 2026.", "Match Day is March 20, 2026.");
    text = replaceAll(page, "body", text, "That’s 106 days to secure financing", "That’s 103 days to secure financing");
    text = replaceAll(page, "body", text, "March 17 — Day 0", "March 20 — Day 0");
    text = replaceAll(page, "body", text, "You have 106 days until July 1.", "You have 103 days until July 1.");
    text = replaceAll(page, "body", text, "March 20–25 — Days 3–8", "March 20–25 — Days 0–5");
    text = replaceAll(page, "body", text, "March 25 – April 5 — Days 8–19", "March 25 – April 5 — Days 5–16");
    text = replaceAll(page, "body", text, "April 5–May 10 — Days 19–54", "April 5–May 10 — Days 16–51");
    text = replaceAll(page, "body", text, "May 10–June 20 — Days 54–95", "May 10–June 20 — Days 51–92");
    text = replaceAll(page, "body", text, "June 25–30 — Days 100–106", "June 25–30 — Days 97–102");
    text = replaceAll(page, "body", text, "Effective rate: ~2.18%. On a $300K home, that’s $6,540/year ($545/month).", "Use roughly 2% of assessed value as a planning number, then verify the parcel at Bell CAD because city, ISD, county, college district, exemptions, and appraisal all change the bill.");
    text = replaceAll(page, "body", text, "The math favors buying in Temple for residencies of 3+ years.", "The math usually favors buying in Temple for 4–7 year residencies or fellowship-to-attending paths. A 3-year program is a genuine toss-up; 1–2 year prelim paths usually point to renting.");
    text = replaceFirst(page, "body", text, "</ul> </div> </div> </section>", '</ul><p style="font-size:.78rem;color:var(--pm-slate);margin-top:1rem">Program terms, eligibility, loan availability, and savings vary by lender and borrower profile. Equal Housing Opportunity.</p> </div> </div> </section>');
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
      "Why medical families should start the Temple childcare search before housing: 6–6 daycare hours, waitlists, and shift-friendly options near BSW."
    );
    submitMeta(
      "/physician-mortgage-loans-central-texas/",
      2230,
      "Physician Mortgage Loans in Central Texas | Temple TX",
      "How physician mortgage loans work in Central Texas — the 0%-down, no-PMI options some lenders offer doctors and residents. By Temple agent Taylor Dasch."
    );

    submitRedirect("edit", 88, "/best-neighborhoods-baylor-scott-white-temple-tx/", "/neighborhoods-near-bsw-by-commute/", "");
    submitRedirect("edit", 89, "/best-neighborhoods-baylor-scott-white/", "/neighborhoods-near-bsw-by-commute/", "");
    submitRedirect("add", null, "/best-neighborhoods-bsw/", "/neighborhoods-near-bsw-by-commute/", "");
  } catch (error) {
    report.errors.push({ message: error.message, stack: error.stack });
  }

  report.finishedAt = new Date().toISOString();
  return JSON.stringify(report);
})();
