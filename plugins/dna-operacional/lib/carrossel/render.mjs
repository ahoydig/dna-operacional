import { chromium } from 'playwright';
import path from 'path'; import fs from 'fs';
const dir = process.argv[2];
const files = fs.readdirSync(dir).filter(f => /^\d\d\.html$/.test(f)).sort();
const b = await chromium.launch();
for (const f of files) {
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.resolve(dir, f), { waitUntil: 'networkidle' });
  try { await p.evaluate(() => document.fonts.ready); } catch {}
  await p.waitForTimeout(2200);
  const out = path.join(dir, f.replace('.html','.png'));
  await p.screenshot({ path: out, clip: { x:0, y:0, width:1080, height:1350 } });
  console.log('rendered', f); await p.close();
}
await b.close(); console.log('DONE');
