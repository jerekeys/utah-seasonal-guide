const { chromium, webkit, devices } = require('playwright');
const fs = require('fs');
const assert = require('assert');
const root = 'http://127.0.0.1:8765';
const results = [];
fs.mkdirSync('research/qa', { recursive: true });
async function audit(page, label) {
  await page.addScriptTag({ path: require.resolve('axe-core/axe.min.js') });
  const violations = await page.evaluate(async () => (await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa'] } })).violations.map(v => ({ id: v.id, impact: v.impact, targets: v.nodes.map(n => n.target) })));
  assert.deepEqual(violations, [], label + ' accessibility: ' + JSON.stringify(violations));
  assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), label + ' horizontal overflow');
}
(async () => {
  for (const [name, engine, device] of [['Android Chrome engine', chromium, devices['Pixel 5']], ['iPhone Safari engine', webkit, devices['iPhone 13']]]) {
    const browser = await engine.launch({ headless: true, ...(engine === chromium ? { args: ['--no-sandbox'] } : {}) });
    const context = await browser.newContext(device);
    const page = await context.newPage();
    page.setDefaultTimeout(20000);
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(root + '/');
    await page.waitForSelector('.card');
    await page.evaluate(() => navigator.serviceWorker.ready);
    await page.waitForFunction(() => !!navigator.serviceWorker.controller);
    const manifest = await page.evaluate(async () => await (await fetch(document.querySelector('link[rel=manifest]').href)).json());
    assert.equal(manifest.display, 'standalone'); assert.equal(manifest.start_url, '/');
    assert(manifest.icons.some(i => i.sizes === '192x192')); assert(manifest.icons.some(i => i.sizes === '512x512' && i.purpose === 'maskable'));
    let installability;
    if (engine === chromium) {
      const session = await context.newCDPSession(page);
      installability = await session.send('Page.getInstallabilityErrors');
      assert.deepEqual(installability.installabilityErrors, [], 'Chrome installability requirements');
    }
    await page.locator('.save-button').first().click();
    await page.getByRole('link', { name: /My saved events 1/ }).click();
    await page.waitForSelector('#savedEvents .card');
    await page.reload();
    assert.equal(await page.locator('#savedEvents .card').count(), 1, 'Saved list persists after reload');
    const downloadPromise = page.waitForEvent('download');
    await page.click('#exportSaved');
    const download = await downloadPromise;
    const payload = JSON.parse(fs.readFileSync(await download.path(), 'utf8'));
    assert.equal(payload.events.length, 1);
    await page.locator('#savedEvents .save-button').click();
    assert.equal(await page.locator('#savedEvents .card').count(), 0, 'Unsave removes the card');
    await page.setInputFiles('#importSaved', { name: 'saved.json', mimeType: 'application/json', buffer: Buffer.from(JSON.stringify(payload)) });
    await page.waitForSelector('#savedEvents .card');
    await page.setInputFiles('#importSaved', { name: 'bad.json', mimeType: 'application/json', buffer: Buffer.from('{"format":"wrong"}') });
    await page.waitForFunction(() => document.querySelector('#savedFeedback').textContent.includes('could not be imported'));
    assert.equal(await page.locator('#savedEvents .card').count(), 1, 'Invalid import preserves saved list');
    await audit(page, name + ' saved');
    await page.screenshot({ path: `research/qa/saved-${engine === chromium ? 'android' : 'iphone'}.png`, fullPage: true });
    await page.locator('#savedEvents .event-image-link').click();
    await page.waitForSelector('.detail-panel');
    const visited = page.url();
    await context.setOffline(true);
    await page.reload();
    await page.waitForSelector('.detail-panel');
    assert.equal(page.url(), visited);
    await page.goto(root + '/saved/');
    await page.waitForSelector('#savedEvents .card');
    await page.goto(root + '/?holiday=Christmas');
    await page.waitForSelector('.card');
    assert.equal(await page.locator('#holidayFilter').inputValue(), 'Christmas');
    assert(await page.locator('.connection-notice').isVisible());
    await page.goto(root + '/events/not-previously-opened/');
    assert(await page.getByRole('heading', { name: 'You’re offline.' }).isVisible());
    await context.setOffline(false);
    await page.goto(root + '/contact/?topic=sponsorship');
    assert.equal(await page.locator('#contact-topic').inputValue(), 'sponsorship');
    await page.fill('#contact-email', 'test@example.com'); await page.fill('#contact-message', 'Local QA fixture only; do not transmit.');
    await page.route(root + '/', async route => route.request().method() === 'POST' ? route.fulfill({ status: 500, body: 'Unavailable' }) : route.continue());
    await page.getByRole('button', { name: 'Send message' }).click();
    await page.waitForFunction(() => document.querySelector('#formFeedback').textContent.includes('could not be confirmed'));
    assert.equal(await page.locator('#contact-message').inputValue(), 'Local QA fixture only; do not transmit.');
    await context.setOffline(true);
    await page.getByRole('button', { name: 'Send message' }).click();
    assert((await page.locator('#formFeedback').textContent()).includes('not been sent'));
    await context.setOffline(false);
    await page.unroute(root + '/');
    for (const path of ['/app/', '/about/', '/terms/', '/privacy/', '/contact/', '/submit/']) {
      await page.goto(root + path); await audit(page, name + path);
      assert(!/jerekeys|email jere|to jere/i.test(await page.content()), 'Personal identity removed from ' + path);
    }
    await page.goto(root + '/app/');
    assert.equal(await page.locator('#installGuide').isVisible(), false, 'No fake install prompt on unsupported state');
    if (engine === chromium) {
      await page.evaluate(() => {
        const event = new Event('beforeinstallprompt');
        event.prompt = () => Promise.resolve(); event.userChoice = Promise.resolve({ outcome: 'dismissed' }); window.dispatchEvent(event);
      });
      assert(await page.locator('#installGuide').isVisible());
      await page.click('#installGuide');
      await page.waitForFunction(() => document.querySelector('#installStatus').textContent.includes('install later'));
    }
    await page.screenshot({ path: `research/qa/install-${engine === chromium ? 'android' : 'iphone'}.png`, fullPage: true });
    assert.deepEqual(errors, []);
    results.push({ platform: name, deviceEmulation: true, physicalInstallationVerified: false, installability, manifest: true, savedPersistence: true, exportImport: true, offlineSearch: true, visitedPageOffline: true, offlineFallback: true, failedFormPreservesInput: true, offlineFormDoesNotSend: true, publicIdentityRemoved: true, accessibility: 'no automated violations on tested pages', errors });
    await browser.close();
  }
  // Exercise a real paid-slot fixture without publishing a pretend sponsor.
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await page.goto(root + '/');
  await page.waitForSelector('.card');
  await page.evaluate(() => {
    const day = window.DATE_TOOLS.today();
    window.SITE_DATA.site.sponsoredPlacements = [{ eventId: 'grand-america-witches-tea', startsOn: day, endsOn: day }]; initSponsored();
  });
  assert(await page.locator('#sponsoredEvents').isVisible());
  assert((await page.locator('#sponsoredEvents').textContent()).includes('Sponsored advertisement'));
  assert(await page.locator('#sponsoredEvents').evaluate(e => e.compareDocumentPosition(document.querySelector('.controls')) & Node.DOCUMENT_POSITION_FOLLOWING));
  await audit(page, 'Sponsored placement');
  await browser.close();
  fs.writeFileSync('research/qa/app-results.json', JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));
})().catch(error => { console.error(error); process.exitCode = 1; });
