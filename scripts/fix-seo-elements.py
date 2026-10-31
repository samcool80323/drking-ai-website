import os as _os, sys as _sys
if _os.environ.get('DRKING_ALLOW_LEGACY') != '1':
    _sys.exit('LEGACY GENERATOR: the committed *.html files are now the source of truth (claims cleaned, sprites restored 2026-10-31). Re-running this would overwrite them with old copy. Set DRKING_ALLOW_LEGACY=1 only if you have ported those fixes into this script.')
"""Fix all remaining SEO elements on vendor pages: og tags, JSON-LD,
titles, breadcrumb schema, and stale references from the fork source."""
from pathlib import Path
import json, re

root = Path(__file__).resolve().parents[1]

FIX = {
    'dentally-integration': {
        'vendor': 'Dentally', 'type': 'Dental Clinics',
        'title': 'DrKing + Dentally | AI Receptionist for Dental Clinics',
        'og_title': 'Your Dentally calendar. Always full. | DrKing',
        'old_dentist': 'Dr Patel', 'new_dentist': 'Dr Chen',
    },
    'dental4web-integration': {
        'vendor': 'Dental4Web', 'type': 'Dental Practices',
        'title': 'DrKing + Dental4Web | AI Receptionist for Dental',
        'og_title': 'Your Dental4Web calendar. Always full. | DrKing',
        'old_dentist': 'Dr Patel', 'new_dentist': 'Dr Chen',
    },
    'core-practice-integration': {
        'vendor': 'Core Practice', 'type': 'Dental Clinics',
        'title': 'DrKing + Core Practice | AI Receptionist for Dental',
        'og_title': 'Core Practice. Coming soon. | DrKing',
        'old_dentist': 'Dr Patel', 'new_dentist': 'Dr Lee',
    },
    'cliniko-integration': {
        'vendor': 'Cliniko', 'type': 'Allied Health',
        'title': 'DrKing + Cliniko | AI Receptionist for Allied Health',
        'og_title': 'Your Cliniko calendar. Always full. | DrKing',
        'old_dentist': 'Dr Patel', 'new_dentist': 'Sarah',
    },
    'nookal-integration': {
        'vendor': 'Nookal', 'type': 'Allied Health',
        'title': 'DrKing + Nookal | AI Receptionist for Allied Health',
        'og_title': 'Your Nookal calendar. Always full. | DrKing',
        'old_dentist': 'Dr Patel', 'new_dentist': 'James',
    },
    'power-diary-integration': {
        'vendor': 'Power Diary', 'type': 'Psychology',
        'title': 'DrKing + Power Diary | AI Receptionist for Psychology',
        'og_title': 'Your Power Diary calendar. Always full. | DrKing',
        'old_dentist': 'Dr Patel', 'new_dentist': 'Dr Taylor',
    },
}

for slug, f in FIX.items():
    p = root / (slug + '.html')
    s = p.read_text()
    vendor = f['vendor']
    url = f'https://drking.ai/{slug}'

    # 1. Fix <title>
    old_title = f'<title>DrKing + {vendor} \u2014 AI Receptionist for Your Practice</title>'
    new_title = f'<title>{f["title"]}</title>'
    if old_title in s:
        s = s.replace(old_title, new_title, 1)
    else:
        # generic fallback: replace any title
        s = re.sub(r'<title>[^<]*</title>', new_title, s, count=1)

    # 2. Fix og:url
    s = s.replace(
        'property="og:url" content="https://drking.ai/missed-call-recovery"',
        f'property="og:url" content="{url}"', 1)

    # 3. Fix og:title
    s = re.sub(
        r'property="og:title" content="[^"]*"',
        f'property="og:title" content="{f["og_title"]}"', s, count=1)

    # 4. Fix og:description (match meta description)
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', s)
    if desc_m:
        s = re.sub(r'property="og:description" content="[^"]*"',
                   f'property="og:description" content="{desc_m.group(1)}"', s, count=1)

    # 5. Fix remaining "missed-call-recovery" in JSON-LD and schema
    # (only in URLs, not in nav links which correctly point to /missed-call-recovery)
    # og:url already fixed. Fix JSON-LD:
    s = s.replace(f'"@id":"https://drking.ai/missed-call-recovery#webpage"',
                  f'"@id":"{url}#webpage"', 1)
    s = s.replace(f'"url":"https://drking.ai/missed-call-recovery","description"',
                  f'"url":"{url}","description"', 1)
    # BreadcrumbList
    s = s.replace('"name":"Missed Call Recovery","item":"https://drking.ai/missed-call-recovery"',
                  f'"name":"{vendor}","item":"{url}"', 1)

    # 6. Fix stale dentist name
    s = s.replace(f['old_dentist'], f['new_dentist'])

    # 7. Update JSON-LD WebPage name to match new title
    m = re.search(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', s)
    if m:
        try:
            data = json.loads(m.group(1))
            for node in data.get('@graph', []):
                if node.get('@type') == 'WebPage':
                    node['name'] = f['title']
                    node['url'] = url
            new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            s = s[:m.start(1)] + new_json + s[m.end(1):]
        except (json.JSONDecodeError, ValueError):
            pass

    p.write_text(s)

    # verify
    remaining = s.count('missed-call-recovery')
    # nav links legitimately point there; subtract them
    nav_count = s.count('href="/missed-call-recovery"')
    seo_leftovers = remaining - nav_count
    print(f'{slug}: title="{f["title"][:50]}" og_url={"OK" if url in s else "FAIL"} '
          f'jsonld_name={"OK" if f["title"] in s else "FAIL"} '
          f'stale_dentist={"FIXED" if f["old_dentist"] not in s else "STILL THERE"} '
          f'seo_leftovers={seo_leftovers}')

print('\nAll vendor pages fixed')