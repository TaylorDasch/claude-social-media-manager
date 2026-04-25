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
  'Modern Texas new construction homes, bright daylight, wide angle architectural photography, clean suburban street, 16:9';

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

  const offsetX = [0, -18, 22][variant % 3];
  const offsetY = [0, 14, -18][variant % 3];

  let buf = await applyGradientOverlay(background, W, H, [
    {
      x0: 0, y0: 0, x1: W, y1: 0,
      stops: [
        { at: 0, color: hexToRgba(BRAND.colors.midnight, 0.82) },
        { at: 0.5, color: hexToRgba(BRAND.colors.midnight, 0.55) },
        { at: 1, color: hexToRgba(BRAND.colors.midnight, 0.4) },
      ],
    },
  ]);

  buf = await compositeExpression(buf, expressionPath, {
    width: W,
    height: H,
    targetHeight: Math.round(H * 0.98),
    left: -Math.round(W * 0.04),
    top: Math.round(H * 0.02),
    flip: false,
  });

  const { canvas, ctx } = createTextCanvas(W, H);

  const textZoneX = Math.round(W * 0.54) + offsetX;
  const textZoneY = Math.round(H * 0.16) + offsetY;
  const textZoneW = Math.round(W * 0.44);
  const textZoneH = Math.round(H * 0.52);

  const heroSize = fitTextToWidth(ctx, text, textZoneW, textZoneH, 900, 320);
  drawHeroText(ctx, text, textZoneX, textZoneY, {
    fontPx: heroSize,
    color: accent,
    weight: 900,
    align: 'left',
    baseline: 'top',
    strokeWidth: 10,
  });

  if (subtext) {
    const subSize = Math.round(heroSize * 0.3);
    drawHeroText(ctx, subtext, textZoneX, textZoneY + heroSize + 18, {
      fontPx: subSize,
      color: BRAND.colors.white,
      weight: 800,
      align: 'left',
      baseline: 'top',
      strokeWidth: 6,
    });
  }

  ctx.fillStyle = accent;
  ctx.fillRect(0, H - 3, W, 3);

  const overlay = canvas.toBuffer('image/png');
  buf = await overlayCanvas(buf, overlay, W, H);
  return {
    buffer: buf,
    textRegion: { x: 0.52, y: 0.14, w: 0.46, h: 0.56 },
  };
}

module.exports = { compose, DEFAULT_SCENE };
