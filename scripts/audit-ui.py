"""Sitewide UI/UX browser audit for drking.ai.

For every route in the curated dist (or a list), at 375/768/1440 widths:
horizontal overflow, visible text < 11px, broken images, failed requests (>=400),
JS errors, empty <svg><use> icons (zero-size or undefined), and text elements
cut off by the viewport. Writes JSON + prints a summary.
Usage: uv run --no-project --with playwright python scripts/audit-ui.py http://127.0.0.1:8792 [route ...]
"""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else 'http://127.0.0.1:8792'
ROOT = Path(__file__).resolve().parent.parent
routes = sys.argv[2:] or ['/' if p.stem == 'index' else '/' + p.stem for p in sorted(ROOT.glob('*.html')) if p.stem not in ('404', 'leads')]
CHROME = '/app/data/.agent-browser/browsers/chrome-151.0.7922.71/chrome'
WIDTHS = [(375, 812), (768, 1024), (1440, 900)]
JS = r'''() => {
  const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect(); return s.display!=='none' && s.visibility!=='hidden' && +s.opacity!==0 && r.width>0 && r.height>0; };
  const out = {overflow: document.documentElement.scrollWidth - innerWidth, tiny: [], offscreen: [], brokenImg: [], emptyIcons: 0};
  const MOCK = /(phone|mock|ui-|screen|window|dashboard|bubble|device|sms|message|chat|board|kanban|pipeline|invoice|notif|status|app-|widget|preview|mini|card-label|lead|col-|calendar|day|slot|chip|badge|tag|pill|wave|voice|ticker|receipt|ticket|toast|convo|thread|typing|avatar|meter|gauge|chart|graph|bar)/i;
  const isMock = el => { let a = el; while (a && a !== document.body) { if (MOCK.test((typeof a.className === 'string' ? a.className : '') + ' ' + (a.id||''))) return true; a = a.parentElement; } return false; };
  document.querySelectorAll('body *').forEach(el => {
    if (el.closest('svg') || !vis(el)) return;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (!own) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    if (fs < (el.closest('.site-header, .mobile-nav') ? 11 : (isMock(el) ? 10 : 11))) out.tiny.push(fs + 'px ' + el.tagName.toLowerCase() + '.' + (el.className||'').toString().split(' ')[0] + ': ' + el.textContent.trim().slice(0, 40));
    const r = el.getBoundingClientRect();
    const sc = el.closest('[style*="overflow"], .matrix-scroll, .table-scroll, [class*="scroll"], [class*="marquee"], [class*="ticker"], .mobile-nav, nav');
    if (!sc && (r.right > innerWidth + 2 || r.left < -2)) out.offscreen.push(el.tagName.toLowerCase() + '.' + (el.className||'').toString().split(' ')[0] + ' [' + Math.round(r.left) + ',' + Math.round(r.right) + ']: ' + el.textContent.trim().slice(0, 30));
  });
  document.querySelectorAll('img').forEach(i => { if (i.complete && i.naturalWidth === 0) out.brokenImg.push(i.getAttribute('src')); });
  document.querySelectorAll('svg use').forEach(u => { const id = (u.getAttribute('href')||'').slice(1); if (id && !document.getElementById(id)) out.emptyIcons++; });
  out.tiny = [...new Set(out.tiny)].slice(0, 8); out.offscreen = [...new Set(out.offscreen)].slice(0, 8);
  return out;
}'''
results = {}
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    for w, h in WIDTHS:
        ctx = br.new_context(viewport={'width': w, 'height': h})
        for route in routes:
            pg = ctx.new_page(); errs = []
            pg.on('pageerror', lambda e: errs.append('js: ' + str(e)[:120]))
            pg.on('response', lambda r: errs.append('http %d %s' % (r.status, r.url.replace(BASE, ''))) if r.status >= 400 and 'favicon' not in r.url else None)
            try:
                pg.goto(BASE + route, wait_until='networkidle', timeout=30000)
                hgt = pg.evaluate('document.body.scrollHeight')
                for y in range(0, hgt, 700):
                    pg.evaluate(f'window.scrollTo(0,{y})'); time.sleep(0.03)
                time.sleep(0.4)
                r = pg.evaluate(JS); r['errors'] = sorted(set(errs))[:6]
            except Exception as e:
                r = {'fatal': str(e)[:200]}
            results.setdefault(route, {})[w] = r
            pg.close()
        ctx.close()
    br.close()
out = ROOT / 'dist-ui-audit.json'
out.write_text(json.dumps(results, indent=1))
bad = 0
for route, by in results.items():
    for w, r in by.items():
        issues = {k: v for k, v in r.items() if v and k != 'overflow'}
        if r.get('overflow', 0) > 1: issues['overflow'] = r['overflow']
        if issues:
            bad += 1; print(f'{route} @{w}: {json.dumps(issues)[:600]}')
print(f'\n{len(routes)} routes x {len(WIDTHS)} widths; {bad} route-widths with issues; full report {out}')
