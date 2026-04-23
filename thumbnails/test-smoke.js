#!/usr/bin/env node
// Smoke test: renders one thumbnail per layout using a solid gradient background
// (skips Nano Banana for speed). Verifies all layouts compose without throwing.
// Run: node test-smoke.js

const fs = require('fs');
const path = require('path');
const { generate } = require('./generator');
const { BRAND } = require('./brand');
const { makeSolidGradient, loadBackground } = require('./services/compositor');

async function makeFixtureBg() {
  // Pre-render a deterministic background image file so --bg-image works
  const W = BRAND.dimensions.width;
  const H = BRAND.dimensions.height;
  const grad = await makeSolidGradient(BRAND.colors.midnight, BRAND.colors.emerald, W, H, 25);
  const out = path.join(__dirname, 'output', '__test_bg.png');
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, grad);
  return out;
}

async function main() {
  const bg = await makeFixtureBg();
  const outDir = path.join(__dirname, 'output', '__smoke_test');
  fs.mkdirSync(outDir, { recursive: true });

  const cases = [
    { layout: 'data-reveal', text: '17 DAYS', subtext: '$230K', expression: 'shocked', channel: 'living' },
    { layout: 'list-anchor', text: 'TOP 3', subtext: 'BUILDERS', expression: 'pointing-right', channel: 'investing' },
    { layout: 'negative-hook', text: 'RATE TRAP', subtext: 'WHAT THEY HIDE', expression: 'serious', channel: 'living' },
    { layout: 'location-showcase', text: 'CANYON CREEK', subtext: 'Best Kept Secret', expression: 'smiling', channel: 'living' },
    { layout: 'vs-split', text: 'VS', leftLabel: 'BELTON', rightLabel: 'TEMPLE', expression: 'arms-crossed', channel: 'living' },
  ];

  const results = [];
  for (const c of cases) {
    try {
      const r = await generate({
        ...c,
        bgImage: bg,
        variants: 1,
        outputDir: outDir,
      });
      if (r.length === 0) throw new Error('no output');
      const contrast = r[0].legibility.contrast;
      console.log(`  PASS ${c.layout} — contrast=${contrast?.toFixed(2) || 'n/a'} attempts=${r[0].attempts}`);
      results.push({ layout: c.layout, ok: true });
    } catch (e) {
      console.log(`  FAIL ${c.layout} — ${e.message}`);
      results.push({ layout: c.layout, ok: false, error: e.message });
    }
  }

  // Test word count rejection
  try {
    await generate({
      layout: 'data-reveal',
      text: 'This has too many words here',
      expression: 'shocked',
      channel: 'living',
      bgImage: bg,
      variants: 1,
      outputDir: outDir,
    });
    console.log('  FAIL word-count-rejection — did not throw');
    results.push({ layout: 'word-count-rejection', ok: false });
  } catch (e) {
    if (/4 words or fewer/.test(e.message)) {
      console.log('  PASS word-count-rejection');
      results.push({ layout: 'word-count-rejection', ok: true });
    } else {
      console.log(`  FAIL word-count-rejection — wrong error: ${e.message}`);
      results.push({ layout: 'word-count-rejection', ok: false });
    }
  }

  // Test unknown layout rejection
  try {
    await generate({
      layout: 'nonexistent',
      text: 'TEST',
      expression: 'shocked',
      channel: 'living',
      bgImage: bg,
      variants: 1,
      outputDir: outDir,
    });
    console.log('  FAIL unknown-layout-rejection — did not throw');
    results.push({ layout: 'unknown-layout-rejection', ok: false });
  } catch (e) {
    if (/Unknown layout/.test(e.message)) {
      console.log('  PASS unknown-layout-rejection');
      results.push({ layout: 'unknown-layout-rejection', ok: true });
    } else {
      console.log(`  FAIL unknown-layout-rejection — wrong error: ${e.message}`);
      results.push({ layout: 'unknown-layout-rejection', ok: false });
    }
  }

  const passed = results.filter(r => r.ok).length;
  const total = results.length;
  console.log(`\n${passed}/${total} tests passed`);
  process.exit(passed === total ? 0 : 1);
}

main().catch(e => {
  console.error(e);
  process.exit(1);
});
