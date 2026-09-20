import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const port = Number(process.env.PORT || 4174);
const types = new Map([
  ['.css', 'text/css; charset=utf-8'],
  ['.html', 'text/html; charset=utf-8'],
  ['.js', 'text/javascript; charset=utf-8'],
  ['.svg', 'image/svg+xml'],
  ['.ttf', 'font/ttf'],
  ['.woff2', 'font/woff2'],
  ['.txt', 'text/plain; charset=utf-8'],
  ['.xml', 'application/xml; charset=utf-8'],
]);
const redirects = new Map([
  ['/features_page', '/'],
  ['/features_page.html', '/'],
  ['/ai-voice', '/ai-voice-receptionist'],
  ['/ai-voice.html', '/ai-voice-receptionist'],
]);

http.createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, `http://${request.headers.host}`).pathname);
  if (redirects.has(pathname)) {
    response.writeHead(301, { location: redirects.get(pathname) });
    response.end();
    return;
  }
  if (pathname.endsWith('.html') && pathname !== '/404.html') {
    response.writeHead(301, { location: pathname.slice(0, -5) || '/' });
    response.end();
    return;
  }
  const clean = pathname === '/' ? '/index.html' : pathname;
  const candidates = path.extname(clean) ? [clean] : [`${clean}.html`, `${clean}/index.html`];
  const target = candidates
    .map((candidate) => path.resolve(root, `.${candidate}`))
    .find((candidate) => candidate.startsWith(`${root}${path.sep}`) && fs.existsSync(candidate) && fs.statSync(candidate).isFile());

  if (!target) {
    response.writeHead(404, {
      'cache-control': 'no-store',
      'content-signal': 'ai-train=no, search=yes, ai-input=yes',
      'content-type': 'text/html; charset=utf-8',
    });
    fs.createReadStream(path.join(root, '404.html')).pipe(response);
    return;
  }

  const headers = {
    'cache-control': 'no-store',
    'content-signal': 'ai-train=no, search=yes, ai-input=yes',
    'content-type': types.get(path.extname(target)) || 'application/octet-stream',
  };
  if (pathname === '/') headers.link = '</llms.txt>; rel="describedby"; type="text/markdown"';
  response.writeHead(200, headers);
  fs.createReadStream(target).pipe(response);
}).listen(port, '127.0.0.1', () => {
  console.log(`DrKing preview: http://127.0.0.1:${port}`);
});
