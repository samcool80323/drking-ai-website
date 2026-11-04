#!/usr/bin/env python3
"""Set page title/description everywhere they must match (title, meta, og when equal, JSON-LD page node).
Usage: edit CHANGES below; run from repo root. Asserts every replacement."""
import html, json, re
from pathlib import Path

import sys
CHANGES = {
    'ai-chat.html': ('AI Chat for Medical Clinics in Australia | DrKing', None),
    'medical-centres.html': ('Communication Software for Medical Centres | DrKing', None),
    'text-to-pay.html': ('Text-to-Pay for Australian Medical Practices | DrKing', None),
    'veterinary.html': ('AI Receptionist for Vet Clinics in Australia | DrKing', None),
    'aged-care.html': ('Communication Automation for Aged Care | DrKing', None),
    'cosmetic-clinics.html': ('Lead Conversion for Cosmetic Clinics Australia | DrKing', None),
    'slow-follow-up.html': ('Stop Losing Patients to Slow Follow-Up | DrKing', None),
    'missed-call-recovery.html': ('Missed Call Text-Back for Australian Clinics | DrKing', None),
    'roi-calculator.html': ('Clinic Revenue Leak Calculator | DrKing', None),
    'patient-no-shows.html': ('Reduce Patient No-Shows in Australian Clinics | DrKing', None),
    'vs-receptionist.html': ('AI Receptionist vs Human Receptionist for Clinics | DrKing', None),
}
PAGE_TYPES = {'WebPage', 'AboutPage', 'ContactPage', 'CollectionPage', 'FAQPage', 'ItemPage'}

for f, (title, desc) in CHANGES.items():
    p = Path(f); s = p.read_text(encoding='utf-8')
    assert len(title) <= 60, (f, len(title))
    old_t = html.unescape(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    old_d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    new_d = desc or old_d
    assert 70 <= len(new_d) <= 160, (f, len(new_d))
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{html.escape(title, quote=False)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*"', lambda m: f'<meta name="description" content="{html.escape(new_d)}"', s, count=1)
    for prop, old, new in (('og:title', old_t, title), ('og:description', old_d, new_d)):
        s = re.sub(rf'<meta property="{prop}" content="([^"]*)"',
                   lambda m: f'<meta property="{prop}" content="{html.escape(new)}"' if html.unescape(m.group(1)) == old else m.group(0), s, count=1)
    m = re.search(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', s, re.S)
    g = json.loads(m.group(2)); hit = 0
    for n in g['@graph']:
        t = n.get('@type'); t = t if isinstance(t, list) else [t]
        if PAGE_TYPES & set(t) and n.get('name') == old_t:
            n['name'] = title; hit += 1
            if n.get('description') == old_d: n['description'] = new_d
    assert hit == 1, (f, 'page node not found')
    if f == 'index.html' and False:
        for n in g['@graph']:
            if n.get('@type') == 'WebSite':
                n['alternateName'] = ['DrKing AI', 'Dr King AI', 'drking.ai']
            if n.get('@type') == 'Organization':
                n['alternateName'] = 'DrKing AI'
    payload = json.dumps(g, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:m.start(2)] + payload + s[m.end(2):]
    p.write_text(s, encoding='utf-8')
    print(f, '->', title)
