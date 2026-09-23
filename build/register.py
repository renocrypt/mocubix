"""Lay a later photograph over an earlier one taken from the same spot.

For each pair a showcase lists (its PAIRS: earlier label, later label, ..., and a
few points on stable rock in the earlier picture, chosen by eye), finds each point
in the later picture by correlating a small patch around it, then solves the
scale, turn and shift that carry the later picture onto the earlier (least
squares), and the crop the two share. Writes assets/registration.json. It works
on the 960px copies in assets/curated.json; every number is a fraction of the
picture, so the registration holds at any size.

    python3 build/register.py image_comparison_slider
    python3 build/register.py stitch kinetic_drag     # a showcase's SHEETS, laid end to end

The model is the CSS the page applies to the later picture, about its centre:
translate(tx, ty) rotate(rot) scale(s).
"""
import json, math, sys, tempfile, time, urllib.request
from pathlib import Path
from PIL import Image, ImageChops, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[1]
UA = {'User-Agent': 'Mocubix/1.0 (https://github.com/renocrypt/mocubix)'}
works = {w['label']: w for w in json.load(open(ROOT / 'assets/curated.json', encoding='utf-8'))}


CACHE = Path(tempfile.gettempdir()) / 'mocubix-register'


def fetch(label, width=960):
    """A served copy (960px unless asked), kept in the temp folder between runs (Commons throttles bursts)."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / (label.replace(' ', '_') + f'-{width}.jpg')
    if not path.exists():
        for wait in (0, 3, 8, 20):
            time.sleep(wait)
            try:
                path.write_bytes(urllib.request.urlopen(urllib.request.Request(works[label]['sources'][str(width)], headers=UA), timeout=60).read())
                break
            except Exception:
                pass
        else:
            raise SystemExit(f'could not fetch {label}')
    return Image.open(path).convert('RGB')


def place(im, s, rot, tx, ty):
    """The later picture as it lands in the earlier one's frame (inverse map for PIL)."""
    W, H = im.size
    cx, cy, ox, oy = W / 2, H / 2, W / 2 + tx * W, H / 2 + ty * H
    c, n = math.cos(math.radians(rot)) / s, math.sin(math.radians(rot)) / s
    return im.transform(im.size, Image.AFFINE, (c, n, cx - c * ox - n * oy, -n, c, cy + n * ox - c * oy), Image.BILINEAR)


def match(A, B, pt, reach=110, half=24):
    """Where a small patch of the earlier picture (around pt) turns up in the later one:
    the offset, within reach, whose patch correlates best. Returns the point in B and the correlation."""
    x, y = pt
    patch = A.crop((x - half, y - half, x + half, y + half))
    pa = ImageStat.Stat(patch)
    best = (-2, pt)
    for step, around, span in ((4, pt, reach), (1, None, 4)):
        cx, cy = around or best[1]
        for dy in range(-span, span + 1, step):
            for dx in range(-span, span + 1, step):
                u, v = cx + dx, cy + dy
                cand = B.crop((u - half, v - half, u + half, v + half))
                pb = ImageStat.Stat(cand)
                if not pa.stddev[0] or not pb.stddev[0]:
                    continue
                ab = ImageStat.Stat(ImageChops.multiply(patch, cand)).mean[0] * 255
                r = (ab - pa.mean[0] * pb.mean[0]) / (pa.stddev[0] * pb.stddev[0])
                if r > best[0]:
                    best = (r, (u, v))
    return best[1], best[0]


def fit(src, dst):
    """The scale, turn (radians) and shift that best carry points src onto dst, least squares: q = s R p + t."""
    n = len(src)
    mx, my = sum(p[0] for p in src) / n, sum(p[1] for p in src) / n
    qx, qy = sum(q[0] for q in dst) / n, sum(q[1] for q in dst) / n
    a = sum((p[0] - mx) * (q[0] - qx) + (p[1] - my) * (q[1] - qy) for p, q in zip(src, dst))
    b = sum((p[0] - mx) * (q[1] - qy) - (p[1] - my) * (q[0] - qx) for p, q in zip(src, dst))
    norm = sum((p[0] - mx) ** 2 + (p[1] - my) ** 2 for p in src)
    th, s = math.atan2(b, a), math.hypot(a, b) / norm
    c, n_ = math.cos(th), math.sin(th)
    return s, th, qx - s * (c * mx - n_ * my), qy - s * (n_ * mx + c * my)


def apply(m, p):
    s, th, tx, ty = m
    c, n = math.cos(th), math.sin(th)
    return (s * (c * p[0] - n * p[1]) + tx, s * (n * p[0] + c * p[1]) + ty)


def compose(m1, m2):
    """m1 after m2."""
    s1, t1, x1, y1 = m1
    s2, t2, x2, y2 = m2
    x, y = apply((s1, t1, 0, 0), (x2, y2))
    return (s1 * s2, t1 + t2, x + x1, y + y1)


def invert(m):
    s, th, tx, ty = m
    x, y = apply((1 / s, -th, 0, 0), (tx, ty))
    return (1 / s, -th, -x, -y)


def similarity(src, dst, size):
    """The scale, turn and shift (about the picture's centre, as the CSS applies them) that best carry
    the later picture's points (src) onto the earlier one's (dst), least squares."""
    s, th, tx, ty = fit(src, dst)
    c, n_ = math.cos(th), math.sin(th)
    W, H = size
    Tx, Ty = tx + s * (c * W / 2 - n_ * H / 2) - W / 2, ty + s * (n_ * W / 2 + c * H / 2) - H / 2   # about the centre
    residuals = [math.hypot(s * (c * p[0] - n_ * p[1]) + tx - q[0], s * (n_ * p[0] + c * p[1]) + ty - q[1]) for p, q in zip(src, dst)]
    return s, math.degrees(th), Tx / W, Ty / H, residuals


def crop(size, s, rot, tx, ty):
    """The largest window with the frame's own shape that both pictures fill, centred on what they share."""
    W, H = size
    mask = place(Image.new('L', size, 255), s, rot, tx, ty)
    l, t, r, b = mask.getbbox()
    cx, cy = (l + r) / 2 / W, (t + b) / 2 / H
    lo, hi = 0.3, 1.0
    for _ in range(20):
        k = (lo + hi) / 2
        x0, y0 = min(max(cx - k / 2, 0), 1 - k), min(max(cy - k / 2, 0), 1 - k)
        box = (round(W * x0), round(H * y0), round(W * (x0 + k)), round(H * (y0 + k)))
        lo, hi = (k, hi) if ImageStat.Stat(mask.crop(box)).extrema[0][0] == 255 else (lo, k)
    k = lo - 0.006   # a hair inside, so no edge ever shows
    x0, y0 = min(max(cx - k / 2, 0), 1 - k), min(max(cy - k / 2, 0), 1 - k)
    return [round(x0, 4), round(y0, 4), round(k, 4), round(k, 4)]


def corners(G, rock, cells=8, half=24):
    """Candidate points: in each cell of a grid over the stable rock, the patch with the most contrast."""
    W, H = G.size
    x0, y0, x1, y1 = (round(f * n) for f, n in zip(rock, (W, H, W, H)))
    pts = []
    for i in range(cells):
        for j in range(cells):
            best = None
            for x in range(x0 + half + (x1 - x0 - 2 * half) * i // cells, x0 + half + (x1 - x0 - 2 * half) * (i + 1) // cells, 8):
                for y in range(y0 + half + (y1 - y0 - 2 * half) * j // cells, y0 + half + (y1 - y0 - 2 * half) * (j + 1) // cells, 8):
                    sd = ImageStat.Stat(G.crop((x - half, y - half, x + half, y + half))).stddev[0]
                    if best is None or sd > best[0]:
                        best = (sd, (x, y))
            if best and best[0] > 18:
                pts.append(best[1])
    return pts


def consensus(pairs, size, tol=3.0):
    """The similarity most of the matches agree on (every two matches far enough apart propose one)."""
    best = []
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            (p1, q1), (p2, q2) = pairs[i], pairs[j]
            if math.dist(p1, p2) < 80:
                continue
            s, rot, tx, ty, _ = similarity([p1, p2], [q1, q2], size)
            agree = [k for k, (p, q) in enumerate(pairs) if residual(s, rot, tx, ty, p, q, size) < tol]
            if len(agree) > len(best):
                best = agree
    return [pairs[k] for k in best]


def residual(s, rot, tx, ty, p, q, size):
    W, H = size
    c, n = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    x, y = p[0] - W / 2, p[1] - H / 2
    return math.hypot(W / 2 + tx * W + s * (c * x - n * y) - q[0], H / 2 + ty * H + s * (n * x + c * y) - q[1])


def band(G):
    """A map's rows: between the paper's blank top and bottom margins (long runs of rows with no sea in
    them), from the first row after the one to the last row before the other that sea fills a share of."""
    W, H = G.size
    v = G.load()
    dark = [sum(1 for x in range(W // 10, W - W // 10, 3) if v[x, y] < 170) / (W * .8 / 3) for y in range(H)]
    blank = [d < 0.08 for d in dark]

    def run(rows):   # the first stretch of 25 blank rows met walking along rows
        count = 0
        for y in rows:
            count = count + 1 if blank[y] else 0
            if count >= 25:
                return y
        return None

    top_margin, bottom_margin = run(range(H // 3)), run(range(H - 1, H * 2 // 3, -1))
    top = next(y for y in range(top_margin, H) if dark[y] >= 0.3)
    bottom = next(y for y in range(bottom_margin, 0, -1) if dark[y] >= 0.3)
    return top, bottom


def ncc(a, b):
    sa, sb = ImageStat.Stat(a), ImageStat.Stat(b)
    if not sa.stddev[0] or not sb.stddev[0]:
        return -2
    return (ImageStat.Stat(ImageChops.multiply(a, b)).mean[0] * 255 - sa.mean[0] * sb.mean[0]) / (sa.stddev[0] * sb.stddev[0])


def seam(A, B, ba, edge):
    """How sheet B continues sheet A, where their ends overlap: slide A's last strip over B at a quarter
    of the size, then match patches across the overlap near that offset and fit what most of them agree on."""
    q, x1 = 4, edge - 40
    a, b = A.resize((A.width // q, A.height // q)), B.resize((B.width // q, B.height // q))
    strip = a.crop(((x1 - 160) // q, (ba[0] + 20) // q, x1 // q, (ba[1] - 20) // q))
    best = (-2, None)
    for dy in range(-12, 13):
        y0 = (ba[0] + 20) // q + dy
        for x in range(0, int(b.width * .6)):
            if 0 <= y0 and y0 + strip.height <= b.height:
                c = ncc(strip, b.crop((x, y0, x + strip.width, y0 + strip.height)))
                if c > best[0]:
                    best = (c, (x * q - (x1 - 160), dy * q))
    dx, dy = best[1]
    matched = []
    for px in range(x1 - 150, x1, 20):
        for py in range(ba[0] + 30, ba[1] - 30, 40):
            patch = A.crop((px - 24, py - 24, px + 24, py + 24))
            if ImageStat.Stat(patch).stddev[0] < 14 or not 30 < px + dx < B.width - 30:
                continue
            got = max(((ncc(patch, B.crop((x - 24, y - 24, x + 24, y + 24))), (x, y))
                       for y in range(py + dy - 10, py + dy + 11, 2) for x in range(px + dx - 10, px + dx + 11, 2)))
            if got[0] > 0.6:
                matched.append((got[1], (px, py)))
    agreed = consensus(matched, A.size, tol=2.5)
    m = fit([q_ for q_, _ in agreed], [p for _, p in agreed])
    worst = max(math.dist(apply(m, q_), p) for q_, p in agreed)
    return m, len(agreed), len(matched), worst


def stitch(name):
    """Lay a showcase's SHEETS end to end: each sheet's scale, turn and shift into the first sheet's frame,
    where each is cut (the middle of every overlap) and the box around the whole, at the 1920px copies."""
    sys.path.insert(0, str(ROOT / 'build' / 'showcases'))
    showcase = __import__(name)
    grey = [ImageOps.grayscale(fetch(label, 1920)) for label in showcase.SHEETS]
    bands = [band(g) for g in grey]
    edge = lambda g: g.width - 9
    to_first, pairs = [(1.0, 0.0, 0.0, 0.0)], []
    for k in range(len(grey) - 1):
        m, n, of, worst = seam(grey[k], grey[k + 1], bands[k], edge(grey[k]))
        pairs.append(m)
        to_first.append(compose(to_first[-1], m))
        print(f'  seam {k + 1}|{k + 2}: {n} of {of} patches agree; s={m[0]:.4f} turn={math.degrees(m[1]):+.2f}° '
              f'shift=({m[2]:.0f}, {m[3]:.0f}); worst {worst:.1f}px', flush=True)
    cuts = []   # (cut in the earlier sheet, the same line in the later one)
    for k, m in enumerate(pairs):
        mid = (bands[k + 1][0] + bands[k + 1][1]) / 2
        start = apply(m, (8, mid))[0]                      # where the later sheet begins, in the earlier
        c = (start + edge(grey[k])) / 2
        cuts.append((c, apply(invert(m), (c, (bands[k][0] + bands[k][1]) / 2))[0]))
    def east(g, b):
        """Where the map itself ends on the last sheet: walking in from the right, past the scan's dark border
        and across the blank paper, the first column its sea fills again."""
        v = g.load()
        sea = lambda x: sum(1 for y in range(b[0], b[1], 3) if v[x, y] < 170) / ((b[1] - b[0]) / 3)
        x, blank = g.width - 1, 0
        while x > g.width // 2 and blank < 20:
            blank = blank + 1 if sea(x) < 0.15 else 0
            x -= 1
        while x > g.width // 2 and sea(x) <= 0.3:
            x -= 1
        return x

    pad, sheets, ys = -2, [], []
    for k, g in enumerate(grey):
        x0 = cuts[k - 1][1] if k else 8
        x1 = cuts[k][0] + 8 if k < len(cuts) else east(g, bands[k]) + 4   # a little under the next sheet: no hairline
        y0, y1 = bands[k][0] - pad, bands[k][1] + pad
        s_, th, tx, ty = to_first[k]
        sheets.append({'label': showcase.SHEETS[k], 'w': g.width, 'h': g.height, 's': round(s_, 5),
                       'rot': round(math.degrees(th), 4), 'tx': round(tx, 2), 'ty': round(ty, 2),
                       'clip': [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)]})
        # where this sheet's own map band lies in the common frame, at both ends of the part that shows
        ys += [(apply(to_first[k], (x, bands[k][0]))[1], apply(to_first[k], (x, bands[k][1]))[1]) for x in (x0, x1)]
    # each sheet is cut tight to its own band; the strip spans them all, and where a sheet's band falls short
    # the ground shows: the colour of the map's own sea, so the map reads as ringed by its ocean
    box = [8, round(min(t for t, _ in ys), 1), round(apply(to_first[-1], (sheets[-1]['clip'][2], 0))[0], 1),
           round(max(b for _, b in ys), 1)]
    sea = []   # the ocean along every sheet's top and bottom edge
    for label, g, (t, b) in zip(showcase.SHEETS, grey, bands):
        im = fetch(label, 1920)
        for box_ in ((0, t, im.width, t + 30), (0, b - 30, im.width, b)):
            sea += [px for px, v in zip(im.crop(box_).getdata(), g.crop(box_).getdata()) if v < 150]
    ground = '#%02X%02X%02X' % tuple(sorted(p[i] for p in sea)[len(sea) // 2] for i in range(3))
    out_path = ROOT / 'assets/registration.json'
    out = json.load(open(out_path)) if out_path.exists() else {}
    out[f'stitch:{name}'] = {'scale': 1920, 'box': box, 'ground': ground, 'sheets': sheets}
    json.dump(out, open(out_path, 'w'), indent=1)
    print(f'stitched {len(sheets)} sheets into a strip {box[2] - box[0]:.0f} × {box[3] - box[1]:.0f} (at 1920px a sheet)')


def main(name):
    sys.path.insert(0, str(ROOT / 'build' / 'showcases'))
    showcase = __import__(name)
    out_path = ROOT / 'assets/registration.json'
    out = json.load(open(out_path)) if out_path.exists() else {}
    for then, now, *_, rock in showcase.PAIRS:
        A, B = fetch(then), fetch(now)
        B = B.resize(A.size, Image.LANCZOS)
        ga, gb = ImageOps.grayscale(A), ImageOps.grayscale(B)
        # the most contrasty patches on the earlier picture's stable rock, each found in the later picture
        matched = []
        for p in corners(ga, rock):
            q, r = match(ga, gb, p)
            if r > 0.6:
                matched.append((q, p))
        agreed = consensus(matched, A.size)
        s, rot, tx, ty, fit = similarity([q for q, _ in agreed], [p for _, p in agreed], A.size)
        print(f'  {then} → {now}: {len(agreed)} of {len(matched)} matches agree; s={s:.4f} rot={rot:+.2f}° '
              f't=({tx:+.4f}, {ty:+.4f}); worst residual {max(fit):.1f}px of 960', flush=True)
        out[f'{then}|{now}'] = {'s': round(s, 4), 'rot': round(rot, 2), 'tx': round(tx, 4), 'ty': round(ty, 4),
                                'crop': crop(A.size, s, rot, tx, ty), 'points': len(agreed)}
    json.dump(out, open(out_path, 'w'), indent=1)
    print(f'registered {len(showcase.PAIRS)} pairs into {out_path.relative_to(ROOT)}')


if __name__ == '__main__':
    stitch(sys.argv[2]) if sys.argv[1] == 'stitch' else main(sys.argv[1])
