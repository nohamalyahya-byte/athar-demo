const { chromium } = require('playwright');
const fs = require('fs');
// Usage: node shot_site.js <site index.html> <fonts.css> <output dir>
(async () => {
  const [site, fontsCss, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  // Block external requests; fonts are injected from local files instead
  await page.route(/^https?:\/\//, r => r.abort());
  await page.goto('file://' + site);
  // Resolve the stylesheet's relative font URLs against its own folder
  const css = fs.readFileSync(fontsCss, 'utf8').replace(/url\((?![a-z]+:)/g, 'url(file://' + require('path').dirname(fontsCss) + '/');
  await page.addStyleTag({ content: css });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  await page.screenshot({ path: out + '/site_top.png' });
  await page.screenshot({ path: out + '/site_full.png', fullPage: true });
  await browser.close();
})();
