"""Scroll-Triggered Count, in full: six of the charts W. E. B. Du Bois and his students at
Atlanta University drew for the Paris Exposition of 1900, a generation after emancipation.
Each plate's figures are set beside it as the plate letters them (year, a band in the
plate's own colour, the figure), the last of them large.

Every figure is text on the page. Each of its digits is also a wheel the stylesheet turns:
a figure waits until the whole of it is on screen, then counts up to its value, once. The
trigger, the count and the wheels are CSS; there is no script. The boards are cut from
their scans by build/cutout.py (assets/cutouts.json).
"""
import html, json, re
from pathlib import Path

TITLE = 'A generation, counted'
LEDE = ('In 1900 W. E. B. Du Bois and his students at Atlanta University drew charts of Black life in Georgia for the '
        'Paris Exposition, a generation after emancipation. Scroll: each figure counts up to its value as it comes '
        'into view — once.')

# label in assets/curated.json; the plate's title as lettered; the years; the plate's heading over its figures, if it
# has one; the figures as printed — (year or what, figure, the colour that keys it on the plate) — the last the one set
# large; the colour keying the rest; the section's ground, ink and large figure; the chart, described
PLATES = [
    dict(label='Slaves and free', title='Slaves and free Negroes.', years='1790–1870', head='Percent of free Negroes',
         figures=[('1790', '1.3%'), ('1800', '1.7%'), ('1810', '1.7%'), ('1820', '1.2%'), ('1830', '0.8%'),
                  ('1840', '0.9%'), ('1850', '0.7%'), ('1860', '0.8%'), ('1870', '100%')],
         key='#AE2943', ground='#1B1A1A', ink='#E4D8CA', hero='#E4D8CA',
         alt='A column black for the enslaved and a thin band of crimson for the free, 1790 to 1860; in 1870 the crimson fills it'),
    dict(label='City and rural', title='City and rural population. 1890.', years='1890', head=None,
         figures=[('In cities of over 10,000 inhabitants', '78,139', '#536F60'),
                  ('In cities from 5,000 to 10,000', '8,025', '#5B71A3'),
                  ('In cities from 2,500 to 5,000', '37,699', '#E6B31E'),
                  ('Living in the country and villages', '734,952', '#BD2F43')],
         key=None, ground='#E4D8CA', ink='#1B1A1A', hero='#B31D37',
         alt='Short lines of green, blue and gold for the cities, then a long crimson spiral for the country and villages'),
    dict(label='Schools', title='Negro children enrolled in the public schools.', years='1860–1897', head=None,
         figures=[('1860', '7'), ('1870', '10,351'), ('1878', '72,655'), ('1884', '110,150'), ('1888', '120,533'),
                  ('1891', '156,836'), ('1897', '180,565')],
         key='#8A9079', ground='#4D5244', ink='#E9DFD0', hero='#E9DFD0',
         alt='Green bars hanging from the top of the sheet, one for each year, each longer than the last'),
    dict(label='Acres', title='Acres of land owned by Negroes in Georgia.', years='1874–1899', head=None,
         figures=[('1874', '338,769'), ('1899', '1,062,223')],
         key='#E9A3AE', ground='#BF2B47', ink='#F2E8DA', hero='#F2E8DA',
         alt='A crimson bar for every year from 1874 to 1899, lengthening down the sheet'),
    dict(label='Furniture', title='Assessed value of household and kitchen furniture owned by Georgia Negroes.',
         years='1875–1899', head=None,
         figures=[('1875', '$21,186', '#DDAEA6'), ('1880', '$498,532', '#A1A4B5'), ('1885', '$736,170', '#BCA58E'),
                  ('1890', '$1,173,624', '#E3B343'), ('1895', '$1,322,694', '#D4CAB8'), ('1899', '$1,434,975', '#C1394D')],
         key=None, ground='#DDAA31', ink='#1B1A1A', hero='#1B1A1A',
         alt='A spiral of coloured arcs, one for each year, the longer the greater'),
    dict(label='Property', title='Assessed valuation of all taxable property owned by Georgia Negroes.',
         years='1875–1899', head=None,
         figures=[('1875', '$5,393,885', '#1B1B1B'), ('1880', '$5,764,293', '#9C8A7C'), ('1885', '$8,153,390', '#35447A'),
                  ('1890', '$12,322,003', '#DAA909'), ('1895', '$12,941,230', '#CDC2AF'), ('1899', '$13,447,423', '#A52339')],
         key=None, ground='#35447A', ink='#ECE3D3', hero='#E3B303',
         alt='Rings of black, tan, blue and gold, with a wedge cut through them for each year'),
]
HEAD = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/anybody/wdth.css">\n'

SOURCE = ('https://en.wikipedia.org/wiki/The_Exhibit_of_American_Negroes', 'The Exhibit of American Negroes')

HOW = """.odo { timeline-trigger: --count view() contain 0% contain 100%;   /* the whole figure on screen… */
        animation: count 3s linear both; animation-trigger: --count play-once }   /* …counts, once */
.odo > span {                                              /* every digit is a wheel */
  --p: pow(10, sibling-count() - sibling-index());          /* its place */
  --pos: mod(max(0, (var(--n) - mod(var(--to), var(--p))) / var(--p)), 10) }"""

NOTE = ('There is no script. The trigger is a view timeline that fires once, when the whole figure is on screen; the '
        'count is one registered number running from 0 to 1. Every digit is a wheel set by that count, divided by its '
        'place and turned to land on its own digit. The count closes on its figure by a power of ten at a time, so the '
        'wheels come to rest one by one from the left, as a counting machine’s do. The figure itself is ordinary text, '
        'as Du Bois lettered it: the wheels are drawn over it.')

MATERIAL = ('Material — W. E. B. Du Bois and Atlanta University, The Georgia Negro: A Social Study, 1900 · '
            'Library of Congress · public domain')

EM = {',': .300, '.': .196, '$': .806, '%': .872}          # Anybody at 150% width; its figures are .841em each


def _cutouts():
    path = Path(__file__).resolve().parents[2] / 'assets/cutouts.json'
    return json.load(open(path, encoding='utf-8')) if path.exists() else {}   # build/cutout.py writes it


def _figure(text):
    """A figure as printed, its digits wheels: the text stays the figure."""
    pre, num, post = re.fullmatch(r'(\D*)([\d.,]+)(\D*)', text).groups()
    digits = re.sub(r'\D', '', num)
    wheels = ''.join(f'<span>{c}</span>' if c.isdigit() else c for c in num)
    return f'{pre}<span class="odo" style="--to:{int(digits)};--k:{len(digits)}">{wheels}</span>{post}'


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'dubois'}
    cuts = _cutouts()
    n = len(PLATES)
    plates = []
    for i, p in enumerate(PLATES, 1):
        w = by[p['label']]
        rows = []
        for j, (what, figure, *colour) in enumerate(p['figures']):
            last = j == len(p['figures']) - 1
            em = f';--em:{sum(EM.get(c, .841) for c in figure):.3f}' if last else ''
            rows.append(f'<div{" class=\"most\"" if last else ""} style="--c:{colour[0] if colour else p["key"]}{em}">'
                        f'<dt>{html.escape(what)}</dt><dd>{_figure(figure)}</dd></div>')
        cut = f';clip-path:{cuts[p["label"]]}' if p['label'] in cuts else ''
        alt = f'Du Bois’s chart “{p["title"].rstrip(".")}”, {p["years"]}: {p["alt"]}'
        plates.append(
            f'<article class="plate {"left" if i % 2 else "right"}" style="--ground:{p["ground"]};--ink:{p["ink"]};--hero:{p["hero"]}" '
            f'aria-labelledby="plate{i}">\n'
            f'  <figure class="board"><img src="{w["default"]}" srcset="{w["srcset"]}" '
            f'sizes="(max-width: 760px) 80vw, min(66svh, 720px)" width="{w["w"]}" height="{w["h"]}" '
            f'style="--ar:{w["w"] / w["h"]:.4f}{cut}" alt="{html.escape(alt, quote=True)}" decoding="async"'
            f'{" fetchpriority=\"high\"" if i == 1 else " loading=\"lazy\""}></figure>\n'
            f'  <div class="figures">\n'
            f'    <p class="no">{i:02d} / {n:02d} · {p["years"]}</p>\n'
            f'    <h2 id="plate{i}">{html.escape(p["title"])}</h2>\n'
            + (f'    <p class="head">{html.escape(p["head"])}</p>\n' if p['head'] else '') +
            f'    <dl>{"".join(rows)}</dl>\n'
            f'  </div>\n'
            f'</article>')
    return ('<section class="georgia stage" data-material aria-label="Six charts by W. E. B. Du Bois, 1900, and their figures">\n'
            + '\n'.join(plates) + '\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'dubois'}
    links = ', '.join(f'<a href="{by[p["label"]]["descurl"]}">{html.escape(p["title"].rstrip("."))}</a>' for p in PLATES)
    return ('Plates — W. E. B. Du Bois and Atlanta University, The Georgia Negro: A Social Study, drawn for the Exhibit of '
            'American Negroes at the Paris Exposition of 1900; Library of Congress, Prints and Photographs Division; '
            f'public domain, via Wikimedia Commons: {links}. The figures are read from the plates. '
            f'Facts — <a href="{SOURCE[0]}">{SOURCE[1]}</a>. The boards are cut from their scans by build/cutout.py.')
