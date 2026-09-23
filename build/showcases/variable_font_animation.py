"""Variable Font Animation, in full: William Caslon's specimen sheet of 1734, where every size of type
is a separate font of metal known by a name, faced by one variable font.

A loupe travels down the sheet at the same scale as the live type, stepping from one of Caslon's sizes
to the next (French Cannon down to Pearl); beside it one line of Cicero, set in a single file, glides
through every size in between as you scroll, its optical size following its size. Its weight is a
dial. The sizes are the sheet's own, measured from its scan: each block's line period, by
autocorrelation of its rows (Pica 31.8px, so about 2.65px to the point at this scan).
"""
import html, math

TITLE = 'Twelve sizes, one file'
GLOSS = ('Weight is a dial here, not a set of steps. Drag it, and the letters thicken without ever swapping to another file.')
LEDE = ('William Caslon’s specimen sheet of 1734, where every size of type is a separate font of metal, known by a '
        'name. Scroll down the sheet: beside it, one variable font runs through every size in between. Then drag the '
        'dial.')

# Caslon's name for each size (as the sheet spells it), its line period on the 2898px scan, and its block on
# the sheet (x0, y0, x1, y1), largest first
SIZES = [
    ('French Cannon', 126.7, (20, 1320, 745, 2100)),
    ('Two Lines Great Primer', 89.6, (20, 2195, 745, 2935)),
    ('Two Lines English', 73.4, (20, 3010, 745, 3575)),
    ('Double Pica', 55.1, (755, 540, 1450, 872)),
    ('Great Primer', 44.8, (755, 890, 1450, 1258)),
    ('English', 35.1, (755, 1280, 1450, 1575)),
    ('Pica', 31.8, (755, 1592, 1450, 1885)),
    ('Small Pica', 27.7, (755, 1890, 1450, 2152)),
    ('Long Primer', 25.3, (755, 2440, 1450, 2705)),
    ('Brevier', 21.0, (755, 2995, 1450, 3205)),
    ('Nonpareil', 15.0, (755, 3228, 1450, 3428)),
    ('Pearl', 12.8, (755, 3445, 1085, 3598)),
]
WEIGHTS = [(200, 'Extra Light'), (300, 'Light'), (400, 'Regular'), (600, 'Semi­bold'), (700, 'Bold'), (900, 'Black')]
LINE = 'Quousque tandem abutere, Catilina, patientia nostra?'
SOURCES = [('https://en.wikipedia.org/wiki/William_Caslon', 'William Caslon'),
           ('https://en.wikipedia.org/wiki/Traditional_point-size_names', 'Traditional point-size names'),
           ('https://en.wikipedia.org/wiki/Typeface_anatomy#Optical_size', 'optical size'),
           ('https://en.wikipedia.org/wiki/Source_Serif', 'Source Serif')]


def _pct(i):
    return 100 * i / (len(SIZES) - 1)


def _head():
    """The glide (the line's size, in the sheet's own units, log-linear between Caslon's steps) and the
    loupe's walk (holding on each block, moving between), both on the run's timeline."""
    glide = ' '.join(f'{_pct(i):.3f}%{{--lb:{math.log(b):.4f}}}' for i, (_, b, _r) in enumerate(SIZES))
    hold = 100 / (len(SIZES) - 1) * .32
    steps = []
    for i, (_, _b, (x0, y0, x1, y1)) in enumerate(SIZES):
        # centred on the block, but never past the sheet's edge
        at = (f'translate:clamp(calc(100cqw - var(--sw) * var(--m) * 1px), calc(50cqw - {(x0 + x1) / 2:.0f}px * var(--m)), 0px) '
              f'clamp(calc(100cqh - var(--sh) * var(--m) * 1px), calc(50cqh - {(y0 + y1) / 2:.0f}px * var(--m)), 0px)')
        for p in {max(0, _pct(i) - hold), min(100, _pct(i) + hold)}:
            steps.append((p, at))
    walk = ' '.join(f'{p:.3f}%{{{at}}}' for p, at in sorted(steps))
    return ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/source-serif-4/opsz.css">\n'
            f'<style>@keyframes glide{{{glide}}}@keyframes walk{{{walk}}}</style>\n')


HEAD = _head()

HOW = """@property --w { syntax: '<number>'; inherits: true; initial-value: 400 }
.line { font-weight: var(--w);                     /* the dial: any weight in one file */
        font-optical-sizing: auto;                 /* the design follows the size */
        font-size: calc(exp(var(--lb)) * var(--m) * 1px) }   /* the size glides with the scroll */
dial.oninput = () => stage.style.setProperty('--dial', dial.value)"""

NOTE = ('Caslon cut every size by hand as its own font, and a size was designed for its size: sturdier and clearer '
        'when small, finer when large. A variable font carries that as an axis, optical size, so as the line shrinks it '
        'turns into a text face and as it grows, into a display face. Weight is another axis. A family used to be six '
        'files, ExtraLight to Black; here they are six marks on one dial, and every weight between them is there too.')

MATERIAL = ('Material — William Caslon, A Specimen, 1734 · public domain; set against Source Serif 4, a variable font '
            'after the types of Pierre Simon Fournier')


def render(works):
    w = next(w for w in works if w['kind'] == 'caslon')
    n = len(SIZES)
    blocks = ''.join(f'<i style="--i:{i};--x:{x0};--y:{y0};--bw:{x1 - x0};--bh:{y1 - y0}"></i>'
                     for i, (_, _b, (x0, y0, x1, y1)) in enumerate(SIZES))
    sizes = ''.join(f'<li style="--i:{i}">{html.escape(name)}</li>' for i, (name, _b, _r) in enumerate(SIZES))
    marks = ''.join(f'<li style="--at:{(v - 200) / 700:.4f}"><b>{v}</b><span>{name}</span></li>' for v, name in WEIGHTS)
    alt = ('William Caslon’s specimen sheet of 1734: the opening of Cicero’s first speech against Catiline set in every '
           'size of his roman and italic, from French Cannon down to Pearl, beside Greek, Hebrew, Arabic and other scripts')
    return (f'<section class="specimen stage" data-material style="--n:{n}" aria-label="Caslon’s sizes of 1734, and one variable font">\n'
            '<div class="run">\n'
            '  <div class="frame">\n'
            '    <figure class="loupe">\n'
            f'      <div class="sheet" style="--sw:{w["w"]};--sh:{w["h"]}"><img src="{w["default"]}" srcset="{w["srcset"]}" '
            f'sizes="(max-width: 760px) 110vw, 180vw" width="{w["w"]}" height="{w["h"]}" alt="{html.escape(alt, quote=True)}" '
            f'decoding="async" fetchpriority="high"><span class="blocks" aria-hidden="true">{blocks}</span></div>\n'
            '      <figcaption>Metal · a separate font for every size</figcaption>\n'
            '    </figure>\n'
            '    <div class="file">\n'
            '      <p class="kicker">One file · every size and weight between</p>\n'
            f'      <p class="line" lang="la">{html.escape(LINE)}</p>\n'
            '      <div class="dial">\n'
            '        <label for="weight">Weight</label><output for="weight">400</output>\n'
            '        <input type="range" id="weight" min="200" max="900" step="1" value="400">\n'
            f'        <ol class="marks" aria-label="The weights a family once shipped as separate files">{marks}</ol>\n'
            '      </div>\n'
            '    </div>\n'
            f'    <ol class="sizes" aria-label="Caslon’s sizes, largest first">{sizes}</ol>\n'
            '  </div>\n'
            '</div>\n'
            '</section>')


def credit(works):
    w = next(w for w in works if w['kind'] == 'caslon')
    return (f'Sheet — <a href="{w["descurl"]}">A Specimen by William Caslon, Letter-Founder, in Chiswell-Street, London</a>, '
            '1734; public domain, via Wikimedia Commons. Type — Source Serif 4, Adobe, inspired by the forms of Pierre '
            'Simon Fournier; SIL Open Font License. Facts — ' + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
