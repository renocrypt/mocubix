"""Curtain Overlap, in full: Montmartre in posters, 1889–1896. Eight posters by
Chéret, Toulouse-Lautrec, Mucha and Steinlen, each on a panel the height of the
screen in one of its own inks. Every panel is sticky at the top of the stage, so
the next one rides up over it; the incoming sheet casts its shadow on the one it
covers, and the covered one recedes a little, on the incoming one's own timeline.

The grounds and inks are the posters' own colours (their quantised palettes,
build/palette.py), chosen by eye so that neighbours never share one; some are
deepened or lightened so the type reads.
"""
import html

TITLE = 'Montmartre, pasted over'
LEDE = ('Eight posters from the Paris of 1889 to 1896, each on a panel in one of its own inks. Scroll, and each new '
        'panel rides up over the last — the way a billposter pasted one poster over another.')

# label in assets/curated.json, the words on it, artist, year, one line, where the scan is from,
# the panel's ground, its ink (both taken from the poster), which side the poster hangs on
POSTERS = [
    ('Bal du Moulin Rouge', 'Moulin Rouge', 'Jules Chéret', '1889',
     'For the opening of the Moulin Rouge on the Place Blanche, on 6 October 1889.', 'Bibliothèque nationale de France',
     '#A6473A', '#F0E0C2', 'right'),
    ('La Goulue', 'La Goulue', 'Henri de Toulouse-Lautrec', '1891',
     'His first poster, for the Moulin Rouge: La Goulue dancing, the crowd a black frieze, her partner Valentin in grey.',
     'The Metropolitan Museum of Art', '#DCC47E', '#0E1820', 'left'),
    ('Saxoléine', 'Saxoléine', 'Jules Chéret', '1891',
     'A safety paraffin for lamps, sold by a woman in yellow under a red shade.', 'Bibliothèque nationale de France',
     '#101634', '#E0673F', 'right'),
    ('Aristide Bruant', 'Aristide Bruant', 'Henri de Toulouse-Lautrec', '1892',
     'The singer in his black cape and red scarf, for his season at the Ambassadeurs.', 'Art Institute of Chicago',
     '#D8703E', '#1C2229', 'left'),
    ('Divan Japonais', 'Divan Japonais', 'Henri de Toulouse-Lautrec', '1893',
     'A café-concert at 75 rue des Martyrs: the dancer Jane Avril and the critic Édouard Dujardin in the front row.',
     'National Gallery of Victoria', '#2B2926', '#D9BF7C', 'right'),
    ('La Loïe Fuller', 'Loïe Fuller', 'Jules Chéret', '1893',
     'The Folies-Bergère’s Loïe Fuller, whose Serpentine Dance swirled silk under coloured light of her own design.',
     'Bibliothèque nationale de France', '#C08E70', '#241E30', 'left'),
    ('Gismonda', 'Gismonda', 'Alphonse Mucha', '1894',
     'For Sarah Bernhardt in Sardou’s Gismonda. It went up on 1 January 1895; she ordered four thousand copies and '
     'gave Mucha a six-year contract.', 'Museum of Decorative Arts in Prague', '#4F4C35', '#EAD3AF', 'right'),
    ('Chat Noir', 'Le Chat Noir', 'Théophile-Alexandre Steinlen', '1896',
     'Coming soon: the shadow theatre of Rodolphe Salis’s cabaret, on tour.', 'Rijksmuseum', '#CFA06A', '#1E1A18', 'left'),
]
SOURCES = [('https://en.wikipedia.org/wiki/Moulin_Rouge', 'Moulin Rouge'), ('https://en.wikipedia.org/wiki/Alphonse_Mucha', 'Alphonse Mucha'),
           ('https://en.wikipedia.org/wiki/Divan_Japonais', 'Divan Japonais'), ('https://en.wikipedia.org/wiki/Le_Chat_Noir', 'Le Chat Noir'),
           ('https://en.wikipedia.org/wiki/Loie_Fuller', 'Loie Fuller')]

HOW = """.panel { position: sticky; top: var(--bar); height: calc(100svh - var(--bar)) }
  /* every panel sticks at the same place, so the next one rides over it */
.panel::before { bottom: 100%; background: linear-gradient(transparent, rgb(0 0 0 / .4)) }
  /* the incoming sheet's shadow falls on the one it covers */
.panel > .room { animation: recede linear both; animation-timeline: --next;
                 animation-range: entry 0% entry 100% }  /* on the next panel's timeline */"""

NOTE = ('The overlap itself is two lines: every panel is sticky at the same place, so each one that follows scrolls up over '
        'it. Nothing is animated for that. The depth is extra and costs little: the incoming panel carries its own shadow '
        'above its top edge, and the covered one recedes on the incoming one’s view timeline, shared through '
        '<code>timeline-scope</code>.')

MATERIAL = 'Material — posters by Chéret, Toulouse-Lautrec, Mucha and Steinlen, 1889–1896 · public domain'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'posters'}
    n = len(POSTERS)
    panels = []
    for i, (label, words, artist, year, line, source, ground, ink, side) in enumerate(POSTERS):
        w = by[label]
        own = f';view-timeline-name:--c{i}' if i else ''                          # its timeline, for the one it covers
        nxt = f' style="--next:--c{i + 1}"' if i + 1 < n else ''                  # the timeline of the one that covers it
        panels.append(
            f'<article class="panel {side}" style="--ground:{ground};--ink:{ink}{own}">\n'
            f'  <div class="room"{nxt}>\n'
            f'    <figure class="bill" style="--ar:{w["w"] / w["h"]:.4f}"><img src="{w["default"]}" srcset="{w["srcset"]}" '
            f'sizes="(max-width: 760px) 64vw, min(46svh, 560px)" width="{w["w"]}" height="{w["h"]}" '
            f'alt="{html.escape(f"{artist}, {words}, poster, {year}", quote=True)}" decoding="async"'
            f'{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}></figure>\n'
            f'    <div class="words"><p class="no">{i + 1:02d} / {n:02d} · {year}</p>'
            f'<h2>{html.escape(words)}</h2>'
            f'<p class="by">{html.escape(artist)}</p><p class="line">{html.escape(line)}</p>'
            f'<p class="src">{html.escape(source)}</p></div>\n'
            f'  </div>\n'
            f'</article>')
    scope = ', '.join(f'--c{i}' for i in range(1, n))
    return (f'<section class="hoarding stage" data-material style="timeline-scope:{scope}" '
            f'aria-label="Eight posters from Montmartre, 1889 to 1896">\n' + '\n'.join(panels) + '\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'posters'}
    links = ', '.join(f'<a href="{by[p[0]]["descurl"]}">{html.escape(p[1])}</a> ({html.escape(p[5])})' for p in POSTERS)
    return (f'Posters — public domain, via Wikimedia Commons: {links}. '
            'Facts — ' + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
