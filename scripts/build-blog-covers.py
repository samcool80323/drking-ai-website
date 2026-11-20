#!/usr/bin/env python3
"""Generate DrKing Journal cover images (1200x675) for blog index cards and og:image.

Usage: uv run --no-project --with playwright python scripts/build-blog-covers.py [slug ...]
       (no args = every slug in blog-content/ that has no cover yet)

Reads title/category/reading time from blog-content/<slug>.json, renders the site's
visual language (paper background, organic blobs, serif headline with teal <em>,
DrKing brand mark), saves assets/covers/<slug>.png.
"""
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / 'blog-content'
COVERS = ROOT / 'assets' / 'covers'
PORT = 8781
CHROME = '/app/data/.agent-browser/browsers/chrome-157.0.8103.78/chrome'

TEMPLATE = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
<style>
@font-face {{ font-family: Geomanist; src: url('/fonts/geomanist-regular.woff2') format('woff2'); font-weight: 400; }}
* {{ margin: 0; box-sizing: border-box; }}
.stage {{ position: relative; width: 1200px; height: 675px; background: #F7F5F2; overflow: hidden;
         font-family: Geomanist, sans-serif; color: #1C1814; }}
.blob-a {{ position: absolute; top: -180px; right: -170px; width: 640px; height: 640px; }}
.blob-b {{ position: absolute; bottom: -220px; left: -160px; width: 520px; height: 520px; opacity: .55; }}
.brand {{ position: absolute; top: 44px; left: 64px; display: flex; align-items: center; gap: 12px; }}
.brand img {{ height: 30px; width: auto; }}
.foot {{ position: absolute; bottom: 44px; left: 64px; font-size: 15px; color: #5f5c55; letter-spacing: .02em; }}
.copy {{ position: absolute; top: 172px; left: 64px; width: 820px; }}
.eyebrow {{ font-weight: 400; font-size: 15px; letter-spacing: .16em; text-transform: uppercase; color: #C8553D; margin-bottom: 20px; }}
h1 {{ font-family: Newsreader, Georgia, serif; font-weight: 400; font-size: 50px; line-height: 1.14; letter-spacing: -.02em; }}
h1 em {{ color: #0D5C5C; }}
.motif {{ position: absolute; right: 64px; bottom: 56px; width: 300px; }}
.chat {{ background: #fff; border-radius: 18px; padding: 16px 18px; box-shadow: 0 2px 4px rgba(28,24,20,.04), 0 12px 24px rgba(28,24,20,.06); font-size: 14.5px; line-height: 1.45; }}
.chat .who {{ font-size: 12px; color: #5f5c55; margin-bottom: 6px; letter-spacing: .06em; text-transform: uppercase; }}
.reply {{ margin-top: 10px; background: #0D5C5C; color: #fff; border-radius: 14px 14px 14px 4px; padding: 10px 14px; font-size: 13.5px; width: fit-content; }}
.pill {{ margin-top: 12px; background: #3d7a52; color: #fff; border-radius: 999px; padding: 8px 14px; font-size: 12.5px; width: fit-content; }}
</style></head><body>
<div class="stage">
  <svg class="blob-a" viewBox="0 0 480 480" preserveAspectRatio="none"><path fill="#DDE7D8" d="M247 14C344-4 443 64 455 163c12 94-20 226-110 268-90 43-228 32-292-37C-9 324 0 198 43 122S153 31 247 14Z"/></svg>
  <svg class="blob-b" viewBox="0 0 480 480" preserveAspectRatio="none"><path fill="#0D5C5C" opacity=".07" d="M247 14C344-4 443 64 455 163c12 94-20 226-110 268-90 43-228 32-292-37C-9 324 0 198 43 122S153 31 247 14Z"/></svg>
  <div class="brand"><img src="/drking-logo.svg" alt="DrKing"></div>
  <div class="copy"><div class="eyebrow">{eyebrow}</div><h1>{title}</h1></div>
  <div class="motif"><div class="chat"><div class="who">{chat_who}</div>{chat_line}<div class="reply">{reply}</div><div class="pill">{pill}</div></div></div>
  <div class="foot">drking.ai · DrKing Journal</div>
</div></body></html>'''


def load(slug):
    a = json.loads((CONTENT / f'{slug}.json').read_text())
    cat = a.get('category') or 'Practice growth'
    return {
        'eyebrow': html.escape(f"{cat} · {a['reading_minutes']} min read"),
        'title': a['h1'],
        'chat_who': 'Your practice, with DrKing',
        'chat_line': html.escape((a.get('hero') or {}).get('bubble', 'Thanks for calling! I can book you in for Thursday 10am.')[:110]),
        'reply': 'Thursday 10am works — see you then.',
        'pill': (a.get('hero') or {}).get('pill', 'Appointment confirmed'),
    }


def main():
    from playwright.sync_api import sync_playwright
    import http.server, socketserver, os

    slugs = sys.argv[1:] or sorted(p.stem for p in CONTENT.glob('*.json')
                                   if not (COVERS / f'{p.stem}.png').exists())
    COVERS.mkdir(parents=True, exist_ok=True)

    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('127.0.0.1', PORT), H) as srv:
        import threading
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=CHROME)
            page = browser.new_page(viewport={'width': 1200, 'height': 675})
            for slug in slugs:
                page.set_content('''<base href="http://127.0.0.1:%d/">''' % PORT)
                page.goto(f'http://127.0.0.1:{PORT}/')
                page.set_content(TEMPLATE.format(**load(slug)), wait_until='networkidle')
                page.wait_for_timeout(600)  # let Google Fonts settle
                out = COVERS / f'{slug}.png'
                page.screenshot(path=str(out))
                print('wrote', out)
            browser.close()


if __name__ == '__main__':
    main()
