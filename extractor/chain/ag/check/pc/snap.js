const { chromium } = require('playwright');
const vid = process.argv[2], out = process.argv[3], fmt = process.argv[4];
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({acceptDownloads:true, viewport:{width:1280,height:900}});
  const p = await ctx.newPage();
  await p.goto('https://www.snapyt.app/', {waitUntil:'domcontentloaded'});
  await p.waitForTimeout(3000);
  await (await p.$('input')).fill('https://www.youtube.com/watch?v='+vid);
  await p.keyboard.press('Enter');
  await p.waitForSelector('text=Download Video', {timeout:90000});
  await p.waitForTimeout(3000);
  const opts = await p.$$eval('#fmt-select option', os=>os.map(o=>o.value+'='+o.textContent.trim()));
  console.log('OPTS', JSON.stringify(opts));
  if (!fmt) { await b.close(); return; }
  await p.selectOption('#fmt-select', fmt); await p.waitForTimeout(1500);
  const dlP = p.waitForEvent('download', {timeout:900000}).catch(e=>null);
  await p.click('text=Download Video');
  const dl = await dlP;
  if (dl) { console.log('DOWNLOAD start'); await dl.saveAs(out); console.log('SAVED', await dl.failure()); }
  else console.log('NO DOWNLOAD');
  await b.close();
})();
