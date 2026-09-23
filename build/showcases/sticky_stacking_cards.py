"""Sticky Stacking Cards, in full: the trumps of the Visconti-Sforza tarot, made
around 1451, dealt onto the table as the page scrolls. Every card is sticky at
the same place, a few pixels lower than the last, so each lands on the pile.

Twenty of the twenty-two trumps survive. For the Devil and the Tower the deal
pauses: their places are in the list beside the pile, and nothing lands.
"""
import html, random

TITLE = 'Twenty of twenty-two'
LEDE = ('The trumps of the tarot made around 1451 for the Sforza dukes of Milan, dealt onto the table as you scroll: '
        'each catches on the pile and the next lands over it. Of the deck’s 78 cards, 74 survive. Two of its trumps, '
        'the Devil and the Tower, have never been found.')

# the trumps in their usual order: name (a label in assets/curated.json, or a lost card), what is painted on it
TRUMPS = [
    ('The Fool', 'A ragged man, barefoot, with feathers in his hair and a club over his shoulder.'),
    ('The Magician', 'A man in red at a table set with small things, a wand in his hand.'),
    ('The Popess', 'A woman in a nun’s habit, wearing the papal crown, a book in her hand.'),
    ('The Empress', 'A crowned woman with a sceptre and a shield of the black eagle.'),
    ('The Emperor', 'A bearded emperor, crowned, with sceptre and orb.'),
    ('The Pope', 'A pope enthroned in the triple crown, his hand raised in blessing.'),
    ('The Lovers', 'A couple join hands beneath Cupid, blindfolded, on a pedestal.'),
    ('The Chariot', 'A crowned lady in a golden chariot drawn by two white horses.'),
    ('Justice', 'A woman with sword and scales; above her, a knight rides out.'),
    ('The Hermit', 'An old man in a blue cloak and a wide hat, holding an hourglass.'),
    ('The Wheel of Fortune', 'Fortune, blindfolded, at the hub of her wheel: one climbs, one reigns, one falls, one crawls beneath.'),
    ('Strength', 'A young man raises a club over a lion.'),
    ('The Hanged Man', 'A man hangs by one foot from a wooden frame.'),
    ('Death', 'A skeleton with a bow.'),
    ('Temperance', 'A woman pours from one jug into another.'),
    ('The Devil', None),
    ('The Tower', None),
    ('The Star', 'A woman in blue holds up a star.'),
    ('The Moon', 'A woman holds up the crescent moon.'),
    ('The Sun', 'A winged child flies over the hills, holding up the sun’s face.'),
    ('Judgement', 'Angels sound their trumpets and the dead rise from the tomb.'),
    ('The World', 'Two winged children hold up a walled city under the stars.'),
]
SOURCE = ('https://en.wikipedia.org/wiki/Visconti-Sforza_tarot_deck', 'Visconti-Sforza tarot deck')

HOW = """.card { position: sticky; top: calc(var(--bar) + 6svh + var(--i) * 5px);  /* each lands a little lower */
        view-timeline: --land }
.face { animation: deal linear both; animation-timeline: --land;
        animation-range: cover 0% cover 48% }            /* dealt in before it sticks */"""

NOTE = ('One property builds the pile: every card is sticky at nearly the same place, so each one that arrives stops over '
        'the last, five pixels lower, and the deck’s edge grows down the table. The deal itself is the card’s own view '
        'timeline, finished before it sticks; the glint across the gold leaf rides the same timeline.')

MATERIAL = 'Material — the Visconti-Sforza tarot (Pierpont Morgan–Bergamo deck), about 1451 · public domain'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'tarot'}
    rnd = random.Random(1451)
    cards, labels, dealt = [], [], 0
    for i, (name, what) in enumerate(TRUMPS):
        if what is None:
            cards.append(f'<li class="card gap" aria-hidden="true" style="--i:{dealt}"></li>')
            labels.append(f'<li class="lost"><b>{html.escape(name)}</b><span>Lost</span></li>')
            continue
        w = by[name]
        side = 1 if rnd.random() < .5 else -1
        style = f'--i:{dealt};--r:{side * rnd.uniform(.6, 2.4):.2f}deg;--r0:{-side * rnd.uniform(9, 15):.1f}deg;--x0:{-side * rnd.uniform(16, 30):.0f}%'
        cards.append(f'<li class="card" style="{style}"><div class="face"><img src="{w["default"]}" srcset="{w["srcset"]}" '
                     f'sizes="(max-width: 760px) min(18svh, 140px), min(32svh, 270px)" width="{w["w"]}" height="{w["h"]}" '
                     f'alt="{html.escape(f"{name}: {what}", quote=True)}" decoding="async"{"" if i < 3 else " loading=\"lazy\""}></div></li>')
        labels.append(f'<li><b>{html.escape(name)}</b><span>{html.escape(what)}</span></li>')
        dealt += 1
    return ('<section class="deal stage" data-material aria-label="The Visconti-Sforza trumps, dealt onto a pile">\n'
            f'<ol class="pile">{"".join(cards)}</ol>\n'
            f'<ol class="names">{"".join(labels)}</ol>\n'
            '</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'tarot'}
    links = ', '.join(f'<a href="{by[n]["descurl"]}">{html.escape(n.replace("The ", ""))}</a>' for n, w in TRUMPS if w)
    return ('Cards — the Visconti-Sforza tarot, the Pierpont Morgan–Bergamo deck, about 1451 (the Morgan Library & Museum, '
            f'the Accademia Carrara and the Colleoni family), public domain, via Wikimedia Commons: {links}. '
            f'Facts — <a href="{SOURCE[0]}">{SOURCE[1]}</a>.')
