#!/usr/bin/env node
/**
 * YouTube outro/end-screen frame renderer — channel-aware
 * Usage: node make-outro.js [living|investing|all]
 * Output: 1920 x 1080 PNG, 16:9
 *
 * Design: End screen with reserved zones for YouTube's overlay elements.
 *   - Subscribe circle zone (~196-300px): bottom-left, visually cued with arrow
 *   - Video element zones (2): right half, stacked, 16:9 each
 *   - Keep all text OUTSIDE those zones so YT overlays don't cover copy
 */

const fs = require('fs');
const path = require('path');
const { createRequire } = require('module');

const thumbDir = path.resolve(__dirname, '../../thumbnails');
const thumbReq = createRequire(path.join(thumbDir, 'package.json'));
const sharp = thumbReq('sharp');
const { createCanvas, GlobalFonts, loadImage } = thumbReq('@napi-rs/canvas');

const { COLORS, CHANNELS } = require('./brand-channels');

const HEADSHOT_PATH = '/Users/taylordasch_1/headshot.jpeg';
const W = 1920;
const H = 1080;

// Reserved zones (YouTube editor places elements here; keep background subtle, no text)
const SUBSCRIBE_ZONE = { cx: 280, cy: 820, r: 160 };         // circular subscribe
const VIDEO_ZONE_1 = { x: 1080, y: 200, w: 720, h: 405 };    // top-right 16:9
const VIDEO_ZONE_2 = { x: 1080, y: 645, w: 720, h: 405 };    // bottom-right 16:9

function registerFonts() {
  const fontsDir = path.join(thumbDir, 'assets/fonts');
  for (const f of fs.readdirSync(fontsDir)) {
    if (!/\.(ttf|otf)$/i.test(f)) continue;
    try { GlobalFonts.registerFromPath(path.join(fontsDir, f), 'Montserrat'); } catch {}
  }
}

function hexToRgba(hex, a = 1) {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r},${g},${b},${a})`;
}

async function prepFaceCrop(srcPath, outSize) {
  const meta = await sharp(srcPath).metadata();
  const edge = Math.round(Math.min(meta.width, meta.height) * 0.72);
  const cropTop = Math.round((meta.height - edge) * 0.20);
  const cropLeft = Math.round((meta.width - edge) / 2);
  return sharp(srcPath)
    .rotate()
    .extract({ left: cropLeft, top: cropTop, width: edge, height: edge })
    .resize(outSize, outSize, { fit: 'cover' })
    .png()
    .toBuffer();
}

function drawBackground(ctx, ch) {
  ctx.fillStyle = COLORS.midnightDeep;
  ctx.fillRect(0, 0, W, H);

  // Vertical depth gradient
  const vert = ctx.createLinearGradient(0, 0, 0, H);
  vert.addColorStop(0, hexToRgba(COLORS.midnight, 1));
  vert.addColorStop(1, hexToRgba(COLORS.midnightDeep, 1));
  ctx.fillStyle = vert;
  ctx.fillRect(0, 0, W, H);

  // Accent glow lower-left (around subscribe zone — visual cue)
  const subGlow = ctx.createRadialGradient(
    SUBSCRIBE_ZONE.cx, SUBSCRIBE_ZONE.cy, 40,
    SUBSCRIBE_ZONE.cx, SUBSCRIBE_ZONE.cy, 520
  );
  subGlow.addColorStop(0, hexToRgba(ch.accent, 0.50));
  subGlow.addColorStop(0.5, hexToRgba(ch.accent, 0.18));
  subGlow.addColorStop(1, hexToRgba(ch.accent, 0));
  ctx.fillStyle = subGlow;
  ctx.fillRect(0, 0, W, H);

  // Secondary emerald glow top-right for visual balance (same accent)
  const rightGlow = ctx.createRadialGradient(W - 260, 240, 40, W - 260, 240, 720);
  rightGlow.addColorStop(0, hexToRgba(ch.accent, 0.20));
  rightGlow.addColorStop(1, hexToRgba(ch.accent, 0));
  ctx.fillStyle = rightGlow;
  ctx.fillRect(0, 0, W, H);

  // Corner reticles (match banner system)
  ctx.strokeStyle = hexToRgba(ch.accent, 0.35);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(40, 40); ctx.lineTo(40, 100);
  ctx.moveTo(40, 40); ctx.lineTo(100, 40);
  ctx.moveTo(W - 40, H - 40); ctx.lineTo(W - 40, H - 100);
  ctx.moveTo(W - 40, H - 40); ctx.lineTo(W - 100, H - 40);
  ctx.stroke();
}

function drawZoneFrames(ctx, ch) {
  // Dashed placeholder frames for video zones (subtle — they're meant to sit under real videos)
  ctx.strokeStyle = hexToRgba(ch.accent, 0.6);
  ctx.lineWidth = 3;
  ctx.setLineDash([12, 8]);

  for (const z of [VIDEO_ZONE_1, VIDEO_ZONE_2]) {
    ctx.strokeRect(z.x, z.y, z.w, z.h);
  }

  // Subscribe zone circle outline (dashed)
  ctx.beginPath();
  ctx.arc(SUBSCRIBE_ZONE.cx, SUBSCRIBE_ZONE.cy, SUBSCRIBE_ZONE.r, 0, Math.PI * 2);
  ctx.stroke();

  ctx.setLineDash([]);
}

function drawHeroCopy(ctx, ch) {
  // Top-left: channel bar
  ctx.fillStyle = ch.accent;
  ctx.fillRect(60, 80, 8, 80);

  ctx.fillStyle = COLORS.snow;
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
  ctx.font = `900 48px Montserrat, sans-serif`;
  ctx.fillText(ch.displayName, 96, 80);

  ctx.fillStyle = ch.accent;
  ctx.font = `800 22px Montserrat, sans-serif`;
  ctx.fillText('TAYLOR DASCH  ·  EG REALTY  ·  TEMPLETXHOMES.NET', 96, 140);

  // Middle-left hero copy (kept clear of subscribe zone below)
  ctx.fillStyle = COLORS.snow;
  ctx.font = `900 120px Montserrat, sans-serif`;
  ctx.fillText(ch.outroHeading.split(' ')[0], 60, 280); // "THANKS"

  ctx.font = `900 120px Montserrat, sans-serif`;
  ctx.fillText(ch.outroHeading.split(' ').slice(1).join(' '), 60, 408); // "FOR WATCHING"

  // Accent underline
  ctx.fillStyle = ch.accent;
  ctx.fillRect(60, 550, 200, 6);

  // Sub
  ctx.fillStyle = hexToRgba(COLORS.snow, 0.82);
  ctx.font = `700 30px Montserrat, sans-serif`;
  ctx.fillText(ch.outroSub, 60, 580);

  // Right-side column header (above video zones)
  ctx.fillStyle = ch.accent;
  ctx.font = `900 36px Montserrat, sans-serif`;
  ctx.textAlign = 'left';
  ctx.fillText('WATCH NEXT →', VIDEO_ZONE_1.x, VIDEO_ZONE_1.y - 56);

  ctx.fillStyle = hexToRgba(COLORS.snow, 0.65);
  ctx.font = `600 20px Montserrat, sans-serif`;
  ctx.fillText('Picked for you', VIDEO_ZONE_1.x, VIDEO_ZONE_1.y - 24);

  // Subscribe arrow/label (guides eye to the subscribe element zone)
  ctx.fillStyle = ch.accent;
  ctx.font = `900 44px Montserrat, sans-serif`;
  ctx.textAlign = 'left';
  ctx.textBaseline = 'middle';
  ctx.fillText('SUBSCRIBE', SUBSCRIBE_ZONE.cx + SUBSCRIBE_ZONE.r + 40, SUBSCRIBE_ZONE.cy - 20);

  ctx.fillStyle = hexToRgba(COLORS.snow, 0.7);
  ctx.font = `600 22px Montserrat, sans-serif`;
  ctx.fillText('It costs you nothing.', SUBSCRIBE_ZONE.cx + SUBSCRIBE_ZONE.r + 40, SUBSCRIBE_ZONE.cy + 24);
  ctx.fillText('It helps more than you know.', SUBSCRIBE_ZONE.cx + SUBSCRIBE_ZONE.r + 40, SUBSCRIBE_ZONE.cy + 58);

  // Arrow from text toward subscribe circle
  ctx.strokeStyle = ch.accent;
  ctx.lineWidth = 5;
  ctx.lineCap = 'round';
  ctx.beginPath();
  const ax1 = SUBSCRIBE_ZONE.cx + SUBSCRIBE_ZONE.r + 30;
  const ay1 = SUBSCRIBE_ZONE.cy - 70;
  const ax2 = SUBSCRIBE_ZONE.cx + SUBSCRIBE_ZONE.r - 6;
  const ay2 = SUBSCRIBE_ZONE.cy - 6;
  ctx.moveTo(ax1, ay1);
  ctx.bezierCurveTo(ax1 - 80, ay1 - 40, ax2 - 60, ay2 - 120, ax2, ay2);
  ctx.stroke();
  // Arrowhead
  ctx.beginPath();
  ctx.moveTo(ax2, ay2);
  ctx.lineTo(ax2 - 22, ay2 - 20);
  ctx.moveTo(ax2, ay2);
  ctx.lineTo(ax2 - 8, ay2 - 28);
  ctx.stroke();

  // Bottom strip — website + phone
  ctx.textAlign = 'center';
  ctx.textBaseline = 'bottom';
  ctx.fillStyle = hexToRgba(COLORS.snow, 0.75);
  ctx.font = `700 24px Montserrat, sans-serif`;
  ctx.fillText('TEMPLETXHOMES.NET  ·  254-718-4249  ·  DEALSWITHDASCH@GMAIL.COM', W / 2, H - 40);
}

async function drawSmallHeadshot(ctx, ch) {
  // Small portrait near hero copy (upper-middle, between text and video zones would collide — place above "THANKS")
  const faceBuf = await prepFaceCrop(HEADSHOT_PATH, 360);
  const img = await loadImage(faceBuf);
  const cx = 900;
  const cy = 430;
  const r = 170;

  const glow = ctx.createRadialGradient(cx, cy, r, cx, cy, r + 60);
  glow.addColorStop(0, hexToRgba(ch.accent, 0.55));
  glow.addColorStop(1, hexToRgba(ch.accent, 0));
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(cx, cy, r + 60, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, r + 6, 0, Math.PI * 2);
  ctx.strokeStyle = ch.accent;
  ctx.lineWidth = 8;
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.closePath();
  ctx.clip();
  ctx.drawImage(img, cx - r, cy - r, r * 2, r * 2);
  ctx.restore();
}

async function renderChannel(channelKey) {
  const ch = CHANNELS[channelKey];
  if (!ch) throw new Error(`unknown channel: ${channelKey}`);

  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  drawBackground(ctx, ch);
  drawZoneFrames(ctx, ch);
  await drawSmallHeadshot(ctx, ch);
  drawHeroCopy(ctx, ch);

  const pngBuf = canvas.toBuffer('image/png');
  const finalBuf = await sharp(pngBuf).png({ compressionLevel: 9 }).toBuffer();
  const outPath = path.join(__dirname, `${ch.slug}-outro.png`);
  fs.writeFileSync(outPath, finalBuf);
  const kb = (fs.statSync(outPath).size / 1024).toFixed(0);
  console.log(`  outro   ${ch.slug}  ${W}x${H}  ${kb} KB  → ${outPath}`);
  return outPath;
}

async function main() {
  registerFonts();
  if (!fs.existsSync(HEADSHOT_PATH)) throw new Error(`headshot missing: ${HEADSHOT_PATH}`);

  const arg = (process.argv[2] || 'all').toLowerCase();
  const keys = arg === 'all' ? Object.keys(CHANNELS) : [arg];
  for (const k of keys) await renderChannel(k);
}

if (require.main === module) {
  main().catch(e => { console.error(e.stack || e.message); process.exit(1); });
}

module.exports = { renderChannel };
