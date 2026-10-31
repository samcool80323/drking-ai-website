"""Build favicon.svg / favicon.ico / apple-touch-icon.png from the DrKing logo mark.

Takes the logo's green brand mark (class cls-2), crops it with its real bounding box,
and places it on a rounded paper tile. Rendered with headless Chrome; ICO via Pillow.
Run with: uv run --no-project --with playwright --with pillow python scripts/build-favicon.py
"""
import base64
import re
from io import BytesIO
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
CHROME = '/app/data/.agent-browser/browsers/chrome-151.0.7922.71/chrome'
logo = (ROOT / 'drking-logo.svg').read_text()
paths = re.findall(r'<path class="cls-2" d="([^"]+)"', logo)
assert paths, 'brand mark not found'
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, executable_path=CHROME, args=['--no-sandbox'])
    pg = br.new_page()
    pg.set_content('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2019.86 616.44"><g id="m">'
                   + ''.join(f'<path d="{d}"/>' for d in paths) + '</g></svg>')
    bb = pg.evaluate('(()=>{const b=document.getElementById("m").getBBox();return [b.x,b.y,b.width,b.height]})()')
    x, y, w, h = bb
    side = max(w, h) * 1.45
    cx, cy = x + w / 2, y + h / 2
    vb = f'{cx - side/2:.2f} {cy - side/2:.2f} {side:.2f} {side:.2f}'
    r = side * 0.22
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
           f'<rect x="{cx - side/2:.2f}" y="{cy - side/2:.2f}" width="{side:.2f}" height="{side:.2f}" rx="{r:.2f}" fill="#F7F5F2"/>'
           + ''.join(f'<path fill="#3d7a52" d="{d}"/>' for d in paths) + '</svg>')
    (ROOT / 'favicon.svg').write_text(svg)
    pngs = {}
    for size in (16, 32, 48, 180):
        pg.set_viewport_size({'width': size, 'height': size})
        pg.set_content(f'<html><body style="margin:0;background:transparent">'
                       f'<img src="data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}" width="{size}" height="{size}" style="display:block"></body></html>')
        pg.wait_for_timeout(100)
        pngs[size] = Image.open(BytesIO(pg.screenshot(omit_background=True))).convert('RGBA')
    br.close()
pngs[180].save(ROOT / 'apple-touch-icon.png')
pngs[48].save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
print('bbox', [round(v) for v in bb], '-> favicon.svg, favicon.ico, apple-touch-icon.png')
