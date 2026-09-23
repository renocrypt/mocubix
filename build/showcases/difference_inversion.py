"""Difference Inversion, in full: one line of white type held in the middle of the
screen while four of Ansel Adams's photographs for the Department of the Interior
pass beneath it, then the eleven zones of his Zone System, black to white. The
line turns into the opposite of every tone it crosses, and vanishes on one.

The zones are lab() greys, even steps of lightness; Zone V is L* 50, middle grey.
"""
import html

TITLE = 'Every tone but one'
LEDE = ('Four of Ansel Adams’s photographs of the national parks, 1941–42, then the eleven zones of the Zone System he '
        'worked out with Fred Archer around 1939–40, from pure black to pure white. The line in the middle is white '
        'and set to <i>difference</i>: watch what happens to it on Zone V.')

# label in assets/curated.json, the National Archives' caption, year, identifier, a line of our own
PRINTS = [
    ('Tetons', 'The Tetons — Snake River, Grand Teton National Park, Wyoming', '1942', '79-AA-G01',
     'A copy travels on the Voyager Golden Record, launched in 1977.'),
    ('Old Faithful', 'Old Faithful Geyser, Yellowstone National Park, Wyoming', '1941', '79-AA-T26',
     'Taken at dusk or dawn, during an eruption.'),
    ('Yellowstone Lake', 'Yellowstone Lake, Yellowstone National Park, Wyoming', '1941', '79-AA-T06', ''),
    ('Giant Dome', 'The Giant Dome, Hall of Giants, Big Room, Carlsbad Caverns National Park, New Mexico', '1941', '79-AA-W06',
     'The largest stalagmite then found: sixteen feet across.'),
]
ZONES = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
ZONE_WORDS = {0: 'pure black', 5: 'middle grey: what a light meter makes of anything it reads', 10: 'pure white'}
SOURCES = [('https://en.wikipedia.org/wiki/Zone_System', 'Zone System'),
           ('https://science.nasa.gov/mission/voyager/golden-record-contents/images/', 'NASA, the Golden Record’s images')]

HOW = """.line { position: sticky; top: 50%; color: #fff;
        mix-blend-mode: difference }        /* each pixel: |white − what is behind| */
.zone { background: lab(calc(var(--z) * 10%) 0 0) }   /* Zone V = L* 50 */
.walk { isolation: isolate }                 /* what the line may blend with */"""

NOTE = ('White set to <code>difference</code> becomes, pixel by pixel, the opposite of what lies beneath: black over '
        'white, white over black, a new tone over every picture. Over middle grey the opposite of the tone is nearly '
        'the tone itself, so the line all but disappears — the one place to keep it away from.')

MATERIAL = 'Material — Ansel Adams, photographs of the national parks for the Department of the Interior, 1941–42 · public domain'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'adams'}
    prints = []
    for i, (label, caption, year, ident, line) in enumerate(PRINTS):
        w = by[label]
        tall = ' tall' if w['h'] > w['w'] else ''
        prints.append(
            f'<figure class="print{tall}">\n'
            f'  <img src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 92vw, {"62svh" if tall else "108svh"}" '
            f'width="{w["w"]}" height="{w["h"]}" style="--ar:{w["w"] / w["h"]:.4f}" '
            f'alt="{html.escape(f"Ansel Adams, {caption}, {year}", quote=True)}" '
            f'decoding="async"{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}>\n'
            f'  <figcaption><span>{html.escape(caption)}</span><span>Ansel Adams, {year} · National Archives {ident}</span>'
            + (f'<span class="aside">{html.escape(line)}</span>' if line else '') + '</figcaption>\n'
            f'</figure>')
    zones = ''.join(f'<li class="zone" style="--z:{n}"><b>{z}</b>'
                    + (f'<span>{ZONE_WORDS[n]}</span>' if n in ZONE_WORDS else '') + '</li>'
                    for n, z in enumerate(ZONES))
    return ('<section class="walk stage" data-material aria-label="A line of white type over Ansel Adams’s photographs and the eleven zones">\n'
            '<p class="line" aria-hidden="true">Every tone but one</p>\n'
            + '\n'.join(prints) +
            f'\n<ol class="zones" aria-label="The Zone System, 0 to X">{zones}</ol>\n'
            '</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'adams'}
    links = ', '.join(f'<a href="{by[p[0]]["descurl"]}">{p[3]}</a>' for p in PRINTS)
    return (f'Photographs — Ansel Adams, Photographs of National Parks and Monuments, compiled 1941–42, Records of the '
            f'National Park Service, National Archives, public domain, via Wikimedia Commons: {links}. '
            + 'Facts — ' + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
