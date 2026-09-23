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
