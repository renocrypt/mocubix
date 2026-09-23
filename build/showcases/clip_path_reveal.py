"""Clip-path Reveal, in full: Sergei Prokudin-Gorsky's colour photographs of the Russian
Empire, 1905–1915, made the way he made them. His camera took three black-and-white
exposures, one after another, through red, green and blue filters; the Library of
Congress's colour renderings were put together from those three records, so each of their
channels is one of them.

Each picture is held on a black stage while you scroll, and its three records are laid down
one at a time: an edge in the filter's colour travels across and uncovers the red record,
then the green, then the blue, and the colour arrives where all three have passed. Each
record is the same picture seen through its filter (multiplied by pure red, green or blue);
the three are added back together (screen, on black). No script.
"""
import html

TITLE = 'Red, then green, then blue'
LEDE = ('Sergei Prokudin-Gorsky photographed the Russian Empire in colour with a camera that made three black-and-white '
        'exposures, one after another, through red, green and blue filters. Scroll: an edge carries each record across '
        'the picture, and the colour arrives where all three have passed.')

# label in assets/curated.json, who or what, where and when, the picture described
PICTURES = [
    ('Alim Khan', 'Alim Khan, Emir of Bukhara', 'Bukhara · 1911',
     'Alim Khan, the Emir of Bukhara, seated in a robe of blue silk figured with flowers, before a carved wooden door'),
    ('Peasant girls', 'Peasant girls', 'On the Sheksna, near Kirillov · 1909',
     'Three young peasant women in red and purple dresses before a wooden house, offering berries'),
    ('Gur-e Amir', 'The Gur-e Amir, Timur’s tomb', 'Samarkand · 1905–15',
     'The ribbed blue dome of the Gur-e Amir in Samarkand, seen from the east'),
    ('Tea harvest', 'Harvesting tea', 'Chakva · 1905–15',
     'Women and girls with baskets standing among the rows of a tea plantation on the hills at Chakva'),
    ('Nilov Monastery', 'The Nilov Monastery', 'From Svetlitsa Island, Lake Seliger · 1910',
     'The white Nilov Monastery across the water of Lake Seliger, a wooden causeway leading to it'),
]
RECORDS = [('r', 'Red'), ('g', 'Green'), ('b', 'Blue')]
SOURCE = ('https://en.wikipedia.org/wiki/Sergey_Prokudin-Gorsky', 'Sergey Prokudin-Gorsky')

HOW = """.rec { background: var(--filter) }             /* red, green or blue */
.rec img { mix-blend-mode: multiply }          /* the picture through that filter: one record */
.rec + .rec { mix-blend-mode: screen }         /* the three records added back together */
.rec { animation: uncover linear both; animation-timeline: --picture; animation-range: contain 4% contain 30% }
@keyframes uncover { from { clip-path: inset(0 100% 0 0) } }   /* an edge travels across */"""

NOTE = ('Each record is the same file seen through its filter — multiplied by pure red, green or blue, so only that '
        'record survives — and the three are added back together on black. Each is uncovered by an edge that travels '
        'across it with the scroll, never faded up underneath, so wherever one or two records have passed the '
        'picture is in the colours of one or two filters, and it comes right only where all three have been. Where '
        'someone moved between the three exposures — the girl at the left of the tea harvest — the records disagree, '
        'and her outline keeps a fringe of colour.')

MATERIAL = 'Material — Sergei Prokudin-Gorsky, colour photographs of the Russian Empire, 1905–1915 · public domain'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'prokudin'}
    rooms = []
    for i, (label, who, where, alt) in enumerate(PICTURES):
        w = by[label]
        img = (f'<img src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 92vw, min(120svh, 1400px)" '
               f'width="{w["w"]}" height="{w["h"]}" decoding="async"{" fetchpriority=\"high\"" if i == 0 else " loading=\"lazy\""}')
        recs = ''.join(
            f'<div class="rec {k}">{img} '
            + (f'alt="{html.escape(f"Sergei Prokudin-Gorsky: {alt}", quote=True)}"' if k == 'b' else 'alt=""')
            + '></div>' for k, _ in RECORDS)
        legend = ''.join(f'<li class="{k}">{name}</li>' for k, name in RECORDS)
        rooms.append(
            f'<article class="picture" style="--ar:{w["w"] / w["h"]:.4f}" aria-labelledby="pic{i}">\n'
            f'  <div class="frame">\n'
            f'    <figure><div class="pic">{recs}</div>\n'
            f'      <figcaption><span class="who"><b id="pic{i}">{html.escape(who)}</b><span>{html.escape(where)}</span></span>'
            f'<ol class="records" aria-label="The three records">{legend}</ol></figcaption></figure>\n'
            f'  </div>\n'
            f'</article>')
    return ('<section class="empire stage" data-material aria-label="Five colour photographs by Prokudin-Gorsky, '
            'each laid down in its three records">\n' + '\n'.join(rooms) + '\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'prokudin'}
    links = ', '.join(f'<a href="{by[p[0]]["descurl"]}">{html.escape(p[1])}</a>' for p in PICTURES)
    return ('Photographs — Sergei Prokudin-Gorsky; colour renderings from his three-colour glass negatives, Library of '
            'Congress Prints and Photographs Division; public domain, via Wikimedia '
            f'Commons: {links}. Facts — <a href="{SOURCE[0]}">{SOURCE[1]}</a>.')
