# LAUNCH CHECKLIST — "Retiring in Temple TX vs Georgetown"
## Living in Temple | Go-live: July 14, 2026

Legend: 🟢 autonomous (Claude can do / technical) · 🟡 GATED (needs Taylor's OK — publish to audience / send) · ⚪ Taylor-only manual step

---

### T-minus (before July 14)
- [ ] ⚪ Confirm the final cut matches the captioned SRT runtime (~10:12) and the chapter timestamps in `chapters.txt`.
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
- [ ] 🟢 Deploy via `tools/rocket_publish.py`, then run `tools/contrast_fix.py audit` — must NOT flag the page BROKEN.
- [ ] 🟢 Verify the live page: video renders, link in description resolves, UTM intact. **Claude will give a go/no-go at deploy time.**

### Distribution (staggered after the long-form is live)
- [ ] 🟡 Short 1 ("The $180K gap") — YT Shorts + TikTok + IG Reels via Postiz, launch day +1.
- [ ] 🟡 Short 2 ("The hospital…") — +3 days.
- [ ] 🟡 Short 3 ("Don't retire in Temple if…") — +5 days.
- [ ] 🟡 Short 4 ("Tax freeze trap") — week 2. (Never 2 Shorts same CT weekday.)
- [ ] 🟡 Temple Insider newsletter (`newsletter-draft.md`) — manual publish in Beehiiv (API is enterprise-gated). Send only after the video is live.
- [ ] 🟡 GBP post tying the video to the retiree hub — ready-to-paste draft in `gbp-post-draft.md` (fits the "Neighborhood Guide / Expertise Tip" rotation).
- [ ] 🟡 (Optional) Spanish cut of the strongest Short (Short 1 "$180K gap" or Short 2 "hospital"), or a Spanish caption track on the long-form — Central TX Hispanic-buyer reach. Keep numbers/claims identical; re-run banned-word + lane checks on the translated copy.

### Attribution (web AND phone/text/DM)
- [ ] 🟢 Confirm UTM tags fire: YouTube → `utm_medium=description`; newsletter → `utm_medium=email`; GBP → `utm_source=gbp`. Watch GA4 + Daschboard for inbound from `retiring-in-temple-tx`.
- [ ] 🟢 **Create a Daschboard/FUB lead source tag for this video** (e.g. `YT-Retiring-Temple-vs-Georgetown`). The video's primary CTA is phone/text/DM (254-718-4249, "comment/DM RETIRE") — those leads carry NO UTM, so without a manual source tag they land untagged and the launch can't prove ROI on its core conversion path. Intake habit: when a call/text/DM mentions the retiree or Georgetown video, tag the contact with that source. Manual-tag warm inbound only — no auto-FUB push of cold/public-record contacts (standing rule).

---

### Gate summary (what needs Taylor's explicit OK)
1. Publishing the video itself (Taylor uploads) and pinned comment.
2. Publishing the 4 Shorts to social audiences.
3. Sending the Temple Insider newsletter.
Everything technical (page embed, schema, data refresh, deploy) is autonomous — Claude ships and states a go/no-go on July 14. The VIDEO_ID blocker is cleared (`lgupQUgJcvo` wired into all page assets); the page deploy waits only for the video to flip public on July 14.
