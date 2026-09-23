"""Take a picture's palette: the ground, ink and accent a page can wear to stand in its light.

    python3 build/palette.py threshold_flip      # the labels in the showcase's PAINTINGS

Writes assets/palettes.json, keyed by label. Every colour is chosen in OKLab from the
picture's own colours (a median cut of its 500px copy): the ground is its most common
colour, its lightness moved out of the middle band where no type reads well on it; the
accent is its most colourful colour, moved in lightness until it stands off the ground;
the ink is the ground's own hue at the far end of lightness.
"""
import io, json, math, sys, time, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
UA = {'User-Agent': 'Mocubix/1.0 (https://github.com/renocrypt/mocubix)'}
works = {w['label']: w for w in json.load(open(ROOT / 'assets/curated.json', encoding='utf-8'))}


def lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def gam(c):
    c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return round(min(max(c, 0), 1) * 255)


def oklab(rgb):
    r, g, b = (lin(v) for v in rgb)
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def srgb(L, a, b):
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def to_hex(L, C, h):
    """An OKLCh colour as sRGB hex, its chroma reduced until it fits the gamut."""
    for _ in range(40):
        rgb = srgb(L, C * math.cos(h), C * math.sin(h))
        if all(-1e-4 <= v <= 1 + 1e-4 for v in rgb):
            break
        C *= 0.93
    return '#%02X%02X%02X' % tuple(gam(v) for v in rgb)


def colours(label):
    url = works[label]['sources']['500']
    for wait in (0, 5, 15, 30):
        time.sleep(wait)
        try:
            im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()))
            break
        except Exception:
            pass
    q = im.convert('RGB').quantize(colors=10, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    out = []
    for count, i in sorted(q.getcolors(), reverse=True):
        L, a, b = oklab(pal[3 * i:3 * i + 3])
        out.append((count, L, math.hypot(a, b), math.atan2(b, a)))
    return out


def palette(label):
    cs = colours(label)
    total = sum(c[0] for c in cs)
    _, L, C, h = cs[0]                                   # the most common colour
    L = min(L, 0.36) if L < 0.56 else max(L, 0.76)       # out of the band no type reads on
    ground = (L, min(C, 0.09), h)
    dark = L < 0.5
    # the most colourful colour that covers a real share of the picture
    _, aL, aC, ah = max((c for c in cs if c[0] > total * 0.03), key=lambda c: c[2])
    aL = max(aL, 0.74) if dark else min(aL, 0.5)
    ink = (0.96 if dark else 0.2, 0.02, h)
    return {'ground': to_hex(*ground), 'accent': to_hex(aL, max(aC, 0.08), ah), 'ink': to_hex(*ink),
            'mid': to_hex((ink[0] * 0.72 + L * 0.28), 0.025, h), 'dark': dark}


def main(name):
    sys.path.insert(0, str(ROOT / 'build' / 'showcases'))
    showcase = __import__(name)
    path = ROOT / 'assets/palettes.json'
    out = json.load(open(path)) if path.exists() else {}
    for label in (p[0] for p in showcase.PAINTINGS):
        out[label] = palette(label)
        print(f'  {label}: {out[label]}')
    json.dump(out, open(path, 'w'), indent=1, ensure_ascii=False)
    print(f'wrote {len(showcase.PAINTINGS)} palettes into {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main(sys.argv[1])
