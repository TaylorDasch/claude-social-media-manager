# LAUNCH CHECKLIST — "Retiring in Temple TX vs Georgetown"
## Living in Temple | Go-live: July 14, 2026

Legend: 🟢 autonomous (Claude can do / technical) · 🟡 GATED (needs Taylor's OK — publish to audience / send) · ⚪ Taylor-only manual step

---

### T-minus (before July 14)
- [ ] ⚪ Confirm the final cut matches the captioned SRT runtime (~10:12) and the chapter timestamps in `chapters.txt`.
- [ ] ⚪ **FACT CHECK — stop-ship:** replace or visibly correct “your taxes are frozen” at ~3:33. The Texas over-65 benefit is a school-district tax ceiling, not a freeze on the entire property-tax bill.
- [ ] ⚪ **CAPTION CHECK — stop-ship:** use **Olin E. Teague Veterans' Medical Center** and **Salado**; remove “Allen E. Teague” and “Selah.”
- [ ] ⚪ **FAIR-HOUSING CHECK — stop-ship:** recaption/remove “alongside a lot of other retirees” and “Salado is great for retirees.” Describe housing, price, access, and amenities instead of resident demographics.
- [x] ✅ Title SET: **"Retiring in Temple TX: The Honest Georgetown Alternative"** — video scheduled July 14 (ID `lgupQUgJcvo`). Locked; don't A/B below ~1k impressions.
- [ ] ⚪ Send Concept-1 thumbnail to **Pikzels** using the prompt in `thumbnail-brief.md` + Taylor's headshot as face reference. (Backup: Concept 3.)
- [ ] 🟢 Generate the social Shorts cuts (4 scripts ready in `shorts-package.md`) — stage in Postiz as drafts.
- [ ] 🟡 (Optional) **Community-tab teaser** the day before: poll "Retiring in Central TX — Temple or Georgetown?" to warm Living in Temple subscribers and seed first-hour CTR. Skip if the channel hasn't unlocked the community tab.

### Launch day — July 14
- [ ] ⚪ Upload the video to **Living in Temple** (relocation/buyer channel — not Investing in Temple).
- [ ] ⚪ Paste the title + the description from `description-block.md` (chapters already embedded).
- [ ] ⚪ Add the tags from `description-block.md`. Set category, "not made for kids," add to a Temple-relocation playlist.
- [ ] ⚪ Upload the Pikzels thumbnail.
- [ ] ⚪ Post the **pinned first comment** (from `description-block.md`) and pin it.
- [ ] ⚪ **Set end screens** for the last ~20s: (1) Subscribe element, (2) a relevant next video — a "Moving to Temple" / BSW-relocation upload from Living in Temple (never an investor video — lane discipline), (3) optionally a link element to the retiree hub. Add one mid-video card (~5:36 neighborhoods or ~8:43 Salado) to a related Temple video if one exists.
- [ ] ⚪ Keep `comment-replies.md` open for the first 24h — reply to early comments fast (algorithm signal); pin the seed question.
- [x] ✅ **VIDEO_ID acquired: `lgupQUgJcvo`** — already wired into the page embed + schema + comparison block.

### Website amplify (the "written breakdown" the video links to) — 🟢 autonomous, deploy ON July 14 when video is public
- [x] ✅ `video-embed-and-schema.html` + `comparison-h2-block.html` wired with ID `lgupQUgJcvo` — ready.
- [ ] 🟢 Insert the `<section>` + VideoObject schema into the live hub `/retiring-in-temple-tx/` (page 2812), above the AI Answer Box. (See `amplify-spec.md`.)
- [ ] 🟢 Do the July-2026 data refresh on the hub (medians, Form 50-272, "Olin E. Teague," Updated: July 2026 stamp).
- [ ] 🟢 **Recalculate every tax example, table, FAQ, and FAQ schema entry** using the current statewide school exemptions: $140,000 general residence homestead + $60,000 additional age-65-or-older/disabled exemption. Remove the stale $100,000 + $10,000 figures.
- [ ] 🟢 Update SEO metadata to use **school-tax ceiling**, not a blanket **tax freeze**, and reframe the safety H2 around objective safety/emergency-access evaluation.
- [ ] 🟢 Deploy via `tools/rocket_publish.py`, then run `tools/contrast_fix.py audit` — must NOT flag the page BROKEN.
- [ ] 🟢 Verify the live page: video renders, link in description resolves, UTM intact. **Claude will give a go/no-go at deploy time.**

### Distribution (staggered after the long-form is live)
- [ ] 🟡 Short 1 ("The $180K gap") — YT Shorts + TikTok + IG Reels via Postiz, launch day +1.
- [ ] 🟡 Short 2 ("The hospital…") — +3 days.
- [ ] 🟡 Short 3 ("Don't retire in Temple if…") — +5 days.
- [ ] 🟡 Short 4 ("Tax freeze trap") — week 2. (Never 2 Shorts same CT weekday.)
- [x] ✅ Temple Insider newsletter — APPROVED (2026-07-01), sends July 14 via the launch trigger (Beehiiv; falls back to ready-to-paste + notify if enterprise-gated).
- [x] ✅ GBP post — APPROVED (2026-07-01), auto-publishes July 14 via the launch trigger (draft: `gbp-post-draft.md`).
- [ ] 🟡 (Optional) Spanish cut of the strongest Short (Short 1 "$180K gap" or Short 2 "hospital"), or a Spanish caption track on the long-form — Central TX Hispanic-buyer reach. Keep numbers/claims identical; re-run banned-word + lane checks on the translated copy.

### Attribution (web AND phone/text/DM)
- [ ] 🟢 Confirm UTM tags fire: YouTube → `utm_medium=description`; newsletter → `utm_medium=email`; GBP → `utm_source=gbp`. Watch GA4 + Daschboard for inbound from `retiring-in-temple-tx`.
- [ ] 🟢 **Create a Daschboard/FUB lead source tag for this video** (e.g. `YT-Retiring-Temple-vs-Georgetown`). The video's primary CTA is phone/text/DM (254-718-4249, "comment/DM RETIRE") — those leads carry NO UTM, so without a manual source tag they land untagged and the launch can't prove ROI on its core conversion path. Intake habit: when a call/text/DM mentions the retiree or Georgetown video, tag the contact with that source. Manual-tag warm inbound only — no auto-FUB push of cold/public-record contacts (standing rule).

---

### ⚙️ Automation scheduled (2026-07-01)
Scheduled task **`retiring-temple-july14-launch`** (`~/.claude/scheduled-tasks/…`) fires **July 14, 8:00 PM CT**: verifies the video is public → deploys the hub embed + comparison H2 + July-2026 data refresh → publishes the GBP post → sends the Temple Insider newsletter → reports go/no-go + what needs a manual click. **Caveat:** it runs only while the Claude app is open; if closed at 8pm CT it runs on next launch. (The `create_trigger` cloud service was 404'ing, so this uses the local scheduled-tasks runner instead.)

### Gate summary (updated 2026-07-01)
- ✅ **AUTO on July 14 via the launch trigger** (Taylor pre-approved): page deploy (embed + comparison H2 + data refresh), **GBP post**, and **Temple Insider newsletter**.
- ⚪ **Still Taylor-manual at upload:** the video going public (already scheduled), the pinned first comment, end screens/cards, and the 4 Shorts to social.
- The VIDEO_ID blocker is cleared (`lgupQUgJcvo` wired into all page assets). The trigger verifies the video is public before deploying; it will not embed a private video.
