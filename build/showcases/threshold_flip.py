"""Threshold Flip, in full: six of Monet's Rouen Cathedral paintings, one façade in
six lights. As each canvas reaches the middle of the screen, the whole stage takes
its colours at once: ground, ink and accent, each taken from that canvas by
build/palette.py (assets/palettes.json).

A few lines of script watch which canvas is at eye level and name it on the stage;
the stylesheet holds one palette per canvas and a short transition between them.
"""
import html, json
from pathlib import Path

TITLE = 'One façade, six lights'
GLOSS = ('At one point on the way down, the whole stage changes its colours at once rather than easing between them: '
         'each painting brings its own.')
LEDE = ('Monet painted the west front of Rouen Cathedral more than thirty times, in 1892 and 1893, from rooms across the '
        'street, and reworked the canvases in his studio in 1894. Scroll: as each of these six reaches the middle of the '
        'screen, the page takes its colours, all at once.')

# label in assets/curated.json (Monet's own words for the light), the English title as the museum gives it, year, where it is
PAINTINGS = [
    ('Brouillard', 'The Cathedral in the Fog', '1893–94', 'private collection'),
    ('Effet du matin', 'Rouen Cathedral Façade and Tour d’Albane (Morning Effect)', '1894', 'Museum of Fine Arts, Boston'),
    ('Au soleil', 'Rouen Cathedral, West Façade, Sunlight', '1894', 'National Gallery of Art, Washington'),
    ('Midi', 'Rouen Cathedral at Noon', '1894', 'Pushkin Museum, Moscow'),
    ('Temps gris', 'The Portal, Grey Weather', '1892', 'Musée d’Orsay, Paris'),
    ('Fin de journée', 'Rouen Cathedral in the Evening', '1894', 'Pushkin Museum, Moscow'),
]
SOURCE = ('https://en.wikipedia.org/wiki/Rouen_Cathedral_(Monet_series)', 'Rouen Cathedral (Monet series)')


def _palettes():
    path = Path(__file__).resolve().parents[2] / 'assets/palettes.json'
    return json.load(open(path, encoding='utf-8')) if path.exists() else {}   # build/palette.py writes it from PAINTINGS


def _key(i):
    return f'l{i}'


# one palette per canvas, written from assets/palettes.json so the colours live in one place
HEAD = ('<style>' + ''.join(
    f'.rouen[data-light="{_key(i)}"]{{--ground:{p["ground"]};--ink:{p["ink"]};--mid:{p["mid"]};--accent:{p["accent"]}}}'
    for i, p in enumerate(_palettes().get(label) for label, *_ in PAINTINGS) if p) + '</style>\n')

HOW = """new IntersectionObserver(fn, { rootMargin: '-45% 0px -45% 0px' })
  /* the canvas crossing eye level names itself: stage.dataset.light = … */
.rouen[data-light="l3"] { --ground: …; --ink: …; --accent: … }   /* from the canvas */
.rouen { background: var(--ground); transition: background-color .7s }"""

NOTE = ('These six palettes are not a rotation of one another — fog, blue morning, full sun, ochre noon, grey weather and '
        'evening have nothing in common but the stone — so they are written out, one per canvas, and the stage jumps '
        'between them. Each was taken from its painting in OKLab: its most common colour as the ground, moved out of the '
        'middle band where no type reads, and its most colourful as the accent.')

MATERIAL = 'Material — Claude Monet, the Rouen Cathedral series, 1892–94 · public domain'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'monet'}
    rooms = []
    for i, (label, title, year, where) in enumerate(PAINTINGS):
        w = by[label]
        rooms.append(
            f'<figure class="canvas" data-light="{_key(i)}">\n'
            f'  <img src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 70vw, min(52svh, 520px)" '
            f'width="{w["w"]}" height="{w["h"]}" alt="{html.escape(f"Claude Monet, {title}, {year}", quote=True)}" decoding="async"'
            f'{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}>\n'
            f'  <figcaption><b lang="fr">{html.escape(label)}</b><span class="t">{html.escape(title)}</span>'
            f'<span class="w">{year} · {html.escape(where)}</span></figcaption>\n'
            f'</figure>')
    return ('<section class="rouen stage" data-material data-light="l0" aria-label="Six paintings of Rouen Cathedral; the stage takes each one’s colours">\n'
            + '\n'.join(rooms) + '\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'monet'}
    links = ', '.join(f'<a href="{by[p[0]]["descurl"]}">{html.escape(p[1])}</a> ({html.escape(p[3])})' for p in PAINTINGS)
    return (f'Paintings — Claude Monet, public domain, via Wikimedia Commons: {links}. '
            f'Facts — <a href="{SOURCE[0]}">{SOURCE[1]}</a>. The palettes are taken from the paintings by build/palette.py.')
