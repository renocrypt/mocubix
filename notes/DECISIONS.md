# Mocubix — asset & typography decisions

Recorded 2026-09-15. Every line below is a measured result, not an assumption.

## Typography — non-Google, verified loading in Chrome from `file://`

| Role | Face | Source | Evidence |
|---|---|---|---|
| Display | **Melodrama** | Fontshare | `loaded`, visually distinct in probe 2 |
| Sans | **Switzer** | Fontshare | `loaded` |
| Mono | **Geist Mono Variable** | Vercel via jsDelivr | `loaded`, distinct from system mono |
| CJK display | **Smiley Sans 得意黑** | jsDelivr `cn-fontsource-smiley-sans-oblique-regular` | 14 faces loaded |
| CJK text | **LXGW WenKai 霞鹜文楷** | jsDelivr `cn-fontsource-lxgw-wen-kai-gb-screen` | 19 faces loaded |
| CJK song | **Source Han Serif SC** | jsDelivr `cn-fontsource-source-han-serif-sc-vf` | 19 faces loaded |

### Two traps, both hit and both fixed

1. **One Fontshare request per family.** A single combined
   `f[]=a&f[]=b&f[]=c` request silently delivered only the first family.
   Everything else fell back with no error. Symptom: four different serif
   specimens rendering identically.

2. **Width comparison cannot verify a CJK face.** Every ideograph is 1em wide
   in every CJK font, so advance width matches the fallback exactly even when
   the face loaded correctly. Enumerate `document.fonts` instead.

### A third trap, found 2026-09-17: loading is not working

**Smiley Sans Oblique advances 0 in `writing-mode: vertical-rl`.** The package
`cn-fontsource-smiley-sans-oblique-regular` loads all 14 faces and renders
horizontally, and `document.fonts` lists it — so every check in the table above
passed. Set vertically it collapsed: six ideographs occupied 0px of vertical
advance, and the whole column rendered as a 19px smear. The other two lines in
the specimen only survived because the face does not cover kana or Hangul and
they fell back.

Measured at 100px in a `vertical-rl` box, vertical advance per glyph:

| face | 中文 | 日本語 | 한글 |
|---|---|---|---|
| Smiley Sans Oblique | **0** | — falls back | — falls back |
| LXGW WenKai GB Screen | 1.088em | 1.175em | 0.992em |
| **Source Han Serif SC VF** | **1.000em** | **1.000em** | **1.000em** |

Vertical setting stands on a square em. WenKai renders but its advance wanders
18% between scripts, which shows as three different rhythms in three columns.
Source Han Serif is exact in all three, so the specimen is now one face across
all three scripts, differentiated by size and colour.

**Rule: a face used vertically is verified a second time, by measuring the
height of a `vertical-rl` box.** `document.fonts` only proves the file arrived.

Two more things this cost:

- **The family name is `Source Han Serif SC VF`, not `Source Han Serif SC`.**
  The bare name silently matched the system 宋体 instead. Read the family name
  out of `document.fonts`, never off the package name.
- `document.fonts.check(font, text)` is **not** a coverage oracle for a
  subsetted CJK package — it reports on the subsets that happen to have loaded,
  so it returns false for characters the font certainly contains. Discriminate
  by measuring advance against the candidate fallbacks instead.

### Rejected

- **Any Google Fonts face** — house constraint.
- `cn-fontsource-source-han-serif-cn-vf` — package does not exist (`-sc-` not `-cn-`).
- `Fontquan-XinYiJiXiangSong` 新艺吉祥宋 — 70 faces declared, **0 loaded**.
- Clash Display — loads fine, but too widely used to lead with.

## Motion — what the audit of 2026-09-17 found

Easing held: every transition and animation in the Lexicon resolves to the
house curve, the authored `--pan` curve, or `linear` (correct, and only, for
scrub). Zero stock curves.

What did not hold was **scale**. Measuring stage fill per specimen — the union
box of everything that paints, over the stage box — gave a median of 0.90 and
five outliers, all of them a small thing centred in a large empty box:

| | was | now |
|---|---|---|
| 01 dial | 180px ring | fills 76% of stage height |
| 03 pinned frame | 540px | 780px |
| 14 path drawing | 328px of a ~840px stage | 95% of stage width |
| 34 text mask | capped at 92px | 114px, measured to fit |
| 35 vertical writing | 25% of stage width, no motion at all | 47%, four columns, written downward on scroll |

Two measurement traps met while doing it:

- **`a.effect.getTiming().easing` is always `linear` for a CSS animation.** The
  real curve lives per-keyframe in `getKeyframes()`. An easing census built on
  the effect-level value reports nothing and looks clean.
- **The `animation` shorthand resets `animation-range`.** `.vert p{animation:…}`
  is specificity (0,1,1) and beat the per-column `.vt1{animation-range:…}` at
  (0,1,0), so all four columns staggered identically. Per-item ranges need the
  descendant form — which `.pdraw .p1` already used and I did not copy.

## Imagery — CC0 / public domain, CORS-clean

**Source: Wikimedia Commons.** The only source tested that serves
`access-control-allow-origin: *`, so `crossorigin="anonymous"` images are
canvas-readable — pixel-level work (palette extraction, dithering,
displacement, WebGL textures) is available.

### Primary body of work

**Kamisaka Sekka 神坂雪佳, _Momoyogusa_ 百々世草 (1909–10)** — Rijksmuseum CC0
scans, 12 plates at 5,800–10,400 px native. Flat, graphic, radically modern
in construction. `assets/curated.json` carries a full `srcset` per plate.

**Anna Atkins, _Photographs of British Algae_ (1843)** — 3 cyanotypes.
Monochrome Prussian blue; the texture lane.

### Rejected

- **JWST / Hubble nebula imagery** — technically perfect, aesthetically
  stock. Overused to the point of being wallpaper.
- Hokusai *Great Wave*, *Red Fuji* — same problem. Sekka's *Tatsunami*
  is a better wave and is not on every laptop sticker.
- **Art Institute of Chicago IIIF** — 403 to curl *and* to Chrome. Dead for
  hotlinking despite an excellent API.
- **Met Museum CDN** — loads bare, but fails with `crossorigin="anonymous"`.
  No CORS header, so no pixel access.

## 3D

- **Poly Haven** — CC0, `access-control-allow-origin: *` on `dl.polyhaven.org`.
  521 models, plus HDRIs for image-based lighting.
- **Khronos glTF samples** — serve fine, but `DamagedHelmet` is the single
  most overexposed model in the three.js ecosystem. Not using it.

## Libraries

CDN is permitted for this preview. Classic (non-module) builds only —
ES module imports are blocked by CORS on a `file://` page.

## Rate limits

The Commons API returns 429 under a burst. Batch titles (3 per request) and
back off exponentially.

## Two traps in Wikimedia image delivery

### curl is blocked; the browser is not

`upload.wikimedia.org` and `thumb.wikimedia.org` return **400 to curl** for
URLs that Chrome loads without complaint — including URLs copied verbatim out
of the API response. An entire round of "broken URL" diagnosis was a false
alarm caused by trusting curl.

**Rule: image URLs are verified in the browser, never with curl.** curl remains
fine for the JSON API, which is not gated the same way.

### Thumbnail widths snap to a bucket ladder

The API's `thumbwidth` field echoes what was *requested*; the URL carries what
is actually *served*:

| requested | URL delivered |
|---|---|
| 640 | `960px-…` |
| 1024 | `1280px-…` |
| 1600 | `1920px-…` |

So rewriting the `/<N>px-` segment by hand fabricates a bucket that may not
exist. Parse the width back off each returned URL and key the `srcset` by
that, which is what `build-manifest.py` now does.

## Exhibit 01 rebuilt, 2026-09-20 — plate 626 measured, the scrub moved to CSS

**Why.** The projected frame was cut from whichever thumbnail the strip's
`sizes` had picked — the 960px one — so each frame had 232 source pixels
stretched to ~600px. The opening was a text-only hero with the plate off
screen, and the run floated two unrelated objects in a black field.

**Resolution ceiling.** The Commons API, asked for a 2560px thumbnail of the
NGA scan (3000px original), returned the *unscaled original* (4.65 MB) as
`thumbnail_unscaled`: there is no bucket between 1920 and the original for
this file. 1920 is the ceiling, 465 source px per frame, one file used three
times (opening object, index, projection).

**Frame geometry, measured on the 1920 thumb (1920×1482).** Each row is a
separately mounted strip: rows are split by dark bands, but frames within a
row are printed edge to edge with only a faint line between them, and the
backdrop carries a ~60px grid of threads, so column-mean profiles find the
horses and the threads before they find the frame edges. What worked: a
1:1 screenshot of the rendered image analysed locally (PIL), rows from
full-width dark runs, columns from the per-column "consistently darker than
both neighbours" score plus the tonal step where one print meets the next.

| | px on 1920×1482 |
|---|---|
| rows (y0–y1) | 35–371 · 409–735 · 775–1094 · 1135–1456 |
| columns (x0–x1) | 25–477 · 478–947 · 948–1419 · 1420–1882 |

Frame widths therefore differ (452, 469, 471, 462 px) and aspects run
1.345–1.476. The gate is fixed at 1.44; each frame fills its height,
left-aligned, with up to 1.5% invisible stretch; frames narrower than the
gate are clipped on the right (`clip-path` per keyframe), never allowed to
show the neighbour's edge. Keyframes were generated from these numbers;
`probes/plate-grid.html` and `probes/plate-raw.html` are the measurement
pages, `notes/evidence/plate-cells.png` the sixteen cuts.

**The stride, read at 3–5× zoom (`notes/evidence/hooves-*.png`).** Frames
2, 3, 4: all four hooves off the ground, legs gathered. 5–6: one hind hoof
down. 7–8: both hinds. 9–11: a hind and a fore. 12–15: forelegs. 16 and 1:
the last forehoof leaving, dust visible. Frame 1 read as a landing until the
leg angle showed it trailing; the earlier per-frame gait labels were replaced
with phase names, which stay true when a hoof is a pixel off the ground.

**Mechanism.** No JavaScript in the run. One view timeline on the runway;
`--i` is a registered `<integer>` stepped 0→15 with `steps(16, jump-none)`;
the projection's `background-size/position/clip-path` and the gate's box are
17-keyframe animations on `steps(1, jump-end)` over the same range, so the
picture, the gate and the counter switch in the same frame. The stride label
is seven real spans whose opacity is `clamp(0, 1 - max(a - i, i - b), 1)`.
Measured under 4× CPU throttle on a scripted scroll through the whole run:
191 frames, median 8.3 ms, p99 10.4 ms, none over 16.7 ms.

**Reduced motion** turns the opening→run transition into a cut on the first
scroll (`steps(1, jump-end)` over a 2% range — `jump-start` with `fill: both`
applies the end value at progress 0, so the cut fired before any scroll); the
frame stepping stays,
because it is the content and it is entirely under the visitor's hand.

## Exhibit 07 rebuilt, 2026-09-20 — colour photographs, a palette that follows them, an instrument per phase

**Why.** The four phases were one treatment (grayscale photograph under a
colour blend) in four hues, so the palette snap was the only thing that
changed; the Warning pill was unreadable in the pink phase; the readings were
invented. The 2018 photographs are the strongest material in the collection
and the tint was throwing them away.

**What changed.** The photographs are shown in colour on one fixed backdrop
that cuts at each break, and the palette angle is set per phase to the hue of
that phase's own light: lava lake at night → terra (0°), crater from the air →
blue-grey (−150°), sparks in the palms → amber (+15°), dusk river → violet
(−115°), steam over the sea → teal (−200°, the short way round from −115°).
Teal clips in sRGB at C 0.16 and comes out muted, which suits steam. Each
break is a dated dashed line, and the panel changes instrument: a
cross-section of the crater with the lake at the rim; the rift line with 24
fissures and the eighth taller; a fountain and cone against a metre scale;
land covered against land made. Readings are USGS figures for the 2018
eruption (first fissure 3 May; lake −220 m by 6 May; 24 fissures by 27 May;
M 6.9 on 4 May; fountain 80 m; cone ≈50 m; ocean entry at Kapoho 3 June;
35.5 km² covered; 875 acres of new land; over 700 structures; 62 collapse
events and more than 500 m of summit subsidence; SO₂ near 200,000 t/d at the
peak). Alert levels are HVO's: Watch/Orange before 3 May, Warning/Red after.
The seismogram is the one simulated element and is labelled so.

**Mechanism, kept distinct from 01.** 01 is scroll-driven (position is the
frame); 07 is scroll-triggered (crossing a line trips a state): an
IntersectionObserver with a one-pixel band at mid-screen sets `data-phase` on
the deck and `--rot` on the root; CSS does the rest (which photograph, which
instrument, which readings). Measured under 4× CPU throttle on a scripted
scroll through the deck: 119 frames, median 8.3 ms, p99 10.3 ms, none over
16.7 ms, with `backdrop-filter: blur(18px)` on the panel over full-bleed
photographs.

**Two layout traps.** A `.phase .txt{max-width:58%}` rule reached the hero
once the hero became a phase section and wrapped the headline to three lines,
pushing the eyebrow under the fixed chrome — hero rules need their own
max-width. On phone, a sticky panel with `height:auto` and
`margin-top:-100svh` shifted the whole text column up by its own height
(the hero started at −643px); the panel now keeps `height:0` and lets its
content overflow, and the text column starts at 0.

## The height-attribute trap, found by the user on 03 and 05, 2026-09-20

Every `<img>` here carries its true `width` and `height` attributes so the
browser can reserve space before the file arrives. Those attributes are
presentational hints: `width="8105" height="6923"` is `width:8105px;
height:6923px` in the cascade. A rule like `.grid img{width:100%;
aspect-ratio:1;object-fit:cover}` overrides the width and leaves the height
hint standing, so the image is laid out 300px wide and 6,923px tall and
`object-fit:cover` magnifies a sliver of it about twenty times. On 03 the four
typhoons became full-height blurry strips and the page grew to 12,230px; on 05
the two Solari boards became tall empty crops. The images were never
low-resolution.

**Rule: any image rule that sets `width` and relies on `aspect-ratio` must
also set `height:auto`.** A script listing img rules with width and
aspect-ratio but no height found exactly these two across `artifacts/`; both
are fixed. 05's boards were also stacked at column width with `sizes` raised
to match, because the crisp version showed how small they had been.

## Type palette and guest display faces, 2026-09-20

**Decision (the user's direction, my structure).** Every subpage gets its own
display voice; the frame stays constant. Switzer, Geist Mono, navigation, the
switch, the wall-label structure and the house curve never change. Melodrama
becomes the institution's face (index, Lexicon index). Each exhibit sets one
guest display face as `--display` and carries the reason in a comment beside
its font link.

**Verified on `probes/type-palette.html`** (25 Fontshare families, one request
each, real headlines at 92px, `document.fonts` enumerated after load):

| face | true italic | verdict |
|---|---|---|
| Boska | yes | 01 · Didone bones for an 1887 plate |
| Zodiak | yes | 03 · sharp, fast, a lively italic for velocity |
| Gambetta | yes | 04 · warm old-style for 1928 botanical plates |
| Rowan | yes | 06 · calm classical serif for an orrery |
| Bespoke Serif, Sentient | yes | palette, reserved for Lexicon specimens |
| Stardom, Britney | no | palette, display-only Didones for type specimens |
| Panchang | no | 02 · extra-wide engineered face for a window that travels sideways |
| Khand | no | 05 · condensed, the cadence of station signage (the flaps themselves letter in Switzer, as Solari's did in Helvetica — corrected 2026-09-22) |
| Tanker | no, caps only | 07 · heavy capitals for warning signage and molten mass |
| Technor, Plein | no / yes | palette |
| Erode, Excon, Alpino, Chillax, Ranade, Gambarino | — | rejected as generic |
| Kola, Kihim, Telma, Array | — | rejected as gimmick (Array kept in mind for a pixel type specimen) |
| Pilcrow | did not load under that name | dropped |

Melodrama itself has no italic: every italic accent the house has shipped so
far was a synthesized oblique. Faces without italics now carry the accent word
in colour alone (`em{font-style:normal}`), never in fake oblique.

**Per-face tuning.** Each face needed its own tracking and size: Didones and
old-styles lose the −.04em display tracking (−.02em), Panchang drops the
headline to 8.2vw because it is nearly twice as wide as Melodrama, Khand and
Tanker go larger because they are condensed, and 07's phase numerals stop
being italic. Verified on all seven pages at 1440 and 390: the guest face is
the computed family of the headline, the italic face is loaded where the
design uses it, no horizontal overflow, no console messages.

Chrome also flags any lazy-loaded image whose box it cannot reserve, even
with `width`/`height` attributes present, once a stylesheet sets one
dimension to `auto`. Every lazy image now carries an inline
`aspect-ratio:W/H` from its own attributes — except where the stylesheet
crops to a fixed ratio (03's square typhoons), because an inline ratio would
win over the stylesheet's.

## Exhibit 05 rebuilt, 2026-09-22 — the Secaucus boards, flap for flap; the first part

**What was wrong** (the user: "cheesy… it only flicked once… amateur"). A
generic dark table in letterspaced Geist Mono, grey squares standing in for
flaps with an empty band through the middle, nothing like the boards
photographed beneath it. The hall ran at 12× with 3–15 minute headways, so a
visitor saw one event at most, and each "flip" was a 90 ms wobble of a whole
glyph, not a flap falling.

**Material first.** The seven curated Commons photographs (4300streetcar,
June 2026) looked at 1:1 at 1920 (`probes/solari-sheet.html`,
`notes/evidence/solari-*.png`). What they show, and the page now reproduces:
one board per line in the line's own enamel — Northeast Corridor red, Coast
blue, Morristown teal, Main Line yellow with black print, Pascack Valley
purple — with the flaps printed in that enamel; the hour flap carries its own
colon, minutes are two digit flaps; destinations and stops are whole printed
name flaps with a split line and pin marks; one letter flap for the track, a
blank status flap; printed, underlined column heads; a black message row of
letter flaps (the three messages used are the ones in the photographs); a red
seven-segment LED clock in the header; the "solari udine" mark. Enamel was
sampled with PIL from the photographs; the hue is kept and the lightness
lifted out of the shade.

**Idea and sequence: object → mechanism → scale → reality.** The Morristown
board is the opening object and wakes blank, then settles unevenly. The bench
slows one destination flap to 520 ms at full width, lays its drum out in
order and strikes through the journey: "it only turns forward" — distance,
not an authored delay, is what makes a board settle like rain. The concourse
shows four more lines, each waking the first time it is seen, 750 ms apart
when seen together. The photographs close it.

**Time.** 30× (a minute every two seconds), opening at 5:44 so the first
departure comes ~10 s in. Each line has a clock-face timetable repeating
hourly; seeded delays (~10%) and cancellations (~2.5%); status blank →
Boarding (4 min) → All Aboard (1 min) → the rows shift up. Morristown's
message alternates every 20 hall minutes; a narrow board turns long messages
in lines. Pause (WCAG 2.2.2) freezes the hall clock; Sound is opt-in.

**The first part.** `artifacts/parts/split-flap.js`, a custom element, is the
reason the charter's "exactly two shared files" law was amended (see
`AGENTS.md`). One module, any drum, value as real DOM text, themed through
`--flap-*` properties, optional synthesized sound, reduced motion and
off-screen modules cut instead of turning.

**Performance — four designs, measured, not guessed.**

| design | result | cause |
|---|---|---|
| `--p` custom property per module per frame; CSS derives rotateX and shade | 4× hero wake p95 62 ms, 56/120 frames > 33 ms | an inherited custom property restyles the whole shadow subtree (~17 style objects per module) |
| a pair of compositor animations (rotateX + brightness) per flap | 4× hero wake median 215 ms | every flap promotes both leaves to layers and cancelling demotes them: layer churn and re-raster |
| flat fall: scaleY + colour shade, one write per leaf | 4× hero 13.9 ms median, but 1× four-board wake still 14 ms median, 168/435 frames > 16.7 | not JS — the same with or without CPU throttle. Trace: Layerize 629 ms, GPU process 5.6 s in 7.7 s. ~5,600 paint-property nodes at rest (static `translate` on lettering, axle and pins; overflow clips on four halves; paint-containment clip on the host) walked every frame |
| rest state is one unclipped face with the axle drawn over it; halves exist only while turning; no static transforms; `contain:size layout style` | 1× four-board wake median 7.0, max 14.5, 0 > 16.7. 4×: opening wake max 14.7 (0 > 16.7), bench in true 3D max 7.9, running max 27.2 (1 frame), four boards woken at once by a jump p99 21.3 | — |

**Rule: a component instantiated by the hundred must cost nothing at rest.**
True perspective is kept behind a `depth` attribute for the one large flap
where it shows; at board sizes and 60–95 ms per flap a foreshortened fall
reads the same.

**Two custom-element traps.** (1) Defined before the document is parsed,
`connectedCallback` fires at the start tag, before the element's text exists:
the bench flap initialised blank. The part now reads its value at
DOMContentLoaded or on first use, whichever comes first. (2) A drum
registered after the element connects is adopted on first turn.

**Verified** at 1440 and 390, night and day, reduced motion (no module ever
enters the turning state; departures cut), no console messages, no horizontal
overflow, Khand / Switzer 500 / DSEG7 Classic italic loaded, Sound creates
and suspends its AudioContext, Pause freezes the clock. Evidence:
`05-before-*`, `05-after-*`.

## Exhibit 02 rebuilt, 2026-09-22 — eight passes along the way the station flies

**What was wrong.** The track's `animation-range: contain …` sat on a
`scroll(root)` timeline, where `contain` means nothing, so the window moved
across the whole page instead of the pin and the exit dragged half-cropped
photographs and the HUD upward. The route jumped around the planet (New York,
Northern Europe, Moscow… then back west to the Nile). The clock was the
scroll position dressed as time; the orbit dial and the altitude were
decoration. The hero was the collection's shared full-bleed-photo pattern.

**The idea: ride the station east across the night side.** The Commons
descriptions gave every photograph a date, an expedition and, for six of
them, the altitude (262 mi → 422 km, etc.); Moscow and Central Asia are
12 frames apart on the same pass, 16 September 2024. Eight of the nine
passes lie along the shape an ISS ground track actually has — climbing to
northern Europe, then descending south-east over Moscow, Kazakhstan, India
and Southeast Asia to Melbourne — so they are ordered by it. The Nile sits
too far south-west for that line and was dropped (still curated).

**The instrument.** NASA Earth Observatory's Black Marble 2016
(`BlackMarble20161km.jpg`, 43,200 × 21,600, equirectangular, public domain),
added through `build/curate.py` with a 3840 bucket requested only for it.
Crop lon −105…165, lat 66…−48, so longitude and latitude map straight onto a
270 × 114 viewBox. The route is a centripetal Catmull–Rom spline through the
eight places (the uniform spline looped west between Southeast Asia and
Malaysia); x is monotonic, so on the map the route is always east. Arc-length
fractions at the dots were sampled once and written into the keyframes.
Verified on `probes/02-map-probe.html`: dots land on the lights of New York,
Moscow, the strait and Melbourne; `offset-path` on an SVG element uses
viewBox units, so the marker lands on India at exactly 61.014%.

**Readouts are measured, not decorative.** Ground covered is the sum of
great-circle distances along the route (22,858 km); the time is that
distance at 7.66 km/s (49:44); altitude is each photograph's own, or "not
recorded". Both counters are registered `<integer>` properties interpolated
by the scroll animation and printed through `counter()` — mm:ss with
`round()` and `mod()` inside `counter-reset`.

**Sequence (one view timeline, no script).** Opening: the whole route on the
night map, the title beside it. 0–12% the map docks into the corner (house
curve) while the window arrives; 15–85% one pass is centred every 10% and
the station, the drawn route and the counters move with it; labels switch
halfway between passes (`--i` stepped over 10–90%). 88–92% the window
clears; 91–100% the map opens again with the route complete and the arrival
— "22,858 km" — takes the title's place. Phone: the map lifts under the
words at the opening and closing and docks at the foot during the run.

**Reduced motion** (forced on `probes/02-reduced.html`): the map docks in one
cut, the window steps from pass to pass at the midpoints, the station and
counters jump with it; multi-keyframe animations use `steps(1, jump-end)`
over a range shifted half an interval earlier so the jumps land at the
midpoints too.

**Verified** 1440 and 390, no horizontal overflow, no console messages, no
palette tokens used (the page is the night in both palettes), 4× CPU
throttle scripted scroll across the whole run: median 6.9 ms, p99 13.6 ms,
one frame over 16.7 ms. Evidence: `02-before-*`, `02-after-*`.

## Exhibit 06 rebuilt, 2026-09-22 — an orrery that is true where it claims to be

**What was wrong.** No Venus, Pluto included ("eight rings" for Mercury…Pluto);
periods that "keep their order, not their scale" (Neptune ran 26× Mercury's
period instead of 684×); a false-colour green ultraviolet Sun; a "light"
layer that was a decorative glow; names sitting on their planets; an
exploded view that ran off the stage; on a phone, the model below the fold.

**The idea: a true orrery.** It opens on today — each planet at its
heliocentric longitude from JPL's approximate Keplerian elements (Standish,
1800–2050: e, L, ϖ and their rates; Kepler's equation solved per frame; the
orbital tilts ignored) — and runs at the true relative pace, one Earth year
every four seconds, so the inner planets whirl and Neptune creeps (Kepler's
third law, visible). Distances and sizes are not to scale and the copy says
so; directions and periods are. Checked against the sky of September 2026:
Earth on the 0° line at the September equinox; Uranus ≈ 63°, Saturn ≈ 10°,
Neptune ≈ 3°.

**The layers now mean something.** L0 the ecliptic — the plane, a degree
ring and the ♈ direction the longitudes are measured from; L1 the orbits;
L2 the bodies; L3 the names, which billboard to face the viewer when the
model tilts and drop leaders to their planets as the layers part, like an
exploded technical drawing.

**Material.** Venus (Mariner 10 real colour, 480 px, public domain) and the
Sun in visible light (SDO HMI continuum, 10 August 2024, public domain)
curated through `build/curate.py`, which now keeps a small file's unscaled
original when the API returns it (Venus is smaller than any bucket). Saturn
keeps its rings: a soft elliptical mask instead of a blend mode, because
`mix-blend-mode` is isolated inside preserve-3d layers. The model's sky
stays dark in both palettes; the side panel follows the switch.

**Verified** 1440 and 390 (phone order: title, model, controls, intro — the
model is in the first screen), night and day, reduced motion (opens on
today, still, with a Run button), no console messages, no horizontal
overflow; 4× CPU throttle while running: flat, exploding and exploded all
under 16.7 ms (max 13.2 ms). Planet sizes are measured once per resize, not
per frame. Evidence: `06-before-*`, `06-after-*`.

## Exhibit 03 rebuilt, 2026-09-22 — velocity read on the scale that measures storms

**What was wrong.** One frozen composition for ~3,800 px — only the eye
turned. Scroll velocity was displayed as Florence's "sustained wind",
"pressure" and "Category TS" under a real, dated storm: false on its face
(NASA's caption for these photographs gives 130 mph, Category 4). The eye
turned clockwise; a northern-hemisphere hurricane turns counter-clockwise.
The loop ran every frame forever. The headline ran into the disc.

**The idea: both signals of one scroll, kept apart.** Position walks the
three minutes the station spent over the storm — NASA's external-camera
frames stamped 11:50 (over the horizon, the robotic arm in view) and 11:52
(straight down into the eyewall), then Alexander Gerst's long-lens view of
the eye (11:51). Velocity is measured in px/s and read, at a declared 30 px/s
to the knot, on the real Saffir–Simpson bands (34 / 64 / 83 / 96 / 113 /
137 kt), beside Florence's actual reading from the caption (130 mph = 113 kt,
the bottom of Category 4). Over the eye, the whole storm turns
counter-clockwise at a rate proportional to your knots, and stops when you
stop.

**Composition.** The eye frame takes two thirds of a 7,200 px pin so a
real throw lands inside it (a scripted 4,000 px/s throw with momentum moved
2,548 px and stayed in the pin). The eye sits at the centre of a square as
wide as the screen's diagonal (`hypot(100vw, 100svh)`), so it can turn any
distance without an edge. The title carries its own scrim and takes it away.
Teleports — a jump of more than a screen in one frame — are not throws;
readings cap at 200 kt. `sizes` describe the width actually drawn: a 3:2
cover on a portrait phone is ~330vw wide, the turning eye ~450vw.

**Verified** 1440 and 390, no overflow, no console messages, reduced motion
forced on `probes/03-reduced.html` (frames cut at 16.5% and 33%, no push-in,
no rotation, the gauge still reads), 4× CPU throttle across the whole pass
including a throw over the turning eye: median 6.9 ms, max 13.8 ms, none
over 16.7 ms. Frames curated through `build/curate.py` (the eye at 3840).
Evidence: `03-before-*`, `03-after-*`.

## Exhibit 04 revised, 2026-09-22 — prints that develop on their own clocks, and their real names

**What was wrong.** Each plate was revealed by a clip from the bottom over
`entry 0% → cover 38%`, so for its first stretch on screen a plate was
mostly an empty box — the black voids. Captions read "Plate 11", "Plate 11,
second study", "third study": wrong (they are plates 111, 115 and 119) and
empty. The lede was about the mechanism ("that disagreement is the whole
piece"), the junior tell. The Getty print appeared twice.

**Names from the book.** The Rijksmuseum records give each loose plate's
printed number and "…facher Vergrößerung" but no species. The 1929 English
edition, *Art Forms in Nature* (Commons, public domain), carries the plate
descriptions: species, part and enlargement for all 120 plates, same
numbering. Text extracted with `pdftotext`; the OCR misread 82–89 as 62–69
on one page, so plate 84 is the second "64" entry (Cirsium canum, flower
head ×12) — sequence checked against its neighbours, and plates 46 (ostrich
fern frond) and 115 (milkweed umbel) checked against their images.

**Develop, don't reveal.** Each print now comes up out of its own paper (a
`--paper` overlay sampled from the scans, #f6f2e3, fading 0.93 → 0 over
`entry 0% → cover 40%`) — a photogravure in the bath, on its own clock. The
plate is always present, so there is no void; only its tone arrives. The
page rail and each plate's own progress number stay as the instruments.
Plates run in book order.

**Also** `house.css` gives `.back` and `.theme` a halo of the page's own
ground, so the fixed chrome stays legible over whatever scrolls beneath it
on every page.

**Verified** 1440 and 390, no overflow, no console messages, 4× CPU throttle
scripted scroll through the whole garden: median 8.3 ms, max 16.5 ms, none
over 16.7 ms. Evidence: `04-before-*`, `04-after-*`.

## Closing the audit, 2026-09-22 — 01, 07, the index, and 03 by day

**01.** The legend's orange row was a fixed `.hot` on frames 2–4, so it read
as "the frame you are on" whatever frame you were on. Each row now carries its
frame range (`--a/--b`, plus `--a2/--b2` for "1 · 16", which wraps) and lights
by the same clamp the frame labels use against the stepped `--i`: only the
stride on screen is orange. Checked at frames 3, 8 and 16.

**07.** The "Seismogram · simulated trace" label was absolutely placed over
the SVG, so bursts in phases 3–4 wrote through it. `.seis` is now a two-row
grid, label above, trace below, and the SVG clips its own row — no amplitude
can reach the label. Phase 4 said "half past ten at night" over a daytime
aerial of Kapoho Bay; its copy now describes what the photograph shows (June,
the bay boiled away, 875 acres of new land).

**Index.** The lede was a synthesized oblique of Melodrama (it has no italic);
it is set roman. The "House curve" strip that recited the bezier to visitors
is gone (a copy-voice leak). Card copy rewritten for the rebuilt 02–06, the 02
card shows the night map, each card title is set in its exhibit's guest face,
and the footer credits the frame faces plus "a guest face for every exhibit".

**03 by day.** The fixed chrome was hard-set light for the storm photographs,
so in the day palette it ghosted on the paper sections after the pass. It is
now light over the photographs and takes the palette once the gauge — the
stage's last band, set on the page's ground — rises under it: a registered
`--paper` cuts 0 → 1 (`steps(1,jump-end)`) on the runway's view timeline,
scoped to `body` with `timeline-scope`, range end
`exit calc(100% - 29px - var(--gh))`. Colours mix from `--paper`, so hover
still works (animating `color` itself would override `:hover`). The animation
sits on the two chrome elements, not on `body` — an inherited custom property
animated on `body` would restyle the whole page. `--gh` moved to `:root` so the
chrome can read it. Measured: the cut lands with the gauge's top at 29 px, at
1440 (gauge 135 px) and 390 (gauge 188 px), in both palettes.

**Regression sweep** after the shared `house.css` change: index and all seven
at 1440 and 390, scrolled end to end — no console messages, no horizontal
overflow, no broken or stalled images. Evidence: `07-after-*`,
`01-after-legend-1440`, `index-after-1440`, `03-before/after-day-chrome-1440`.

## Out of sketch, 2026-09-22 — git, a permanent address per page, and what crawlers see

**Stack.** Plain HTML, CSS and a little JavaScript; no framework, no bundler.
Nothing here is app-like (no state, no data, no routing), readable source is
part of what the site offers, and build-time static HTML is exactly what the
discoverability research endorses. No animation library by default either:
native motion is the exhibit, and it runs without our script working every
frame. If an advanced piece needs springs with momentum, shape morphing, line
splitting, long choreography or a 3D scene, anime.js (4.5.0, MIT, UMD build
available) is the pick, loaded only on that page from a pinned copy.

**Git.** `renocrypt/mocubix`, created private; it must turn public to publish
(Pages on the org's free plan). Ignored: `.DS_Store`, `.claude/`,
`notes/evidence/`. The Wikimedia User-Agent contact in `build/*.py` is now
the repository URL, so no personal email is in the history.

**Addresses.** `artifacts/` became `site/`, one folder per page:

| was | now |
| --- | --- |
| `01-scroll-timeline.html` | `/annie-g/` |
| `02-horizontal.html` | `/night-side/` |
| `03-velocity.html` | `/florence/` |
| `04-view-progress.html` | `/urformen/` |
| `05-autonomous-time.html` | `/departures/` |
| `06-live-teardown.html` | `/orrery/` |
| `07-theme-rotation.html` | `/kilauea/` |
| `lexicon.html` | `/lexicon/` |

Permanent once published. Folder addresses do not open from disk, so preview
is `python3 -m http.server 8765 --directory site`. The Lexicon generator was
checked to reproduce the committed page byte for byte before the move and the
rewritten page byte for byte after it. Verified over the local server: 52
local references resolve, every page loads the shared files, 196 images, no
overflow; the only 404 is `/favicon.ico`, which the site has never had.

**What crawlers see.** Raw HTML text against the DOM after scripts, per page
(headless Chrome `--dump-dom`): index, 01–04 and 07 carry every word in the
HTML (scripts add only the switch's label; 06 adds its live date and
readouts). **05 builds 145 words (~28% of its text, the boards' destinations
and messages) in script, and the Lexicon 722 of 4,696** — a crawler that runs
no JavaScript misses them. The charter now says it outright: a script may
move what the HTML holds, never write it. Also missing site-wide: canonical
addresses, share previews, favicon, sitemap, 404 page; the index has no
description and is titled "Exhibition slice 01"; 07's five photographs and
02's map carry `alt=""`. Sizes are 18–141 KB against Googlebot's 2 MB, titles
at the top. Per the research (§5), no `llms.txt` and no schema aimed at AI.

**The Lexicon plan changed with it.** One page with `#effect` links breaks
hard constraint 11 (fragments are not addresses), so each effect gets a real
page, bound like a book: the entrance shows every effect as a small moving
preview, each page carries the contents and next/previous, and the next page
is prepared in advance so turning is instant.

## One rule for what text stands on, 2026-09-22 — replacing three patches

**What the user found (day palette).** The orrery's switch blurred: the house
halo was a 12 px glow of the page's ground, so by day a paper glow sat on
the black sky. Florence's way back painted dark ink on the black storm photo.
Kīlauea by day set dark ink on dark photographs and washed every photograph
in a paper veil to compensate. They asked for one consistent answer, not
another patch.

**Why Florence failed.** Its chrome took its colour from `color-mix()` over a
registered `--paper` animated by a view timeline. `getComputedStyle` said
`#E9E4DC`; the pixels said `(28,24,20)`, the day ink. Pinning the same value
inline repainted it at once `(232,228,221)`: Chrome recomputed the colour but
did not repaint text whose colour depends on a scroll-animated custom
property. My earlier check read computed style only. Rule now in the charter:
measure what is painted — contrast from screenshot pixels.

**The system.** Ink follows the surface it stands on:
- *ground* — the page's own surface, takes the palette;
- *plate* — a piece of the ground laid over something else (the chrome,
  03's gauge, 07's panel), takes the palette;
- *material* — a photograph, 02's night, 06's sky, 05's enamel — keeps its
  own light. `[data-material]` re-declares the night tokens (and restarts
  `color`, since inherited colour arrives already computed), so words laid on
  it stay light in both palettes; words on a photograph carry their own shade,
  as 03's title already did.

The way back and the switch are defined once in `house.css`, on a plate at
90% of the ground with a 14 px backdrop blur, text in `--mid`, a focus ring
for keyboards. Deleted: every page's `.back` rules (7 copies), 02's and 07's
halo overrides, 03's `--paper` scroll switch, the house halo. 02's body is
material (its plate is night, like the page); 07's `.backdrop` and
`main.phases` are material (the panel and footer follow the switch).

**Measured from pixels**, text against plate: by day 5.5–6.9:1 (lowest: the
switch over the orrery's black sky), by night 8.1–8.8:1, at 1324 and 390 —
AA for small text is 4.5:1. By arithmetic a 90% plate holds about 5.7:1 over
pure black by day and 6.9:1 over pure white by night, whatever is beneath.

**Found on the way.**
- 07's phase logic trusted the section crossing the middle; the last
  section ends above the middle before the foot of the page, so a jump (End,
  a reload at the bottom) left the previous phase on screen. It now asks, on
  every crossing, for the last section whose line has crossed. Checked: jumps
  both ways, reload at the foot, and each break 4 px either side of its line.
- The new text shades widened 07 to 447 px on a phone. The overflow sweeps
  had compared `scrollWidth` with `innerWidth`, which on a phone grows with
  the overflow and hides it; the right measure is `clientWidth`. Clipped
  (`.phases{overflow-x:clip}`) and all nine pages re-swept at 390: none.
- Python's `http.server` sends no caching headers, so Chrome kept serving the
  old `house.css`. `build/serve.py` serves `site/` with `no-store`.

Evidence: `07-day-*` (before), `07-day-after*` (after), `chrome-*` (each page's
chrome, with the rects the contrast was read from).

## Ready to be found, 2026-09-22 — the address, share cards, credits

**Address.** `https://mocubix.renocrypt.com/` (the user's choice). Every page
carries its canonical address, favicon links and share tags (`og:*`, a
`summary_large_image` card) right after its description, above the
stylesheets. `robots.txt` allows everything and names `sitemap.xml` (nine
addresses). `404.html` uses root paths, because Pages serves it at whatever
address was asked for; `build/serve.py` serves it the same way locally.

**Share cards.** Each is the page's own opening, rendered at 1440×756 CSS px,
2×, night palette, chrome hidden, scaled to 1200×630 (48–133 KB). Kīlauea's
card is phase 3 (Fissure 8, USGS, public domain) rather than the opening's
CC BY-SA lava lake. Florence's card and the index card (which shows the
Florence thumbnail) carry the photograph's credit in the corner.

**Favicon.** The switch's half-disc in terra on the night ground: SVG, a
32/16 px ICO, and a 180 px touch icon.

**Credits.** An audit of every Commons image against each page's visible
credits found the index crediting none of its three CC photographs, and
Florence calling the eye CC BY-SA 3.0 IGO where the file is CC BY-SA 2.0.
Fixed, and every CC licence named on the site now links to its deed (the 2.0
licences require the link). "Private preview" is gone from the index footer
and the Lexicon's kicker. The index is now titled "Mocubix — Seven ways a page
can move" and has a description; Kīlauea's five photographs and Night side's
map have real alt text.

**Verified** over the local server: nine pages, one canonical each matching
the sitemap, all share tags present, share images 1200×630, zero broken local
links, the 404 page served with status 404.

## Published, 2026-09-22 — https://mocubix.renocrypt.com/

The user approved making the repository public and serving it at the
subdomain. Before the flip, the whole history was scanned for the personal
email and token-like strings: none.

- **Pages by Actions.** `.github/workflows/pages.yml` uploads `site/` and
  deploys it (checkout v7, configure-pages v6, upload-pages-artifact v5,
  deploy-pages v5 — the latest releases on the day). It runs only when
  `site/` or the workflow changes, so notes and research never redeploy.
- **Domain, in the safe order.** The custom domain was set on the repository
  first, then one Cloudflare record added: CNAME `mocubix` →
  `renocrypt.github.io`, proxy off, TTL auto — the same as `futur` and `kb`.
  It went through the user's sanctioned wrapper (`armada/bin/cf`), which reads
  the token itself; the token never entered a command line or this log.
- **The certificate stalled** at "DNS check in progress" for over twenty
  minutes (a redeploy did not help), because the domain had been attached
  before its record existed. `renocrypt.com` is verified for Pages (both the
  organization and the user hold a `_github-pages-challenge` TXT record), so
  removing and re-adding the domain carried no takeover risk; authorization
  succeeded and the certificate was approved within a minute. HTTPS enforced.
- **Verified live:** Let's Encrypt certificate for the host (to 2026-12-22,
  renewed by GitHub); every page, `robots.txt`, `sitemap.xml`, favicon and
  share cards 200; unknown addresses 404 with our page; `http://` and
  `renocrypt.github.io/mocubix/` both 301 to the canonical address; in Chrome,
  no console messages, no broken images, Kīlauea lands on phase 4 at its foot.

## Chrome only, 2026-09-23

A Playwright checker across Chromium, WebKit and Firefox (with downloaded
browsers and a CI gate) was built and removed within the hour: the user's
call, and the right one — "nobody who does UX design would use Safari for
design; Chrome is the one to go", Firefox is single-digit share, and the
weight was not worth it. Verification stays in Chrome through DevTools.

Two small changes from that hour are kept because they are simpler in any
browser: Night side's distance counter is fed `calc(var(--km))`, and each
Urformen plate's rail now reads the same `--p` as the number beside it (one
clock, not two animations that could disagree). Both verified in Chrome:
the counter reads 8011 km at 35% of the page; rails read 0.47 and 0.42
against 47% and 42%; no overflow, no console messages.

## The Lexicon in three layers, 2026-09-23

The user's verdict on the one-page Lexicon: scrolling past 41 terms is too
much, but the card format ("a quickie way to know what each effect is
about") is good, and fuller individual pages should come gradually. So:

- **Index** (`/lexicon/`): one screen. A find field in the display face
  matches names and aliases from the start of words ("scrolltrigger" finds
  Pinning & Scrub; "pin" no longer lights snapping), the rest step back
  without anything moving, and hovering a term puts its meaning in a caption
  line. The chosen word carries a cross-document `view-transition-name` into
  the term page's title; speculation rules prerender on hover.
- **Pillars** (`/lexicon/<pillar>/`): the cards, one pillar per page — five
  pillars now, Scroll split into Scroll-driven (13) and Scroll behaviour (11).
- **Terms** (`/lexicon/<term>/`): 41 pages with the pillar beside them, ← →
  to turn, each to be elevated into its own showcase in turn.

The demos moved out of the old template into `site/lexicon/lexicon.css` and
`lexicon.js` (every block already returned when its demo was absent); two
scoping slips (term-link styles catching pillar-name links) were caught in
Chrome and fixed. Verified in Chrome through DevTools: all five pillar pages
and sampled terms without console messages or overflow, index fitting one
screen at 1324×725, phone at 390.

## The first showcase: Scroll Markers, a journey outward, 2026-09-23

**Why this one first.** The user's bar: the most beautiful, dazzling, varied
motion, and breadth of material. Webb's images are material the site had not
touched, and Chrome's native carousel (`scroll-marker-group`,
`::scroll-marker`, `:target-current`, `::scroll-button()`) is exactly the
kind of capability the Lexicon exists to show — built entirely in CSS here.

**The idea.** Nine public-domain Webb images in order of how far their light
has come; the scroll markers are the stops, each a thumbnail carrying its
distance. Every figure is sourced: Jupiter from NASA's Jupiter facts
("sunlight takes 43 minutes"), Rho Ophiuchi 390 ly, Orion Bar 1,350 ly,
Cassiopeia A 11,000 ly, Cartwheel 500 million ly and the Deep Field (cluster
at 4.6 billion years, one galaxy's light 13.1 billion years) from NASA
releases; the Southern Ring 2,500 ly from ESA/Webb; the Pillars 6,500 ly and
the Cosmic Cliffs 7,600 ly from the images' NASA descriptions.

**How showcases work (for all that follow).** A module in
`build/showcases/<term>.py` gives TITLE, LEDE, optional GLOSS, HOW (the real
code), NOTE and `render(works)`; styles sit beside the page in
`site/lexicon/<term>/showcase.css`. The generator gives that term a showcase
page (header, full-bleed stage, then details, pillar list, pager), marks it
with a terracotta dot in the index and pillar pages, and keeps the quick card
on the pillar page. `build/curate.py <kind>` now fetches just one kind, with
the 1920 and 3840 buckets for material shown full-bleed.

**Craft notes.** Subjects shown whole take their own shape right of centre
and feather into the dark (their photographs' black is never the stage's
black, so a contained image shows its frame otherwise). Marker thumbnails
are cover-fitted with the distance set inside them. The arrows sit together
at the lower right, clear of the captions.

**Found on the way.** Japanese and Chinese in the Lexicon's footer, one alias
and one code comment drew as boxes: the system's Han fallback is missing on
this macOS 27 install (even Latin in "PingFang SC" drew boxes). The Lexicon's
sans and mono stacks now fall to its own Source Han Serif webfont before the
generic family, loading only the ranges used.

## The second showcase: Word Scrub, endless forms, 2026-09-23

**The idea.** The closing paragraph of *On the Origin of Species* (first
edition, 1859, p. 490, checked against Wikisource), lit a word at a time by
the scroll. Its four sentences take turns in one pinned place. Some words
call up a plate from Haeckel's *Kunstformen der Natur*: the black-ground
engravings are screened into the dark so only the forms stay (lichens and
fungi entangle at "entangled bank"; diatoms, ammonites at "Extinction";
crabs, then antelopes inverted to silver at "higher animals"; radiolarians
at "grandeur"). From "endless" on, every word brings one of twelve colour
plates, arriving in silver and blooming. The famous phrase keeps its light.
Material the site had not touched: a text, and lithographs.

**How it is built.** No script. The build wraps each word in a span and
writes where each sentence sits in the reading (`--a`, `--b`); one view
timeline spans the run; each word's slice comes from `sibling-index()` and
`sibling-count()`, and a plate keyed to a word carries the same numbers.
The pace (`--pace`, per word) and the overlap (`--w`, five words) are CSS
knobs. Without motion, the paragraph is set whole beside the colour plates.
Nineteen public-domain plates, curated like everything else; Tafel numbers
checked against the scans.

**Along the way.** The Lexicon's bar is one line everywhere now: where it
is narrow, the pillars slide under the brand and the current one starts in
view (`scroll-initial-target`). Its height is one value, `--bar`, which every
pinned stage reads. Showcases name their own material in the footer and can
add a credit line. `curate.py` also asks Commons for 330 and 500 px, so small
tiles stop downloading 960 px files. Chrome paints the whole reading at 120
fps with a p99 frame of about 10 ms.

## The third showcase: Image Comparison Slider, where the ice was, 2026-09-23

**The idea.** Five views in Glacier National Park, each photographed from the
same spot decades apart (1907–2025), from the park's repeat-photography
project and archives, all public domain: Grinnell Glacier from Lower Grinnell
Ridge (1910 | 2025), Jackson Glacier below Mount Jackson (1914 | 2020), Sperry
Glacier below Mount Edwards (1907, Morton J. Elrod | 2023), Jackson Glacier
from Going-to-the-Sun Road (1941, Marian Post | 2025) and Boulder Glacier's ice
cave (1932, T. J. Hileman, four people standing in it | 1988, Jerry DeSanto,
rubble). The lede's numbers are the USGS's: about 80 glaciers larger than
0.1 km² at the Little Ice Age peak, 32 by 2005.

**Registration is the craft.** "Same spot" photographs are never framed alike
(Grinnell's 2025 frame is turned 3.2°, Road's is zoomed 1.5×), and a divider
across misregistered pictures lies. `build/register.py` picks the most
contrasty patches on each pair's stable rock, finds each in the later picture
by correlation, keeps the placement most matches agree on, fits scale, turn
and shift by least squares (worst residual under 3 px of 960) and computes the
window both pictures fill. Checked by red/cyan overlays and checkerboards, and
at the divider in Chrome. A global edge-correlation search was tried first and
found false optima; two candidate pairs (Gem Glacier from Mount Gould, Grinnell
from Mount Gould) would not register and were dropped.

**The control.** A native range input, invisible over the whole picture:
drag anywhere, click, arrow keys, screen readers. `showcase.js` (a dozen
lines) hands its value to `--x`, and the first time a pair is seen the
divider eases from the whole old picture back to the middle. The handle is
clamped inside the frame with container units.

## The fourth showcase: Vertical Writing Mode, the narrow road, 2026-09-23

**The idea.** The opening of Bashō's *Oku no hosomichi* (1702), the preface
and the departure with both haiku, set as a handscroll that the page's scroll
unrolls from the right between two rolls: the unread part thins on the rod at
the left while the read part gathers at the right. The scroll has its own
front (an indigo cover with a title slip, then gold-flecked endpaper), the
English runs sideways between the passages, Buson's 1778 painting of the
leave-taking is mounted on paper of its own colour, and his fan painting of
the two travellers walking on is cut from its mount and pasted on. A colophon
sets its figures upright (`text-combine-upright`). All the characters are text.

**The text.** Sugiura Shōichirō's edition (Iwanami bunko, 1957) as published by
Aozora Bunko, with a selection of its readings as ruby and its repetition mark
〻. Japanese Wikisource's text (a 1911 edition) was set aside: unpunctuated,
and its 「行春や鳥は啼き魚の目は泪」 departs from the haiku as it is known. The
face is Noto Serif JP (the Japanese Source Han Serif) from Fontsource, on this
page only; the Lexicon's own Han face is the Chinese cut, whose shapes differ.

**Craft notes.** A column is 13.4 em long by construction, so the size follows
the scroll's height and the columns break the same everywhere; a haiku is set a
size smaller so that it keeps to one column after its drop. The run's length is
estimated from the text's column count so the scroll unrolls at about 1.4× its
own pace; the translation itself needs no measure (`100cqw - 100%` to 0). The
fan's mask is an annulus about the point its ribs meet, between its outer ribs,
fitted to the scan (centre, radii, angles). The endpaper's gold is scattered by
the build from a fixed seed. A class named `cover` collided with an old demo's
absolute positioning; renamed. Without motion the scroll lies open as a native
vertical-rl scroller, which starts at its right end by itself.

## The fifth showcase: Difference Inversion, every tone but one, 2026-09-23

**The idea.** One line of white type, "Every tone but one", held in the middle
of the screen and set to `mix-blend-mode: difference`, while four of Ansel
Adams's photographs for the Department of the Interior (1941–42, National
Archives, public domain) pass beneath it — the Tetons and the Snake River,
Old Faithful at dusk, Yellowstone Lake, the Giant Dome in Carlsbad Caverns —
and then the eleven zones of the Zone System he worked out with Fred Archer,
pure black to pure white. The line turns into the opposite of every tone it
crosses, and on Zone V, middle grey, it all but vanishes. The one weakness of
the effect is the payoff, and Adams's own scale names the tone.

**How it is built.** No script. The stage is isolated so the line blends only
with what is on it; the line is sticky with no height in flow, so it is already
at the middle when the first print arrives. The zones are `lab(n×10% 0 0)`,
even steps of lightness, and each label takes the lightness half a scale away
with `mod()`, so every numeral reads on its own band. Facts sourced: the Zone
System (Wikipedia), the Tetons print on the Voyager Golden Record (NASA's list),
the captions (National Archives, via their Commons records). Chrome holds
120 fps through the whole walk, p99 frame 10 ms.

## Share cards for the showcases, 2026-09-23

Each showcase now has its own 1200×630 card (`site/share/lexicon-<term>.jpg`),
taken in Chrome at a telling moment of its stage — the Pillars of Creation,
Darwin's last line with the colour plates, Grinnell 1910 | 2025 at the
divider, the scroll's cover and first columns, Old Faithful under the inverted
line — with a small "Mocubix Lexicon · <term>" plate. The generator uses a
term's card when the file exists, otherwise the Lexicon's. The Lexicon's own
card was stale (it still showed the one-page Lexicon) and was retaken from the
entrance. The showcase dot in the index is now held to its term's last word,
so it never wraps onto a line of its own.

## The sixth showcase: Ken Burns, slower than attention, 2026-09-23

**The idea.** Six photographs made for the Farm Security Administration,
1936–38 (Library of Congress, public domain), run as a documentary: Rothstein's
farmer and sons walking into the dust storm, Lange's half-buried Coldwater farm,
her "Tractored out" furrows, Rothstein's steer skull, Evans's Allie Mae
Burroughs, Lange's Migrant Mother. Each has its own authored move — in on the
walkers, across the buried fence to the house, up the furrows to the house on
the horizon, a drift from the skull along its shadow, up from the collar to
the stare, out from the mother's face to her children — nine seconds a
picture, a two-second cross-dissolve, a lower third with the Library's caption,
and a reel of six hairlines. Resting the pointer holds the film.

**How it is built.** No script. A move is two focus points and two scales: the
picture is cover-fitted with `object-position` and `transform-origin` on the
focus (two registered `<percentage>` properties, so they interpolate), and
`scale` pushes in or pulls out about it — the frame is covered at any shape of
screen, phone portrait included. One 54 s cycle per picture, staggered by
`--i`; z-index keyframes put the incoming picture on top while it dissolves in.
Chrome holds 120 fps through a dissolve (p99 10 ms), though the focus animates
on the main thread. The Dust storm scan includes the print's edge, so its move
starts at 1.08. The card uses the Coldwater farm rather than anyone's face.

## The seventh showcase: Duotone, two inks — and the demos scoped to their cards, 2026-09-23

**The idea.** Six of William P. Gottlieb's jazz portraits (1946–47; the
collection entered the public domain at his wish on 16 February 2010) printed
as record sleeves, two inks each in the Blue Note tradition: Billie Holiday in
blue, Charlie Parker in orange, Thelonious Monk in green, Sarah Vaughan in
pink, Ella Fitzgerald in gold, Billy Strayhorn in teal. Scrolling in presses
each sleeve from its grey into its inks; a row of ink choices (real radio
inputs, CSS `:has()`, pinned while the sleeves pass) gives all six one pair
and shows how duotone makes disparate photographs a set; resting the pointer
lifts the ink. The sleeve's type is printed in the same two inks.

**How it is built.** Exact, not approximate: the dark ink is the ground and
the light ink lies over it through a mask made of the photograph's own
luminance (`mask-mode: luminance`; Commons serves CORS), so every grey lands
on the line between the inks. Both inks are registered colours, so a change of
pair eases; the press (`--p`) and the lift (`--h`) mix the inks toward black
and white, where the sleeve is the photograph. The ink rules are written by the
build from the module's one list of pairs.

**The systemic fix.** Three showcases in a row inherited an old demo's rules
through a shared class name (`.cover`, `.frame`, `.duo` — the last made the
stage a scroll container and killed the pinned ink row). The demos' styles now
live inside `@scope (.spec)`: verified in Chrome that scoped `@keyframes`,
`@property` and `@media` work, that `:root[data-theme="day"] :scope …` matches
(a bare `:root …` does not inside a scope), and that the cards still render
in both palettes. The demos' reduced-motion rule (`*{animation-duration:1ms}`)
had been global — it would have left the Ken Burns film black for visitors who
prefer less motion — and now applies to the cards alone.

## The eighth showcase: Kinetic Drag, throw the Roman world, 2026-09-23

**The idea.** The Tabula Peutingeriana — every road of the Roman Empire on one
parchment scroll 6.75 m long and 35 cm high, from the Channel to India —
laid out whole in Konrad Miller's facsimile of 1888 (National Library of
Australia, public domain), as one strip to grab and throw. Pins mark the lost
first segment, Rome enthroned, Constantinople, Antioch, "Hic Alexander
responsum accepit" at the edge of the known world, and Taprobane. Under the
map, the one number that decides how a throw feels — the share of its speed
the map keeps each frame: 0.90 stops dead, 0.94 like an object, 0.98 slides
for ever — and the whole scroll small, with a window that follows the map on
a scroll timeline (no script) and takes you where you click.

**Stitching.** The eight sheets overlap by 400–900 px (at 1920). `register.py
stitch` finds each seam by sliding the end of one sheet over the next at a
quarter size, then matching patches across the overlap and fitting what
nearly all of them agree on (54–83 patches a seam, worst residual 2.4 px; the
sheets differ by up to 0.6 % in scale and 0.4° in turn). Each sheet is set in
the first one's frame by a composed transform and cut at the middle of its
overlap; the strip ends where the map's torn edge ends, found past the scan's
border. A sheet's map band is measured between the paper's blank margins —
two earlier definitions (dark rows; the longest run of sea rows) broke on
sheet 6's border and on the Mediterranean's gaps. Where a sheet's band falls
short, the strip's ground is the map's own sea, sampled from every sheet's
edges and hatched as the facsimile hatches it.

**The throw.** The map is a native horizontal scroller, so touch, trackpads
and keys move it as they always do; `showcase.js` adds the grab and the throw
for a mouse (a pause before release is a put-down, not a throw), frame-rate
independent (`decay ** (dt / 16.7)`), and none of it when the visitor prefers
less motion. Measured in Chrome: from the same flick, 0.90 glides 598 px in
0.8 s, 0.94 1,104 px in 1.5 s, 0.98 3,522 px in 4.4 s.

## The ninth showcase: Sticky Stacking Cards, twenty of twenty-two, 2026-09-23

**The idea.** The trumps of the Visconti-Sforza tarot (the Pierpont
Morgan–Bergamo deck, about 1451, public domain) dealt onto a candle-lit table
as you scroll: each card comes in turned and a little to the side, lands on the
pile five pixels below the last, and the gold leaf catches the light once as it
comes down. Beside the pile, each card's name and what is painted on it travel
with the card and dim once it lands. Of the deck's 78 cards 74 survive; the two
lost trumps, the Devil and the Tower, keep their places in the list, struck
through, while the deal pauses and nothing lands. The names and descriptions
are ours, from looking at the cards; the facts are Wikipedia's.

**How it is built.** No script. Every card is sticky at nearly the same place
(`top: calc(var(--bar) + 6svh + var(--i) * 5px)`); a card's box is one step of
the deal and its face overflows it, so each arrives over the last. The deal and
the glint ride each card's own view timeline, finished before it sticks (a stuck
card's timeline stops). Found on the way: a sticky element is held only within
its container's content box, so the hold after the last card is a spacer inside
the list, not padding. Chrome holds 120 fps through the deal (p99 10 ms).

## The tenth showcase: Text Mask, through the letters, 2026-09-23

**The idea.** Four of William Morris's patterns — Strawberry Thief (1883),
Honeysuckle (1876), Willow Bough (1887), Snakeshead (1877), from the Cleveland
Museum of Art and the Met, CC0 — each seen first through the letters of its own
name, set huge in Zodiak Black. The pattern holds still; the letters are
windows onto it. Scrolling grows the letters toward the thickest stroke near
the middle of the name until they are great windows, then the ground dissolves
and the whole pattern is there, with a plate carrying the museums' lines (May
Morris on the thrushes and on Honeysuckle, "the very symbol of a garden
tangle"). Willow Bough stands on deep green, the rest on paper.

**How it is built.** No script. The name is real text with
`background-clip: text`; its background is `fixed`, so the pattern stays put
while the letters grow and stays sharp (it is never magnified). Two registered
numbers drive the zoom: `--z` scales the font size, `--k` steers the growth
toward the chosen stroke, whose position (in em from the word's centre) and
each word's width were measured once in Chrome by redrawing the laid-out glyphs
on a canvas and finding the thickest ink nearest the centre. The ending needs
no mask: the whole-pattern layer is the very same fixed picture, fading in over
the ground, so the letters simply dissolve into it. Each scan is scaled a little
past cover so no mount or selvedge ever shows. The face (Zodiak 900, Fontshare)
loads on this page only. 120 fps through the zoom (p99 10 ms), though the font
size lays out each frame.

## The eleventh showcase: Threshold Flip, one façade, six lights, 2026-09-23

**The idea.** Six of Monet's Rouen Cathedral paintings (1892–94; the Getty,
Boston, the National Gallery of Art, the Pushkin twice, the Musée d'Orsay, a
private collection), each a room of the page. As a canvas reaches eye level,
the whole stage takes its colours at once — ground, ink and accent — so the
page turns from fog blue to deep morning blue, sunlit ivory, ochre noon,
charcoal and lilac, evening tan. Each room names its light in Monet's own
words (Brouillard, Effet du matin, Au soleil, Midi, Temps gris, Fin de
journée), set against the painting like a gallery label.

**The palettes are the paintings'.** `build/palette.py` quantises each
painting (median cut, 500 px) and chooses in OKLab: the most common colour as
the ground, moved out of the 0.36–0.76 lightness band where no type reads;
the most colourful colour covering 3 % or more as the accent, moved in
lightness to stand off the ground; the ground's own hue at the far end of
lightness for the ink. Written to `assets/palettes.json`; the build writes the
six `[data-light]` rules into the page's head from it, so the colours live in
one place. The module guards its import-time read so the tool can run first.

**How it is built.** Six lines of script: an IntersectionObserver with the
`-45%` band names the canvas at eye level on the stage; the stylesheet holds
the palettes and a .7 s transition. Museums checked on the Commons records
(Boston's and Orsay's through their Google Art Project metadata).

## The twelfth showcase: Curtain Overlap, Montmartre pasted over, 2026-09-23

**The idea.** Eight posters from the Paris of 1889–1896, in order: Chéret's
Bal du Moulin Rouge (the opening, 6 October 1889), Lautrec's La Goulue (his
first poster, 1891), Chéret's Saxoléine, Lautrec's Aristide Bruant (1892) and
Divan Japonais (1893, Jane Avril and Édouard Dujardin in the front row),
Chéret's Loïe Fuller, Mucha's Gismonda (up on 1 January 1895; Bernhardt
ordered four thousand and gave him a six-year contract) and Steinlen's
Tournée du Chat Noir (1896). Each sits on a screen-high panel in one of its
own inks; every panel is sticky at the same place, so each new one rides up
over the last, as a billposter pasted one poster over another. Scans from the
BnF, the Met, the Art Institute of Chicago, the NGV, the Museum of Decorative
Arts in Prague and the Rijksmuseum; all public domain or CC0.

**Colour.** The posters are mostly paper and black ink; their vivid inks
cover only 10–18 %, so one automatic rule gave five red panels. The grounds
and inks are still each poster's own (from palette.py's quantisation), but
chosen by eye so neighbours never share one and lightness alternates; that
choice is written in the module with the reason.

**How it is built.** No script. The overlap is two rules (sticky, same top).
Depth: the incoming panel carries a shadow above its top edge; the covered
sheet recedes (scale .93, up 3 %) and dims on the incoming panel's own view
timeline — a named `view-timeline` per panel, shared with its predecessor
through `timeline-scope` on the hoarding and a `--next` custom property. The
whole sheet recedes with its ground into the dark hoarding behind. Found on the
way: a grid row sized by an image of a tall poster overflowed the room
(`grid-template-rows: minmax(0,1fr)` fixed it); and `animation-timeline: none`
does not neutralise a 0 s fill-both animation — Chrome runs it to its end —
so the last sheet takes `animation: none`. Posters are sized explicitly from
their proportions (no lazy-image layout warning). 120 fps, p99 10 ms.

## The thirteenth showcase: Scroll Snap, twelve months, a page each, 2026-09-23

**The idea.** The calendar of the Très Riches Heures du Duc de Berry (the
Limbourg brothers, about 1412–16; Musée Condé, Chantilly, MS 65; public
domain) as a book that snaps: its own vertical scroller, a page a month, and
however far it is thrown it comes to rest on a whole month. Each page: the
miniature under its zodiac arch, and facing it the month in French, its Roman
numeral, the two signs on its arch (checked against the arches themselves —
October's shows the scales and the scorpion), and one line on the scene, with
castles named only where Wikipedia names them. The stage wears the
manuscript's own ultramarine, sampled from the arches (OKLCh h ≈ 269°) and
deepened; vellum for the words, gold for the marks.

**How it is built.** Two properties make the book (`scroll-snap-type: y
mandatory` on the scroller, `scroll-snap-align: start` on each page). A thumb
index of the months runs down the edge; its gold mark rides the book's own
scroll timeline (`scroll-timeline: --book`, shared through `timeline-scope`),
continuously, so the difference between the scroll and the resting page can
be seen. Each month's words rise on the page's timeline, not the words' own —
a page the book's height is fully entered exactly when it snaps, so the rise
always finishes at rest (keyed to the words themselves, they stayed half-faded
on phones, where they sit below the middle). No script. `.index` was taken
(the Lexicon's entrance), so the list is `.months`.

## The fourteenth showcase: Scroll-Triggered Count, a generation counted, 2026-09-23

**The idea.** Six of the charts W. E. B. Du Bois and his students at Atlanta
University drew for the Exhibit of American Negroes at the Paris Exposition of
1900 (The Georgia Negro: A Social Study; Library of Congress, public domain):
slaves and free, city and rural, children in school, acres, household
furniture, all taxable property. Beside each plate, its figures are set the
way the plate letters them: the year, a band in the plate's own colour, the
figure, and the plate's last figure large. Every number was read off
full-resolution crops of the plates (the city plate's four parts add up to
the population plate's 858,815, a check). The mark under 1860 on the schools
plate is a 7, not Du Bois's question mark: his "?" has a curl and a dot. Each
section wears the plate's own inks, sampled from the inked pixels only:
black, paper, the schools' olive, crimson, gold, and the property rings'
ultramarine with gold figures. The numerals are Anybody at 150 % width,
weight 200: its tabular figures are as wide and thin as the plates' lettering,
and its heavy weight does the plates' titles.

**How it is built.** No script. Each figure is text; each digit is a span and
also a wheel. `timeline-trigger: --count view() contain 0% contain 100%` with
`animation-trigger: --count play-once` starts a registered `--t` from 0 to 1
once, when the whole figure is on screen. Each wheel's place comes from
`pow(10, sibling-count() - sibling-index())`; the count is
`to · (1 − 10^(−k·t)) / (1 − 10^(−k))`, closing on its figure a power of ten
at a time, so the wheels come to rest one by one from the left, each at a
readable pace; each wheel turns to `mod(max(0, (n − mod(to, p)) / p), 10)`,
which lands exactly on its own digit. The strip is generated content with
empty alt text (`content: '0\A 1…' / ''`), so it is never read aloud; the
real digit is transparent underneath. `text-box: trim-both cap alphabetic`
makes the window exactly the figure's height; a little padding over it,
masked, lets digits roll in and out as on a drum, and a large wheel turning
fast blurs by `log()` of its speed. Rows count a beat apart
(`--i: sibling-index()`, registered). Reduced motion: no animation, `--t: 1`.

**The boards.** The scans show the boards in clear sleeves on a scanner bed,
white at every torn corner; on a coloured ground that read as a frame.
`build/cutout.py <kind>` floods the backing from the picture's edge (light and
nearly colourless; the sleeve's edge line is RGB spread ≤ 17, the board's
paper ≥ 25), traces the board's outline, pulls it in a pixel and simplifies it
(Douglas–Peucker) into a clip-path polygon in `assets/cutouts.json`. The
shadow is a `drop-shadow` on the figure, so it follows the torn edge.

**Checked.** At 1324×725 and on a phone at 390×844, no overflow, and every
large figure fits its column (`100cqi / --em`, the figure's width in em
computed at build). A smooth sweep through all six: 120 fps, p99 10.2 ms; all
34 figures fire. A trap on the way: a test sweep that calls `scrollTo(0, y)`
every frame on this site (`scroll-behavior: smooth`) keeps restarting a smooth
scroll, and triggers stop firing mid-sweep. With `behavior: 'instant'`, and
with real Page Down scrolling, every trigger fires.

## The fifteenth showcase: Split Text Reveal, two contrary states, 2026-09-23

**The idea.** Six of William Blake's Songs of Innocence and of Experience, from
copy Z (printed and painted in 1826, the year before he died; Library of
Congress, public domain): Introduction, The Lamb and Infant Joy from
Innocence; The Tyger, The Sick Rose and London from Experience, a hundred
lines in the book's own order. Each poem is set beside its plate. Innocence
stands on paper with sepia verse and Blake's orange-brown for titles;
Experience stands on night with parchment verse and gold. The page turns dark
at The Tyger, after the book's own subtitle, "Shewing the Two Contrary States
of the Human Soul". The verse is set in IM Fell English, whose inky,
hand-cut irregularity sits well beside etched letters. The text is Blake's,
with his spelling (chear, vanish'd, sieze, charter'd, mind-forg'd, blackning)
and his ampersands, read against the plates at full resolution. Where his ?
and ! are indistinguishable, the standard reading stands.

**How it is built.** No script. Every line is a window (`overflow: clip`,
with a little clip margin for the ascenders), its words translated 105 %
below the sill and tilted 2.5° about their left foot. A trigger on each
stanza (`timeline-trigger: --verse view() entry 70% exit 30%`, so a stanza
taller than the screen still fires) starts every line in it once, and
`animation-delay` from `sibling-index()` makes each a beat (85 ms) behind the
one before. Chrome resolves `animation-trigger` names from ancestors, which
was checked before relying on it. Triggering per line was tried first: the
beat then reset at every stanza and meant nothing while scrolling. The plate
is sticky beside its poem while the verse passes. On phones it stacks above.

**Checked.** At 1324×725 and at 390×844: all 106 windows (100 lines, 6
titles) rise, no line wraps on the phone, no overflow; a sweep through the
page runs at 120 fps (p99 10.2 ms); the console is clean. The card is The
Tyger on night with its second stanza caught rising.

## The sixteenth showcase: Clip-path Reveal, red, then green, then blue, 2026-09-23

**The idea.** Sergei Prokudin-Gorsky photographed the Russian Empire in
colour with a camera that made three black-and-white exposures through red,
green and blue filters. The Library of Congress's colour renderings were put
together from those three records, so each channel of the rendering is one of
them. Five renderings (Alim Khan, Emir of Bukhara, 1911; peasant girls on the
Sheksna near Kirillov, 1909; the Gur-e Amir, Samarkand; harvesting tea,
Chakva; the Nilov Monastery, Lake Seliger, 1910; LOC, public domain) are
each laid down record by record. An edge in the filter's colour carries the
red record across, then the green, then the blue, and the colour comes right
only where all three have passed. A first choice, Tolstoy at Yasnaya
Polyana, was dropped: that file is a scan of a printed reproduction (its
halftone dots show), so its channels are not his records. The glass-plate
scans themselves are not on Commons under any findable name, and the house
rule is Commons URLs only; the channels of the renderings stand in for them.

**How it is built.** No script. Each picture's article is 230svh, with a
sticky frame and a named view timeline (inset by the bar). Three layers of
the same file make it: each `.rec` has its filter's pure colour as
background, and the image multiplies onto it, so only that record survives.
The layers screen onto each other over black, which adds light exactly
because the channels are disjoint. The same URL three times is one request.
Each layer's `clip-path: inset(0 calc(100% - var(--p) * 100%) 0 0)` runs on
the timeline, in the contain ranges 4–30 %, 34–60 % and 64–90 %. Its
`::after` is the travelling edge, a 2px line with a glow in the filter's
colour, visible only mid-sweep. A legend (red, green, blue) lights on the
same ranges. Only the blue layer carries the alt text; the other two are
empty-alt duplicates.

**Checked.** At 1324×725 and at 390×844: a sweep runs at 120 fps (p99
10.2 ms) with three blended layers per picture; every picture ends in full
colour; no overflow; the console is clean. In the tea harvest, a girl who
moved between exposures keeps a colour fringe, and the note points to it.
The card is the Emir with blue two-thirds across: full colour behind the
edge, red and green ahead of it.

## The seventeenth showcase: Horizontal Scroll Section, the end of the tapestry, 2026-09-23

**The idea.** The last scenes of the Bayeux Tapestry (55–58, public domain;
the Université de Caen Normandie, CNRS and ENSICAEN digitisation of the 2017
photographic campaign), from William lifting his helmet to show he is alive,
through Harold's death, to the ragged end of the cloth. You scroll down; the
cloth travels sideways, the way it is read. The Latin tituli sit under the
words stitched above them, each with its English, and the last line is set
under the last stitch: the rest has been missing from time immemorial. "Et
fuga verterunt Angli" is noted as probably added shortly before 1814, as
Wikipedia reports. The date is given as the source gives it: produced in
England in the years after the Conquest.

**How it is built.** No script. The run is exactly as tall as the strip is
wider than the screen (`--travel`, computed from the strip's own size); the
frame is sticky, and the track pans on the run's view timeline to
`translate: calc(100cqw - 100%)`, so the last stitch lands a gutter from the
frame's edge whatever the screen. A hairline beneath fills as you go. The
strip is four overlapping photographs laid end to end by `register.py
stitch`, now general enough for a textile: a showcase may give BAND (its
band as fractions of the height) where a map would have blank margins, and
sheets served at one width but of different scale (the four scans are
15400–22000 px wide, all 5550 tall) are brought to one height before
matching, the scale folded back into the fit. All three seams agreed on
every patch (101, 72, 75), worst residual 1.9 px; the joins are invisible
("…CVM HAROLDO" flows into "HIC" across two scans).

**Weight.** The scans are PNG only, and embroidered linen compresses badly:
3840px copies are 6–9 MB each (29 MB for the four). No public-domain JPEG
of these scenes exists on Commons (only details, and CC BY-SA photographs).
The srcset is therefore capped at 1920 (7.4 MB, the Montmartre posters' order
of weight), which reads well on a retina screen at this height. All four load
eagerly: a lazy image inside the clipped, travelling track is not
"intersecting" until it is on screen, and would arrive visibly late.
`register.py`'s fetch now retries more patiently, because large copies are
often cut short in transit. Resuming with Range was tried: upload.wikimedia
answers 200 with the whole file, not 206.

**Checked.** At 1324×725 and at 390×844 (where the cloth is half the screen):
no overflow; a sweep runs at 120 fps (p99 10.2 ms); the console is clean.
With reduced motion the run collapses to one screen and the cloth becomes an
ordinary sideways scroller. The card is Harold's death with its titulus.

## The eighteenth showcase: Variable Font Animation, twelve sizes and one file, 2026-09-23

**The idea.** William Caslon's specimen sheet of 1734 (public domain) shows
every size of his type as a separate font of metal, known by a name, from
French Cannon (so spelt) down to Pearl, each set in the opening of Cicero's
first speech against Catiline. It faces one variable font, Source Serif 4
(Adobe, after the types of Pierre Simon Fournier, Caslon's French
contemporary), with optical size and weight axes. A loupe walks down the
sheet at the same scale as the live type and holds on each of Caslon's sizes
in turn, framing the block. Beside it, "Quousque tandem abutere, Catilina,
patientia nostra?" glides through every size in between as you scroll, its
optical size following its size. Its weight is a dial, marked with the six
weights a family once shipped as six files, swept once, 400 → 900 → 200 →
the dial, as the frame pins. Bodoni's Manuale tipografico was the first
choice, but Commons renders its PDF pages only at 500px, whatever width is
asked, which is too small for type.

**Measured, not assumed.** Each size's body on the scan was measured as the
period of its rows (autocorrelation of the row-darkness profile, refined
with a parabola). Taking Pica as 12 points gives French Cannon 47.8, Two
Lines English 27.7, Brevier 7.9 and Pearl 4.8, so the sheet agrees with the
traditional names. The live line glides through the sheet's own measured
sizes, so at each step it is exactly the size of the metal beside it. No
point values are claimed on the page: in 1734 sizes had names, and "their
exact length would vary … from foundry to foundry".

**How it is built.** One sticky frame on the run's named view timeline:
`--t` 0→1, and `--lb` (the log of the size) through keyframes written from
the measured sheet into the page's head, log-linear between steps.
`font-size: calc(exp(var(--lb)) * var(--m) * 1px)`, where `--m` is CSS px per
px of the scan, shared with the loupe. The loupe's walk is keyframes with a
plateau at each block, clamped so the sheet never shows its edge. Block
frames and the names light by distance: `opacity: clamp(…, 1 - abs(var(--t)
* 11 - var(--i)) * k, 1)`. The weight readout is a CSS counter of the
registered `--w` (`counter-reset: w calc(var(--w))` rounds), so it counts
through the sweep. The `<output>` keeps the dial's value as text, set by a
six-line showcase.js. A trap: a `timeline-trigger` with an anonymous
`view()` has no inset, so a run taller than the screen only "covers" it once
its top passes under the bar. The trigger uses the run's named timeline
(`--arrive --size contain 0% contain 100%`) instead, which carries the inset.

**Checked.** At 1324×725 and at 390×844: the sweep waits above the run and
fires as the frame pins; the dial drives weight and readout; no overflow; a
sweep runs at 120 fps (p99 10.3 ms, one 42 ms frame on the sheet's first
decode); the console is clean. The card is French Cannon, metal against the
file at weight 780.

## The nineteenth showcase: Scrollspy, eighty days leg by leg, 2026-09-23

**The idea.** Around the World in Eighty Days (1872). The index is the plan
the Morning Chronicle works out in chapter III (London to Suez 7 days … New
York to London 9; total 80), set as a timetable with dotted leaders and a
double-ruled total, with the route map of the illustrated French edition
above it. It stays beside the story. The story is the eight legs as they
went, each with an engraving by Alphonse de Neuville or Léon Benett (the
wager, the Malabar Hill pagoda, the elephant Kiouni, the Hong Kong tavern,
the Tankadere in the typhoon, the Long Noses' pyramid, the sail-sledge, the
return to the Reform Club) and a line of Towle's translation, verbatim, cut
only with an ellipsis. The coda is the day gained by travelling east.
Whichever leg has reached the top is marked in the timetable, the legs
behind are ticked off, and the ones ahead wait. The type is Old Standard TT,
modelled on the book faces of the period.

**Material choices.** The 1873 English edition's 55 illustrations are PNG
(3.6 MB at 960px), so the JPGs of the French plates were used (0.66 MB), a
high-resolution set plus four medium ones where a leg had no large plate.
Their Commons captions come from another translation, so the scenes were
identified by eye and each quote was found in the Towle text itself. An
Encyclopédie plate with its "explication" was considered and set aside
(plates, text and figure positions all to assemble).

**How it is built.** No script. The timetable's `<ol>` has
`scroll-target-group: auto`, so its links (plain `#leg-N` anchors) become
scroll markers. `:target-current` marks the leg reached, `:target-before`
ticks the legs behind (✓), and `:target-after` dims the ones ahead. The
links still work as links, and `scroll-margin-top` lands a jump just under
the bar. On a phone the plan becomes a strip under the bar showing only the
current row (every row in one grid cell, `li:has(a:not(:target-current))`
hidden).

**Checked.** Above the stage leg I is current; at the end all seven are
ticked and VIII is current; a click lands at the bar and marks its leg; no
overflow at 1324 or 390. The card is leg V with four legs ticked.

## The twentieth showcase: Gamut Arc, round the circle or straight across, 2026-09-23

**The idea.** Michel Eugène Chevreul's first chromatic circle (1864, engraved
by René-Henri Digeon; Science History Institute, public domain): seventy-two
hues "franches", twelve named, five numbered steps between each. It sits on
the seam between two screen-high fields that go from one of his colours to
its opposite. Round the outside, the left field passes through every sector
of his circle between the two. Straight across, the right field takes the
line CSS takes unless asked otherwise. A white dot rides the rim of the plate
along the round route and a ring rides the dashed chord. The left field names
the sector in his notation ("Jaune-vert 3"); the right gives the mixture as a
recipe ("58% jaune / 42% bleu-violet"). A meter under each shows the chroma
left.

**Measured, not assumed.** `palette.py ring` samples the plate's 72 sectors
from the geometry declared in the module (RING). The circle's centre was
first fitted to the coloured band with a chroma mask, and came out 29px wrong:
Chevreul's surviving blues and violets are so dull (C ≈ 0.04) that the mask
missed them. Refitted to the disc's edge against the paper (residual 4.7px),
with the separators fitted to the white lines, every sector lands in its
cell. His hues run monotonically round Oklab's full circle. The pairs are the
ones that are opposites in Oklab as well: Jaune and Bleu-violet 182.5° apart,
Vert and Violet 177.6°, Rouge-orangé and Bleu 178.4°. His own opposites (red
across from green) are perceptual, not Oklab's. In every pair the straight
route falls to grey (C 0.003–0.005). The round route never drops below 0.082,
at Bleu, where sRGB pinches near cyan, and peaks at 0.237 in the violets. Each
round stop keeps the sector's measured hue and lightness and takes all the
chroma sRGB holds there (bisection on the Oklab→sRGB transform).

**How it is built.** Almost no script, and none for the colour. One sticky
frame on the run's view timeline drives `--t`; the round field's colour and
chroma are keyframes written from the measured sectors into the page's head,
one set per pair; the straight field is `color-mix(in oklab, …)`, its chroma
`sqrt()` of the mixed a and b. The pair is a radio, and `:has()` hands its
numbers to the stage. The dot rides by `cos()`/`sin()` of an angle on `--t`,
and the arc is a conic gradient masked to a ring, travelled part solid. Ink
flips with each field's lightness by relative colour syntax. Counters make
the readouts. Found on the way: `.kicker` is taken by the page header
(renamed `.road`), and grid auto-placement swapped the meter's number and bar
(explicit order).

**Checked.** At 1324×725 and 390×844 (stacked, plate on the seam): no
overflow, 120 fps (p99 9.4 ms) with either pair, console clean. The card is
the violet moment: Violet at chroma .20 against a taupe mud at .03.

## The twenty-first showcase: Path Drawing, the march drawn again, 2026-09-23

**The idea.** Charles Joseph Minard's map of the French army's losses in
Russia, 1812–13 (Paris, 20 November 1869; BnF via Gallica, public domain;
the sheet also carries its companion, Hannibal's march, which is cropped
away). The bands draw themselves as you scroll, and nothing is redrawn: the
bands on screen are Minard's own lithograph. Rose goes in from the Niemen to
Moscow, splitting off the northern corps (22,000) and the column to Polotzk.
Black comes out: down from Moscow, west past Smolensk, joined at Bobr by the
30,000 from Polotzk, across the Berezina, and back to Kowno, where the
6,000 rejoin. The thermometer under it draws itself in step. A ledger below
reads Minard's figures as the pen passes them, each with the stretch it is
written on ("24,000 · Smolensk → Orscha", positions read against the town
names on the scan), and his readings with their dates.

**Minard's calendar.** The black band keeps the dates in his temperature
table: each dated reading is tied to a place on the retreat by one of his
thin vertical lines, so the band reaches that line on that day (0° on 18
October … −30° on 6 December, −26° on 7 December), and the thermometer
reaches the same reading at the same moment. The −11° is undated on the map
and the page shows no date for it; placed between its neighbours by
position, it falls on 24 November, the date usually given. The rose band is
timed by distance (its dates are not on the map).

**How it is built.** Over each band lies a veil, the paper's colour with
`mix-blend-mode: lighten` at .9, so it lifts only ink: bands and figures
become a ghost, and the paper is untouched. The veil is an SVG mask holding
the band's own outline in white (traced from the scan) and its pens in
black: strokes with `pathLength="1"` whose dashoffset follows the route's
progress. Each route's progress is a registered number on the run's view
timeline, its keyframes written into the page's head from the tracings and
the calendar. The pens are split where the band narrows by a third, each as
wide as its stretch, and they run past the line's ends by half the widest
nearby run, along the last 60px of the line's direction, so their square
ends clear a band cut obliquely. On a phone the map is 60svh tall and
follows the pens (`--fx`, a keyframed number).

**The tools.** `build/trace.py` is new and general: it follows a line of
one ink from a start, one step at a time, taking the run of ink nearest the
last centre (a band's runs a few px apart merged, so figures written across
it don't break it; a running median against letters), simplifies it, and
keeps each vertex's width. It also traces a band's whole outline (the
largest region of an ink, holes closed, thin strokes opened away). A line
that can't be followed (the thermometer, crossed by the table's rulings) is
given by its vertices. The thinnest miles of the retreat are lost to the
outline's opening; there the veil is a stroke along the traced line instead.

**Checked.** At the end of the run the map is exactly the lithograph: a
screenshot with the veils diffed against one without them, 0 pixels differ.
The first diff found 89: the rose band's slanted end at Kowno, and the branch
at Polotzk, fixed by extending the pens along each line's local direction.
It runs at the display's refresh rate (p50 6.9 ms, p99 7.7 ms at 144 Hz),
with no overflow at 1324 or 390, and the console is clean. On the phone the
frame's implicit grid column grew to the 1083px map and carried the ledger
off-screen; the fix was an explicit `minmax(0,1fr)`.

## The twenty-second showcase: Ordered Dithering, tones taken away, 2026-09-23

**The idea.** Three photographs from three centuries, taken down to a
handful of tones, the missing ones made up out of the regular grain of the
8×8 Bayer matrix: Nadar's Sarah Bernhardt (1864), a plate of the Moon from
Loewy and Puiseux's photographic atlas for the Paris Observatory (Blancanus,
Tycho, Schiller, 1899; the National Gallery of Art, CC0), and Apollo 8's
Earthrise (1968). On arrival the tones fall by themselves from the
photograph to two, once; then a dial takes them from 16 to 2, with three
grains and the matrix itself shown as 64 greys with their thresholds as
text.

**Made right, not just made.** The dither is real, computed live on a
canvas over the photograph: Wikimedia serves `access-control-allow-origin:
*`, so a canvas can read the image. Each pixel takes the tone just below or
just above its own by its cell's threshold, and the choice is made in linear
light, so the grain averages to the photograph's brightness (in sRGB a
two-tone dither makes every mid-tone too light). The tones are spaced
evenly in sRGB, and a 256-entry table per setting (the tone below, the
fraction towards the one above) keeps the inner loop to a lookup and a
compare. The monochrome prints dither between their own ink and paper, the
0.5th and 99th percentiles measured on each (Bernhardt neutral #0B0B0B /
#E5E5E5; the Moon plate warm #322F26 / #F8F4EB). Earthrise dithers per
channel, so at two tones it has eight colours, and it is cropped to the
Earth and the horizon. A redraw of 1.3–1.75 Mpx costs about 5–14 ms.

**Crops, and a trap.** A picture may declare the part shown. The `<img>`
crops itself with `object-view-box: inset(…)` (its width, height and --ar
are the crop's, its `sizes` scaled up by the crop's width). The script must
draw the same part, and `drawImage`'s source rectangle is in the file's own
pixels, while `naturalWidth` is density-corrected for srcset images and
ignores `object-view-box`: a source rectangle computed from `naturalWidth`
drew the black sky. The fix draws the whole picture into a larger
destination rectangle, offset so the part fills the canvas, which needs no
source units at all.

**Checked.** At 1324×725 and at 390×844, no overflow, and the console is
clean. The photograph stays in the page as the image, with its alt; the
canvas is aria-hidden, and the tone count is an `<output>`. The card is
Bernhardt at two tones.

## The twenty-third showcase: Progressive Blur, captions that stand on the picture, 2026-09-23

**The idea.** Six photochroms of the 1890s (Photoglob Zürich and the Detroit
Publishing Company; the Library of Congress Photochrom Print Collection,
public domain): Amalfi from the Capuchins, the Admiralty at Algiers, the Mer
de Glace, the Stockholm Exposition of 1897, a Sami family in Nordland, and
the Silver Apron in Yosemite. Each is shown whole and as wide as the screen,
with its caption on the picture. Photochroms were printed from one
black-and-white negative and ten to fifteen lithographic stones, coloured
from the photographer's notes. Every print carries a switch (labels for one
radio group) comparing the softening with what it replaces: a black bar, or
nothing.

**Where the blur goes is the design.** The first cut used one layout for
all six (full-bleed, softening the bottom 52%, captions bottom-left). It
blurred the Amalfi woman's face, the Sami children and the Mulberry Street
crowd: a progressive blur over a subject is worse than a bar. So each print
now declares its quiet edge, how far the softening reaches (30–42%, stopping
short of the subject), and the caption's side and ink. The ink comes from
the measured lightness of that corner: light over the dark granite (L .45),
dark over the Sami sky (L .77), the ice and the sunlit quay. The Sami family
is softened at the top, over the sky: the children fill the bottom of the
print. Mulberry Street, busy at both edges, was replaced by the Silver
Apron. Scans with a mount or the Library's colour target are cropped to the
picture with `object-view-box`. On a phone each print is cropped tall,
held on its subject by a per-print x.

**How it is built.** No script. Six layers of `backdrop-filter: blur()`
(1, 2, 4, 8, 16, 32px), each masked to its own band of the veil and
overlapping the next, grow the blur itself towards the edge. A single
blurred layer under a gradient mask only fades a uniform blur, which reads
as frosted glass. The mask direction is a custom property (`--to: to
bottom` or `to top`), so one rule serves both edges. A whisper of tint
under the ink finishes it. The switch's radios are visually hidden with
`aria-label`s (six sets of labels would otherwise concatenate into their
names); the label sets are aria-hidden, styled from the radios by `:has()`,
and show their focus ring through `:has(:focus-visible)`.

**Checked.** At 1324×725 and at 390×844: no overflow, all six loaded, the
console clean, and a sweep at the display's refresh rate (p50 6.9 ms, p99
7.7 ms at 144 Hz) with 36 backdrop layers on the page. Found on the way:
the title's descenders ran into the line below (padding-bottom .16em), and
the phone switch wrapped because `right: 50%` halved its available width
(centred with `left` instead). The card is the Silver Apron.

## The twenty-fourth showcase: Blur-up (LQIP), colour first, then the line, 2026-09-23

**The idea.** Sixteen of Hiroshige's *One Hundred Famous Views of Edo*
(1856–58), four to a season, on a wall the colour of their paper. The series
is arranged by season (spring 1–42, summer 43–72, autumn 73–98, winter
99–118), so the wall is a year in Edo. Every print is in the page from the
start as a stand-in: a WebP sixteen pixels across, 124–246 bytes, 3.1 KB for
all sixteen, written into the HTML. The prints are flat fields of colour,
graded at their edges (bokashi), bound by line. At sixteen pixels the fields
survive and the line does not, so the rain at Atake, the fireworks at
Ryōgoku, the eagle at Jūmantsubo and the foxes at Ōji arrive with the print,
and a wall of stand-ins already reads as the seasons.

**Material.** Chosen print by print for the freshest impression, from a
contact sheet of 45 candidate scans (the Sudden Shower in five, the foxfires
in three): eleven from the Met (CC0), three from the Library of Congress
(Nihonbashi, the irises, the Moon Pine), the Kameido plums from the Cantor
Arts Center at Stanford (a Google Art Project file: the credit is Stanford's,
not Brooklyn's, which the file name suggests), the carp streamer from the
MFA Boston. Every scan is cropped to its printed image. The edge is the
strongest step from paper into keyline near each side; a darkness threshold
failed on the dark scan backgrounds and on the pale edges of snow and cloth.
Each edge was checked corner by corner, zoomed. The series' frame has
notched corners. Measured on all 64 corners, their radius is 1.7% of the
print's width (quartiles 1.4–2.1%), so every slot is cut with `corner-shape:
scoop` at that radius and even a stand-in has the series' shape. The wall
has one slot shape (the median proportion, 0.6586) so the rows line up; each
print covers it and loses at most a hundredth at an edge.

**How it is built.** `build/lqip.py <showcase>` (new, for any picture):
the smallest copy Commons serves, cropped to the part shown, averaged down
to 16 px across, padded with two pixels of its own edge, WebP at quality 50,
into `assets/lqip.json`. The padding matters: blurred, a picture fades to
transparency at its border; padded with its own edge, the blur finds its
colour there. Ten pixels across lost the round window at Massaki and the
lantern at Asakusa; twenty-four added bytes and little the eye needs. The
stand-in is the slot's `::before`, stretched past the slot by its padding
and blurred 3.5cqi; at 2.2cqi the 16-pixel grid shows through as blocks. The
print is held back by `showcase.js` until its file has arrived and been
decoded, then comes into focus over its stand-in (opacity and `blur(2cqi)`
to none, 1.2 s). Without the script nothing is held back: each print paints
over its stand-in. What each print cost comes from Resource Timing (Wikimedia
sends Timing-Allow-Origin), per print and summed in the deck. Replay brings
them in again in the order they arrived on this visit, evenly spaced: on
their real spacing, twelve bunched into the first moment because the lazy
winter row came seconds later. A stand-ins switch holds the wall as the page
first has it.

**Checked.** At 1324×725 and 390×844: no overflow, console and issues
clean, all sixteen arrived; a scroll sweep p50 6.9 ms, p99 8.5 ms at 144 Hz;
during the replay p99 14 ms, with one 26 ms frame as all sixteen fall back
together. Found on the way: the deck's top margin collapsed through the
stage (now the stage's padding); on a phone the sticky deck was 126 px, a
sixth of the screen, all the way down (static there); the cost line
orphaned its "KB" (now two unbreakable halves). The card is the winter row,
prints and stand-ins alternating under the deck's count of bytes.

## The twenty-fifth showcase: Marquee, fifty-five greetings still travelling, 2026-09-23

**The idea.** The fifty-five greetings of the Voyager Golden Record (1977),
from Sumerian to English, in the order they were recorded, running in five
bands out from under the record into the dark. Each greeting is set in its
own script, with its time on the record and its English translation beneath.
The marquee is the one effect that ignores scroll; here it has something to
carry: greetings still travelling, on both Voyagers, out of the solar
system. The texts, written forms and translations are those listed in
Wikipedia's contents of the record (the table gives the written form for all
55, cuneiform and Imperial Aramaic included); Wikipedia stores the Arabic
greeting with its full stop at the logical start, for display inside
left-to-right text, and here it is set right-to-left with the stop at its
end.

**The record.** NASA's photograph of the disc (GPN-2000-001976), on a black
matched to the stage (#040205). The photograph is clipped to the disc's own
outline about the spindle hole, so only the disc stands in front of the
bands, not the photograph's black square, and the bands end at the hole, so
every greeting comes out from behind the record's round edge. Only the label
turns, at the 16⅔ rpm the record was cut for: a second copy of the same file,
clipped at 0.179 of the width (inside the dark run-out band, so the seam
between still and turning falls on black) and rotated about the hole (found
as the centroid of the dark pixels at the centre). The grooves look the same
at every angle, and the photograph's glints stay where the light was.

**How it is built.** Each band's greetings are set twice in one moving
flex row, which travels `-50%`; the copy is `aria-hidden` and `inert`. The
duration is one set's measured width over the band's speed in pixels a
second (a ResizeObserver in showcase.js, so it is measured again when the
fonts arrive): bands of 6,000 to 12,600 px keep their paces. Five bands differ
in size, speed (23–54 px/s) and light, so they read as depths. Hover stops a
band and Hold stops them all (WCAG 2.2.2: anything moving for more than five
seconds must be stoppable; hover alone leaves out touch and keyboard); with
reduced motion the bands stand still and scroll by hand. Twenty-one faces,
Noto Serif for most scripts, Naskh for Arabic and Persian, Nastaliq for Urdu
(at 0.82em: it sits larger), Noto Sans for cuneiform and Imperial Aramaic,
come in one Google Fonts request with `text=`, cut down to the 488 characters
the greetings use (a 4.2 KB URL).

**Checked.** At 1324×725 and 390×844: no overflow, all 21 faces loaded,
console clean; Hold stops all five (0 px of movement), and five bands plus
the turning label run at p50 6.9 ms, p99 7.8 ms at 144 Hz, all on the
compositor. Found on the way: the photograph's black square hid the bands
along a straight line (clipped to the disc), a sliver of text showed right
of the disc at the bottom band (the bands now end at the hole), and on a
phone, where the record sits above, the bands run the full width below it
instead. The card is the stage itself.

## The twenty-sixth showcase: Token Interpolation, one angle, every colour, 2026-09-23

**The idea.** Philipp Otto Runge's *Farben-Kugel* (Hamburg, 1810) beside an
interface whose every colour is one number. Runge's sphere has the geometry
of OKLCH: lightness is the axis between his white and black poles, hue the
angle round the equator, chroma the distance out from the grey core. Each
token (ground, surface, rule, soft ink, ink, accent, complement) is a point
on it with its own lightness and chroma; they share one angle, and scrolling
a runway four screens tall turns it through the whole circle. A table of the
tokens gives each value live, only its hue moving.

**Chosen to hold.** The lightnesses and chromas sit inside sRGB at every
hue (computed: the accent's 0.118 is the most an L 0.72 colour can have at
the cyan, where sRGB is narrowest; the ground's 0.016 the most at L 0.965
near blue), so no colour is clipped out of step on the way round, and the
contrasts hold: ink on ground 13.45–13.78:1, soft ink on ground
5.96–6.39:1, ink on accent 5.84–6.30:1, all computed over 360 hues. The
turn starts at 18.17°, the hue of Runge's own red.

**Runge's plate, measured.** His section through the equator fitted as a
circle against the paper (120 edge points, residual 0.9 px), and its twelve
sectors measured in OKLCH with `palette.py ring` (the broad second ring,
where his inks are purest). A needle on that section points, at every step,
at the ink he printed at the palette's hue: its keyframes are generated from
the measurements and run on the same view timeline as the turn. The
measurements show his circle has no cyan: from his green at 142° to his
blue at 217° is one sector step, a fifth of the circle, and the needle slows
across it.

**How it is built.** `@property --turn` (an angle) animated by the runway's
view timeline (inset by the top bar); every token is `oklch(L C
calc(18.17deg + var(--turn)))`, declared on the pinned frame, not the root.
The hue readouts are counters fed by a registered integer turning with it
(`counter-reset: d mod(calc(18 + var(--deg)), 360)`). Four chart series a
quarter-turn apart use `sibling-index()`. Found on the way: the shared
Lexicon stylesheet's unscoped `.btn` (from the old demos) pulled the card's
links out to the frame's corner (renamed `.act`), and the display face's
tabular zero is slashed (proportional figures, a fixed-width readout).

**Checked.** At 1324×725 and 390×844, through the whole turn: no overflow,
console clean, p50 6.9 ms, worst 7.9 ms at 144 Hz with the frame recoloured
every frame. The card is the frame at 179°, the needle upright in Runge's
missing cyan.

## The twenty-seventh showcase: Scoped Rotation, where the angle lives, 2026-09-23

**The idea.** Georges Seurat's *A Sunday on La Grande Jatte — 1884*
(1884–86, Art Institute of Chicago, CC0) redrawn as 3,456 dots, and its
palette as 24 swatches. One turning angle can be declared nowhere, on the
swatches, on the root of the page, or on the painting (a radio group), and
a counter gives the frames a second the page keeps and how many elements
the declaration reaches, with a sparkline of the last two seconds. On the
root the page slows to about a fifth of its pace for a change that shows
only on the same 24 swatches; on the painting, every dot takes the angle
and the Grande Jatte turns through the hues.

**What the counter found.** First version: the angle chosen by `:has()`
rules and each dot's colour a relative colour (`oklch(from var(--c) …)`).
Timing the style work alone (forced inside `requestAnimationFrame`, where
the animations have ticked and style has not), the painting cost 90 ms a
frame at 7,776 dots, the root 15. A prototype separated the causes: the
`:has()` in the dots' selectors made their style work five times dearer,
every element re-matching its selectors each frame, so the choice is now
mirrored into a `data-scope` attribute by the script. And in relative
colour syntax the `h` channel is a number, so `calc(h + <angle>)` is
invalid (the swatches rendered transparent): the turn is a registered
`<number>` of degrees. Then a trace showed the style work was not the whole
cost: every element given a fresh computed style each frame leaves garbage,
and collecting it took more time than the recalculation (paint was almost
free). So the counter measures what a visitor feels, the time from frame to
frame, and nothing is forced. At 7,776 dots the painting ran at 9 frames a
second, at 5,400 at 13, at 3,456 at 20, where a turn of 8 s moves each dot's
hue under a degree a frame and reads as smooth; so 72 × 48.

**How it is built.** The dots are sampled from the painting's image in the
browser (Wikimedia sends CORS headers), each given its OKLCH lightness,
chroma and hue once, as custom properties; the swatches are the painting's
24 most representative colours from the new `palette.py swatches` mode
(octree, not median cut: median cut greys a painting of mixed dots, mean
chroma 0.035 against 0.049). Out of view the angle is declared nowhere, so
leaving the stage in root mode gives the page back its pace (29 frames a
second in view, 141 away, the choice restored on return).

**Checked.** At 1324×725 and 390×844: no overflow, console clean; the
swatches at the display's 145 frames a second, the root at 27–29, the
painting at 20–23. Also fixed across the Lexicon: Melodrama's zero is
slashed in every setting, so the meters here, in Token Interpolation and in
Ordered Dithering set their numerals in Switzer. The card is the painting
turned, the counter at 21 and the sparkline's jump.

## Wrapping up, 2026-09-23

**A regression sweep** of all 27 showcases, each loaded in an iframe at 1324
and at 390 wide and scrolled through: no horizontal overflow, no broken
images, no failed resources, no script errors, every page its own card.

**Melodrama's zero is slashed in every setting** (default, lining,
`zero` off, old-style, every stylistic set), so wherever the display face
sets figures that are the point (a measured count, a percentage, a
distance, a scale), the figures are set in Switzer: Path Drawing's
soldiers and temperatures, Scroll Markers' distances, Difference
Inversion's scale, Gamut Arc's mixture (its figures in Switzer, Chevreul's
colour names still in the italic, split into two pseudo-elements), and the
three meters fixed earlier. Figures inside running prose stay in the face
they belong to. The meters also declared Switzer at 300, a weight the site
never loads: they now say 400, what they always rendered.

**Two things decided with the user.** Motion is the content here: no
effort goes into `prefers-reduced-motion` variants (it moves no SEO signal,
and a still showcase shows nothing); the rules already in place stay. And
Google Fonts only as a convenience for script coverage (the Marquee's Noto),
never for a curated choice of face; fonts may stay on CDNs.

## The mark, 2026-09-23

The old mark, a half-filled disc in a ring, read as any app's icon and pulled
the site's look down. It is the site's only artwork of its own: the page
chrome names Mocubix in text. Candidates were judged at 16 to 128 px and in
light and dark tabs. A house curve, a rolling cube, an onion-skinned M and a
streak went first; of a terra M, the M on a two-leaf split flap with hinge
pins, the terra M cut by a split, and a speed stroke, the user chose the cut
M: the institution's face in the one accent, with a seam that suggests a
state about to change and none of the flap's parts that turn to noise at
16 px.

An SVG favicon renders as an image and loads no web font, so the M is
Melodrama Bold's own outline: straight lines, twelve corners, taken once with
fontTools and kept in font units in `build/mark.py`, which writes the SVG, the
ICO (16, 32 and 48 px) and the 180 px apple-touch icon from one geometry. On
its 32-unit grid a unit is a device pixel on a 16 px tab at 2x, so the M's top
and baseline and the split's edges sit on whole units: the M from 7 to 24, the
split from 15 to 16. The V's notch ends inside the split, so the upper half
reads as two strokes and the lower as the V. The font's licence (name table,
ID 13) asks that ITF faces be named and ITF credited in production credits;
the README does.

## Every page shows its source, 2026-09-23

The site is meant to be taken apart: a person who likes an effect, or an
agent asked to build one, should get from the page to its code in one step.
Each page now links to its own folder in the repository, in the chrome where
the eye already goes for the way back and the switch: top right on the front
door and the exhibits, where the source and the switch share one plate (the
corner), and in the Lexicon's bar. The link is written into each page's HTML,
so crawlers and agents read it; its mark, an open tag, is drawn once in
`house.js` and moves only when pointed at or focused: the brackets part and
the slash is written again. A showcase also lists its files, whole, under the
excerpt in How it is built.

For machines, each page's JSON-LD says what the page is and what it is built
from (`isBasedOn`, a `SoftwareSourceCode` with the folder and the repository),
and `site/llms.txt` lists every page with its description and its folder, in
the site's own order: the exhibits as the front door shows them, the Lexicon
by pillar, with its showcases marked. `build/sitemap.py` writes it with the
sitemap and refuses to run while any page's link names another folder.

The chrome's class names are now reserved: Scoped Rotation's thumbnail of
the painting was `.source`, and became `.original`.
