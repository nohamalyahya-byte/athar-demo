// Render selected timestamps of the intro page to PNGs for review
const { chromium } = require('playwright');
(async () => {
  const [page_, outDir, ...times] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await page.goto('file://' + page_);
  await page.evaluate(() => window.ready);
  for (const t of times) {
    await page.evaluate(t => window.seek(t), +t);
    await page.screenshot({ path: `${outDir}/p_${t}.png` });
  }
  await browser.close();
})();
