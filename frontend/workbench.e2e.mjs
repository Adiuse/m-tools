import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.MTOOLS_BROWSER_URL || 'http://127.0.0.1:8000';
const tag = Date.now().toString(36);
const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
  args: process.env.CHROMIUM_PATH ? ['--no-sandbox'] : [],
});
try {
  const page = await browser.newPage({ viewport: { width: 1365, height: 900 } });
  page.setDefaultTimeout(10_000);
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  const button = (name) => page.getByRole('button', { name, exact: true });
  const fill = (label, value) => page.getByLabel(label, { exact: true }).fill(value);
  await page.goto(base);
  await button('English').click();
  await fill('Email', process.env.MTOOLS_TEST_EMAIL || 'browser@example.com');
  await fill('Password', process.env.MTOOLS_TEST_PASSWORD || '');
  await button('Sign in').click();

  async function workspace(name) {
    await button('New workspace').click();
    await fill('Workspace name', name);
    await fill('Industry', 'Retail');
    await fill('Product or service', 'Footwear');
    await fill('Current objective', 'Measure demand');
    await fill('Currency code', 'EUR');
    await fill('Timezone', 'Europe/Berlin');
    await button('Create workspace').click();
    await page.getByRole('heading', { name, exact: true }).waitFor();
  }

  const north = 'North ' + tag;
  const south = 'South ' + tag;
  await workspace(north);
  await button('Evidence').click();
  await fill('Evidence title', 'Source ' + tag);
  await fill('Date collected', '2026-11-28');
  await fill('Quality notes', 'Version one');
  await button('Save evidence').click();
  await fill('Quality notes', 'Version two');
  await button('Save new version').click();
  const firstEvidence = page.getByRole('button', { name: 'Source ' + tag + ' Version 1' });
  await firstEvidence.click();
  assert.equal(await page.getByLabel('Quality notes').inputValue(), 'Version one');

  await button('Datasets').click();
  await fill('Dataset title', 'Demand ' + tag);
  await page.getByLabel('Source evidence', { exact: true }).selectOption({ label: 'Source ' + tag + ' · 2' });
  await fill('Population or scope', 'Store visitors');
  await fill('Unit', 'count');
  await fill('Period start', '2026-11-01');
  await fill('Exclusive period end', '2026-12-01');
  await fill('Row date 1', '2026-11-28');
  await fill('Value 1', '0');
  await button('Save dataset').click();
  await page.getByRole('button', { name: 'Demand ' + tag + ' Version 1' }).waitFor();

  await button('Analysis and drafts').click();
  await fill('Search', 'S01');
  await page.getByRole('button', { name: 'S01 Problem diagnosis Planned' }).click();
  await fill('Analysis question', 'Why did visits fall?');
  await page.getByLabel('Evidence and versions', { exact: true }).selectOption([
    { label: 'Source ' + tag + ' · 2' }, { label: 'Source ' + tag + ' · 1' },
  ]);
  await button('Check input').click();
  await page.getByText('Missing inputs', { exact: false }).waitFor();
  await button('Save draft').click();
  await page.getByText('Draft saved.').waitFor();
  await page.reload();
  await page.getByRole('button', { name: new RegExp(north) }).click();
  await button('Analysis and drafts').click();
  await page.getByRole('button', { name: 'Why did visits fall? Version 1' }).click();
  assert.equal(await page.getByLabel('Analysis question').inputValue(), 'Why did visits fall?');
  const sources = page.getByLabel('Evidence and versions', { exact: true });
  assert.equal(await sources.evaluate((select) => select.selectedOptions.length), 2);
  await fill('Analysis question', 'Why did visits fall this week?');
  await button('Save draft').click();
  await page.getByRole('button', { name: 'Why did visits fall this week? Version 2' }).waitFor();
  assert.equal(await sources.evaluate((select) => select.selectedOptions.length), 2);

  await button('History').click();
  await page.getByText('Dataset recorded').waitFor();
  await button('Back to workbench').click();
  await workspace(south);
  await button('Evidence').click();
  assert.equal(await page.getByRole('button', { name: new RegExp('Source ' + tag) }).count(), 0);
  await button('فارسی').click();
  assert.equal(await page.locator('html').getAttribute('dir'), 'rtl');
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByLabel('عنوان شاهد', { exact: true }).focus();
  await page.keyboard.press('Tab');
  assert.equal(await page.getByLabel('نوع شاهد', { exact: true }).evaluate((field) => document.activeElement === field), true);
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth), true);
  if (process.env.MTOOLS_SCREENSHOT) await page.screenshot({ path: process.env.MTOOLS_SCREENSHOT, fullPage: true });
  assert.deepEqual(errors, []);
  console.log('PASS: browser sign-in, two workspaces, evidence versions, dataset, preflight, draft restore with source versions, history, RTL and mobile width.');
} finally {
  await browser.close();
}
