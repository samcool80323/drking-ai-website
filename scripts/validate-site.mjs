import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = path.resolve(import.meta.dirname, '..');
const pages = fs.readdirSync(root).filter((file) => file.endsWith('.html')).sort();
const problems = [];

for (const file of pages) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  const count = (pattern) => (html.match(pattern) || []).length;
  const checks = {
    doctype: count(/<!doctype html>/gi),
    htmlOpen: count(/<html\b/gi),
    htmlClose: count(/<\/html>/gi),
    headOpen: count(/<head\b/gi),
    headClose: count(/<\/head>/gi),
    bodyOpen: count(/<body\b/gi),
    bodyClose: count(/<\/body>/gi),
    mainOpen: count(/<main\b/gi),
    mainClose: count(/<\/main>/gi),
    h1: count(/<h1\b/gi),
    header: count(/<header\b[^>]*class=["'][^"']*site-header/gi),
    mobileNav: count(/\bid=["']mobile-nav["']/gi),
    shellCss: count(/href=["']\/assets\/site-shell\.css["']/gi),
    shellJs: count(/src=["']\/assets\/site-shell\.js["']/gi),
  };
  for (const [name, value] of Object.entries(checks)) {
    const expected = name === 'h1' ? 1 : 1;
    if (value !== expected) problems.push({ file, type: 'structure', detail: `${name}: expected ${expected}, found ${value}` });
  }

  const footerYear = html.indexOf('id="year"');

  for (const [index, match] of [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)].entries()) {
    const [, attrs, source] = match;
    if (/\bsrc=/i.test(attrs)) continue;
    if (!/application\/ld\+json/i.test(attrs) && /(?:getElementById\(["']year["']\)|querySelector\(["']#year["']\))/i.test(source) && (footerYear < 0 || footerYear > match.index)) {
      problems.push({ file, type: 'dom-order', detail: 'footer year is unavailable to synchronous page script' });
    }
    try {
      if (/application\/ld\+json/i.test(attrs)) JSON.parse(source);
      else new vm.Script(source, { filename: `${file}:inline-script-${index + 1}` });
    } catch (error) {
      problems.push({ file, type: /ld\+json/i.test(attrs) ? 'json-ld' : 'javascript', detail: error.message });
    }
  }
}

const result = { pages: pages.length, problems };
console.log(JSON.stringify(result, null, 2));
if (problems.length) process.exitCode = 1;
