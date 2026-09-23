# Measured Anatomy

First-party measurements taken here, in a real browser, against live sites. One section per site.

This file exists because of the charter's **Measure; never eyeball** law, and because secondary descriptions of craft have repeatedly proven wrong — including descriptions produced inside this project. What a curator, an award listing, or a research summary says a site looks like is a lead. What `getComputedStyle` returns is evidence.

**Method.** Open the page, run one aggregation script over every rendered element, close the page. Colours are weighted by **painted area**, not by count, because area is what the eye reads as dominant. Type roles are deduplicated by the tuple (family, size, weight, line-height, tracking, transform) and ranked by instance count. Easing and duration are censused across every element carrying a transition.

---

## cerebrium.ai — measured 2026-09-15

Serverless GPU infrastructure product site. Awwwards Site of the Day + Developer Award, 2026-09-10.
**Date caveat:** that date is an award date, not a first-party launch date. Per `RESEARCH-METHOD.md` it is a lead, not proof. The measurements below are first-party regardless — they are what the live site rendered on the date measured.

Measured at desktop width. 3,909 elements, 1 h1, 6,062 characters of rendered text, **1 canvas**.

### Type

Three families, no more, and a strict division of labour:

| Family | Uses | Role |
| --- | --- | --- |
| Suisse Int'l | 1,197 | everything that reads as text |
| Suisse Int'l Mono | 160 | labels, eyebrows, UI micro-copy |
| ABC Favorit | 60 | display only |

**All self-hosted woff2 from the site's own origin. Zero external stylesheet hosts.** Total type payload **108 KB**: SuisseIntl-Regular 61 KB, ABCFavorit-Light 33 KB, SuisseIntlMono-Regular 14 KB.

**The display face runs at weight 300.** ABC Favorit Light at 144px, 86.09px, 72.61px, 57.39px, 43.91px — large and light, not large and bold. This is the least obvious choice on the page.

**One tracking rule, scaled across the whole ramp.** Letter-spacing is consistently ≈ **−0.05em**, applied proportionally rather than picked per size:

| Size | Tracking | As em |
| --- | --- | --- |
| 86.09px | −2.15px | −0.025 |
| 72.61px | −1.82px | −0.025 |
| 57.39px | −2.87px | −0.050 |
| 43.91px | −2.20px | −0.050 |
| 36.09px | −0.90px | −0.025 |
| 26.52px | −0.66px | −0.025 |
| 21.26px | −0.53px | −0.025 |

**Type is fluid, not stepped.** Sizes land on 26.5214px, 43.9117px, 57.3909px, 72.6086px, 86.0864px — non-integer values mean `clamp()` / vw interpolation, not breakpoint switching.

**The single most repeated role is a label, not a heading:** mono, 13px, weight 400, line-height 13.91px, tracking −0.325px (−0.025em), uppercase — **65 instances**, carried by a custom element `<c-scramble-text>` (a character-scramble reveal).

### Palette, by painted area

| Colour | Hex | Painted area (px²) | Role |
| --- | --- | --- | --- |
| rgb(16, 20, 33) | `#101421` | 17,521,618 | the ground — near-black, cooled toward navy |
| white | `#FFFFFF` | 6,227,016 | inverted sections |
| rgb(238, 242, 245) | `#EEF2F5` | 4,569,879 | cool light fill |
| black | `#000000` | 2,718,720 | |
| rgb(219, 229, 237) | `#DBE5ED` | 2,049,492 | |
| rgb(23, 43, 118) | `#172B76` | 226,024 bg · 1,242,432 text | the deep blue — mostly ink, rarely fill |
| rgb(255, 72, 139) | `#FF488B` | 89,404 bg · 19,939 text | **accent** |
| rgb(246, 24, 106) | `#F6186A` | 50,619 | accent, second tone |

**The accent is ~0.48% of all painted area.** Roughly 160,000 px² of hot pink against ~33.5 million px² of ground, white and cool greys. Saturation is used as a scalpel, and the measurement is what proves it — no description of this site would have conveyed how little pink is actually on screen.

One `oklab()` value is present in the computed styles, so modern colour syntax is in use, if only just.

### Motion

**Two curves carry almost everything** — 226 of roughly 245 transitions:

| Curve | Uses | Identity |
| --- | --- | --- |
| `cubic-bezier(0.4, 0, 0.2, 1)` | 128 | the Material standard curve |
| `cubic-bezier(0.645, 0.045, 0.355, 1)` | 98 | easeInOutCubic |

**0.2s is the workhorse** — 167 uses, against 0.4s ×28, 0.3s ×22, 0.6s ×5, 0.8s ×3.

Worth noting for this project's purposes: neither curve is distinctive. Both are defaults an engineer reaches for. On a site otherwise this disciplined, motion is the dimension that was *not* authored — which is precisely the gap the charter's **Nothing ships at default** law points at.

### Geometry

One radius does the work: **7px, 270 uses**. Then 10px ×34, 6px ×12, 100% ×10 (circles), 15px ×4, 4px ×2, 32px ×2. The specific value matters — 7px is not 8px, not a framework default, and not a round number.

---

## basement.studio — measured 2026-09-15

Design and engineering studio, own site. Measured at desktop width with the identical script used on cerebrium.ai, so the two are directly comparable.

**681 elements**, 1 h1, 2,742 characters of rendered text, **2 canvases**.

### Type

**One family carries the entire site.** Geist (431 uses), Geist Mono (3 uses), Times (1, an unstyled stray).

Self-hosted, 3 files, **66 KB total**. Stylesheets come only from the site's own origin.

**Every size runs at weight 600.** 13px/600, 20px/600, 24px/600, 38px/600, 76px/600, 87px/600 — weight 500 appears twice, 400 once, and nothing else exists. One family, one weight, for the whole page. This is the opposite pole from cerebrium.ai's Light-300 display, and equally deliberate.

**Display line-height sits below 1.0**, consistently ≈ 0.89: 87px/78px, 76px/68px, 38px/33.82px.

**Tracking is ≈ −0.04em on display**, relaxing at small sizes: 87px→−3.48px, 76px→−3.04px, 38px→−1.52px, 24px→−0.72px (−0.03em), 20px→−0.4px (−0.02em), and `normal` at 13px and below.

**The ramp is stepped, not fluid** — 9, 12, 13, 20, 24, 38, 76, 87px, all integers. The opposite of cerebrium.ai's `clamp()`-interpolated ramp.

### Palette, by painted area

| Colour | Hex / notation | Painted area (px²) | Role |
| --- | --- | --- | --- |
| black | `#000000` | 19,622,431 | the ground, pure black |
| black @ 0.9 | `rgba(0,0,0,0.9)` | 1,241,280 | overlay |
| rgb(196,196,196) | `#C4C4C4` | 1,024,508 text | body ink |
| rgb(230,230,230) | `#E6E6E6` | 422,672 text | brighter ink |
| `color(srgb 0.901961 …)` | ≈ `#E6E6E6` | 122,512 text | modern colour syntax in use |
| rgb(117,117,117) | `#757575` | 79,265 text | dim tier |
| rgb(255,77,0) | `#FF4D00` | **1,764 text · 36 bg** | accent |

**The accent occupies ~0.0086% of painted area** — roughly 1,800 px² of orange against ~20.9 million px². For comparison, cerebrium.ai's accent is 0.48%: **basement.studio is 56× more restrained.** No written description would convey this; only area weighting does.

### Motion

| Curve | Uses |
| --- | --- |
| `cubic-bezier(0.4, 0, 0.2, 1)` | 57 |
| `linear` | 27 |

Durations: **0.3s ×47**, **0.06s ×27**, 0.2s ×5, 0.1s ×4, 0.15s ×1.

The 27 `linear` transitions pairing exactly with 27 instances of 0.06s is the signature of a **character-scramble / glitch-text reveal** — the same technique family as cerebrium.ai's `<c-scramble-text>` element. Two unrelated studios, same trick.

### Geometry

**Essentially no radius.** 9999px ×4 (pill chips) and 4px ×1. Everything else is square. Against cerebrium.ai's 7px ×270, this is the other extreme.

---

## immersive-g.com — measured 2026-09-15

Immersive Garden, French interactive studio; Awwwards Agency of the Year tier. Same script again.

**784 elements**, 1 h1, 2,401 characters of rendered text, **8 canvases** — by far the heaviest page measured here.

### Type

Three families: an unstyled `sans-serif` inherited by 383 elements, **HelveticaNeueRegular** (119) for text, **PSTimes, serif** (69) for display. Self-hosted: PSTimes 50 KB + HelveticaNeue 9 KB = **59 KB**.

**A serif carries the display role** — the only one of the three sites to do so; the other two both use grotesks.

**Five sizes exist on the entire page**: 14px (58 uses), 22px (20), 12px (18), 44px (9), 28px (8). That is a tighter ramp than basement.studio's eight and cerebrium.ai's fourteen.

**Everything is weight 400.** Not a light display, not a uniform 600 — plain regular throughout.

**Letter-spacing is `normal` everywhere.** Zero tracking adjustment at any size, including the 44px h1. Both other sites scale negative tracking carefully across the ramp; this one does not touch it at all.

**Line-heights are authored as clean ratios** — 1.10 (14/15.4, 12/13.2, 44/48.4), 1.20 (28/33.6, 44/52.8), 1.40 (22/30.8).

### Palette, by painted area

| Colour | Hex | Painted area (px²) | Role |
| --- | --- | --- | --- |
| rgb(232, 232, 232) | `#E8E8E8` | 3,723,840 bg · 35,432 text | the ground — light, not dark |
| rgb(3, 3, 3) | `#030303` | 1,050,328 text · 1,349 bg | ink |
| black | `#000000` | 572 text · 12 bg | stray |

**Three colours on the whole page, and no accent at all.** Light-mode, near-monochrome. Against cerebrium.ai's 0.48% accent and basement.studio's 0.0086%, this is zero — the colour work is carried entirely by the canvases.

### Motion

| Curve | Uses |
| --- | --- |
| `ease` | 129 |
| `ease-in-out` | 53 |
| `cubic-bezier(0.165, 0.84, 0.44, 1)` (easeOutQuart) | 4 |
| everything else | ≤ 2 each |

Durations: **0.25s ×123**, **1.9s ×53**, 0.5s ×7, 0.8s ×2.

The 1.9s ×53 pairing exactly with `ease-in-out` ×53 is a slow ambient loop — a genuinely authored, distinctive choice. But the dominant curve is the bare CSS keyword `ease`.

### Geometry

**`100%` × 124, and nothing else.** Every rounded thing on the page is a full circle; everything else is square. A third site, a third completely different radius stance.

---

## What the three measurements say together

| | cerebrium.ai | basement.studio | immersive-g.com |
| --- | --- | --- | --- |
| Elements | 3,909 | 681 | 784 |
| Canvases | 1 | 2 | **8** |
| Type families | 3 | **1** | 2 + fallback |
| Display face | grotesk | grotesk | **serif** |
| Weights in use | 300 display, 400, 500 | **600 only** | **400 only** |
| Distinct sizes | 14 | 8 | **5** |
| Type ramp | fluid, `clamp()` | stepped, integers | stepped, integers |
| Display line-height | ≈ 1.0 | **≈ 0.89** | ≈ 1.10 |
| Tracking rule | ≈ −0.025 / −0.05em | ≈ −0.04em display | **`normal` everywhere** |
| Ground | `#101421` near-black navy | pure `#000000` | **`#E8E8E8` light** |
| Accent share of painted area | 0.48% | 0.0086% | **none** |
| Radius | 7px, 270 uses | none | **100% only, 124 uses** |
| Type payload | 108 KB | 66 KB | 59 KB |
| Workhorse duration | 0.2s | 0.3s, plus 0.06s | 0.25s, plus 1.9s |
| Dominant easing | **`cubic-bezier(0.4, 0, 0.2, 1)`** | **`cubic-bezier(0.4, 0, 0.2, 1)`** | **`ease` / `ease-in-out`** |

Three award-tier sites that agree on almost nothing. Dark navy, pure black, light grey. One family, one-plus-mono, two-plus-serif. Fluid against stepped. A 7px radius everywhere, no radius at all, circles only. Tracking scaled to the em, and tracking never touched. Every craft axis is contested.

**They converge on exactly one thing, and it is the wrong one.**

| Site | Dominant easing | What it is |
| --- | --- | --- |
| cerebrium.ai | `cubic-bezier(0.4, 0, 0.2, 1)` ×128 | Material Design standard curve |
| basement.studio | `cubic-bezier(0.4, 0, 0.2, 1)` ×57 | Material Design standard curve |
| immersive-g.com | `ease` ×129, `ease-in-out` ×53 | bare CSS keywords |

**Three out of three default on their dominant motion curve.** Immersive Garden is Agency-of-the-Year tier and the curve carrying most of its page is the unmodified `ease` keyword. Each of these studios authored type, colour, density and geometry to the pixel — and each reached for stock when it came to easing.

Authored curves do exist in the measurements, but only at the margins: Immersive Garden's 1.9s `ease-in-out` ambient loop (53 uses, genuinely distinctive) and a handful of `easeOutQuart` instances. The signature moments are authored; the connective tissue is not.

**Finding: motion is the dimension where even frontier work defaults.** This is direct measured support for the charter's *Nothing ships at default* law, and it names the specific opening — **an authored motion signature is rarer than an authored palette**, so it is cheaper differentiation per unit of effort than anything else measured here.

**Watch item for the exhausted list:** character-scramble / glitch text reveals appear on both cerebrium.ai (`<c-scramble-text>`, 65 instances) and basement.studio (27 × 0.06s linear), implemented the same way. Two of three is a flag, not yet a verdict.

---

## Measured here, while building

Platform behaviour established by probing Chrome directly during construction of `artifacts/` (now `site/`). Recorded because none of it is stated in the documentation, and each cost a debugging cycle.

### Feature support is not the problem

Confirmed live via `CSS.supports()` on 2026-09-15: `animation-timeline: scroll()`, `animation-timeline: view()`, and `animation-range: entry 0% cover 50%` all return **true**. Scroll-driven animation is fully usable today in the development target. The failures below were authoring errors, not gaps.

### `scroll()` is exact, and free

Measured on `artifacts/01-scroll-timeline.html` (now `site/annie-g/`): a rail bound to `animation-timeline: scroll(root)` tracked document progress to three decimals — `scaleX(0.2998)` at 30%, `0.6199` at 62%, `0.9498` at 95% — with **zero JavaScript**. Same result on the horizontal track in `02`: `translateX` hit −383, −766, −1149, −1532 px against a measured 1532 px of overflow, linear and exact.

### `view()` collapses on a subject with no usable extent

**The finding worth keeping.** A progress bar implemented as `position: absolute; inset: 0` inside a 2px-tall parent, bound to `animation-timeline: view()`, resolved to a **constant `scaleX(0.5)` at every scroll position** — across four independent instances, at 30%, 55% and 80% of the page.

It is not a support gap. Sibling headings on `view()` in the same document cascaded correctly in the same samples:

| Scroll | Heading opacities |
| --- | --- |
| 30% | 1, 0.33, 0, 0 |
| 55% | 1, 1, 0.51, 0 |
| 80% | 1, 1, 1, 0.69 |

`view()` measures **the animated element's own box** against the scrollport. A 2px sliver has effectively no entry or exit phase, the range degenerates, and the animation resolves to a midpoint rather than erroring or clamping — it fails silently, at a plausible-looking value.

**Fix:** publish the timeline from the element that has real extent and bind descendants to it by name — `view-timeline-name: --itemView` on the article, `animation-timeline: --itemView` on the bar. Never let a hairline measure itself.

A first attempt that removed `position: sticky` from the bar's parent changed nothing, which was the clue: sticky was a plausible culprit and an irrelevant one.

### A mechanism can be correct and still demonstrate nothing

`02` initially overflowed its frame by **272 px** across a 3275 px scroll runway — mathematically correct, visually imperceptible. Horizontal travel needs to be on the order of a viewport width before the axis change registers at all. Rebuilt at 1532 px of travel (1.06 viewports) with seven cards instead of four.

Correctness and legibility are separate checks. Passing the first says nothing about the second.

### Every fault found by looking was invisible to probing

All six mechanisms passed numeric verification. Three real faults were then found by taking a screenshot, and **not one of them would ever have surfaced in a probe**:

| Page | What the numbers said | What the picture showed |
| --- | --- | --- |
| `index` | Six cards present, all links valid | `auto-fit` resolved to 4 + 2 with a dead cell showing through — reads as a bug |
| `04` | Timelines correct, four distinct values | Half a viewport of void before the first item, and no scroll affordance at all — reads as the page ending |
| `06` | Layer offsets exact, animations running | At rest the glow and rings wash the document text to near-illegible — on a page whose entire argument is *DOM owns meaning* |

The `06` case is the sharpest: a layered composition has to be **legible in its collapsed state**, because that is the state it is argued about in. Decoration that only resolves once the viewer interacts is decoration that failed.

### `backdrop-filter` blurs what is beneath it, whatever its own opacity

The `06` washout took **three attempts** because the first two treated it as an opacity problem. The sequence is worth keeping, because each step was a reasonable guess that measurement then refuted:

| Attempt | Theory | What measurement said |
| --- | --- | --- |
| 1 | Overlay layers too strong — scale their opacity with the separation value | `.geo` and `.tick` obeyed at `0.15`. **`.shade` read `0.848`** and ignored the rule |
| 2 | `.shade` ignores it because an **animated** property outranks a static declaration; fold the variable into the keyframes | Worked — `.shade` fell to `0.080`. **Text still washed out** |
| 3 | Something above the text is filtering it, not dimming it | Layer 1's `.plate` carried `backdrop-filter: blur(1px)` and paints above the document layer. Stripping it restored legibility with **every opacity value unchanged** |

Two distinct traps, stacked in one element:

1. **An animated property beats a static declaration.** A `@keyframes` block that sets `opacity` silently overrides any `opacity` rule on that element. To make an animation respect a variable, the variable has to appear *inside the keyframes*.
2. **`backdrop-filter` is not opacity.** It filters the backdrop — everything painted beneath the element — and no amount of reducing its own opacity or its background alpha changes that. A 1px blur on a transparent plate was enough to smear the text two layers below it.

**Rule:** a numeric probe proves the mechanism runs. Only looking proves it communicates. The charter demands both, and the second is where the failures actually were.

**Corollary:** when a fix measurably applies and the symptom persists, the theory is wrong, not the fix. Attempt 2 was correct and insufficient — keeping it and looking again was what found attempt 3.

### Never hide the mechanism to make a page fit

The phone pass at 390×844 found a defect in **four of six** pages, all invisible at desktop width:

| Page | Defect at 390px |
| --- | --- |
| `01` | A media query hid `.intro` **and `.steps`** — but the four-step list *is* the mechanism, so a phone visitor watched shapes change with nothing to read them against |
| `02` | 240px cards clipped the second card mid-heading; no partial width avoids this, so the fix was near-full-bleed with a thin edge as the affordance |
| `03` | Combs resolved to 4px wide — the demo's entire visual payload all but vanished |
| `05` | The field sat below a full-viewport sidebar and never appeared on screen at all |

`01` is the one to remember. Hiding a block is the reflexive way to make a layout fit, and here it silently deleted the thing the page exists to demonstrate. **On a page whose subject is a mechanism, the explanation is not chrome — compress it, never remove it.**

`05` also produced a false alarm worth recording: its instance count fell from 169 to 70 on mobile, which looked like a regression. It is the floor in `max(70, w·h/5200)`, and at phone dimensions 70 marks are *denser* per unit area than 169 were on desktop. Not every changed number is a defect — check the formula before fixing it.

---

## Corrections to earlier project data

Both errors below came from research produced inside this project, not from the open web. They are recorded because `RESEARCH-METHOD.md` catalogues unreliable secondary description, and this is the fourth instance of that pattern — this time originating in-house.

| Claim | Source | Measured |
| --- | --- | --- |
| cerebrium.ai has **0 canvases** | earlier research pass | **1 canvas** |
| basement.studio has **0 canvases** | earlier research pass | **2 canvases** |
| immersive-g.com has **2 canvases** | earlier research pass | **8 canvases** |
| palette is `#172B76` / `#902177` | earlier research pass | `#172B76` correct; the accent is **`#FF488B`** and **`#F6186A`**. `#902177` does not appear on the page. |

---

## Note: foundry news pages are weak date sources

Checked 2026-09-15 while looking for dated 2026 type releases:

- **commercialtype.com/news** — **no visible dates anywhere**, on any item. Fails the provenance rule by construction, like Httpster and Godly.
- **abcdinamo.com/news** — dates appear **only on newsletter items** (September 2026 "Areal is now available free for everyone"; July 2026 "The Return of Gravity"; one June 2026 item). Release Notes and Guest Essays carry no dates at all.

Foundries are first-party about their own releases, which should make them ideal sources — but most do not publish dates on release pages. Typography research at this project's date bar will have to lean on release tags in version control, dated newsletters, and specimen pages carrying explicit release dates, rather than on foundry news feeds.
