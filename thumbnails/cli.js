#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { Command } = require('commander');
const { generate, LAYOUTS, EXPRESSIONS, loadConfig } = require('./generator');
const { processExpressionPhoto } = require('./services/background-remover');

// Load GEMINI_API_KEY from ~/shared-keys.env if not already set
function loadSharedKeys() {
  if (process.env.GEMINI_API_KEY) return;
  const sharedPath = path.join(require('os').homedir(), 'shared-keys.env');
  if (!fs.existsSync(sharedPath)) return;
  try {
    const txt = fs.readFileSync(sharedPath, 'utf8');
    for (const line of txt.split('\n')) {
      const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
      if (m && !process.env[m[1]]) {
        let val = m[2];
        if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
        process.env[m[1]] = val;
      }
    }
  } catch {}
}
loadSharedKeys();

const program = new Command();
program
  .name('yt-thumb')
  .description('YouTube thumbnail generator for Living in Temple + Investing in Temple')
  .version('1.0.0');

program
  .command('generate')
  .description('Generate a thumbnail (or variants)')
  .requiredOption('--text <text>', 'Hero text (1–4 words)')
  .option('--subtext <text>', 'Secondary text (price, stat, location)')
  .requiredOption('--expression <name>', `One of: ${EXPRESSIONS.join(', ')}`)
  .requiredOption('--layout <name>', `One of: ${Object.keys(LAYOUTS).join(', ')}`)
  .requiredOption('--channel <name>', 'living or investing')
  .option('--scene <prompt>', 'Custom Nano Banana scene prompt (overrides layout default)')
  .option('--variants <n>', 'Number of variants to generate', v => parseInt(v, 10))
  .option('--left-image <path>', 'vs-split: left side image')
  .option('--right-image <path>', 'vs-split: right side image')
  .option('--left-label <text>', 'vs-split: left label')
  .option('--right-label <text>', 'vs-split: right label')
  .option('--bg-image <path>', 'Skip Nano Banana, use this local image as background')
  .option('--output <dir>', 'Output directory')
  .option('--composite-mode <mode>', 'ai (Nano Banana places Taylor) or manual (Sharp composites)', 'manual')
  .option('--hq', 'Use Nano Banana Pro (higher quality, slower, ~3.5x cost)', false)
  .option('--config <path>', 'Path to config.json', path.join(__dirname, 'config.json'))
  .action(async (opts) => {
    try {
      const results = await generate({
        text: opts.text,
        subtext: opts.subtext,
        expression: opts.expression,
        layout: opts.layout,
        channel: opts.channel,
        scene: opts.scene,
        variants: opts.variants,
        bgImage: opts.bgImage,
        leftImage: opts.leftImage,
        rightImage: opts.rightImage,
        leftLabel: opts.leftLabel,
        rightLabel: opts.rightLabel,
        outputDir: opts.output,
        compositeMode: opts.compositeMode,
        hq: opts.hq,
        config: opts.config,
      });
      if (results.length === 0) {
        console.error('No thumbnails generated.');
        process.exit(1);
      }
      console.log(`\nDone — generated ${results.length} thumbnail${results.length > 1 ? 's' : ''}:`);
      for (const r of results) console.log(`  ${r.path}`);
    } catch (e) {
      console.error(`Error: ${e.message}`);
      process.exit(1);
    }
  });

program
  .command('setup-expressions')
  .description("Process Taylor's raw expression photos (bg-remove, crop, flip)")
  .requiredOption('--input <dir>', 'Directory with raw expression photos')
  .option('--output <dir>', 'Where to write processed PNGs', path.join(__dirname, 'assets/expressions'))
  .action(async (opts) => {
    const input = path.resolve(opts.input);
    const output = path.resolve(opts.output);
    if (!fs.existsSync(input)) {
      console.error(`Input dir not found: ${input}`);
      process.exit(1);
    }
    if (!fs.existsSync(output)) fs.mkdirSync(output, { recursive: true });

    const files = fs.readdirSync(input).filter(f => /\.(jpg|jpeg|png|webp)$/i.test(f));
    if (files.length === 0) {
      console.error(`No image files found in ${input}`);
      process.exit(1);
    }

    for (const f of files) {
      const full = path.join(input, f);
      console.log(`Processing ${f}...`);
      try {
        const { transparentPath, flippedPath } = await processExpressionPhoto(full, output);
        console.log(`  -> ${transparentPath}`);
        console.log(`  -> ${flippedPath}`);
      } catch (e) {
        console.error(`  Failed: ${e.message}`);
      }
    }
    console.log(`\nDone. Drop-in expressions: ${EXPRESSIONS.join(', ')}`);
  });

program
  .command('list-layouts')
  .description('List available layouts')
  .action(() => {
    for (const [name, mod] of Object.entries(LAYOUTS)) {
      console.log(`\n${name}`);
      console.log(`  default scene: ${mod.DEFAULT_SCENE || '(none)'}`);
    }
  });

program
  .command('check')
  .description('Check environment (fonts, expressions, API key)')
  .option('--config <path>', 'Path to config.json', path.join(__dirname, 'config.json'))
  .action((opts) => {
    const cfg = loadConfig(opts.config);
    console.log('Config:');
    console.log(`  expressionsDir: ${cfg.expressionsDir}`);
    console.log(`  outputDir:      ${cfg.outputDir}`);
    console.log(`  fontsDir:       ${cfg.fontsDir}`);
    console.log(`  default model:  ${cfg.defaultModel}`);
    console.log(`  hq model:       ${cfg.hqModel}`);
    console.log(`  GEMINI_API_KEY: ${cfg.geminiApiKey ? 'SET' : 'MISSING'}`);

    const fonts = fs.existsSync(cfg.fontsDir) ? fs.readdirSync(cfg.fontsDir).filter(f => /\.(ttf|otf)$/i.test(f)) : [];
    console.log(`  fonts found:    ${fonts.length ? fonts.join(', ') : '(none — download Montserrat)'}`);

    const exprs = fs.existsSync(cfg.expressionsDir)
      ? fs.readdirSync(cfg.expressionsDir).filter(f => f.endsWith('.png') && !f.endsWith('-flipped.png')).map(f => path.basename(f, '.png'))
      : [];
    console.log(`  expressions:    ${exprs.length ? exprs.join(', ') : '(none — run setup-expressions)'}`);

    console.log('\nLayouts: ' + Object.keys(LAYOUTS).join(', '));
    console.log('Channels: living, investing');
  });

program.parse(process.argv);
