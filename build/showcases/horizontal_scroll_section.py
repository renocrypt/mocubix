"""Horizontal Scroll Section, in full: the last scenes of the Bayeux Tapestry, from Duke William
showing his face to his men to the end of the cloth. You scroll down; the tapestry travels
sideways, as it reads. The section is exactly as tall as the strip is wider than the screen,
so the last stitch arrives as the scroll runs out.

The strip is four overlapping photographs of the tapestry laid end to end by
`build/register.py stitch` (assets/registration.json): each is placed by a shift, a turn and a
scale and cut at the middle of its overlap, as Kinetic Drag places the Tabula's sheets. CROP is
the window on that strip, measured by hand: the embroidery between the backing above (where the
museum's scene numbers are pencilled) and the lining below, up to where the cloth ends.
"""
import html, json
from pathlib import Path

TITLE = 'The end of the tapestry'
LEDE = ('The last scenes of the Bayeux Tapestry, embroidered in England in the years after the Conquest: Duke William '
        'lifts his helmet to show his men he is alive, the English fall around their king, Harold is killed, and the '
        'English turn and run. Scroll down: the cloth travels sideways, the way it is read.')

SHEETS = ['Scene 55', 'Scene 56', 'Scene 57', 'Scene 58']   # labels in assets/curated.json, left to right
BAND = (0, 1)          # a textile: the whole height of every scan is the band (for register.py)
CROP = (8, 184, 5295, 606)   # the window on the stitched strip, in its units (the first sheet at 1920px)

# where each titulus is embroidered (x on the strip), the Latin as it is stitched, and its English
TITULI = [
    (40, '… BACULU[M] TENENS CONFORTAT PUEROS', 'Bishop Odo, holding a club, gives strength to the boys'),
    (476, 'HIC EST WILLEL[MUS] DUX · E[USTA]TIUS', 'Here is Duke William · Eustace'),
    (862, 'HIC FRANCI PUGNANT ET CECIDERUNT QUI ERANT CUM HAROLDO',
     'Here the French do battle, and those who were with Harold fell'),
    (2930, 'HIC HAROLD REX INTERFECTUS EST', 'Here King Harold was slain'),
    (4200, 'ET FUGA VERTERUNT ANGLI',
     'And the English have turned in flight — words said to have been added shortly before 1814'),
]
END = 'Here the cloth ends. The rest has been missing from time immemorial.'
SOURCES = [('https://en.wikipedia.org/wiki/Bayeux_Tapestry', 'Bayeux Tapestry'),
           ('https://en.wikipedia.org/wiki/Bayeux_Tapestry_tituli', 'Bayeux Tapestry tituli')]

HOW = """.run { height: calc(100svh + var(--travel)); view-timeline: --run }  /* as much scroll as the cloth is long */
.frame { position: sticky; top: 0; container-type: inline-size }     /* the view holds still… */
.track { animation: pan linear both; animation-timeline: --run;
         animation-range: contain 0% contain 100% }                   /* …while the cloth moves */
@keyframes pan { to { translate: calc(100cqw - 100%) 0 } }           /* until its end meets the frame's */
/* --travel: the strip's width at this height, less the screen's */"""

NOTE = ('Down becomes across. The section is exactly as tall as the strip is wider than the screen, measured from the '
        'cloth and not guessed, so the last stitch arrives as the scroll runs out. The strip is four overlapping '
        'photographs of the tapestry, joined where the embroidery in one carries on in the next.')

MATERIAL = 'Material — the Bayeux Tapestry, 11th century, Bayeux · public domain'


def _layout():
    return json.load(open(Path(__file__).resolve().parents[2] / 'assets/registration.json'))['stitch:horizontal_scroll_section']


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'bayeux'}
    lay = _layout()
    cx0, cy0, cx1, cy1 = CROP
    W, H = cx1 - cx0, cy1 - cy0
    sheets = []
    for k, sh in enumerate(lay['sheets']):
        w = by[sh['label']]
        x0, y0, x1, y1 = sh['clip']
        style = (f'--iw:{sh["w"]};--ih:{sh["h"]};--x:{sh["tx"] - cx0:.1f};--y:{sh["ty"] - cy0:.1f};--r:{sh["rot"]}deg;'
                 f'--s:{sh["s"]};--ct:{y0};--cr:{sh["w"] - x1:.1f};--cb:{sh["h"] - y1:.1f};--cl:{x0}')
        a = sh['w'] * sh['s'] / H                          # the sheet's width on screen, per unit of strip height
        # all eager: a lazy image waits until it is inside the frame, and would arrive visibly late
        sheets.append(f'<img class="sheet" src="{w["sources"]["1920"]}" srcset="{w["srcset"]}" '
                      f'sizes="(max-width: 760px) min({a * 50:.0f}vh, {a * 460:.0f}px), min({a * 58:.0f}vh, {a * 640:.0f}px)" '
                      f'width="{w["w"]}" height="{w["h"]}" alt="" '
                      f'decoding="async"{" fetchpriority=\"low\"" if k > 1 else ""} style="{style}">')
    tituli = ''.join(f'<li style="--tx:{x}"><b lang="la">{html.escape(la)}</b><span>{html.escape(en)}</span></li>'
                     for x, la, en in TITULI)
    return ('<section class="bayeux stage" data-material aria-label="The last scenes of the Bayeux Tapestry, travelling sideways as you scroll">\n'
            f'<div class="run" style="--mw:{W};--mh:{H}">\n'
            '  <div class="frame">\n'
            '    <p class="where">The Bayeux Tapestry · the Battle of Hastings, 14 October 1066</p>\n'
            '    <div class="track">\n'
            f'      <div class="strip" role="img" aria-label="The last scenes of the Bayeux Tapestry: Duke William lifts his '
            f'helmet among his knights; English and French fall; King Harold is struck down; the English flee on foot and '
            f'on horseback; the cloth ends">{"".join(sheets)}</div>\n'
            f'      <ol class="tituli">{tituli}<li class="end" style="--tx:{W}"><span>{html.escape(END)}</span></li></ol>\n'
            '    </div>\n'
            '    <div class="along" aria-hidden="true"></div>\n'
            '  </div>\n'
            '</div>\n'
            '</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'bayeux'}
    links = ', '.join(f'<a href="{by[s]["descurl"]}">{s.lower()}</a>' for s in SHEETS)
    return ('Tapestry — the Bayeux Tapestry, 11th century, Bayeux Museum; digitised by the Université de Caen '
            'Normandie, the CNRS and ENSICAEN from the 2017 photographic campaign of La Fabrique de patrimoines en '
            f'Normandie; public domain, via Wikimedia Commons: {links}, joined end to end by build/register.py. '
            'Tituli, translations and facts — ' + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
