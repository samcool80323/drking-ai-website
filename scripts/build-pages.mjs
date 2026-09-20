import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const output = path.join(root, 'dist');
const rootAssets = [
  '_headers',
  '_redirects',
  'drking-logo.svg',
  'indexnow-key.txt',
  'llms.txt',
  'robots.txt',
  'sitemap.xml',
];

fs.rmSync(output, { recursive: true, force: true });
fs.mkdirSync(output, { recursive: true });

for (const file of fs.readdirSync(root).filter((entry) => entry.endsWith('.html'))) {
  fs.copyFileSync(path.join(root, file), path.join(output, file));
}
for (const file of rootAssets) fs.copyFileSync(path.join(root, file), path.join(output, file));
for (const directory of ['assets', 'fonts']) {
  fs.cpSync(path.join(root, directory), path.join(output, directory), { recursive: true });
}

console.log(`Prepared ${fs.readdirSync(output).length} root entries in ${output}`);
