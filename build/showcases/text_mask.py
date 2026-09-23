"""Text Mask, in full: four of William Morris's patterns, each seen first through
the letters of its own name. The wallpaper holds still; the letters are windows
onto it. Scroll, and the windows widen towards the thickest stroke of the name,
until the ground dissolves and the whole pattern is there.

The text is real text, filled with its pattern (background-clip: text); the
pattern is fixed to the screen, so it stays put while the letters grow. Where to
grow towards (a point in the thickest stroke near the word's middle, in em from
its centre) and how wide each word is were measured once in Chrome, in Zodiak Black.
"""
import html

TITLE = 'Through the letters'
LEDE = ('Four patterns by William Morris, from 1876 to 1887, each seen first through the letters of its own name. '
        'The pattern holds still; the letters are windows onto it. Scroll, and the windows widen until the whole pattern is there.')

HEAD = '<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f%5B%5D=zodiak@900&display=swap">\n'

# label in assets/curated.json, designed, this piece, where it is, the ground its name stands on, a line about it,
# and the measurements: word width in em, the point to grow towards (em from the word's centre)
PATTERNS = [
    ('Strawberry Thief', 'designed 1883', 'printed 1936', 'Cleveland Museum of Art', '#EEE6D3',
     'The thrushes in the garden at Kelmscott Manor. His daughter May remembered him telling the gardener that no bird '
     'in the garden must be touched.', 8.069, (-0.213, -0.23)),
    ('Honeysuckle', 'registered 1876', 'printed about 1900', 'Cleveland Museum of Art', '#F1E2DA',
     'May Morris called it “the most mysterious and poetic — the very symbol of a garden tangle.”', 8.425, (0.04, -0.04)),
    ('Willow Bough', 'designed 1887', 'wallpaper', 'The Metropolitan Museum of Art', '#1E291C',
     'A wallpaper of willow leaves on their branches, drawn close enough to count.', 4.833, (0.06, -0.213)),
    ('Snakeshead', 'designed 1877', 'printed about 1920', 'Cleveland Museum of Art', '#EDE7D6',
     'The fritillary, a wildflower he remembered from the meadows near Oxford, in a red and black that was in fashion '
     'only briefly.', 7.874, (0.161, -0.092)),
]
SOURCES = [('https://clevelandart.org/art/1937.696', 'Cleveland Museum of Art, Strawberry Thief'),
           ('https://clevelandart.org/art/1937.697', 'Honeysuckle'), ('https://clevelandart.org/art/1937.695', 'Snakeshead')]

HOW = """.word { background: var(--pattern) center / cover fixed;   /* the pattern holds still */
        background-clip: text; color: transparent;
        font-size: calc(var(--f0) * var(--z)) }               /* --z: 1 → 7 on the scroll */"""

NOTE = ('The pattern is fixed to the screen, not to the letters, so as the letters grow they open onto more of the same '
        'wallpaper rather than magnifying it. The last step needs no mask at all: the ground around the letters fades, '
        'and because the pattern behind is the very same fixed picture, the letters simply dissolve into it.')

MATERIAL = 'Material — William Morris’s patterns, 1876–1887, Cleveland Museum of Art and the Met · CC0'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'morris'}
    out = []
    for name, designed, piece, where, ground, line, wem, (dx, dy) in PATTERNS:
        w = by[name]
        big = w['sources'][str(max(map(int, w['sources'])))]
        # past cover by enough that a scan's mount and selvedges never show
        over = 1.12 if name == 'Willow Bough' else 1.24
        style = (f"--pattern:image-set(url('{w['sources']['1920']}') 1x,url('{big}') 2x);--ground:{ground};"
                 f"--ar:{w['w'] / w['h']:.4f};--over:{over};--wem:{wem};--dx:{dx};--dy:{dy}")
        dark = int(ground[1:3], 16) < 0x60
        out.append(
            f'<section class="pat{" dark" if dark else ""}" style="{style}">\n'
            f'  <div class="pin">\n'
            f'    <h2 class="word">{html.escape(name)}</h2>\n'
            f'    <div class="whole" role="img" aria-label="{html.escape(f"{name}, a pattern by William Morris, {designed}", quote=True)}"></div>\n'
            f'    <p class="cap"><b>{html.escape(name)}</b><span class="when">{designed} · {piece} · {html.escape(where)}</span>'
            f'<span class="line">{html.escape(line)}</span></p>\n'
            f'  </div>\n'
            f'</section>')
    return ('<div class="morris stage" data-material>\n' + '\n'.join(out) + '\n</div>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'morris'}
    links = ', '.join(f'<a href="{by[p[0]]["descurl"]}">{html.escape(p[0])}</a>' for p in PATTERNS)
    return (f'Patterns — William Morris, via Wikimedia Commons from the Cleveland Museum of Art and the Metropolitan Museum '
            f'of Art (both CC0): {links}. The lines about them follow the museums’ records.')
