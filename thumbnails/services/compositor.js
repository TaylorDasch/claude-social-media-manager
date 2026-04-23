const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { createCanvas, GlobalFonts, loadImage } = require('@napi-rs/canvas');
const { BRAND } = require('../brand');

// YouTube overlays a timestamp pill in the bottom-right ~15% of the thumbnail.
// Text should stay out of this zone.
const TIMESTAMP_ZONE = {
  xStart: 0.82,
  yStart: 0.82,
};

function getTimestampZoneBounds(width, height) {
  return {
    left: Math.round(width * TIMESTAMP_ZONE.xStart),
    top: Math.round(height * TIMESTAMP_ZONE.yStart),
    right: width,
    bottom: height,
  };
}

function clearsTimestampZone(x, y, textWidth, textHeight, width, height, align = 'left', baseline = 'top') {
  const zone = getTimestampZoneBounds(width, height);
  let left = x;
  let right = x + textWidth;
  if (align === 'center') { left = x - textWidth / 2; right = x + textWidth / 2; }
  if (align === 'right') { left = x - textWidth; right = x; }
  let top = y;
  let bottom = y + textHeight;
  if (baseline === 'middle') { top = y - textHeight / 2; bottom = y + textHeight / 2; }
  if (baseline === 'bottom') { top = y - textHeight; bottom = y; }
  return !(right > zone.left && bottom > zone.top);
}

let fontsRegistered = false;
function registerFonts(fontsDir) {
  if (fontsRegistered) return;
  if (!fs.existsSync(fontsDir)) {
    console.warn(`[compositor] fonts dir not found: ${fontsDir} — falling back to system sans-serif`);
    fontsRegistered = true;
    return;
  }
  const files = fs.readdirSync(fontsDir).filter(f => /\.(ttf|otf)$/i.test(f));
  for (const f of files) {
    const abs = path.join(fontsDir, f);
    try {
      GlobalFonts.registerFromPath(abs, 'Montserrat');
    } catch (e) {
      console.warn(`[compositor] could not register font ${f}: ${e.message}`);
    }
  }
  fontsRegistered = true;
}

function hexToRgba(hex, alpha = 1) {
  const h = hex.replace('#', '');
  const r = parseInt(h.substring(0, 2), 16);
  const g = parseInt(h.substring(2, 4), 16);
  const b = parseInt(h.substring(4, 6), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

function adjustLightness(hex, delta) {
  const h = hex.replace('#', '');
  let r = parseInt(h.substring(0, 2), 16);
  let g = parseInt(h.substring(2, 4), 16);
  let b = parseInt(h.substring(4, 6), 16);
  r = Math.max(0, Math.min(255, Math.round(r + 255 * delta)));
  g = Math.max(0, Math.min(255, Math.round(g + 255 * delta)));
  b = Math.max(0, Math.min(255, Math.round(b + 255 * delta)));
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
}

async function loadBackground(buffer, width, height) {
  return sharp(buffer)
    .resize(width, height, { fit: 'cover', position: 'centre' })
    .toBuffer();
}

async function makeSolidGradient(from, to, width, height, angleDeg = 0) {
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext('2d');
  const rad = (angleDeg * Math.PI) / 180;
  const x = Math.cos(rad);
  const y = Math.sin(rad);
  const x0 = width / 2 - (x * width) / 2;
  const y0 = height / 2 - (y * height) / 2;
  const x1 = width / 2 + (x * width) / 2;
  const y1 = height / 2 + (y * height) / 2;
  const grad = ctx.createLinearGradient(x0, y0, x1, y1);
  grad.addColorStop(0, from);
  grad.addColorStop(1, to);
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, width, height);
  return canvas.toBuffer('image/png');
}

function measureText(ctx, text, fontPx, weight) {
  ctx.font = `${weight} ${fontPx}px Montserrat, sans-serif`;
  return ctx.measureText(text);
}

function fitTextToWidth(ctx, text, maxWidth, maxHeight, weight, startPx = 260) {
  let size = startPx;
  while (size > 24) {
    ctx.font = `${weight} ${size}px Montserrat, sans-serif`;
    const m = ctx.measureText(text);
    const w = m.width;
    const h = (m.actualBoundingBoxAscent || size * 0.8) + (m.actualBoundingBoxDescent || size * 0.2);
    if (w <= maxWidth && h <= maxHeight) return size;
    size -= 4;
  }
  return size;
}

// Manual kerning: draws glyph-by-glyph with -2% spacing for bold impact.
// Canvas letterSpacing is inconsistent across @napi-rs/canvas versions,
// so we hand-space to guarantee the tightening.
function drawKernedText(ctx, text, x, y, align, baseline, kernRatio) {
  ctx.save();
  ctx.textAlign = 'left';
  ctx.textBaseline = baseline;
  const fontMatch = ctx.font.match(/(\d+(?:\.\d+)?)px/);
  const fontPx = fontMatch ? parseFloat(fontMatch[1]) : 64;
  const kernAdjust = fontPx * kernRatio;
  const widths = [];
  let total = 0;
  for (const ch of text) {
    const w = ctx.measureText(ch).width;
    widths.push(w);
    total += w;
  }
  total += kernAdjust * (text.length - 1);

  let cursor = x;
  if (align === 'center') cursor = x - total / 2;
  if (align === 'right') cursor = x - total;

  let i = 0;
  for (const ch of text) {
    ctx.fillText(ch, cursor, y);
    cursor += widths[i] + kernAdjust;
    i++;
  }
  ctx.restore();
  return total;
}

function drawKernedStroke(ctx, text, x, y, align, baseline, kernRatio) {
  ctx.save();
  ctx.textAlign = 'left';
  ctx.textBaseline = baseline;
  const fontMatch = ctx.font.match(/(\d+(?:\.\d+)?)px/);
  const fontPx = fontMatch ? parseFloat(fontMatch[1]) : 64;
  const kernAdjust = fontPx * kernRatio;
  const widths = [];
  let total = 0;
  for (const ch of text) {
    const w = ctx.measureText(ch).width;
    widths.push(w);
    total += w;
  }
  total += kernAdjust * (text.length - 1);

  let cursor = x;
  if (align === 'center') cursor = x - total / 2;
  if (align === 'right') cursor = x - total;

  let i = 0;
  for (const ch of text) {
    ctx.strokeText(ch, cursor, y);
    cursor += widths[i] + kernAdjust;
    i++;
  }
  ctx.restore();
}

function drawHeroText(ctx, text, x, y, {
  fontPx,
  color,
  weight = 900,
  align = 'left',
  baseline = 'top',
  strokeColor = 'rgba(0,0,0,0.8)',
  strokeWidth = 8,
  shadow = true,
  kern = -0.02,
}) {
  ctx.save();
  ctx.font = `${weight} ${fontPx}px Montserrat, sans-serif`;
  if (shadow) {
    ctx.shadowColor = 'rgba(0,0,0,0.65)';
    ctx.shadowOffsetX = 4;
    ctx.shadowOffsetY = 6;
    ctx.shadowBlur = 12;
  }
  if (strokeWidth > 0) {
    ctx.lineWidth = strokeWidth;
    ctx.strokeStyle = strokeColor;
    ctx.lineJoin = 'round';
    ctx.miterLimit = 2;
    drawKernedStroke(ctx, text, x, y, align, baseline, kern);
  }
  ctx.shadowColor = 'transparent';
  ctx.fillStyle = color;
  drawKernedText(ctx, text, x, y, align, baseline, kern);
  ctx.restore();
}

// Returns total rendered width of kerned text for layout math.
function measureKernedWidth(ctx, text, fontPx, weight, kern = -0.02) {
  ctx.save();
  ctx.font = `${weight} ${fontPx}px Montserrat, sans-serif`;
  let total = 0;
  for (const ch of text) total += ctx.measureText(ch).width;
  total += fontPx * kern * (text.length - 1);
  ctx.restore();
  return total;
}

async function applyGradientOverlay(baseBuffer, width, height, stops) {
  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext('2d');
  const img = await loadImage(baseBuffer);
  ctx.drawImage(img, 0, 0, width, height);

  for (const stop of stops) {
    const grad = ctx.createLinearGradient(stop.x0, stop.y0, stop.x1, stop.y1);
    for (const s of stop.stops) grad.addColorStop(s.at, s.color);
    ctx.fillStyle = grad;
    if (stop.composite) ctx.globalCompositeOperation = stop.composite;
    ctx.fillRect(0, 0, width, height);
    ctx.globalCompositeOperation = 'source-over';
  }

  return canvas.toBuffer('image/png');
}

async function compositeExpression(baseBuffer, expressionPath, {
  width,
  height,
  targetHeight,
  left,
  top,
  flip = false,
}) {
  if (!expressionPath) return baseBuffer; // AI composite mode — skip manual paste
  if (!fs.existsSync(expressionPath)) {
    console.warn(`[compositor] expression photo not found: ${expressionPath}`);
    return baseBuffer;
  }

  let expr = sharp(expressionPath);
  const meta = await expr.metadata();
  const scale = targetHeight / meta.height;
  const newW = Math.round(meta.width * scale);
  const newH = targetHeight;

  let pipeline = sharp(expressionPath).resize(newW, newH, { fit: 'inside' });
  if (flip) pipeline = pipeline.flop();
  const exprBuffer = await pipeline.toBuffer();

  const finalLeft = Math.max(0, Math.min(width - newW, Math.round(left)));
  const finalTop = Math.max(0, Math.min(height - newH, Math.round(top)));

  return sharp(baseBuffer)
    .composite([{ input: exprBuffer, left: finalLeft, top: finalTop }])
    .toBuffer();
}

async function overlayCanvas(baseBuffer, canvasBuffer, width, height) {
  return sharp(baseBuffer)
    .composite([{ input: canvasBuffer, left: 0, top: 0 }])
    .toBuffer();
}

function createTextCanvas(width, height) {
  const canvas = createCanvas(width, height);
  return { canvas, ctx: canvas.getContext('2d') };
}

async function finalizePng(buffer) {
  return sharp(buffer)
    .sharpen({ sigma: 0.6 })
    .png({ compressionLevel: 9, quality: 95 })
    .toBuffer();
}

// Relative luminance per WCAG 2.1.
function srgbLuminance(r, g, b) {
  const toLin = (c) => {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * toLin(r) + 0.7152 * toLin(g) + 0.0722 * toLin(b);
}

function contrastRatio(l1, l2) {
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Samples a region of the thumbnail downscaled to browse-size (160x90),
// splits into text pixels vs background pixels by luminance split, and
// returns the WCAG contrast ratio between the two groups.
// textRegion is {x,y,w,h} in normalized [0..1] coordinates; defaults to full image.
async function validateLegibility(buffer, textRegion = null) {
  try {
    const raw = await sharp(buffer)
      .resize(160, 90)
      .removeAlpha()
      .raw()
      .toBuffer({ resolveWithObject: true });
    const { data, info } = raw;
    const w = info.width;
    const h = info.height;

    const region = textRegion
      ? {
          x0: Math.max(0, Math.floor(textRegion.x * w)),
          y0: Math.max(0, Math.floor(textRegion.y * h)),
          x1: Math.min(w, Math.ceil((textRegion.x + textRegion.w) * w)),
          y1: Math.min(h, Math.ceil((textRegion.y + textRegion.h) * h)),
        }
      : { x0: 0, y0: 0, x1: w, y1: h };

    const lums = [];
    for (let y = region.y0; y < region.y1; y++) {
      for (let x = region.x0; x < region.x1; x++) {
        const idx = (y * w + x) * 3;
        lums.push(srgbLuminance(data[idx], data[idx + 1], data[idx + 2]));
      }
    }
    if (lums.length < 10) return { ok: true, contrast: null };

    lums.sort((a, b) => a - b);
    const lowQuartile = lums[Math.floor(lums.length * 0.1)];
    const highQuartile = lums[Math.floor(lums.length * 0.9)];
    const contrast = contrastRatio(highQuartile, lowQuartile);
    // WCAG AA threshold for large text (18pt+ bold) is 3.0:1.
    // Thumbnail hero text is always much larger than this, so we use
    // 3.5:1 as the pass bar (small safety margin).
    return { ok: contrast >= 3.5, contrast };
  } catch (e) {
    return { ok: true, contrast: null, error: e.message };
  }
}

module.exports = {
  registerFonts,
  hexToRgba,
  adjustLightness,
  loadBackground,
  makeSolidGradient,
  applyGradientOverlay,
  compositeExpression,
  overlayCanvas,
  createTextCanvas,
  drawHeroText,
  drawKernedText,
  drawKernedStroke,
  measureKernedWidth,
  fitTextToWidth,
  measureText,
  finalizePng,
  validateLegibility,
  contrastRatio,
  srgbLuminance,
  clearsTimestampZone,
  getTimestampZoneBounds,
  TIMESTAMP_ZONE,
};
