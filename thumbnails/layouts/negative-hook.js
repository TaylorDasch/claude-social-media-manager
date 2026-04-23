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
  'Dark moody real estate photograph, empty suburban house at dusk, dramatic shadows, slightly ominous atmosphere, blue hour photography, 16:9';

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

  const offsetX = [0, -14, 18][variant % 3];
  const offsetY = [0, 20, -22][variant % 3];

  let buf = await applyGradientOverlay(background, W, H, [
    {
      x0: 0, y0: 0, x1: W, y1: H,
      stops: [
        { at: 0, color: 'rgba(75, 15, 15, 0.62)' },
        { at: 0.5, color: hexToRgba(BRAND.colors.midnight, 0.85) },
        { at: 1, color: 'rgba(10, 10, 20, 0.95)' },
      ],
    },
    {
      x0: 0, y0: 0, x1: W, y1: 0,
      stops: [
        { at: 0, color: hexToRgba(BRAND.colors.midnight, 0.7) },
        { at: 1, color: hexToRgba(BRAND.colors.midnight, 0.3) },
      ],
    },
  ]);

  buf = await compositeExpression(buf, expressionPath, {
    width: W,
    height: H,
    targetHeight: Math.round(H * 0.96),
    left: Math.round(W * 0.04),
    top: Math.round(H * 0.04),
    flip: false,
  });

  const { canvas, ctx } = createTextCanvas(W, H);

  // subtle caution stripe top
  ctx.save();
  ctx.globalAlpha = 0.6;
  for (let i = 0; i < W; i += 40) {
    ctx.fillStyle = i % 80 === 0 ? BRAND.colors.gold : 'rgba(0,0,0,0)';
    ctx.fillRect(i, 0, 40, 6);
  }
  ctx.restore();

  const textZoneX = Math.round(W * 0.42) + offsetX;
  const textZoneY = Math.round(H * 0.2) + offsetY;
  const textZoneW = Math.round(W * 0.55);
  const textZoneH = Math.round(H * 0.5);

  const heroSize = fitTextToWidth(ctx, text, textZoneW, textZoneH, 900, 320);

  // extra-heavy shadow for drama
  ctx.save();
  ctx.shadowColor = 'rgba(0,0,0,0.9)';
  ctx.shadowOffsetX = 6;
  ctx.shadowOffsetY = 8;
  ctx.shadowBlur = 16;
  drawHeroText(ctx, text, textZoneX, textZoneY, {
    fontPx: heroSize,
    color: BRAND.colors.gold,
    weight: 900,
    align: 'left',
    baseline: 'top',
    strokeWidth: 12,
    shadow: false,
  });
  ctx.restore();

  if (subtext) {
    const subSize = Math.round(heroSize * 0.32);
    ctx.save();
    ctx.globalAlpha = 0.85;
    drawHeroText(ctx, subtext, textZoneX, textZoneY + heroSize + 20, {
      fontPx: subSize,
      color: BRAND.colors.white,
      weight: 800,
      align: 'left',
      baseline: 'top',
      strokeWidth: 6,
    });
    ctx.restore();
  }

  const overlay = canvas.toBuffer('image/png');
  buf = await overlayCanvas(buf, overlay, W, H);
  return {
    buffer: buf,
    textRegion: { x: 0.40, y: 0.18, w: 0.58, h: 0.55 },
  };
}

module.exports = { compose, DEFAULT_SCENE };
