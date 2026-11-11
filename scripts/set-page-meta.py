#!/usr/bin/env python3
"""Set page title/description everywhere they must match (title, meta, og when equal, JSON-LD page node).
Usage: edit CHANGES below; run from repo root. Asserts every replacement."""
import html, json, re
from pathlib import Path

import sys
CHANGES = {
    'ai-chat.html': (None, 'DrKing AI chat answers patient questions on your clinic website day and night, captures enquiries and guides people to book. Built for Australian clinics.'),
    'veterinary.html': (None, 'An AI receptionist for Australian vet clinics: answers the phone day and night, escalates emergencies, takes bookings and reassures worried pet owners.'),
    'about.html': (None, 'DrKing is the Australian AI front desk for clinics: calls, chat, SMS and email in one inbox, with booking, reminders and patient follow-up built in.'),
    'missed-calls.html': (None, 'Missed calls are lost patients. DrKing recovers missed clinic calls with automatic text-back that captures the enquiry and guides patients to book.'),
    'missed-call-recovery.html': (None, 'Missed call text-back for Australian clinics: when a call rings out, DrKing sends an SMS, captures the details and guides patients back to booking.'),
    'lead-management.html': (None, 'Every clinic enquiry in one pipeline: DrKing tracks leads from calls, chat and campaigns, automates follow-up and shows which channels fill your diary.'),
    'ai-voice-receptionist.html': (None, 'DrKing\'s AI voice receptionist answers your clinic\'s phone day and night, books appointments and hands urgent calls to your team. Built for Australian clinics.'),
    'dentists.html': (None, 'DrKing is the AI receptionist for dental clinics in Australia: answers calls, books appointments, sends reminders and reactivates patients. Book a free demo.'),
    'physiotherapy.html': (None, 'AI receptionist for Australian physiotherapy clinics: answers new-injury calls, books assessments, reminds treatment blocks and follows up old patients.'),
    'psychology.html': (None, 'AI admin support for Australian psychology practices: answers calls, books sessions, sends reminders and handles admin so your team stays with clients.'),
    'chiropractic.html': (None, 'AI receptionist for Australian chiropractic clinics: answers calls, books adjustments, sends reminders and follows up care plans. Book a free demo.'),
    'podiatry.html': (None, 'AI receptionist for Australian podiatry clinics: answers calls, books appointments, sends reminders and follows up old patients. Book a free demo.'),
    'allied-health.html': (None, 'AI receptionist for Australian allied health clinics: physio, psych, chiro and podiatry. One inbox, online booking, reminders and follow-up. Book a demo.'),
}
PAGE_TYPES = {'WebPage', 'AboutPage', 'ContactPage', 'CollectionPage', 'FAQPage', 'ItemPage'}

for f, (title, desc) in CHANGES.items():
    p = Path(f); s = p.read_text(encoding='utf-8')
    if title is not None:
        assert len(title) <= 60, (f, len(title))
    old_t = html.unescape(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    old_d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    new_d = desc or old_d
    assert 70 <= len(new_d) <= 160, (f, len(new_d))
    new_t = title if title is not None else old_t
    s = re.sub(r'<title>.*?</title>', lambda m: f'<title>{html.escape(new_t, quote=False)}</title>', s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*"', lambda m: f'<meta name="description" content="{html.escape(new_d)}"', s, count=1)
    for prop, old, new in (('og:title', old_t, new_t), ('og:description', old_d, new_d)):
        s = re.sub(rf'<meta property="{prop}" content="([^"]*)"',
                   lambda m: f'<meta property="{prop}" content="{html.escape(new)}"' if html.unescape(m.group(1)) == old else m.group(0), s, count=1)
    m = re.search(r'(<script type="application/ld\+json"[^>]*>)(.*?)(</script>)', s, re.S)
    g = json.loads(m.group(2)); hit = 0
    for n in g['@graph']:
        t = n.get('@type'); t = t if isinstance(t, list) else [t]
        if PAGE_TYPES & set(t) and n.get('name') == old_t:
            n['name'] = new_t; hit += 1
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
