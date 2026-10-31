"""Restore SVG icon sprites that the 2026-09-16 header/footer unification stripped.

Many pages reference <use href="#id"> symbols whose <symbol> definitions were removed,
so icons, blob backgrounds and waveforms render blank. This re-injects the ORIGINAL
symbols from the approved design sources in /app/data/workspaces/drking-variants.
Idempotent: only injects ids that are still undefined; existing sprite is replaced.
Usage: python3 scripts/restore-svg-sprites.py [--check]
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = Path('/app/data/workspaces/drking-variants')
MARK_START, MARK_END = '<!-- drking-svg-sprite -->', '<!-- /drking-svg-sprite -->'

def variant_symbols():
    out = {}
    for f in sorted(VARIANTS.glob('*/index.html')):
        s = f.read_text(errors='ignore')
        syms = {m.group(1): m.group(0) for m in re.finditer(r'<symbol\b[^>]*\bid="([^"]+)".*?</symbol>', s, re.S)}
        grads = {m.group(1): m.group(0) for m in re.finditer(r'<(linearGradient|radialGradient|clipPath|pattern)\b[^>]*\bid="([^"]+)".*?</\1>', s, re.S) for _ in [0]}
        if syms:
            out[f.parent.name] = (syms, {m.group(2): m.group(0) for m in re.finditer(r'<(linearGradient|radialGradient|clipPath|pattern)\b[^>]*\bid="([^"]+)".*?</\1>', s, re.S)})
    return out

def page_ids(s):
    s2 = re.sub(re.escape(MARK_START) + '.*?' + re.escape(MARK_END), '', s, flags=re.S)
    return s2, set(re.findall(r'\bid=["\']([^"\']+)["\']', s2)), set(re.findall(r'<use[^>]+href=["\']#([^"\']+)["\']', s2))

def pick(stem, missing, variants):
    named = [d for d in variants if d == stem or d.endswith('-' + stem)]
    order = named + [d for d in variants if d not in named]
    best = min(order, key=lambda d: (len(missing - set(variants[d][0])), order.index(d)))
    return best

def main(check=False):
    variants = variant_symbols()
    changed, unresolved = [], {}
    for page in sorted(ROOT.glob('*.html')):
        raw = page.read_text(encoding='utf-8')
        raw_ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', raw))
        raw_uses = set(re.findall(r'<use[^>]+href=["\']#([^"\']+)["\']', raw))
        if not (raw_uses - raw_ids):
            continue
        s, ids, uses = page_ids(raw)
        missing = uses - ids
        src = pick(page.stem, missing, variants)
        syms, extras = variants[src]
        found = [syms[i] for i in sorted(missing) if i in syms]
        still = sorted(i for i in missing if i not in syms)
        # second pass: fill any remainder from any variant
        for i in list(still):
            for d, (sy, _) in variants.items():
                if i in sy:
                    found.append(sy[i]); still.remove(i); break
        refs = set(re.findall(r'url\(#([^)]+)\)', ''.join(found)))
        defs = [extras[r] for r in sorted(refs) if r in extras and r not in ids]
        if still:
            unresolved[page.name] = still
        sprite = (MARK_START + '<svg aria-hidden="true" focusable="false" width="0" height="0" '
                  'style="position:absolute;width:0;height:0;overflow:hidden" xmlns="http://www.w3.org/2000/svg">'
                  '<defs>' + ''.join(defs) + ''.join(found) + '</defs></svg>' + MARK_END)
        body = re.search(r'<body\b[^>]*>', s)
        if body is None:
            unresolved[page.name] = ['no <body>']
            continue
        new = s[:body.end()] + sprite + s[body.end():]
        changed.append((page.name, src, len(found)))
        if not check:
            page.write_text(new, encoding='utf-8')
    for c in changed:
        print('restored %-30s from %-32s symbols=%d' % c)
    print('pages changed:', len(changed), '| unresolved:', unresolved or 'none')
    return 1 if (check and changed) or unresolved else 0

if __name__ == '__main__':
    sys.exit(main('--check' in sys.argv))
