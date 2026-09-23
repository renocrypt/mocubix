"""Progressive Blur, in full: six photochroms of the 1890s, each as wide as the screen, with its caption set on the
picture itself. Towards the caption's edge the picture softens through six layers of backdrop blur, each twice the
one before and masked to its own band, so the words have something quiet to stand on and the picture is still there
under them. Every print carries a switch to compare it with what it replaces: a black bar, or nothing.

The softening goes where each picture is quiet: over the ice, the water, the quay, the parapet, the granite; over the
sky for the Sami family, whose children fill the bottom of the print. How far it reaches is chosen per picture to
stop short of its subject, and the caption's ink is the one that corner needs (its lightness measured on the print).
Photochroms were made from one black-and-white negative and the photographer's notes on the colours, printed from ten
to fifteen lithographic stones; where a scan includes its mount or the Library's colour target, the picture is cropped
to itself with object-view-box.
"""
import html

TITLE = 'Captions that stand on the picture'
GLOSS = ('The picture softens towards its edge, so the caption sits on something readable without a black bar laid '
         'across it.')
LEDE = ('Six photochroms, the colour views of the 1890s, printed from one black-and-white negative and ten to fifteen '
        'lithographic stones. Each caption stands on its own picture, which softens where it is quiet. Switch any of '
        'them to a black bar to see the difference.')

# label in assets/curated.json; title, place and date; the part of the scan shown (top, right, bottom, left);
# the quiet edge and how much of the picture the softening covers; the caption's side and ink; where a phone's tall
# crop is held (x); the picture described
PICTURES = [
    dict(label='Amalfi', title='Amalfi, from the Capuchins', place='Italy', date='1890–1900', crop=(.14, .10, .15, .12),
         edge='bottom', reach=.38, side='right', ink='light', x='44%',
         alt='A woman in white sits on the parapet of a vine-covered terrace above the town of Amalfi and the sea'),
    dict(label='Algiers', title='The Admiralty', place='Algiers', date='about 1899', crop=(.02, .02, .03, .025),
         edge='bottom', reach=.30, side='right', ink='dark', x='40%',
         alt='The arcades and wooden balconies of the Admiralty on the quay at Algiers, a sailing boat and figures in white'),
    dict(label='Mer de Glace', title='The Mer de Glace', place='Chamonix, Mont Blanc', date='1890–1900', crop=None,
         edge='bottom', reach=.42, side='left', ink='dark', x='56%',
         alt='Three climbers on the crevassed ice of the Mer de Glace beneath dark peaks'),
    dict(label='Stockholm', title='The Exposition of 1897', place='Stockholm', date='1897', crop=None,
         edge='bottom', reach=.36, side='left', ink='light', x='58%',
         alt='The domed hall of the General Art and Industrial Exposition behind a bridge over the water'),
    dict(label='Sami', title='A Sami family', place='Nordland, Norway', date='about 1896', crop=None,
         edge='top', reach=.34, side='left', ink='dark', x='46%',
         alt='A Sami family before their tents: two women, a man with a pipe, four children and a dog'),
    dict(label='Silver Apron', title='The Silver Apron', place='Yosemite Valley', date='1898', crop=(.014, .016, .022, .016),
         edge='bottom', reach=.34, side='right', ink='light', x='60%',
         alt='The Merced River pouring over the Silver Apron in white water across a slab of granite, pines behind'),
]
BLURS = [1, 2, 4, 8, 16, 32]
UNDER = [('blur', 'progressive blur'), ('bar', 'a black bar'), ('none', 'nothing')]
SOURCES = [('https://en.wikipedia.org/wiki/Photochrom', 'Photochrom'),
           ('https://www.loc.gov/pictures/collection/pgz/', 'the Library of Congress Photochrom Print Collection')]

HOW = """.veil i { backdrop-filter: blur(var(--b));            /* 1, 2, 4, 8, 16, 32px: each twice the last */
          mask: linear-gradient(transparent calc(var(--k) * 12.5%), #000 calc((var(--k) + 1) * 12.5%),
                                #000 calc((var(--k) + 2) * 12.5%), transparent calc((var(--k) + 3) * 12.5%)) }
/* each layer blurs its own band and overlaps the next, so the softening has no edges */"""

NOTE = ('A single blurred layer under a gradient mask looks wrong: its blur is the same everywhere and only fades, so '
        'the picture seems to sit behind frosted glass. Stacking layers, each twice as blurred as the one before and '
        'masked to its own band, makes the blur itself grow towards the edge. Where it goes is the real decision: on '
        'the quiet part of each picture, stopping short of its subject. For the Sami family that is the sky.')

MATERIAL = ('Material — photochroms by Photoglob Zürich and the Detroit Publishing Company, 1890s · '
            'Library of Congress · public domain')


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'photochrom'}
    veil = ''.join(f'<i style="--k:{k};--b:{b}px"></i>' for k, b in enumerate(BLURS))
    switch = ''.join(f'<label for="under-{k}">{name}</label>' for k, name in UNDER)
    panels = []
    for i, p in enumerate(PICTURES):
        w = by[p['label']]
        t, r, b, l = p['crop'] or (0, 0, 0, 0)
        cw, ch = w['w'] * (1 - l - r), w['h'] * (1 - t - b)
        view = f' style="object-view-box:inset({t:.1%} {r:.1%} {b:.1%} {l:.1%})"' if p['crop'] else ''
        panels.append(
            f'<figure class="print {p["edge"]} {p["side"]} {p["ink"]}" style="--ar:{cw / ch:.4f};--x:{p["x"]};--reach:{p["reach"]:.0%}" '
            f'aria-labelledby="print{i}">\n'
            f'  <img src="{w["default"]}" srcset="{w["srcset"]}" sizes="{100 / (1 - l - r):.0f}vw" width="{round(cw)}" '
            f'height="{round(ch)}"{view} '
            f'alt="{html.escape("Photochrom: " + p["alt"], quote=True)}" decoding="async"'
            f'{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}>\n'
            f'  <div class="veil" aria-hidden="true">{veil}</div><div class="bar" aria-hidden="true"></div>\n'
            f'  <figcaption><span class="no">{i + 1:02d} / {len(PICTURES):02d}</span><b id="print{i}">{html.escape(p["title"])}</b>'
            f'<span class="where">{html.escape(p["place"])} · {p["date"]}</span></figcaption>\n'
            f'  <p class="switch" aria-hidden="true">{switch}</p>\n'
            f'</figure>')
    radios = ''.join(f'<input type="radio" name="under" id="under-{k}" aria-label="{name}"{" checked" if k == "blur" else ""}>'
                     for k, name in UNDER)
    return ('<section class="photochroms stage" data-material aria-label="Six photochroms, each captioned on its own picture">\n'
            f'<fieldset class="under"><legend>Under each caption</legend>{radios}</fieldset>\n'
            + '\n'.join(panels) + '\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'photochrom'}
    links = ', '.join(f'<a href="{by[p["label"]]["descurl"]}">{html.escape(p["title"])}</a>' for p in PICTURES)
    return ('Photochroms — Photoglob Zürich and the Detroit Publishing Company, 1890s; Library of Congress, Prints and '
            f'Photographs Division, Photochrom Print Collection; public domain, via Wikimedia Commons: {links}. Amalfi, '
            'Algiers and the Silver Apron are cropped to the picture, without the scan’s mount and colour target. Facts — '
            + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
