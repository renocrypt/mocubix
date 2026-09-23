"""Marquee, in full: the fifty-five greetings of the Voyager Golden Record (1977), from Sumerian to English, in the
order they were recorded, running in five bands out from under the record into the dark. Each greeting is set in
its own script's face and carries its time on the record and its English translation. Hover over a band to stop it;
Hold stops them all (anything moving for more than five seconds must be stoppable); with reduced motion the bands
stand still and scroll by hand.

Each band's greetings are set twice and the pair travels half its width, so the seam never shows; the copy is
aria-hidden and inert. The duration is one set's measured width over the band's speed (showcase.js), so bands of
any length keep their pace. The record is NASA's photograph; only its label turns, at the 16⅔ rpm the record was
cut for, clipped inside the dark run-out band so the seam between still and turning falls on black. The grooves
look the same at every angle, and the photograph's glints stay where the light was.
"""
import html, urllib.parse

TITLE = 'Fifty-five greetings, still travelling'
LEDE = ('In 1977 each Voyager carried a gold record of the sounds of Earth, and on it greetings in fifty-five '
        'languages, from Sumerian to English. Here they run out from under the record in the order they were '
        'recorded, each in its own script. Hover over a band to stop it; Hold stops them all.')

# the greetings as recorded: time on the record, language, its tag (script and direction follow from it), the
# greeting as written, and in English
GREETINGS = [
    ('0:00:00', 'Sumerian', 'sux', '𒁲𒈠𒃶𒈨𒂗',
     'May all be well.'),
    ('0:00:04', 'Ancient Greek', 'grc', 'Οἵτινές ποτ᾿ ἔστε χαίρετε! Εἰρηνικῶς πρὸς φίλους ἐληλύθαμεν φίλοι.',
     'Greetings to you, whoever you are. We come in friendship to those who are friends.'),
    ('0:00:11', 'Portuguese', 'pt', 'Paz e felicidade a todos',
     'Peace and happiness to everyone.'),
    ('0:00:14', 'Cantonese', 'yue-Hant', '各位好嗎？祝各位平安健康快樂。',
     "How's everyone? Wish you peace, health and happiness."),
    ('0:00:19', 'Akkadian', 'akk', 'Adanniš lu šulmu',
     'May all be very well.'),
    ('0:00:22', 'Russian', 'ru', 'Здравствуйте! Приветствую вас!',
     'Greetings! I welcome you!'),
    ('0:00:25', 'Thai', 'th', 'สวัสดีค่ะ สหายในธรณีโพ้น พวกเราในธรณีนี้ขอส่งมิตรจิตมาถึงท่านทุกคน',
     'Hello friends from farland. We in this land have sent you warm greeting to you all.'),
    ('0:00:32', 'Arabic', 'ar', 'تحياتنا للأصدقاء في النجوم. يا ليت يجمعنا الزمان.',
     'Our greetings to the friends amongst the stars. We wish that time would unite us.'),
    ('0:00:38', 'Romanian', 'ro', 'Salutări la toată lumea',
     'Regards to everyone.'),
    ('0:00:42', 'French', 'fr', 'Bonjour tout le monde',
     'Hello, everyone.'),
    ('0:00:45', 'Burmese', 'my', 'နေကောင်းပါသလား',
     'Are you well?'),
    ('0:00:48', 'Hebrew', 'he', 'שלום',
     'Peace.'),
    ('0:00:50', 'Spanish', 'es', 'Hola y saludos a todos',
     'Hello and greetings to everyone.'),
    ('0:00:54', 'Indonesian', 'id', 'Selamat malam hadirin sekalian, selamat berpisah dan sampai bertemu lagi di lain waktu',
     'Good night, ladies and gentlemen. Goodbye and see you next time.'),
    ('0:00:59', 'Quechua', 'qu', 'Kay pachamamta niytapas maytapas rimapallasta runasimipi',
     'Hello to everybody from this Earth, in Quechua language.'),
    ('0:01:04', 'Punjabi', 'pa', 'ਆਓ ਜੀ, ਜੀ ਆਇਆਂ ਨੂੰ',
     'Welcome home. It is a pleasure to receive you.'),
    ('0:01:07', 'Hittite', 'hit', 'aššuli',
     'Greetings / Hail! (literally "in goodwill")'),
    ('0:01:08', 'Bengali', 'bn', 'নমস্কার, বিশ্বে শান্তি হোক',
     'Hello! Let there be peace everywhere.'),
    ('0:01:11', 'Latin', 'la', 'Salvete quicumque estis; bonam erga vos voluntatem habemus, et pacem per astra ferimus',
     'Greetings to you, whoever you are; we have good will towards you and bring peace across space.'),
    ('0:01:19', 'Aramaic', 'arc', '𐡌𐡋𐡔',
     'Hello (literally "peace")'),
    ('0:01:22', 'Dutch', 'nl', 'Hartelijke groeten aan iedereen',
     'Dear/sincere greetings to everyone.'),
    ('0:01:24', 'German', 'de', 'Herzliche Grüße an alle',
     'Warm greetings to everyone.'),
    ('0:01:27', 'Urdu', 'ur', 'السلام عليکم ـ ہم زمين کے رہنے والوں کى طرف سے آپ کو خوش آمديد کہتے ھيں',
     'Peace be upon you. We, the inhabitants of this earth, send our greetings to you.'),
    ('0:01:37', 'Vietnamese', 'vi', 'Chân thành gửi tới các bạn lời chào thân hữu',
     'Sincerely sending greetings to you.'),
    ('0:01:40', 'Turkish', 'tr', 'Sayın Türkçe bilen arkadaşlarımız, sabah şerifleriniz hayrolsun',
     'Dear Turkish-speaking friends, may the honors of the morning be upon your heads.'),
    ('0:01:45', 'Japanese', 'ja', 'こんにちは。お元気ですか？',
     'Hello (literally "How is your day?"), how are you?'),
    ('0:01:48', 'Hindi', 'hi', 'धरती के वासियों की ओर से नमस्कार',
     'Greetings from the inhabitants of the earth.'),
    ('0:01:51', 'Welsh', 'cy', 'Iechyd da i chi yn awr, ac yn oesoedd',
     'Good health to you now and forever.'),
    ('0:01:54', 'Italian', 'it', 'Tanti auguri e saluti',
     'Many greetings and wishes.'),
    ('0:01:57', 'Sinhala', 'si', 'ආයුබෝවන්!',
     'Wish You a Long Life.'),
    ('0:02:00', 'Zulu', 'zu', 'Siya nibingelela maqhawe sinifisela inkonzo ende.',
     'We greet you, great ones. We wish you longevity.'),
    ('0:02:05', 'Sotho', 'st', 'Reani lumelisa marela.',
     'We greet you, O great ones.'),
    ('0:02:08', 'Wu', 'wuu-Hans', '祝㑚大家好。',
     'Best wishes to you all.'),
    ('0:02:12', 'Armenian', 'hy', 'Բոլոր անոնց որ կը գտնուին տիեզերգի միգամածութիւնէն անդին, ողջոյններ',
     'To all those who exist in the universe, greetings.'),
    ('0:02:19', 'Korean', 'ko', '안녕하세요',
     'Hello (literally "Are you peaceful?" or "Be peaceful")'),
    ('0:02:22', 'Polish', 'pl', 'Witajcie, istoty z zaświatów.',
     'Welcome, beings from beyond the world.'),
    ('0:02:25', 'Nepali', 'ne', 'प्रिथ्वी वासीहरु बाट शान्ति मय भविष्य को शुभकामना',
     'Wishing you a peaceful future from the earthlings.'),
    ('0:02:29', 'Mandarin', 'cmn-Hans', '各位都好吧？我们都很想念你们，有空请到这儿来玩。',
     "How's everyone? We all very much wish to meet you, if you're free please come and visit."),
    ('0:02:35', 'Ila', 'ilb', 'Mypone kaboutu noose.',
     'We wish all of you well.'),
    ('0:02:38', 'Swedish', 'sv', 'Hälsningar från en dataprogrammerare i den lilla universitetsstaden Ithaca på planeten Jorden',
     'Greetings from a computer programmer in the small university town of Ithaca on (the) planet Earth.'),
    ('0:02:45', 'Nyanja', 'ny', 'Mulibwanji imwe boonse bantu bakumwamba.',
     'How are all you people of other planets?'),
    ('0:02:48', 'Gujarati', 'gu', 'પૃથ્વી ઉપર વસનાર એક માનવ તરફથી બ્રહ્માંડના અન્ય અવકાશમાં વસનારાઓને હાર્દિક અભિનંદન. આ સંદેશો મળ્યે, વળતો સંદેશો મોકલાવશો.',
     'Greetings from a human being of the Earth. Please contact.'),
    ('0:03:03', 'Ukrainian', 'uk', "Пересилаємо привіт із нашого світу, бажаємо щастя, здоров'я і многая літа",
     'We are sending greetings from our world, wishing you happiness, health and many years.'),
    ('0:03:09', 'Persian', 'fa', 'درود بر ساکنین ماورای آسمان\u200cها. بنی\u200cآدم اعضای یک پیکرند، که در آفرینش ز یک گوهرند، چو عضوی به درد آورد روزگار، دگر عضوها را نماند قرار.',
     'Greetings to the residents of far skies. Human Beings are members of a whole, In creation of one essence and soul, If one member is inflicted with pain, Other members uneasy will remain.'),
    ('0:03:22', 'Serbian', 'sr', 'Желимо вам све најлепше са наше планете',
     'We wish you all the best, from our planet.'),
    ('0:03:25', 'Oriya', 'or', 'ସୂର୍ଯ୍ୟ ତାରକାର ତୃତୀୟ ଗ୍ରହ ପୃଥିବୀରୁ ବିଶ୍ୱବ୍ରହ୍ମାଣ୍ଡର ଅଧିବାସୀ ମାନଙ୍କୁ ଅଭିନନ୍ଦନ',
     'Greetings to the inhabitants of the universe from the third planet Earth of the star Sun.'),
    ('0:03:34', 'Ganda', 'lg', 'Musulayo mutya abantu bensi eno mukama abawe emirembe bulijo.',
     'Greetings to all peoples of the universe. God give you peace always.'),
    ('0:03:38', 'Marathi', 'mr', 'नमस्कार. ह्या पृथ्वीतील लोक तुम्हाला त्यांचे शुभविचार पाठवतात आणि त्यांची इच्छा आहे की तुम्ही ह्या जन्मी धन्य व्हा.',
     'Greetings. The people of the Earth send their good wishes and hope you find good fortune in this life.'),
    ('0:03:47', 'Amoy', 'nan-Hant', '太空朋友，恁好！恁食飽未？有閒著來阮遮坐喔。',
     'Friends from space, how are you all? Have you eaten yet? Come visit us if you have time.'),
    ('0:03:55', 'Hungarian', 'hu', 'Üdvözletet küldünk magyar nyelven minden békét szerető lénynek a Világegyetemen',
     'We are sending greetings in the Hungarian language to all peace-loving beings on the Universe.'),
    ('0:04:01', 'Telugu', 'te', 'నమస్తే, తెలుగు మాట్లాడే జనముననించి మా శుభాకాంక్షలు.',
     'Greetings. Best wishes from Telugu-speaking people.'),
    ('0:04:05', 'Czech', 'cs', 'Milí přátelé, přejeme vám vše nejlepší',
     'Dear Friends, we wish you the best.'),
    ('0:04:08', 'Kannada', 'kn', 'ನಮಸ್ತೆ, ಕನ್ನಡಿಗರ ಪರವಾಗಿ ಶುಭಾಷಯಗಳು.',
     "Greetings. On behalf of Kannada-speaking people, 'good wishes'."),
    ('0:04:12', 'Rajasthani', 'raj', 'सब भाइमो ने म्हारो राम पहुॅचे हमा अंडे खुशी डॉ उम्हा वहाँ खुगो रीगो',
     'Hello to everyone. We are happy here and you be happy there.'),
    ('0:04:18', 'English', 'en', 'Hello from the children of planet Earth.',
     'Hello from the children of planet Earth.'),
]
RTL = {'ar', 'he', 'ur', 'fa', 'arc'}
# five bands, eleven greetings each, in the record's order: size, speed in pixels a second, and how much light each
# keeps, so they read as depths
BANDS = [(.7, 28, .6), (.95, 42, .85), (1.15, 54, 1), (.82, 35, .72), (.62, 23, .5)]
RECORD = dict(label='Sounds of Earth', hole=(.5048, .4916), turning=.179)   # the spindle hole; the label, clipped
FACES = ['Noto Serif Display', 'Noto Serif JP', 'Noto Serif TC', 'Noto Serif SC', 'Noto Serif KR', 'Noto Serif Thai',
         'Noto Naskh Arabic', 'Noto Nastaliq Urdu', 'Noto Serif Hebrew', 'Noto Serif Myanmar', 'Noto Serif Gurmukhi',
         'Noto Serif Bengali', 'Noto Serif Devanagari', 'Noto Serif Sinhala', 'Noto Serif Armenian', 'Noto Serif Gujarati',
         'Noto Serif Oriya', 'Noto Serif Telugu', 'Noto Serif Kannada', 'Noto Sans Cuneiform', 'Noto Sans Imperial Aramaic']
SOURCES = [('https://en.wikipedia.org/wiki/Voyager_Golden_Record', 'Voyager Golden Record'),
           ('https://en.wikipedia.org/wiki/Contents_of_the_Voyager_Golden_Record', 'Contents of the Voyager Golden Record'),
           ('https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html', 'WCAG 2.2, Pause, Stop, Hide')]

# every face in one request, each cut down to the characters the greetings use
_TEXT = ''.join(sorted(set(''.join(g[3] for g in GREETINGS))))
HEAD = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        + '&amp;'.join('family=' + f.replace(' ', '+') for f in FACES)
        + '&amp;display=swap&amp;text=' + urllib.parse.quote(_TEXT) + '">\n')

HOW = """<div class="run">                                <!-- moves; holds the greetings twice -->
  <ul class="set">…eleven greetings…</ul>
  <ul class="set" aria-hidden="true" inert>…the same eleven…</ul>
</div>
.run { width: max-content; animation: run var(--dur) linear infinite }
@keyframes run { to { translate: -50% 0 } }      /* one set's width: it lands on the seam */
.band:hover .run, .voyager:has(#hold:checked) .run { animation-play-state: paused }"""

NOTE = ('The copy is <code>aria-hidden</code> and <code>inert</code>, so a screen reader reads each greeting once and '
        'the keyboard never tabs into the ghost. Speed is set in pixels a second, not seconds a loop: the duration is '
        'one set’s measured width over the band’s speed, measured again when the fonts arrive, so five bands of '
        'different lengths keep their own paces. Anything that moves for more than five seconds must be stoppable: '
        'hover stops a band, Hold stops them all, and with reduced motion they stand still and scroll by hand. Each '
        'greeting is set in its own script’s face, and all twenty-one faces come in one request cut down to the '
        'characters the greetings use. Only the label turns, at the 16⅔ rpm the record was cut for: the grooves look '
        'the same at every angle, and the photograph’s glints stay where the light was.')

MATERIAL = ('Material — the Voyager Golden Record, <i>The Sounds of Earth</i>, 1977 · NASA · public domain; the '
            'greetings as recorded on it')


def _time(t):
    h, m, s = map(int, t.split(':'))
    return f'<time datetime="PT{m}M{s}S">{m}:{s:02d}</time>'


def _greeting(g):
    t, language, tag, text, english = g
    rtl = ' dir="rtl"' if tag.split('-')[0] in RTL else ''
    return (f'<li><span class="g" lang="{tag}"{rtl}>{html.escape(text)}</span>'
            f'<span class="t">{_time(t)} {html.escape(language)}'
            + (f' · {html.escape(english)}' if english != text else '') + '</span></li>')


def render(works):
    w = next(w for w in works if w['kind'] == 'voyager')
    hx, hy = RECORD['hole']
    img = (f'src="{w["default"]}" srcset="{w["srcset"]}" sizes="(max-width: 760px) 120vw, min(96svh, 64vw)" '
           f'width="{w["w"]}" height="{w["h"]}" decoding="async"')
    bands = []
    for k, (size, speed, light) in enumerate(BANDS):
        items = ''.join(_greeting(g) for g in GREETINGS[k * 11:(k + 1) * 11])
        bands.append(f'<div class="band" data-speed="{speed}" style="--size:{size};--light:{light}"><div class="run">'
                     f'<ul class="set">{items}</ul><ul class="set" aria-hidden="true" inert>{items}</ul></div></div>')
    return (
        '<section class="voyager stage" data-material aria-label="The fifty-five greetings of the Voyager Golden '
        'Record, in five running bands">\n'
        f'<figure class="record" style="--hx:{hx:.2%};--hy:{hy:.2%};--turning:{RECORD["turning"]:.1%}">'
        f'<img class="disc" {img} alt="The Voyager Golden Record, a gold-plated disc; its label reads The Sounds of '
        f'Earth, United States of America, Planet Earth"><img class="label" {img} alt="" aria-hidden="true"></figure>\n'
        '<div class="bands">\n' + '\n'.join(bands) + '\n</div>\n'
        '<div class="foot"><input type="checkbox" id="voy-hold"><label for="voy-hold">Hold</label>'
        f'<p>{len(GREETINGS)} greetings in the order they were recorded, 0:00 to 4:18 · the label turns at 16⅔ rpm</p></div>\n'
        '</section>')


def credit(works):
    w = next(w for w in works if w['kind'] == 'voyager')
    return (f'Photograph — <a href="{w["descurl"]}">The Sounds of Earth</a>, NASA, public domain, via Wikimedia Commons. '
            'Greetings — recorded for the Voyager record in 1977; written forms and translations as listed in '
            'Wikipedia’s contents of the record. Facts — ' + '; '.join(f'<a href="{u}">{t}</a>' for u, t in SOURCES) + '.')
