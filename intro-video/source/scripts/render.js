// Render the intro page frame-by-frame into JPEG frames, split across parallel workers
const { chromium } = require('playwright');
const path = require('path');

const [pageFile, outDir, fpsArg, durArg, workersArg] = process.argv.slice(2);
const FPS = +fpsArg || 30;
const DURATION = +durArg || 69.5;
const WORKERS = +workersArg || 4;
const total = Math.round(FPS * DURATION);

async function worker(browser, id) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('pageerror', e => console.error(`[w${id}] PAGE ERROR`, e.message));
  await page.goto('file://' + pageFile);
  await page.evaluate(() => window.ready);
  for (let f = id; f < total; f += WORKERS) {
    await page.evaluate(t => window.seek(t), f / FPS);
    await page.screenshot({ path: path.join(outDir, `f${String(f).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 95 });
    if (id === 0 && f % (WORKERS * 60) === 0) console.log(`frame ${f}/${total}`);
  }
}

(async () => {
  const browser = await chromium.launch();
  const t0 = Date.now();
  await Promise.all(Array.from({ length: WORKERS }, (_, i) => worker(browser, i)));
  await browser.close();
  console.log(`done: ${total} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})();
