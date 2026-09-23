"""Path Drawing, in full: Charles Joseph Minard's map of the French army's losses in Russia, 1812-13 (1869).

The bands are Minard's own ink, and they draw themselves as you scroll. Each band starts veiled: a stroke of
the paper's colour over it, blended with `lighten`, so only ink is lifted (the band and its figures turn to a
faint ghost) and the paper is untouched. A pen, a stroke-dashoffset on the same line in the veil's mask,
takes the veil away. The lines were followed on the scan by build/trace.py (assets/tracings.json); the rose
band going in is timed by distance, the black band coming out by Minard's own dates in his temperature table,
and the thermometer draws itself in step with it: each dated reading is tied to a place on the retreat by one
of his thin vertical lines.
"""
import html, json, math
from pathlib import Path

TITLE = 'The march, drawn again'
GLOSS = ('The line draws itself as you arrive, as though someone were tracing it in front of you.')
LEDE = ('In 1869 Charles Joseph Minard drew the French army’s march on Moscow in 1812 as a band as wide as the army: '
        'rose going in, black coming out, and under it the cold. Scroll, and his bands draw themselves again.')

# the lines to follow, read at 1920px wide: rose is the army going in, ink the army coming out (and the thermometer)
TRACE = dict(label='Campagne de Russie', width=1920,
             inks=dict(rose=dict(a=(0.018, 1), L=(0.5, 0.8), merge=24), ink=dict(L=(0, 0.42))),
             lines=[
                 dict(name='corps-out', ink='rose', start=(267, 1098), axis='y', step=-2, end=985, window=8, maxrun=20),
                 dict(name='advance', ink='rose', start=(180, 1203), axis='x', step=2, end=1790, window=70, maxrun=400),
                 dict(name='branch', ink='rose', start=(781, 1054), axis='x', step=-2, end=400, window=14, maxrun=60),
                 dict(name='descent', ink='ink', start=(1783, 915), axis='y', step=2, end=1082, window=16, maxrun=45),
                 dict(name='retreat', ink='ink', start=(1768, 1084), axis='x', step=-2, end=190, window=12, maxrun=45, gap=12),
                 dict(name='polotzk', ink='ink', start=(805, 1152), axis='y', step=2, end=1290, window=10, maxrun=20,
                      before=[(778, 1054), (783, 1078)], hidden=12),
                 dict(name='corps-back', ink='ink', start=(251, 1104), axis='y', step=-2, end=983, window=8, maxrun=12),
                 # below the rose band the 6,000 come down to the black band at Kowno: a short stub, by its vertices
                 dict(name='corps-join', points=[(239, 1258), (239, 1275)], hidden=5),
                 # the thermometer, by its vertices (the table's rulings cross it): 0° at y 1452, 3.53px a degree Réaumur
                 dict(name='cold', points=[(1775, 1452), (1324, 1486.5), (1162.5, 1526.5), (850, 1492.5), (738.5, 1523.5),
                                           (638, 1539), (565, 1558), (360, 1544)], hidden=4),
             ],
             # the bands' own outlines, for their veils: rose with the figures written on it closed over, black with
             # letters and rivers opened away (the thinnest miles of the retreat go with them; strokes veil those)
             areas=[dict(name='rose', ink='rose', box=(80, 860, 1900, 1400), close=7, open=3),
                    dict(name='black', ink='ink', box=(80, 860, 1900, 1400), open=5)])
CROP = (40, 740, 1880, 1600)            # the map, its title and the table, at 1920px wide
VEIL = '#CCBFAA'                         # the paper's median beside the bands: lighten lifts their ink to it
VEIL_TABLE = '#BEB19D'                   # the temperature table's paper is darker (median #BEB19D)

# Minard's temperature table: the x (at 1920px) of each reading's vertical line, the reading, and its date as
# printed; days count from 18 October. The −11° has no date on the map; its day is placed between its neighbours.
READINGS = [(1775, 'Zéro', '18 October', 0), (1324, '−9°', '9 November', 22), (1162.5, '−21°', '14 November', 27),
            (850, '−11°', None, None), (738.5, '−20°', '28 November', 41), (638, '−24°', '1 December', 44),
            (565, '−30°', '6 December', 49), (360, '−26°', '7 December', 50)]
# the figures written along the bands, where they are written (x at 1920px, read against the town names on the
# scan), in the order the pen meets them, and the stretch each is written on
GOING = [(200, 422000, 'Kowno'), (311, 400000, 'Kowno → Wilna'), (983, 175000, 'Witebsk → Smolensk'),
         (1172, 145000, 'Smolensk'), (1517, 127100, 'Chjat → Mojaisk'), (1600, 100000, 'Mojaisk'), (1733, 100000, 'Moscou')]
COMING = [(1783, 100000, 'Moscou'), (1665, 96000, 'Malo-jarosewli → Mojaisk'), (1500, 87000, 'Mojaisk → Wizma'),
          (1380, 55000, 'Wizma → Dorogobouge'), (1255, 37000, 'Dorogobouge → Smolensk'), (1075, 24000, 'Smolensk → Orscha'),
          (917, 20000, 'Orscha → Bobr'), (808, 50000, 'Bobr → Studienska'), (680, 28000, 'Studienska → Molodezno'),
          (533, 12000, 'Molodezno → Smorgoni'), (422, 14000, 'Smorgoni → Wilna'), (360, 8000, 'Wilna'),
          (261, 4000, 'Wilna → Kowno'), (217, 10000, 'Kowno')]
PHASES = (0.03, 0.45, 0.49, 0.93, 0.97)  # going in, in Moscow, coming out (18 Oct–7 Dec), the last miles to the Niemen
SOURCES = [('https://en.wikipedia.org/wiki/Charles_Joseph_Minard', 'Charles Joseph Minard'),
           ('https://en.wikipedia.org/wiki/French_invasion_of_Russia', 'French invasion of Russia')]

HOW = """.veil { background: #BAAE99; mix-blend-mode: lighten; mask: url(#veil-advance) }  /* lifts only the ink */
<mask id="veil-advance"> <path d="…" stroke="#fff"/>              <!-- the band, veiled -->
  <path class="pen" d="…" stroke="#000" pathLength="1"/> </mask>  <!-- the pen takes the veil away -->
.pen { stroke-dasharray: 1; animation: draw linear both; animation-timeline: --march }
@keyframes draw { from { stroke-dashoffset: 1 } to { stroke-dashoffset: 0 } }"""

NOTE = ('Nothing is redrawn: the bands are Minard’s lithograph. Each starts under a veil the colour of the paper, '
        'blended so that it lifts only ink, and a pen, one stroke-dashoffset in the veil’s mask, takes the veil away '
        'along the line. The black band keeps his calendar: the dates in his table of the cold, each tied to a place '
        'on the retreat by one of his thin vertical lines, set its pace, and the thermometer draws itself in step. '
        'Étienne-Jules Marey praised the map’s “brutal eloquence, which seems to defy the pen of the historian”.')

MATERIAL = ('Material — Charles Joseph Minard, Carte figurative des pertes successives en hommes de l’Armée Française '
            'dans la campagne de Russie 1812–1813, 1869 · Bibliothèque nationale de France · public domain')


def _data():
    path = Path(__file__).resolve().parents[2] / 'assets/tracings.json'
    return json.load(open(path, encoding='utf-8')).get('path_drawing') if path.exists() else None


def _lines(data):
    W = TRACE['width']
    out = {k: ([(x * W, y * W) for x, y in v['points']], [w * W for w in v['widths']]) for k, v in data['lines'].items()}
    for k in ('branch', 'corps-back'):                  # followed against the march: the pen draws them the other way
        out[k] = (out[k][0][::-1], out[k][1][::-1])
    down = out.pop('descent')                            # coming out: down from Moscow, then west (the first steps
    back = out.pop('retreat')                            # of the retreat overlap the descent)
    keep = [i for i, p in enumerate(back[0]) if p[0] < down[0][-1][0]]
    out['out'] = (down[0] + [back[0][i] for i in keep], down[1] + [back[1][i] for i in keep])
    return out


def _cum(pts):
    out = [0.0]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        out.append(out[-1] + math.hypot(x1 - x0, y1 - y0))
    return out


def _at_x(pts, x, skip=0):
    """The fraction of the way along pts where it first reaches x (walking from vertex `skip`)."""
    cum = _cum(pts)
    for i in range(skip, len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        if (x0 - x) * (x1 - x) <= 0 and x0 != x1:
            f = (x - x0) / (x1 - x0)
            return (cum[i] + f * (cum[i + 1] - cum[i])) / cum[-1]
    return 1.0 if abs(pts[-1][0] - x) < abs(pts[0][0] - x) else 0.0


def _x_at(pts, s):
    """The x at the fraction s of the way along pts."""
    cum = _cum(pts)
    d = s * cum[-1]
    for i in range(len(pts) - 1):
        if cum[i] <= d <= cum[i + 1]:
            f = (d - cum[i]) / ((cum[i + 1] - cum[i]) or 1)
            return pts[i][0] + f * (pts[i + 1][0] - pts[i][0])
    return pts[-1][0]


def _plan():
    """Each route's progress as keyframes on the scroll, and when each figure and reading is met."""
    data = _data()
    if not data:
        return None
    L = _lines(data)
    a0, a1, r0, r1, end = PHASES
    adv, out, cold = L['advance'][0], L['out'][0], L['cold'][0]
    t_adv = lambda s: a0 + s * (a1 - a0)
    keys = {'advance': [(a0, 0), (a1, 1)]}
    lenA = _cum(adv)[-1]
    for name in ('corps-out', 'branch'):                 # each leaves the main band as its pen passes, at its pace
        pts = L[name][0]
        start = t_adv(_at_x(adv, pts[0][0]))
        keys[name] = [(start, 0), (min(a1, start + _cum(pts)[-1] / lenA * (a1 - a0)), 1)]
    # coming out keeps Minard's calendar: a reading's day sets when the band reaches its vertical line; the
    # undated reading takes the day that its place between its neighbours gives it
    days = [d for *_, d in READINGS]
    for i, (x, _, _, d) in enumerate(READINGS):
        if d is None:
            (xp, dp), (xn, dn) = (READINGS[i - 1][0], days[i - 1]), (READINGS[i + 1][0], READINGS[i + 1][3])
            days[i] = dp + (xp - x) / (xp - xn) * (dn - dp)
    t_day = lambda d: r0 + d / 50 * (r1 - r0)
    skip = 6                                             # the descent's vertices: look for x on the westward run
    keys['out'] = [(t_day(d), 0 if i == 0 else _at_x(out, x, skip)) for i, ((x, *_), d) in enumerate(zip(READINGS, days))]
    keys['out'].append((end, 1))
    ccum = _cum(cold)
    keys['cold'] = [(t_day(d), ccum[i] / ccum[-1]) for i, d in enumerate(days)]

    def t_out(x):                                        # when the black band reaches x
        s = _at_x(out, x, skip)
        for (ta, sa), (tb, sb) in zip(keys['out'], keys['out'][1:]):
            if sa <= s <= sb:
                return ta + (s - sa) / ((sb - sa) or 1) * (tb - ta)
        return end
    bobr = t_out(L['polotzk'][0][-1][0])
    keys['polotzk'] = [(bobr - 0.05, 0), (bobr, 1)]
    keys['corps-back'] = [(end - 0.05, 0), (end - 0.012, 1)]
    keys['corps-join'] = [(end - 0.012, 0), (end, 1)]
    # where the pens are, for a phone's view to follow: the rose pen going in, the black pen coming out
    x0, _, x1, _ = CROP
    fx = [(t_adv(k / 40), _x_at(adv, k / 40)) for k in range(41)]
    fx += [(t, _x_at(out, s)) for t, s in keys['out']]
    fx += [(t_out(x), x) for x in range(1700, 200, -60)]
    fx = sorted((t, (x - x0) / (x1 - x0)) for t, x in fx)
    going = [(-1 if i == 0 else t_adv(_at_x(adv, x)), f'{n:,}', place) for i, (x, n, place) in enumerate(GOING)]
    coming = [(max(r0, t_out(x)), f'{n:,}', place) for x, n, place in COMING]
    dated = [(t_day(d), reading, date) for (x, reading, date, _), d in zip(READINGS, days)]
    return dict(data=data, lines=L, keys=keys, fx=fx, going=going, coming=coming, dated=dated)


def _groups(pts, widths):
    """A pen for each stretch of like width (a new one where the band narrows by a third), each starting one vertex
    back so its round join covers the bend: (points, width, from, to) as fractions of the way along."""
    cum = _cum(pts)
    total = cum[-1]
    out, start, top = [], 0, widths[0]
    for i in range(1, len(pts)):
        if widths[i] < top * 0.67 and i - start > 2:
            out.append((start, i, top))
            start, top = i - 1, widths[i]
        top = max(top, widths[i])
    out.append((start, len(pts) - 1, top))
    return [(pts[a:b + 1], w, cum[a] / total, cum[b] / total) for a, b, w in out]


def _css(plan):
    names = list(plan['keys'])
    css = [''.join(f'@property --p-{n}{{syntax:"<number>";inherits:true;initial-value:0}}' for n in names),
           '@property --fx{syntax:"<number>";inherits:true;initial-value:0}',
           '.frame{animation-name:progress,' + ','.join(f'p-{n}' for n in names) + ',follow}']
    for n, ks in plan['keys'].items():
        css.append(f'@keyframes p-{n}{{0%{{--p-{n}:0}}' + ''.join(f'{t * 100:.3f}%{{--p-{n}:{s:.5f}}}' for t, s in ks)
                   + f'100%{{--p-{n}:1}}}}')
    css.append('@keyframes follow{' + ''.join(f'{t * 100:.3f}%{{--fx:{x:.4f}}}' for t, x in plan['fx']) + '}')
    return '<style>' + ''.join(css) + '</style>\n'


PLAN = _plan()
HEAD = _css(PLAN) if PLAN else ''


def _svg(plan):
    """Three veils (rose, black, the thermometer), each a mask: the veil in white, then its pens in black."""
    x0, y0, x1, y1 = CROP
    W = TRACE['width']
    L = plan['lines']
    at = lambda pts: 'M' + 'L'.join(f'{x - x0:.1f} {y - y0:.1f}' for x, y in pts)
    area = lambda name: at([(x * W, y * W) for x, y in plan['data']['areas'][name]]) + 'Z'

    west = min(x for x, _ in plan['data']['areas']['black']) * W

    def thin(pts, widths, beyond=None):                  # the stretches too thin to survive the band's outline
        return ''.join(f'<path d="{at([a, b])}" stroke-width="{min(max(wa, wb), 12) + 5:.1f}"/>'
                       for a, b, wa, wb in zip(pts, pts[1:], widths, widths[1:])
                       if beyond is None or min(a[0], b[0]) < beyond)

    def reach(pts, widths, at_end):                       # a pen runs on past the end of its line, far enough that
        if at_end:                                        # its square end clears a band cut obliquely: along the
            pts, widths = pts[::-1], widths[::-1]         # line's way over its last 60px, by half its widest run
        cum = _cum(pts)                                   # within 80px of the end
        by = max(w for w, c in zip(widths, cum) if c <= 80) / 2 + 6
        j = next((i for i, c in enumerate(cum) if c >= 60), len(pts) - 1)
        (xa, ya), (xb, yb) = pts[0], pts[j]
        d = math.hypot(xb - xa, yb - ya) or 1
        tip = (xa - (xb - xa) / d * by, ya - (yb - ya) / d * by)
        return [tip] + pts if not at_end else ([tip] + pts)[::-1]

    def pens(name):
        pts, widths = L[name]
        groups = _groups(pts, widths) if name in ('advance', 'out') else [(pts, max(widths), 0, 1)]
        out = []
        for k, (g, w, a, b) in enumerate(groups):
            if k == 0:
                g = reach(g, widths, False)
            if k == len(groups) - 1:
                g = reach(g, widths, True)
            out.append(f'<path class="pen" d="{at(g)}" stroke-width="{w + 20:.1f}" pathLength="1" '
                       f'style="--p:var(--p-{name});--a:{a:.4f};--b:{b:.4f}"/>')
        return ''.join(out)
    polotzk = L['polotzk']
    veils = {
        'rose': (f'<path d="{area("rose")}"/>', ('advance', 'branch', 'corps-out')),
        'black': (f'<path d="{area("black")}"/><g fill="none" stroke-linecap="round">{thin(*L["out"], beyond=west + 10)}'
                  f'{thin(polotzk[0][:2], [12, 12])}{thin(*L["corps-back"])}{thin(*L["corps-join"])}</g>',
                  ('out', 'polotzk', 'corps-back', 'corps-join')),
        # the thermometer's line has its hatching below it: the veil sits a little low to cover both
        'cold': (f'<path d="{at([(x, y + 2) for x, y in L["cold"][0]])}" fill="none" stroke-width="9"/>', ('cold',)),
    }
    masks = ''.join(
        f'<mask id="veil-{v}" maskContentUnits="objectBoundingBox">'
        f'<g transform="scale({1 / (x1 - x0):.7f} {1 / (y1 - y0):.7f})" stroke="#fff" fill="#fff">{shape}</g>'
        f'<g transform="scale({1 / (x1 - x0):.7f} {1 / (y1 - y0):.7f})" stroke="#000" fill="none" '
        f'stroke-linejoin="round">{"".join(pens(n) for n in routes)}</g></mask>'
        for v, (shape, routes) in veils.items())
    return '<svg class="masks" width="0" height="0" aria-hidden="true"><defs>' + masks + '</defs></svg>'


def render(works):
    w = next(w for w in works if w['kind'] == 'minard')
    x0, y0, x1, y1 = CROP
    W = TRACE['width']
    H = W * w['h'] / w['w']
    cw, ch = x1 - x0, y1 - y0
    plan = PLAN
    a0, a1, r0, r1, end = PHASES
    veils = ''.join(f'<div class="veil" style="mask:url(#veil-{n});--veil:{c}"></div>'
                    for n, c in (('rose', VEIL), ('black', VEIL), ('cold', VEIL_TABLE))) if plan else ''

    def rows(items, until):
        spans = list(zip(items, [b[0] for b in items[1:]] + [until]))
        return ''.join(f'<li style="--from:{a[0]:.4f};--to:{b:.4f}"><b>{a[1]}</b> <span>{html.escape(a[2])}</span></li>'
                       for a, b in spans)
    alt = ('Minard’s map of the French army in Russia, 1812–13: a rose band as wide as the army runs from the Niemen at '
           'Kowno to Moscow, narrowing from 422,000 men to 100,000; a black band brings the army back, narrowing to '
           '10,000; beneath, a table of the temperatures on the retreat, falling to −30° Réaumur')
    going = rows(plan['going'], r0) if plan else ''
    coming = rows(plan['coming'], 2) if plan else ''
    dated = ''.join(f'<li style="--from:{t:.4f};--to:{b[0]:.4f}"><b>{r}</b> <span>{d or ""}</span></li>'
                    for (t, r, d), b in zip(plan['dated'], plan['dated'][1:] + [(2,)])) if plan else ''
    return (
        '<section class="march stage" data-material aria-label="Minard’s map of the campaign in Russia, drawing itself">\n'
        '<div class="run">\n'
        '  <div class="frame">\n'
        f'    <figure class="map" style="--ar:{cw / ch:.5f};--iw:{W / cw:.5f};--ix:{-x0 / cw:.5f};--iy:{-y0 / ch:.5f};--ih:{H / ch:.5f}">\n'
        f'      <img src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 260vw, 106vw" '
        f'width="{w["w"]}" height="{w["h"]}" alt="{html.escape(alt, quote=True)}" decoding="async" fetchpriority="high">\n'
        f'      {veils}\n'
        f'      {_svg(plan) if plan else ""}\n'
        '    </figure>\n'
        '    <div class="ledger">\n'
        f'      <p class="phase"><span style="--from:-1;--to:{a1:.3f}">Going in, from 24 June 1812 · rose</span>'
        f'<span style="--from:{a1:.3f};--to:{r0:.3f}">In Moscow, from 14 September</span>'
        f'<span style="--from:{r0:.3f};--to:2">Coming out · black · the cold, in degrees Réaumur</span></p>\n'
        f'      <ol class="men" aria-label="The men, as the band is written">{going}{coming}</ol>\n'
        f'      <ol class="cold" aria-label="The cold, as the table is written">{dated}</ol>\n'
        '    </div>\n'
        '  </div>\n'
        '</div>\n'
        '</section>')


def credit(works):
    w = next(w for w in works if w['kind'] == 'minard')
    return (f'Map — <a href="{w["descurl"]}">Carte figurative des pertes successives en hommes de l’Armée Française dans '
            'la campagne de Russie 1812–1813</a>, drawn by Charles Joseph Minard, Paris, 20 November 1869 (printed with '
            'its companion, Hannibal’s march); Bibliothèque nationale de France, via Gallica; public domain, via '
            'Wikimedia Commons. The figures, places and readings are Minard’s, as written on the map. Facts — '
            + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
