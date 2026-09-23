"""Scroll Markers, in full: a journey outward through nine Webb images.

The markers are the carousel's own ::scroll-marker pseudo-elements; each
stop's distance is from NASA or ESA (sources noted beside each)."""
import html

TITLE = 'A journey outward'
GLOSS = 'The row of pictures along the bottom is made by the carousel itself, and follows wherever you are in it.'
LEDE = ('Nine pictures from the James Webb Space Telescope, in order of how far their light has come. '
        'The row along the bottom is the carousel’s own scroll markers: each stop, with its distance.')

# label in assets/curated.json, what it is, marker label, distance figure, unit line, light line, source
STOPS = [
    ('Jupiter', 'The largest planet, in Webb’s infrared: the brighter a cloud, the higher it sits.',
     '43 min', '43', 'light-minutes from the Sun', 'Sunlight takes 43 minutes to reach it.', 'NASA'),
    ('Rho Ophiuchi', 'The nearest place to us where stars are being born.',
     '390 ly', '390', 'light-years', 'This light set out 390 years ago.', 'NASA, 12 July 2023'),
    ('Orion Bar', 'A ridge of the Orion Nebula, carved by the light of the young stars beside it.',
     '1,350 ly', '1,350', 'light-years', 'This light set out 1,350 years ago.', 'NASA, 26 June 2023'),
    ('Southern Ring Nebula', 'The shells of gas a dying star has been shedding for thousands of years.',
     '2,500 ly', '2,500', 'light-years', 'This light set out 2,500 years ago.', 'ESA/Webb, 12 July 2022'),
    ('Pillars of Creation', 'Columns of gas and dust in the Eagle Nebula, with new stars forming inside them.',
     '6,500 ly', '6,500', 'light-years', 'This light set out 6,500 years ago.', 'NASA'),
    ('Cosmic Cliffs', 'The edge of a vast cavity in the Carina Nebula, glittering with newborn stars.',
     '7,600 ly', '7,600', 'light-years', 'This light set out 7,600 years ago.', 'NASA'),
    ('Cassiopeia A', 'What is left of a star that exploded, its shell still expanding into space.',
     '11,000 ly', '11,000', 'light-years', 'This light set out 11,000 years ago.', 'NASA, 7 April 2023'),
    ('Cartwheel Galaxy', 'A galaxy set into rings by a collision about 400 million years ago.',
     '500 m ly', '500 million', 'light-years', 'This light set out 500 million years ago.', 'NASA, 2 August 2022'),
    ('Webb\'s First Deep Field', 'A cluster of galaxies as it was 4.6 billion years ago, bending the light of galaxies behind it.',
     '13.1 bn yr', '13.1 billion', 'years of travel', 'Light from one galaxy here travelled 13.1 billion years to reach Webb.', 'NASA, 12 July 2022'),
]

# How each photograph sits in a wide frame: round subjects float whole on black.
# Framed whole, they sit right of centre so the words on the left have their own space.
FRAME = {'Jupiter': ('contain', '72% 50%'), 'Southern Ring Nebula': ('contain', '72% 50%'), 'Cassiopeia A': ('contain', '72% 50%'),
         'Cartwheel Galaxy': ('contain', '72% 50%'), 'Pillars of Creation': ('cover', '50% 40%')}

MATERIAL = 'Material — NASA, ESA, CSA, STScI: images from the James Webb Space Telescope · public domain'

HOW = """.reel { scroll-snap-type: x mandatory; scroll-marker-group: after }
.stop::scroll-marker { content: attr(data-far); background: var(--thumb) }
.stop::scroll-marker:target-current { /* the stop on screen */ }
.reel::scroll-button(right) { content: '→' }   /* and (left) */"""

NOTE = ('Chrome builds the navigation from the scroller itself: one marker per snap stop, a group to hold them, '
        'and buttons that page it. No script tracks which stop is showing; <code>:target-current</code> says so.')


def render(works):
    """The voyage: markup for the full-bleed carousel, from the curated Webb records."""
    by = {w['label']: w for w in works if w['kind'] == 'webb'}
    out = []
    for i, (label, what, short, figure, unit, light, source) in enumerate(STOPS):
        w = by[label]
        ws = sorted(map(int, w['sources']))
        thumb = w['sources'][str(ws[0])]
        loading = 'eager' if i == 0 else 'lazy'
        alt = html.escape(f'{label}, photographed by the James Webb Space Telescope: {what}', quote=True)
        fit, pos = FRAME.get(label, ('cover', '50% 50%'))
        out.append(
            f'<figure class="stop{" whole" if fit == "contain" else ""}" data-far="{short}" style="--thumb:url(\'{thumb}\');--fit:{fit};--pos:{pos}">\n'
            f'  <img src="{w["default"]}" srcset="{w["srcset"]}" sizes="100vw" width="{w["w"]}" height="{w["h"]}" '
            f'alt="{alt}" loading="{loading}" decoding="async"{" fetchpriority=\"high\"" if i == 0 else ""}>\n'
            f'  <figcaption>\n'
            f'    <span class="count">{i + 1:02d} / {len(STOPS):02d}</span>\n'
            f'    <h2>{html.escape(label)}</h2>\n'
            f'    <p class="what">{what}</p>\n'
            f'    <p class="far"><b>{figure}</b> {unit}</p>\n'
            f'    <p class="light">{light}</p>\n'
            f'    <span class="cr">NASA, ESA, CSA, STScI · public domain · distance: {source}</span>\n'
            f'  </figcaption>\n'
            f'</figure>')
    return ('<section class="voyage stage" data-material aria-label="Nine Webb images, from Jupiter outward">\n'
            '<div class="reel" tabindex="0" aria-label="Carousel: use the markers, the arrows or your arrow keys">\n'
            + '\n'.join(out) + '\n</div>\n</section>')
