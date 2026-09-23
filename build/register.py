"""Lay a later photograph over an earlier one taken from the same spot.

For each pair a showcase lists (its PAIRS: earlier label, later label, ..., and a
few points on stable rock in the earlier picture, chosen by eye), finds each point
in the later picture by correlating a small patch around it, then solves the
scale, turn and shift that carry the later picture onto the earlier (least
squares), and the crop the two share. Writes assets/registration.json. It works
on the 960px copies in assets/curated.json; every number is a fraction of the
picture, so the registration holds at any size.

    python3 build/register.py image_comparison_slider

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


def fetch(label):
    """The 960px copy, kept in the temp folder between runs (Commons throttles bursts)."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / (label.replace(' ', '_') + '.jpg')
    if not path.exists():
        for wait in (0, 3, 8, 20):
            time.sleep(wait)
            try:
                path.write_bytes(urllib.request.urlopen(urllib.request.Request(works[label]['sources']['960'], headers=UA), timeout=60).read())
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


def similarity(src, dst, size):
    """The scale, turn and shift (about the picture's centre, as the CSS applies them) that best carry
    the later picture's points (src) onto the earlier one's (dst), least squares."""
    n = len(src)
    mx, my = sum(p[0] for p in src) / n, sum(p[1] for p in src) / n
    qx, qy = sum(q[0] for q in dst) / n, sum(q[1] for q in dst) / n
    a = sum((p[0] - mx) * (q[0] - qx) + (p[1] - my) * (q[1] - qy) for p, q in zip(src, dst))
    b = sum((p[0] - mx) * (q[1] - qy) - (p[1] - my) * (q[0] - qx) for p, q in zip(src, dst))
    norm = sum((p[0] - mx) ** 2 + (p[1] - my) ** 2 for p in src)
    th, s = math.atan2(b, a), math.hypot(a, b) / norm
    c, n_ = math.cos(th), math.sin(th)
    tx, ty = qx - s * (c * mx - n_ * my), qy - s * (n_ * mx + c * my)          # q = s R p + t
    W, H = size
    Tx, Ty = tx + s * (c * W / 2 - n_ * H / 2) - W / 2, ty + s * (n_ * W / 2 + c * H / 2) - H / 2   # about the centre
    fit = [math.hypot(s * (c * p[0] - n_ * p[1]) + tx - q[0], s * (n_ * p[0] + c * p[1]) + ty - q[1]) for p, q in zip(src, dst)]
    return s, math.degrees(th), Tx / W, Ty / H, fit


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
    main(sys.argv[1])
