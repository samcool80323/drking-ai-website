import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const pages = fs.readdirSync(root).filter((file) => file.endsWith('.html') && file !== '404.html').sort();
const problems = [];
const titles = new Map();
const descriptions = new Map();
const incoming = Object.fromEntries(pages.map((file) => [file, 0]));
const pageTypes = new Set(['WebPage', 'AboutPage', 'ContactPage', 'CollectionPage']);

function hasType(node, type) {
  const values = Array.isArray(node?.['@type']) ? node['@type'] : [node?.['@type']];
  return values.includes(type);
}

function record(map, value, file) {
  map.set(value, [...(map.get(value) || []), file]);
}

for (const file of pages) {
  const html = fs.readFileSync(path.join(root, file), 'utf8');
  const title = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1].replace(/<[^>]+>/g, '').trim() || '';
  const descriptionTag = html.match(/<meta\b[^>]*\bname=["']description["'][^>]*>/i)?.[0] || '';
  const description = descriptionTag.match(/\bcontent=(["'])([\s\S]*?)\1/i)?.[2] || '';
  const canonical = html.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)/i)?.[1] || '';
  const headings = [...html.matchAll(/<h([1-6])\b/gi)].map((match) => Number(match[1]));
  const h1Count = headings.filter((level) => level === 1).length;

  if (!title) problems.push(`${file}: missing title`);
  if (!description) problems.push(`${file}: missing meta description`);
  if (title.length > 60) problems.push(`${file}: title exceeds 60-character review threshold (${title.length})`);
  if (description.length < 70 || description.length > 160) problems.push(`${file}: description outside 70-160 review range (${description.length})`);
  if (h1Count !== 1) problems.push(`${file}: expected one H1, found ${h1Count}`);
  if (headings.some((level, index) => index > 0 && level - headings[index - 1] > 1)) problems.push(`${file}: heading level is skipped`);
  if (!/^https:\/\/drking\.ai\/(?:[^.]*)?$/.test(canonical)) problems.push(`${file}: invalid canonical ${canonical || '(missing)'}`);
  if (!html.includes('site-footer-disclaimer')) problems.push(`${file}: missing claims disclaimer`);

  for (const image of html.matchAll(/<img\b[^>]*>/gi)) {
    if (!/\balt=["']/.test(image[0])) problems.push(`${file}: image missing alt text`);
    if (!/\bwidth=["']/.test(image[0]) || !/\bheight=["']/.test(image[0])) problems.push(`${file}: image missing intrinsic dimensions`);
  }

  const schemaScripts = [...html.matchAll(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)];
  if (schemaScripts.length !== 1) problems.push(`${file}: expected one consolidated JSON-LD graph, found ${schemaScripts.length}`);
  for (const script of schemaScripts) {
    try {
      const data = JSON.parse(script[1]);
      const graph = data['@graph'];
      if (!Array.isArray(graph)) problems.push(`${file}: structured data is not a graph`);
      else {
        const organisations = graph.filter((node) => node['@id'] === 'https://drking.ai/#organization');
        if (organisations.length !== 1) problems.push(`${file}: expected one canonical DrKing Organisation node`);
        if (graph.some((node) => node['@type'] === 'MedicalBusiness' && node.name === 'DrKing')) problems.push(`${file}: DrKing is incorrectly typed as MedicalBusiness`);
        const pageNode = graph.find((node) => [...pageTypes].some((type) => hasType(node, type)));
        if (!pageNode) problems.push(`${file}: missing WebPage-family structured-data node`);
        else {
          if (pageNode.name !== title) problems.push(`${file}: structured-data page name does not match title`);
          if (pageNode.description !== description) problems.push(`${file}: structured-data page description does not match meta description`);
          if (pageNode.url !== canonical) problems.push(`${file}: structured-data page URL does not match canonical`);
        }
        const ids = graph.map((node) => node['@id']).filter(Boolean);
        if (new Set(ids).size !== ids.length) problems.push(`${file}: duplicate structured-data @id values`);
      }
    } catch (error) {
      problems.push(`${file}: invalid JSON-LD (${error.message})`);
    }
  }

  record(titles, title, file);
  record(descriptions, description, file);
  for (const match of html.matchAll(/href=["'](?:https:\/\/drking\.ai)?\/([^#?"']*)/gi)) {
    const slug = (match[1] || 'index').replace(/\/$/, '') || 'index';
    const target = slug === 'index' ? 'index.html' : `${slug}.html`;
    if (incoming[target] !== undefined && target !== file) incoming[target] += 1;
  }
}

for (const [title, files] of titles) if (title && files.length > 1) problems.push(`duplicate title: ${files.join(', ')}`);
for (const [description, files] of descriptions) if (description && files.length > 1) problems.push(`duplicate description: ${files.join(', ')}`);
for (const [file, count] of Object.entries(incoming)) if (file !== 'index.html' && count === 0) problems.push(`${file}: no incoming internal links`);

const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
const sitemapUrls = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);
if (sitemapUrls.length !== pages.length) problems.push(`sitemap has ${sitemapUrls.length} URLs for ${pages.length} indexable pages`);
for (const file of pages) {
  const expected = file === 'index.html' ? 'https://drking.ai/' : `https://drking.ai/${file.slice(0, -5)}`;
  if (!sitemapUrls.includes(expected)) problems.push(`${file}: missing from sitemap`);
}

const robots = fs.readFileSync(path.join(root, 'robots.txt'), 'utf8');
if (!robots.includes('Content-Signal: ai-train=no, search=yes, ai-input=yes')) problems.push('robots.txt: missing approved Content Signal');
if (!robots.includes('Sitemap: https://drking.ai/sitemap.xml')) problems.push('robots.txt: missing sitemap declaration');

const redirects = fs.readFileSync(path.join(root, '_redirects'), 'utf8');
if (/^\/\*\s+\/:splat\s+200\s*$/m.test(redirects)) problems.push('_redirects: soft-404 catch-all is present');

const notFound = fs.readFileSync(path.join(root, '404.html'), 'utf8');
if (!/<meta\s+name=["']robots["']\s+content=["']noindex,follow["']/i.test(notFound)) problems.push('404.html: missing noindex,follow');

const llms = fs.readFileSync(path.join(root, 'llms.txt'), 'utf8');
if (!llms.includes('https://drking.ai/about') || !llms.includes('Citation and interpretation notes')) problems.push('llms.txt: missing canonical orientation content');

const result = {
  indexablePages: pages.length,
  sitemapUrls: sitemapUrls.length,
  orphanPages: Object.values(incoming).filter((count) => count === 0).length - (incoming['index.html'] === 0 ? 1 : 0),
  problems,
};
console.log(JSON.stringify(result, null, 2));
if (problems.length) process.exitCode = 1;
