"""The mark: Melodrama Bold's M in terra on the night ground, cut through the middle by a split.

    python3 build/mark.py

draws it once and writes it three ways: site/favicon.svg (the tab icon; Chrome takes the SVG), site/favicon.ico
(16, 32 and 48 px, for whatever asks for /favicon.ico) and site/apple-touch-icon.png (180 px, full bleed: iOS rounds
the corners itself). The grid is 32 units, so on a 16 px tab at 2x a unit is a device pixel: the M's top and baseline
and both edges of the split sit on whole units, and stay sharp there. The M is the font's own outline in font units
(1000 to the em, cap height 693, advance 632), straight lines only: Melodrama Bold, © Indian Type Foundry, from
Fontshare.
"""
import re
from pathlib import Path
from PIL import Image, ImageDraw

SITE = Path(__file__).resolve().parents[1] / 'site'
M = 'M55 0V693H201L322 351L438 693H577V0H438V652L258 129H256L69 645V0Z'
CAP, TOP, SPLIT = 17, 7, 15         # the M from 7 to 24; the split from 15 to 16, its middle
INK, GROUND, RADIUS = '#D4673F', '#0B0A09', 7.5


def outline():
    """The M's corners on the grid: scaled to CAP, its advance centred (both sidebearings are 55), y turned down."""
    s, x, y, pts = CAP / 693, 0, 0, []
    for op, args in re.findall(r'([MLHV])([^MLHVZ]*)', M):
        n = [float(v) for v in args.split()]
        x, y = n if op in 'ML' else (n[0], y) if op == 'H' else (x, n[0])
        pts.append((16 + (x - 316) * s, TOP + (693 - y) * s))
    return pts


def num(v):
    return f'{v:.2f}'.rstrip('0').rstrip('.')


def svg():
    pts = [(num(x), num(y)) for x, y in outline()]
    d = f'M{pts[0][0]} {pts[0][1]}'
    for (px, py), (x, y) in zip(pts, pts[1:]):
        d += f'V{y}' if x == px else f'H{x}' if y == py else f'L{x} {y}'
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
            '<!-- build/mark.py; the M is Melodrama Bold, © Indian Type Foundry -->'
            f'<rect width="32" height="32" rx="{RADIUS}" fill="{GROUND}"/>'
            f'<path d="{d}Z" fill="{INK}"/>'
            f'<rect y="{SPLIT}" width="32" height="1" fill="{GROUND}"/></svg>\n')


def raster(size, bleed=False, k=16):
    """The mark at size px: drawn k times larger, then each pixel the mean of its k by k block."""
    n = size * k
    u = n / 32
    im = Image.new('RGBA', (n, n))
    d = ImageDraw.Draw(im)
    if bleed:
        d.rectangle((0, 0, n - 1, n - 1), GROUND)
    else:
        d.rounded_rectangle((0, 0, n - 1, n - 1), RADIUS * u, GROUND)
    d.polygon([(x * u, y * u) for x, y in outline()], INK)
    d.rectangle((0, SPLIT * u, n - 1, (SPLIT + 1) * u - 1), GROUND)
    return im.resize((size, size), Image.BOX)


if __name__ == '__main__':
    (SITE / 'favicon.svg').write_text(svg())
    icons = [raster(s) for s in (16, 32, 48)]
    icons[-1].save(SITE / 'favicon.ico', sizes=[im.size for im in icons], append_images=icons[:-1])
    raster(180, bleed=True).convert('RGB').save(SITE / 'apple-touch-icon.png', optimize=True)
    print('mark:', ', '.join(f'{p} {(SITE / p).stat().st_size} B' for p in ('favicon.svg', 'favicon.ico', 'apple-touch-icon.png')))
