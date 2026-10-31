"""Raise unreadably small text sitewide without redesigning.

Renders each page at 375/768/1440, finds visible text below the readability floor
(11px for real copy, 10px for decorative UI mock-ups such as phone screens and
dashboards) and writes page-scoped `font-size: Npx !important` overrides into a
marked <style id="drking-readability"> block at the end of <head>. Idempotent.
Usage: uv run --no-project --with playwright python scripts/fix-tiny-text.py http://127.0.0.1:PORT [route ...]
"""
import re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/')
ROOT = Path(__file__).resolve().parent.parent
routes = sys.argv[2:] or ['/' if p.stem == 'index' else '/' + p.stem for p in sorted(ROOT.glob('*.html')) if p.stem not in ('404', 'leads')]
CHROME = '/app/data/.agent-browser/browsers/chrome-151.0.7922.71/chrome'
START, END = '<style id="drking-readability">', '</style><!-- /drking-readability -->'
JS = r'''() => {
  const MOCK = /(phone|mock|ui-|screen|window|dashboard|bubble|device|sms|message|chat|board|kanban|pipeline|invoice|notif|status|app-|widget|preview|mini|card-label|lead|col-|calendar|day|slot|chip|badge|tag|pill|wave|voice|ticker|receipt|ticket|toast|convo|thread|typing|avatar|meter|gauge|chart|graph|bar)/i;
  const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect(); return s.display!=='none' && s.visibility!=='hidden' && r.width>0 && r.height>0; };
  const esc = c => CSS.escape(c);
  const sel = el => {
    const own = el.tagName.toLowerCase() + [...el.classList].map(c => '.' + esc(c)).join('');
    let a = el.parentElement, chain = [];
    while (a && a !== document.body && chain.length < 2) {
      if (a.classList.length) chain.unshift('.' + esc(a.classList[0]));
      else if (a.id) chain.unshift('#' + esc(a.id));
      a = a.parentElement;
    }
    return (chain.join(' ') + ' ' + own).trim();
  };
  const out = [];
  document.querySelectorAll('body *').forEach(el => {
    if (el.closest('svg, script, style, .site-header, .mobile-nav') || !vis(el)) return;
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1)) return;
    const fs = parseFloat(getComputedStyle(el).fontSize);
    let mock = false, a = el;
    while (a && a !== document.body) { if (MOCK.test((a.className && a.className.baseVal === undefined ? a.className : '') + ' ' + (a.id||''))) { mock = true; break; } a = a.parentElement; }
    const floor = mock ? 10 : 11;
    if (fs < floor) out.push([sel(el), floor]);
  });
  return out;
}'''
rules = {}
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    for w, h in [(375, 812), (768, 1024), (1440, 900)]:
        ctx = br.new_context(viewport={'width': w, 'height': h})
        for route in routes:
            pg = ctx.new_page()
            try:
                pg.goto(BASE + route, wait_until='networkidle', timeout=30000)
                for s, floor in pg.evaluate(JS):
                    page = 'index.html' if route == '/' else route.strip('/') + '.html'
                    d = rules.setdefault(page, {})
                    d[s] = max(d.get(s, 0), floor)
            except Exception as e:
                print('skip', route, w, str(e)[:100])
            pg.close()
        ctx.close()
    br.close()
total = 0
for page, sels in sorted(rules.items()):
    f = ROOT / page
    s = f.read_text(encoding='utf-8')
    existing = re.search(re.escape(START) + r'(.*?)' + re.escape(END), s, re.S)
    merged = {}
    if existing:
        for sel, size in re.findall(r'([^{}\n]+)\{font-size:(\d+)px!important\}', existing.group(1)):
            merged[sel.strip()] = int(size)
        s = s[:existing.start()] + s[existing.end():]
    for sel, size in sels.items():
        merged[sel] = max(merged.get(sel, 0), size)
    block = START + '\n' + '\n'.join(f'{k}{{font-size:{v}px!important}}' for k, v in sorted(merged.items())) + '\n' + END
    s = s.replace('</head>', block + '\n</head>', 1)
    f.write_text(s, encoding='utf-8')
    total += len(sels)
    print(f'{page}: {len(sels)} selectors raised')
print('pages', len(rules), 'selectors', total)
