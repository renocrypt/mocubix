"""Blur-up (LQIP), in full: sixteen of Hiroshige's One Hundred Famous Views of Edo (1856–58), four to a season, on a
wall the colour of their paper. Every print is in the page from the start as its stand-in: a WebP sixteen pixels
across, a couple of hundred bytes, written into the HTML (build/lqip.py → assets/lqip.json), stretched over the
print's slot and blurred. The print comes into focus over it when its file has arrived (showcase.js), and the
captions give what each cost, measured by the browser. Replay brings the prints in again, in the order they came.

The prints are made of flat fields of colour, graded at their edges, bound by line: at sixteen pixels the fields
survive and the line does not, so the rain at Atake, the fireworks at Ryōgoku, the eagle and the foxes arrive with
the print. Every scan is cropped to its printed image, inside the margins (object-view-box), and every slot is cut
with the series' own notched corners, which CSS draws as corner-shape: scoop.
"""
import html, json
from pathlib import Path

TITLE = 'Colour first, then the line'
GLOSS = ('A stand-in of a couple of hundred bytes holds each picture’s place and colour, blurred, until the picture '
         'itself arrives.')
LEDE = ('Sixteen of Hiroshige’s <i>One Hundred Famous Views of Edo</i>, four to a season. Each is in the page from the '
        'start as a stand-in sixteen pixels across: its colours, blurred, and none of its line. The rain, the '
        'fireworks, the eagle and the foxes arrive with the print.')

# per season: its name, then each print: label in assets/curated.json, its number in the series, title, title as
# printed, year, the printed image inside the scan's margins (top, right, bottom, left, in fractions; found from
# the step between paper and keyline), and the picture described
SEASONS = [
    ('Spring', '春', 'prints 1–42', [
        dict(label='Nihonbashi', no=1, title='Nihonbashi: Clearing after Snow', ja='日本橋雪晴', year=1856,
             crop=(.0542, .0312, .0313, .0688),
             alt='Boats crowd the river under the bridge at Nihonbashi after a snowfall; snow on the roofs of the fish '
                 'market, Edo Castle and Mount Fuji under a pink dawn sky'),
        dict(label='Sendagi', no=16, title='Flower Park and Dangozaka Slope in Sendagi', ja='千駄木団子坂花屋敷',
             year=1856, crop=(.0299, .0510, .0452, .0698),
             alt='Blossom as white as cloud fills the flower park on Dangozaka slope; a teahouse among dark trees '
                 'above, visitors and a pond below'),
        dict(label='Kameido', no=30, title='Plum Park in Kameido', ja='亀戸梅屋舗', year=1857,
             crop=(.0171, .0292, .0192, .0333),
             alt='A plum branch in white blossom crosses the whole print; behind it the orchard at Kameido and '
                 'visitors beyond a fence, under a red sky'),
        dict(label='Massaki', no=36, title='View from Massaki of Suijin Shrine, Uchigawa Inlet, and Sekiya',
             ja='真崎辺より水神の森内川関屋の里を見る図', year=1857, crop=(.0187, .0240, .0221, .0208),
             alt='The Sumida River at dusk through a round window, a spray of plum across it; boats on the water, '
                 'geese in the sky, a mountain far off'),
    ]),
    ('Summer', '夏', 'prints 43–72', [
        dict(label='Suido', no=48, title='Suidō Bridge and the Surugadai Quarter', ja='水道橋駿河台', year=1857,
             crop=(.0390, .0552, .0238, .0594),
             alt='A carp streamer, black with a white eye, fills the sky above Suidō Bridge; smaller streamers, the '
                 'roofs of Surugadai and Mount Fuji behind'),
        dict(label='Mannen', no=56, title='Mannen Bridge in Fukagawa', ja='深川萬年橋', year=1857,
             crop=(.0466, .0479, .0296, .0479),
             alt='A turtle hangs by a cord from a bucket handle, framed by the bridge; beyond it the river, sailing '
                 'boats and Mount Fuji'),
        dict(label='Atake', no=58, title='Sudden Shower over Shin-Ōhashi Bridge and Atake', ja='大はしあたけの夕立',
             year=1857, crop=(.0694, .0625, .0386, .0708),
             alt='Rain falls in dense lines over the great bridge at Atake; people bent under hats and straw capes '
                 'hurry across, a raftsman poles along the grey river'),
        dict(label='Horikiri', no=64, title='Horikiri Iris Garden', ja='堀切の花菖蒲', year=1857,
             crop=(.0457, .0177, .0242, .0594),
             alt='Irises in close-up, tall stems and purple flowers against a pale sky; beyond them the iris garden '
                 'at Horikiri and its visitors'),
    ]),
    ('Autumn', '秋', 'prints 73–98', [
        dict(label='Kanda', no=75, title='The Dyers’ Quarter in Kanda', ja='神田紺屋町', year=1857,
             crop=(.0561, .0573, .0376, .0594),
             alt='Long lengths of dyed cloth, blue and white, hang from drying racks above the roofs of the dyers’ '
                 'quarter; Mount Fuji far off'),
        dict(label='Moon Pine', no=89, title='“Moon Pine” in Ueno', ja='上野山内月のまつ', year=1857,
             crop=(.0238, .0365, .0238, .0292),
             alt='The Moon Pine at Ueno, its branch trained into a ring, frames the town across Shinobazu Pond '
                 'under a red evening sky'),
        dict(label='Mama', no=94, title='The Maple Trees at Mama, the Tekona Shrine and Tsugihashi Bridge',
             ja='真間の紅葉手古那の社継はし', year=1857, crop=(.0575, .0469, .0356, .0333),
             alt='Red maple leaves hang across the foreground; through them the Tekona shrine, its bridge, water '
                 'and fields, and mountains beyond'),
        dict(label='Ryogoku', no=98, title='Fireworks by Ryōgoku Bridge', ja='両国花火', year=1858,
             crop=(.0202, .0344, .0195, .0198),
             alt='A firework bursts and trails down over the dark river at Ryōgoku; boats crowd the water by the '
                 'long bridge'),
    ]),
    ('Winter', '冬', 'prints 99–118', [
        dict(label='Kinryuzan', no=99, title='Kinryūzan Temple in Asakusa', ja='浅草金龍山', year=1856,
             crop=(.0655, .0521, .0406, .0906),
             alt='Snow falls on the temple at Asakusa, seen from its gate beneath a huge red lantern: the inner gate, '
                 'a five-storey pagoda and visitors under umbrellas'),
        dict(label='Asakusa', no=101, title='Asakusa Ricefields and Torinomachi Festival', ja='浅草田甫酉の町詣',
             year=1857, crop=(.0112, .0573, .0231, .0177),
             alt='A white cat sits at a latticed window looking over the Asakusa ricefields, where a procession '
                 'passes; geese and Mount Fuji at dusk'),
        dict(label='Jumantsubo', no=107, title='Fukagawa Susaki and Jūmantsubo', ja='深川州崎十万坪', year=1857,
             crop=(.0710, .0667, .0397, .0583),
             alt='An eagle swoops over the snow-covered plain of Jūmantsubo; a wooden bucket lies on the snow, a '
                 'mountain rises white in the distance'),
        dict(label='Oji', no=118, title='Fox Fires on New Year’s Eve under the Enoki Tree near Ōji',
             ja='王子装束ゑの木大晦日の狐火', year=1857, crop=(.0289, .0437, .0289, .0437),
             alt='On New Year’s Eve foxes gather under a great enoki tree, each with a ghostly fire at its head; '
                 'more fires come across the dark fields'),
    ]),
]
PRINTS = [p for *_, ps in SEASONS for p in ps]
LQIP = {p['label']: p['crop'] for p in PRINTS}      # what build/lqip.py makes stand-ins of
HOLDERS = {'Nihonbashi': 'LC', 'Moon Pine': 'LC', 'Horikiri': 'LC', 'Kameido': 'Cantor', 'Suido': 'MFA'}  # the rest: the Met
SOURCES = [('https://en.wikipedia.org/wiki/One_Hundred_Famous_Views_of_Edo', 'One Hundred Famous Views of Edo'),
           ('https://en.wikipedia.org/wiki/Ukiyo-e', 'Ukiyo-e')]

HEAD = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/noto-serif-jp/index.css">\n'

HOW = """<div class="slot" style="--lqip: url(data:image/webp;base64,UklGRq4AAABXRUJQ…)">  <!-- 16 pixels, ~170 bytes -->
  <img src="…/960px-print.jpg" loading="lazy" width="870" height="1324" alt="…">
</div>
.slot::before { background: var(--lqip) 0 0 / 100% 100%; filter: blur(3.5cqi) }  /* the stand-in, softened */
.held .slot img:not(.in) { opacity: 0; filter: blur(2cqi) }  /* until the file has arrived and decoded */"""

NOTE = ('A stand-in small enough to write into the page costs no request of its own and is there with the words. '
        'Sixteen pixels across is the least that still holds a composition: at ten, the round window at Massaki '
        'and the lantern at Asakusa are gone. The browser stretches it over the print’s slot and blurs it; padded '
        'with two pixels of its own edge, the blur finds the picture’s colour at the border and not a fade to '
        'nothing. Then the print comes into focus over it rather than being pasted on top. Each colour in these '
        'prints came from its own woodblock, ten or more to a print, with bokashi grading the skies: that is what '
        'survives, which is why a wall of stand-ins already reads as the seasons.')

MATERIAL = ('Material — Utagawa Hiroshige, <i>One Hundred Famous Views of Edo</i>, 1856–58 · the Metropolitan Museum '
            'of Art, the Library of Congress, the Cantor Arts Center, the Museum of Fine Arts, Boston · public domain')

def _standins():
    return json.load(open(Path(__file__).resolve().parents[2] / 'assets/lqip.json', encoding='utf-8'))


def _bytes(n):
    return f'{n / 1000:.1f} KB' if n >= 1000 else f'{n} B'


def render(works):
    by, standins = {w['label']: w for w in works if w['kind'] == 'edo'}, _standins()
    total = sum(standins[p['label']]['bytes'] for p in PRINTS)
    # one slot shape for the whole wall, the median of the prints' own (0.644 to 0.667), so every row lines up; each
    # print covers it, losing at most a hundredth at an edge
    shapes = sorted(by[p['label']]['w'] * (1 - p['crop'][1] - p['crop'][3]) / (by[p['label']]['h'] * (1 - p['crop'][0] - p['crop'][2]))
                    for p in PRINTS)
    ar = (shapes[7] + shapes[8]) / 2
    seasons = []
    for k, (season, kanji, span, prints) in enumerate(SEASONS):
        figs = []
        for p in prints:
            w, s = by[p['label']], standins[p['label']]
            t, r, b, l = p['crop']
            cw, ch = w['w'] * (1 - l - r), w['h'] * (1 - t - b)
            grow = 1 / (1 - l - r)
            load = ' loading="eager"' if k == 0 else ' loading="lazy"'
            figs.append(
                f'<figure class="print">\n'
                f'  <div class="slot" style="--px:{s["pad"] / s["w"]:.2%};--py:{s["pad"] / s["h"]:.2%};'
                f'--lqip:url({s["uri"]})">'
                f'<img src="{w["default"]}" srcset="{w["srcset"]}" '
                f'sizes="(max-width: 760px) calc((100vw - 44px) / 2 * {grow:.3f}), calc((min(92vw, 1400px) - 72px) / 4 * {grow:.3f})" '
                f'width="{round(cw)}" height="{round(ch)}" '
                f'style="object-view-box:inset({t:.2%} {r:.2%} {b:.2%} {l:.2%})" '
                f'alt="{html.escape(p["alt"], quote=True)}" decoding="async"{load}></div>\n'
                f'  <figcaption><span class="no">No. {p["no"]} · {p["year"]}</span>'
                f'<b>{html.escape(p["title"])}</b><span class="ja" lang="ja">{p["ja"]}</span>'
                f'<span class="cost"><span>stand-in {_bytes(s["bytes"])}</span><span>print <output>—</output></span></span></figcaption>\n'
                f'</figure>')
        seasons.append(
            f'<section class="season" aria-labelledby="edo-{season.lower()}">\n'
            f'<h3 id="edo-{season.lower()}"><span class="kanji" lang="ja">{kanji}</span>{season}<small>{span}</small></h3>\n'
            f'<div class="prints">\n' + '\n'.join(figs) + '\n</div>\n</section>')
    return (
        f'<section class="edo stage" data-material style="--ar:{ar:.4f}" aria-label="Sixteen prints from One Hundred '
        'Famous Views of Edo, four to a season, each shown first as its stand-in">\n'
        '<div class="deck">\n'
        '  <fieldset class="show"><legend>Show</legend>'
        '<input type="radio" name="edo-show" id="edo-prints" checked><label for="edo-prints">prints</label>'
        '<input type="radio" name="edo-show" id="edo-standins"><label for="edo-standins">stand-ins</label></fieldset>\n'
        '  <button type="button" class="replay" hidden>Replay the arrivals</button>\n'
        f'  <p class="total"><span><b>{_bytes(total)}</b> of stand-ins, in this page</span>'
        f'<span><output class="got">—</output> of prints, <output class="n">0</output> of {len(PRINTS)} arrived</span></p>\n'
        '</div>\n' + '\n'.join(seasons) + '\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'edo'}
    held = {'Met': [], 'LC': [], 'Cantor': [], 'MFA': []}
    for p in PRINTS:
        held[HOLDERS.get(p['label'], 'Met')].append(f'<a href="{by[p["label"]]["descurl"]}">{p["no"]}</a>')
    names = {'Met': 'the Metropolitan Museum of Art (CC0)', 'LC': 'the Library of Congress',
             'Cantor': 'the Cantor Arts Center, Stanford University', 'MFA': 'the Museum of Fine Arts, Boston'}
    return ('Prints — Utagawa Hiroshige, <i>One Hundred Famous Views of Edo</i>, 1856–58, public domain, via Wikimedia '
            'Commons, by number in the series: ' + '; '.join(f'{names[k]}, {", ".join(v)}' for k, v in held.items())
            + '. Each is shown cropped to its printed image, without the margins of its sheet. Facts — '
            + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
