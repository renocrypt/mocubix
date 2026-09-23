"""Scrollspy, in full: Around the World in Eighty Days. The index is the plan the Morning Chronicle
worked out in chapter III (eight legs, eighty days), set as a timetable that stays beside the story;
the story is the eight legs as they went, each with an engraving from the illustrated French edition
(Alphonse de Neuville and Léon Benett) and a line of the 1873 translation by George Makepeace Towle.

Whichever leg has reached the top of the screen is marked in the timetable, the legs behind it are
ticked off, and the ones ahead wait. No script: the timetable's links form a scroll-target group
(scroll-target-group: auto), and :target-current, :target-before and :target-after do the rest.
"""
import html

TITLE = 'Eighty days, leg by leg'
GLOSS = 'Whatever has reached the top of the screen is the thing the index marks as where you are.'
LEDE = ('In the winter of 1872 readers of Le Temps followed Phileas Fogg around the world in instalments, and the last '
        'appeared on his deadline. Read the journey: the timetable beside it marks the leg you are on, and ticks off '
        'the ones behind you.')

# the plan as the Morning Chronicle printed it (chapter III), and each leg as it went: the engraving's label in
# assets/curated.json, what it shows, a line of the 1873 translation, its chapter
LEGS = [
    ('From London to Suez, viâ Mont Cenis and Brindisi, by rail and steamboats', 7, 'Wager',
     'The wager at the Reform Club', '“The world is big enough.” “It was once,” said Phileas Fogg, in a low tone.', 'III'),
    ('From Suez to Bombay, by steamer', 13, 'Pagoda', 'Passepartout in the pagoda on Malabar Hill',
     '…he happened to espy the splendid pagoda on Malabar Hill, and was seized with an irresistible desire to see its '
     'interior.', 'X'),
    ('From Bombay to Calcutta, by rail', 3, 'Elephant', 'Across India on the elephant Kiouni',
     '“What a price, good heavens!” cried Passepartout, “for an elephant.”', 'XI'),
    ('From Calcutta to Hong Kong, by steamer', 13, 'Tavern', 'Fix and Passepartout in a Hong Kong tavern',
     'It was in one of these dens that Fix and Passepartout, in search of a friendly glass, found themselves.', 'XIX'),
    ('From Hong Kong to Yokohama (Japan), by steamer', 6, 'Tankadere', 'The Tankadere in the typhoon',
     'But John Bunsby believed in the “Tankadere,” which rode on the waves like a seagull; and perhaps he was not '
     'wrong.', 'XXI'),
    ('From Yokohama to San Francisco, by steamer', 22, 'Pyramid', 'The human pyramid of the Long Noses at Yokohama',
     '…the pyramid tottered, the balance was lost, one of the lower noses vanished from the pyramid, and the human '
     'monument was shattered like a castle built of cards!', 'XXIII'),
    ('From San Francisco to New York, by rail', 7, 'Sledge', 'A sledge with sails across the frozen plains',
     'The sledge sped on as lightly as a boat over the waves.', 'XXXI'),
    ('From New York to London, by steamer and rail', 9, 'Reform Club', 'Back at the Reform Club',
     '…the pendulum had not beat the sixtieth second when Phileas Fogg appeared, followed by an excited crowd who had '
     'forced their way through the club doors, and in his calm voice, said, “Here I am, gentlemen!”', 'XXXVI'),
]
ROMAN = 'I II III IV V VI VII VIII'.split()
SOURCES = [('https://en.wikipedia.org/wiki/Around_the_World_in_Eighty_Days', 'Around the World in Eighty Days'),
           ('https://www.gutenberg.org/ebooks/103', 'the Towle translation at Project Gutenberg')]

HEAD = ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/old-standard-tt/index.css">\n'
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource/old-standard-tt/400-italic.css">\n')

HOW = """.plan ol { scroll-target-group: auto }        /* its links become markers for the sections */
.plan a:target-current { color: var(--ink) }   /* the leg you are on */
.plan a:target-before::before { content: '✓' } /* the legs behind you */
.plan a:target-after { opacity: .45 }          /* the legs ahead */"""

NOTE = ('The index is only links to the eight legs, grouped: scroll-target-group makes the browser keep track of which '
        'target you have reached, and the timetable styles itself from that, with no observer and no script. The '
        'links still work as links. Fogg believed he had come home a day late; travelling east, he had seen eighty '
        'sunrises while London saw seventy-nine, and he had won.')

MATERIAL = ('Material — Jules Verne, Around the World in Eighty Days, 1872; engravings by Alphonse de Neuville and '
            'Léon Benett; translated by George Makepeace Towle · public domain')


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'verne'}
    day, rows, legs = 0, [], []
    for i, (plan, days, label, shows, line, chapter) in enumerate(LEGS):
        first, day = day + 1, day + days
        w = by[label]
        rows.append(f'<li><a href="#leg-{i + 1}"><span class="n">{ROMAN[i]}</span><span class="way">{html.escape(plan)}</span>'
                    f'<span class="d">{days} days</span></a></li>')
        legs.append(
            f'<section class="leg" id="leg-{i + 1}" aria-labelledby="leg-{i + 1}-h">\n'
            f'  <p class="when">Days {first}–{day} of 80</p>\n'
            f'  <h2 id="leg-{i + 1}-h"><span>{ROMAN[i]}</span> {html.escape(plan.split(",")[0])}</h2>\n'
            f'  <figure><img src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 78vw, min(40vw, 46svh, 520px)" '
            f'width="{w["w"]}" height="{w["h"]}" alt="{html.escape(f"Engraving by de Neuville or Benett: {shows}", quote=True)}" '
            f'decoding="async"{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}>'
            f'<figcaption>{html.escape(shows)}</figcaption></figure>\n'
            f'  <blockquote><p>{html.escape(line)}</p><cite>Chapter {chapter}</cite></blockquote>\n'
            f'</section>')
    m = by['Map']
    return ('<section class="voyage stage" data-material aria-label="Around the World in Eighty Days: the plan, and the journey">\n'
            '<nav class="plan" aria-label="The plan, leg by leg">\n'
            f'  <img class="route" src="{m["default"]}" srcset="{m["srcset"]}" sizes="30vw" '
            f'width="{m["w"]}" height="{m["h"]}" alt="The route of the journey on a map of the world, from the illustrated French edition" '
            'decoding="async" loading="lazy">\n'
            '  <p class="head">The plan, as the Morning Chronicle worked it out</p>\n'
            f'  <ol>{"".join(rows)}</ol>\n'
            '  <p class="total"><span>Total</span><span class="d">80 days</span></p>\n'
            '</nav>\n'
            '<div class="legs">\n' + '\n'.join(legs) + '\n'
            '<p class="coda">Phileas Fogg had, without suspecting it, gained one day on his journey, and this merely because he '
            'had travelled constantly eastward. <cite>Chapter XXXVII</cite></p>\n'
            '</div>\n'
            '</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'verne'}
    links = ', '.join(f'<a href="{by[l[2]]["descurl"]}">{html.escape(l[3].lower())}</a>' for l in LEGS)
    return ('Engravings — Alphonse de Neuville and Léon Benett, for the illustrated French edition of Le Tour du monde en '
            f'quatre-vingts jours; public domain, via Wikimedia Commons: {links}, and <a href="{by["Map"]["descurl"]}">the '
            'route map</a>. Text — the translation by George Makepeace Towle. Facts — '
            + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
