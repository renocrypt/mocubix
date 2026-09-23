"""Follow the lines of a printed map or chart: each line a centreline, simplified, with its width.

    python3 build/trace.py path_drawing        # the lines in the showcase's TRACE

TRACE gives the picture (label), the width to read it at, and its lines: a name, the ink to follow (OKLab
bounds), where to start, which way to walk (along x or along y, and the step), where to stop, how far the line
may move between steps, and how wide a run of ink may be. At every step the line is the run of ink nearest the
last centre; for a band, runs a few pixels apart count as one (its ink's merge), so figures written across it do
not break it; a running median takes out the odd step that caught a letter. Points a
line passes where it cannot be seen (under another band) may be given before it, and a line that cannot be followed
at all (crossed by rulings) may be given by its vertices. The centreline is simplified
(Douglas-Peucker, a pixel and a half) and each vertex keeps the band's widest run since the vertex before.
An area is the outline of the largest region of one ink within a box, after its holes are closed (figures
written on a band) and its thin strokes opened away (letters, rivers), simplified to a polygon.
Writes assets/tracings.json under the showcase's name, in fractions of the picture's width on both axes.
"""
import io, json, sys, time, urllib.request
from pathlib import Path
from collections import deque
from PIL import Image, ImageFilter
import palette
from cutout import simplify

ROOT = Path(__file__).resolve().parents[1]
UA = {'User-Agent': 'Mocubix/1.0 (https://github.com/renocrypt/mocubix)'}


def fetch(label, width):
    work = next(w for w in json.load(open(ROOT / 'assets/curated.json', encoding='utf-8')) if w['label'] == label)
    src = min((w for w in work['sources'] if int(w) >= width), key=int, default=max(work['sources'], key=int))
    for wait in (0, 2, 5, 10, 20, 30, 45):          # large copies are often cut short in transit: try again
        time.sleep(wait)
        try:
            im = Image.open(io.BytesIO(urllib.request.urlopen(urllib.request.Request(work['sources'][src], headers=UA), timeout=90).read()))
            im.load()
            return im.convert('RGB').resize((width, round(width * im.height / im.width)), Image.LANCZOS)
        except Exception:
            pass
    raise SystemExit(f'could not fetch {label}')


def follow(im, ink, start, axis, step, end, window=10, maxrun=400, gap=8):
    """The centreline from start, one step at a time along axis, and the width of the run at each point."""
    merge = ink.get('merge', 0)
    W, H = im.size
    px, seen = im.load(), {}

    def inked(x, y):
        if (x, y) not in seen:
            L, a, _ = palette.oklab(px[x, y])
            seen[(x, y)] = all(lo <= v <= hi for v, (lo, hi) in ((L, ink.get('L', (0, 1))), (a, ink.get('a', (-1, 1)))))
        return seen[(x, y)]

    pos, c = (start[0], start[1]) if axis == 'x' else (start[1], start[0])
    out, miss = [], 0
    while (pos - end) * step <= 0:
        raw, cur = [], None
        for v in range(int(c - window), int(c + window) + 1):
            x, y = (pos, v) if axis == 'x' else (v, pos)
            if 0 <= x < W and 0 <= y < H and inked(x, y):
                cur = [v, v] if cur is None else [cur[0], v]
            elif cur is not None:
                raw.append(cur); cur = None
        if cur is not None:
            raw.append(cur)
        runs = []
        for r in raw:                                    # a gap of a few pixels: the same band
            if runs and r[0] - runs[-1][1] <= merge:
                runs[-1][1] = r[1]
            else:
                runs.append(r)
        runs = [r for r in runs if r[1] - r[0] + 1 <= maxrun]
        if runs:
            r = min(runs, key=lambda r: abs((r[0] + r[1]) / 2 - c))
            c, miss = (r[0] + r[1]) / 2, 0
            out.append(((pos, c) if axis == 'x' else (c, pos), r[1] - r[0] + 1))
        else:
            miss += 1
            if miss > gap:
                break
        pos += step
    return out


def area(im, ink, box, close=0, open_=0):
    """The outline of the largest region of ink in box, as a simplified polygon."""
    x0, y0, x1, y1 = box
    crop = im.crop(box)
    w, h = crop.size
    px = crop.load()
    mask = Image.new('L', (w, h), 0)
    mp = mask.load()
    for y in range(h):
        for x in range(w):
            L, a, _ = palette.oklab(px[x, y])
            if all(lo <= v <= hi for v, (lo, hi) in ((L, ink.get('L', (0, 1))), (a, ink.get('a', (-1, 1))))):
                mp[x, y] = 255
    if close:
        mask = mask.filter(ImageFilter.MaxFilter(close)).filter(ImageFilter.MinFilter(close))
    if open_:
        mask = mask.filter(ImageFilter.MinFilter(open_)).filter(ImageFilter.MaxFilter(open_))
    mp = mask.load()
    seen, best = bytearray(w * h), []
    for y in range(h):
        for x in range(w):
            if mp[x, y] and not seen[y * w + x]:
                comp, q = [], deque([(x, y)])
                seen[y * w + x] = 1
                while q:
                    a, b = q.popleft()
                    comp.append((a, b))
                    for u, v in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= u < w and 0 <= v < h and mp[u, v] and not seen[v * w + u]:
                            seen[v * w + u] = 1
                            q.append((u, v))
                if len(comp) > len(best):
                    best = comp
    inside = set(best)
    at = lambda x, y: (x, y) in inside
    start = min(best, key=lambda p: (p[1], p[0]))            # the topmost, then leftmost: its left is outside
    ring = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    path, (x, y), d = [start], start, 6                     # as if arrived moving up its left side: look from the left
    while True:
        for k in range(8):
            dx, dy = ring[(d + 6 + k) % 8]
            if at(x + dx, y + dy):
                d = (d + 6 + k) % 8
                x, y = x + dx, y + dy
                break
        else:
            break
        if (x, y) == start:
            break
        path.append((x, y))
    half = len(path) // 2                                    # a closed ring simplifies as two halves
    poly = simplify(path[:half + 1], 1.0)[:-1] + simplify(path[half:] + path[:1], 1.0)[:-1]
    return [(x + x0, y + y0) for x, y in poly], len(best)


def main(name):
    sys.path.insert(0, str(ROOT / 'build' / 'showcases'))
    spec = __import__(name).TRACE
    im = fetch(spec['label'], spec['width'])
    W = im.width
    inks = spec['inks']
    lines = {}
    for line in spec['lines']:
        if 'points' in line:                             # a line drawn by its vertices, where it cannot be followed
            lines[line['name']] = {'points': [[round(x / W, 5), round(y / W, 5)] for x, y in line['points']],
                                   'widths': [round(line['hidden'] / W, 5)] * len(line['points'])}
            continue
        got = follow(im, inks[line['ink']], line['start'], line['axis'], line['step'], line['end'],
                     line.get('window', 10), line.get('maxrun', 400), gap=line.get('gap', 8))
        # a running median across the walk takes out the odd step that caught a letter
        axis_i = 1 if line['axis'] == 'x' else 0
        across = [p[axis_i] for p, _ in got]
        smooth = [sorted(across[max(0, i - 4):i + 5])[len(across[max(0, i - 4):i + 5]) // 2] for i in range(len(across))]
        pts = [((p[0], m) if axis_i else (m, p[1])) for (p, _), m in zip(got, smooth)]
        width = {q: w for q, (_, w) in zip(pts, got)}
        head = [tuple(p) for p in line.get('before', [])]
        verts = head + simplify(pts, 1.5)
        widths, i = [], 0
        for v in verts:                                  # the widest run since the vertex before
            if v in width:
                j = pts.index(v)
                widths.append(max(width[p] for p in pts[i:j + 1]))
                i = j
            else:
                widths.append(line.get('hidden', 4))     # given points, where the line cannot be seen
        lines[line['name']] = {'points': [[round(x / W, 5), round(y / W, 5)] for x, y in verts],
                               'widths': [round(w / W, 5) for w in widths]}
        print(f'  {line["name"]}: {len(pts)} steps, {len(verts)} vertices')
    areas = {}
    for a in spec.get('areas', []):
        poly, n = area(im, inks[a['ink']], a['box'], a.get('close', 0), a.get('open', 0))
        areas[a['name']] = [[round(x / W, 5), round(y / W, 5)] for x, y in poly]
        print(f'  {a["name"]}: {n} pixels, {len(poly)} vertices')
    path = ROOT / 'assets/tracings.json'
    out = json.load(open(path, encoding='utf-8')) if path.exists() else {}
    out[name] = {'label': spec['label'], 'aspect': round(im.width / im.height, 5), 'lines': lines, 'areas': areas}
    json.dump(out, open(path, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(f'wrote {len(lines)} lines into {path.relative_to(ROOT)}')


if __name__ == '__main__':
    main(sys.argv[1])
