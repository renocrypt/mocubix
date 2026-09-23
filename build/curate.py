"""Curate the collection's material from Wikimedia Commons.

Every URL comes back from the API; widths are keyed by what Commons actually
served (it snaps to its own bucket ladder). Merges into assets/curated.json,
keeping whatever kinds are already there and not listed here.
"""
import json, urllib.request, urllib.parse, re, time, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = {'User-Agent': 'Mocubix/1.0 (https://github.com/renocrypt/mocubix)'}

WORKS = [
 [
  "gottlieb",
  "Billie Holiday",
  "File:Billie Holiday, Downbeat, New York, N.Y., ca. Feb. 1947 (William P. Gottlieb 04251).jpg"
 ],
 [
  "gottlieb",
  "Charlie Parker",
  "File:Charlie Parker, (Gottlieb 06851) (cropped).jpg"
 ],
 [
  "gottlieb",
  "Thelonious Monk",
  "File:Thelonious Monk, Minton's Playhouse, New York, N.Y., ca. Sept. 1947 (William P. Gottlieb 06191).jpg"
 ],
 [
  "gottlieb",
  "Sarah Vaughan",
  "File:Sarah Vaughan - William P. Gottlieb - No. 1.jpg"
 ],
 [
  "gottlieb",
  "Ella Fitzgerald",
  "File:Ella Fitzgerald (Gottlieb 02871).jpg"
 ],
 [
  "gottlieb",
  "Billy Strayhorn",
  "File:Billy Strayhorn, New York, N.Y., between 1946 and 1948 (William P. Gottlieb 08211).jpg"
 ],
 [
  "fsa",
  "Dust storm",
  "File:Farmer walking in dust storm Cimarron County Oklahoma.jpg"
 ],
 [
  "fsa",
  "Coldwater farm",
  "File:Dust Bowl farm. Coldwater District, north of Dalhart, Texas.jpg"
 ],
 [
  "fsa",
  "Tractored out",
  "File:Tenantless farm Texas panhandle 1938.jpg"
 ],
 [
  "fsa",
  "Steer skull",
  "File:Arthur Rothstein - The bleached skull of a steer, South Dakota Badlands, 1936.jpg"
 ],
 [
  "fsa",
  "Allie Mae Burroughs",
  "File:Allie Mae Burroughs print.jpg"
 ],
 [
  "fsa",
  "Migrant Mother",
  "File:Lange-MigrantMother02.jpg"
 ],
 [
  "adams",
  "Tetons",
  "File:Ansel Adams - National Archives 79-AA-G01.jpg"
 ],
 [
  "adams",
  "Old Faithful",
  "File:Ansel Adams - National Archives 79-AA-T26.jpg"
 ],
 [
  "adams",
  "Yellowstone Lake",
  "File:Ansel Adams - National Archives 79-AA-T06.jpg"
 ],
 [
  "adams",
  "Giant Dome",
  "File:Ansel Adams - National Archives 79-AA-W06.jpg"
 ],
 [
  "buson",
  "Departure",
  "File:与謝蕪村《奥の細道画巻》1778、海の見える杜美術館 2.jpg"
 ],
 [
  "buson",
  "Fan",
  "File:Yosa Buson 与謝蕪村 - Narrow Road to the Deep North (Oku no Hosomichi 奥の細道) - 2020-382 - Princeton University Art Museum.jpg"
 ],
 [
  "glacier",
  "Road 1941",
  "File:Jackson Glacier Distant in 1941 (54209695863).jpg"
 ],
 [
  "glacier",
  "Road 2025",
  "File:Jackson Glacier Distant in 2025 (54748630053).jpg"
 ],
 [
  "glacier",
  "Grinnell 1910",
  "File:Grinnell Glacier from Lower Grinnell Ridge in 1910 (54209461966).jpg"
 ],
 [
  "glacier",
  "Grinnell 2025",
  "File:Grinnell Glacier from Lower Grinnell Ridge in 2025 (54774556535).jpg"
 ],
 [
  "glacier",
  "Jackson 1914",
  "File:Jackson Glacier and Mount Jackson in 1914 (54209695843).jpg"
 ],
 [
  "glacier",
  "Jackson 2020",
  "File:Jackson Glacier and Mount Jackson in 2020 (54208559982).jpg"
 ],
 [
  "glacier",
  "Boulder 1932",
  "File:Boulder Glacier in 1932 (54209867980).jpg"
 ],
 [
  "glacier",
  "Boulder 1988",
  "File:Boulder Glacier in 1988 (54209462241).jpg"
 ],
 [
  "glacier",
  "Sperry 1907",
  "File:Sperry Glacier arm below Mount Edwards in 1907 (54209702914).jpg"
 ],
 [
  "glacier",
  "Sperry 2023",
  "File:Sperry Glacier arm below Mount Edwards in 2023 (54208559892).jpg"
 ],
 [
  "haeckel",
  "Lichenes",
  "File:Haeckel Lichenes.jpg"
 ],
 [
  "haeckel",
  "Basimycetes",
  "File:Haeckel Basimycetes.jpg"
 ],
 [
  "haeckel",
  "Diatomea",
  "File:Haeckel Diatomea.jpg"
 ],
 [
  "haeckel",
  "Ammonitida",
  "File:Haeckel Ammonitida.jpg"
 ],
 [
  "haeckel",
  "Decapoda",
  "File:Haeckel Decapoda.jpg"
 ],
 [
  "haeckel",
  "Antilopina",
  "File:Haeckel Antilopina.jpg"
 ],
 [
  "haeckel",
  "Spumellaria",
  "File:Haeckel Spumellaria.jpg"
 ],
 [
  "haeckel",
  "Actiniae",
  "File:Haeckel Actiniae.jpg"
 ],
 [
  "haeckel",
  "Discomedusae",
  "File:Haeckel Discomedusae 8.jpg"
 ],
 [
  "haeckel",
  "Trochilidae",
  "File:Haeckel Trochilidae.jpg"
 ],
 [
  "haeckel",
  "Orchidae",
  "File:Haeckel Orchidae.jpg"
 ],
 [
  "haeckel",
  "Siphonophorae",
  "File:Haeckel Siphonophorae.jpg"
 ],
 [
  "haeckel",
  "Nepenthaceae",
  "File:Haeckel Nepenthaceae.jpg"
 ],
 [
  "haeckel",
  "Chaetopoda",
  "File:Haeckel Chaetopoda.jpg"
 ],
 [
  "haeckel",
  "Batrachia",
  "File:Haeckel Batrachia.jpg"
 ],
 [
  "haeckel",
  "Lacertilia",
  "File:Haeckel Lacertilia.jpg"
 ],
 [
  "haeckel",
  "Chelonia",
  "File:Haeckel Chelonia.jpg"
 ],
 [
  "haeckel",
  "Muscinae",
  "File:Haeckel Muscinae.jpg"
 ],
 [
  "haeckel",
  "Ostraciontes",
  "File:Haeckel Ostraciontes.jpg"
 ],
 [
  "webb",
  "Jupiter",
  "File:Jupiter (NIRCam Image) (2023-147).png"
 ],
 [
  "webb",
  "Rho Ophiuchi",
  "File:Rho Ophiuchi (NIRCam Image) (2023-128).png"
 ],
 [
  "webb",
  "Orion Bar",
  "File:Orion Bar (NIRCam Image) (2023-129).jpg"
 ],
 [
  "webb",
  "Southern Ring Nebula",
  "File:Southern Ring Nebula (NIRCam Image).png"
 ],
 [
  "webb",
  "Pillars of Creation",
  "File:Pillars of Creation (NIRCam Image).jpg"
 ],
 [
  "webb",
  "Cosmic Cliffs",
  "File:NASA’s Webb Reveals Cosmic Cliffs, Glittering Landscape of Star Birth.jpg"
 ],
 [
  "webb",
  "Cassiopeia A",
  "File:Cassiopeia A (NIRCam Image) (2023-149).png"
 ],
 [
  "webb",
  "Cartwheel Galaxy",
  "File:Cartwheel Galaxy (NIRCam and MIRI Composite Image) (weic2211a).jpeg"
 ],
 [
  "webb",
  "Webb's First Deep Field",
  "File:Webb's First Deep Field.jpg"
 ],
 [
  "kilauea",
  "Glow within Halemaʻumaʻu",
  "File:Glow from lava within Halemaʻumaʻu (9b2a2aaf-08a6-4b78-9486-38936ffb3432).JPG"
 ],
 [
  "kilauea",
  "New fissure, Leilani Estates",
  "File:Kilauea eastern rift zone fissure eruption May 2018.jpg"
 ],
 [
  "kilauea",
  "Ocean entry, Kapoho",
  "File:USGS Kīlauea multimediaFile-2329 (2018-06-27).jpg"
 ],
 [
  "kilauea",
  "Summit crater",
  "File:North portion of Kilauea volcano.jpg"
 ],
 [
  "kilauea",
  "Fissure 8 cone",
  "File:Kilauea Fissure 8 cone erupting on 6-28-2018.jpg"
 ],
 [
  "kilauea",
  "Lava lake at night",
  "File:Halemaumau Lava Lake, April 19th 2018, Vulcanoes National Park, Big Island, Hawaii (28887175718).jpg"
 ],
 [
  "kilauea",
  "Flow front and houses",
  "File:USGS Kīlauea multimediaFile-2185 (2018-06-06).jpg"
 ],
 [
  "kilauea",
  "A new island",
  "File:USGS Kīlauea MultimediaFile-2428 (2018-07-13).jpg"
 ],
 [
  "muybridge",
  "Annie G. galloping, plate 626",
  "File:Eadweard Muybridge, Animal Locomotion, Plate 626, 1887, NGA 136536.jpg"
 ],
 [
  "muybridge",
  "The Horse in Motion",
  "File:The Horse in Motion high res.jpg"
 ],
 [
  "muybridge",
  "Sallie Gardner, 1878",
  "File:Eadweard Muybridge-Sallie Gardner 1878.jpg"
 ],
 [
  "muybridge",
  "Horse Dan galloping",
  "File:Horse Dan galloping, saddled with rider (rbm-QP301M8-1887-634).jpg"
 ],
 [
  "muybridge",
  "Annie G. with rider",
  "File:Horse Annie G. galloping with rider (rbm-QP301M8-1887-626).jpg"
 ],
 [
  "iss",
  "Earth at night, 2016",
  "File:BlackMarble20161km.jpg"
 ],
 [
  "iss",
  "The Nile",
  "File:Egypt’s Nile River stretches is pictured at night from the International Space Station (iss073e0422279).jpg"
 ],
 [
  "iss",
  "New York",
  "File:ISS-53 New York City, Night Lights.jpg"
 ],
 [
  "iss",
  "India and Pakistan",
  "File:ISS-62 City lights of western India and Pakistan.jpg"
 ],
 [
  "iss",
  "South Africa",
  "File:ISS-65 Night lights of South Africa.jpg"
 ],
 [
  "iss",
  "Northern Europe",
  "File:ISS-66 City lights of Northern Europe.jpg"
 ],
 [
  "iss",
  "Moscow",
  "File:Iss071e695407 (Sept 16, 2024) --- The city lights of Moscow, Russia, dotted by its surrounding suburbs, are pictured from the International Space Station as it orbited 264 miles above just west of the Volga River.jpg"
 ],
 [
  "iss",
  "Melbourne",
  "File:Iss072e034554 (Oct 9, 2024) --- The city lights of Melbourne on Port Phillip in Australia's state of Victoria are pictured from the International Space Station as it orbited 271 miles above.jpg"
 ],
 [
  "iss",
  "Central Asia, aurora",
  "File:Iss071e695419 (Sept 16, 2024) --- The city lights of central Asia and an aurora crowning Earth's horizon are pictured in this photograph from the International Space Station as it orbited 264 miles above western Kazak.jpg"
 ],
 [
  "iss",
  "Lightning",
  "File:A flash of lightning shines brighter than the lights of nearby cities in this Oct 29, 2024, image taken by astronaut Don Pettit while aboard the International Space Station (lightning-in-southeast-asia).jpg"
 ],
 [
  "iss",
  "Malaysia and Indonesia",
  "File:ISS-62 City lights and boat lights in Malaysia and Indonesia.jpg"
 ],
 [
  "storm",
  "Florence over the horizon, 11:50",
  "File:Dramatic Views of Hurricane Florence from the International Space Station From 9 12 (42828606570).jpg"
 ],
 [
  "storm",
  "Florence overhead, 11:52",
  "File:Dramatic Views of Hurricane Florence from the International Space Station From 9 12 (42828604840).jpg"
 ],
 [
  "storm",
  "Florence, the eye (Gerst)",
  "File:Staring down a hurricane (44636242351).jpg"
 ],
 [
  "storm",
  "Florence, the eye",
  "File:Dramatic Views of Hurricane Florence from the International Space Station From 9 12 (42828604100).jpg"
 ],
 [
  "storm",
  "Florence, from the station",
  "File:Dramatic Views of Hurricane Florence from the International Space Station From 9 12 (42828602070).jpg"
 ],
 [
  "storm",
  "Florence, the arm",
  "File:Dramatic Views of Hurricane Florence from the International Space Station From 9 12 (42828606570).jpg"
 ],
 [
  "storm",
  "Lingling",
  "File:Typhoon Lingling (MODIS 2019-09-08).jpg"
 ],
 [
  "storm",
  "Talim",
  "File:Typhoon Talim Barrels towards China (MODIS).jpg"
 ],
 [
  "storm",
  "Yinxing",
  "File:Typhoon Yinxing (MODIS 2024-11-10).jpg"
 ],
 [
  "storm",
  "Nesat",
  "File:Typhoon Nesat (MODIS).jpg"
 ],
 [
  "storm",
  "Zeta",
  "File:Iss064e002148 (Oct 28, 2020) --- Hurricane Zeta was pictured from the International Space Station as the category two storm churned in the Gulf of Mexico nearing Louisiana.jpg"
 ],
 [
  "blossfeldt",
  "Thorned bulb",
  "File:Blossfeldt - Thorned bulbous plant, 84.XM.142.5.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 64",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-64.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 84",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-84.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 11",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-111.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 11b",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-115.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 22",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-22.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 39",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-39.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 77",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-77.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 11c",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-119.jpg"
 ],
 [
  "blossfeldt",
  "Plant study 46",
  "File:Plantstudie Urformen der Kunst (serietitel), RP-F-2008-51-2170-46.jpg"
 ],
 [
  "solari",
  "Flap detail",
  "File:NJT Bergen Line Solari board at Secaucus Junction detail June 2026.jpg"
 ],
 [
  "solari",
  "Morristown Line",
  "File:NJT Morristown Line Solari board at Secaucus Junction June 2026.jpg"
 ],
 [
  "solari",
  "Pascack Valley Line",
  "File:NJT Pascack Valley Line Solari board at Secaucus Junction June 2026.jpg"
 ],
 [
  "solari",
  "North Jersey Coast Line",
  "File:NJT North Jersey Coast Line Solari board at Secaucus Junction June 2026.jpg"
 ],
 [
  "solari",
  "Northeast Corridor",
  "File:NJT Northeast Corridor Line Solari board at Secaucus Junction June 2026 2.jpg"
 ],
 [
  "solari",
  "Main Line",
  "File:NJT Main Line Solari board at Secaucus Junction June 2026.jpg"
 ],
 [
  "solari",
  "Main Line detail",
  "File:NJT Main Line Solari board at Secaucus Junction detail June 2026.jpg"
 ],
 [
  "planet",
  "Venus",
  "File:Venus-real color.jpg"
 ],
 [
  "planet",
  "Sun, white light, August 2024",
  "File:SDO 20240810 000000 4096 HMIIC (HMI).jpg"
 ],
 [
  "planet",
  "Earth, Blue Marble 1972",
  "File:The Blue Marble 4463x4163.jpg"
 ],
 [
  "planet",
  "Earth from the Moon",
  "File:Americas from the Moon (LROC231 - E136013771).png"
 ],
 [
  "planet",
  "Enceladus",
  "File:Enceladusstripes cassini-edit1.jpg"
 ],
 [
  "planet",
  "Tethys",
  "File:Tethys PIA07738.jpg"
 ],
 [
  "planet",
  "Sun",
  "File:446667main1 sdo-fulldisk-670.jpg"
 ],
 [
  "planet",
  "Neptune",
  "File:Neptune 1.jpg"
 ],
 [
  "planet",
  "Mercury",
  "File:Mercury in color - Prockter07-edit1.jpg"
 ],
 [
  "planet",
  "Mars",
  "File:OSIRIS Mars true color.jpg"
 ],
 [
  "planet",
  "Moon",
  "File:FullMoon2010.jpg"
 ],
 [
  "planet",
  "Earth, Apollo 17",
  "File:The Earth seen from Apollo 17.jpg"
 ],
 [
  "planet",
  "Uranus",
  "File:Uranus2.jpg"
 ],
 [
  "planet",
  "Jupiter",
  "File:Jupiter, image taken by NASA's Hubble Space Telescope, June 2019.png"
 ],
 [
  "planet",
  "Pluto",
  "File:Pluto in True Color - High-Res.jpg"
 ],
 [
  "planet",
  "Saturn",
  "File:Saturn from Cassini Orbiter (2004-10-06).jpg"
 ]
]

def api(params, tries=6):
    u = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    delay = 6
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
        except Exception:
            if i == tries - 1: raise
            time.sleep(delay); delay *= 2

def strip(v): return re.sub(r'<[^>]+>', '', v).strip() if v else None
def real_width(url):
    m = re.search(r'/(\d+)px-', url or ''); return int(m.group(1)) if m else None

ONLY = set(sys.argv[1:])          # e.g. `python3 build/curate.py webb` fetches only that kind
if ONLY: WORKS = [w for w in WORKS if w[0] in ONLY]
# material shown large asks for the big buckets too
WIDE = {'webb': (1920, 3840), 'glacier': (1920,), 'buson': (1920, 2560), 'adams': (1920,), 'fsa': (1920, 3840)}

recs = {}
for width in (330, 500, 640, 1024, 1600, 1920, 2560, 3840):   # 330, 500: tiles, thumbnails, pictures shown small
    titles = [w[2] for w in WORKS if width <= 1600 or width in WIDE.get(w[0], ())]
    if not titles: continue
    for i in range(0, len(titles), 4):
        chunk = titles[i:i+4]
        d = api({'action':'query','format':'json','titles':'|'.join(chunk),'prop':'imageinfo',
                 'iiprop':'url|size|extmetadata','iiurlwidth':width})
        norm = {p['title']: p for p in (d.get('query',{}).get('pages') or {}).values() if int(p.get('pageid', -1)) > 0}
        # the API may normalise titles; map back through the 'normalized' list
        back = {n['to']: n['from'] for n in d.get('query',{}).get('normalized', [])}
        for title, p in norm.items():
            ii = (p.get('imageinfo') or [{}])[0]; em = ii.get('extmetadata') or {}
            orig = back.get(title, title)
            kind, label = next(((k, l) for k, l, t in WORKS if t in (orig, title)), (None, None))
            if not kind: continue
            r = recs.setdefault(title, {'title': title, 'label': label, 'kind': kind,
                'w': ii.get('width'), 'h': ii.get('height'),
                'license': strip((em.get('LicenseShortName') or {}).get('value')),
                'artist': (strip((em.get('Artist') or {}).get('value')) or '')[:80],
                'credit': (strip((em.get('Credit') or {}).get('value')) or '')[:80],
                'descurl': ii.get('descriptionurl'), 'sources': {}})
            url = re.sub(r"[?&]utm_[^&]*", "", ii.get("thumburl") or ""); rw = real_width(url)
            if rw: r['sources'][str(rw)] = url
            # a file smaller than the width asked for comes back as its unscaled original: keep that
            elif url and ii.get('width') and ii['width'] <= width: r['sources'][str(ii['width'])] = url
        time.sleep(3)

# A map drawn across the full width at 2x needs the 3840 bucket; ask for it
# only where it is needed, and only keep what Commons really serves.
BIG = {"File:BlackMarble20161km.jpg", "File:Staring down a hurricane (44636242351).jpg"}
d = api({'action':'query','format':'json','titles':'|'.join(BIG),'prop':'imageinfo','iiprop':'url','iiurlwidth':2560}) if not ONLY else {}
for p in (d.get('query',{}).get('pages') or {}).values():
    r = recs.get(p['title'])
    url = re.sub(r"[?&]utm_[^&]*", "", ((p.get('imageinfo') or [{}])[0]).get("thumburl") or ""); rw = real_width(url)
    if r and rw: r['sources'][str(rw)] = url

out = list(recs.values())
for r in out:
    ws = sorted(map(int, r['sources']))
    r['srcset'] = ', '.join(f"{r['sources'][str(w)]} {w}w" for w in ws)
    r['default'] = r['sources'][str(ws[len(ws)//2])] if ws else None

path = ROOT / 'assets/curated.json'
keep = [w for w in json.load(open(path, encoding='utf-8')) if w['kind'] not in {k for k, _, _ in WORKS}]
json.dump(keep + out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f"curated {len(out)} new works, {len(keep)} kept")
for r in out:
    print(f"  {r['kind']:10s} {r['label'][:28]:28s} {r['w']}x{r['h']:<5} served={sorted(map(int, r['sources']))} {r['license']}")
