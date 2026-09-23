"""Cut an object out of the backing it was scanned on: a board, a card, a sheet with torn edges.

    python3 build/cutout.py dubois          # every work of that kind in assets/curated.json

Writes assets/cutouts.json, keyed by label: a clip-path polygon in percentages of the picture,
so it scales with it. The backing (a sleeve, a scanner bed) is whatever reaches the picture's
edge through pixels that are light and nearly colourless; the object is everything else. Its
outline is traced, pulled in a pixel so no backing fringe shows, and simplified (Douglas–Peucker,
within a pixel and a half at 960 wide).
"""
import io, json, sys, time, urllib.request
from collections import deque
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
UA = {'User-Agent': 'Mocubix/1.0 (https://github.com/renocrypt/mocubix)'}


def fetch(work):
    url = work['sources'][min(work['sources'], key=lambda w: abs(int(w) - 960))]
    for wait in (0, 5, 15, 30):
        time.sleep(wait)
        try:
            return Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()))
        except Exception:
            pass
    raise SystemExit(f'could not fetch {url}')


def backing(im, spread=20, light=185):
    """The pixels connected to the edge that are light and colourless."""
    W, H = im.size
    px = im.convert('RGB').load()
    bare = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            bare[y * W + x] = max(r, g, b) - min(r, g, b) < spread and min(r, g, b) > light
    out = bytearray(W * H)
    q = deque(i for i in range(W * H) if (i % W in (0, W - 1) or i // W in (0, H - 1)) and bare[i])
    for i in q: out[i] = 1
    while q:
        i = q.popleft(); x, y = i % W, i // W
        for j in (i - 1 if x else -1, i + 1 if x < W - 1 else -1, i - W, i + W):
            if 0 <= j < W * H and bare[j] and not out[j]:
                out[j] = 1; q.append(j)
    return out


def outline(solid, W, H):
    """Trace the outer boundary of the object (Moore neighbours), clockwise from its left edge."""
    at = lambda x, y: 0 <= x < W and 0 <= y < H and solid[y * W + x]
    y0 = H // 2
    x0 = next(x for x in range(W) if all(at(x + k, y0) for k in range(24)))    # not a speck of dust
    ring = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    path, (x, y), d = [(x0, y0)], (x0, y0), 6        # arrived moving up, so look from the left
    while True:
        for k in range(8):
            dx, dy = ring[(d + 6 + k) % 8]
            if at(x + dx, y + dy):
                d = (d + 6 + k) % 8; x, y = x + dx, y + dy
                break
        if (x, y) == (x0, y0): return path
        path.append((x, y))


def simplify(pts, tol):
    """Douglas–Peucker."""
    if len(pts) < 3: return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    L = ((bx - ax) ** 2 + (by - ay) ** 2) ** .5 or 1
    far, i = max((abs((bx - ax) * (ay - y) - (ax - x) * (by - ay)) / L, i) for i, (x, y) in enumerate(pts))
    if far <= tol: return [pts[0], pts[-1]]
    return simplify(pts[:i + 1], tol)[:-1] + simplify(pts[i:], tol)


def cut(im):
    W, H = im.size
    back = backing(im)
    solid = bytearray(not b for b in back)
    edge = [i for i in range(W * H) if solid[i] and any(back[j] for j in (i - 1, i + 1, i - W, i + W) if 0 <= j < W * H)]
    for i in edge: solid[i] = 0                          # a pixel in, so no backing fringe shows
    pts = outline(solid, W, H)
    half = len(pts) // 2                                 # a closed ring simplifies as two halves
    pts = simplify(pts[:half + 1], 1.6)[:-1] + simplify(pts[half:] + pts[:1], 1.6)[:-1]
    return 'polygon(' + ','.join(f'{x / W * 100:.1f}% {y / H * 100:.1f}%' for x, y in pts) + ')', len(pts)


def main(kind):
    works = [w for w in json.load(open(ROOT / 'assets/curated.json', encoding='utf-8')) if w['kind'] == kind]
    path = ROOT / 'assets/cutouts.json'
    out = json.load(open(path, encoding='utf-8')) if path.exists() else {}
    for w in works:
        out[w['label']], n = cut(fetch(w))
        print(f'  {w["label"]}: {n} points')
    json.dump(out, open(path, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f'wrote {len(works)} outlines into {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main(sys.argv[1])
