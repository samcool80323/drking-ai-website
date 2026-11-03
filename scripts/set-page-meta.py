#!/usr/bin/env python3
"""Set page title/description everywhere they must match (title, meta, og when equal, JSON-LD page node).
Usage: edit CHANGES below; run from repo root. Asserts every replacement."""
import html, json, re
from pathlib import Path

CHANGES = {
    'index.html': ('DrKing | AI Receptionist and Patient Messaging for Clinics',
                   'AI receptionist and patient communication for Australian clinics: answers calls and chats, books appointments, sends reminders and brings patients back.'),
    'ai-voice-receptionist.html': ('AI Receptionist for Clinics in Australia | DrKing',
                   'An AI receptionist (virtual receptionist) for Australian clinics that answers calls, books appointments and hands complex calls to your team, day and night.'),
    'online-booking.html': ('Online Booking System for Clinics in Australia | DrKing', None),
    'appointment-reminders.html': ('Appointment Reminders by SMS for Clinics | DrKing', None),
    'after-hours.html': ('After-Hours Answering Service for Clinics | DrKing', None),
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
    if f == 'index.html':
        for n in g['@graph']:
            if n.get('@type') == 'WebSite':
                n['alternateName'] = ['DrKing AI', 'Dr King AI', 'drking.ai']
            if n.get('@type') == 'Organization':
                n['alternateName'] = 'DrKing AI'
    payload = json.dumps(g, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    s = s[:m.start(2)] + payload + s[m.end(2):]
    p.write_text(s, encoding='utf-8')
    print(f, '->', title)
