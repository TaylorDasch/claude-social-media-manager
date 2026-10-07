// Renders each desk sheet HTML to a Letter-size PDF and a PNG preview.
const { chromium } = require('playwright');
const path = require('path');
const sheets = ['01-daily-power-sheet', '02-weekly-scorecard', '03-goals-pipeline-board'];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 } });
  for (const s of sheets) {
    await page.goto('file://' + path.resolve(__dirname, s + '.html'));
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: path.resolve(__dirname, s + '.pdf'), format: 'Letter', printBackground: true, preferCSSPageSize: true });
    await page.screenshot({ path: path.resolve(__dirname, 'preview-' + s + '.png'), fullPage: true });
    console.log('built', s);
  }
  await browser.close();
})();
