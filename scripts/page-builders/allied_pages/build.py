#!/usr/bin/env python3
"""Fork allied-health.html into 4 practice-type pages (text-only replacements, asserted)."""
import json, re, sys, os, importlib.util

REPO = '/app/data/workspaces/drking-two-guides-20261030'
SRC = open(os.path.join(REPO, 'allied-health.html'), encoding='utf-8').read()
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('content', os.path.join(HERE, 'content.py'))
content = importlib.util.module_from_spec(spec); spec.loader.exec_module(content)

DEMO = 'https://api.leadconnectorhq.com/widget/form/BEzIsss2MUaVG0NelbYd'
ARROW = '<svg class="icon" aria-hidden="true"><use href="#arrow"/></svg>'
CHECK = '<svg class="icon" aria-hidden="true"><use href="#check"/></svg>'


def ic(name):
    return f'<svg class="icon" aria-hidden="true"><use href="#{name}"/></svg>'


def between(s, start, end):
    assert s.count(start) == 1, ('start not unique', start, s.count(start))
    i = s.index(start)
    j = s.index(end, i)
    return s[i:j]


def link(href, text):
    return f'<a href="{href}" style="text-decoration:underline;text-underline-offset:3px">{text}</a>'


# ---------- section templates (same markup as fork) ----------
def t_hero(p):
    return f'<div class="eyebrow">{p["eyebrow"]}</div><h1>{p["h1"]}</h1><p>{p["hero_p"]}</p>'


def t_float(p):
    a, b = p['float']
    return (f'<div class="float-card call-card"><div class="round-icon">{ic("phone")}</div><div><strong>{a[0]}</strong><small>{a[1]}</small></div></div>'
            f'<div class="float-card plan-card"><div class="plan-top"><div class="round-icon">{ic("calendar")}</div><div><strong>{b[0]}</strong><small>{b[1]}</small></div></div>')


def t_spec(p):
    head, items = p['spec']
    return f'<span>{head}</span>' + ''.join(f'<div class="specialty">{ic(i)}{t}</div>' for i, t in items)


def t_stats(p):
    label, items, note = p['stats']
    return (f'<section class="stats" aria-label="{label}"><div class="wrap"><div class="stats-grid">'
            + ''.join(f'<div class="stat"><div class="stat-value">{v}</div><p>{t}</p></div>' for v, t in items)
            + f'</div><p class="stats-note">{note}</p></div></section>')


def t_problem(p):
    pr = p['problem']
    cards = ''.join(
        f'<article class="problem-card reveal"><div class="problem-top">{ic(i)}<span class="small-num">{n}</span></div><h3>{h}</h3><p>{t}</p></article>'
        for i, n, h, t in pr['cards'])
    L = pr['loss']
    return (f'<section class="section wrap" id="the-problem"><div class="section-heading reveal"><div><div class="eyebrow">{pr["eyebrow"]}</div><h2>{pr["h2"]}</h2></div><p>{pr["p"]}</p></div>'
            f'<div class="problem-grid">{cards}</div>'
            f'<div class="loss reveal"><div><div class="loss-label">{L["label"]}</div><h3>{L["h3"]}</h3><div class="loss-inputs"><label for="lost-patients">{L["input"]}</label>'
            f'<input id="lost-patients" type="number" min="0" max="1000" step="1" value="{L["value"]}" inputmode="numeric"><span>{L["span"]}</span></div></div>'
            f'<div class="loss-result"><output id="loss-total" for="lost-patients" aria-live="polite">{L["value"] * L["mult"]:,}</output><p>{L["result"]}</p><small>{L["small"]}</small></div></div></section>')


def t_works(p):
    w = p['works']
    icons = ['arrow', 'arrow', 'check']
    steps = ''.join(f'<article class="step reveal"><div class="step-no">0{k+1}{ic(icons[k])}</div><h3>{h}</h3><p>{t}</p></article>' for k, (h, t) in enumerate(w['steps']))
    return (f'<section class="works" id="how-it-works"><div class="wrap"><div class="center-heading reveal"><div class="eyebrow">{w["eyebrow"]}</div><h2>{w["h2"]}</h2><p>{w["p"]}</p></div>'
            f'<div class="steps">{steps}</div></div></section>')


def copy(f, benefit=True):
    b = f'<div class="feature-benefit">{CHECK}{f["benefit"]}</div>' if benefit and f.get('benefit') else ''
    cls = 'text-link demo-link' if f['href'] == DEMO else 'text-link'
    return f'<div class="feature-copy"><div class="eyebrow">{f["eyebrow"]}</div><h3>{f["h3"]}</h3><p>{f["p"]}</p>{b}<a class="{cls}" href="{f["href"]}">{f["link"]} {ARROW}</a></div></div>'


def t_features(p):
    F = p['features']
    out = (f'<section class="section features wrap" id="features"><div class="center-heading reveal"><div class="eyebrow">{F["eyebrow"]}</div><h2>{F["h2"]}</h2><p>{F["p"]}</p></div>\n')
    f1 = F['f1']
    rows = ''.join(f'<div class="appointment"><div class="date-box">{m}<b>{d}</b></div><div><p>{t}</p><small>{s}</small></div><span class="chip">{c}</span></div>' for m, d, t, s, c in f1['rows'])
    out += (f'<div class="feature-row reveal"><div class="feature-visual sage"><div class="app-card"><div class="app-head"><div>{f1["head"]}<div class="app-sub">{f1["sub"]}</div></div>{ic("calendar")}</div>'
            f'{rows}<div class="mini-banner">{CHECK}{f1["banner"]}</div></div><span class="preview-label">Product illustration</span></div>' + copy(f1) + '\n')
    f2 = F['f2']
    c2 = ''.join(f'<div class="bubble{" out" if o else ""}">{t}</div>' for o, t in f2['chat'])
    out += (f'<div class="feature-row reveal"><div class="feature-visual sand"><div class="app-card"><div class="phone-heading"><div class="round-icon">{ic("leaf")}</div><div><strong>{f2["head"]}</strong><div class="app-sub">{f2["sub"]}</div></div></div>'
            f'<div class="chat">{c2}<div class="mini-banner">{CHECK}{f2["banner"]}</div></div></div><span class="preview-label">Example conversation</span></div>' + copy(f2, False) + '\n')
    f3 = F['f3']
    out += (f'<div class="feature-row reveal"><div class="feature-visual"><div class="app-card"><div class="phone-heading"><div class="round-icon">{ic("calendar")}</div><div><strong>{f3["head"]}</strong><div class="app-sub">{f3["sub"]}</div></div></div>'
            f'<div class="chat"><div class="chat-time">{f3["time"]}</div><div class="bubble">{f3["msg"]}</div><div class="bubble out">{f3["reply"]}</div><div class="mini-banner">{CHECK}{f3["banner"]}</div></div></div><span class="preview-label">Example conversation</span></div>' + copy(f3) + '\n')
    f4 = F['f4']
    c4 = ''.join(f'<div class="bubble{" out" if o else ""}">{t}</div>' for o, t in f4['chat'])
    out += (f'<div class="feature-row reveal"><div class="feature-visual sage"><div class="app-card"><div class="app-head">{f4["head"]} {ic(f4["icon"])}</div>'
            f'<div class="chat">{c4}<div class="mini-banner">{ic("calendar")}{f4["banner"]}</div></div></div><span class="preview-label">Example conversation</span></div>' + copy(f4, False) + '\n')
    f5 = F['f5']
    out += (f'<div class="feature-row reveal"><div class="feature-visual sand"><div class="app-card"><div class="app-head">Simple, secure payments {ic("shield")}</div>'
            f'<div class="pay-total"><small>{f5["small1"]}</small><p>{f5["big"]}</p><small>{f5["small2"]}</small></div><div class="mock-button">Pay securely <span aria-hidden="true">↗</span></div><div class="payment-methods">Secure payment link · No app needed</div></div><span class="preview-label">Product illustration</span></div>' + copy(f5, False) + '\n')
    f6 = F['f6']
    out += (f'<div class="feature-row reveal"><div class="feature-visual"><div class="app-card"><div class="app-head">{f6["head"]} {ic(f6["icon"])}</div><div class="stars" aria-hidden="true">{f6["stars"]}</div>'
            f'<div class="review-copy">{f6["quote"]}</div><div class="bubble" style="max-width:100%">{f6["msg"]}</div><div class="app-sub" style="text-align:center;margin-top:13px">{f6["note"]}</div></div><span class="preview-label">{f6["label"]}</span></div>' + copy(f6, False) + '\n')
    return out


def t_voice_copy(p):
    v = p['voice']
    return f'<div class="voice-copy"><div class="eyebrow">{v["eyebrow"]}</div><h2>{v["h2"]}</h2><p>{v["p"]}</p></div>'


def t_why(p):
    w = p['why']
    items = ''.join(f'<article class="why-item reveal"><span class="why-number">0{k+1}</span><div><h3>{h}</h3><p>{t}</p></div></article>' for k, (h, t) in enumerate(w['items']))
    return (f'<section class="section wrap" id="why-drking"><div class="section-heading reveal"><div><div class="eyebrow">{w["eyebrow"]}</div><h2>{w["h2"]}</h2></div><p>{w["p"]}</p></div>'
            f'<div class="why-grid">{items}</div></section>')


def t_faq(p):
    fq = p['faq']
    items = ''.join(f'<details name="allied-faq"{" open" if k == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for k, (q, a) in enumerate(fq['items']))
    return (f'<section class="faq" id="faq"><div class="faq-intro reveal"><div class="eyebrow">A few things you might be wondering</div><h2>Good questions.<br><em>Clear answers.</em></h2><p>{fq["intro"]}</p>'
            f'<a class="text-link demo-link" href="{DEMO}">Let’s talk about your practice {ARROW}</a></div><div class="faq-list reveal">{items}</div></section>')


def t_cta(p):
    c = p['cta']
    return f'<div class="eyebrow">{c["eyebrow"]}</div><h2>{c["h2"]}</h2><p>{c["p"]}</p>'


def build(p):
    s = SRC
    n = 0

    def rep(old, new, count=1):
        nonlocal s, n
        c = s.count(old)
        if c != count:
            sys.exit(f'[{p["slug"]}] expected {count} of {old[:90]!r}, found {c}')
        s = s.replace(old, new); n += 1

    slug = p['slug']; url = f'https://drking.ai/{slug}'
    # head
    rep('<title>AI Communication for Allied Health Practices | DrKing</title>', f'<title>{p["title"]}</title>')
    rep('<meta name="description" content="DrKing helps Australian allied health practices answer enquiries, support appointment booking and follow up with patients between visits.">',
        f'<meta name="description" content="{p["meta"]}">')
    rep('<link rel="canonical" href="https://drking.ai/allied-health">', f'<link rel="canonical" href="{url}">')
    rep('content="DrKing — AI Practice Management for Allied Health in Australia"', f'content="{p["og_title"]}"')
    rep('content="More completed treatment plans. Less admin. AI communication and growth for Australian allied health practices."', f'content="{p["meta"]}"')
    rep('<meta property="og:url" content="https://drking.ai/allied-health">', f'<meta property="og:url" content="{url}">')
    # body sections
    rep(between(s, '<div class="eyebrow">For allied health practices in Australia</div>', '<div class="hero-actions">'), t_hero(p))
    rep('A calm allied health treatment room, with a practitioner helping a patient stretch while DrKing looks after their bookings.', p['svg_title'])
    rep(between(s, '<div class="float-card call-card">', '<div class="plan-dots"'), t_float(p))
    rep('<span>Every session, taken care of</span>', f'<span>{p["plan_bottom"]}</span>')
    rep('You care for them.<br>We take care of the rest.', p['caption'])
    rep(between(s, '<span>Built for the way<br>you care.</span>', '</div></div></section>\n<section class="stats"'), t_spec(p))
    rep(between(s, '<section class="stats" aria-label=', '\n<section class="section wrap" id="the-problem">'), t_stats(p))
    rep(between(s, '<section class="section wrap" id="the-problem">', '\n<svg class="wave"'), t_problem(p))
    rep(between(s, '<section class="works" id="how-it-works">', '\n<section class="section features wrap"'), t_works(p))
    rep(between(s, '<section class="section features wrap" id="features">', '<div class="voice reveal" id="voice-ai">'), t_features(p))
    rep(between(s, '<div class="voice-copy">', '<div><div class="voice-player"'), t_voice_copy(p))
    old_tr = 'Thanks for calling your allied health practice. I can help you book your next appointment. What day works best for you?'
    rep(f'<span>DRKING</span>“{old_tr}”', f'<span>DRKING</span>“{p["voice"]["transcript"]}”')
    rep(f"new SpeechSynthesisUtterance('{old_tr}')", f"new SpeechSynthesisUtterance('{p['voice']['transcript'].replace(chr(39), chr(8217))}')")
    rep(between(s, '<section class="section wrap" id="why-drking">', '\n<div class="wrap"><section class="security'), t_why(p))
    rep('<h3>Clinical records stay in your practice software.</h3><p>Data is handled in line with what’s agreed for your deployment. Ask us about your practice’s requirements.</p>',
        f'<h3>{p["security"][0]}</h3><p>{p["security"][1]}</p>')
    rep(between(s, '<section class="faq" id="faq">', '\n<section class="final-cta'), t_faq(p))
    rep(between(s, '<div class="eyebrow">Better follow-through starts here</div>', '<a class="btn demo-link"'), t_cta(p))
    # calculator: session/enquiry units instead of dollars
    rep("const currency = new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD', maximumFractionDigits: 0 });",
        "const currency = new Intl.NumberFormat('en-AU', { maximumFractionDigits: 0 });")
    rep('currency.format(Number(lostPatients.value) * 4 * 120 * 52)', f'currency.format(Number(lostPatients.value) * {p["problem"]["loss"]["formula"]})')

    # JSON-LD (single @graph) — rewrite page-specific nodes
    m = re.search(r'(<script type="application/ld\+json" id="structured-data">)(.*?)(</script>)', s, re.S)
    data = json.loads(m.group(2))
    for node in data['@graph']:
        t = node['@type']
        if t == 'WebPage':
            node.update({'@id': f'{url}#webpage', 'url': url, 'name': p['title'], 'description': p['meta'],
                         'mainEntity': {'@id': f'{url}#service'}, 'breadcrumb': {'@id': f'{url}#breadcrumb'}})
            node['about']['description'] = p['about']
        elif t == 'Service':
            node.update({'@id': f'{url}#service', 'name': p['service']})
            node['audience']['audienceType'] = p['audience']
        elif t == 'FAQPage':
            node['@id'] = f'{url}#faq'
            node['mainEntity'] = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faq']['items']]
        elif t == 'BreadcrumbList':
            node['@id'] = f'{url}#breadcrumb'
            node['itemListElement'] = [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://drking.ai/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Industries', 'item': 'https://drking.ai/industries'},
                {'@type': 'ListItem', 'position': 3, 'name': 'Allied health', 'item': 'https://drking.ai/allied-health'},
                {'@type': 'ListItem', 'position': 4, 'name': p['crumb'], 'item': url}]
    new_ld = m.group(1) + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + m.group(3)
    rep(m.group(0), new_ld)

    # checks
    title = p['title']; meta = p['meta']
    assert len(title) <= 60, (slug, len(title)); assert 70 <= len(meta) <= 160, (slug, len(meta))
    assert '&' not in title and '&' not in meta
    assert s.startswith('<!DOCTYPE html>') or s[:15].lower() == '<!doctype html>'
    vis = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    for bad in ['$', '%', 'never miss', 'every call', 'guarantee', 'Alex', 'Sam ']:
        hits = [x for x in re.findall(r'.{0,40}' + re.escape(bad) + r'.{0,40}', vis, flags=re.I)]
        hits = [h for h in hits if 'not industry data or a guarantee' not in h.lower() and 'aud unless' not in h.lower() and 'financial examples' not in h.lower()]
        if hits:
            print(f'  WARN {slug}: {bad!r}: {hits[:3]}')
    out = os.path.join(REPO, f'{slug}.html')
    open(out, 'w', encoding='utf-8').write(s)
    print(f'{slug}.html: {n} replacements; title {len(title)}; meta {len(meta)}')


if __name__ == '__main__':
    for page in content.PAGES:
        build(page)
