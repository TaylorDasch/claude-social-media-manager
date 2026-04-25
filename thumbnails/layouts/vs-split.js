const sharp = require('sharp');
const { BRAND } = require('../brand');
const {
  applyGradientOverlay,
  compositeExpression,
  overlayCanvas,
  createTextCanvas,
  drawHeroText,
  fitTextToWidth,
  hexToRgba,
} = require('../services/compositor');

const DEFAULT_SCENE_LEFT =
  'Aerial photograph of a Texas suburban neighborhood, golden hour, residential homes, wide angle';
const DEFAULT_SCENE_RIGHT =
  'Aerial photograph of downtown Texas small city, golden hour, residential homes, wide angle';
const DEFAULT_SCENE = DEFAULT_SCENE_LEFT;

async function buildSplitBackground(leftBuf, rightBuf, W, H) {
  const left = await sharp(leftBuf).resize(W, H, { fit: 'cover' }).toBuffer();
  const right = await sharp(rightBuf).resize(W, H, { fit: 'cover' }).toBuffer();

  const { createCanvas, loadImage } = require('@napi-rs/canvas');
  const canvas = createCanvas(W, H);
  const ctx = canvas.getContext('2d');

  const leftImg = await loadImage(left);
  const rightImg = await loadImage(right);

  const slant = Math.tan((5 * Math.PI) / 180) * H;

  ctx.save();
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(W / 2 + slant / 2, 0);
  ctx.lineTo(W / 2 - slant / 2, H);
  ctx.lineTo(0, H);
  ctx.closePath();
  ctx.clip();
  ctx.drawImage(leftImg, 0, 0, W, H);
  ctx.fillStyle = 'rgba(5, 150, 105, 0.28)';
  ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = 'rgba(30, 41, 59, 0.55)';
  ctx.fillRect(0, 0, W, H);
  ctx.restore();

  ctx.save();
  ctx.beginPath();
  ctx.moveTo(W / 2 + slant / 2, 0);
  ctx.lineTo(W, 0);
  ctx.lineTo(W, H);
  ctx.lineTo(W / 2 - slant / 2, H);
  ctx.closePath();
  ctx.clip();
  ctx.drawImage(rightImg, 0, 0, W, H);
  ctx.fillStyle = 'rgba(212, 168, 83, 0.28)';
  ctx.fillRect(0, 0, W, H);
  ctx.fillStyle = 'rgba(30, 41, 59, 0.55)';
  ctx.fillRect(0, 0, W, H);
  ctx.restore();

  ctx.strokeStyle = BRAND.colors.white;
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(W / 2 + slant / 2, 0);
  ctx.lineTo(W / 2 - slant / 2, H);
  ctx.stroke();

  return canvas.toBuffer('image/png');
}

async function compose({
  background,
  leftImage,
  rightImage,
  expressionPath,
  text,
  leftLabel,
  rightLabel,
  channel,
  variant = 0,
}) {
  const W = BRAND.dimensions.width;
  const H = BRAND.dimensions.height;

  const leftBuf = leftImage || background;
  const rightBuf = rightImage || background;

  let buf = await buildSplitBackground(leftBuf, rightBuf, W, H);

  const { canvas, ctx } = createTextCanvas(W, H);

  if (leftLabel) {
    const labelSize = fitTextToWidth(ctx, leftLabel, W * 0.42, 120, 900, 120);
    drawHeroText(ctx, leftLabel, Math.round(W * 0.04), Math.round(H * 0.12), {
      fontPx: labelSize,
      color: BRAND.colors.white,
      weight: 900,
      align: 'left',
      baseline: 'top',
      strokeWidth: 8,
    });
  }
  if (rightLabel) {
    const labelSize = fitTextToWidth(ctx, rightLabel, W * 0.42, 120, 900, 120);
    drawHeroText(ctx, rightLabel, Math.round(W * 0.96), Math.round(H * 0.12), {
      fontPx: labelSize,
      color: BRAND.colors.white,
      weight: 900,
      align: 'right',
      baseline: 'top',
      strokeWidth: 8,
    });
  }

  const vsText = text || 'VS';
  const vsSize = 340;
  ctx.save();
  ctx.shadowColor = hexToRgba(BRAND.channels[channel].accentColor, 0.9);
  ctx.shadowBlur = 40;
  drawHeroText(ctx, vsText, W / 2, H / 2, {
    fontPx: vsSize,
    color: BRAND.colors.white,
    weight: 900,
    align: 'center',
    baseline: 'middle',
    strokeWidth: 14,
  });
  ctx.restore();

  const overlay = canvas.toBuffer('image/png');
  buf = await overlayCanvas(buf, overlay, W, H);

  const faceHeight = Math.round(H * 0.38);
  buf = await compositeExpression(buf, expressionPath, {
    width: W,
    height: H,
    targetHeight: faceHeight,
    left: Math.round(W / 2 - faceHeight * 0.55),
    top: Math.round(H - faceHeight * 1.02),
    flip: false,
  });

  return {
    buffer: buf,
    textRegion: { x: 0.30, y: 0.25, w: 0.40, h: 0.50 },
  };
}

module.exports = { compose, DEFAULT_SCENE, DEFAULT_SCENE_LEFT, DEFAULT_SCENE_RIGHT };
