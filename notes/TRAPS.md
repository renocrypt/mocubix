# Traps

Each of these cost time once. One line each, the way out after the dash. When a line turns out wrong, correct it rather than adding another.

## Layout

- `overflow: hidden` makes an ancestor a scroll container, and sticky pins and view timelines inside it stop working — use `overflow: clip`.
- A sticky element is held only within its container's content box — make room with a spacer element, not padding.
- `1fr` is `minmax(auto, 1fr)`, and `auto` is min-content: one wide child blows a track, and the page, wider than the screen — use `minmax(0, 1fr)`, for rows sized by tall images too.
- A sticky frame whose implicit grid column holds an overwide child grows to fit it — give the frame `grid-template-columns: minmax(0, 1fr)`.
- Grid auto-placement moves children nobody placed (a figcaption into a meter's column, a number swapped with its bar) — place grid children explicitly.
- `columns: 2` does nothing on a `display: grid` container.
- A stage with no top padding or border lets its first child's top margin collapse out of it — put the space in the stage's padding.
- An `img` with `width` and `aspect-ratio` must also set `height: auto`, or the height attribute wins.
- A lazy image sized by width with `height: auto` raises Chrome's "lazy-loaded images should have explicit dimensions" issue — pass `--ar` and set both dimensions from CSS.
- Lazy images inside an `overflow: clip` travelling track load only when on screen and pop in — load them eagerly.
- Inside `@scope`, a bare `:root …` never matches — write `:root … :scope …`.
- `lexicon.css` still has an unscoped `.btn` (absolute, bottom left) from the old demos — never name a showcase class `.btn`.
- A `span` selector inside a readout caught the counter itself — use child combinators in readouts.

- A page's own class can collide with the house chrome's (Scoped Rotation's figure was `.source`) — the chrome's names `back`, `theme`, `corner` and `source` are reserved.
- Links set apart by a flex gap read as one word to text extraction (`GitHubindex.html`) — put spaces between them in the markup; the flex row ignores them.

## Scroll-driven and animated

- The `animation` shorthand resets `animation-range`: a base `.x p { animation: … }` beats a per-item `.y { animation-range: … }` — write per-item ranges in the descendant form.
- `animation-timeline: none` does not neutralise a 0s fill-both animation in Chrome — use `animation: none`.
- An anonymous `view()` trigger takes no inset — use a named `view-timeline` with `view-timeline-inset` as the trigger's source.
- The site scrolls smoothly: a scripted per-frame `scrollTo` keeps restarting and scroll triggers never fire in a test — pass `behavior: 'instant'` (a test artefact, not a page bug).
- `effect.getTiming().easing` is always `linear` for a CSS animation — the real curve is per keyframe, in `getKeyframes()`.
- A `fullPage` screenshot of a scroll-driven page captures everything below the fold at scroll zero and looks broken — screenshot the viewport at chosen scroll positions.

## Custom properties and colour

- `@property` with `inherits: false` hides the value from `::after` on descendants — CSS-counter readouts need `inherits: true`.
- Chrome interpolates registered `<color>` properties in plain sRGB (the midpoint is the 8-bit mean), so a naive colour transition greys out — turn the hue of OKLCH tokens held at fixed lightness and chroma.
- The sRGB gamut is not a cylinder: at L 0.63 the most chroma runs from 0.107 (200°) to 0.302 (320°) — the direction of a hue arc is a gamut constraint, and a rotating palette needs L and C inside sRGB at every hue it passes.
- In relative colour syntax `h` is a number, so `calc(h + <angle>)` is invalid and the colour falls back to transparent — animate a registered `<number>` of degrees.
- `getComputedStyle` returns `oklch()` for authored colours and `rgb()` for interpolated ones, and a colour can compute right and paint wrong (Chrome did not repaint text coloured by `color-mix()` over a scroll-animated property) — read colour from painted pixels.
- An animated inherited custom property makes every element below its declaration re-resolve each frame, used or not, and the fresh computed styles leave garbage that costs more than the recalculation — declare it as low as it serves (on `:root` over 1,530 elements: 31.6 ms a frame; on the stage: 8.4 ms).
- A `:has()` in rules matching many elements is re-matched on every recalculation (five times the style work on 7,776 dots) — mirror the state into an attribute.
- A hue readout needs no script: a registered `<integer>` animated with the angle, then `counter-reset: d mod(calc(18 + var(--deg)), 360)`.
- `mix-blend-mode: lighten` in the paper's colour veils only the ink — hide and reveal printed marks without redrawing them.
- Fitting a circle to a printed plate by a chroma mask is biased where sectors are dull — fit to the disc's edge against the paper.

## Type

- Melodrama's zero is slashed in every setting — set figures that are the point of a display in Switzer (`AGENTS.md`, Figures).
- Switzer is loaded at 400, 500 and 600 only — a declared 300 silently renders as 400.
- `document.fonts` proves a file arrived, not that it works: measure a face used vertically in a `vertical-rl` box (Smiley Sans advanced 0 there).
- Wikipedia may store right-to-left text with its full stop at the logical start, for left-to-right embedding — move it to the end when setting `dir="rtl"`.
- Nastaliq sets visibly larger than Naskh or the Noto serifs at one size — scale it down (0.82em in the Marquee).
- An SVG favicon renders as an image and loads no web font — outline the letter into the path (`build/mark.py`).

## Images and Commons

- Commons throttles bursts (429, dropped connections) — pause and retry with backoff.
- An `imageinfo` query with about forty long titles overflows the URL (414) — batch five at a time, or POST.
- Commons renders PDF and DjVu pages only at 500 px, whatever is asked — find single-image scans for anything seen close.
- Commons snaps thumbnail widths to its own ladder (330, 500, 960, 1280, 1920 …) — record the widths it actually served.
- PNG-only scans run 6–9 MB at 3840 px — weigh the served bytes before choosing widths.
- Python `urllib` truncates large downloads (IncompleteRead) — use `curl`.
- Wikimedia sends `Access-Control-Allow-Origin: *` and `Timing-Allow-Origin: *`: a canvas may read its images (`crossorigin="anonymous"`) and Resource Timing reports their sizes.
- Canvas `drawImage` source rectangles are in the file's pixels, while `naturalWidth` is density-corrected and ignores `object-view-box` — crop by drawing the whole image into an offset destination rectangle.
- A Google Art Project file name does not say whose object it is — read the partner on the file page ("Plum Garden, Kameido" is Stanford's Cantor, not Brooklyn's).
- To crop a scan to its printed image, take the strongest step from paper into keyline near each edge — a darkness threshold fails on dark scan backgrounds and pale image edges.
- An object photographed on black hides what passes behind it with its black square — clip the photograph to the object's outline.
- To turn a photographed disc, turn only a clipped copy of its label: the grooves look the same at every angle, and the glints must stay where the light was.

## Verification and tooling

- The DevTools MCP's `resize_page` silently does nothing — use `emulate`, and confirm with `innerWidth`.
- Python's `http.server` sends no cache headers and Chrome serves stale CSS — preview with `build/serve.py`.
- GitHub Pages sends `max-age=600` — check the live site with `?v=<commit>`.
- Timing only the style work understated a page's cost fivefold — measure frame to frame.
- The build links a page's `showcase.js` only if the file exists when the page is built — rebuild after creating it.
- Browser work through subagents fans out into pages nobody closes — do it directly, one page at a time (`AGENTS.md`, Machine and browser discipline).
- A scratch page under `site/` is served, swept into the sitemap by `build/sitemap.py` and published if committed — delete it before building or committing.
- `pip` fails its certificate check inside the sandbox (OSStatus -26276) while `curl` works — take the wheel's URL from `https://pypi.org/pypi/<name>/json`, fetch it with curl and install the file.
- zsh expands an unquoted `--include=*.html` as a glob and aborts with "no matches found" — quote the pattern.
- When script evaluation in the browser is blocked, two channels still work: probe pages that write their results into the DOM (read back from a page snapshot), and 1:1 screenshots analysed locally with PIL.
- `build/sitemap.py` dates each page by its file's mtime, so a build that rewrites unchanged files moves every date to today; a build writes a file only when its content changed (`write()` in `build-lexicon.py`).
- A CSS animation starts at nought each time a rule applies it, so moving one animation between elements (a change of scope) makes it jump; set each one's `startTime` to 0 and they all share the document's clock.
