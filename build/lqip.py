"""Stand-ins for pictures (blur-up): a WebP of each, sixteen pixels across and a couple of hundred bytes, small
enough to write into the page itself and to show, stretched and blurred, in the picture's place until it arrives.

    python3 build/lqip.py <showcase>

reads the showcase module's LQIP, {label: (top, right, bottom, left)}: the part of each picture that is shown, in
fractions, as for object-view-box. It takes the smallest copy Commons serves (assets/curated.json), crops it to that
part, averages it down to WIDTH pixels across and pads it with PAD pixels of its own edge on every side, so that a
blur reaching past the picture's border finds the picture's colour there and not transparency. Writes
assets/lqip.json, {label: {uri, w, h, pad, bytes}} (w and h without the padding), keeping every other label.
"""
import base64, importlib, io, json, sys, time, urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
UA = {'User-Agent': 'Mocubix/1.0 (https://github.com/renocrypt/mocubix)'}
WIDTH, PAD, QUALITY = 16, 2, 50     # 16 keeps a print's fields of colour and its big shapes; 10 loses them


def fetch(url):
    for wait in (0, 2, 5, 10, 20, 30):
        time.sleep(wait)
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            return Image.open(io.BytesIO(data)).convert('RGB')
        except Exception as e:
            err = e
    raise err


def pad(im, p):
    """The picture with p pixels of its own edge repeated around it."""
    w, h = im.size
    out = Image.new('RGB', (w + 2 * p, h + 2 * p))
    out.paste(im, (p, p))
    out.paste(im.crop((0, 0, w, 1)).resize((w, p), Image.NEAREST), (p, 0))
    out.paste(im.crop((0, h - 1, w, h)).resize((w, p), Image.NEAREST), (p, h + p))
    out.paste(out.crop((p, 0, p + 1, h + 2 * p)).resize((p, h + 2 * p), Image.NEAREST), (0, 0))
    out.paste(out.crop((p + w - 1, 0, p + w, h + 2 * p)).resize((p, h + 2 * p), Image.NEAREST), (p + w, 0))
    return out


def standin(im, crop):
    t, r, b, l = crop
    W, H = im.size
    im = im.crop((round(l * W), round(t * H), round(W * (1 - r)), round(H * (1 - b))))
    h = max(1, round(WIDTH * im.height / im.width))
    buf = io.BytesIO()
    pad(im.resize((WIDTH, h), Image.BOX), PAD).save(buf, 'WEBP', quality=QUALITY, method=6)
    data = buf.getvalue()
    return {'uri': 'data:image/webp;base64,' + base64.b64encode(data).decode(), 'w': WIDTH, 'h': h, 'pad': PAD,
            'bytes': len(data)}


def main(name):
    sys.path.insert(0, str(ROOT / 'build' / 'showcases'))
    wanted = importlib.import_module(name).LQIP
    works = {}
    for w in json.load(open(ROOT / 'assets/curated.json', encoding='utf-8')):
        works.setdefault(w['label'], []).append(w)
    path = ROOT / 'assets/lqip.json'
    out = json.load(open(path, encoding='utf-8')) if path.exists() else {}
    for label, crop in wanted.items():
        assert len(works[label]) == 1, f'{label} names {len(works[label])} works: give it a label of its own'
        src = works[label][0]['sources']
        out[label] = standin(fetch(src[min(src, key=int)]), crop)
        print(f'{label:12s} {out[label]["w"]}x{out[label]["h"]}  {out[label]["bytes"]} bytes')
        time.sleep(1)
    json.dump(out, open(path, 'w', encoding='utf-8'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
