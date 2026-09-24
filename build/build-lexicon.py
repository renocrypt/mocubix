# -*- coding: utf-8 -*-
"""Generate the Lexicon: an entrance at /lexicon/ and a page per term at
/lexicon/<term>/, all from SPECS below. The demos' styles and script are
hand-edited sources in site/lexicon/ (lexicon.css, lexicon.js); this writes
the pages and site/lexicon/material.js.

Every image URL comes from assets/curated.json, which holds only URLs the
Wikimedia API actually returned. No URL is ever hand-typed or width-rewritten.
"""
import html as html_lib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

works = json.load(open(ROOT / 'assets/curated.json', encoding='utf-8'))
sekka = [w for w in works if w['kind'] == 'sekka']
atkins = [w for w in works if w['kind'] == 'atkins']

def js_plates(items):
    out = []
    for w in items:
        out.append({
            'label': w['label'],
            'src': w['default'],
            'srcset': w['srcset'],
            'w': w['w'], 'h': w['h'],
            'license': w['license'],
            'href': w['descurl'],
        })
    return json.dumps(out, ensure_ascii=False)

SPECS = [
  # (family, name, aka, gloss, api, note, stage_html, tag)
  # The gloss says what the visitor is looking at and what to do. The note is
  # the practitioner's line and may be technical; vocabulary is its job.
  ("scroll", "Scroll Progress Timeline",
   "scroll-linked animation · page progress",
   "How far you have scrolled is how far the animation has played. The hairline across the top of this page is one.",
   "animation-timeline: scroll(root);",
   "The animation's progress <em>is</em> the scroll container's progress. Zero JavaScript, and it runs off the main thread — so it cannot jank even while the main thread is busy.",
   '<div class="dial"><div class="ring"><div class="hand"></div><span class="pct" id="pctOut">0%</span></div></div>',
   "scroll the page"),

  ("scroll", "View Progress Timeline",
   "view timeline · element-in-viewport progress",
   "Every row times its own animation by its own trip across the screen, so no two are at the same point at the same moment.",
   "view-timeline-name: --plate;\nanimation-timeline: --plate;\nanimation-range: entry 0% cover 45%;",
   "Each element measures <em>its own</em> passage through the viewport, so several different values exist at once. <code>animation-range</code> is the part most people miss — it decides which slice of that passage the animation occupies.",
   '<div class="plates" id="plates"></div>',
   "scroll the page"),

  ("scroll", "Pinning &amp; Scrub",
   "sticky section · pinned stage · ScrollTrigger pin + scrub",
   "The picture holds still while the page keeps moving, and your scrolling becomes the playhead. Scroll back up and it plays backwards.",
   "position: sticky; top: 0;\n/* GSAP */ ScrollTrigger({ pin: true, scrub: 1 })",
   "<b>Pin</b> holds the stage still while the page keeps scrolling. <b>Scrub</b> is the separate idea that progress follows scroll position rather than elapsed time, which is why it reverses exactly. Most “cinematic” sites are these two words.",
   '<div class="pinrun"><div class="pinstage"><div class="frame"><img id="pinImg" alt=""><div class="cover" id="pinCover"></div><span class="flabel">Scrub to wipe</span></div></div></div>',
   "scroll the page"),

  ("scroll", "Parallax",
   "differential scroll · multiplane",
   "The layers move at different rates, and the difference between the rates is the part you read as distance.",
   "@keyframes drift { from { transform: translateY(-10%) } to { transform: translateY(10%) } }\nanimation: drift linear both; animation-timeline: view();\n/* each layer gets its own distance; the difference is the depth */",
   "The oldest trick here and the easiest to overdo. It reads as depth only when the rates differ by a little; large offsets read as broken layout. Built on a view progress timeline it costs no JavaScript.",
   '<div class="para" id="para"><div class="lyr l1" id="paraL1"></div><div class="lyr l2" id="paraL2"></div><div class="pcap">Depth is a rate difference</div></div>',
   "scroll the page"),

  ("scroll", "Horizontal Scroll Section",
   "pinned horizontal scroll · sideways gallery",
   "You scroll down; the content travels sideways. A list you ranked becomes a row you compare across.",
   "/* --travel is the track's overflow, measured from its content */\ntransform: translateX(calc(-1 * var(--travel)));",
   "Changing the axis changes what the content means: a stack implies rank, a track implies comparison. Travel must be measured from real content — a track that barely overflows reads as a glitch, not a journey.",
   '<div class="hrun"><div class="hstage"><div class="htrack" id="htrack"></div></div></div>',
   "scroll the page"),

  ("scroll", "Scroll Snap",
   "snap points · scroll snapping",
   "Scrolling comes to rest on a whole item instead of halfway between two. It feels like turning pages.",
   "scroll-snap-type: y mandatory;\nscroll-snap-align: start;",
   "Two properties, and it inherits the platform's real scroll physics — momentum, rubber-banding, trackpad feel. Every JavaScript reimplementation is worse.",
   '<div class="snap"><div><span>Snap 01</span></div><div><span>Snap 02</span></div><div><span>Snap 03</span></div><div><span>Snap 04</span></div></div>',
   "scroll inside ↓"),

  ("scroll", "Sticky Stacking Cards",
   "card stack · sticky stack",
   "Cards catch at the top one after another and pile over each other as you keep going.",
   "li { position: sticky; top: 76px; }",
   "One property on a list. Each item sticks at the same offset so later items slide over earlier ones and the stack builds itself. No library, no measurement, no scroll listener.",
   '<ul class="stackrun" id="stackrun"></ul>',
   "scroll the page"),

  ("scroll", "Scroll Velocity Skew",
   "skew on scroll · velocity distortion · momentum skew",
   "It reads how fast you are scrolling rather than where you have got to. Throw the page and the picture leans, then settles.",
   "v += (target - v) * (target > v ? 0.34 : 0.055);\ntransform: skewY(calc(var(--vel) * -4deg));",
   "Velocity is a genuinely separate signal from position. The asymmetry is the craft: it rises about six times faster than it falls, which is what makes it read as momentum rather than twitch.",
   '<div class="skew"><div class="skewinner" id="skewinner"></div></div><p class="velout">velocity <span id="velOut">0.00</span></p>',
   "throw the page"),

  ("scroll", "Sticky State Query",
   "stuck detection · scroll-state container query · sticky-aware header",
   "The moment the bar catches at the top of its panel, it knows, and changes itself.",
   "container-type: scroll-state;\n@container scroll-state(stuck: top) { … }",
   "Until this shipped, every “shrink the header once it sticks” needed a scroll listener and a hand-picked pixel threshold that broke under zoom. Now the element is simply told what it <em>is</em>.",
   '<div class="ssq"><div class="ssqhead"><div class="ssqbar"><span>Momoyogusa · plate index</span><b>stuck</b></div></div><div class="ssqbody" id="ssqbody"></div></div><span class="supp" data-f="ss"></span>',
   "scroll inside ↓"),

  ("scroll", "Snapped State Query",
   "snapped detection · active-slide styling · scroll-state(snapped)",
   "Whichever slide is parked at the centre knows it is the one you are looking at, and lights up.",
   "scroll-snap-align: center;\n@container scroll-state(snapped: block) { … }",
   "The companion query. A carousel always needed to know which slide is <em>current</em>, and every hand-rolled version computed it from offsets and got the edges wrong. This is the browser answering the question itself.",
   '<ul class="snapq" id="snapq"></ul><span class="supp" data-f="ss"></span>',
   "scroll inside ↓"),

  ("scroll", "Scroll Markers",
   "::scroll-marker · CSS-only carousel dots · scroll-marker-group",
   "The dots under the strip are made by the strip itself, and follow wherever you are in it.",
   "scroll-marker-group: after;\nli::scroll-marker { content: '' }\nli::scroll-marker:target-current { … }",
   "The dots are generated <em>by</em> the list and track it for free — including keyboard traversal and focus order, which hand-built dot navigation almost never gets right.",
   '<ul class="cml" id="cml"></ul><span class="supp" data-f="sm"></span>',
   "drag · or click a dot"),

  ("scroll", "Scroll Buttons",
   "::scroll-button() · generated prev/next · CSS-only controls",
   "The back and forward arrows come out of the row of items itself, and go grey when there is nothing left that way.",
   "ul::scroll-button(left)  { content: '←' }\nul::scroll-button(right) { content: '→' }\nul::scroll-button(*):disabled { opacity: .25 }",
   "The same idea as the markers, for the arrows — and the <code>:disabled</code> state at each end arrives free, which is the part hand-rolled carousels forget. No JavaScript, and each one is a real button to a screen reader.",
   '<div class="csbwrap"><ul class="csb" id="csb"></ul></div><span class="supp" data-f="sb"></span>',
   "press the arrows"),

  ("scroll", "Timeline Scope",
   "timeline-scope · remote timeline · cross-tree driving",
   "A figure far down the panel drives the bar at the top of it. One element's passage moves something it sits nowhere near.",
   "timeline-scope: --plate;\n/* on a child   */ view-timeline-name: --plate;\n/* on a sibling */ animation-timeline: --plate;",
   "A scroll timeline is normally visible only to the element's own descendants. <code>timeline-scope</code> lifts it onto a shared ancestor, so a bar at the top can be driven by a figure far below it — something that previously required JavaScript by definition.",
   '<div class="tsc"><div class="tschead"><span>bar driven by the figure below</span><div class="tscbar"><i></i></div></div><div class="tscpad">keep scrolling ↓</div><div class="tscbox" id="tscbox"></div><div class="tscpad">— end —</div></div><span class="supp" data-f="ts"></span>',
   "scroll inside ↓"),

  ("scroll", "Path Drawing",
   "stroke-dashoffset scrub · line draw · SVG path reveal",
   "The line draws itself as you arrive, as though someone were tracing it in front of you.",
   'path { pathLength: 1; stroke-dasharray: 1; stroke-dashoffset: 1 }\nanimation-timeline: view();\nanimation-range: entry 5% cover 50%;',
   'The robustness trick is <code>pathLength="1"</code>: it normalises any path to a length of one, so the same two lines of CSS draw any shape without measuring it in JavaScript first.',
   '<div class="pdraw"><svg viewBox="0 0 320 152" fill="none" aria-hidden="true"><path class="p1" pathLength="1" d="M6 98C48 98 54 46 98 46s50 52 94 52 50-52 94-52c20 0 28 12 28 24"/><path class="p2" pathLength="1" d="M6 122C54 122 62 82 110 82s50 40 98 40 52-40 100-40"/><path class="p3" pathLength="1" d="M98 46c8-15 22-23 36-19M286 46c8-15 22-23 30-18"/></svg><p class="pdcap">Draws as you arrive</p></div>',
   "scroll the page"),

  ("scroll", "Word Scrub",
   "read-along highlight · per-word reveal · text scrub",
   "The sentence lights up a word at a time, and how much of it has arrived is how far you have come down the page.",
   "/* per word, i = its index */\nanimation-range: cover calc(var(--i) * 1.5%)\n                 cover calc(var(--i) * 1.5% + 26%);",
   "Each word owns a <em>different slice</em> of one timeline, so the sentence resolves left to right as you descend. The overlap is the entire craft: too little and it strobes word by word, too much and the sentence arrives all at once.",
   '<div class="wscrub" id="wscrub"></div>',
   "scroll the page"),

  ("scroll", "Direction State",
   "auto-hide header · direction-aware nav · scroll-up reveal",
   "Going down puts the bar away so you can read. Going back up brings it straight back.",
   'dir = y > last ? "down" : "up";\n[data-dir="down"] .bar { transform: translateY(-100%) }',
   "Position says where you are; direction says what you want. Descending reads as “reading, leave me alone”, ascending as “looking for something”. A few pixels of dead zone are mandatory, or a trackpad makes it flicker.",
   '<div class="dirs" id="dirs"><div class="dirshead"><span>Momoyogusa</span><b id="dirOut">up</b></div><div class="dirsbody" id="dirsbody"></div></div>',
   "scroll inside ↕"),

  ("scroll", "Curtain Overlap",
   "panel slide-over · curtain reveal · section overlap",
   "The next panel covers the one before it rather than pushing it out of the way.",
   ".a { position: sticky; top: 0 }\n.b { position: relative; z-index: 2 }",
   "Two rules and nothing else. The outgoing panel stays pinned while the incoming one rides over it, so the change reads as depth rather than travel. Note what is absent: no animation, no timeline, no measurement.",
   '<div class="curt"><div class="curtA" id="curtA"><span>01 — stays put</span></div><div class="curtB"><span>02 — rides over</span></div></div>',
   "scroll the page"),

  ("scroll", "Depth of Field",
   "focus falloff · viewport-centre focus · scroll blur",
   "Only the band across the middle of the screen is sharp. Everything above and below it falls out of focus.",
   "@keyframes focusband {\n  0%, 100% { filter: blur(4.5px); opacity: .34 }\n  46%, 54% { filter: blur(0);    opacity: 1 }\n}",
   "A camera metaphor applied to a list: attention is a narrow band, and everything outside it recedes. Keep the blur under about 6px — past that it stops reading as focus and starts reading as a rendering fault.",
   '<div class="dof" id="dof"></div>',
   "scroll the page"),

  ("scroll", "Infinite Loop Scroll",
   "endless scroll · recycled list · seamless wrap",
   "The list has no end. Keep going and it carries on, with no seam to catch on.",
   "el.append(el.firstElementChild);\nel.scrollTop -= rowHeight;   /* same frame, or it jumps */",
   "The correction must happen in the <em>same</em> frame as the move or the seam shows as a jump. Done right the list has no beginning and no end — and the scrollbar stops telling you where you are, which is the price.",
   '<div class="loopx" id="loopx"></div>',
   "never ends ↓"),

  ("scroll", "Kinetic Drag",
   "drag-to-scroll · inertial scrolling · momentum decay",
   "Grab it and throw it. It keeps going after you let go, then slows to a stop as though it had weight.",
   "v *= 0.94;                    /* per frame */\nif (Math.abs(v) < 0.1) stop();",
   "Everything lives in the decay constant. 0.90 stops abruptly and feels cheap; 0.98 slides forever and feels broken. Around <b>0.94</b> is where it starts feeling like an object with mass.",
   '<div class="kin" id="kin"><div class="kintrack" id="kintrack"></div></div>',
   "grab and throw"),

  ("scroll", "Scroll-Triggered Count",
   "odometer · number roll · stat counter",
   "The figures wait until they are on screen, then run up to their value — once, not every time you pass.",
   "font-variant-numeric: tabular-nums;\nnew IntersectionObserver(fn, { threshold: 0.6 })",
   "The tabular figures matter more than the easing — proportional numerals change width as they count and the whole row twitches. It fires <b>once</b>: a counter that replays on every pass is a tell that nobody checked it twice.",
   '<div class="cnt" id="cnt"></div><button class="btn" id="cntBtn">Replay</button>',
   "plays once"),

  ("scroll", "Scrollspy",
   "section tracking · active-anchor highlight · reading position",
   "Whatever has reached eye level is the thing the index marks as where you are.",
   "new IntersectionObserver(fn, {\n  rootMargin: '-45% 0px -45% 0px'\n})",
   "That <code>rootMargin</code> collapses the viewport to a thin band across its middle, so “current” means <em>what is at eye level</em> rather than what merely happens to be on screen. The index pinned to the top of this page is one.",
   '<div class="spy" id="spy"><div class="spyrail" id="spyrail"></div><div class="spybody" id="spybody"></div></div>',
   "scroll inside ↓"),

  ("scroll", "Overscroll Containment",
   "scroll chaining · overscroll-behavior · gesture trapping",
   "Push both panels past their last line. One hands your gesture on to the page behind it; the other keeps it.",
   "overscroll-behavior: contain;",
   "One property, and it is the whole difference between a panel that feels solid and one that feels like a leak. The chaining default is right for a document and wrong for almost every overlay.",
   '<div class="osb"><div><p class="osbcap">default — chains</p><div class="osbpane chain" id="osbA"></div></div><div><p class="osbcap">contain — absorbs</p><div class="osbpane keep" id="osbB"></div></div></div>',
   "scroll both to the end"),

  ("scroll", "Snap Stop",
   "scroll-snap-stop · no-skip snapping · mandatory stop",
   "Flick both tracks hard. The top one skips three or four items in one go; the bottom one stops at the very next one.",
   "scroll-snap-stop: always;",
   "Use it when every item must actually be seen, and leave it off for browsing. It is the difference between a catalogue and a queue.",
   '<div class="snst"><p class="osbcap">normal — a hard flick skips</p><ul class="snstrack" id="snstA"></ul><p class="osbcap">always — one at a time</p><ul class="snstrack stop" id="snstB"></ul></div>',
   "flick both"),

  ("image", "Blur-up (LQIP)",
   "low-quality image placeholder · progressive loading",
   "A small blurred stand-in appears at once and the real picture fades in over it — in a box that was already the right size, so nothing jumps.",
   "figure { aspect-ratio: 3 / 2 }   /* the box is reserved before the file lands */\n.placeholder { filter: blur(18px); transform: scale(1.1) }\n.full { opacity: 0; transition: opacity .9s }   /* → 1 once loaded */",
   "Two jobs at once: something to look at immediately, and a reserved box so nothing shifts when the real file lands. Layout shift is a ranked Core Web Vital, so the <code>aspect-ratio</code> is not decoration.",
   '<div class="lqip" id="lqip"></div><button class="btn" id="lqipBtn">Replay load</button>',
   "watch it load"),

  ("image", "Ken Burns",
   "slow pan and zoom · documentary pan",
   "A still photograph is given a slow drift and a slow push in — just enough to feel like time passing.",
   "@keyframes kb { to { transform: scale(1.14) translate(-2%, 1.5%) } }\nanimation: kb 18s ease-in-out infinite alternate;",
   "Named for the documentarian who made a career of it. The rule is that the move must be slower than the viewer's attention — if they notice the motion starting, it is too fast.",
   '<div class="kb" id="kb"></div>',
   "runs by itself"),

  ("image", "Duotone",
   "two-tone mapping · bichromate",
   "Any photograph, whatever it arrived wearing, comes out in one colour. Drag back to see what it came in as.",
   "background: var(--accent);\nmix-blend-mode: color;  /* over a grayscale base */",
   "A brand-colour treatment that survives any source image. Grayscale the base, then lay a single hue over it with <code>mix-blend-mode</code>.",
   '<div class="duo" id="duo"><div class="duoBase"></div><div class="duoTint"></div></div><input class="rng" id="duoRange" type="range" min="0" max="100" value="100" aria-label="Duotone amount">',
   "drag the slider"),

  ("image", "Progressive Blur",
   "gradient blur · layered blur · tapered blur",
   "The picture softens towards the bottom, so the caption sits on something readable without a black bar laid across it.",
   "backdrop-filter: blur(Npx);\nmask-image: linear-gradient(to top, #000, transparent);",
   "Stacked layers, each blurring more than the last, each masked to a different band. Far more elegant than a scrim because the image stays legible while the text still reads.",
   '<div class="pblur" id="pblur"><div class="pbImg"></div><div class="pbL" style="--b:2px;--s:62%"></div><div class="pbL" style="--b:6px;--s:78%"></div><div class="pbL" style="--b:14px;--s:88%"></div><p class="pbTxt">Text sits on light</p></div>',
   "read the caption"),

  ("image", "Ordered Dithering",
   "Bayer dithering · halftone · posterize",
   "The picture is cut down to a handful of tones, and the ones that are missing are made up out of a regular grain. Drag to take more away.",
   "const BAYER8 = [...];  // 8×8 threshold matrix\nv = v + (BAYER8[y%8][x%8]/64 - 0.5) * spread;",
   "Real pixel work — it needs <code>crossorigin=\"anonymous\"</code> and a CORS-clean host, otherwise the canvas is tainted and <code>getImageData</code> throws. Wikimedia sends the header; most museum CDNs do not.",
   '<div class="dith"><canvas id="dithCv"></canvas></div><input class="rng" id="dithRange" type="range" min="2" max="16" value="4" aria-label="Levels">',
   "drag the slider"),

  ("image", "Clip-path Reveal",
   "mask reveal · wipe · shape reveal",
   "The picture is uncovered by an edge travelling across it, not by fading up underneath.",
   "clip-path: inset(0 100% 0 0)  →  inset(0 0 0 0);\ntransition: clip-path .9s cubic-bezier(.16,.84,.24,1);",
   "A wipe has a direction and an edge; a fade has neither. That edge is what makes the reveal feel authored rather than merely delayed.",
   '<div class="clipr" id="clipr"><div class="clipImg"></div><div class="clipImg alt"></div></div>',
   "hover"),

  ("image", "Image Comparison Slider",
   "before/after · juxtapose",
   "Two versions of the same frame, one laid over the other. Drag the divider across to compare them.",
   "clip-path: inset(0 calc(100% - var(--x)) 0 0);",
   "One image clipped over another, the clip driven by pointer position. Keep both layers exactly registered or the comparison lies.",
   '<div class="cmp" id="cmp"><div class="cmpA"></div><div class="cmpB"></div><div class="cmpBar"></div></div>',
   "drag across"),

  ("type", "Split Text Reveal",
   "staggered line reveal · line mask · SplitText",
   "The lines rise up out of the page one after another, each a beat behind the last.",
   ".line { overflow: hidden }\n.line span { transform: translateY(110%) → none }",
   "The mask is what matters: a wrapper with <code>overflow:hidden</code> and a translated inner. That makes text rise <em>out of</em> the page instead of fading in on top of it.",
   '<div class="reveal" id="reveal"><div class="ln"><span>A name you can say</span></div><div class="ln"><span>is a thing you can ask</span></div><div class="ln"><span>someone else to build.</span></div></div>',
   "plays once"),

  ("type", "Variable Font Animation",
   "axis interpolation · variable axes",
   "Weight is a dial here, not a set of steps. Drag it and the letterforms thicken without ever swapping to another file.",
   "font-variation-settings: 'wght' 340;\ntransition: font-variation-settings .6s;",
   "A variable font exposes continuous axes rather than fixed cuts, so weight can be animated instead of swapped. One file, the whole family, and no flash between weights.",
   '<div class="vf"><p id="vfLine">Weight is a continuous axis</p><input class="rng" id="vfRange" type="range" min="100" max="900" value="400" aria-label="Weight"></div>',
   "drag the slider"),

  ("type", "Text Mask",
   "knockout text · background-clip · image-in-type",
   "The picture shows only through the letters. The type is the window, not the caption.",
   "background-image: url(…);\nbackground-clip: text;\ncolor: transparent;",
   "The type becomes an aperture onto the image. It needs real weight to work — thin letterforms leave too little opening for the picture to read.",
   '<div class="tmask"><h3 id="tmaskTxt">MOMOYOGUSA</h3></div>',
   "look through the letters"),

  ("type", "Vertical Writing Mode",
   "竖排 · tate-gumi · vertical typesetting",
   "Written down the page, as Chinese, Japanese and Korean always have been: the columns arrive right to left, Latin turns sideways, and a year stands upright in one square.",
   "writing-mode: vertical-rl;\ntext-orientation: mixed;\n.year { text-combine-upright: all }   /* 縦中横 */",
   "Native in CSS and correct for CJK — the browser rotates Latin runs and places the punctuation itself. <code>text-combine-upright</code> is the piece almost nobody reaches for: it sets a two- to four-character number upright inside one em box, which is how a printed vertical page has always handled a date. This is the experimental lane: the writing here is material to look at, never the interface.",
   '<div class="vert"><p class="vt1">滚动即时间轴</p><p class="vt2">名は体を表す</p>'
   '<p class="vt3">이름이 곧 형태다</p>'
   '<p class="vt4">神坂雪佳　百々世草　<span class="tcy">1909</span></p></div>',
   "scroll the page"),

  ("type", "Marquee",
   "ticker · infinite scroller · running band",
   "A band of text running sideways under its own power, whether or not you touch the page. Hover to stop it.",
   ".row { width: max-content; animation: slide 26s linear infinite }\n@keyframes slide { to { transform: translateX(-50%) } }\n/* the content is duplicated once, so -50% lands exactly on the seam */",
   "The one effect here that ignores scroll entirely — it gives a page a pulse when nothing else moves. Duplicate the content exactly once and travel <code>-50%</code>; that is what makes the loop seamless.",
   '<div class="marq"><div class="marqrow" id="marqrow"></div></div>',
   "runs by itself"),

  ("colour", "Token Interpolation",
   "scroll-driven theme · animated custom properties · palette rotation",
   "Every colour on the card is held to one dial. Scroll, and they all turn together, in step, never landing on a combination nobody chose.",
   "@property --rot { syntax: '<angle>'; inherits: true }\n--accent: oklch(0.637 0.145 calc(40.2deg + var(--rot)));",
   "The whole palette is one number. <code>@property</code> is what makes it animatable at all — an unregistered custom property has no interpolable type. Every token keeps its lightness and chroma and shares the angle, so nothing can drift out of step.",
   '<div class="ti" id="ti"><div class="tiface"><span class="tieye">Ledger</span><b>Momoyogusa</b><p>Twelve plates, one angle.</p><span class="tibtn">Open</span></div><div class="tibar"></div></div>',
   "scroll the page"),

  ("colour", "Scoped Rotation",
   "custom property invalidation · style recalc scope",
   "The same colour change, asked of a few elements or of a great many. Press the switch and watch the counter beside it.",
   ".stage { --rot: 0deg; animation: turn linear both; animation-timeline: scroll(root) }\n/* declared on .stage, not :root — only this subtree re-resolves each frame */",
   "Where the angle is declared decides what it costs. On the root, every element on the page re-resolves its colours each frame; on the stage, only the stage does. Scope is the whole difference between a palette that animates for free and one that eats the frame budget.",
   '<div class="sc" id="sc"><div class="scgrid" id="scgrid"></div><button class="btn" id="scBtn">24 consumers</button><p class="scout"><span id="scMs">--</span> · <span id="scN">0</span> consumers</p></div>',
   "press the switch"),

  ("colour", "Gamut Arc",
   "hue path · chroma preservation · colour interpolation",
   "Two ways to get from terra to blue. The left field goes round the outside and is a full colour the whole way; the right one goes straight across and turns to mud halfway.",
   "/* round the outside */\nbackground: oklch(0.637 0.148 calc(40.2deg + var(--t) * -135.8deg));\n/* straight across — what you get by default */\nbackground: color-mix(in srgb, <end> calc(var(--t) * 100%), <start>);",
   "How much colour a screen can hold changes with hue: the space bulges towards violet and pinches near cyan, so it is not a cylinder. That makes the route between two colours a gamut question rather than a matter of taste — and the default route, a straight line through the middle of the space, is the one that passes closest to grey. The strips under each field are the whole journey at once.",
   '<div class="ga" id="ga">'
   '<div class="gacol"><div class="gafield rim"></div><div class="gapath rim"></div>'
   '<p class="galab">along the rim<i>full colour the whole way</i></p></div>'
   '<div class="gacol"><div class="gafield chord"></div><div class="gapath chord"></div>'
   '<p class="galab">straight across<i>grey in the middle</i></p></div></div>',
   "scroll the page"),

  ("colour", "Difference Inversion",
   "mix-blend-mode · invert on crossing · self-inverting overlay",
   "The words turn into the opposite of whatever passes behind them, readable over a photograph, over white and over black — and gone over one particular grey.",
   "mix-blend-mode: difference;",
   "One property, no JavaScript, and the overlay never has to know what is behind it. What it cannot survive is mid-grey, where inverting a value returns very nearly the value you started from. Plan for that band rather than discovering it on the one slide that has it.",
   '<div class="di"><div class="dirun" id="dirun"></div><p class="ditxt">Legible on anything</p></div>',
   "watch it cross the grey"),

  ("colour", "Threshold Flip",
   "section theming · discrete palette swap · data-theme",
   "At one point on the way down, the whole panel changes its colours at once rather than easing between them.",
   "new IntersectionObserver(fn, { rootMargin: '-45% 0px -45% 0px' })\n.flip { transition: background-color .7s var(--settle) }\n/* these three palettes are unrelated by design, so they are written out\n   rather than derived from the house tokens */",
   "The common form, and the honest one when two palettes are unrelated rather than a rotation apart. Everything rests on the transition: without one it strobes, and much past a second it lags the scroll and reads as a bug.",
   '<div class="tf" id="tf"><div class="tfpanels" id="tfpanels"></div></div>',
   "scroll inside ↓"),
]


# The five pillars. Scroll is split in two: what scrolling plays, and how
# scrolling itself behaves. Order within a pillar follows SPECS.
PILLARS = [
    ("scroll-driven", "Scroll-driven", "What scrolling plays", [
        "Scroll Progress Timeline", "View Progress Timeline", "Pinning &amp; Scrub", "Parallax",
        "Horizontal Scroll Section", "Sticky Stacking Cards", "Scroll Velocity Skew", "Timeline Scope",
        "Path Drawing", "Word Scrub", "Curtain Overlap", "Depth of Field", "Scroll-Triggered Count"]),
    ("scroll-behaviour", "Scroll behaviour", "How scrolling itself behaves", [
        "Scroll Snap", "Snap Stop", "Scroll Markers", "Scroll Buttons", "Sticky State Query",
        "Snapped State Query", "Direction State", "Infinite Loop Scroll", "Kinetic Drag", "Scrollspy",
        "Overscroll Containment"]),
    ("image", "Image", "What a picture can do", None),
    ("type", "Type", "Letters that move", None),
    ("colour", "Colour", "Colour as one system", None),
]

# Terms that a full exhibit develops further, relative to the site root.
EXHIBITS = {
    "Pinning &amp; Scrub":        ("annie-g/",    "Exhibit 01 · Annie G."),
    "Horizontal Scroll Section":  ("night-side/", "Exhibit 02 · Night side"),
    "Scroll Velocity Skew":       ("florence/",   "Exhibit 03 · Florence"),
    "View Progress Timeline":     ("urformen/",   "Exhibit 04 · Urformen"),
    "Token Interpolation":        ("kilauea/",    "Exhibit 07 · Kīlauea"),
    "Threshold Flip":             ("kilauea/",    "Exhibit 07 · Kīlauea"),
}

BASE = 'https://mocubix.renocrypt.com/'
REPO = 'https://github.com/renocrypt/mocubix'


def plain(s):
    return re.sub(r'<[^>]+>', '', html_lib.unescape(s))


def attr(s):
    return html_lib.escape(plain(s), quote=True)


def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', plain(name).lower().replace('&', ' and ')).strip('-')


by_name = {s[1]: s for s in SPECS}
TERMS = []   # (pillar key, pillar name, spec), in reading order
for key, pname, _, names in PILLARS:
    specs = [by_name[n] for n in names] if names else [s for s in SPECS if s[0] == key]
    TERMS += [(key, pname, s) for s in specs]
assert len(TERMS) == len(SPECS) == len({t[2][1] for t in TERMS}), 'every term in exactly one pillar'
NUM = {t[2][1]: i + 1 for i, t in enumerate(TERMS)}

# A term with a module in build/showcases/ (scroll-markers -> scroll_markers.py) gets a full
# showcase page: the module renders its stage from the curated material and says how it is built.
import importlib, sys
sys.path.insert(0, str(ROOT / 'build' / 'showcases'))
SHOWCASES = {slug(t[2][1]): importlib.import_module(slug(t[2][1]).replace('-', '_')) for t in TERMS
             if (ROOT / 'build' / 'showcases' / (slug(t[2][1]).replace('-', '_') + '.py')).exists()}
SHOW = '<i class="shows" title="Has a full showcase"></i>'


def marked(name):
    """A term's name, with the showcase dot held to its last word so the dot never wraps alone."""
    if slug(name) not in SHOWCASES:
        return name
    head, _, last = name.rpartition(' ')
    return f'{head} <span class="nw">{last}{SHOW}</span>' if head else f'<span class="nw">{last}{SHOW}</span>'


MATERIAL = ('Material — Kamisaka Sekka 神坂雪佳, <i>Momoyogusa</i> 百々世草, 1909–10<br>'
            'Rijksmuseum scans via Wikimedia Commons, CC0. Anna Atkins cyanotypes, 1843.')


def ld(title, url, source):
    """For machines: what the page is, and the folder of the repository it is served from."""
    return json.dumps({'@context': 'https://schema.org', '@type': 'WebPage', 'name': plain(title), 'url': url,
                       'isPartOf': {'@type': 'WebSite', 'name': 'Mocubix', 'url': BASE},
                       'isBasedOn': {'@type': 'SoftwareSourceCode', 'url': source, 'codeRepository': REPO,
                                     'programmingLanguage': ['HTML', 'CSS', 'JavaScript'],
                                     'license': 'https://www.apache.org/licenses/LICENSE-2.0'}},
                      ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def shell(title, desc, path, rel, body, current=None, head='', material=MATERIAL, card=None):
    url, source = BASE + path, f'{REPO}/tree/main/site/{path}'
    # a showcase with its own share card (site/share/lexicon-<term>.jpg) shows it; every other page the Lexicon's
    card_name, card_alt = card or ('lexicon', 'The Mocubix Lexicon: forty-one named interface effects')
    nav = ''
    for k, n, _, _ in PILLARS:
        count = sum(1 for t in TERMS if t[0] == k)
        mark = ' aria-current="true"' if k == current else ''
        nav += f'<a class="navfam" href="{rel}lexicon/{k}/"{mark}>{n}<i>{count}</i></a>'
    return (SHELL.replace('__TITLE__', title).replace('__TITLE_ATTR__', attr(title)).replace('__DESC__', attr(desc))
            .replace('__URL__', url).replace('__NAV__', nav).replace('__COUNT__', str(len(TERMS)))
            .replace('__BODY__', body).replace('__HEAD__', head).replace('__MATERIAL__', material).replace('__REL__', rel)
            .replace('__CARD__', card_name).replace('__CARD_ALT__', attr(card_alt))
            .replace('__SOURCE__', source).replace('__LD__', ld(title, url, source)))


SHELL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<link rel="canonical" href="__URL__">
<script type="application/ld+json">__LD__</script>
<link rel="icon" href="__REL__favicon.ico" sizes="32x32">
<link rel="icon" href="__REL__favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="__REL__apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Mocubix">
<meta property="og:title" content="__TITLE_ATTR__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="__URL__">
<meta property="og:image" content="https://mocubix.renocrypt.com/share/__CARD__.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="__CARD_ALT__">
<meta name="twitter:card" content="summary_large_image">

<link rel="preconnect" href="https://api.fontshare.com">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://upload.wikimedia.org">
<link rel="preconnect" href="https://thumb.wikimedia.org">
<!-- One request per family. A combined f[] request silently delivers only the first. -->
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f%5B%5D=melodrama@400,500&display=swap">
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f%5B%5D=switzer@400,500,600&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/geist-mono/index.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fontsource-variable/geist/index.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/cn-fontsource-source-han-serif-sc-vf/font.css">
<link rel="stylesheet" href="__REL__house.css">
<link rel="stylesheet" href="__REL__lexicon/lexicon.css">
<script src="__REL__house.js"></script>
<!-- Chrome readies a term while the pointer rests on its link, so turning the page is instant. -->
<script type="speculationrules">{"prerender":[{"where":{"href_matches":"/lexicon/*"},"eagerness":"moderate"}]}</script>
__HEAD__</head>
<body>

<div class="readbar" aria-hidden="true"></div>

<nav class="topnav">
  <div class="inner">
    <a class="brand" href="__REL__">Mocubix</a><a class="brand" href="__REL__lexicon/"><i>Lexicon</i></a>
    <div class="navfams">__NAV__</div>
    <span class="navtail">__COUNT__ named effects</span>
    <a class="source" href="__SOURCE__" aria-label="Source of this page, on GitHub"><span>Source</span></a>
    <span data-theme-slot></span>
  </div>
</nav>

<div class="wrap">
__BODY__
<footer>
  <span>__MATERIAL__</span>
  <span>Type — Melodrama · Switzer · Geist · Geist Mono · 思源宋体</span>
  <span><a href="__REL__">The seven exhibits</a></span>
</footer>
</div>

<script src="__REL__lexicon/material.js"></script>
<script src="__REL__lexicon/lexicon.js"></script>
</body>
</html>
"""


def spec_html(pname, s, rel, level='term'):
    """The card. On a term page it is the page's subject (h1); on a pillar page
    it is one of several (h2) and links on to the term's own page."""
    _, name, aka, gloss, api, note, stage, tag = s
    akas = ' · '.join('<i>' + a.strip() + '</i>' for a in aka.split('·'))
    api = api.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')   # code, never markup
    href, label = EXHIBITS.get(name, (None, None))
    deeper = f'<a class="deeper" href="{rel}{href}">{label}</a>' if href else ''
    n, sl = NUM[name], slug(name)
    if level == 'term':
        title = f'<h1 class="name" style="view-transition-name:t-{sl}">{name}</h1>'
        opener = ''
    else:
        title = f'<h2 class="name"><a href="../{sl}/" style="view-transition-name:t-{sl}">{name}</a></h2>'
        opener = f'<a class="deeper open" href="../{sl}/">{"Open its showcase" if sl in SHOWCASES else "Open its page"}</a>'
    return (f'<section class="spec" id="{sl}">\n'
            f'  <div class="meta">\n'
            f'    <span class="idx">{n:02d} / {pname}</span>\n'
            f'    {title}\n'
            f'    <p class="gloss">{gloss}</p>\n'
            f'    <p class="aka">also called {akas}</p>\n'
            f'    <p class="note">{note}</p>\n'
            f'    <details class="how"><summary>How it is built</summary><code class="api">{api}</code></details>\n'
            f'    {opener}{deeper}\n'
            f'  </div>\n'
            f'  <div class="stage"><span class="tag">{tag}</span>{stage}</div>\n'
            f'</section>')


def entrance():
    cols = []
    for key, pname, blurb, _ in PILLARS:
        items = [t for t in TERMS if t[0] == key]
        lis = ''
        for t in items:
            s = t[2]; sl = slug(s[1])
            lis += (f'<li><a href="{sl}/" data-aka="{attr(s[2])}" data-gloss="{attr(s[3])}">'
                    f'<b>{NUM[s[1]]:02d}</b><span style="view-transition-name:t-{sl}">{marked(s[1])}</span></a></li>')
        cols.append(f'<div class="idxcol"><h4><a href="{key}/">{pname}</a><em>{len(items)}</em></h4>'
                    f'<p class="blurb">{blurb}</p><ol>{lis}</ol></div>')
    body = (f'<header class="entrance">\n'
            f'  <div class="mast">\n'
            f'    <p class="kicker">{len(TERMS)} named effects · five pillars</p>\n'
            f'    <h1>Every effect<br>has a <em>name</em></h1>\n'
            f'  </div>\n'
            f'  <div class="find">\n'
            f'    <label class="sr" for="find">Name an effect</label>\n'
            f'    <input id="find" type="search" placeholder="Name an effect…" autocomplete="off" spellcheck="false">\n'
            f'    <p class="caption" aria-live="polite">You cannot ask for what you cannot name. Type any name an effect goes by: '
            f'each of the {len(TERMS)} opens on its own page, running.</p>\n'
            f'  </div>\n'
            f'  <div class="index">{"".join(cols)}</div>\n'
            f'  <p class="keys"><span>Type to find</span><span>↑ ↓ to choose</span><span>Enter to open</span>'
            f'<span>A pillar’s name opens its cards</span><span><i class="shows"></i>A full showcase</span><span>← → on a term to turn the page</span></p>\n'
            f'</header>')
    desc = (f'{len(TERMS)} interface effects in five pillars, each on its own page and running, under the name practitioners use: '
            f'scroll-driven motion, scroll behaviour, image, type and colour.')
    return shell('The Lexicon — Mocubix', desc, 'lexicon/', '../', body)


def pillar_page(p):
    key, pname, blurb, _ = PILLARS[p]
    items = [t for t in TERMS if t[0] == key]
    chips = ''.join(f'<li><a href="#{slug(t[2][1])}"><b>{NUM[t[2][1]]:02d}</b>{t[2][1]}</a></li>' for t in items)
    cards = '\n'.join(spec_html(pname, t[2], '../../', level='pillar') for t in items)
    prev, nxt = PILLARS[p - 1] if p else None, PILLARS[p + 1] if p + 1 < len(PILLARS) else None
    pager = (f'<a class="prev" href="../{prev[0]}/"><small>← Previous pillar</small><span>{prev[1]}</span></a>' if prev else '<span></span>')
    pager += (f'<a class="next" href="../{nxt[0]}/"><small>Next pillar →</small><span>{nxt[1]}</span></a>' if nxt else '<span></span>')
    body = (f'<p class="crumb"><a href="../">Lexicon</a> / {pname}</p>\n'
            f'<header class="pillarhead">\n'
            f'  <h1>{pname}</h1>\n'
            f'  <p class="blurb">{blurb} · {len(items)} named effects, each running below</p>\n'
            f'  <ol class="chips">{chips}</ol>\n'
            f'</header>\n'
            f'{cards}\n'
            f'<nav class="pager" aria-label="Previous and next pillar">{pager}</nav>')
    desc = f'{pname}: {blurb.lower()}. ' + ', '.join(plain(t[2][1]) for t in items) + ' — each named, explained and running.'
    return shell(f'{pname} — Mocubix Lexicon', desc, f'lexicon/{key}/', '../../', body, current=key)


def term_page(i):
    pkey, pname, s = TERMS[i]
    name, rel = s[1], '../../'
    items = [t for t in TERMS if t[0] == pkey]
    lis = ''
    for t in items:
        mark = ' aria-current="page"' if t[2][1] == name else ''
        lis += f'<li><a href="../{slug(t[2][1])}/"{mark}><b>{NUM[t[2][1]]:02d}</b><span>{t[2][1]}</span></a></li>'
    others = ''.join(f'<a href="../{k}/">{n}</a>' for k, n, _, _ in PILLARS if k != pkey)
    prev = TERMS[i - 1] if i else None
    nxt = TERMS[i + 1] if i + 1 < len(TERMS) else None
    pager = (f'<a class="prev" href="../{slug(prev[2][1])}/"><small>← Previous</small><span>{prev[2][1]}</span></a>' if prev else '<span></span>')
    pager += (f'<a class="next" href="../{slug(nxt[2][1])}/"><small>Next →</small><span>{nxt[2][1]}</span></a>' if nxt else '<span></span>')
    sc = SHOWCASES.get(slug(name))
    js = sc and (ROOT / 'site' / 'lexicon' / slug(name) / 'showcase.js').exists()   # a showcase may bring a little script of its own
    if sc:
        _, _, aka, gloss, _, note, _, _ = s
        akas = ' · '.join('<i>' + a.strip() + '</i>' for a in aka.split('·'))
        how = sc.HOW.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        files = ' '.join(f'<a href="{REPO}/blob/main/site/lexicon/{slug(name)}/{f}">{f}</a>'
                        for f in ['index.html', 'showcase.css'] + ['showcase.js'] * bool(js))
        feature = (f'<header class="showhead">\n'
                   f'  <div><span class="idx">{NUM[name]:02d} / {pname}</span>\n'
                   f'    <h1 class="name" style="view-transition-name:t-{slug(name)}">{name}</h1>\n'
                   f'    <p class="gloss">{getattr(sc, "GLOSS", gloss)}</p></div>\n'
                   f'  <div class="journey"><h2>{sc.TITLE}</h2><p>{sc.LEDE}</p></div>\n'
                   f'</header>\n{sc.render(works)}\n')
        detail = (f'<div class="meta showmeta">\n'
                  f'    <p class="aka">also called {akas}</p>\n'
                  f'    <p class="note">{note} {sc.NOTE}</p>\n'
                  f'    <details class="how" open><summary>How it is built</summary><code class="api">{how}</code>'
                  f'<p class="files"><span>In full, on GitHub</span> {files}</p></details>\n'
                  + (f'    <p class="credit">{sc.credit(works)}</p>\n' if hasattr(sc, 'credit') else '') +
                  f'  </div>')
    else:
        feature, detail = '', spec_html(pname, s, rel)
    body = (f'<p class="crumb"><a href="../">Lexicon</a> / <a href="../{pkey}/">{pname}</a> · {items.index(TERMS[i]) + 1} of {len(items)}</p>\n'
            f'{feature}'
            f'<div class="termgrid">\n'
            f'  <aside class="pillarnav" aria-label="{pname}">\n'
            f'    <h4><a href="../{pkey}/">{pname}</a><em>{len(items)}</em></h4>\n'
            f'    <ol>{lis}</ol>\n'
            f'    <p class="others">{others}</p>\n'
            f'  </aside>\n'
            f'  <article class="term">\n{detail}\n  </article>\n'
            f'</div>\n'
            f'<nav class="pager" aria-label="Previous and next term">{pager}</nav>')
    head = '<link rel="stylesheet" href="showcase.css">\n' if sc else ''
    if js:
        head += '<script src="showcase.js" defer></script>\n'
    head += getattr(sc, 'HEAD', '')                                                # and anything else its head needs, such as a face
    card = None
    if sc and (ROOT / 'site' / 'share' / f'lexicon-{slug(name)}.jpg').exists():
        card = (f'lexicon-{slug(name)}', f'{plain(name)}, in the Mocubix Lexicon: {plain(sc.TITLE).lower()}')
    return shell(f'{plain(name)} — Mocubix Lexicon', plain(s[3]), f'lexicon/{slug(name)}/', rel, body, current=pkey, head=head,
                 material=getattr(sc, 'MATERIAL', MATERIAL), card=card)


def write(path, text):
    """Only what changed is written, so a page's date (sitemap.py reads it) is when it last changed."""
    path.parent.mkdir(exist_ok=True)
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.write_text(text, encoding='utf-8')


out = ROOT / 'site' / 'lexicon'
write(out / 'material.js', '/* Generated by build/build-lexicon.py from assets/curated.json: only URLs the Wikimedia API returned. */\n'
      f'var SEKKA = {js_plates(sekka)};\nvar ATKINS = {js_plates(atkins)};\n')
write(out / 'index.html', entrance())
for p in range(len(PILLARS)):
    write(out / PILLARS[p][0] / 'index.html', pillar_page(p))
for i in range(len(TERMS)):
    write(out / slug(TERMS[i][2][1]) / 'index.html', term_page(i))
print(f'wrote the Lexicon: an index, {len(PILLARS)} pillar pages and {len(TERMS)} term pages; '
      f'{len(sekka)} Sekka plates, {len(atkins)} cyanotypes in material.js')
