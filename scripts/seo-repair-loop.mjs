import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const root = path.resolve(import.meta.dirname, '..');
const trackedExtensions = new Set(['.html', '.css', '.js', '.txt', '.xml']);

function run(script, capture = false) {
  const result = spawnSync(process.execPath, [path.join(root, 'scripts', script)], {
    cwd: root,
    encoding: 'utf8',
    stdio: capture ? 'pipe' : 'inherit',
  });
  if (result.status !== 0) {
    if (capture) process.stderr.write(`${result.stdout}${result.stderr}`);
    throw new Error(`${script} failed with exit code ${result.status}`);
  }
  return result.stdout;
}

function sourceHash() {
  const hash = crypto.createHash('sha256');
  const files = fs.readdirSync(root)
    .filter((file) => trackedExtensions.has(path.extname(file)) || ['_headers', '_redirects'].includes(file))
    .sort();
  for (const file of files) hash.update(file).update(fs.readFileSync(path.join(root, file)));
  hash.update(fs.readFileSync(path.join(root, 'assets', 'site-shell.css')));
  return hash.digest('hex');
}

let previousHash = null;
let stable = false;
for (let pass = 1; pass <= 3; pass += 1) {
  console.log(`\nSEO repair loop — pass ${pass}`);
  run('normalise-site.mjs');
  run('repair-seo.mjs');
  run('validate-site.mjs');
  run('validate-seo.mjs');
  run('audit-site.mjs', true);
  run('build-pages.mjs');

  const currentHash = sourceHash();
  if (currentHash === previousHash) {
    stable = true;
    console.log(`SEO repair loop stabilised after ${pass} passes.`);
    break;
  }
  previousHash = currentHash;
}

if (!stable) throw new Error('SEO repair loop did not stabilise within three passes.');

