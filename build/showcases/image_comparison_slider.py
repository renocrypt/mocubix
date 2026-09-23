"""Image Comparison Slider, in full: five places in Glacier National Park, each
photographed from the same spot about a century apart.

The later photograph is laid exactly over the earlier one: build/register.py
measures, once, the scale, turn and shift that put its rock edges on the
earlier's, and the crop both fill (assets/registration.json). The divider is a
native range input; showcase.js only hands its value to the picture.
"""
import html, json
from pathlib import Path

TITLE = 'Where the ice was'
LEDE = ('Five views in Glacier National Park, Montana, each photographed from the same spot decades apart. '
        'At the height of the Little Ice Age the park held about 80 glaciers larger than a tenth of a square kilometre; '
        'by 2005 there were 32. Drag across each pair.')

# earlier label, later label (assets/curated.json), place, where it was taken from, who took each (as recorded),
# and where the stable rock is in the earlier picture (a box, as fractions): build/register.py registers on it
PAIRS = [
    ('Grinnell 1910', 'Grinnell 2025', 'Grinnell Glacier', 'from Lower Grinnell Ridge', '', '6 September 2025', (0.1, 0, 1, 0.45)),
    ('Jackson 1914', 'Jackson 2020', 'Jackson Glacier', 'below Mount Jackson', '', '', (0, 0, 1, 0.35)),
    ('Sperry 1907', 'Sperry 2023', 'Sperry Glacier', 'the arm below Mount Edwards', 'Morton J. Elrod', '', (0, 0, 1, 0.5)),
    ('Road 1941', 'Road 2025', 'Jackson Glacier', 'from Going-to-the-Sun Road', 'Marian Post', '25 August 2025', (0, 0, 1, 0.5)),
    ('Boulder 1932', 'Boulder 1988', 'Boulder Glacier', 'the ice cave', 'T. J. Hileman, for the Great Northern Railway', 'Jerry DeSanto, park ranger', (0, 0, 1, 0.3)),
]
SOURCE = ('https://www.usgs.gov/centers/norock/science/status-glaciers-glacier-national-park', 'USGS, Status of glaciers in Glacier National Park')

HOW = """.then { clip-path: inset(0 calc(100% - var(--x) * 1%) 0 0) }  /* the earlier picture, cut at the divider */
.now img { transform: translate(var(--tx), var(--ty)) rotate(var(--rot)) scale(var(--s)) }
/* --s, --rot, --tx, --ty: measured once, so the later picture's rock lies on the earlier's */
input[type=range] → --x                                         /* the divider is a real slider */"""

NOTE = ('The two photographs of each place were taken from the same spot but never framed exactly alike, so the later one is '
        'scaled, turned and shifted until its rock edges sit on the earlier one’s, and both are cropped to the window they '
        'share. The divider is a native range input underneath: drag it, click anywhere, or use the arrow keys.')

MATERIAL = 'Material — Glacier National Park and its archives: repeat photographs, 1907–2025 · public domain'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'glacier'}
    reg = json.load(open(Path(__file__).resolve().parents[2] / 'assets/registration.json'))
    out = []
    for i, (then, now, place, where, then_by, now_by, _) in enumerate(PAIRS):
        a, b, r = by[then], by[now], reg[f'{then}|{now}']
        y0, y1 = then.split()[-1], now.split()[-1]
        x, y, w, h = r['crop']
        style = (f'--ar:{w * a["w"] / (h * a["h"]):.4f};--cx:{x};--cy:{y};--cw:{w};--ch:{h};'
                 f'--s:{r["s"]};--rot:{r["rot"]}deg;--tx:{r["tx"] * 100:.2f}%;--ty:{r["ty"] * 100:.2f}%')

        def img(rec, year):
            return (f'<img src="{rec["default"]}" srcset="{rec["srcset"]}" sizes="(max-width: 760px) 100vw, 86vw" '
                    f'width="{rec["w"]}" height="{rec["h"]}" alt="{html.escape(f"{place} in {year}", quote=True)}" '
                    f'decoding="async"{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}>')
        who = lambda year, by_: f'<span><b>{year}</b>{" · " + html.escape(by_) if by_ else ""}</span>'
        out.append(
            f'<figure class="pair" style="{style}">\n'
            f'  <div class="frame">\n'
            f'    <div class="layer now"><div class="view">{img(b, y1)}</div></div>\n'
            f'    <div class="layer then"><div class="view">{img(a, y0)}</div></div>\n'
            f'    <div class="divider" aria-hidden="true"><i>{y0}</i><i>{y1}</i></div>\n'
            f'    <input type="range" min="0" max="100" value="50" step="0.1" '
            f'aria-label="{html.escape(f"{place}: move between {y0} and {y1}", quote=True)}">\n'
            f'  </div>\n'
            f'  <figcaption><h2>{html.escape(place)}</h2><p class="where">{html.escape(where)}</p>'
            f'<p class="when">{who(y0, then_by)}{who(y1, now_by)}<span class="gap">{int(y1) - int(y0)} years apart</span></p></figcaption>\n'
            f'</figure>')
    return ('<section class="ice stage" data-material aria-label="Five glaciers, then and now">\n'
            + '\n'.join(out) + '\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'glacier'}
    links = ', '.join(f'<a href="{by[l]["descurl"]}">{l}</a>' for p in PAIRS for l in p[:2])
    return (f'Photographs — Glacier National Park’s repeat photography and archives, public domain, via Wikimedia Commons: {links}. '
            f'Glacier counts — <a href="{SOURCE[0]}">{SOURCE[1]}</a>.')
