import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const pages = fs.readdirSync(root).filter((file) => file.endsWith('.html')).sort();
const files = new Set();
for (const entry of fs.readdirSync(root, { recursive: true })) {
  const full = path.join(root, entry);
  if (fs.existsSync(full) && fs.statSync(full).isFile()) files.add('/' + entry.replaceAll(path.sep, '/'));
}

const results = [];
const internalRefs = [];
for (const file of pages) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  const ids = [...html.matchAll(/\bid=["']([^"']+)["']/gi)].map((match) => match[1]);
  const duplicateIds = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
  const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)];
  const menuScripts = scripts.filter(([, attrs, body]) => /menu-toggle|mobile-nav|nav-links|mega-menu/i.test(attrs + body));
  const menuToggleCount = (html.match(/class=["'][^"']*\bmenu-toggle\b/gi) || []).length;
  const mobileNavCount = (html.match(/id=["']mobile-nav["']/gi) || []).length;
  const fontFamilies = [...new Set([...html.matchAll(/font-family\s*:\s*([^;}]+)/gi)].flatMap((match) => match[1].split(',')).map((name) => name.trim().replaceAll(/["']/g, '')).filter(Boolean))];
  const fontUrls = [...html.matchAll(/url\((["']?)([^)'"\s]+)\1\)/gi)].map((match) => match[2]).filter((url) => url.startsWith('/fonts/'));
  const missingFonts = [...new Set(fontUrls.filter((url) => !files.has(url)))];
  const hrefs = [...html.matchAll(/\bhref=["']([^"']+)["']/gi)].map((match) => match[1]);
  for (const href of hrefs) {
    if (/^(?:https?:|mailto:|tel:|#|javascript:|data:)/i.test(href)) continue;
    const clean = href.split(/[?#]/)[0];
    const target = clean === '/' ? '/index.html' : clean.endsWith('/') ? clean + 'index.html' : path.extname(clean) ? clean : clean + '.html';
    internalRefs.push({ source: file, href, target: target.startsWith('/') ? target : '/' + target });
  }
  results.push({
    file,
    bytes: Buffer.byteLength(html),
    styles: (html.match(/<style\b/gi) || []).length,
    scripts: scripts.length,
    menuScripts: menuScripts.length,
    menuToggleCount,
    mobileNavCount,
    duplicateIds,
    missingFonts,
    fontFamilies,
    inlineImportant: (html.match(/!important/gi) || []).length,
    forms: (html.match(/<form\b/gi) || []).length,
    mailto: (html.match(/mailto:/gi) || []).length,
  });
}

const brokenLinks = internalRefs.filter(({ target }) => !files.has(target));
const totals = {
  pages: results.length,
  bytes: results.reduce((sum, item) => sum + item.bytes, 0),
  pagesWithMultipleMenuScripts: results.filter((item) => item.menuScripts > 1).length,
  pagesWithMissingFonts: results.filter((item) => item.missingFonts.length).length,
  pagesWithDuplicateIds: results.filter((item) => item.duplicateIds.length).length,
  brokenInternalLinks: brokenLinks.length,
};

console.log(JSON.stringify({ totals, brokenLinks, pages: results }, null, 2));
