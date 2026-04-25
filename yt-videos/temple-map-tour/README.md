# Temple TX Map Tour — Production Package

**Target:** 10-min long-form YouTube video using auto-play 3D Mapbox flythrough as B-roll + voiceover
**Format:** Video #1 in the "New 20" priority list (highest impact potential per research)

---

## What's In This Folder

| File | Purpose |
|---|---|
| `temple-map-tour.html` | Self-contained 3D map flythrough. Auto-plays a 10-minute cinematic tour over Temple with zone labels, price cards, and callouts. Uses Mapbox GL JS v3.8 + satellite-streets + 3D terrain + building extrusions. |
| `voiceover-script.md` | Complete teleprompter-ready script (1,250 words, ~10 min @ 125 wpm). Timings match the HTML animation exactly. |
| `README.md` | This file — the production workflow. |

---

## Step 1: Test the HTML Before Filming

1. Open `temple-map-tour.html` in **Chrome** (Safari sometimes lags on 3D terrain)
2. Wait ~5 seconds for Mapbox to load (you'll see "READY" in the top-right HUD)
3. Click **▶ PLAY TOUR**
4. Watch it through once. Note:
   - Does the camera flythrough match the script timings?
   - Do any neighborhood coordinates look wrong? (The camera should center over the actual neighborhood.)

### If a Neighborhood Coord Is Wrong

Open `temple-map-tour.html` in a text editor. Find the `COORDS` object near the top (line ~148). Each entry is `[longitude, latitude]`. Tweak the numbers. Save. Reload in Chrome.

**Quick reference:** longitude is the first number (always negative for Texas, around -97.3 to -97.5). Latitude is second (around 31.05 to 31.14 for Temple).

---

## Step 2: Prep Your Film Setup

**Two recording paths — pick one:**

### Path A: Voiceover-Only (Fastest)
- You record audio only (phone, lav mic, or USB mic)
- Screen-record the HTML playing in Chrome
- Edit them together in CapCut

### Path B: Face-to-Camera Intro + Voiceover for Map Sections
- Film yourself on camera delivering the HOOK (0:00-0:15) and CTA (9:50-10:00)
- Record voiceover for the 5 zone sections + avoid zones + budget map
- Cut between your face and the map flythrough

**Path B recommended** — your research notes say your face-to-camera shots lift retention on long-form.

---

## Step 3: Screen-Record the Map Tour

### On Mac (built-in, no download needed):

1. Press `Cmd + Shift + 5`
2. Choose **"Record Selected Portion"**
3. Drag selection around the Chrome browser window (just the map, not the tabs)
4. Click **Options** → turn OFF the microphone (you'll add voice in post)
5. Click **Record**
6. Go to the HTML tab. Click **▶ PLAY TOUR**. Let it run to completion (10 min).
7. Press `Cmd + Ctrl + Esc` to stop recording
8. Video saves to Desktop as `.mov`

### Tips for Clean Screen Recording

- **Full-screen the browser** (F11 or green maximize button) — hides tabs and controls
- **Hide the bottom-left controls** after starting: after you click PLAY, click anywhere on the map and press `Cmd + Shift + F` to fullscreen just the map div (or click the gray area to defocus the buttons — they're still visible but less distracting)
- **Better option:** delete the `<div class="controls">` block from the HTML before screen-recording so the play/restart buttons disappear entirely. Save as `temple-map-tour-clean.html` and use that copy for recording.

---

## Step 4: Record the Voiceover

Use `voiceover-script.md` as your teleprompter.

**Best free option:** Open the script on your phone. Use a teleprompter app that scrolls at your reading pace (BIGVU, PromptSmart Lite, or just iOS Notes in large text mode). Read paragraph by paragraph.

**Recording setup:**
- Quiet room (no HVAC, no street noise)
- Lav mic or USB condenser mic — NOT built-in MacBook mic
- Record in **QuickTime** (free) or **Audacity** (free)
- Record one section at a time, pause between sections
- If you fluff a line, pause 3 seconds, re-do the paragraph. Clean cut point for post.

---

## Step 5: Edit in CapCut

1. New project in CapCut
2. Drop in the screen-recorded `.mov` (your map tour)
3. Drop in your voiceover `.m4a` or `.wav` file
4. Align them — the HTML timer is visible in the screen recording, so use it as a reference. At 0:15 on screen = start of the "FRAMEWORK" voiceover section.
5. If you filmed face-to-camera for hook + CTA, cut those in at 0:00-0:15 and 9:50-10:00
6. Add under-dialogue music at **-18dB** (duck when you speak) — use YouTube Audio Library free tracks
7. Add captions via CapCut's auto-caption (retention booster per research)
8. Export at 1080p 60fps, MP4

**Title for YouTube:** `The Complete Temple TX Map Tour — 5 Zones, Real Prices, 3 to Avoid (2026)`

**Thumbnail:** Use your proven formula from the audit — on-location shot of you pointing at something (could be a physical paper map for visual interest), pink/red shirt against sky, curious face, text real estate on one side. Big 3-word text: "TEMPLE MAP TOUR" or "3 ZONES TO AVOID".

---

## Step 6: Upload Optimizations

Per the realtor YouTube research:

- **First 2 lines of description:** value summary + CTA
  > "The 5 zones of Temple TX real estate, real 2026 prices, and 3 zones I'd personally avoid. Free neighborhood map PDF + consult link below."
- **Chapters (copy-paste):**
  ```
  0:00 Hook
  0:15 The Framework
  0:45 Zone 1: West Temple / Belton ISD
  2:15 Zone 2: South Temple
  3:45 Zone 3: North Temple
  5:15 Zone 4: Inner / East Temple
  6:45 Zone 5: Belton-Side
  8:15 3 Zones to Avoid
  9:30 Your Budget Map
  9:50 Free Map PDF + How to Reach Me
  ```
- **Pinned comment:** "Which zone fits your budget? Drop your number below and I'll tell you the 3 neighborhoods that work. Free Temple map: [link]"
- **End screen:** Point to "I Ranked Every Temple Neighborhood Worst to Best" (Video #3 in the New 20) — this builds a playlist pipeline.
- **Tags:** moving to temple tx, temple texas neighborhoods, living in temple tx, temple tx real estate, temple tx map tour, best neighborhoods temple tx, temple tx 2026
- **Add to playlist:** "Living in Temple" + "Map Tours"

---

## Step 7: Cross-Post

1. **Shorts from the tour:** pull 3x 60-second clips — one per zone that performs best — and post as standalone Shorts linking back to the full video.
2. **Blog post on templetxhomes.net:** embed the YouTube video + publish a text version with the same zone breakdown. AEO/SEO play.
3. **Newsletter (Temple Insider):** feature the video in the next issue with a 2-sentence teaser.
4. **Pinned social post** on Instagram/Facebook linking to the video.

---

## Known Limitations

- **Neighborhood coordinates are best-guess** — I generated them from my training-data knowledge of Temple. If any feel off when you preview the HTML, adjust in the `COORDS` object at the top of the HTML file. The most likely-wrong ones: Sage Meadows (is it Temple or Belton proper?), Canyon Creek vs The Cliffs (they're close, the camera may not distinguish), flood plain pockets (I used a placeholder — put it where you actually mean).
- **Mapbox free tier:** 50,000 map loads per month. You will never hit that with personal video production. If the project grows into a client-facing site, watch the quota.
- **3D terrain exaggeration:** set to 1.4 in the HTML. Temple is flat so this makes the elevation visible. If it looks too dramatic, change `exaggeration: 1.4` to `exaggeration: 1.0` (real scale).
- **The HTML now uses a placeholder token** — replace `MAPBOX_PUBLIC_TOKEN` near the top of the HTML with your local Mapbox public token before rendering.

---

## One-Command Rollback

Delete the whole folder:

```bash
rm -rf /Users/taylordasch_1/claude-social-media-manager/yt-videos/temple-map-tour/
```

---

## Next After This Video Ships

Per the "New 20" list in `youtube-retention-research-2026-04-20.md`:

- **Video #2:** PCS to Fort Cavazos — Why Smart Military Families Skip Killeen and Live in Temple
- **Video #3:** I Ranked Every Temple Neighborhood Worst to Best (red/yellow/green tier system)

Both of these can reuse the same Mapbox flythrough engine — I can swap the `SEQUENCE` array for a new keyframe path and write a new script in 30 minutes once this video is in production.
