import json, urllib.request, urllib.parse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

UA = {'User-Agent': 'Mocubix/1.0 (https://github.com/renocrypt/mocubix)'}

TITLES = [
 # dark-ground astronomy — matches the house palette natively
 "File:Pillars of Creation (NIRCam Image).jpg",
 "File:Tarantula Nebula by JWST.jpg",
 "File:Orion Nebula in NIRCam short-wavelength channel ESA25105094.jpg",
 "File:Crab Nebula imaged using James Webb Space Telescope.png",
 "File:Southern Ring Nebula (NIRCam and MIRI Images Side by Side).png",
 "File:NASA Unveils Celestial Fireworks as Official Hubble 25th Anniversary Image.jpg",
 "File:30 Doradus, Tarantula Nebula.jpg",
 "File:Pillars of creation 2014 HST WFC3-UVIS full-res denoised.jpg",
 "File:Carina Nebula (NIRCam Image).jpg",
 "File:Webb's First Deep Field.jpg",
 # ukiyo-e — material for the CJK typography lane
 "File:Tsunami by hokusai 19th century.jpg",
 "File:Red Fuji southern wind clear morning.jpg",
 "File:Ōhashi Atake no yūdachi-名所江戸百景 大はしあたけの夕立-Sudden Shower over Shin-Ōhashi Bridge and Atake (Ōhashi Atake no yūdachi), from the series One Hundred Famous Views of Edo (Meisho Edo hyakkei) MET DP123602.jpg",
 "File:「名所江戸百景 深川洲崎十万坪」-“Jūmantsubo Plain at Fukagawa Susaki,” from the series One Hundred Famous Views of Edo (Meisho Edo hyakkei, Fukagawa Susaki Jūmantsubo) MET DP121668.jpg",
 "File:歌川広重画 「名所江戸百景 駒形堂吾嬬橋」-“Azuma Bridge from Komagatadō Temple,” from the series One Hundred Famous Views of Edo (Meisho Edo hyakkei, Komagatadō Azumabashi) MET DP121530.jpg",
]

def clean(u):
    return re.sub(r'[?&]utm_[^&]*', '', u) if u else u

def fetch(titles, width):
    out = []
    for i in range(0, len(titles), 5):
        chunk = titles[i:i+5]
        params = {'action':'query','format':'json','titles':'|'.join(chunk),
                  'prop':'imageinfo','iiprop':'url|size|extmetadata','iiurlwidth':width}
        u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
        for pid, p in (d.get('query',{}).get('pages') or {}).items():
            if int(pid) < 0:
                out.append({'title': p.get('title'), 'missing': True}); continue
            ii = (p.get('imageinfo') or [{}])[0]
            em = ii.get('extmetadata') or {}
            def ev(k):
                v = (em.get(k) or {}).get('value')
                return re.sub(r'<[^>]+>', '', v).strip() if v else None
            out.append({
                'title': p.get('title'),
                'w': ii.get('width'), 'h': ii.get('height'),
                'thumb': clean(ii.get('thumburl')),
                'thumbw': ii.get('thumbwidth'), 'thumbh': ii.get('thumbheight'),
                'license': ev('LicenseShortName'),
                'credit': ev('Credit'), 'artist': ev('Artist'),
                'descurl': ii.get('descriptionurl'),
            })
    return out

if __name__ == '__main__':
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 1600
    rows = fetch(TITLES, width)
    json.dump(rows, open(ROOT / 'assets/manifest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for r in rows:
        if r.get('missing'):
            print("MISSING:", r['title'][:70]); continue
        print(f"{r['w']}x{r['h']:<6} {str(r['license'])[:16]:18s} {r['title'][:58]}")
