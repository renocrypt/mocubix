"""Scoped Rotation, in full: Georges Seurat's A Sunday on La Grande Jatte — 1884 (1884–86) redrawn as 3,456 dots,
and its palette as 24 swatches. One turning angle, @property --turn, can be declared on the swatches, on the root of
the page, or on the painting; a counter gives the frames a second the page keeps, from frame to frame.

A custom property that changes on an element changes on every element that inherits it, and each of those is given
a fresh computed style whether it uses the property or not; a trace shows the recalculation and the garbage it
leaves are the cost, the painting of it almost free. On the swatches the page keeps the screen's pace; on the root it
falls to about a fifth, for the same visible change; on the painting every dot takes the angle. showcase.js samples
the painting into the dots (Wikimedia serves its images to canvases), mirrors the choice into data-scope (an
attribute: a :has() in the dots' selectors made their style work five times dearer) and declares the angle nowhere
while the stage is out of view. The swatches are the painting's 24 most representative colours (palette.py
swatches, octree).
"""
import html, json
from pathlib import Path

TITLE = 'Where the angle lives'
LEDE = ('Seurat’s <i>A Sunday on La Grande Jatte</i>, redrawn as 3,456 dots, and its palette as 24 swatches. One '
        'turning angle can be declared on the swatches, on the root of the page, or on the painting. Choose, and watch '
        'the counter: the same change costs what its scope costs.')

SWATCHES = ('Grande Jatte', 24)          # palette.py swatches: the painting's most representative colours
GRID = (72, 48)                          # the dots, 3 : 2; each re-resolving element costs, and more dots made the
                                         # painting a slideshow (7,776: 9 frames a second; 3,456: 20)
SCOPES = [('still', 'nowhere', 'the colours stand still'),
          ('swatches', 'on the swatches', '25 elements'),
          ('root', 'on the root', 'every element on the page'),
          ('painting', 'on the painting', f'{GRID[0] * GRID[1] + 1:,} elements')]
SOURCES = [('https://en.wikipedia.org/wiki/A_Sunday_Afternoon_on_the_Island_of_La_Grande_Jatte',
            'A Sunday Afternoon on the Island of La Grande Jatte'),
           ('https://developer.mozilla.org/en-US/docs/Web/CSS/@property', '@property (MDN)')]

HOW = """@property --turn { syntax: '<number>'; inherits: true; initial-value: 0 }   /* degrees */
.swatches li { background: oklch(from var(--c) l c calc(h + var(--turn))) }
.swatches { animation: turn 8s linear infinite }   /* 25 elements re-resolve each frame */
:root     { animation: turn 8s linear infinite }   /* all of them do, though only 24 use it */"""

NOTE = ('Measured here in Chrome, frame to frame: declared on the swatches, the turn leaves the page at the screen’s '
        'own pace; declared on the root, it drops to about a fifth of that, for a change that still shows only on the '
        'same 24 swatches. An inherited custom property that changes on an element changes on everything below it, used '
        'or not, and every one of those elements is given a fresh computed style each frame: the recalculation and the '
        'garbage it leaves are the whole cost, and a trace shows the painting of it almost free. Asked of the painting, '
        'all 3,456 dots take the angle, and the cost buys something. The counter caught a selector as well: with a '
        '<code>:has()</code> in the dots’ rules their style work was five times greater, every element re-matching its '
        'selectors each frame, so the choice is mirrored into an attribute. Declare an animated property as low in the '
        'tree as it will serve, and register it with <code>inherits: false</code> when one element is all that needs it.')

MATERIAL = ('Material — Georges Seurat, <i>A Sunday on La Grande Jatte — 1884</i>, 1884–86 · Art Institute of Chicago · '
            'public domain')


def render(works):
    w = next(w for w in works if w['kind'] == 'seurat')
    chips = json.load(open(Path(__file__).resolve().parents[2] / 'assets/palettes.json', encoding='utf-8'))[f'swatches:{SWATCHES[0]}']
    radios = ''.join(
        f'<input type="radio" name="scope" id="scope-{k}" value="{k}"{" checked" if k == "swatches" else ""}>'
        f'<label for="scope-{k}">{name}<small>{note}</small></label>' for k, name, note in SCOPES)
    cols, rows = GRID
    return (
        '<section class="scope stage" data-material data-scope="swatches" aria-label="One turning angle, declared on the swatches, the root or '
        'the painting, and what each costs">\n'
        f'<div class="mosaic" role="img" style="--cols:{cols};--rows:{rows};--src:url({w["sources"]["500"]})" aria-label="Seurat’s A Sunday on La Grande '
        f'Jatte, redrawn as {cols * rows:,} dots"></div>\n'
        '<aside class="panel">\n'
        f'  <fieldset class="where"><legend>Where the angle is declared</legend>{radios}</fieldset>\n'
        '  <div class="meter">\n'
        '    <p class="ms"><output>0</output><span>frames a second</span></p>\n'
        '    <p class="n"><output>0</output><span>elements re‑resolving</span></p>\n'
        '    <canvas width="480" height="96" aria-hidden="true"></canvas>\n'
        '    <p class="scale">the last two seconds, frame by frame; the line is one frame at 60 Hz, 16.7 ms</p>\n'
        '  </div>\n'
        '  <ul class="swatches" aria-label="The painting’s palette, 24 swatches">'
        + ''.join(f'<li style="--c:{c}"></li>' for c in chips) + '</ul>\n'
        f'  <figure class="original"><img src="{w["sources"]["500"]}" width="{w["w"]}" height="{w["h"]}" '
        f'style="--ar:{w["w"] / w["h"]:.4f}" crossorigin="anonymous" alt="Georges Seurat, A Sunday on La Grande Jatte: '
        'Parisians at leisure on an island in the Seine, in the shade and sun of a summer afternoon, painted in small '
        'touches of colour" decoding="async"><figcaption>Georges Seurat, <i>A Sunday on La Grande Jatte — 1884</i>, '
        '1884–86 · Art Institute of Chicago</figcaption></figure>\n'
        '</aside>\n'
        '</section>')


def credit(works):
    w = next(w for w in works if w['kind'] == 'seurat')
    return (f'Painting — Georges Seurat, <a href="{w["descurl"]}">A Sunday on La Grande Jatte — 1884</a>, 1884–86, Art '
            'Institute of Chicago, public domain, via Wikimedia Commons; its dots sampled from the image in the '
            'browser, its swatches its 24 most representative colours. Facts — '
            + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
