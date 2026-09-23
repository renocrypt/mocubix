# Mocubix — frontier UI/UX exhibition

Mocubix is a frontend-only static exhibition of scroll-based interaction design: technically accurate terminology demonstrated through vivid, original experiences, with the aesthetic ambition and execution expected of an S-tier design firm.

## Main objective

Build a demonstrated vocabulary of dynamic content presentation through scrolling. Three requirements carry equal weight:

- **Technical accuracy.** Names and explanations must match the running mechanism. Distinguish scroll-driven progress, scroll-triggered playback, velocity response, pinning, snapping, visual techniques, and narrative purpose. Identify adjacent time-driven or pointer-controlled examples by their actual input.
- **Vivid, distinctive demonstrations.** Provide enough working examples to make materially different mechanisms and their combinations understandable. Each exhibit uses a real subject and original composition to show how interaction reveals, compares, explains, or sequences content. Coverage is judged by meaningful differences and clarity, not example count alone.
- **Exceptional aesthetics.** Art direction, typography, composition, imagery, colour, motion choreography, and interaction detail must form a deliberate, coherent experience. The S-tier design-firm standard is a quality target: every demonstration must be visually compelling and individually resolved, with polish sustained across desktop, phone, and reduced-motion presentations. Technical correctness and breadth do not compensate for weak aesthetic execution.

Effects exist to drive content and context, never as decoration. Each exhibit is a working mechanism paired with an English wall label that explains what it does and why that matters.

**North star (the user's, 2026-09-22).** Once the design is approved this becomes a front-end-only web app that can be shared, and that other agents use as a reference guide — "I want this presentation; tailor it for my project." Not a reason to re-engineer now; the tiebreaker for every decision now: prefer reusable parts and clean seams to one-off code.

**It is a collection, not a chosen direction.** There is no single winning concept to approve — the mechanisms are the holdings. Build them.

## Laws

Every law below was written after breaking it. None is decorative.

### The work

- **Demonstrate, never describe.** A deliverable is a thing that runs. A document *about* an effect, a type specimen, a mood board, a pitch deck — none of these are deliverables here. If the reader cannot scroll it and feel it, it is not done.
- **Nothing ships at default.** Type, layout, palette, motion, and the way they combine must each be resolved to elegance. One unconsidered choice anywhere reads as an unconsidered project everywhere. Motion is where this is hardest and rarest — see `docs/MEASURED-ANATOMY.md`, where three award-tier sites all defaulted on their easing curve.
- **Lead, do not match.** Evidence maps the floor, not the target. Work that reads as 2025 is late; work that reads as 2026 is merely current. Design along the vector the evidence points down and ship the bet before it is safe.
- **The page speaks to the visitor.** Working rules, measurements, provenance and process belong in code comments, `notes/` and this file — never in copy. A sentence that explains how the work was done rather than what the visitor is looking at is not copy; cut it. The visitor is the client, not the reviewer.
- **Every exhibit has a subject; the mechanism serves it.** A page about its own mechanism, dressed in whatever material is to hand, is the junior tell. Each exhibit is a real thing — a mare, a storm, a volcano, a departures board — with its own body of material, its own vibe, and one mechanism doing real work for it. Never reuse one body of material across exhibits.
- **Bold, not subtle.** If the visitor can say "I could theme this by hand", the effect is not demonstrated. Full-screen material, large surfaces that change, state that visibly snaps, instruments that visibly move.
- **Create a distinct visual and interaction identity.** Extract principles from references, never clone them.

### Scope

- **Build what was asked. Do not infer adjacent requirements.** A stated constraint means exactly what it says and nothing more. Do not widen it, do not derive corollaries from it, and do not import standard industry practice it did not ask for.
- **Two constraints that are not the same constraint.** SEO/GEO is satisfied by real DOM text in prerendered HTML and has nothing to do with the rendering layer. Visitor browser support is a separate product decision. Conflating them invents work nobody wanted.
- **WebGPU-first, no compatibility ladder** — do not build fallbacks for GPUs this project is not for. **This is not permission to block small screens.** Every exhibit works down to phone width. Hardware selectivity and responsive layout are unrelated.
- **Standards-process participation is not this project's work.** What browsers will support constrains what gets built. Changing what browsers support does not.

### Delivery

- **The site is plain HTML in `site/`, published as a static site on GitHub Pages.** No framework, no bundler, no animation library by default; what the browser does natively is the exhibit. No artifact platform, no canvas tooling, no intermediate format. One folder per page (`site/florence/index.html` is `/florence/`), real DOM text throughout. **Addresses are permanent**: once published, a page's folder name never changes. Folder addresses do not open from disk, so preview through a local server: `python3 -m http.server 8765 --directory site`. The pages share `house.css` (the tokens, both palettes, the switch) and `house.js` (the switch's boot), plus parts from `site/parts/`, reached from a page as `../house.css`. A page never writes a colour of its own; it consumes tokens, mixing them with `color-mix()` where it needs an alpha. The exceptions are documented material, declared once in a marked block and left alone by the palette switch: 05's board enamel, sampled from photographs; 02's night side, which keeps the night tokens in both palettes because it is the night; 06's sky, the dark the planet photographs were taken against.
- **A part is one self-contained custom element per file** in `site/parts/`: no dependencies, a classic script so it works from `file://` and inside any framework, themed only through custom properties, its value kept as real DOM text, and documented in its own header — attributes, script API, custom properties, behaviour — so a person or an agent can lift the file into another project unchanged. A part exists because a page needed it, never ahead of need. Anything instantiated by the hundred costs nothing at rest: no static transforms, no clips, no layers; structure that only matters in motion exists only in motion. See `notes/DECISIONS.md` (05).
- **English carries the work** — interface copy, explanation, code, comments, filenames. CJK is an experimental lane for visual expression only, never the interface.
- **DOM owns meaning; the canvas is augmentation.** Every word that matters ships as real DOM text in the HTML as served: a script may move, reveal or re-order what the HTML already holds, never write it, because crawlers that run no JavaScript must still read the whole page. The canvas is never the only source of any content, heading, link, or LCP candidate.
- **Verify in-browser before calling anything complete** — desktop, phone width, reduced motion, and realistic performance. **Measure; never eyeball.**

### Machine and browser discipline

- **The user's machine outranks any process.** If it is hot, loud, or struggling, stop what is running first and explain afterwards. Never argue for a running job over the machine it runs on.
- **Do browser work directly, never through subagents.** Dispatched agents fan out invisibly into more agents, each with its own browser, opening pages faster than they can be closed.
- **One page at a time.** Open it, extract everything needed in a single script, close it. Open measurement targets with `background: true` so animation throttles. `close_page` refuses the last page — navigate it to `about:blank` instead.
- **Delegate reading, not rendering.** Subagents are fine for fetching and summarising text. They are not fine for anything that opens a browser.

### Evidence

- **Use current evidence only; research must be dated 2026 or later**, and **every date must come from the work's own source** — a studio project page, a first-party making-of, a release tag, a spec publication. Never a curator, an award page, or a search summary. See `docs/RESEARCH-METHOD.md`.
- **Secondary description is unreliable, including this project's own.** Four separate instances are catalogued. Measure the thing rather than reading about it.
- **An honest "this cannot be met at our bar" beats a quiet citation of a stale page.** Withdraw contaminated evidence rather than softening it; record the withdrawal so it is not re-added.

## Map

- `site/` — everything that is published. `index.html` is the front door; the exhibits are `annie-g/`, `night-side/`, `florence/`, `urformen/`, `departures/`, `orrery/`, `kilauea/` (01–07); `lexicon/` is the Lexicon, the collection's reference wing: every effect named, glossed and running. `house.css` and `house.js` are the two shared files: tokens for both palettes, and the switch.
- `site/parts/` — reusable parts, one custom element per file, each documented in its own header. `split-flap.js` (05) is the first.
- `build/` — the Lexicon generator. `python3 build/build-lexicon.py` rewrites `site/lexicon/index.html` from `build/lexicon.template.html` plus the specs table. Edit the specs, never the generated file.
- `assets/` — curated material. Only URLs the Wikimedia API actually returned; widths are the buckets it really serves. Never hand-typed, never width-rewritten. `build/curate.py` holds the works list (one `kind` per exhibit: `muybridge`, `iss`, `storm`, `blossfeldt`, `solari`, `planet`, `kilauea`, plus the Lexicon's `sekka` and `atkins`) and merges into `assets/curated.json`. Pages inline the resulting `<img>` tags; nothing is fetched at runtime but the images themselves.
- `notes/DECISIONS.md` — the asset and typography evidence log: what was tested, what loaded, what was rejected and why.
- `notes/evidence/` — before/after screenshots and measurement crops per exhibit, named `NN-before-*`, `NN-after-*`. Local only: ignored by git (72 MB).
- Repository: `renocrypt/mocubix` on GitHub. Only `site/` is published.
- `probes/` — the one-off browser pages that produced those verdicts. Kept as evidence, not as deliverables.
- `docs/RESEARCH-METHOD.md` — how evidence enters this project, the failure modes that made the provenance rule necessary, and the source map.
- `docs/MEASURED-ANATOMY.md` — first-party measurements taken here against live sites: type ramps, area-weighted palettes, easing and radius censuses.
- `docs/2026-design-directions.md` — forward design signals. Two sections withdrawn on provenance.
- `docs/2026-interaction-taxonomy.md` — precise interaction language.
- `docs/2026-observed-case-studies.md` — dated observed work. Two entries withdrawn on provenance.
- `docs/2026-platform-and-production-signals.md` — platform and production evidence.
- `docs/2026-generative-and-geometric-work.md` — generative and data-driven material; the explanation gap and the empty reduced-motion field.
- `docs/2026-cjk-typography.md` — the CJK experimental lane: an empty production field, open-source material, hard delivery constraints.
- `docs/2026-discoverability-and-performance.md` — measured evidence that heavy visuals and discoverability are an architectural choice, not a trade-off.

## House identity

Current, and open to revision — but revised deliberately, never drifted.

| | |
| --- | --- |
| Night ground | `#0B0A09` · raise `#131110` · lift `#1A1715` |
| Night ink | `#F2EDE5` · mid `#B4ABA0` · dim `#7E766D` |
| Night accent | terra `#D4673F`, kept under ~0.5% of painted area · indigo `#6E86B8` for measured/derived values only |
| Day ground | `#F4F0E9` · raise `#ECE7DF` · lift `#E5DFD6` — the same hues, re-set for paper |
| Day ink | `#1D1814` · mid `#585149` · dim `#7C756C` |
| Day accent | terra `#BA4E24` · indigo `#49649F` — deepened so labels still clear 4:1 on paper |
| Line | `color-mix(in srgb, var(--ink) 13%, transparent)` — follows whichever ink is current |
| Switch | night is the house default; the visitor's choice persists; the swap is one view transition on the house curve |
| Display | Melodrama for the institution (index, Lexicon index). Each exhibit carries one **guest display face** chosen for its subject and set on the page as `--display`: 01 Boska · 02 Panchang · 03 Zodiak · 04 Gambetta · 05 Khand · 06 Rowan · 07 Tanker. Text, mono, navigation and the switch never change. |
| Text | Switzer |
| Label | Geist Mono Variable |
| CJK | Source Han Serif SC 思源宋体 — one face, three scripts, one em grid |
| House curve | `cubic-bezier(0.16, 0.84, 0.24, 1)` — fast departure, long quiet arrival |

The curve is the point. It is authored, and the measured field is not.

**One guest display face per page, from a curated palette.** The palette (verified to load from Fontshare, 2026-09-20) is Boska, Zodiak, Gambetta, Rowan, Bespoke Serif, Sentient, Stardom, Britney for serifs and Panchang, Khand, Tanker, Technor, Plein for sans; faces with no italic (Panchang, Khand, Tanker, Technor) carry the accent word in colour alone, never in synthesized oblique. Each pairing states its reason in a one-line HTML comment beside the font link. See `notes/DECISIONS.md`. Lettering that belongs to a depicted object uses the object's own kind of face, not a display face: 05's LED clock is DSEG7 Classic (jsDelivr), and its flaps letter in Switzer, as Solari's lettered in Helvetica.

**No Google Fonts.** Not a preference — a ban. Instrument Serif and Martian Mono in particular are the house style of generated work, and anything wearing them is read as generated before a single interaction is tried. Faces are sourced from Fontshare and jsDelivr; each is verified to actually load by enumerating `document.fonts`, never by comparing advance widths. **Loading is not the same as working.** A CJK face can load every subset and still advance zero in `writing-mode: vertical-rl`; any face used vertically is verified a second time by measuring a vertical box. See `notes/DECISIONS.md` for the traps.

Revised 2026-09-16 from the earlier Instrument Serif / Martian Mono / `#0E0D0C` identity, which had drifted into two near-identical palettes across `artifacts/`. Deliberate, not accidental — the whole of `artifacts/` was repainted in the same pass so the collection reads as one system.
