"""Ordered Dithering, in full: three photographs taken down to a handful of tones, the missing ones made up out of
the regular grain of the 8×8 Bayer matrix. Nadar's Sarah Bernhardt (1864), a plate of the Moon from Loewy and
Puiseux's photographic atlas for the Paris Observatory (1899), and Apollo 8's Earthrise (1968).

The dither is done in showcase.js on a canvas over the photograph (Wikimedia serves its images to other sites'
canvases). Each pixel takes the tone just below or just above its own, decided by its cell of the matrix, and the
choice is made in linear light, so the grain averages to the photograph's own brightness. The monochrome prints
are dithered between their own darkest ink and lightest paper (measured on each), the Earthrise per channel of
colour, so at two tones it has eight colours. The photograph itself stays in the page as the image.
"""
import html

TITLE = 'Tones, taken away'
GLOSS = ('The picture is cut down to a handful of tones, and the ones that are missing are made up out of a regular '
         'grain. Drag to take more away.')
LEDE = ('Three photographs from three centuries: an actress, the surface of the Moon, and the Earth seen from it. '
        'Drag the slider: the tones go, and a regular grain makes up for them, down to two.')

# label in assets/curated.json, who or what, by whom, when, its ink and paper (the 0.5th and 99th percentiles of
# its own tones; None dithers each channel of colour), the part shown (top, right, bottom, left, in fractions: the
# print without its mount's corners; the Earth and the horizon), the picture described
PICTURES = [
    ('Bernhardt', 'Sarah Bernhardt', 'Nadar', '1864', ('#0B0B0B', '#E5E5E5'), (.06, .02, .03, .02),
     'Sarah Bernhardt at about twenty, in profile, wrapped in a dark velvet cloak, leaning on a column'),
    ('Moon', 'The Moon: Blancanus, Tycho, Schiller', 'Maurice Loewy and Pierre Puiseux, Paris Observatory', '1899',
     ('#322F26', '#F8F4EB'), (0, 0, 0, 0), 'The southern highlands of the Moon at the terminator, Tycho and its neighbouring craters'),
    ('Earthrise', 'Earthrise', 'William Anders, Apollo 8', '24 December 1968', None, (.33, .12, .10, .25),
     'The Earth, half lit, rising above the grey horizon of the Moon'),
]
BAYER = [0, 32, 8, 40, 2, 34, 10, 42, 48, 16, 56, 24, 50, 18, 58, 26, 12, 44, 4, 36, 14, 46, 6, 38, 60, 28, 52, 20, 62,
         30, 54, 22, 3, 35, 11, 43, 1, 33, 9, 41, 51, 19, 59, 27, 49, 17, 57, 25, 15, 47, 7, 39, 13, 45, 5, 37, 63, 31,
         55, 23, 61, 29, 53, 21]
SOURCES = [('https://en.wikipedia.org/wiki/Ordered_dithering', 'Ordered dithering'),
           ('https://en.wikipedia.org/wiki/Earthrise', 'Earthrise'),
           ('https://en.wikipedia.org/wiki/Sarah_Bernhardt', 'Sarah Bernhardt')]

HOW = """const BAYER8 = [0, 32, 8, 40, 2, 34, 10, 42, …];      // 64 thresholds, spread as evenly as they can be
const t = (BAYER8[(y % 8) * 8 + x % 8] + .5) / 64;   // this pixel's threshold
out = f > t ? above : below;  // f: how far the pixel lies from the tone below to the tone above, in linear light"""

NOTE = ('Every cell of the 8×8 matrix holds a threshold, and the 64 are spread so that neighbours differ as much as '
        'they can. A pixel takes the tone above its own when it lies further towards that tone than its cell’s '
        'threshold, and the tone below when it does not, so a grey a third of the way between two tones lights about '
        'a third of every tile. The decision is made in linear light, where light adds up, so the grain averages to '
        'the photograph’s own brightness. The grain never moves with the picture: it is the same regular pattern '
        'everywhere, which is what separates ordered dithering from the scattered kind.')

MATERIAL = ('Material — Nadar, Sarah Bernhardt, 1864; Loewy and Puiseux, Atlas photographique de la Lune, 1899; '
            'William Anders, Earthrise, 1968 · public domain')


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'tones'}
    pics, radios = [], []
    for i, (label, what, who, when, inks, crop, alt) in enumerate(PICTURES):
        w = by[label]
        t, r, b, l = crop
        cw, ch = w['w'] * (1 - l - r), w['h'] * (1 - t - b)          # the part shown, and the whole behind it
        ink = f' data-ink="{inks[0]}" data-paper="{inks[1]}"' if inks else ''
        view = f';object-view-box:inset({t:.0%} {r:.0%} {b:.0%} {l:.0%})' if any(crop) else ''
        grow = 1 / (1 - l - r)
        pics.append(f'<img src="{w["default"]}" srcset="{w["srcset"]}" '
                    f'sizes="(max-width: 760px) {92 * grow:.0f}vw, calc(min(56vw, 80svh) * {grow:.3f})" '
                    f'width="{round(cw)}" height="{round(ch)}" style="--ar:{cw / ch:.4f}{view}" data-crop="{t} {r} {b} {l}" '
                    f'crossorigin="anonymous" '
                    f'data-pic="{label}"{ink} alt="{html.escape(f"{what}, by {who}, {when}: {alt}", quote=True)}" '
                    f'decoding="async"{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\" hidden"}>')
        radios.append(f'<input type="radio" name="picture" id="pic-{label.lower()}" value="{label}"{" checked" if i == 0 else ""}>'
                      f'<label for="pic-{label.lower()}"><img src="{w["sources"]["330"]}" width="{w["w"]}" height="{w["h"]}" '
                      f'style="--ar:{w["w"] / w["h"]:.4f}" alt="" loading="lazy" decoding="async">'
                      f'<span><b>{html.escape(what)}</b><i>{html.escape(who)} · {html.escape(when)}</i></span></label>')
    tile = ''.join(f'<i style="--v:{v}">{v}</i>' for v in BAYER)
    return (
        '<section class="tones stage" data-material aria-label="Three photographs, dithered to a handful of tones">\n'
        '  <figure class="plate">\n'
        f'    {"".join(pics)}\n'
        '    <canvas aria-hidden="true"></canvas>\n'
        '  </figure>\n'
        '  <div class="panel">\n'
        '    <p class="count"><output for="tones">every tone</output><span class="per"></span></p>\n'
        '    <p class="ladder" aria-hidden="true"></p>\n'
        '    <div class="dial"><label for="tones">Tones</label>'
        '<input type="range" id="tones" min="2" max="17" step="1" value="17">'
        '<span class="ends" aria-hidden="true"><span>2</span><span>the photograph</span></span></div>\n'
        '    <fieldset class="grain"><legend>Grain</legend>'
        '<input type="radio" name="grain" id="grain-1" value="1"><label for="grain-1">fine</label>'
        '<input type="radio" name="grain" id="grain-2" value="2" checked><label for="grain-2">coarse</label>'
        '<input type="radio" name="grain" id="grain-4" value="4"><label for="grain-4">coarser</label></fieldset>\n'
        f'    <figure class="matrix"><div class="tile" aria-label="The 8×8 Bayer matrix of thresholds, 0 to 63">{tile}</div>'
        '<figcaption>The 8×8 Bayer matrix: 64 thresholds, repeated across the picture</figcaption></figure>\n'
        f'    <fieldset class="pictures"><legend>Picture</legend>{"".join(radios)}</fieldset>\n'
        '  </div>\n'
        '</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'tones'}
    links = ', '.join(f'<a href="{by[p[0]]["descurl"]}">{html.escape(p[1])}</a> ({html.escape(p[2])}, {p[3]})' for p in PICTURES)
    links += '; Earthrise is shown cropped to the Earth and the horizon'
    return (f'Photographs — public domain, via Wikimedia Commons: {links}. The Moon plate is from the National Gallery '
            'of Art’s open access collection; Earthrise is NASA’s. Facts — '
            + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
