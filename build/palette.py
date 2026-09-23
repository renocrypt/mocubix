"""Take a picture's palette: the ground, ink and accent a page can wear to stand in its light.

    python3 build/palette.py threshold_flip      # the labels in the showcase's PAINTINGS
    python3 build/palette.py ring gamut_arc      # the sectors of the colour circle in the showcase's RING

Writes assets/palettes.json, keyed by label. Every colour is chosen in OKLab from the
picture's own colours (a median cut of its 500px copy): the ground is its most common
colour, its lightness moved out of the middle band where no type reads well on it; the
accent is its most colourful colour, moved in lightness until it stands off the ground;
the ink is the ground's own hue at the far end of lightness.

A ring is a printed colour circle: RING gives its picture, its centre and the radii of its coloured band (as
fractions of the picture's width, the centre's y of its height), how many sectors it has and the screen angle of
the first sector's centre (degrees clockwise from three o'clock; the sectors run anticlockwise). Each sector's
colour is the median of its middle, clear of the lines between sectors, written as 'ring:<label>'.
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


def fetch(label, width='500'):
    url = works[label]['sources'][width]
    for wait in (0, 5, 15, 30, 45):
        time.sleep(wait)
        try:
            return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()))
        except Exception:
            pass
    raise SystemExit(f'could not fetch {label}')


def colours(label):
    im = fetch(label)
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


def ring(name):
    sys.path.insert(0, str(ROOT / 'build' / 'showcases'))
    r = __import__(name).RING
    width = max(works[r['label']]['sources'], key=int)
    im = fetch(r['label'], width).convert('RGB')
    W, H = im.size
    px = im.load()
    cx, cy = r['centre'][0] * W, r['centre'][1] * H
    r0, r1 = r['radii'][0] * W, r['radii'][1] * W
    step = 360 / r['sectors']
    out = []
    for k in range(r['sectors']):
        th0 = r['first'] - k * step
        got = [px[int(cx + rr * math.cos(math.radians(th0 + d))), int(cy + rr * math.sin(math.radians(th0 + d)))]
               for d in [step * f / 10 for f in range(-3, 4)]
               for rr in range(int(r0 + (r1 - r0) * .15), int(r1 - (r1 - r0) * .1), 4)]
        rgb = [sorted(c[i] for c in got)[len(got) // 2] for i in range(3)]
        L, a, b = oklab(rgb)
        out.append({'L': round(L, 4), 'C': round(math.hypot(a, b), 4), 'h': round(math.degrees(math.atan2(b, a)) % 360, 2),
                    'print': '#%02X%02X%02X' % tuple(rgb)})
    path = ROOT / 'assets/palettes.json'
    data = json.load(open(path)) if path.exists() else {}
    data[f'ring:{r["label"]}'] = out
    json.dump(data, open(path, 'w'), indent=1, ensure_ascii=False)
    print(f'wrote the {len(out)} sectors of {r["label"]} into {path.relative_to(ROOT)}')


def swatches(name):
    """The n most representative colours of a work, in order of hue, from the showcase's SWATCHES = (label, n), into
    assets/palettes.json as swatches:<label>. Octree, not median cut: median cut greys a painting of mixed dots
    (Seurat's 24: mean chroma 0.035 against 0.049), where the octree keeps its blues, violets and oranges."""
    sys.path.insert(0, str(ROOT / 'build' / 'showcases'))
    label, n = __import__(name).SWATCHES
    q = fetch(label).convert('RGB').quantize(colors=n, method=Image.Quantize.FASTOCTREE)
    pal = q.getpalette()
    rgbs = [pal[3 * i:3 * i + 3] for _, i in q.getcolors()]
    rgbs.sort(key=lambda c: math.atan2(oklab(c)[2], oklab(c)[1]) % (2 * math.pi))
    path = ROOT / 'assets/palettes.json'
    data = json.load(open(path)) if path.exists() else {}
    data[f'swatches:{label}'] = ['#%02X%02X%02X' % tuple(c) for c in rgbs]
    json.dump(data, open(path, 'w'), indent=1, ensure_ascii=False)
    print(f'wrote {len(rgbs)} swatches of {label} into {path.relative_to(ROOT)}: {" ".join(data[f"swatches:{label}"])}')


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
    {'ring': ring, 'swatches': swatches}.get(sys.argv[1], main)(sys.argv[-1])
