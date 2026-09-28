/* Run with Node.js + Playwright. All runtime files stay in workflow/.review-check. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const {chromium} = require('playwright');
const appDir = path.resolve(__dirname, '..');
const root = path.resolve(appDir, '../../..');
const scratch = path.join(root, 'workflow/.review-check');
const publicFiles = new Set(fs.readFileSync(path.join(root, 'public-files.txt'), 'utf8').trim().split('\n'));
fs.mkdirSync(scratch, {recursive: true});
process.env.TMPDIR = scratch;
const prefixes = ['/review-preview/repository/', '/another-site/repository/'];
const mime = {'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json',
  '.css':'text/css','.webp':'image/webp','.png':'image/png','.md':'text/plain; charset=utf-8'};
const server = http.createServer((req, res) => {
  const pathname = decodeURIComponent(new URL(req.url, 'http://test.invalid').pathname);
  const prefix = prefixes.find(p => pathname.startsWith(p));
  if (req.method !== 'GET' || !prefix) {res.writeHead(404).end(); return;}
  let file = path.resolve(root, pathname.slice(prefix.length));
  if (!file.startsWith(root + path.sep)) {res.writeHead(403).end(); return;}
  try {
    if (fs.statSync(file).isDirectory()) file = path.join(file, 'index.html');
    if (!publicFiles.has(path.relative(root, file))) {res.writeHead(404).end(); return;}
    res.writeHead(200, {'Content-Type':mime[path.extname(file)] || 'application/octet-stream'});
    fs.createReadStream(file).pipe(res);
  } catch {res.writeHead(404).end();}
});
const checks = [], errors = [], requests = [];
let browser;
async function check(name, fn) {await fn();checks.push(name);console.log('PASS:', name);}
async function settled(page) {await page.waitForFunction(() => state.current && state.loaded && !state.busy && !state.saving && state.editSeq === state.savedSeq);}
async function open(page, url) {await page.goto(url);await settled(page);}
async function point(page, x, y) {
  return page.evaluate(({x,y}) => {const p = new DOMPoint(x,y).matrixTransform(document.getElementById('overlay').getScreenCTM());return {x:p.x,y:p.y};}, {x,y});
}
async function dragBox(page, x, y, w, h) {
  await page.locator('#addBox').click();
  const a = await point(page,x,y), b = await point(page,x+w,y+h);
  await page.mouse.move(a.x,a.y);await page.mouse.down();await page.mouse.move(b.x,b.y,{steps:5});await page.mouse.up();
}
async function downloadRows(page, selector) {
  const event = page.waitForEvent('download');await page.locator(selector).click();
  const download = await event, stream = await download.createReadStream(), chunks = [];
  for await (const chunk of stream) chunks.push(chunk);
  const text = Buffer.concat(chunks).toString('utf8');
  return {filename:download.suggestedFilename(), text, rows:text.trim() ? text.trim().split('\n').map(JSON.parse) : []};
}
(async () => {
  await new Promise((resolve,reject) => {server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
  const origin = `http://127.0.0.1:${server.address().port}`;
  const url = origin + prefixes[0] + 'workflow/assets/human-review/';
  browser = await chromium.launch({headless:true, executablePath:process.env.CHROME_BIN || undefined,
    downloadsPath:scratch, args:['--disable-breakpad','--disable-crash-reporter']});
  const context = await browser.newContext({viewport:{width:1440,height:1000},acceptDownloads:true});
  context.on('request', r => requests.push({url:r.url(),method:r.method()}));
  context.on('page', p => {p.on('pageerror', e => errors.push(e.message));p.on('dialog', d => d.accept());});
  const page = await context.newPage();
  await check('subpath startup, 8 sample pages, 16 images and public evidence links', async () => {
    await open(page,url);
    assert.equal(await page.evaluate(() => state.current.page_id),'demo-1994-p01');
    assert.equal((await page.evaluate(() => api('/api/stats'))).counts.unreviewed,8);
    const samples = JSON.parse(fs.readFileSync(path.join(appDir,'samples.json')));
    for (const row of samples.pages) {
      for (const [view, relative] of Object.entries(row.images)) {
        const response = await context.request.get(new URL(relative,url).href);
        assert.equal(response.status(),200);
        const hash = require('node:crypto').createHash('sha256').update(await response.body()).digest('hex');
        assert.equal(hash,view==='before'?row.safe_sha256:row.sha256);
      }
      for (const relative of Object.values(row.evidence)) assert.equal((await context.request.get(new URL(relative,url).href)).status(),200);
    }
    for (const href of await page.locator('a').evaluateAll(els=>els.map(el=>el.href))) assert.equal((await context.request.get(href)).status(),200);
    // Follow the actual source links through the integrated reading route.
    for (const prefix of prefixes) {
      const route = [
        ['README.md', 'workflow/README.md'],
        ['workflow/README.md', 'demo.md'],
        ['workflow/demo.md', 'assets/human-review/index.html'],
        ['workflow/assets/human-review/index.html', '../../../history/cases/03-review-and-repair.md'],
      ];
      for (const [source, ref] of route) {
        const sourceURL = origin + prefix + source;
        const sourceResponse = await context.request.get(sourceURL);
        assert.equal(sourceResponse.status(), 200);
        const body = await sourceResponse.text();
        assert(body.includes(source.endsWith('.html') ? `href="${ref}"` : `](${ref})`));
        const target = new URL(ref, sourceURL);
        assert(target.pathname.startsWith(prefix));
        const response = await context.request.get(target.href);
        assert.equal(response.status(), 200);
        assert.equal(await response.text(), fs.readFileSync(path.resolve(root, source, '..', ref), 'utf8'));
      }
      for (const ref of await page.locator('nav[aria-label="Related documents"] a').evaluateAll(els=>els.map(el=>el.getAttribute('href')))) {
        const target = new URL(ref, origin + prefix + 'workflow/assets/human-review/');
        assert(target.pathname.startsWith(prefix));
        assert.equal((await context.request.get(target.href)).status(), 200);
      }
      assert.equal((await context.request.get(origin + prefix + '.nojekyll')).status(), 200);
      assert.equal((await context.request.get(origin + prefix + 'workflow/.review-check/browser-results.json')).status(), 404);
    }
  });
  await check('before/after comparison is read-only on input and preserves result binding', async () => {
    const before = await page.evaluate(() => payload());
    await page.locator('#beforeView').click();await settled(page);
    assert((await page.locator('#pageImage').getAttribute('src')).includes('demo-source-safe'));
    assert(await page.locator('#addBox').isDisabled());assert(await page.locator('#note').isDisabled());assert(!(await page.locator('#overlay').isVisible()));
    await page.locator('#viewport').focus();await page.keyboard.press('ArrowRight');
    assert.deepEqual(await page.evaluate(() => payload()),before);
    await page.locator('#afterView').click();await settled(page);
    assert((await page.locator('#pageImage').getAttribute('src')).includes('/final/'));
    assert.deepEqual(await page.evaluate(() => payload()),before);
  });
  await check('memo/issues autosave and typing shortcuts do not navigate', async () => {
    await page.locator('#note').fill('Public sample 검토 메모 <검토>');
    await page.locator('#note').press('Space');await page.locator('#note').press('ArrowRight');
    await page.locator('#issueTypes input[value=token_legibility]').check();await settled(page);
    assert.equal(await page.evaluate(()=>state.current.page_id),'demo-1994-p01');
    assert.equal(await page.evaluate(()=>state.current.status),'issue');
    assert((await page.evaluate(()=>state.current.note)).includes('<검토>'));
  });
  await check('actual pointer BBOX draw, move and resize in image pixels', async () => {
    await dragBox(page,500,650,500,250);await settled(page);
    let box = await page.evaluate(()=>state.current.boxes[0]);
    for(const [key,value] of Object.entries({x:500,y:650,width:500,height:250})) assert(Math.abs(box[key]-value)<=1);
    const center = await point(page,750,775), next = await point(page,850,875);
    await page.mouse.move(center.x,center.y);await page.mouse.down();await page.mouse.move(next.x,next.y,{steps:5});await page.mouse.up();await settled(page);
    box = await page.evaluate(()=>state.current.boxes[0]);assert(Math.abs(box.x-600)<=2);assert(Math.abs(box.y-750)<=2);
    const handle = page.locator('.handle[data-handle=se]'), rect = await handle.boundingBox();
    const target = await point(page,1250,1150);
    await page.mouse.move(rect.x+rect.width/2,rect.y+rect.height/2);await page.mouse.down();await page.mouse.move(target.x,target.y,{steps:5});await page.mouse.up();await settled(page);
    box = await page.evaluate(()=>state.current.boxes[0]);assert(Math.abs(box.width-650)<=3);assert(Math.abs(box.height-400)<=3);
  });
  await check('zoom/rotation preserve coordinates and rotated pointer drawing', async () => {
    const before = await page.evaluate(()=>state.current.boxes);
    await page.locator('#zoomIn').click();await page.locator('#zoomOut').click();await page.locator('#rotateButton').click();
    assert.deepEqual(await page.evaluate(()=>state.current.boxes),before);
    assert.equal(await page.evaluate(()=>state.rotation),270);
    await dragBox(page,1300,1200,300,200);await settled(page);
    const box = await page.evaluate(()=>state.current.boxes.at(-1));
    for(const [key,value] of Object.entries({x:1300,y:1200,width:300,height:200})) assert(Math.abs(box[key]-value)<=1);
    await page.reload();await settled(page);assert.equal(await page.evaluate(()=>state.current.boxes.length),2);
    assert((await page.locator('#note').inputValue()).includes('Public sample 검토 메모'));
  });
  await check('pending BBOX survives reload; name confirmation, empty guard and IME protection', async () => {
    await page.locator('#reviewStatus').selectOption('needs_review');await settled(page);await page.locator('#fitButton').click();
    await dragBox(page,1600,1400,260,180);
    const pending = await page.evaluate(()=>state.pendingBox);assert(pending);
    await page.reload();await page.waitForFunction(()=>state.loaded && state.pendingBox);
    assert.equal(await page.evaluate(()=>state.pendingBox),pending);
    await page.locator('#confirmBox').click();await settled(page);
    await page.locator('#issueNext').click();assert.equal(await page.evaluate(()=>state.current.page_id),'demo-1994-p01');
    const fields = page.locator('[data-name-input]');
    for(let i=0;i<await fields.count();i++) await fields.nth(i).fill('가상 이름 검토');
    await fields.last().dispatchEvent('keydown',{key:'Enter',isComposing:true,keyCode:229});
    assert(await fields.last().evaluate(el=>document.activeElement===el));
    await fields.last().press('Enter');await settled(page);
    assert.equal(await page.evaluate(()=>state.selected),null);
  });
  await check('history retains annotations when OK clears boxes; JSONL downloads', async () => {
    await page.locator('#historyDetails').evaluate(el=>el.open=true);
    await page.waitForFunction(()=>document.querySelectorAll('#historyList details').length>0);
    await page.locator('#okNext').click();await settled(page);
    assert.equal(await page.evaluate(()=>state.current.status),'ok');assert.equal(await page.evaluate(()=>state.current.boxes.length),0);
    const history = await page.evaluate(()=>api('/api/history?page_id=demo-1994-p01'));
    assert(history.items.some(item=>item.snapshot.boxes.length===3));
    const reviews = await downloadRows(page,'#exportButton');assert.equal(reviews.rows.length,8);
    assert(reviews.rows.every(row=>row.source.kind==='public-sample'&&row.annotation_target==='final'));
    assert(!reviews.text.includes('/'+'Users/'));
    await page.locator('#historyDetails').evaluate(el=>el.open=true);
    const exported = await downloadRows(page,'#exportHistory');assert(exported.rows.length>=history.total);
    assert(exported.rows.some(row=>row.event==='before_edit'&&row.snapshot.boxes.length===3));
  });
  await check('search/filter/empty results, pagination and state-preserving navigation', async () => {
    await page.locator('#browseButton').click();await page.locator('#search').fill('없는-샘플');
    await page.waitForFunction(()=>document.getElementById('listSummary').textContent.startsWith('0'));
    await page.locator('#search').fill('2003');
    await page.waitForFunction(()=>document.querySelectorAll('.file-entry').length===3);
    await page.locator('#filter').selectOption('ok');
    await page.waitForFunction(()=>document.querySelectorAll('.file-entry').length===0);
    await page.locator('#filter').selectOption('');
    await page.waitForFunction(()=>document.querySelectorAll('.file-entry').length===3);
    await page.locator('.file-entry').first().click();await settled(page);
    assert.equal(await page.evaluate(()=>state.current.page_id),'demo-2003-p05');
    await page.locator('#next').click();await settled(page);assert.equal(await page.evaluate(()=>state.current.page_id),'demo-2003-p07');
    await page.locator('#previous').click();await settled(page);assert.equal(await page.evaluate(()=>state.current.status),'unreviewed');
    const list = await page.evaluate(()=>api('/api/images?limit=2&edge=last'));
    assert.equal(list.offset,6);assert.equal(list.items.length,2);
  });
  await check('atomic revision conflict preserves the newer tab and downloadable draft', async () => {
    const other = await context.newPage();await open(other,url);
    const current = await other.evaluate(()=>payload());
    await page.evaluate(body=>api('/api/review',{...body,note:'먼저 저장한 탭'}),current);
    await other.locator('#note').fill('충돌한 탭의 보관 초안');
    await other.waitForFunction(()=>state.conflict);
    assert.equal((await page.evaluate(()=>api('/api/image?page_id=demo-2003-p05'))).note,'먼저 저장한 탭');
    const draft = await downloadRows(other,'#downloadDraft');assert.equal(draft.rows[0].note,'충돌한 탭의 보관 초안');
    await other.locator('#loadServer').click();await settled(other);
    assert.equal(await other.locator('#note').inputValue(),'먼저 저장한 탭');await other.close();
  });
  await check('invalid geometry rejected and concurrent saves are serialized', async () => {
    const base = await page.evaluate(()=>api('/api/image?page_id=demo-2003-p15'));
    const invalid = await page.evaluate(async body=>{
      try{await api('/api/review',{...body,status:'issue',boxes:[{id:'invalid',name:'',color:0,x:2400,y:0,width:100,height:100}]});return false;}catch(error){return error.status===400;}
    },base);assert(invalid);
    const statuses = await page.evaluate(async body=>{
      const replies = await Promise.allSettled([api('/api/review',{...body,note:'동시 저장 A'}),api('/api/review',{...body,note:'동시 저장 B'})]);
      return replies.map(r=>r.status==='fulfilled'?'saved':r.reason.status).sort();
    },base);assert.deepEqual(statuses,[409,'saved']);
  });
  await check('disabled browser storage fails visibly without a false saved state', async () => {
    const blocked = await browser.newContext();await blocked.addInitScript(()=>Object.defineProperty(window,'indexedDB',{value:undefined}));
    const p = await blocked.newPage();await p.goto(url);
    await p.waitForFunction(()=>document.getElementById('saveState').textContent==='Cannot open storage');
    assert(await p.locator('#addBox').isDisabled());await blocked.close();
  });
  await check('visitor and deployment-path isolation', async () => {
    const fresh = await browser.newContext(), visitor = await fresh.newPage();
    await open(visitor,url);assert.equal((await visitor.evaluate(()=>api('/api/stats'))).counts.unreviewed,8);
    const separate = await context.newPage();await open(separate,origin+prefixes[1]+'workflow/assets/human-review/');
    assert.equal((await separate.evaluate(()=>api('/api/stats'))).counts.unreviewed,8);
    await separate.close();await fresh.close();
  });
  await check('storage failure is visible and unsaved annotations remain downloadable', async () => {
    const isolated = await browser.newContext({acceptDownloads:true}), p = await isolated.newPage();await open(p,url);
    await p.evaluate(()=>{IDBObjectStore.prototype.put=function(){throw new DOMException('quota test','QuotaExceededError');};});
    await p.locator('#note').fill('저장 실패 때 보관할 Public sample 초안');
    await p.waitForFunction(()=>document.getElementById('saveState').textContent.includes('Save failed'));
    const draft=await downloadRows(p,'#downloadDraft');assert.equal(draft.rows[0].note,'저장 실패 때 보관할 Public sample 초안');
    await isolated.close();
  });
  await check('mobile layout, sample notice and clean sample screenshot', async () => {
    const clean = await browser.newContext({viewport:{width:1440,height:1000}}), p = await clean.newPage();
    p.on('dialog',d=>d.accept());await open(p,url);
    await p.locator('#browseButton').click();await p.locator('#search').fill('2017');
    await p.waitForFunction(()=>document.querySelectorAll('.file-entry').length===3);
    await p.locator('.file-entry').first().click();await settled(p);
    await p.locator('#reviewStatus').selectOption('needs_review');await settled(p);await p.locator('#fitButton').click();
    await dragBox(p,1640,1780,430,175);await p.locator('#confirmBox').click();
    await p.locator('[data-name-input]').fill('고나린 · synthetic name');await p.locator('[data-name-input]').press('Enter');
    await p.locator('#note').fill('Public sample review: compare cancellation marks in the input with the final tokens. This note demonstrates the controls; it is not an actual correction request.');await settled(p);
    await p.locator('#viewport').focus();assert.equal((await p.evaluate(()=>api('/api/stats'))).counts.needs_review,1);await p.screenshot({path:path.join(scratch,'review-screen.png')});
    await p.setViewportSize({width:390,height:844});
    assert(await p.locator('.sample-banner').isVisible());
    assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    await p.locator('#beforeView').click();await settled(p);assert(await p.locator('#addBox').isDisabled());
    await p.screenshot({path:path.join(scratch,'mobile.png'),fullPage:true});
    await clean.close();
  });
  await check('no runtime errors, API traffic, writes or external requests', async () => {
    assert.deepEqual(errors,[]);
    assert(requests.every(r=>r.method==='GET'&&r.url.startsWith(origin+'/')));
    assert(!requests.some(r=>new URL(r.url).pathname.startsWith('/api/')));
  });
})().then(()=>{
  fs.writeFileSync(path.join(scratch,'browser-results.json'),JSON.stringify({passed:true,checks,browser:'Chromium',external_deployment:false},null,2)+'\n');
}).catch(error=>{
  console.error(error);
  fs.writeFileSync(path.join(scratch,'browser-results.json'),JSON.stringify({passed:false,checks,error:String(error),errors},null,2)+'\n');
  process.exitCode=1;
}).finally(async()=>{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));});
