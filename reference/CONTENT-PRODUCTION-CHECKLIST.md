# CONTENT PRODUCTION CHECKLIST — Per Video
## Reusable checklist Claude references when building daily plans
## Nothing falls through the cracks

---

## PRE-PRODUCTION

- [ ] Topic selected from priority queue (check social-media-output.txt or AEO-GAP-VIDEOS.md)
- [ ] **Pillar tag declared** (1 Relocation / 2 Market Update / 3 Neighborhood Deep Dive / 4 Home Tour / 5 Lifestyle & Community — see YOUTUBE-GROWTH-PLAYBOOK §5 Pillars)
- [ ] Pillar rotation check — last video NOT same pillar (Gate 12)
- [ ] Script formula chosen from VIDEO-SCRIPT-FORMULAS.md
- [ ] **Hook drafted with open-loop tease** — one specific curiosity promise saved for later (see Master Script Architecture §1)
- [ ] **Early CTA variant chosen** — canonical "private 1:1" or persona-specific from Master Script Architecture §2
- [ ] **End-screen handoff video chosen** — specific next-video target, not generic (see YOUTUBE-GROWTH-PLAYBOOK § End Screen Handoff)
- [ ] Key data points pulled from TEMPLE-TX-DATA-VAULT.md
- [ ] Script/outline written (or generated via /produce)
- [ ] Shot list prepared (which setups needed: desk, drive-through, walk-and-talk?)
- [ ] B-roll needs identified (MLS photos, Google Maps, spreadsheets) — keep light, raw > polished
- [ ] Lead magnet selected from LEAD-MAGNET-MATRIX.md (match to persona)
- [ ] Matching website page identified (check VIDEO-TO-PAGE-MAP.md)

---

## PRODUCTION (Tuesday = Film Day)

- [ ] A-roll filmed per script
- [ ] B-roll captured (property photos, driving footage, location shots)
- [ ] Extra footage for TikTok/Shorts (vertical clips, face-to-camera hooks)
- [ ] Audio quality verified on playback
- [ ] Change shirt/jacket between videos if batch filming

---

## POST-PRODUCTION

- [ ] Edited with visual change every 15-20 seconds (long) or 7 seconds (short) — but don't over-polish (raw > polished per 2026 algorithm rules)
- [ ] Captions added (CapCut auto → manual cleanup for proper nouns)
- [ ] **3 thumbnails created** for YouTube built-in A/B test (Studio → Content → Test & Compare). Follow Thumbnail Anatomy in YOUTUBE-GROWTH-PLAYBOOK: face ~33%, 3-5 words, mobile-readable, text ≠ title, high contrast.
- [ ] Title follows proven formula from VIDEO-SCRIPT-FORMULAS.md
- [ ] Description follows 7-section structure from YOUTUBE-GROWTH-PLAYBOOK.md
- [ ] Entity declaration in first 3 lines of description
- [ ] **Early CTA verified at 0:30–1:00 position** in final cut (not just buried at end). On-screen lower-third overlay matches verbal CTA.
- [ ] Tags added (10-15, mix of broad + hyper-local)
- [ ] Pinned comment written with persona-matched lead magnet from LEAD-MAGNET-MATRIX.md
- [ ] **End-screen verbal handoff scripted into last 20–30 seconds** (curiosity tease into specific next video — see YOUTUBE-GROWTH-PLAYBOOK § End Screen Handoff). NOT generic "like and subscribe."
- [ ] End screen element configured in YouTube Studio (subscribe + specific recommended next video, not auto-pick)
- [ ] Cards added at relevant topic mentions (never in first 30 seconds)
- [ ] Chapter markers added to description (question-format titles)
- [ ] **Retention curve checked at 7-day mark** — AVD ≥30% target. Document drops for next-video correction (see YOUTUBE-GROWTH-PLAYBOOK § Watch Time Benchmarks).
- [ ] **Thumbnail A/B winner logged** in `data/thumbnail-winners.csv` after 7-14 days (variant pattern + CTR delta + pillar).

---

## DEPLOYMENT

- [ ] Uploaded to correct YouTube channel (Living in Temple vs Investing in Temple)
- [ ] Auto-transcript downloaded from YouTube Studio (~30 min after upload)
- [ ] Transcript cleaned (proper nouns, neighborhood names, numbers corrected)
- [ ] Run /transcript-to-blog skill on cleaned transcript
- [ ] Blog page deployed to AgentFire with video embedded
- [ ] VideoObject schema added to page
- [ ] FAQPage schema added/updated on page
- [ ] Article schema added (if new blog post)
- [ ] AgentFire cache cleared
- [ ] Google Search Console indexing requested for new page
- [ ] GMB post published same day (30-sec clip or text post with link)
- [ ] UTM parameters on all links in description (see CONTENT-TO-LEAD-ATTRIBUTION.md)

---

## REPURPOSING (Run /repurpose Skill)

- [ ] 1-2 Shorts/Reels clips identified and cut from long-form
- [ ] Shorts uploaded 24-48 hours AFTER long-form (gives long-form head start)
- [ ] TikTok version posted (geo-tagged, keywords in first 3 seconds spoken + on-screen)
- [ ] TikTok caption: long-form, keyword-dense, DM keyword CTA
- [ ] YouTube Community post scheduled between this video and next
- [ ] BiggerPockets engagement (if investor topic — genuine reply with data, link to blog not video)
- [ ] LinkedIn carousel outline (if investor or BSW topic)

---

## ATTRIBUTION

- [ ] UTM parameters correct on all outbound links
- [ ] Hidden form fields correct on matching website page (source_url, asset_name, persona_rail)
- [ ] FUB source tag verified for this page's forms
- [ ] Lead magnet download linked and working

---

## WEEKLY RHYTHM (When to do what)

| Day | Primary Task |
|-----|-------------|
| Monday | Select topics, write scripts, prep shot list, pull Deal of the Week property |
| Tuesday | FILM: primary video + TikTok clips + B-roll |
| Wednesday | Edit, upload, deploy transcript + page + schema |
| Thursday | Community post, BP engagement, source next week's deal |
| Friday | Pipeline review, attribution check, plan next week |
| Saturday | Page audits, schema validation, freshness scanner |
| Sunday | TikTok review, content calendar, set Monday queue |
