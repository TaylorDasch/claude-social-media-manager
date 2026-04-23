#!/usr/bin/env node
/**
 * YouTube profile avatar renderer — channel-aware
 * Usage: node make-profile.js [living|investing|all]
 * Output: 800 x 800 PNG (YouTube spec, displayed as circle)
 *
 * Design: Tight face crop + brand ring. Reads at 32px nav icon size.
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
const SIZE = 800;

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
  // Tighter crop than banner — zoom in on face. Face sits in upper-center of portrait.
  const meta = await sharp(srcPath).metadata();
  const edge = Math.round(Math.min(meta.width, meta.height) * 0.70); // tighter edge
  const cropTop = Math.round((meta.height - edge) * 0.18); // pull up toward face
  const cropLeft = Math.round((meta.width - edge) / 2);
  return sharp(srcPath)
    .rotate()
    .extract({ left: cropLeft, top: cropTop, width: edge, height: edge })
    .resize(outSize, outSize, { fit: 'cover' })
    .png()
    .toBuffer();
}

async function renderChannel(channelKey) {
  const ch = CHANNELS[channelKey];
  if (!ch) throw new Error(`unknown channel: ${channelKey}`);

  const faceBuf = await prepFaceCrop(HEADSHOT_PATH, SIZE);
  const img = await loadImage(faceBuf);

  const canvas = createCanvas(SIZE, SIZE);
  const ctx = canvas.getContext('2d');

  // Full background tile (visible behind transparent corners when YT crops to circle)
  const bgGrad = ctx.createRadialGradient(SIZE / 2, SIZE / 2, 100, SIZE / 2, SIZE / 2, SIZE / 2);
  bgGrad.addColorStop(0, hexToRgba(ch.accent, 0.9));
  bgGrad.addColorStop(1, COLORS.midnightDeep);
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, SIZE, SIZE);

  // Outer accent ring (visible inside the circular crop YouTube applies)
  const ringOuter = SIZE / 2 - 10;
  const ringInner = ringOuter - 32;

  // Glow behind face
  const glow = ctx.createRadialGradient(SIZE / 2, SIZE / 2, ringInner - 40, SIZE / 2, SIZE / 2, ringOuter);
  glow.addColorStop(0, hexToRgba(ch.accent, 0));
  glow.addColorStop(1, hexToRgba(ch.accent, 0.45));
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(SIZE / 2, SIZE / 2, ringOuter, 0, Math.PI * 2);
  ctx.fill();

  // Face clipped to inner circle
  ctx.save();
  ctx.beginPath();
  ctx.arc(SIZE / 2, SIZE / 2, ringInner, 0, Math.PI * 2);
  ctx.closePath();
  ctx.clip();
  // Face fill
  ctx.drawImage(img, (SIZE - SIZE) / 2, (SIZE - SIZE) / 2, SIZE, SIZE);
  ctx.restore();

  // Brand ring (between inner and outer)
  ctx.strokeStyle = ch.accent;
  ctx.lineWidth = 22;
  ctx.beginPath();
  ctx.arc(SIZE / 2, SIZE / 2, (ringOuter + ringInner) / 2, 0, Math.PI * 2);
  ctx.stroke();

  // Thin snow separator ring (inside)
  ctx.strokeStyle = hexToRgba(COLORS.snow, 0.9);
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(SIZE / 2, SIZE / 2, ringInner + 3, 0, Math.PI * 2);
  ctx.stroke();

  // Thin snow separator ring (outside)
  ctx.strokeStyle = hexToRgba(COLORS.snow, 0.55);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(SIZE / 2, SIZE / 2, ringOuter - 2, 0, Math.PI * 2);
  ctx.stroke();

  const pngBuf = canvas.toBuffer('image/png');
  const finalBuf = await sharp(pngBuf).png({ compressionLevel: 9 }).toBuffer();
  const outPath = path.join(__dirname, `${ch.slug}-profile.png`);
  fs.writeFileSync(outPath, finalBuf);
  const kb = (fs.statSync(outPath).size / 1024).toFixed(0);
  console.log(`  profile ${ch.slug}  ${SIZE}x${SIZE}  ${kb} KB  → ${outPath}`);
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
