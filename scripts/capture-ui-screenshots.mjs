#!/usr/bin/env node
/**
 * Captures UI screenshots for report.tex (fractal, pipeline, Python extension).
 * Requires: ng serve on :4201, docker stack with api-gateway + backends.
 *
 * Usage: node scripts/capture-ui-screenshots.mjs
 */
import { chromium } from 'playwright';
import { mkdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'docs', 'figures', 'ui');
const BASE_URL = process.env.MINIPAR_UI_URL ?? 'http://localhost:4201';

async function selectBackend(page, labelText) {
  await page.getByText(labelText, { exact: true }).click();
}

async function selectTemplate(page, optionLabel) {
  await page.locator('mat-select').first().click();
  await page.locator('mat-option').filter({ hasText: optionLabel }).click();
  await page.waitForTimeout(500);
}

async function runPipeline(page) {
  const runBtn = page.getByRole('button', { name: 'Executar código MiniPar' });
  await runBtn.click();
  await page.locator('mat-spinner').waitFor({ state: 'hidden', timeout: 120_000 }).catch(() => {});
  await page
    .locator('.status-chip--success, .output__error-panel, .output__message')
    .first()
    .waitFor({ timeout: 120_000 });
  await page.waitForTimeout(1000);
}

async function setEditorCode(page, code) {
  await page.locator('.monaco-editor').first().click();
  await page.keyboard.press('Control+A');
  await page.keyboard.insertText(code);
}

async function shot(page, name) {
  const file = path.join(OUT, `${name}.png`);
  await page.screenshot({ path: file, fullPage: true });
  console.log('saved', file);
}

async function main() {
  await mkdir(OUT, { recursive: true });

  const pythonFixture = await readFile(
    path.join(ROOT, 'sources', 'examples', '16_codegen_python.minipar'),
    'utf8',
  );

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport: { width: 1600, height: 1000 },
    deviceScaleFactor: 2,
  });

  await page.goto(BASE_URL, { waitUntil: 'networkidle', timeout: 60_000 });
  await page.waitForSelector('app-compiler-workspace', { timeout: 30_000 });

  // 1 — Pipeline (Compilador C, exemplo mínimo)
  await selectBackend(page, 'Compilador → C (gcc -O2)');
  await selectTemplate(page, '01 — Classe com método run');
  await runPipeline(page);
  await shot(page, '01-pipeline-codegen-c');

  // 2 — Fractal Sierpinski (Interpretador)
  const sierpinskiFixture = await readFile(
    path.join(ROOT, 'sources', 'examples', '13_sierpinski.minipar'),
    'utf8',
  );
  await selectBackend(page, 'Interpretador');
  await setEditorCode(page, sierpinskiFixture);
  await runPipeline(page);
  await page.locator('.output__message').filter({ hasText: 'Tapete de Sierpinski' }).waitFor({
    timeout: 120_000,
  });
  await shot(page, '02-fractal-sierpinski');

  // 3 — Extensão Python
  await selectBackend(page, 'Compilador → Python (extensão)');
  await setEditorCode(page, pythonFixture);
  await runPipeline(page);
  await page.locator('.output__message').filter({ hasText: 'hello from Python backend' }).waitFor({
    timeout: 120_000,
  });
  await shot(page, '03-python-extension');

  // 4 — Visão geral da variabilidade LPS (sidebar)
  await page.locator('.workspace__sidebar').screenshot({
    path: path.join(OUT, '04-lps-feature-panel.png'),
  });
  console.log('saved', path.join(OUT, '04-lps-feature-panel.png'));

  await browser.close();
  console.log('Done — screenshots in docs/figures/ui/');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
