(function () {
  const report = { startedAt: new Date().toISOString(), editorSaves: [], changes: [], skipped: [], errors: [] };

  function xhr(method, url, body, headers) {
    const req = new XMLHttpRequest();
    req.open(method, url, false);
    if (headers) Object.keys(headers).forEach((key) => req.setRequestHeader(key, headers[key]));
    req.send(body || null);
    return { status: req.status, text: req.responseText || "" };
  }

  function replaceAll(page, text, before, after) {
    const count = text.split(before).length - 1;
    if (!count) {
      report.skipped.push({ page, before, reason: "target text not found" });
      return text;
    }
    report.changes.push({ page, before, after, count });
    return text.split(before).join(after);
  }

  function replaceFirst(page, text, before, after) {
    const idx = text.indexOf(before);
    if (idx < 0) {
      report.skipped.push({ page, before, reason: "target text not found" });
      return text;
    }
    report.changes.push({ page, before, after, count: 1 });
    return text.slice(0, idx) + after + text.slice(idx + before.length);
  }

  function extractJsonVar(html, name) {
    const marker = "var " + name + " = ";
    const start = html.indexOf(marker);
    if (start < 0) throw new Error("Missing " + name);
    let i = start + marker.length;
    while (/\s/.test(html[i])) i++;
    let depth = 0, inString = false, escape = false;
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

  function saveEditor(page, postId, mutate) {
    const editor = xhr("GET", "/wp-admin/admin.php?page=agentfire-editor&post_id=" + postId);
    if (editor.status !== 200) throw new Error(page + " editor GET failed: " + editor.status);
    const values = extractJsonVar(editor.text, "afe_values");
    const nonceMatch = editor.text.match(/var afe_wp_nonce = '([^']+)'/);
    if (!nonceMatch) throw new Error(page + " nonce missing");
    const rawItem = (values.items || []).find((item) => item && item.id === "raw_content" && item.values && item.values.code && item.values.code.twig);
    if (!rawItem) throw new Error(page + " raw_content missing");
    const before = rawItem.values.code.twig;
    const after = mutate(before);
    if (after === before) {
      report.editorSaves.push({ page, postId, status: "unchanged" });
      return;
    }
    rawItem.values.code.twig = after;
    const saved = xhr("POST", "/wp-json/agentfire/v1/spark-editor/page/" + postId, JSON.stringify({ element_id: "spark_page", values }), {
      "Content-Type": "application/json",
      "X-WP-Nonce": nonceMatch[1]
    });
    if (saved.status < 200 || saved.status >= 300) throw new Error(page + " save failed: " + saved.status);
    report.editorSaves.push({ page, postId, status: saved.status });
  }

  function mutateMatch(text) {
    const page = "/match-day-2026-bsw-housing-timeline/";
    text = replaceAll(page, text, "<strong>3-year categorical (IM, FM, Peds):</strong> Break-even. Buying works if you plan to keep the property as a rental. <strong>4\u20137 years (Surgery, Radiology, fellowship track):</strong> Buy. The math overwhelmingly favors ownership.", "<strong>3-year categorical (IM, FM, Peds):</strong> Genuine toss-up. Buying can work if you plan to keep the property as a rental and have reserves. <strong>4\u20137 years (Surgery, Radiology, fellowship track):</strong> Buying usually wins.");
    text = replaceAll(page, text, "On a $255K purchase with 0% down, your mortgage is ~$1,650. At $1,500 rent, you break even while building equity.", "On a ~$274K purchase with 0% down, rerun the current PITI before assuming a rental conversion breaks even.");
    return text;
  }

  function mutateHub(text) {
    const page = "/baylor-scott-white-relocation/";
    text = replaceAll(page, text, "Physician mortgage loans are available locally with <strong>0% down and no PMI</strong>", "Some physician mortgage lenders offer <strong>0% down and no PMI options</strong>");
    text = replaceAll(page, text, "Physician loans: 0% down, no PMI (Extraco, Regions)", "Physician loan options: some lenders offer 0% down/no PMI (verify terms)");
    text = replaceAll(page, text, "Physician mortgage loans exclude student debt from DTI calculations and offer 0% down with no PMI.", "Some physician mortgage programs may exclude student debt from DTI calculations and offer 0% down/no PMI options.");
    text = replaceAll(page, text, "Physician mortgage loans offer 0\u20135% down payment with no PMI, and exclude student loans from debt-to-income calculations.", "Some physician mortgage loans offer 0\u20135% down payment with no PMI and may treat student loans differently in debt-to-income calculations.");
    return text;
  }

  function mutatePhysician(text) {
    const page = "/physician-mortgage-loans-central-texas/";
    text = replaceAll(page, text, "0% down, no PMI on purchases up to $1M at most lenders; up to $1.5M at 5% down", "Some lenders offer 0% down/no PMI options on purchases up to program caps; verify max loan amounts directly");
    text = replaceAll(page, text, "Residents qualify with signed contract 90 days before start date\u2014no W-2 history required", "Some residents may qualify with a signed contract before start date\u2014verify documentation requirements with the lender");
    text = replaceAll(page, text, "Physician loans eliminate this entirely.", "Some physician loan products can eliminate this.");
    text = replaceFirst(page, text, "where medians exceed $525K.</p>", "where medians exceed $525K.</p><p style=\"font-size:.78rem;color:var(--pm-slate);margin-top:1rem\">Program terms, eligibility, loan availability, and savings vary by lender and borrower profile. Equal Housing Opportunity.</p>");
    return text;
  }

  try {
    saveEditor("/match-day-2026-bsw-housing-timeline/", 2271, mutateMatch);
    saveEditor("/baylor-scott-white-relocation/", 2223, mutateHub);
    saveEditor("/physician-mortgage-loans-central-texas/", 2230, mutatePhysician);
  } catch (error) {
    report.errors.push({ message: error.message, stack: error.stack });
  }

  report.finishedAt = new Date().toISOString();
  return JSON.stringify(report);
})();
