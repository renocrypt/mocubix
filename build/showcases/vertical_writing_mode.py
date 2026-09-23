"""Vertical Writing Mode, in full: the opening of Bashō's Oku no hosomichi,
set as a handscroll that the page's scroll unrolls from the right, with two of
Yosa Buson's paintings of the journey mounted in it.

Every character is text laid out by the browser's own vertical writing: the
columns, the readings beside them, the punctuation, the sideways English and the
upright figures. The unrolling is one scroll-driven translation of the strip.
"""
import html, re

TITLE = 'The narrow road'
GLOSS = ('Set down the page instead of across it: each column is written downward, the columns run right to left, '
         'and a scroll is read by unrolling it towards the left.')
LEDE = ('The opening of Bashō’s <i>Oku no hosomichi</i>, 1702, as a handscroll: scroll, and it unrolls from the right. '
        'The readings sit beside the characters, the English turns on its side, and two of Yosa Buson’s paintings '
        'of the journey are mounted in the scroll.')

HEAD = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/noto-serif-jp/index.css">\n'

# The text of Sugiura Shōichirō's edition (Iwanami bunko, 1957) as published by Aozora Bunko; [base|reading] keeps
# a selection of that edition's readings, 〻 is its repetition mark. Each passage: paragraphs, haiku marked with 句.
SOURCE = ('https://www.aozora.gr.jp/cards/002240/card61619.html', 'Aozora Bunko')
OPENING = [
    '月日は[百代|はくだい]の[過客|くわかく]にして、行かふ年も又旅人也。舟の上に生涯をうかべ馬の口とらえて老をむかふる物は、日〻旅にして旅を[栖|すみか]とす。'
    '古人も多く旅に死せるあり。予もいづれの年よりか、[片雲|へんうん]の風にさそはれて、漂泊の思ひやまず海濱にさすらへ、去年の秋[江上|かうじやう]の[破屋|はをく]に'
    '蜘の古巣をはらひて、やゝ年も暮春立る霞の空に白川の關こえんと、そゞろ神の物につきて心をくるはせ、[道祖神|だうそじん]のまねきにあひて取もの手につかず、'
    'もゝ引の破をつゞり笠の緒付かえて、三里に灸すゆるより松嶋の月先心にかゝりて、住る方は人に讓り[杉風|さんぷう]が[別墅|べつしよ]に移るに、',
    '句草の戸も住替る代ぞひなの家',
    '[面八句|おもてはちく]を庵の柱に懸置。',
]
DEPARTURE = [
    '[彌生|やよひ]も末の七日、明ぼのゝ空[朧〻|ろうろう]として、月は[在明|ありあけ]にて光おさまれる物から、[不二|ふじ]の峯[幽|かすか]にみえて、上野谷中の花の梢又いつかはと'
    '心ぼそし。むつましきかぎりは宵よりつどひて、舟に乘て送る。千じゆと云所にて船をあがれば、前途三千里のおもひ胸にふさがりて、幻のちまたに離別の泪をそゝく。',
    '句行春や鳥啼魚の目は泪',
    '是を[矢立|やたて]の初として行道なをすゝまず。人〻は途中に立ならびて、後かげのみゆる迄はと見送なるべし。',
]

# The English runs sideways between the passages, in plain renderings of our own.
NOTES = {
    'title': 'Matsuo Bashō · The Narrow Road to the Deep North · printed 1702',
    'opening': ('The months and days are travellers of a hundred ages, and the years that come and go are travellers too.',
                'Even a grass hut changes hands: now a house for the dolls.'),
    'departure': ('Spring is leaving: the birds cry, and there are tears in the eyes of the fish.',),
    'end': 'They left Fukagawa by boat on the 27th day of the third month, 16 May 1689, for about 150 days on foot.',
}

HOW = """.strip { writing-mode: vertical-rl }            /* columns downward, right to left */
.strip .en { text-orientation: mixed }            /* Latin turns on its side */
.tcy { text-combine-upright: all }                /* 27 upright, in one square */
ruby rt { font-size: .42em }                      /* readings beside the column */
.strip { translate: calc(100vw - 100%) 0 }        /* the start: its right end at the screen's */
  /* → 0 over the run: one scroll-driven translation unrolls it */"""

NOTE = ('Nothing on the strip is drawn: the columns, the readings beside them, the stops in the top right of their '
        'squares, the English on its side and the upright figures are all the browser’s own vertical layout. '
        'The unrolling needs no measuring either: it starts at the strip’s own width, <code>100%</code>, and ends at zero.')

MATERIAL = ('Material — Matsuo Bashō, <i>Oku no hosomichi</i>, 1702 · Yosa Buson’s paintings of it, 1778 and undated · public domain')


def _ja(text):
    """Text with [base|reading] marks → HTML with ruby."""
    out, pos = [], 0
    for m in re.finditer(r'\[([^|\]]+)\|([^\]]+)\]', text):
        out.append(html.escape(text[pos:m.start()]))
        out.append(f'<ruby>{html.escape(m.group(1))}<rt>{html.escape(m.group(2))}</rt></ruby>')
        pos = m.end()
    out.append(html.escape(text[pos:]))
    return ''.join(out)


def _passage(paras):
    return '\n'.join(f'<p class="ku">{_ja(p[1:])}</p>' if p.startswith('句') else f'<p>{_ja(p)}</p>' for p in paras)


def _chars(paras):
    return sum(len(re.sub(r'\[([^|\]]+)\|[^\]]+\]', r'\1', p)) for p in paras)


def _gold(seed=1702, n=150):
    """The endpaper's cut gold leaf: flakes and slivers and dust, scattered once, the same on every build."""
    import random
    r = random.Random(seed)
    shapes = []
    for _ in range(n):
        x, y, a = r.uniform(0, 100), r.uniform(0, 600), r.uniform(0, 180)
        tone = r.choice(['#F2DE9E', '#E6CD86', '#FBEDC2', '#D9BD72', '#C9A95A'])
        kind = r.random()
        if kind < .55:     # 切箔: small squares of leaf
            w = r.uniform(1.2, 4.2); shapes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{w * r.uniform(.7, 1.3):.1f}" fill="{tone}" transform="rotate({a:.0f} {x:.1f} {y:.1f})"/>')
        elif kind < .75:   # 野毛: slivers
            shapes.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{r.uniform(5, 13):.1f}" height=".7" fill="{tone}" transform="rotate({a:.0f} {x:.1f} {y:.1f})"/>')
        else:              # 砂子: dust
            shapes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r.uniform(.3, .8):.2f}" fill="{tone}"/>')
    return ('<svg viewBox="0 0 100 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<defs><linearGradient id="g" x1="0" y1="0" x2=".4" y2="1"><stop offset="0" stop-color="#CDB684"/>'
            '<stop offset=".55" stop-color="#BFA46C"/><stop offset="1" stop-color="#CBB27E"/></linearGradient></defs>'
            '<rect width="100" height="600" fill="url(#g)"/>' + ''.join(shapes) + '</svg>')


def render(works):
    by = {w['label']: w for w in works if w['kind'] == 'buson'}
    dep, fan = by['Departure'], by['Fan']

    def img(w, sizes, alt):
        return (f'<img src="{w["default"]}" srcset="{w["srcset"]}" sizes="{sizes}" width="{w["w"]}" height="{w["h"]}" '
                f'alt="{html.escape(alt, quote=True)}" loading="lazy" decoding="async">')

    en = lambda *lines: '\n'.join(f'<p class="en">{html.escape(l)}</p>' for l in lines)
    strip = (
        '<div class="front"><p class="slip" lang="ja">おくのほそ道</p></div>\n'
        f'<div class="endpaper" aria-hidden="true">{_gold()}</div>\n'
        f'<p class="en title">{html.escape(NOTES["title"])}</p>\n'
        f'<section class="passage" lang="ja">\n{_passage(OPENING)}\n</section>\n'
        f'{en(*NOTES["opening"])}\n'
        f'<section class="passage" lang="ja">\n{_passage(DEPARTURE)}\n</section>\n'
        f'{en(*NOTES["departure"])}\n'
        f'<figure class="painting">{img(dep, "(max-width: 760px) 220vw, 160svh", "Yosa Buson: Bashō and Sora take their leave of the friends who saw them off, with the passage in Buson’s hand")}'
        '<figcaption class="en">Yosa Buson, the leave-taking, from his handscroll of the book, 1778. Umi-Mori Art Museum</figcaption></figure>\n'
        f'<figure class="fan">{img(fan, "(max-width: 760px) 120vw, 80svh", "Yosa Buson: Bashō and Sora seen from behind, walking on, painted on a fan with lines from the book")}'
        '<figcaption class="en">Buson, the two travellers walking on, a fan painting. Princeton University Art Museum</figcaption></figure>\n'
        '<p class="colophon" lang="ja">元禄<span class="tcy">2</span>年<span class="tcy">3</span>月<span class="tcy">27</span>日、江戸深川を舟で発つ</p>\n'
        f'{en(NOTES["end"])}\n'
        '<div class="tail" aria-hidden="true"></div>\n')
    # How many columns the text makes at 13 characters a column: the stylesheet turns it into the run's length.
    cols = sum(-(-_chars([p]) // 13) for p in OPENING + DEPARTURE)
    return ('<section class="scroll-stage stage" data-material aria-label="Oku no hosomichi, a handscroll that unrolls from the right">\n'
            f'<div class="run" style="--cols:{cols}">\n<div class="pin">\n'
            '<div class="roll left" aria-hidden="true"></div>\n'
            f'<div class="window">\n<div class="strip">\n{strip}</div>\n</div>\n'
            '<div class="roll right" aria-hidden="true"></div>\n'
            '<p class="cue" aria-hidden="true">Scroll to unroll</p>\n'
            '</div>\n</div>\n</section>')


def credit(works):
    by = {w['label']: w for w in works if w['kind'] == 'buson'}
    return (f'Text — Matsuo Bashō, <i>Oku no hosomichi</i> (1702), in Sugiura Shōichirō’s edition (Iwanami bunko, 1957), '
            f'via <a href="{SOURCE[0]}">{SOURCE[1]}</a>; the readings are a selection of that edition’s. '
            f'Paintings — Yosa Buson, <a href="{by["Departure"]["descurl"]}">the leave-taking</a> from his handscroll of 1778 '
            f'(Umi-Mori Art Museum) and <a href="{by["Fan"]["descurl"]}">a fan painting</a> (Princeton University Art Museum), '
            'public domain, via Wikimedia Commons. The English renderings are ours.')
