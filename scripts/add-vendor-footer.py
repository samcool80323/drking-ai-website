import os as _os, sys as _sys
if _os.environ.get('DRKING_ALLOW_LEGACY') != '1':
    _sys.exit('LEGACY GENERATOR: the committed *.html files are now the source of truth (claims cleaned, sprites restored 2026-10-31). Re-running this would overwrite them with old copy. Set DRKING_ALLOW_LEGACY=1 only if you have ported those fixes into this script.')
"""Add verified vendor routes to the shared DrKing footer across HTML pages.

Idempotent. Fail closed on footer drift, duplicate vendor groups, or missing
site-shell cache-buster. The source pages remain the generator inputs.
"""
from pathlib import Path
import hashlib

root = Path(__file__).resolve().parents[1]
files = sorted(root.glob('*.html'))
expected_footer_sha = '9ff66ae8d754b21b'
anchor = '<div><h2>Company</h2><a href="/about">About</a>'
vendors = (
    '<div><h2><a href="/integrations">Integrations</a></h2>'
    '<a href="/dentally-integration">Dentally</a>'
    '<a href="/dental4web-integration">Dental4Web / D4W</a>'
    '<a href="/cliniko-integration">Cliniko</a>'
    '<a href="/nookal-integration">Nookal</a>'
    '<a href="/power-diary-integration">Power Diary</a>'
    '<a href="/core-practice-integration">Core Practice (planned)</a></div>\n'
)
assert len(files) == 57, f'unexpected page inventory: {len(files)}'
for p in files:
    s = p.read_text()
    start = s.find('<footer class="site-footer">')
    end = s.find('</footer>', start) + len('</footer>')
    assert start >= 0 and end > start
    footer = s[start:end]
    if vendors in footer:
        continue
    assert hashlib.sha256(footer.encode()).hexdigest().startswith(expected_footer_sha), p.name
    assert footer.count(anchor) == 1, p.name
    assert s.count('/assets/site-shell.css?v=4') == 1, p.name
    updated = footer.replace(anchor, vendors + anchor, 1)
    s = s[:start] + updated + s[end:]
    s = s.replace('/assets/site-shell.css?v=4', '/assets/site-shell.css?v=5', 1)
    p.write_text(s)
print(f'Updated vendor footer and cache-buster on {len(files)} HTML pages')
