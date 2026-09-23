import json, urllib.request, urllib.parse, re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UA = {'User-Agent': 'Mocubix/1.0 (https://github.com/renocrypt/mocubix)'}

def api(params, tries=5):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    delay = 2.0
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
        except Exception:
            if i == tries - 1: raise
            time.sleep(delay); delay *= 2

def clean(u):
    return re.sub(r'[?&]utm_[^&]*', '', u) if u else u

def strip_tags(v):
    return re.sub(r'<[^>]+>', '', v).strip() if v else None

def real_width(url):
    """The width Wikimedia actually served, read back off the URL. It snaps
    requests to its own bucket ladder, so the requested width is not the
    delivered one — rewriting the number by hand yields a bucket that does
    not exist."""
    m = re.search(r'/(\d+)px-', url)
    return int(m.group(1)) if m else None

WANT = ["De berg Fuji", "Witte reiger Shirasagi", "Hoge golf Tatsunami",
        "Dwarrelende sneeuw Tomoe no yuki", "Waaiers Suehiro", "Blauwe winde Asagao",
        "Maan en grassen", "Pijnbomen Shosho", "Yatsubashi", "Witte feniks Hakuho",
        "Chrysanten Momoyogusa", "Klimop Tsuta"]
ATKINS = ["File:Anna Atkins Cystoseira granulata.jpg",
          "File:Photographs of British Algae. Cyanotype Impressions, RP-F-2016-133.jpg",
          "File:Met DP-17302-004.jpg"]

sekka = json.load(open(ROOT / 'assets/sekka.json', encoding='utf-8'))
titles, label_of, kind_of = [], {}, {}
for w in WANT:
    hit = next((r for r in sekka if w.lower() in r['title'].lower()), None)
    if hit:
        titles.append(hit['title']); label_of[hit['title']] = w; kind_of[hit['title']] = 'sekka'
for t in ATKINS:
    titles.append(t); label_of[t] = "Cyanotype"; kind_of[t] = 'atkins'

ASK = [640, 1024, 1600]
recs = {}
for width in ASK:
    for i in range(0, len(titles), 3):
        chunk = titles[i:i+3]
        d = api({'action':'query','format':'json','titles':'|'.join(chunk),
                 'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':width})
        for pid, p in (d.get('query',{}).get('pages') or {}).items():
            if int(pid) < 0: continue
            ii = (p.get('imageinfo') or [{}])[0]
            em = ii.get('extmetadata') or {}
            t = p['title']
            r = recs.setdefault(t, {
                'title': t, 'label': label_of.get(t, t), 'kind': kind_of.get(t),
                'w': ii.get('width'), 'h': ii.get('height'),
                'license': strip_tags((em.get('LicenseShortName') or {}).get('value')),
                'artist': strip_tags((em.get('Artist') or {}).get('value')),
                'descurl': ii.get('descriptionurl'),
                'sources': {},
            })
            url = clean(ii.get('thumburl'))
            rw = real_width(url)
            if rw: r['sources'][str(rw)] = url     # keyed by the width ACTUALLY served
        time.sleep(1.2)

out = list(recs.values())
for r in out:
    r['srcset'] = ', '.join(f"{u} {w}w" for w, u in sorted(r['sources'].items(), key=lambda kv: int(kv[0])))
    widths = sorted(map(int, r['sources']))
    r['default'] = r['sources'][str(widths[len(widths)//2])] if widths else None

json.dump(out, open(ROOT / 'assets/curated.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"curated {len(out)} works — widths are the buckets Wikimedia actually served\n")
for r in out:
    print(f"  {r['label'][:30]:30s} {r['kind']:6s} {r['w']}x{r['h']:<5} served={sorted(map(int,r['sources']))}")
