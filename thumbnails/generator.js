const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { BRAND } = require('./brand');
const { NanoBananaService } = require('./services/nano-banana');
const {
  registerFonts,
  loadBackground,
  makeSolidGradient,
  finalizePng,
  validateLegibility,
  applyGradientOverlay,
  hexToRgba,
} = require('./services/compositor');

const LAYOUTS = {
  'data-reveal': require('./layouts/data-reveal'),
  'vs-split': require('./layouts/vs-split'),
  'list-anchor': require('./layouts/list-anchor'),
  'negative-hook': require('./layouts/negative-hook'),
  'location-showcase': require('./layouts/location-showcase'),
};

const EXPRESSIONS = ['shocked', 'serious', 'pointing-right', 'pointing-left', 'smiling', 'arms-crossed'];

function wordCount(text) {
  return text.trim().split(/\s+/).filter(Boolean).length;
}

function loadConfig(configPath) {
  const base = {
    geminiApiKey: '',
    geminiApiKeyEnv: 'GEMINI_API_KEY',
    defaultModel: 'gemini-2.5-flash-image',
    hqModel: 'gemini-3-pro-image-preview',
    defaultVariants: 3,
    defaultCompositeMode: 'manual',
    expressionsDir: path.join(__dirname, 'assets/expressions/'),
    outputDir: path.join(__dirname, 'output/'),
    fontsDir: path.join(__dirname, 'assets/fonts/'),
  };
  if (configPath && fs.existsSync(configPath)) {
    try {
      const raw = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      Object.assign(base, raw);
    } catch (e) {
      console.warn(`[generator] could not read config ${configPath}: ${e.message}`);
    }
  }
  if (!base.geminiApiKey && base.geminiApiKeyEnv) {
    base.geminiApiKey = process.env[base.geminiApiKeyEnv] || '';
  }
  if (!path.isAbsolute(base.expressionsDir)) base.expressionsDir = path.resolve(__dirname, base.expressionsDir);
  if (!path.isAbsolute(base.outputDir)) base.outputDir = path.resolve(__dirname, base.outputDir);
  if (!path.isAbsolute(base.fontsDir)) base.fontsDir = path.resolve(__dirname, base.fontsDir);
  return base;
}

function resolveExpressionPath(config, name, flip = false) {
  const fn = flip ? `${name}-flipped.png` : `${name}.png`;
  return path.join(config.expressionsDir, fn);
}

function listAvailableExpressions(config) {
  if (!fs.existsSync(config.expressionsDir)) return [];
  return fs
    .readdirSync(config.expressionsDir)
    .filter(f => f.endsWith('.png') && !f.endsWith('-flipped.png'))
    .map(f => path.basename(f, '.png'));
}

async function getBackground({ layout, sceneOverride, bgImage, channel, nanoBanana, compositeMode, expressionPath, hq }) {
  const W = BRAND.dimensions.width;
  const H = BRAND.dimensions.height;

  if (bgImage) {
    if (!fs.existsSync(bgImage)) throw new Error(`--bg-image not found: ${bgImage}`);
    return loadBackground(fs.readFileSync(bgImage), W, H);
  }

  const scenePrompt = sceneOverride || LAYOUTS[layout].DEFAULT_SCENE;

  if (!nanoBanana) {
    console.warn('[generator] no Gemini API key available — falling back to solid gradient background');
    const accent = BRAND.channels[channel].accentColor;
    const grad = await makeSolidGradient(BRAND.colors.midnight, accent, W, H, 25);
    return loadBackground(grad, W, H);
  }

  try {
    let buf;
    if (compositeMode === 'ai' && fs.existsSync(expressionPath)) {
      buf = await nanoBanana.generateWithCharacter(scenePrompt, expressionPath, { hq });
    } else {
      buf = await nanoBanana.generateBackground(scenePrompt, { hq });
    }
    return loadBackground(buf, W, H);
  } catch (e) {
    console.warn(`[generator] Gemini image generation failed (${e.message}) — using solid gradient fallback`);
    const accent = BRAND.channels[channel].accentColor;
    const grad = await makeSolidGradient(BRAND.colors.midnight, accent, W, H, 25);
    return loadBackground(grad, W, H);
  }
}

async function generate(options) {
  const config = loadConfig(options.config);
  registerFonts(config.fontsDir);

  const {
    text,
    subtext,
    expression,
    layout,
    channel,
    scene,
    variants = config.defaultVariants,
    bgImage,
    leftImage,
    rightImage,
    leftLabel,
    rightLabel,
    outputDir,
    compositeMode = config.defaultCompositeMode,
    hq = false,
  } = options;

  if (!text || typeof text !== 'string') throw new Error('--text is required');
  if (wordCount(text) > 4) {
    throw new Error(
      `Thumbnail text must be 4 words or fewer. Current: ${wordCount(text)} words. Strong thumbnails use 2-3 words max.`
    );
  }
  if (!LAYOUTS[layout]) {
    throw new Error(`Unknown layout "${layout}". Valid: ${Object.keys(LAYOUTS).join(', ')}`);
  }
  if (!BRAND.channels[channel]) {
    throw new Error(`Unknown channel "${channel}". Valid: living, investing`);
  }
  if (!EXPRESSIONS.includes(expression)) {
    const avail = listAvailableExpressions(config);
    throw new Error(
      `Unknown expression "${expression}". Valid: ${EXPRESSIONS.join(', ')}.\nInstalled on disk: ${avail.join(', ') || '(none — run setup-expressions)'}`
    );
  }

  const expressionPath = resolveExpressionPath(config, expression);
  if (!fs.existsSync(expressionPath)) {
    console.warn(
      `[generator] Expression photo not found: ${expressionPath}\n  Run: node cli.js setup-expressions --input ./raw-photos/\n  Proceeding without face composite.`
    );
  }

  const finalOutputDir = outputDir || config.outputDir;
  if (!fs.existsSync(finalOutputDir)) fs.mkdirSync(finalOutputDir, { recursive: true });

  const nanoBanana = config.geminiApiKey
    ? new NanoBananaService(config.geminiApiKey, config.defaultModel, config.hqModel)
    : null;

  if (!nanoBanana) {
    console.warn('[generator] GEMINI_API_KEY not set — backgrounds will use solid gradient fallback');
  }

  const results = [];
  const ts = Date.now();

  const W = BRAND.dimensions.width;
  const H = BRAND.dimensions.height;

  // When Nano Banana places Taylor in the scene (compositeMode=ai),
  // pass a null expressionPath so the layout skips its own composite step.
  const expressionForLayout = compositeMode === 'ai' ? null : expressionPath;

  const composeArgs = (bg, v) => ({
    background: bg,
    expressionPath: expressionForLayout,
    text,
    subtext,
    channel,
    variant: v,
    leftImage: leftImage ? fs.readFileSync(leftImage) : null,
    rightImage: rightImage ? fs.readFileSync(rightImage) : null,
    leftLabel,
    rightLabel,
  });

  const unwrap = (res) => (res && res.buffer ? res : { buffer: res, textRegion: null });

  for (let v = 0; v < variants; v++) {
    try {
      const background = await getBackground({
        layout,
        sceneOverride: scene,
        bgImage,
        channel,
        nanoBanana,
        compositeMode,
        expressionPath,
        hq,
      });

      const layoutMod = LAYOUTS[layout];
      let result = unwrap(await layoutMod.compose(composeArgs(background, v)));
      let buf = await finalizePng(result.buffer);

      // WCAG-style contrast check over the actual text region.
      let legibility = await validateLegibility(buf, result.textRegion);
      let attempts = 0;
      let currentBg = background;
      while (!legibility.ok && attempts < 2) {
        attempts++;
        console.warn(
          `[generator] v${v + 1}: low contrast (${legibility.contrast?.toFixed(2) || 'n/a'}) — darkening background pass ${attempts}`
        );
        // Progressively darken the background under the text region.
        const regionX0 = result.textRegion ? result.textRegion.x * W : 0;
        const regionX1 = result.textRegion ? (result.textRegion.x + result.textRegion.w) * W : W;
        currentBg = await applyGradientOverlay(currentBg, W, H, [
          {
            x0: regionX0, y0: 0, x1: regionX1, y1: 0,
            stops: [
              { at: 0, color: hexToRgba(BRAND.colors.midnight, 0.55 + 0.15 * attempts) },
              { at: 1, color: hexToRgba(BRAND.colors.midnight, 0.55 + 0.15 * attempts) },
            ],
          },
          {
            x0: 0, y0: 0, x1: W, y1: 0,
            stops: [
              { at: 0, color: hexToRgba(BRAND.colors.midnight, 0.4 + 0.1 * attempts) },
              { at: 1, color: hexToRgba(BRAND.colors.midnight, 0.2 + 0.1 * attempts) },
            ],
          },
        ]);
        result = unwrap(await layoutMod.compose(composeArgs(currentBg, v)));
        buf = await finalizePng(result.buffer);
        legibility = await validateLegibility(buf, result.textRegion);
      }

      if (!legibility.ok) {
        console.warn(
          `[generator] v${v + 1}: contrast still below 4.5:1 (${legibility.contrast?.toFixed(2) || 'n/a'}) after ${attempts} recomposites — shipping anyway`
        );
      }

      const outPath = path.join(finalOutputDir, `${ts}_${layout}_${channel}_v${v + 1}.png`);
      fs.writeFileSync(outPath, buf);
      console.log(`[generator] wrote ${outPath} (contrast=${legibility.contrast?.toFixed(2) || 'n/a'}, attempts=${attempts + 1})`);
      results.push({ path: outPath, variant: v + 1, legibility, attempts: attempts + 1 });
    } catch (e) {
      console.error(`[generator] variant ${v + 1} failed: ${e.message}\n${e.stack}`);
    }
  }

  return results;
}

module.exports = { generate, LAYOUTS, EXPRESSIONS, loadConfig, listAvailableExpressions };
