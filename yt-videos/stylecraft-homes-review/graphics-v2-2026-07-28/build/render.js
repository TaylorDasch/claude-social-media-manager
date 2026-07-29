#!/usr/bin/env node
/**
 * Stylecraft graphics v2 renderer.
 * Full-frame cards  -> opaque PNG  (fullframe-1080/)
 * Overlay cards     -> alpha PNG   (overlays-1080/)
 *
 * Usage: node render.js [id ...]      (no args = render everything)
 */
const path = require('path');
const fs = require('fs');
const { chromium } = require(
  '/Users/taylordasch_1/claude-video/branded-maps/node_modules/playwright'
);

const BUILD = __dirname;
const ROOT = path.resolve(BUILD, '..');
const OUT_FULL = path.join(ROOT, 'fullframe-1080');
const OUT_OV = path.join(ROOT, 'overlays-1080');

(async () => {
  const only = process.argv.slice(2);
  [OUT_FULL, OUT_OV].forEach(d => fs.mkdirSync(d, { recursive: true }));

  // Playwright's bundled chromium isn't installed on this machine; drive the
  // system Chrome instead (verified present at /Applications/Google Chrome.app).
  const browser = await chromium.launch({ channel: 'chrome' });
  const page = await browser.newPage({
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 1,
  });

  await page.goto('file://' + path.join(BUILD, 'stylecraft-graphics.html'));
  await page.waitForLoadState('networkidle');
  await page.evaluate(() => document.fonts.ready);

  // CRITICAL: omitBackground only drops Chrome's *default* white. An author-set
  // background on html/body still paints, which silently produces opaque RGB
  // overlays (colortype 2) that would black out the footage instead of layering
  // over it. Strip it — full-frame .stage carries its own opaque background.
  await page.evaluate(() => {
    document.documentElement.style.background = 'transparent';
    document.body.style.background = 'transparent';
  });
  await page.waitForTimeout(600);

  const ids = await page.evaluate(() =>
    [...document.querySelectorAll('.stage[id], .ov[id]')].map(el => ({
      id: el.id,
      overlay: el.classList.contains('ov'),
    }))
  );

  let n = 0;
  for (const { id, overlay } of ids) {
    if (only.length && !only.includes(id)) continue;
    const dir = overlay ? OUT_OV : OUT_FULL;
    const file = path.join(dir, `${id}.png`);
    await page.locator(`#${id}`).screenshot({
      path: file,
      omitBackground: overlay,
    });
    console.log(`${overlay ? 'alpha ' : 'opaque'}  ${id}.png`);
    n++;
  }

  await browser.close();
  console.log(`\n${n} graphics rendered.`);
})().catch(e => { console.error(e); process.exit(1); });
