"""Gamut Arc, in full: Michel Eugène Chevreul's first chromatic circle (1864), seventy-two hues in their
purest ('couleurs franches'), and two ways from one of his colours to its opposite.

Round the outside, the field passes through every sector of his circle between the two, each with its hue and
lightness as measured on the plate (build/palette.py ring, assets/palettes.json) and as much chroma as sRGB can
hold there. Straight across, it takes the line CSS takes unless asked otherwise, and meets grey on the way. The
pairs are opposites in Oklab as well as colours of his circle: measured, his Jaune and Bleu-violet are 182.5°
apart, Vert and Violet 177.6°, Rouge-orangé and Bleu 178.4°. A marker rides each route on the plate.
"""
import html, json, math
from pathlib import Path
import palette                                   # build/ is on the path when the Lexicon is built

TITLE = 'Round the circle, or straight across'
GLOSS = ('Two ways to get from a colour to its opposite. One goes round the outside and is a full colour the whole way; '
         'the other goes straight across and turns to grey on the way.')
LEDE = ('Michel Eugène Chevreul studied dyes as director at the Gobelins tapestry works, and set out his colours as a '
        'circle of seventy-two. Scroll: the left field goes round his circle to the opposite colour, the right goes '
        'straight across, as CSS does unless asked otherwise.')

# the plate's colour circle, measured on the 1920px copy: centre (x of the width, y of the height; fitted to the
# disc's edge against the paper), the coloured band's inner and outer radius (of the width), 72 sectors, Rouge's
# centre at 92.62° (clockwise from three o'clock; the separators fitted to the white lines between sectors)
RING = dict(label='Premier cercle', centre=(0.48823, 0.45404), radii=(0.1375, 0.345), sectors=72, first=92.62)
CROP = 0.381          # the medallion's radius, of the width: the disc (0.374) and a hair of paper
MARK = 0.29           # the radius the markers ride at, of the width: on the sectors, clear of the ring
NAMES = ['Rouge', 'Rouge-orangé', 'Orangé', 'Orangé-jaune', 'Jaune', 'Jaune-vert', 'Vert', 'Vert-bleu', 'Bleu',
         'Bleu-violet', 'Violet', 'Violet-rouge']
# (id, from, to, which way round his circle: +1 as his numbers run, -1 against)
PAIRS = [('jaune', 4, 9, 1), ('vert', 6, 10, 1), ('rouge', 1, 8, -1)]
SOURCES = [('https://en.wikipedia.org/wiki/Michel_Eug%C3%A8ne_Chevreul', 'Michel Eugène Chevreul'),
           ('https://en.wikipedia.org/wiki/Oklab_color_space', 'Oklab')]


def _sectors():
    path = Path(__file__).resolve().parents[2] / 'assets/palettes.json'
    return json.load(open(path, encoding='utf-8')).get(f'ring:{RING["label"]}', []) if path.exists() else []


def _franc(L, h):
    """As much chroma as sRGB holds at this lightness and hue (a hair inside the edge)."""
    lo, hi = 0.0, 0.5
    for _ in range(30):
        c = (lo + hi) / 2
        rgb = palette.srgb(L, c * math.cos(math.radians(h)), c * math.sin(math.radians(h)))
        lo, hi = (c, hi) if all(-1e-6 <= v <= 1 + 1e-6 for v in rgb) else (lo, c)
    return lo - .002


def _route(pair):
    _, a, b, d = pair
    k0, n = 6 * a, ((6 * b - 6 * a) * d) % 72
    return [(k0 + d * j) % 72 for j in range(n + 1)]


def _theta(k):
    return RING['first'] - 360 / RING['sectors'] * k


def _pairs():
    """Each pair's route round his circle, its keyframe stops, its ends (as CSS and as Oklab a, b) and where its
    routes lie on the plate, in medallion radii."""
    sec = _sectors()
    if not sec:
        return []
    out = []
    for pair in PAIRS:
        pid, a, b, d = pair
        route = _route(pair)
        n = len(route) - 1
        col = []
        for k in route:
            s = sec[k]
            c = _franc(s['L'], s['h'])
            col.append((f'oklch({s["L"]:.3f} {c:.3f} {s["h"]:.1f})', c, c * math.cos(math.radians(s['h'])),
                        c * math.sin(math.radians(s['h']))))
        t0, t1 = math.radians(_theta(route[0])), math.radians(_theta(route[-1]))
        m = MARK / CROP
        ax, ay, bx, by = math.cos(t0) * m, math.sin(t0) * m, math.cos(t1) * m, math.sin(t1) * m
        sweep = -d * n * 360 / RING['sectors']                 # screen degrees, clockwise positive
        out.append(dict(id=pid, a=a, b=b, d=d, route=route, n=n, col=col, ax=ax, ay=ay, bx=bx, by=by, sweep=sweep,
                        chord=math.hypot(bx - ax, by - ay), chord_angle=math.degrees(math.atan2(by - ay, bx - ax)),
                        # conic angles start at twelve o'clock: the arc is drawn clockwise from its earlier end
                        arc_from=(min(_theta(route[0]), _theta(route[0]) + sweep) + 90) % 360))
    return out


def _head():
    css = []
    for p in _pairs():
        stops = ''.join(f'{100 * j / p["n"]:.3f}%{{--round:{c[0]};--cr:{c[1]:.4f}}}' for j, c in enumerate(p['col']))
        (ca, _, a1, b1), (cb, _, a2, b2) = p['col'][0], p['col'][-1]
        css.append(
            f'.gamut:has(#pair-{p["id"]}:checked){{--a:{ca};--b:{cb};--a1:{a1:.4f};--b1:{b1:.4f};--a2:{a2:.4f};--b2:{b2:.4f};'
            f'--n:{p["n"]};--na:"{NAMES[p["a"]].lower()}";--nb:"{NAMES[p["b"]].lower()}";'
            f'--th0:{_theta(p["route"][0]):.2f}deg;--sweep:{p["sweep"]:.2f}deg;--span:{abs(p["sweep"]):.2f}deg;'
            f'--flip:{1 if p["d"] == 1 else 0};--arc-from:{p["arc_from"]:.2f}deg;'
            f'--ax:{p["ax"]:.4f};--ay:{p["ay"]:.4f};--bx:{p["bx"]:.4f};--by:{p["by"]:.4f};'
            f'--chord:{p["chord"]:.4f};--chord-angle:{p["chord_angle"]:.2f}deg}}'
            f'.gamut:has(#pair-{p["id"]}:checked) .fields{{animation-name:progress,round-{p["id"]}}}'
            f'.gamut:not(:has(#pair-{p["id"]}:checked)) .names-{p["id"]}{{display:none}}'
            f'@keyframes round-{p["id"]}{{{stops}}}')
    return '<style>' + ''.join(css) + '</style>\n' if css else ''


HEAD = _head()

HOW = """.round    { background: var(--round) }   /* through every sector between, each as strong as sRGB holds */
.straight { background: color-mix(in oklab, var(--a), var(--b) calc(var(--t) * 100%)) }  /* the straight line */
/* with no keyframes at all, color-mix(in oklch, var(--a), var(--b) …) also goes round: it interpolates the hue */"""

NOTE = ('Straight across is what CSS does unless asked otherwise: a transition, an animation or a gradient between two '
        'colours takes the straight line between them, and two opposite colours meet in grey on the way. Round the '
        'outside keeps the colour. How much it can keep depends on the hue: sRGB holds little chroma near cyan and a '
        'great deal towards violet, which is the arc’s own shape, and the meter shows it. On the plate as it survives, '
        'Chevreul’s blues and violets are barely stronger than grey; the fields give each of his hues all the chroma '
        'a screen can.')

MATERIAL = ('Material — Michel Eugène Chevreul, first chromatic circle, engraved by René-Henri Digeon, 1864 · '
            'Science History Institute · public domain')


def render(works):
    w = next(w for w in works if w['kind'] == 'chevreul')
    cx, cy = RING['centre']
    scale = 1 / (2 * CROP)                                # the image's width, in medallion diameters
    ih = scale * w['h'] / w['w']
    radios, names = [], []
    for i, p in enumerate(_pairs()):
        radios.append(f'<input type="radio" name="pair" id="pair-{p["id"]}"{" checked" if i == 0 else ""}>'
                      f'<label for="pair-{p["id"]}" style="--ca:{p["col"][0][0]};--cb:{p["col"][-1][0]}"><i class="dot"></i>'
                      f'<span lang="fr">{NAMES[p["a"]]} <b>↔</b> {NAMES[p["b"]]}</span></label>')
        labels = ''.join(f'<li style="--j:{j}">{NAMES[k // 6]}{f" <small>{k % 6}</small>" if k % 6 else ""}</li>'
                         for j, k in enumerate(p['route']))
        names.append(f'<ol class="names names-{p["id"]}" lang="fr">{labels}</ol>')
    alt = ('Chevreul’s first chromatic circle: seventy-two sectors of colour round a central disc that reads “1er cercle '
           'chromatique de Mr Chevreul renfermant les couleurs franches”, with the names of his colours on the ring')
    return (
        '<section class="gamut stage" data-material aria-label="Two routes across Chevreul’s colour circle">\n'
        '<div class="run">\n'
        '  <div class="fields">\n'
        '    <div class="field round">\n'
        '      <p class="road"><i class="glyph"></i><b>Round the outside</b><span>through every sector of his circle</span></p>\n'
        f'      <div class="now">{"".join(names)}</div>\n'
        '      <p class="meter"><span>chroma</span><b aria-hidden="true"></b><i></i></p>\n'
        '    </div>\n'
        '    <div class="field straight">\n'
        '      <p class="road"><i class="glyph"></i><b>Straight across</b><span>the line CSS takes unless asked otherwise</span></p>\n'
        '      <p class="mix" aria-hidden="true"></p>\n'
        '      <p class="meter"><span>chroma</span><b aria-hidden="true"></b><i></i></p>\n'
        '    </div>\n'
        f'    <figure class="medallion" style="--iw:{scale:.5f};--ih:{ih:.5f};--ix:{0.5 - cx * scale:.5f};--iy:{0.5 - cy * ih:.5f};'
        f'--m:{MARK / CROP:.4f}">\n'
        f'      <img src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 60vw, min(66svh, 50vw)" '
        f'width="{w["w"]}" height="{w["h"]}" alt="{html.escape(alt, quote=True)}" decoding="async" fetchpriority="high">\n'
        '      <i class="arc" aria-hidden="true"></i><i class="chord" aria-hidden="true"></i>\n'
        '      <i class="marker round" aria-hidden="true"></i><i class="marker straight" aria-hidden="true"></i>\n'
        '    </figure>\n'
        f'    <fieldset class="pairs"><legend>From a colour to its opposite</legend>{"".join(radios)}</fieldset>\n'
        '  </div>\n'
        '</div>\n'
        '</section>')


def credit(works):
    w = next(w for w in works if w['kind'] == 'chevreul')
    return (f'Plate — <a href="{w["descurl"]}">Premier cercle chromatique renfermant les couleurs franches</a>, from Michel '
            'Eugène Chevreul’s Des couleurs et de leurs applications aux arts industriels à l’aide des cercles '
            'chromatiques (J.-B. Baillière et fils, Paris, 1864), engraved by René-Henri Digeon; Science History '
            'Institute; public domain, via Wikimedia Commons. The colours of its 72 sectors were measured from the scan. '
            'Facts — ' + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
