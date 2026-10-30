const { chromium } = require('playwright');
const vid = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({acceptDownloads:true, viewport:{width:1280,height:900}});
  const p = await ctx.newPage();
  p.on('request', r=>{ const u=r.url(); if(/snapyt\.app\/(wp-admin|dl|download|stream|proxy)|googlevideo/.test(u)) console.log('REQ',r.method(),u.slice(0,300),(r.postData()||'').slice(0,300)); });
  await p.goto('https://www.snapyt.app/', {waitUntil:'domcontentloaded'});
  await p.waitForTimeout(3000);
  await (await p.$('input')).fill('https://www.youtube.com/watch?v='+vid);
  await p.keyboard.press('Enter');
  await p.waitForSelector('text=Download Video', {timeout:60000});
  await p.waitForTimeout(3000);
  await p.selectOption('#fmt-select', process.argv[3] || '7'); await p.waitForTimeout(1500);
  const dlP = p.waitForEvent('download', {timeout:600000}).catch(e=>null);
  const popP = ctx.waitForEvent('page', {timeout:600000}).catch(e=>null);
  await p.click('text=Download Video');
  const [dl,pop] = await Promise.all([dlP, popP]);
  if (dl) { console.log('DOWNLOAD start'); await dl.saveAs('/tmp/claude-0/ak/video/'+vid+'.mp4'); console.log('SAVED', await dl.failure()); }
  if (pop) { await pop.waitForTimeout(3000); console.log('POPUP', pop.url().slice(0,400)); }
  await p.waitForTimeout(1000);
  await p.screenshot({path:'snap2.png'});
  await b.close();
})();
