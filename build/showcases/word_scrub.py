"""Word Scrub, in full: the closing paragraph of On the Origin of Species, lit a
word at a time by the scroll, with some of its words calling up a plate from
Ernst Haeckel's Kunstformen der Natur.

Every word is served as text. The build wraps each in a span and says where its
sentence sits in the reading (--a, --b as a share of the run); the stylesheet
gives each word its own slice of that from its place among its siblings. A plate
keyed to a word carries the same numbers, so it arrives exactly with its word.
"""
import html

TITLE = 'Endless forms'
GLOSS = ('The paragraph lights up a word at a time, and how much of it has arrived is how far you have come down the page.')
LEDE = ('The closing paragraph of Darwin’s <i>On the Origin of Species</i>, 1859. Scroll, and it lights a word at a time; '
        'some of its words call up a plate from Ernst Haeckel’s <i>Art Forms in Nature</i> — in silver, until the last line.')

# The paragraph as printed in the first edition (London: John Murray, 1859), page 490.
SENTENCES = [
    'It is interesting to contemplate an entangled bank, clothed with many plants of many kinds, with birds singing on the '
    'bushes, with various insects flitting about, and with worms crawling through the damp earth, and to reflect that these '
    'elaborately constructed forms, so different from each other, and dependent on each other in so complex a manner, have '
    'all been produced by laws acting around us.',
    'These laws, taken in the largest sense, being Growth with Reproduction; Inheritance which is almost implied by '
    'reproduction; Variability from the indirect and direct action of the external conditions of life, and from use and '
    'disuse; a Ratio of Increase so high as to lead to a Struggle for Life, and as a consequence to Natural Selection, '
    'entailing Divergence of Character and the Extinction of less-improved forms.',
    'Thus, from the war of nature, from famine and death, the most exalted object which we are capable of conceiving, '
    'namely, the production of the higher animals, directly follows.',
    'There is grandeur in this view of life, with its several powers, having been originally breathed into a few forms or '
    'into one; and that, whilst this planet has gone cycling on according to the fixed law of gravity, from so simple a '
    'beginning endless forms most beautiful and most wonderful have been, and are being, evolved.',
]
SOURCE = ('https://en.wikisource.org/wiki/On_the_Origin_of_Species_(1859)/Chapter_XIV', 'Wikisource')

# Haeckel's plates: label in assets/curated.json -> (Tafel, what it shows)
PLATES = {
    'Lichenes': (83, 'lichens'), 'Basimycetes': (63, 'fungi'), 'Diatomea': (84, 'diatoms'),
    'Ammonitida': (44, 'ammonites'), 'Decapoda': (86, 'crabs'), 'Antilopina': (100, 'antelopes'),
    'Spumellaria': (91, 'radiolarians'), 'Actiniae': (49, 'sea anemones'), 'Discomedusae': (8, 'jellyfish'),
    'Trochilidae': (99, 'hummingbirds'), 'Orchidae': (74, 'orchids'), 'Siphonophorae': (17, 'siphonophores'),
    'Nepenthaceae': (62, 'pitcher plants'), 'Chaetopoda': (96, 'bristle worms'), 'Batrachia': (68, 'frogs'),
    'Lacertilia': (79, 'lizards'), 'Chelonia': (89, 'turtles'), 'Muscinae': (72, 'mosses'), 'Ostraciontes': (42, 'boxfishes'),
}
# The silver plates, each called up by a word: (sentence, the word, plate). White-ground engravings are inverted.
CALLS = [(0, 'entangled', 'Lichenes'), (0, 'damp', 'Basimycetes'),
         (1, 'Growth', 'Diatomea'), (1, 'Extinction', 'Ammonitida'),
         (2, 'war', 'Decapoda'), (2, 'higher', 'Antilopina'),
         (3, 'grandeur', 'Spumellaria')]
INVERT = {'Antilopina'}
# From "endless" on, every word brings one of the colour plates, the grid filling from its middle outwards.
TILES = ['Actiniae', 'Discomedusae', 'Trochilidae', 'Orchidae', 'Siphonophorae', 'Nepenthaceae',
         'Chaetopoda', 'Batrachia', 'Lacertilia', 'Chelonia', 'Muscinae', 'Ostraciontes']
GRID = [(2, 2), (2, 3), (3, 2), (1, 2), (3, 3), (1, 3), (2, 1), (2, 4), (3, 1), (1, 4), (3, 4), (1, 1)]   # (row, column), in order of arrival
FINALE, PHRASE = 'endless', 7   # "endless forms most beautiful and most wonderful" keeps its light once it arrives

# The reading, in word-lengths: a lead-in, each sentence one unit per word, a gap between sentences, a tail to finish on.
LEAD, GAP, TAIL = 6, 14, 24

HOW = """.word { --k: sibling-index(); --n: sibling-count();
  --at: calc(var(--a) + (var(--b) - var(--a)) * (var(--k) - 1) / var(--n));
  animation: lit linear both; animation-timeline: --read;
  animation-range: contain calc(var(--at) * 1%) contain calc((var(--at) + var(--w)) * 1%) }"""

NOTE = ('Every word is plain text in the page, each in its own span. The stylesheet reads a word’s place among its siblings '
        'with <code>sibling-index()</code>, so no script counts, wraps or measures anything — and a plate keyed to a word '
        'arrives on exactly the same slice.')

MATERIAL = 'Material — Charles Darwin, 1859 · Ernst Haeckel, <i>Kunstformen der Natur</i>, 1899–1904 · public domain'
CREDIT = ('Text — Charles Darwin, <i>On the Origin of Species</i>, London: John Murray, 1859, p. 490, via '
          f'<a href="{SOURCE[0]}">{SOURCE[1]}</a>. Plates — Ernst Haeckel, <i>Kunstformen der Natur</i>, 1899–1904, public domain, '
          'via Wikimedia Commons: ')


def _bare(word):
    return word.strip('.,;:').lower()


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'haeckel'}
    words = [s.split() for s in SENTENCES]
    units = LEAD + sum(len(ws) for ws in words) + GAP * (len(words) - 1) + TAIL
    at, t = [], LEAD
    for ws in words:
        at.append((t, t + len(ws)))
        t += len(ws) + GAP
    pct = lambda u: f'{u / units * 100:.3f}'.rstrip('0').rstrip('.')

    # the paragraph: one <p>, a span per sentence, a span per word
    sents = []
    for i, ws in enumerate(words):
        a, b = at[i]
        fs = (390 / len(SENTENCES[i])) ** .5
        finale = ws.index(FINALE) if i == len(words) - 1 else len(ws)
        spans = ' '.join(f'<span{" class=\"em\"" if finale <= j < finale + PHRASE else ""}>{html.escape(w)}</span>'
                         for j, w in enumerate(ws))
        sents.append(f'<span class="s" style="--a:{pct(a)};--b:{pct(b)};--fs:{fs:.2f}">{spans}</span>')

    # The whole stage sits near the top of the page, so every plate is within lazy-loading reach at once anyway:
    # load them outright, the later ones at low priority so the first plates win the bandwidth.
    def img(w, sizes, priority='low'):
        return (f'<img src="{w["default"]}" srcset="{w["srcset"]}" sizes="{sizes}" width="{w["w"]}" height="{w["h"]}" '
                f'alt="" decoding="async" fetchpriority="{priority}">')

    def key(i, word):
        k = next(j for j, w in enumerate(words[i]) if _bare(w) == word.lower()) + 1
        a, b = at[i]
        return f'--a:{pct(a)};--b:{pct(b)};--n:{len(words[i])};--k:{k}'

    fin = words[-1].index(FINALE)
    plates = []
    for c, (i, word, label) in enumerate(CALLS):
        n, what = PLATES[label]
        also = ' also' if c and CALLS[c - 1][0] == i else ''   # a second plate in the same sentence: its caption sits under the first
        # the last silver plate gives way when the colour arrives, on the word that brings it
        last = f' last" style="{key(i, word)};--kout:{fin + 1}' if i == len(words) - 1 else f'" style="{key(i, word)}'
        inv = ' inv' if label in INVERT else ''
        plates.append(f'<figure class="specimen{inv}{also}{last}">{img(by[label], "(max-width: 760px) 90vw, min(46vw, 58vh)", "auto" if c < 2 else "low")}'
                      f'<figcaption>Tafel {n} · <i>{label}</i> — {what}</figcaption></figure>')

    a, b = at[-1]
    tiles = []
    for j, label in enumerate(TILES):
        n, what = PLATES[label]
        r, c = GRID[j]
        tiles.append(f'<figure class="tile" style="--a:{pct(a)};--b:{pct(b)};--n:{len(words[-1])};--k:{fin + j + 1};grid-area:{r}/{c}">'
                     f'{img(by[label], "(max-width: 760px) 22vw, min(12vw, 20vh)")}<figcaption><i>{label}</i> {n}</figcaption></figure>')

    return ('<section class="read stage" data-material aria-label="The closing paragraph of On the Origin of Species, read a word at a time">\n'
            f'<div class="run" style="--units:{units}">\n<div class="pin">\n'
            '<figure class="passage">\n<blockquote cite="' + SOURCE[0] + '"><p>' + ' '.join(sents) + '</p></blockquote>\n'
            '<figcaption>Charles Darwin · <cite>On the Origin of Species</cite> · 1859 · the closing paragraph</figcaption>\n</figure>\n'
            '<div class="field" aria-hidden="true">\n<p class="cue">Scroll to read</p>\n' + '\n'.join(plates) + '\n<div class="tiles">' + ''.join(tiles) + '</div>\n</div>\n'
            '</div>\n</div>\n</section>')


def credit(works):
    """The plates used, each linked to its Commons record."""
    by = {w['label']: w for w in works if w['kind'] == 'haeckel'}
    used = [c[2] for c in CALLS] + TILES
    return CREDIT + ', '.join(f'<a href="{by[l]["descurl"]}">Tafel {PLATES[l][0]} <i>{l}</i></a>' for l in used) + '.'
