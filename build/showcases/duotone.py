"""Duotone, in full: six of William P. Gottlieb's jazz portraits, 1946–47, printed
as record sleeves in two inks each.

The duotone is exact: the dark ink is the sleeve's ground, and the light ink is
laid over it through a mask made of the photograph's own luminance, so every
tone lands on the line between the two inks. Scrolling in presses each sleeve
from its grey into its inks; a row of radio inputs gives all six one pair
(CSS :has(), no script); resting the pointer lifts the ink off.
"""
import html

TITLE = 'Two inks'
GLOSS = ('Any photograph, whatever it arrived wearing, comes out in the same two inks, so a set of them reads as a set. '
         'Rest the pointer on one to see what it came in as.')
LEDE = ('Six portraits William P. Gottlieb made in New York’s jazz clubs, 1946–47, printed as record sleeves in two inks '
        'each. Choose one pair for all six and see how it makes them a set; rest the pointer on a sleeve to lift the ink.')

# label in assets/curated.json, the club (all in New York) or None, when (as the records give it), dark ink, light ink
SLEEVES = [
    ('Billie Holiday', 'Downbeat', 'February 1947', '#0F1D45', '#A9CFEA'),
    ('Charlie Parker', 'Three Deuces', 'August 1947', '#26100A', '#F08A2C'),
    ('Thelonious Monk', 'Minton’s Playhouse', 'September 1947', '#0F2418', '#D6E36A'),
    ('Sarah Vaughan', 'Café Society', 'August 1946', '#2A0B2D', '#F3A2BE'),
    ('Ella Fitzgerald', None, 'November 1946', '#3A0B0C', '#F1C24F'),
    ('Billy Strayhorn', None, '1946–48', '#0A2A2D', '#EFE4C6'),
]
# one pair for all six: name, dark, light ('own' keeps each sleeve's; 'none' is the photograph as it came)
INKS = [('own', 'Each its own', None, None), ('blue', 'Blue', '#0F1D45', '#A9CFEA'),
        ('orange', 'Orange', '#1A120E', '#F08A2C'), ('terra', 'Terracotta', '#1D1814', '#D4673F'),
        ('none', 'No ink', '#000000', '#FFFFFF')]

# the one-pair-for-all rules, written from INKS so the pairs live in one place
HEAD = ('<style>' + ''.join(f'.duo:has(#ink-{k}:checked) .sleeve{{--dark:{a};--light:{b}}}' for k, _, a, b in INKS if a)
        + '</style>\n')

HOW = """.sleeve       { background: var(--dark) }            /* ink one: the ground */
.sleeve .ink  { background: var(--light);              /* ink two, through the photograph */
                mask: var(--src) center / cover luminance }
/* each tone lands between the inks: dark + v × (light − dark) */
.duo:has(#ink-blue:checked) .sleeve { --dark: …; --light: … }"""

NOTE = ('A true duotone maps every grey onto the line between two inks. Here the dark ink is the ground and the light ink '
        'shows through a mask made of the photograph’s own luminance: bright tones let through more of it, dark ones less. '
        'Both inks are registered colours, so choosing a pair eases every sleeve into it.')

MATERIAL = 'Material — William P. Gottlieb, jazz portraits, 1946–47, Library of Congress · public domain'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'gottlieb'}
    choices = ''.join(f'<input type="radio" name="ink" id="ink-{k}" value="{k}"{" checked" if k == "own" else ""}>'
                      f'<label for="ink-{k}" style="{f"--a:{a};--b:{b}" if a else ""}"><i></i><span>{html.escape(n)}</span></label>'
                      for k, n, a, b in INKS)
    sleeves = []
    for i, (label, club, when, dark, light) in enumerate(SLEEVES):
        w = by[label]
        src = w['sources']['960']
        where = f'{club} · {when}' if club else f'New York · {when}'
        alt = f'{label}, photographed by William P. Gottlieb' + (f' at {club}' if club else '') + f', New York, {when}'
        sleeves.append(
            f'<figure class="sleeve" style="--i:{i};--own-dark:{dark};--own-light:{light};--src:url(\'{src}\')">\n'
            f'  <div class="print"><img src="{src}" width="{w["w"]}" height="{w["h"]}" '
            f'alt="{html.escape(alt, quote=True)}" '
            f'decoding="async"{" loading=\"lazy\"" if i > 2 else ""}><div class="ink" aria-hidden="true"></div></div>\n'
            f'  <figcaption><b>{html.escape(label)}</b><span>{html.escape(where)}</span></figcaption>\n'
            f'</figure>')
    return ('<section class="duo stage" data-material aria-label="Six jazz portraits printed in two inks">\n'
            f'<fieldset class="inks"><legend>One pair for all six</legend>{choices}</fieldset>\n'
            '<div class="sleeves">\n' + '\n'.join(sleeves) + '\n</div>\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'gottlieb'}
    links = ', '.join(f'<a href="{by[s[0]]["descurl"]}">{html.escape(s[0])}</a>' for s in SLEEVES)
    return ('Photographs — William P. Gottlieb, 1946–47, from the William P. Gottlieb Collection at the Library of Congress, '
            f'which at his wish entered the public domain in 2010; via Wikimedia Commons: {links}.')
