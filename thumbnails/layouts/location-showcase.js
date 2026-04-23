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

const DEFAULT_SCENE =
  'Beautiful luxury Texas neighborhood entrance with stone monument sign, manicured landscaping, wide tree-lined street, golden hour, high-end residential community, aerial perspective, 16:9';

async function compose({
  background,
  expressionPath,
  text,
  subtext,
  channel,
  variant = 0,
}) {
  const W = BRAND.dimensions.width;
  const H = BRAND.dimensions.height;
  const accent = BRAND.channels[channel].accentColor;

  const offsetX = [0, -16, 18][variant % 3];
  const offsetY = [0, 16, -16][variant % 3];

  let buf = await applyGradientOverlay(background, W, H, [
    {
      x0: 0, y0: H, x1: 0, y1: Math.round(H * 0.35),
      stops: [
        { at: 0, color: hexToRgba(BRAND.colors.midnight, 0.92) },
        { at: 1, color: 'rgba(0,0,0,0)' },
      ],
    },
    {
      x0: 0, y0: 0, x1: W, y1: 0,
      stops: [
        { at: 0, color: hexToRgba(BRAND.colors.midnight, 0.62) },
        { at: 0.5, color: 'rgba(0,0,0,0.25)' },
        { at: 1, color: 'rgba(0,0,0,0.1)' },
      ],
    },
  ]);

  buf = await compositeExpression(buf, expressionPath, {
    width: W,
    height: H,
    targetHeight: Math.round(H * 0.72),
    left: Math.round(W * 0.02),
    top: Math.round(H * 0.26),
    flip: false,
  });

  const { canvas, ctx } = createTextCanvas(W, H);

  const textZoneX = Math.round(W * 0.98) + offsetX;
  const textZoneY = Math.round(H * 0.12) + offsetY;
  const textZoneW = Math.round(W * 0.6);
  const textZoneH = Math.round(H * 0.3);

  // accent line above location name
  ctx.strokeStyle = accent;
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(textZoneX - Math.round(W * 0.22), textZoneY - 16);
  ctx.lineTo(textZoneX, textZoneY - 16);
  ctx.stroke();

  const heroSize = fitTextToWidth(ctx, text, textZoneW, textZoneH, 800, 200);
  drawHeroText(ctx, text, textZoneX, textZoneY, {
    fontPx: heroSize,
    color: BRAND.colors.white,
    weight: 900,
    align: 'right',
    baseline: 'top',
    strokeWidth: 8,
  });

  if (subtext) {
    const subSize = Math.round(heroSize * 0.3);
    drawHeroText(ctx, subtext, textZoneX, textZoneY + heroSize + 18, {
      fontPx: subSize,
      color: accent,
      weight: 800,
      align: 'right',
      baseline: 'top',
      strokeWidth: 5,
    });
  }

  const overlay = canvas.toBuffer('image/png');
  buf = await overlayCanvas(buf, overlay, W, H);
  return {
    buffer: buf,
    textRegion: { x: 0.36, y: 0.10, w: 0.62, h: 0.42 },
  };
}

module.exports = { compose, DEFAULT_SCENE };
