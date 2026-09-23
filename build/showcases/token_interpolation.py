"""Token Interpolation, in full: Philipp Otto Runge's Farben-Kugel (1810) and an interface whose every colour is one
number. Runge's sphere has the geometry of OKLCH: lightness is the axis between his white and black poles, hue the
angle round the equator, chroma the distance out from the grey core. Each token here is a point on it, with its own
lightness and chroma; they share one angle, and the scroll turns it through the whole circle.

The stage is pinned inside a tall runway whose view timeline animates a registered angle, --turn; every token is
oklch(L C calc(18.17deg + var(--turn))). The lightnesses and chromas are chosen inside what sRGB can show at every
hue (the accent's 0.118 is the most a mid-tone can have at the cyan, where sRGB is narrowest), so nothing is clipped
out of step, and the contrasts hold all the way round (ink on ground 13.45 to 13.78:1). The start, 18.17°, is the
hue of Runge's own red, measured on the plate. A needle on his section through the equator points, at every step,
at the ink he printed at the palette's hue: his twelve sectors measured in OKLCH (palette.py ring), the needle's
keyframes placed at their hues. Between his green (142°) and his blue (217°) there is no cyan on the plate, and the
needle slows across that step.
"""
import html, json
from pathlib import Path

TITLE = 'One angle, every colour'
LEDE = ('Philipp Otto Runge’s colour sphere of 1810 has white at one pole, black at the other and the pure colours '
        'round its equator: lightness, hue and chroma. Every colour of the interface beside it is a point on that '
        'sphere, and all of them share one angle. Scroll, and it turns.')

# Runge's section through the equator: its centre, the band sampled (the broad second ring, where his inks are
# purest and even), twelve sectors, the first centred 15° below 3 o'clock
R = .2093
RING = dict(label='Farbenkugel', centre=(.2546, .7759), radii=(R * .78, R * .96), sectors=12, first=15)
START = 18.17                     # the hue of Runge's red (sector 8 of the ring, measured)
# the tokens: name, lightness, chroma, and a turn of their own (the complement sits half way round)
TOKENS = [('ground', .965, .016, 0), ('surface', .925, .03, 0), ('rule', .85, .045, 0), ('soft ink', .47, .075, 0),
          ('ink', .27, .045, 0), ('accent', .72, .118, 0), ('complement', .72, .118, 180)]
SOURCES = [('https://en.wikipedia.org/wiki/Philipp_Otto_Runge', 'Philipp Otto Runge'),
           ('https://en.wikipedia.org/wiki/Oklab_color_space', 'Oklab color space')]


def _needle():
    """The needle's keyframes: at each of Runge's sectors, the turn at which the palette reaches its hue, and the
    sector's angle on the plate (clockwise from 3 o'clock)."""
    ring = json.load(open(Path(__file__).resolve().parents[2] / 'assets/palettes.json', encoding='utf-8'))['ring:Farbenkugel']
    n = len(ring)
    pts = sorted(((s['h'] - START) % 360, RING['first'] - k * 360 / n) for k, s in enumerate(ring))
    # the plate's order: the angle falls by one sector per step; keep it falling through the wrap
    angles = [pts[0][1]]
    for _, a in pts[1:]:
        while a > angles[-1]:
            a -= 360
        angles.append(a)
    frames = [f'{t / 360:.2%}{{rotate:{a:.1f}deg}}' for (t, _), a in zip(pts, angles)]
    frames.append(f'100%{{rotate:{angles[0] - 360:.1f}deg}}')
    return '@keyframes needle{' + ''.join(frames) + '}'


HEAD = f'<style>{_needle()}</style>\n'

HOW = """@property --turn { syntax: '<angle>'; inherits: true; initial-value: 0deg }
.frame { animation: turn linear both; animation-timeline: --dial;    /* the scroll turns one number */
         --h: calc(18.17deg + var(--turn));
         --ground: oklch(.965 .016 var(--h));  --ink: oklch(.27 .045 var(--h));  --accent: oklch(.72 .118 var(--h)) }
@keyframes turn { to { --turn: 360deg } }"""

NOTE = ('Each token keeps its own lightness and chroma and only the angle is shared, so what makes a palette work (dark '
        'ink on a pale ground, the accent between them) holds at every hue: ink on ground stays between 13.45 and '
        '13.78 to 1 all the way round, soft ink never below 5.96. The lightnesses and chromas are chosen inside what a '
        'screen can show at every hue, the accent’s 0.118 being the most a mid-tone can have at the cyan, where sRGB '
        'is narrowest, so no colour is clipped out of step on the way. Runge’s sphere has the same three measures, and '
        'the needle points at the ink he printed at the palette’s hue, his twelve sectors measured on the plate. His '
        'circle has no cyan: between his green and his blue the needle slows across a fifth of the circle.')

MATERIAL = ('Material — Philipp Otto Runge, <i>Farben-Kugel</i>, Hamburg, 1810 · public domain')


def render(works):
    w = next(w for w in works if w['kind'] == 'runge')
    cx, cy = RING['centre']
    toks = ''.join(
        f'<div style="--c:var(--t{k})"><dt>{html.escape(n)}</dt>'
        f'<dd>oklch({L:g} {C:g} <b class="h{" far" if turn else ""}"></b>)</dd></div>'
        for k, (n, L, C, turn) in enumerate(TOKENS))
    return (
        '<section class="sphere stage" data-material aria-label="Runge’s colour sphere beside an interface whose colours '
        'all turn on one angle">\n'
        '<div class="runway">\n<div class="frame">\n'
        f'  <figure class="plate" style="--cx:{cx};--cy:{cy};--r:{R * .98:.4f};--ar:{w["w"] / w["h"]:.4f}">'
        f'<span class="face"><img src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 48vw, min(40vw, 70svh)" '
        f'width="{w["w"]}" height="{w["h"]}" alt="Runge’s plate: the colour sphere seen from its white pole and from its '
        'black pole, and cut through the equator and through both poles" decoding="async">'
        '<span class="needle" aria-hidden="true"></span></span>'
        '<figcaption>Farben-Kugel · the sphere from its white pole and its black pole, and cut through the equator and '
        'through both poles</figcaption></figure>\n'
        '  <article class="card">\n'
        '    <p class="eyebrow">Philipp Otto Runge · Hamburg, 1810</p>\n'
        '    <h3>Farben-Kugel</h3>\n'
        '    <p class="sub">The colour sphere: white at one pole, black at the other, the pure colours round its '
        'equator, and every mixture in between.</p>\n'
        f'    <p class="actions"><a class="act" href="{w["descurl"]}">See the plate</a>'
        f'<a class="act ghost" href="{SOURCES[0][0]}">Read about Runge</a></p>\n'
        '    <ul class="chips"><li>lightness, the axis</li><li>hue, the angle</li><li>chroma, the distance out</li></ul>\n'
        '    <p class="series" aria-hidden="true"><i></i><i></i><i></i><i></i></p>\n'
        '    <p class="dial"><span class="deg" aria-hidden="true"></span><span>the angle every colour here shares</span></p>\n'
        '  </article>\n'
        f'  <dl class="tokens">{toks}</dl>\n'
        '</div>\n</div>\n</section>')


def credit(works):
    w = next(w for w in works if w['kind'] == 'runge')
    return (f'Plate — Philipp Otto Runge, <a href="{w["descurl"]}">Farben-Kugel</a>, Hamburg, 1810, public domain, via '
            'Wikimedia Commons; its twelve equatorial inks measured in OKLCH from the scan. Facts — '
            + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
