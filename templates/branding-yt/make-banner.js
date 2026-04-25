#!/usr/bin/env node
/**
 * YouTube banner renderer — channel-aware
 * Usage: node make-banner.js [living|investing|all]
 * Output: 2560 x 1440 PNG per channel (YouTube recommended spec)
 * Mobile safe area (always visible): 1546 x 423 centered
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

// YouTube banner spec
const W = 2560;
const H = 1440;
const SAFE_W = 1546;
const SAFE_H = 423;
const SAFE_X = (W - SAFE_W) / 2;
const SAFE_Y = (H - SAFE_H) / 2;

function registerFonts() {
  const fontsDir = path.join(thumbDir, 'assets/fonts');
  for (const f of fs.readdirSync(fontsDir)) {
    if (!/\.(ttf|otf)$/i.test(f)) continue;
    try {
      GlobalFonts.registerFromPath(path.join(fontsDir, f), 'Montserrat');
    } catch (e) {
      console.warn(`font register failed: ${f} — ${e.message}`);
    }
  }
}

function hexToRgba(hex, a = 1) {
  const h = hex.replace('#', '');
  const r = parseInt(h.slice(0, 2), 16);
  const g = parseInt(h.slice(2, 4), 16);
  const b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r},${g},${b},${a})`;
}

async function prepHeadshot(srcPath, size) {
  const meta = await sharp(srcPath).metadata();
  const edge = Math.min(meta.width, meta.height);
  const cropTop = Math.round((meta.height - edge) * 0.25);
  const cropLeft = Math.round((meta.width - edge) / 2);
  return sharp(srcPath)
    .rotate()
    .extract({ left: cropLeft, top: cropTop, width: edge, height: edge })
    .resize(size, size, { fit: 'cover' })
    .png()
    .toBuffer();
}

function drawBackground(ctx, ch) {
  ctx.fillStyle = COLORS.midnightDeep;
  ctx.fillRect(0, 0, W, H);

  const vert = ctx.createLinearGradient(0, 0, 0, H);
  vert.addColorStop(0, hexToRgba(COLORS.midnight, 1));
  vert.addColorStop(0.5, hexToRgba(COLORS.midnight, 1));
  vert.addColorStop(1, hexToRgba(COLORS.midnightDeep, 1));
  ctx.fillStyle = vert;
  ctx.fillRect(0, 0, W, H);

  // Accent radial glow behind the portrait (left-center of safe zone)
  const glowCX = SAFE_X + 280;
  const glowCY = H / 2;
  const glow = ctx.createRadialGradient(glowCX, glowCY, 40, glowCX, glowCY, 780);
  glow.addColorStop(0, hexToRgba(ch.accent, 0.38));
  glow.addColorStop(0.5, hexToRgba(ch.accent, 0.12));
  glow.addColorStop(1, hexToRgba(ch.accent, 0));
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, W, H);

  // Secondary emerald glow on far right for visual balance (same accent, weaker)
  const rightGlow = ctx.createRadialGradient(W - 260, H / 2, 40, W - 260, H / 2, 900);
  rightGlow.addColorStop(0, hexToRgba(ch.accent, 0.16));
  rightGlow.addColorStop(0.6, hexToRgba(ch.accent, 0.05));
  rightGlow.addColorStop(1, hexToRgba(ch.accent, 0));
  ctx.fillStyle = rightGlow;
  ctx.fillRect(0, 0, W, H);

  // Safe zone top & bottom accent rules
  ctx.fillStyle = ch.accent;
  ctx.fillRect(SAFE_X, SAFE_Y - 6, SAFE_W, 3);
  ctx.fillRect(SAFE_X, SAFE_Y + SAFE_H + 3, SAFE_W, 3);

  // Wing vertical bars
  ctx.fillStyle = hexToRgba(ch.accent, 0.55);
  ctx.fillRect(120, H / 2 - 200, 4, 400);
  ctx.fillRect(W - 124, H / 2 - 200, 4, 400);

  // Corner reticles
  ctx.strokeStyle = hexToRgba(ch.accent, 0.35);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(60, 60); ctx.lineTo(60, 120);
  ctx.moveTo(60, 60); ctx.lineTo(120, 60);
  ctx.moveTo(W - 60, H - 60); ctx.lineTo(W - 60, H - 120);
  ctx.moveTo(W - 60, H - 60); ctx.lineTo(W - 120, H - 60);
  ctx.stroke();
}

function drawTitleBlock(ctx, ch, textBlockX) {
  ctx.fillStyle = ch.accent;
  ctx.font = `800 38px Montserrat, sans-serif`;
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
  ctx.fillText(ch.eyebrow, textBlockX, SAFE_Y + 22);

  ctx.fillStyle = COLORS.snow;
  ctx.textBaseline = 'top';

  // Line A sizing — scale so "INVESTING IN" fits same width as "LIVING IN"
  const lineAFont = ch.heroLineA.length > 10 ? 82 : 104;
  ctx.font = `900 ${lineAFont}px Montserrat, sans-serif`;
  ctx.fillText(ch.heroLineA, textBlockX, SAFE_Y + 78 + (lineAFont === 104 ? 0 : 20));

  // Line B + tag (big)
  ctx.font = `900 188px Montserrat, sans-serif`;
  const mainW = ctx.measureText(ch.heroLineB).width;
  ctx.fillStyle = COLORS.snow;
  ctx.fillText(ch.heroLineB, textBlockX, SAFE_Y + 186);
  ctx.fillStyle = ch.accent;
  ctx.fillText(ch.heroTag, textBlockX + mainW, SAFE_Y + 186);

  // Underscore
  const titleBottom = SAFE_Y + 186 + 188 + 8;
  ctx.fillStyle = ch.accent;
  ctx.fillRect(textBlockX, titleBottom, 180, 6);

  // Tagline
  ctx.fillStyle = COLORS.snow;
  ctx.font = `700 42px Montserrat, sans-serif`;
  ctx.fillText(ch.tagline, textBlockX, titleBottom + 24);

  // Credential
  ctx.fillStyle = hexToRgba(COLORS.snow, 0.75);
  ctx.font = `600 30px Montserrat, sans-serif`;
  ctx.fillText(ch.credential, textBlockX, titleBottom + 82);
}

function drawFooterWings(ctx, ch) {
  ctx.fillStyle = ch.accent;
  ctx.font = `900 26px Montserrat, sans-serif`;
  ctx.textAlign = 'left';
  ctx.textBaseline = 'middle';
  ctx.fillText(ch.schedule, 180, H / 2 + 320);

  ctx.fillStyle = COLORS.snow;
  ctx.font = `800 26px Montserrat, sans-serif`;
  ctx.textAlign = 'right';
  ctx.fillText('TEMPLETXHOMES.NET', W - 180, H / 2 + 320);

  ctx.fillStyle = hexToRgba(COLORS.snow, 0.55);
  ctx.font = `600 18px Montserrat, sans-serif`;
  ctx.textAlign = 'left';
  ctx.fillText(ch.scheduleSub, 180, H / 2 + 350);

  ctx.textAlign = 'right';
  ctx.fillText(ch.coverage, W - 180, H / 2 + 350);
}

function drawVerticalSideLabels(ctx, ch) {
  ctx.save();
  ctx.translate(78, H / 2);
  ctx.rotate(-Math.PI / 2);
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = hexToRgba(COLORS.snow, 0.55);
  ctx.font = `800 22px Montserrat, sans-serif`;
  ctx.fillText(ch.verticalLeft, 0, 0);
  ctx.restore();

  ctx.save();
  ctx.translate(W - 78, H / 2);
  ctx.rotate(Math.PI / 2);
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = hexToRgba(ch.accent, 0.7);
  ctx.font = `800 22px Montserrat, sans-serif`;
  ctx.fillText(ch.verticalRight, 0, 0);
  ctx.restore();
}

async function drawHeadshot(ctx, ch, squareBuf, size, cx, cy) {
  const img = await loadImage(squareBuf);

  const grd = ctx.createRadialGradient(cx, cy, size / 2 + 4, cx, cy, size / 2 + 70);
  grd.addColorStop(0, hexToRgba(ch.accent, 0.55));
  grd.addColorStop(1, hexToRgba(ch.accent, 0));
  ctx.fillStyle = grd;
  ctx.beginPath();
  ctx.arc(cx, cy, size / 2 + 70, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, size / 2 + 8, 0, Math.PI * 2);
  ctx.strokeStyle = ch.accent;
  ctx.lineWidth = 10;
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(cx, cy, size / 2 + 2, 0, Math.PI * 2);
  ctx.strokeStyle = hexToRgba(COLORS.snow, 0.9);
  ctx.lineWidth = 3;
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.beginPath();
  ctx.arc(cx, cy, size / 2, 0, Math.PI * 2);
  ctx.closePath();
  ctx.clip();
  ctx.drawImage(img, cx - size / 2, cy - size / 2, size, size);
  ctx.restore();
}

async function renderChannel(channelKey) {
  const ch = CHANNELS[channelKey];
  if (!ch) throw new Error(`unknown channel: ${channelKey}`);

  const headshotSize = 420;
  const squareBuf = await prepHeadshot(HEADSHOT_PATH, headshotSize * 2);

  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  drawBackground(ctx, ch);
  drawVerticalSideLabels(ctx, ch);

  const headCX = SAFE_X + 260;
  const headCY = H / 2;
  await drawHeadshot(ctx, ch, squareBuf, headshotSize, headCX, headCY);

  const textBlockX = SAFE_X + 540;
  drawTitleBlock(ctx, ch, textBlockX);
  drawFooterWings(ctx, ch);

  const pngBuf = canvas.toBuffer('image/png');
  const finalBuf = await sharp(pngBuf).png({ compressionLevel: 9 }).toBuffer();
  const outPath = path.join(__dirname, `${ch.slug}-banner.png`);
  fs.writeFileSync(outPath, finalBuf);
  const kb = (fs.statSync(outPath).size / 1024).toFixed(0);
  console.log(`  banner  ${ch.slug}  ${W}x${H}  ${kb} KB  → ${outPath}`);
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
