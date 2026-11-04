#!/usr/bin/env python3
"""Put each hero's keyword eyebrow INSIDE the H1 without changing how the page looks.

Why: Google often rewrites a page's search title from its H1. Creative H1s ("Pet owners call
when their animal is sick") lose the keyword. Moving the eyebrow ("AI receptionist for vet
clinics") into the H1 as its first line gives Google a descriptive H1 while the visual stays
the same: the span keeps the eyebrow classes, and a page-scoped style block restores the
eyebrow's own font/size/spacing (measured in a real browser before the change).

Usage: uv run --with playwright python scripts/eyebrow-into-h1.py http://127.0.0.1:PORT
Idempotent (skips pages that already have .h1-eyebrow). Edit EYEBROWS to set the keyword text.
"""
import html, json, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BASE = sys.argv[1].rstrip('/')
CHROME = '/app/data/.agent-browser/browsers/chrome-151.0.7922.71/chrome'
EYEBROWS = {  # page: new eyebrow text (None = keep current text)
    'admin-overhead': 'Clinic admin automation', 'after-hours': 'After-hours answering for clinics',
    'allied-health': None, 'analytics': 'Clinic analytics dashboard', 'chiropractic': None,
    'general-practice': None, 'lead-management': 'Clinic CRM and lead management',
    'medical-centres': 'Communication software for medical centres', 'medicaldirector-integration': 'MedicalDirector + AI receptionist',
    'multi-location-chaos': 'Multi-location clinic management', 'online-reviews': 'Google reviews for clinics',
    'patient-reactivation': None, 'physiotherapy': None, 'podiatry': None, 'psychology': None,
    'specialists': None, 'text-to-pay': 'Text-to-pay for clinics', 'veterinary': 'AI receptionist for vet clinics',
    'vs-receptionist': 'AI receptionist vs human receptionist', 'security': 'Security and data handling',
}
PROPS = ['font-family', 'font-size', 'font-weight', 'font-style', 'line-height', 'letter-spacing', 'text-transform', 'color', 'display', 'align-items', 'gap', 'justify-content']
MEASURE = r'''() => {
  const h = document.querySelector('main h1') || document.querySelector('h1');
  let e = h.previousElementSibling;
  if (!e || !/eyebrow|kicker/.test(e.className)) return null;
  const cs = getComputedStyle(e), hs = getComputedStyle(h);
  const er = e.getBoundingClientRect(), hr = h.getBoundingClientRect();
  const props = {}; for (const p of PROPS) props[p] = cs.getPropertyValue(p);
  return {props, eTop: er.top + scrollY, eH: er.height, hTop: hr.top + scrollY, gap: hr.top - er.bottom,
          eMT: parseFloat(cs.marginTop), hMT: parseFloat(hs.marginTop), w: er.width};
}'''.replace('PROPS', json.dumps(PROPS))


def measure(pg, url):
    pg.goto(url, wait_until='networkidle')
    pg.add_style_tag(content='*{animation:none!important;transition:none!important}')
    return pg.evaluate(MEASURE)


def main():
    out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
        for page in EYEBROWS:
            f = ROOT / f'{page}.html'; s = f.read_text(encoding='utf-8')
            if 'h1-eyebrow' in s:
                print('skip', page); continue
            ms = {}
            for w in (1440, 375):
                pg = b.new_page(viewport={'width': w, 'height': 900}); ms[w] = measure(pg, f'{BASE}/{page}'); pg.close()
            if not ms[1440]:
                print('no eyebrow before h1:', page); continue
            # locate eyebrow element + h1 in source
            h1m = re.search(r'<h1([^>]*)>', s)
            pre = s[:h1m.start()]
            em = list(re.finditer(r'<(div|p|span)([^>]*class="([^"]*(?:eyebrow|kicker)[^"]*)"[^>]*)>(.*?)</\1>\s*$', pre, re.S))
            if not em:
                print('source eyebrow not found:', page); continue
            e = em[-1]
            inner = e.group(4)
            if EYEBROWS[page]:
                # keep leading svg/icons, replace text
                icons = ''.join(re.findall(r'<svg.*?</svg>|<span[^>]*class="[^"]*dot[^"]*"[^>]*></span>', inner, re.S))
                inner = icons + html.escape(EYEBROWS[page])
            cls = e.group(3) + ' h1-eyebrow'
            attrs = re.sub(r'class="[^"]*"', f'class="{cls}"', e.group(2))
            span = f'<span{attrs}>{inner}</span>'
            s = s[:e.start()] + s[e.end():h1m.start()].lstrip() + s[h1m.start():]
            h1m = re.search(r'<h1([^>]*)>', s)
            s = s[:h1m.end()] + span + s[h1m.end():]
            css = []
            for w, sel in ((1440, '@media(min-width:701px)'), (375, '@media(max-width:700px)')):
                m = ms[w]
                if not m: continue
                pr = m['props']
                decl = ';'.join(f'{k}:{v}' for k, v in pr.items() if v and k not in ('display',))
                disp = 'flex' if pr['display'] in ('flex', 'inline-flex') else 'block'
                css.append(f"{sel}{{main h1 .h1-eyebrow{{{decl};display:{disp};margin:0 0 {max(m['gap'],0):.1f}px;white-space:normal}}"
                           f"main h1:has(>.h1-eyebrow){{margin-top:{m['eMT']:.1f}px}}}}")
            s = s.replace('</head>', '<style id="drking-h1-eyebrow">' + ''.join(css) + '</style>\n</head>', 1)
            f.write_text(s, encoding='utf-8')
            out[page] = ms
            print('done', page)
        b.close()
    (ROOT / 'dist-eyebrow-measure.json').write_text(json.dumps(out))


main()
