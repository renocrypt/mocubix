"""Kinetic Drag, in full: the Tabula Peutingeriana, the Roman road map that is a
scroll 6.75 metres long, laid out whole in Konrad Miller's facsimile of 1888.
Grab it and throw it: it keeps going, and slows as though it had weight.

The eight sheets of the facsimile overlap; build/register.py (stitch) measures
each seam and places every sheet in the first one's frame, cut at the middle of
each overlap, so the strip runs on without a seam. The map is a native horizontal
scroller, so a trackpad, a finger or the keyboard move it as they always do;
showcase.js adds the grab and the throw for a mouse.
"""
import html, json, math
from pathlib import Path

TITLE = 'Throw the Roman world'
LEDE = ('The Tabula Peutingeriana: every road of the Roman Empire on one parchment scroll, 6.75 metres long and 35 '
        'centimetres high, from the Channel to India. Grab it and throw it. How far it runs, and how it comes to rest, is one number.')

SHEETS = [f'Sheet {i}' for i in range(1, 9)]

# (sheet, x, y at the 1920px copy of that sheet, name, line) — found on the facsimile by eye
PINS = [
    (0, 34, 134, 'Segmentum I', 'The first section, lost “to the injustice of time”'),
    (2, 975, 380, 'Roma', 'Rome, enthroned at the centre of her roads'),
    (4, 1395, 310, 'Constantinopolis', 'The new Rome, on the Bosporus'),
    (6, 850, 425, 'Antiochia', 'Antioch, with the springs of Daphne'),
    (7, 1560, 275, 'Hic Alexander responsum accepit', '“Here Alexander received the answer”: the edge of the known world'),
    (7, 1500, 605, 'Taprobane', 'Sri Lanka'),
]
# the throw: how much of its speed the map keeps each sixtieth of a second
DECAYS = [('0.90', 'stops dead'), ('0.94', 'like an object'), ('0.98', 'slides for ever')]
SOURCE = ('https://en.wikipedia.org/wiki/Tabula_Peutingeriana', 'Tabula Peutingeriana')

HOW = """v *= decay ** (dt / 16.7)        /* each frame keeps a share of its speed */
if (Math.abs(v) < 0.02) stop()
.roads { overflow-x: auto }       /* touch, trackpad, keys: the native scroll */
.sheet { transform: translate(…) rotate(…) scale(…); clip-path: inset(…) }  /* stitched */"""

NOTE = ('Try all three under the map. The strip itself is eight overlapping sheets of the facsimile, each measured against '
        'the next and set in place with a scale, a turn of a fraction of a degree and a cut at the middle of the overlap, '
        'so no town appears twice; where a sheet’s band falls short, the map’s own sea fills in.')

MATERIAL = 'Material — Tabula Peutingeriana, in Konrad Miller’s facsimile of 1888, National Library of Australia · public domain'


def _layout():
    return json.load(open(Path(__file__).resolve().parents[2] / 'assets/registration.json'))['stitch:kinetic_drag']


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'tabula'}
    lay = _layout()
    gx0, gy0, gx1, gy1 = lay['box']
    W, H = gx1 - gx0, gy1 - gy0

    def sheets(sizes, cls):
        out = []
        for k, sh in enumerate(lay['sheets']):
            w = by[sh['label']]
            x0, y0, x1, y1 = sh['clip']
            style = (f'--iw:{sh["w"]};--ih:{sh["h"]};--x:{sh["tx"] - gx0:.1f};--y:{sh["ty"] - gy0:.1f};--r:{sh["rot"]}deg;--s:{sh["s"]};'
                     f'--ct:{y0};--cr:{sh["w"] - x1:.1f};--cb:{sh["h"] - y1:.1f};--cl:{x0}')
            out.append(f'<img class="{cls}" src="{w["sources"]["1920"]}" srcset="{w["srcset"]}" sizes="{sizes}" '
                       f'width="{w["w"]}" height="{w["h"]}" alt="" draggable="false" decoding="async"'
                       f'{" loading=\"lazy\"" if k > 1 else ""} style="{style}">')
        return ''.join(out)

    def to_global(k, x, y):
        sh = lay['sheets'][k]
        th = math.radians(sh['rot'])
        return (sh['s'] * (math.cos(th) * x - math.sin(th) * y) + sh['tx'] - gx0,
                sh['s'] * (math.sin(th) * x + math.cos(th) * y) + sh['ty'] - gy0)

    pins = []
    for k, x, y, name, line in PINS:
        px, py = to_global(k, x, y)
        # labels stay on the map, and off the words they point to
        side = (' low' if py > H * .55 else '') + (' west' if px > W - 900 else '') + (' south' if px < 300 else '')
        pins.append(f'<li class="pin{side}" style="--px:{px:.0f};--py:{py:.0f}"><b lang="la">{html.escape(name)}</b>'
                    f'<span>{html.escape(line)}</span></li>')
    decays = ''.join(f'<input type="radio" name="decay" id="decay-{v[2:]}" value="{v}"{" checked" if v == "0.94" else ""}>'
                     f'<label for="decay-{v[2:]}"><b>{v}</b><span>{html.escape(what)}</span></label>' for v, what in DECAYS)
    return ('<section class="tabula stage" data-material aria-label="The Tabula Peutingeriana, to grab and throw">\n'
            '<p class="cue">Grab the map and throw it — or swipe, or use the arrow keys</p>\n'
            f'<div class="roads" tabindex="0" aria-label="The map, 6.75 metres of it: drag, throw, or use the arrow keys" '
            f'style="--mw:{W:.0f};--mh:{H:.0f};--sea:{lay["ground"]}">\n'
            f'<div class="strip">{sheets(f"(max-width: 760px) {1920 / H * 52:.0f}svh, min({1920 / H * 56:.0f}svh, {1920 / H * 620:.0f}px)", "sheet")}\n'
            f'<ol class="pins">{"".join(pins)}</ol></div>\n</div>\n'
            '<div class="under">\n'
            f'<fieldset class="decay"><legend>Each frame the map keeps</legend>{decays}</fieldset>\n'
            f'<div class="mini" aria-hidden="true" style="--mw:{W:.0f};--mh:{H:.0f};--sea:{lay["ground"]}"><div class="strip">{sheets("330px", "sheet")}</div><i class="window"></i></div>\n'
            '</div>\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'tabula'}
    links = ', '.join(f'<a href="{by[l]["descurl"]}">{l.lower()}</a>' for l in SHEETS)
    return ('Map — the Tabula Peutingeriana (the surviving copy, about 1200, Austrian National Library), in Konrad Miller’s '
            f'facsimile of 1888, from the National Library of Australia, public domain, via Wikimedia Commons: {links}. '
            f'Facts — <a href="{SOURCE[0]}">{SOURCE[1]}</a>.')
