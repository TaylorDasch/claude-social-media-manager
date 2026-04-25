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
  'Professional real estate data visualization background, subtle bar charts and graphs, dark blue tones, bokeh depth of field, modern and clean, cinematic lighting, 16:9';

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

  const offsetX = [0, -16, 20][variant % 3];
  const offsetY = [0, 18, -24][variant % 3];
  const gradAngle = [0, -8, 10][variant % 3];

  let buf = await applyGradientOverlay(background, W, H, [
    {
      x0: 0, y0: 0, x1: W, y1: 0,
      stops: [
        { at: 0, color: hexToRgba(BRAND.colors.midnight, 0.95) },
        { at: 0.5, color: hexToRgba(BRAND.colors.midnight, 0.72) },
        { at: 1, color: hexToRgba(BRAND.colors.midnight, 0.4) },
      ],
    },
    {
      x0: 0, y0: H, x1: 0, y1: H * 0.6,
      stops: [
        { at: 0, color: hexToRgba(BRAND.colors.midnight, 0.85) },
        { at: 1, color: 'rgba(0,0,0,0)' },
      ],
    },
  ]);

  buf = await compositeExpression(buf, expressionPath, {
    width: W,
    height: H,
    targetHeight: Math.round(H * (0.95 + (variant === 2 ? 0.03 : 0))),
    left: -Math.round(W * 0.08),
    top: Math.round(H * 0.05),
    flip: false,
  });

  const { canvas, ctx } = createTextCanvas(W, H);

  const textZoneX = Math.round(W * 0.48) + offsetX;
  const textZoneY = Math.round(H * 0.22) + offsetY;
  const textZoneW = Math.round(W * 0.48);
  const textZoneH = Math.round(H * 0.42);

  const heroSize = fitTextToWidth(ctx, text, textZoneW, textZoneH, 900, 300);
  drawHeroText(ctx, text, textZoneX, textZoneY, {
    fontPx: heroSize,
    color: accent,
    weight: 900,
    align: 'left',
    baseline: 'top',
    strokeWidth: 10,
  });

  if (subtext) {
    const subSize = Math.round(heroSize * 0.32);
    drawHeroText(ctx, subtext, textZoneX, textZoneY + heroSize + 24, {
      fontPx: subSize,
      color: BRAND.colors.white,
      weight: 800,
      align: 'left',
      baseline: 'top',
      strokeWidth: 6,
    });
  }

  ctx.fillStyle = accent;
  ctx.fillRect(0, H - 8, W, 8);

  const overlay = canvas.toBuffer('image/png');
  buf = await overlayCanvas(buf, overlay, W, H);
  return {
    buffer: buf,
    textRegion: { x: 0.46, y: 0.18, w: 0.52, h: 0.50 },
  };
}

module.exports = { compose, DEFAULT_SCENE };
