#!/usr/bin/env python3
"""Build DrKing editorial blog pages from blog-content/*.json.

Fork source: patient-reactivation.html (head, embedded CSS, SVG sprite, header, footer,
scripts). Only <main>, head metadata and JSON-LD are replaced, so articles share the
approved DrKing design. Also builds blog.html (index), adds articles to sitemap.xml and
a sitewide footer "Blog" link. Idempotent.

Article JSON keys: slug, title, meta_description, h1, dek, primary_keyword,
secondary_keywords, reading_minutes, key_takeaways, body_html, faq[{q,a}],
sources[{title,publisher,url}], hero{card_title,rows[3],bubble,pill,note},
published (YYYY-MM-DD), updated (optional), category (optional).
"""
import html, json, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'blog-content'
FORK = ROOT / 'patient-reactivation.html'
BASE = 'https://drking.ai'
MONTHS = 'January February March April May June July August September October November December'.split()

ARTICLE_CSS = r'''<style id="drking-article">
.article-hero{padding-bottom:56px}.article-hero h1{font-size:clamp(40px,4.2vw,60px)}
.article-dek{font-size:20px;line-height:1.6;color:#4b4842;max-width:620px;margin:0 0 22px}
.byline{display:flex;flex-wrap:wrap;gap:8px 18px;font-size:14px;color:#5f5c55;align-items:center}
.byline a{color:var(--teal);border-bottom:1px solid #0d5c5c44}.byline span:not(:last-child):after{content:'·';margin-left:18px;color:#a5a29a}
.breadcrumb{font-size:13px;color:#5f5c55;display:flex;gap:8px;flex-wrap:wrap;margin-bottom:-8px}.breadcrumb a{color:var(--teal)}
.article-hero .booking-badge{right:8px}.article-hero .phone{top:40px}.art-list{position:absolute;left:-14px;bottom:30px;z-index:3;background:#fff;border-radius:22px;padding:16px 18px;width:230px;box-shadow:0 2px 4px #1c18140a,0 12px 24px #1c18140f;transform:rotate(-2deg)}
.art-list strong{display:block;font:500 14px/1.3 Geomanist,sans-serif;margin-bottom:8px}
.art-list li{list-style:none;display:flex;gap:8px;align-items:flex-start;font-size:12.5px;line-height:1.4;color:#4b4842;padding:5px 0;border-top:1px solid #efede7}
.art-list li:before{content:'';flex:0 0 7px;height:7px;border-radius:50%;background:var(--sage);margin-top:5px}
.art-list ul{margin:0;padding:0}
.article-shell{display:grid;grid-template-columns:250px minmax(0,720px);gap:72px;justify-content:center;padding:24px 0 90px}
.toc{position:sticky;top:120px;align-self:start;font-size:14px}
.toc-title{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:var(--teal);margin:0 0 12px;font-weight:500}
.toc ol{list-style:none;margin:0;padding:0;border-left:1px solid var(--line)}
.toc a{display:block;padding:7px 0 7px 16px;margin-left:-1px;border-left:2px solid transparent;color:#4b4842;line-height:1.4}
.toc a:hover,.toc a.active{color:var(--teal);border-left-color:var(--terra)}
.article-body{font-size:18px;line-height:1.78;color:#2a2621}
.article-body>p:first-of-type{font-size:20px;line-height:1.7}
.article-body h2{font:300 clamp(30px,3vw,40px)/1.15 var(--serif);letter-spacing:-.8px;margin:64px 0 18px;color:var(--ink);scroll-margin-top:120px}
.article-body h2 em,.article-body h3 em{color:var(--teal)}
.article-body h3{font:500 21px/1.35 Geomanist,sans-serif;margin:36px 0 10px}
.article-body p{margin:0 0 20px}.article-body ul,.article-body ol{margin:0 0 24px;padding-left:24px}.article-body li{margin:0 0 8px}
.article-body a{color:var(--teal);text-decoration:underline;text-decoration-color:#0d5c5c55;text-underline-offset:3px}
.article-body a:hover{color:var(--terra)}
.article-body strong{font-weight:600}
.article-body blockquote{margin:32px 0;padding:4px 0 4px 26px;border-left:3px solid var(--terra);font:300 italic 24px/1.5 var(--serif);color:var(--ink)}
.takeaways{background:#E7EEE7;border-radius:22px;padding:26px 30px;margin:0 0 40px}
.takeaways h2{font:500 13px/1 Geomanist,sans-serif!important;letter-spacing:2px;text-transform:uppercase;color:var(--teal);margin:0 0 14px!important}
.takeaways ul{margin:0;padding-left:20px}.takeaways li{margin:0 0 8px;font-size:17px}
.callout{background:#fffefa;border:1px solid #e3e5dc;border-left:3px solid var(--terra);border-radius:4px 18px 18px 4px;padding:18px 22px;margin:28px 0}
.callout strong{display:block;font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--terra);margin-bottom:6px;font-weight:500}
.callout p{margin:0 0 10px;font-size:16.5px}.callout p:last-child{margin:0}
.template-box{background:#fff;border-radius:20px 20px 20px 5px;box-shadow:0 2px 4px #1c18140a,0 12px 24px #1c18140f;padding:18px 22px;margin:22px 0 26px;max-width:600px}
.template-label{font-size:12px;letter-spacing:1.6px;text-transform:uppercase;color:var(--teal);font-weight:500;margin-bottom:6px;display:flex;gap:8px;align-items:center}
.template-label:before{content:'';width:7px;height:7px;border-radius:50%;background:var(--teal)}
.template-box p{margin:0 0 8px;font-size:16.5px;line-height:1.6}.template-box p:last-child{margin:0}
.table-scroll{overflow-x:auto;margin:26px 0 30px;border:1px solid var(--line);border-radius:16px;background:#fffefa}
table.compare{border-collapse:collapse;width:100%;min-width:560px;font-size:15px;line-height:1.5}
table.compare th{background:#eef2ec;text-align:left;font-weight:500;padding:12px 14px;color:var(--ink);font-size:14px}
table.compare td{padding:12px 14px;border-top:1px solid var(--line);vertical-align:top}
.article-meta-box{margin:56px 0 0;padding:26px 28px;border:1px solid var(--line);border-radius:22px;background:#fffefa;font-size:15.5px;line-height:1.65}
.article-meta-box h2{font:500 13px/1 Geomanist,sans-serif!important;letter-spacing:2px;text-transform:uppercase;color:var(--teal);margin:0 0 12px!important}
.article-meta-box p{margin:0 0 10px}
.sources{margin:40px 0 0}.sources h2{font:300 28px/1.2 var(--serif)!important;margin:0 0 14px!important}
.sources ol{font-size:15px;line-height:1.6;padding-left:22px}.sources li{margin:0 0 8px}.sources a{word-break:break-word}
.related{padding:20px 0 30px}.related-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:22px;margin-top:26px}
.related-card{display:block;background:#fff;border-radius:22px;padding:26px;box-shadow:0 2px 4px #1c18140a,0 12px 24px #1c18140f;transition:transform .2s}
.related-card:hover{transform:translateY(-3px)}
.related .eyebrow,.related-card .eyebrow{font-size:11.5px!important}.related-card h2,.related-card h3{font:300 25px/1.2 var(--serif);margin:12px 0 10px}.related-card p{margin:0;color:#5f5c55;font-size:15px;line-height:1.6}
.blog-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:26px;padding:10px 0 90px}
.mobile-toc{display:none}
@media(max-width:1000px){.article-shell{grid-template-columns:minmax(0,1fr);gap:0}.toc{display:none}.mobile-toc{display:block;margin:0 0 30px;border:1px solid var(--line);border-radius:16px;background:#fffefa;padding:4px 18px}
.mobile-toc summary{cursor:pointer;padding:12px 0;font-weight:500;color:var(--teal);list-style:none}.mobile-toc ol{margin:0 0 14px;padding-left:20px;font-size:15.5px}.mobile-toc li{margin:0 0 6px}.mobile-toc a{color:#2a2621}}
@media(max-width:700px){.article-hero .phone{top:56px}.article-body{font-size:17px}.article-body>p:first-of-type{font-size:18px}.article-dek{font-size:18px}.art-list{display:none}.takeaways,.article-meta-box{padding:22px}.byline span:not(:last-child):after{margin-left:10px}.byline{gap:6px 10px}}
/* ---- visual components (HTML-only, no inline styles) ---- */
.flow{list-style:none;margin:30px 0 34px;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;counter-reset:fl}
.flow li{counter-increment:fl;position:relative;background:#fff;border-radius:20px;padding:44px 18px 18px;box-shadow:0 2px 4px #1c18140a,0 12px 24px #1c18140f;margin:0}
.flow li:before{content:counter(fl);position:absolute;top:14px;left:18px;width:24px;height:24px;border-radius:50%;background:var(--teal);color:#fff;font:500 13px/24px Geomanist,sans-serif;text-align:center}
.flow li strong{display:block;font:500 16px/1.3 Geomanist,sans-serif;margin-bottom:4px;color:var(--ink)}.flow li span{display:block;font-size:14.5px;line-height:1.5;color:#4b4842}
.stat-tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:30px 0 34px}
.stat-tiles .tile{background:#E7EEE7;border-radius:22px;padding:22px 22px 20px}.stat-tiles .tile b{display:block;font:300 clamp(34px,4vw,46px)/1.05 var(--serif);color:var(--teal);letter-spacing:-1px}
.stat-tiles .tile span{display:block;margin-top:8px;font-size:14.5px;line-height:1.5;color:#3f3c36}.stat-tiles .tile small{display:block;margin-top:8px;font-size:13px;color:#4b4842}
.bars{margin:30px 0 34px;background:#fffefa;border:1px solid var(--line);border-radius:20px;padding:22px 24px}.bars .bar{margin:0 0 14px}.bars .bar:last-child{margin:0}
.bars .bl{display:flex;justify-content:space-between;gap:12px;font-size:14.5px;margin-bottom:6px;color:#2a2621}.bars .bl em{font-style:normal;color:var(--teal);font-weight:600}
.bars .track{height:12px;border-radius:99px;background:#eef2ec;overflow:hidden}.bars .fill{display:block;height:100%;border-radius:99px;background:var(--teal)}
.bars .w5{width:5%}.bars .w10{width:10%}.bars .w15{width:15%}.bars .w20{width:20%}.bars .w25{width:25%}.bars .w30{width:30%}.bars .w35{width:35%}.bars .w40{width:40%}.bars .w45{width:45%}.bars .w50{width:50%}.bars .w55{width:55%}.bars .w60{width:60%}.bars .w65{width:65%}.bars .w70{width:70%}.bars .w75{width:75%}.bars .w80{width:80%}.bars .w85{width:85%}.bars .w90{width:90%}.bars .w95{width:95%}.bars .w100{width:100%}
.bars .note{margin:14px 0 0;font-size:13px;color:#4b4842}
.compare-cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin:30px 0 34px}
.compare-cards .cc{border-radius:22px;padding:22px 24px;background:#fff;box-shadow:0 2px 4px #1c18140a,0 12px 24px #1c18140f;border-top:4px solid var(--teal)}.compare-cards .cc.bad{border-top-color:var(--terra)}
.compare-cards .cc h3{margin:0 0 10px;font:500 13px/1 Geomanist,sans-serif;letter-spacing:1.8px;text-transform:uppercase;color:var(--teal)}.compare-cards .cc.bad h3{color:var(--terra)}
.compare-cards ul{list-style:none;margin:0;padding:0}.compare-cards li{padding:8px 0 8px 26px;position:relative;font-size:16px;line-height:1.5;border-top:1px solid #efede7;margin:0}.compare-cards li:first-child{border-top:0}
.compare-cards li:before{content:'\2713';position:absolute;left:2px;top:7px;font:600 16px/1.5 Geomanist,sans-serif;color:var(--teal)}.compare-cards .bad li:before{content:'\2715';color:var(--terra)}
.checklist{list-style:none;margin:26px 0 30px;padding:0;background:#fffefa;border:1px solid var(--line);border-radius:20px}.checklist li{position:relative;margin:0;padding:14px 18px 14px 52px;border-top:1px solid var(--line);font-size:16.5px;line-height:1.5}.checklist li:first-child{border-top:0}
.checklist li:before{content:'';position:absolute;left:18px;top:15px;width:20px;height:20px;border-radius:6px;border:2px solid var(--teal);box-sizing:border-box}.checklist li:after{content:'';position:absolute;left:24px;top:19px;width:6px;height:10px;border:solid var(--teal);border-width:0 2px 2px 0;transform:rotate(45deg)}
.timeline{list-style:none;margin:30px 0 34px 12px;padding:0 0 0 26px;border-left:2px solid var(--sage)}.timeline li{position:relative;margin:0 0 22px;padding-left:18px}.timeline li:last-child{margin:0}
.timeline li:before{content:'';position:absolute;left:-35px;top:6px;width:14px;height:14px;border-radius:50%;background:#fff;border:3px solid var(--teal)}.timeline li b{display:block;font:500 13px/1 Geomanist,sans-serif;letter-spacing:1.6px;text-transform:uppercase;color:#A8442F;margin-bottom:6px}
.chat{max-width:440px;margin:28px 0 32px;background:#fff;border-radius:26px;padding:18px 18px 14px;box-shadow:0 2px 4px #1c18140a,0 14px 30px #1c181412}.chat .chat-head{font-size:12px;letter-spacing:1.6px;text-transform:uppercase;color:var(--teal);font-weight:500;margin:0 0 12px}
.chat .msg{max-width:84%;padding:11px 14px;border-radius:18px;font-size:15.5px;line-height:1.5;margin:0 0 10px}.chat .out{background:#E7EEE7;border-bottom-left-radius:5px}.chat .in{background:var(--teal);color:#fff;margin-left:auto;border-bottom-right-radius:5px}.chat .when{font-size:12.5px;color:#4b4842;margin:0 0 12px}.chat .when.r{text-align:right}
.pull{margin:38px 0;padding:28px 30px;border-radius:24px;background:var(--teal);color:#fff}.pull p{margin:0;font:300 clamp(24px,3vw,32px)/1.3 var(--serif);letter-spacing:-.4px}.pull small{display:block;margin-top:12px;font-size:13px;letter-spacing:1.4px;text-transform:uppercase;opacity:.92}
figure.viz{margin:34px 0;padding:22px 20px 16px;background:#fffefa;border:1px solid var(--line);border-radius:22px}figure.viz svg{display:block;width:100%;height:auto}figure.viz figcaption{margin-top:12px;font-size:13.5px;line-height:1.5;color:#4b4842;text-align:center}
.article-body .flow,.article-body .checklist,.article-body .compare-cards ul{padding-left:0}.article-body .timeline{padding-left:26px;margin-left:12px}
@media(max-width:700px){.flow{grid-template-columns:1fr}.flow li{padding:16px 18px 16px 58px}.flow li:before{top:16px;left:18px}.bars,.compare-cards .cc,.pull{padding-left:20px;padding-right:20px}.stat-tiles{grid-template-columns:1fr 1fr}.stat-tiles .tile:last-child:nth-child(odd){grid-column:1/-1}}
</style>'''

ARROW = '<svg fill="none" stroke="currentColor" stroke-width="1.5"><use href="#arrow"/></svg>'
CHECK = '<svg fill="none" stroke="currentColor" stroke-width="1.5"><use href="#check"/></svg>'
PLUS = '<svg fill="none" stroke="currentColor" stroke-width="1.5"><use href="#plus"/></svg>'


def esc(s):
    return html.escape(s, quote=True)


def nice_date(d):
    y, m, dd = map(int, d.split('-'))
    return f'{dd} {MONTHS[m - 1]} {y}'


def strip_tags(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()


def load_articles():
    arts = []
    for f in sorted(CONTENT.glob('*.json')):
        a = json.loads(f.read_text(encoding='utf-8'))
        a.setdefault('published', '2026-10-31')
        a.setdefault('updated', a['published'])
        a.setdefault('category', 'Practice growth')
        arts.append(a)
    arts.sort(key=lambda a: (a['published'], a['slug']), reverse=True)
    return arts


def fork_parts():
    s = FORK.read_text(encoding='utf-8')
    head_end = s.index('</head>')
    main_start = s.index('<main')
    main_end = s.index('</main>') + len('</main>')
    return s, head_end, main_start, main_end


def set_meta(s, title, desc, url, og_type):
    full = f'{title}'
    rep = [
        (r'<title>.*?</title>', f'<title>{esc(full)}</title>'),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">'),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{esc(full)}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{esc(desc)}">'),
        (r'<meta property="og:type" content="[^"]*">', f'<meta property="og:type" content="{og_type}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">'),
    ]
    for pat, new in rep:
        s, n = re.subn(pat, lambda m: new, s, count=1, flags=re.S)
        assert n == 1, pat
    return s


def null_safe(s):
    # fork's ROI calculator script expects #patients; articles have no calculator
    old = "patients.addEventListener('input'"
    assert s.count(old) == 1
    return s.replace(old, "patients&&patients.addEventListener('input'")


def org_node(s):
    m = re.search(r'<script type="application/ld\+json" id="structured-data">(.*?)</script>', s, re.S)
    g = json.loads(m.group(1))
    return [n for n in g['@graph'] if n.get('@type') == 'Organization'][0]


def set_ld(s, graph):
    payload = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))
    payload = payload.replace('</', '<\\/')
    s, n = re.subn(r'(<script type="application/ld\+json" id="structured-data">).*?(</script>)',
                   lambda m: m.group(1) + payload + m.group(2), s, count=1, flags=re.S)
    assert n == 1
    return s


def add_ids_and_toc(body):
    toc = []
    def fix(m):
        attrs, inner = m.group(1), m.group(2)
        idm = re.search(r'id="([^"]+)"', attrs)
        hid = idm.group(1) if idm else re.sub(r'[^a-z0-9]+', '-', strip_tags(inner).lower()).strip('-')[:60]
        toc.append((hid, strip_tags(inner)))
        return f'<h2 id="{hid}">{inner}</h2>'
    body = re.sub(r'<h2([^>]*)>(.*?)</h2>', fix, body, flags=re.S)
    body = body.replace('<a href="http', '<a rel="noopener" target="_blank" href="http') if 'rel="noopener"' not in body else body
    return body, toc


def hero_html(a, h1, dek, crumbs, byline):
    h = a.get('hero') or {}
    rows = ''.join(f'<li>{esc(r)}</li>' for r in h.get('rows', [])[:3])
    label = f"Illustration: {h.get('card_title','')}. Example message: {h.get('bubble','')}"
    return f'''<section class="hero wrap article-hero" aria-labelledby="hero-title"><div class="hero-copy">{crumbs}<div class="eyebrow" style="margin-top:22px">DrKing Journal · {esc(a['category'])}</div><h1 id="hero-title">{h1}</h1><p class="article-dek">{esc(dek)}</p>{byline}</div> <div class="hero-art" role="img" aria-label="{esc(label)}"><svg class="blob" viewBox="0 0 480 480" preserveAspectRatio="none" aria-hidden="true"><path fill="#DDE7D8" d="M247 14C344-4 443 64 455 163c12 94-20 226-110 268-90 43-228 32-292-37C-9 324 0 198 43 122S153 31 247 14Z"/></svg><div class="orbit"></div><svg class="spark" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.5"><path d="m20 1 1 13L32 6l-7 11 14 3-14 2 8 12-12-8-1 13-3-13L6 34l8-12-13-2 13-3L6 6l11 8Z"/></svg><div class="art-list"><strong>{esc(h.get('card_title',''))}</strong><ul>{rows}</ul></div><div class="phone"><div class="phone-head"><div class="avatar"><svg><use href="#brand"/></svg></div><div>Your practice, with DrKing<small>Patient follow-up</small></div><span class="dots">···</span></div><div class="today">TODAY, 9:41 AM</div><div class="message">{esc(h.get('bubble',''))}<br><span style="font-size:11px;color:#5f6659">Reply STOP to opt out.</span></div><div class="delivered">Delivered</div></div><div class="booking-badge"><div class="check-circle">{CHECK}</div><div><strong>{esc(h.get('pill',''))}</strong><small>Illustrative example</small></div></div><div class="art-caption">{esc(h.get('note',''))}<svg viewBox="0 0 50 40" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 34C30 39 45 23 38 4m-6 7 6-8 8 6"/></svg></div></div></section>'''


def faq_html(faq):
    items = ''.join(f'<details><summary>{esc(f["q"])}{PLUS}</summary><p>{esc(f["a"])}</p></details>' for f in faq)
    return f'''<section class="section wrap faq-layout" id="faq" aria-labelledby="faq-heading"><div class="faq-title"><div class="eyebrow">Questions practice managers ask</div><h2 id="faq-heading">Good questions.<br><em>Clear answers.</em></h2><p>Short answers to the questions that come up most.</p></div><div class="faq-list">{items}</div></section>'''


def closing_html(h2, p, href, cta):
    return f'''<section class="closing wrap" aria-labelledby="closing-heading"><svg viewBox="0 0 280 300" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M140 290V90M140 195C35 195 20 60 20 60s120 15 120 135Zm0-50C140 35 260 10 260 10s0 135-120 135Z"/></svg><h2 id="closing-heading">{h2}</h2><p>{esc(p)}</p><a class="btn" href="{href}">{esc(cta)} {ARROW}</a></section>'''


def card(a, h='h3'):
    return f'''<a class="related-card" href="/{a['slug']}"><div class="eyebrow">{esc(a['category'])} · {a['reading_minutes']} min read</div><{h}>{esc(strip_tags(a['h1']))}</{h}><p>{esc(a['dek'])}</p></a>'''


def build_article(a, arts, src, org):
    s, head_end, ms, me = src
    url = f"{BASE}/{a['slug']}"
    title = a['title'] if a['title'].endswith('| DrKing') else a['title'] + ' | DrKing'
    assert len(title) <= 60, (a['slug'], len(title))
    desc = a['meta_description']
    assert 70 <= len(desc) <= 160, (a['slug'], len(desc))
    body, toc = add_ids_and_toc(a['body_html'])
    crumbs = f'<nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/blog">Blog</a></nav>'
    upd = f'<span>Updated {nice_date(a["updated"])}</span>' if a['updated'] != a['published'] else ''
    byline = f'<div class="byline"><span>By <a href="#about-this-article">DrKing Editorial Team</a></span><span>Published <time datetime="{a["published"]}">{nice_date(a["published"])}</time></span>{upd}<span>{a["reading_minutes"]} min read</span></div>'
    toc_items = ''.join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
    takeaways = ''.join(f'<li>{esc(t)}</li>' for t in a['key_takeaways'])
    sources = ''.join(f'<li><a href="{esc(x["url"])}" rel="noopener" target="_blank">{esc(x["title"])}</a> — {esc(x["publisher"])}</li>' for x in a['sources'])
    sources_html = f'<section class="sources" aria-labelledby="sources-heading"><h2 id="sources-heading">Sources</h2><ol>{sources}</ol></section>' if a['sources'] else ''
    about = f'''<section class="article-meta-box" id="about-this-article" aria-labelledby="about-heading"><h2 id="about-heading">About this article</h2><p>Written and reviewed by the DrKing Editorial Team for Australian practice owners and practice managers. We check every statistic against the original source linked below and leave out figures we cannot verify. This is general information, not legal, financial or clinical advice — confirm decisions with your own advisers and clinicians.</p><p>Published {nice_date(a['published'])}{'; updated ' + nice_date(a['updated']) if a['updated'] != a['published'] else ''}. Spotted something out of date? <a href="/contact">Tell us</a>.</p></section>'''
    others = [x for x in arts if x['slug'] != a['slug']][:3]
    related = f'''<section class="related wrap" aria-labelledby="related-heading"><div class="eyebrow">Keep reading</div><h2 id="related-heading" style="font:300 clamp(32px,3.4vw,46px)/1.1 var(--serif);margin:14px 0 0">More from the <em style="color:var(--terra)">DrKing Journal</em></h2><div class="related-grid">{''.join(card(x) for x in others)}</div></section>''' if others else ''
    main = f'''<main id="main"> {hero_html(a, a['h1'], a['dek'], crumbs, byline)} <div class="wrap article-shell"><aside class="toc" aria-label="On this page"><p class="toc-title">On this page</p><ol>{toc_items}<li><a href="#faq">FAQs</a></li></ol></aside><article class="article-body" aria-labelledby="hero-title"><details class="mobile-toc"><summary>On this page</summary><ol>{toc_items}<li><a href="#faq">FAQs</a></li></ol></details><section class="takeaways" aria-labelledby="takeaways-heading"><h2 id="takeaways-heading">Key takeaways</h2><ul>{takeaways}</ul></section>{body}{about}{sources_html}</article></div> {faq_html(a['faq'])} {related} {closing_html('Follow-up that <em>keeps going.</em>', 'See how DrKing runs reactivation, reminders and treatment follow-up for Australian practices.', '/demo', 'Book a demo')} </main>'''
    out = s[:ms] + main + s[me:]
    out = set_meta(out, title, desc, url, 'article')
    out = out.replace('</head>', ARTICLE_CSS + '\n</head>', 1)
    out = null_safe(out)
    graph = [org,
        {'@type': 'WebPage', '@id': url + '#webpage', 'reviewedBy': {'@type': 'Organization', 'name': 'DrKing Editorial Team', 'url': BASE + '/about'}, 'url': url, 'name': title, 'description': desc, 'inLanguage': 'en-AU',
         'isPartOf': {'@id': BASE + '/#website'} if False else None, 'publisher': {'@id': BASE + '/#organization'},
         'breadcrumb': {'@id': url + '#breadcrumb'}, 'datePublished': a['published'], 'dateModified': a['updated']},
        {'@type': 'BlogPosting', '@id': url + '#article', 'headline': strip_tags(a['h1'])[:110], 'description': desc,
         'mainEntityOfPage': {'@id': url + '#webpage'}, 'datePublished': a['published'], 'dateModified': a['updated'],
         'author': {'@type': 'Organization', 'name': 'DrKing Editorial Team', 'url': BASE + '/about'},
         'publisher': {'@id': BASE + '/#organization'}, 'inLanguage': 'en-AU',
         'image': 'https://drking.ai/assets/drking-social-share.jpg?v=ae223eb8',
         'keywords': ', '.join([a['primary_keyword']] + a.get('secondary_keywords', [])),
         'citation': [x['url'] for x in a['sources']] or None},
        {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Blog', 'item': BASE + '/blog'},
            {'@type': 'ListItem', 'position': 3, 'name': strip_tags(a['h1'])[:110], 'item': url}]},
        {'@type': 'FAQPage', '@id': url + '#faq', 'mainEntity': [
            {'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in a['faq']]},
    ]
    graph = [{k: v for k, v in n.items() if v is not None} for n in graph]
    out = set_ld(out, graph)
    (ROOT / f"{a['slug']}.html").write_text(out, encoding='utf-8')
    return url


def build_index(arts, src, org):
    s, head_end, ms, me = src
    url = BASE + '/blog'
    title = 'DrKing Blog: Practice Growth Guides | DrKing'
    desc = 'Practical guides for Australian practice owners and managers on patient reactivation, treatment follow-up, no-shows and front-desk communication.'
    cards = ''.join(card(a, 'h2') for a in arts)
    main = f'''<main id="main"> <section class="hero wrap article-hero" aria-labelledby="hero-title" style="padding-bottom:30px"><div class="hero-copy" style="width:100%"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a></nav><div class="eyebrow" style="margin-top:22px">DrKing Journal</div><h1 id="hero-title">Guides for practices that want patients to <em>come back.</em></h1><p class="article-dek">Practical, sourced guides for Australian practice owners and practice managers: patient reactivation, unbooked treatment, no-shows and front-desk follow-up.</p></div></section> <section class="wrap" aria-label="Articles"><div class="blog-list">{cards}</div></section> {closing_html('Follow-up that <em>keeps going.</em>', 'See how DrKing runs reactivation, reminders and treatment follow-up for Australian practices.', '/demo', 'Book a demo')} </main>'''
    out = s[:ms] + main + s[me:]
    out = set_meta(out, title, desc, url, 'website')
    out = out.replace('</head>', ARTICLE_CSS + '\n</head>', 1)
    out = null_safe(out)
    graph = [org,
        {'@type': 'CollectionPage', '@id': url + '#webpage', 'url': url, 'name': title, 'description': desc, 'inLanguage': 'en-AU',
         'publisher': {'@id': BASE + '/#organization'},
         'mainEntity': {'@type': 'ItemList', 'itemListElement': [
             {'@type': 'ListItem', 'position': i + 1, 'url': f"{BASE}/{a['slug']}", 'name': strip_tags(a['h1'])} for i, a in enumerate(arts)]}},
        {'@type': 'Blog', '@id': url + '#blog', 'name': 'DrKing Journal', 'url': url, 'publisher': {'@id': BASE + '/#organization'},
         'blogPost': [{'@id': f"{BASE}/{a['slug']}#article"} for a in arts]}]
    out = set_ld(out, graph)
    (ROOT / 'blog.html').write_text(out, encoding='utf-8')


def update_sitemap(urls):
    p = ROOT / 'sitemap.xml'
    s = p.read_text(encoding='utf-8')
    today = date.today().isoformat()
    for u in urls:
        if f'<loc>{u}</loc>' in s:
            continue
        s = s.replace('</urlset>', f'  <url><loc>{u}</loc></url>\n</urlset>', 1)
    p.write_text(s, encoding='utf-8')


def footer_link():
    old = '<div><h2>Resources</h2><a href="/case-studies">'
    new = '<div><h2>Resources</h2><a href="/blog">Blog</a><a href="/case-studies">'
    n = 0
    for f in ROOT.glob('*.html'):
        t = f.read_text(encoding='utf-8')
        if old in t:
            f.write_text(t.replace(old, new, 1), encoding='utf-8'); n += 1
    return n


if __name__ == '__main__':
    arts = load_articles()
    src = fork_parts()
    org = org_node(src[0])
    urls = [build_article(a, arts, src, org) for a in arts]
    build_index(arts, src, org)
    update_sitemap([BASE + '/blog'] + urls)
    print('articles', len(arts), 'footer links added', footer_link())
