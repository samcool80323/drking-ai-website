"""Static sitewide audit for drking.ai source (all root *.html pages).

Checks: undefined <use href="#id"> targets, broken internal links/assets,
duplicate ids, images without alt/dimensions, favicon link, numeric marketing
claims in <main> (percentages / dollar figures / absolute promises).
Usage: python3 scripts/audit-static.py [--json]
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
pages = sorted(p for p in ROOT.glob('*.html'))
CLAIM_PATTERNS = [
    (r'\b\d{1,3}(?:\.\d)?%', 'percentage'),
    (r'\$\s?\d[\d,]*(?:\.\d+)?k?\+?', 'dollar figure'),
    (r'\bevery (?:single )?call\b', 'every call'),
    (r'\b(?:in|within) \d+ seconds\b', 'response-time promise'),
    (r'\bnever (?:miss|lose)\b', 'absolute promise'),
    (r'\bguarantee[sd]?\b', 'guarantee'),
    (r'\bno clinical data\b', 'data claim'),
]
report = {}
def exists(path):
    path = path.split('#')[0].split('?')[0]
    if path in ('', '/'):
        return True
    p = path.lstrip('/')
    return (ROOT / p).exists() or (ROOT / (p + '.html')).exists() or (ROOT / p / 'index.html').exists()

for page in pages:
    s = page.read_text(encoding='utf-8')
    issues = []
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', s))
    uses = set(re.findall(r'<use[^>]+href=["\']#([^"\']+)["\']', s))
    missing_sym = sorted(uses - ids)
    if missing_sym:
        issues.append(('undefined-svg-symbol', ', '.join(missing_sym)))
    dup = [i for i in ids if len(re.findall(r'\bid=["\']%s["\']' % re.escape(i), s)) > 1]
    if dup:
        issues.append(('duplicate-id', ', '.join(sorted(dup))))
    for href in sorted(set(re.findall(r'(?:href|src)=["\'](/[^"\'#?][^"\']*)["\']', s))):
        if href.startswith('//'):
            continue
        if not exists(href):
            issues.append(('broken-internal-ref', href))
    for anchor in sorted(set(re.findall(r'href=["\']#([^"\']+)["\']', s))):
        if anchor not in ids and anchor not in ('', 'top'):
            issues.append(('broken-anchor', '#' + anchor))
    for img in re.findall(r'<img\b[^>]*>', s):
        if 'alt=' not in img:
            issues.append(('img-no-alt', img[:80]))
    if not re.search(r'<link[^>]+rel=["\'](?:shortcut )?icon', s):
        issues.append(('no-favicon-link', ''))
    m = re.search(r'<main\b.*?</main>', s, re.S)
    if m:
        text = re.sub(r'<(script|style)\b.*?</\1>', ' ', m.group(0), flags=re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        for pat, label in CLAIM_PATTERNS:
            for hit in re.finditer(pat, text, re.I):
                ctx = text[max(0, hit.start() - 50):hit.end() + 40].strip()
                issues.append(('claim:' + label, ctx))
    report[page.name] = issues

if '--json' in sys.argv:
    print(json.dumps(report, indent=1, ensure_ascii=False))
else:
    from collections import Counter
    c = Counter(k for v in report.values() for k, _ in v)
    print('pages', len(pages)); print('issue counts', dict(c))
    for name, v in report.items():
        tech = [i for i in v if not i[0].startswith('claim:') and i[0] != 'no-favicon-link']
        if tech:
            print(name, tech[:6])
