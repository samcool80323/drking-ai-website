#!/usr/bin/env python3
"""Add a 'From the DrKing Journal' guide strip to product pages (topical hub links).
Idempotent: content between <!-- drking-guides --> markers is regenerated. Inserted just
before the page's final CTA section. Cards use the site's paper/ink/teal tokens."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTS = {json.loads(p.read_text())['slug']: json.loads(p.read_text()) for p in (ROOT / 'blog-content').glob('*.json')}
PAGES = {
    'patient-reactivation.html': ['patient-reactivation-calendar', 'unscheduled-treatment-follow-up', 'no-show-to-lost-patient'],
    'patient-no-shows.html': ['no-show-to-lost-patient', 'patient-reactivation-calendar', 'unscheduled-treatment-follow-up'],
    'appointment-reminders.html': ['no-show-to-lost-patient', 'patient-reactivation-calendar'],
    'dentists.html': ['unscheduled-treatment-follow-up', 'patient-reactivation-calendar', 'no-show-to-lost-patient'],
    'slow-follow-up.html': ['unscheduled-treatment-follow-up', 'no-show-to-lost-patient'],
}
CSS = ('<style id="drking-guides-css">.dk-guides{width:min(1200px,calc(100% - 40px));margin:0 auto;padding:20px 0 70px}.dk-guides h2{font:300 clamp(30px,3.2vw,42px)/1.12 Newsreader,serif;letter-spacing:-.6px;margin:12px 0 24px;color:#1C1814}'
       '.dk-guides h2 em{color:#0D5C5C}.dk-guides-k{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#0D5C5C;font-weight:500}'
       '.dk-guides-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px}'
       '.dk-guide{display:block;background:#fff;border-radius:22px;padding:24px;box-shadow:0 2px 4px #1c18140a,0 12px 24px #1c18140f;color:#1C1814;text-decoration:none;transition:transform .2s}'
       '.dk-guide:hover{transform:translateY(-3px)}.dk-guide span{font-size:12px;letter-spacing:1.4px;text-transform:uppercase;color:#b94a32}'
       '.dk-guide strong{display:block;font:300 23px/1.25 Newsreader,serif;margin:10px 0 8px}.dk-guide p{margin:0;font-size:15px;line-height:1.6;color:#5f5c55}</style>')
CTA = re.compile(r'<section class="(?:closing wrap|cta wrap|cta-shell wrap reveal|demo-section|cta reveal)"')

def strip(s):
    return re.sub(r'<[^>]+>', '', s)

for page, slugs in PAGES.items():
    p = ROOT / page; s = p.read_text(encoding='utf-8')
    s = re.sub(r'<!-- drking-guides -->.*?<!-- /drking-guides -->', '', s, flags=re.S)
    cards = ''.join(f'<a class="dk-guide" href="/{x}"><span>Guide · {ARTS[x]["reading_minutes"]} min read</span><strong>{strip(ARTS[x]["h1"])}</strong><p>{ARTS[x]["dek"]}</p></a>' for x in slugs)
    block = (f'<!-- drking-guides --><section class="dk-guides" aria-labelledby="dk-guides-h"><div class="dk-guides-k">From the DrKing Journal</div>'
             f'<h2 id="dk-guides-h">Practical guides for <em>practice managers</em></h2><div class="dk-guides-grid">{cards}</div></section><!-- /drking-guides -->')
    ms = list(CTA.finditer(s)); assert ms, page
    i = ms[-1].start()
    s = s[:i] + block + s[i:]
    if 'drking-guides-css' not in s:
        s = s.replace('</head>', CSS + '\n</head>', 1)
    p.write_text(s, encoding='utf-8'); print(page, len(slugs))
