"""Scroll Snap, in full: the calendar of the Très Riches Heures du Duc de Berry,
twelve months, a page each. The book is its own scroller and snaps: however far
you throw it, it comes to rest on a whole month, never between two.

Two properties make the book (scroll-snap-type on the scroller, scroll-snap-align
on each page). The gold mark in the index beside it rides the book's own scroll
timeline, continuously, so the difference between where you are scrolling and
where the page comes to rest can be seen.
"""
import html

TITLE = 'Twelve months, a page each'
GLOSS = ('Scrolling comes to rest on a whole page instead of halfway between two. It feels like turning the pages of a book.')
LEDE = ('The calendar of the Très Riches Heures, painted for the Duke of Berry by the Limbourg brothers about 1412–16. '
        'Scroll the book: it always comes to rest on a whole month. The mark beside it shows where you really are.')

# label in assets/curated.json (the month), the signs of the zodiac on its arch, what is painted below
MONTHS = [
    ('Janvier', 'Capricorn · Aquarius', 'The Duke of Berry at his New Year’s feast.'),
    ('Février', 'Aquarius · Pisces', 'Snow on a farmyard: three warm themselves at the fire while a man cuts wood outside.'),
    ('Mars', 'Pisces · Aries', 'Ploughing, pruning and sowing below the Château de Lusignan.'),
    ('Avril', 'Aries · Taurus', 'A betrothal in a walled garden, the Château de Dourdan behind.'),
    ('Mai', 'Taurus · Gemini', 'A May ride through the woods, the riders crowned with leaves.'),
    ('Juin', 'Gemini · Cancer', 'Haymaking before the Palais de la Cité and the Sainte-Chapelle.'),
    ('Juillet', 'Cancer · Leo', 'Harvesting the wheat and shearing sheep below the palace at Poitiers.'),
    ('Août', 'Leo · Virgo', 'Falconers ride out; swimmers in the river below the Château d’Étampes.'),
    ('Septembre', 'Virgo · Libra', 'The grape harvest below the Château de Saumur.'),
    ('Octobre', 'Libra · Scorpio', 'Sowing winter wheat before the Louvre.'),
    ('Novembre', 'Scorpio · Sagittarius', 'A swineherd knocks down acorns for his pigs.'),
    ('Décembre', 'Sagittarius · Capricorn', 'The boar hunt at bay, the Château de Vincennes behind the trees.'),
]
ROMAN = 'I II III IV V VI VII VIII IX X XI XII'.split()
SOURCE = ('https://en.wikipedia.org/wiki/Tr%C3%A8s_Riches_Heures_du_Duc_de_Berry', 'Très Riches Heures du Duc de Berry')

HOW = """.book { overflow-y: auto; scroll-snap-type: y mandatory;   /* the book comes to rest… */
        scroll-timeline: --book }
.page { scroll-snap-align: start }                         /* …on a whole page */
.months::after { animation: turn linear; animation-timeline: --book } /* where you really are */"""

NOTE = ('Two properties, and the book inherits the platform’s own scrolling: momentum, a trackpad’s feel, the keyboard, '
        'a flick that carries it three months at once and still lands on a whole one. The index beside it moves with the '
        'scroll itself, so you can watch the page settle where the scroll would not.')

MATERIAL = ('Material — the Très Riches Heures du Duc de Berry, calendar, the Limbourg brothers, about 1412–16, '
            'Musée Condé, Chantilly · public domain')


def _id(month):
    return 'm-' + month.lower().replace('é', 'e').replace('û', 'u')


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'heures'}
    pages, index = [], []
    for i, (month, signs, scene) in enumerate(MONTHS):
        w = by[month]
        pages.append(
            f'<article class="page" id="{_id(month)}">\n'
            f'  <img src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 60vw, min(46svh, 520px)" '
            f'width="{w["w"]}" height="{w["h"]}" style="--ar:{w["w"] / w["h"]:.4f}" '
            f'alt="{html.escape(f"The Très Riches Heures, {month}: {scene}", quote=True)}" decoding="async"'
            f'{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}>\n'
            f'  <div class="leaf"><p class="num">{ROMAN[i]}</p><h2 lang="fr">{month}</h2>'
            f'<p class="signs">{signs}</p><p class="scene">{html.escape(scene)}</p></div>\n'
            f'</article>')
        index.append(f'<li><a href="#{_id(month)}"><b>{ROMAN[i]}</b><span lang="fr">{month}</span></a></li>')
    return ('<section class="heures stage" data-material aria-label="The calendar of the Très Riches Heures, a page a month">\n'
            '<div class="book" tabindex="0" aria-label="The book: scroll, or use the arrow keys">\n'
            + '\n'.join(pages) +
            '\n</div>\n'
            f'<ol class="months" aria-label="The months">{"".join(index)}</ol>\n'
            '<p class="colophon">The Limbourg brothers · about 1412–16 · Musée Condé, Chantilly, MS 65</p>\n'
            '</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'heures'}
    links = ', '.join(f'<a href="{by[m[0]]["descurl"]}" lang="fr">{m[0]}</a>' for m in MONTHS)
    return ('Pages — the Très Riches Heures du Duc de Berry, calendar, painted by the Limbourg brothers about 1412–16 and '
            f'finished in 1485–89 by Jean Colombe; Musée Condé, Chantilly; public domain, via Wikimedia Commons: {links}. '
            f'Facts — <a href="{SOURCE[0]}">{SOURCE[1]}</a>.')
