# End Card Templates — Living in Temple, TX

Reusable, evergreen end cards. Drop the PNG on the last 20s of any video. Zero edits required.

## Files

| File | Use |
|------|-----|
| `living-in-temple-end-card.png` | **Channel-wide outro.** Drag onto V1 (or last clip) of every Living in Temple video. 1920×1080. |
| `living-in-temple-end-card.html` | Source — edit if branding ever changes |
| `taylor-headshot.jpg` | Headshot asset (referenced by HTML) |

## CapCut workflow (one-time setup)

1. In CapCut, open Media library
2. Drag `living-in-temple-end-card.png` in
3. Right-click → **Add to favorites**
4. From now on, the card lives in your quick-access tray on every project — two-click drop on the timeline

## Placement rule

- IN: last 20–24 seconds of video
- OUT: end of video
- Track: V1 (replaces talking head) — or top overlay if you want talking head visible behind
- Fade-in: 16 frames
- Hold static through final sign-off

## Re-render after edits

```bash
cd ~/claude-social-media-manager/templates/end-cards/
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1920,1080 \
  --screenshot=living-in-temple-end-card.png \
  "file://$(pwd)/living-in-temple-end-card.html"
```

## What lives here vs. what doesn't

This template is **channel-agnostic** within Living in Temple. It does NOT reference any specific video, date, or data pull. If you need a video-specific end card (e.g., "Next pull June 14" for the monthly Market Read), keep that in the video's own folder, not here.

If/when you build an Investing in Temple end card, save it as `investing-in-temple-end-card.html` in this same folder.
