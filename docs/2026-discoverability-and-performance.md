# 2026 Discoverability and Performance

Evidence window: 2026-01-01 through 2026-09-15. Claims are labelled MEASURED, VENDOR-DOCUMENTED, or ASSERTED per `RESEARCH-METHOD.md`.

## Executive Finding

Heavy visuals and discoverability are not a trade-off. They are an architectural choice, and the line falls exactly where the existing research already put it: **DOM owns meaning, WebGL owns exceptional states.**

That pattern is now the difference between having Core Web Vitals and having none at all.

## 1. The Measured A/B

Two award-winning sites, same conditions — Chrome, Lighthouse 13.4.1, mobile emulation, 4× CPU throttle, Slow 4G. MEASURED.

| | landonorris.com — DOM+WebGL, **21 canvases** | bruno-simon.com — single full-page canvas |
| --- | --- | --- |
| LCP | **1007 ms** (TTFB 23ms, render delay 984ms) | **no LCP recorded at all** |
| CLS | 0.00 | 0.00 |
| Longest animation frame | 747 ms (693 ms blocking) | **18,703 ms** (646 ms blocking) |
| Rendered visible text | 3,298 chars | **0 chars** (parent `opacity: 0`, rect 0×0) |
| `h1` / `h2` | 1 / 12 | **0** / 6 |
| JS heap | 24.9 MB | 98.2 MB |
| Lighthouse SEO | **100** | 75 |
| Accessibility | **93** | 74 |
| Agentic Browsing | **100** | 33 |
| CrUX field data | none | none |

**Finding:** a 21-canvas site scored SEO 100 with a 1007 ms LCP under throttling. Canvas count is not the problem; canvas *monopoly* is.

## 2. Canvas Is Not an LCP Candidate

[W3C Paint Timing](https://www.w3.org/TR/paint-timing/) (2026-09-02) lists timing-eligible elements exactly: `img`, `image` inside `svg`, `video` with a poster frame, an element with a contentful `background-image`, and a text node. **Canvas is absent.** Canvas *is* "contentful" — it qualifies when its context mode is not `none` — so it counts for FCP but never for LCP. [Largest Contentful Paint](https://www.w3.org/TR/largest-contentful-paint/) (2026-08-26) defers entirely to Paint Timing; MDN corroborates (2026-08-28).

**Consequence:** on a full-bleed WebGL page, LCP attributes to some text block, poster `<img>` or `background-image` — never the scene. LCP is decoupled from when the 3D actually appears, in both directions. Element Timing cannot instrument canvas paint either; `PerformanceElementTiming` supports the same five types.

VENDOR-DOCUMENTED, and confirmed by the trace A/B above.

## 3. Canvas Has No Accessibility Semantics

[MDN's canvas reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/canvas) (2026-04-24) states it outright: *"Canvas content is not exposed to accessibility tools as semantic HTML is. In general, you should avoid using canvas in an accessible website or app."*

Google concedes the same by implication. The stated benefits of its [HTML-in-Canvas origin trial](https://developer.chrome.com/) (2026-05-19) include content being *"exposed to the accessibility tree"* and *"Indexability and AI agent interfaceable — web crawlers and AI agents can seamlessly index and read the text rendered into your 2D and 3D scenes."* An experimental API to fix a problem is an admission the problem exists.

That API is nevertheless disqualified for this project: *"HTML-in-canvas is drawn with JavaScript, which means that scrolling and animations cannot update independently of JavaScript."* It re-couples DOM content to the rAF loop — the opposite of what a jank-sensitive page needs.

## 4. Crawling in 2026

[Googlebot fetches only the first 2MB of any URL](https://developers.google.com/search/blog/2026/03/crawler-blog-post) (2026-03-31). Truncated bytes *"aren't fetched, they aren't rendered, and they aren't indexed."* The limit includes HTTP request headers. Referenced subresources get their own separate per-URL counter. Google's stated best practice: keep HTML lean, and **"Order matters"** — meta tags, `<title>`, `<link>`, canonicals and structured data high in the document.

The Web Rendering Service executes JS and CSS and processes XHR, but **requests no images or video**, and **operates statelessly** — it clears local and session storage between requests. Rendering is queued on evergreen Chromium with no latency commitment; non-200 pages may skip rendering entirely. ([JS SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics), 2026-03-04.)

Google deleted its "test with JS off" advice in March 2026, but the same page keeps the load-bearing sentence: *"server-side or pre-rendering is still a great idea because it makes your website faster for users and crawlers, and **not all bots can run JavaScript**."*

**Finding:** build-time static HTML is explicitly endorsed. Per-request SSR is nowhere required — which is the permission a GitHub Pages deployment needs.

## 5. GEO — What Does Not Work

**`llms.txt` is dead on the evidence.** [Ahrefs](https://ahrefs.com/blog/llmstxt-study/) (2026-06-15), all 137,210 domains with May 2026 traffic: ~28% publish one; only ~1,100 domains received any request at all — **97% were never requested**. Of requests that did occur, **AI retrieval bots were 1.1%**; SEO audit tools were 21%. The AI share of 404s on *missing* llms.txt was **zero** — *"AI tools never go looking for llms.txt files that aren't there."* MEASURED.

Google states flatly (2026-07-10): *"Google Search itself doesn't use them,"* and creating them *"will neither harm nor help your site's visibility or rankings."* The one contradictory signal is Chrome Lighthouse adding an "Agentic Browsing" category that audits for llms.txt; Mueller calls the file *"a temporary crutch."*

Of 10 award sites tested here, only 2 serve a genuine llms.txt; **2 more return HTTP 200 with `content-type: text/html` containing their own homepage** — SPA soft-404s that naive tooling scores as a pass. MEASURED.

**Structured data does not measurably help AI retrieval.** [Ahrefs](https://ahrefs.com/blog/schema-ai-citations/) (2026-05-11): 1,885 pages that added JSON-LD versus 4,000 matched controls, matched difference-in-differences plus three robustness checks — AI Overviews **−4.6% (p < 0.0004)**; AI Mode +2.4% and ChatGPT +2.2%, both indistinguishable from noise. Google agrees: *"there's no special schema.org markup you need to add."* MEASURED.

## 6. GEO — What Does Work

- **Relevance and position dominate; formatting does not.** [SIGIR '26 paper](https://arxiv.org/abs/2605.25517) (2026-05-25): 252,000 trials across 6 LLMs, 1,440 scenarios, 18 factors varied one at a time, brand-anonymized and order-counterbalanced. *"Topical relevance and list position are the biggest drivers of being cited first"*; formatting-only edits have little impact. MEASURED.
- **No technique has a durable effect.** [Meta-review of 45 studies](https://arxiv.org/abs/2607.14035) (2026-07-15): *"No reviewed technique shows a stable, longitudinal, cross-platform causal effect on organic discoverability"*; *"citation-oriented rewrites can impair retrieval."* MEASURED.
- **Retrievability beats ranking.** Pages ranking across multiple query-fan-out variants are **161% more likely** to be cited (Spearman 0.77). **Word count ↔ citations: Spearman ≈ 0.04** — length does not matter. (Ahrefs, 2026-01-20, 146M SERPs.) MEASURED.
- **Top-10 ranking now explains less than half of AI Overview citations**: top-10 37.9%, positions 11–100 31.2%, beyond 100 31.0% — down from 76% top-10 a year earlier. (Ahrefs, 2026-03-02, 863,000 SERPs.) MEASURED.
- **"URL accessibility" scores highest of 23 evaluated factors** (9.5/10), above search rank (9.4) and fan-out rank (9.3); Domain Authority only 5.0. (Zyppy, 2026-05-07, synthesis of 54 experiments; the author's own caveat is that correlation is not causation.) MEASURED.

**Finding:** GEO is not a technique layer. It is being genuinely relevant and genuinely accessible.

## 7. Core Web Vitals in 2026

**The metric set is unchanged.** LCP, INP, CLS at p75. Nothing added, retired, or re-thresholded. This rests on negative evidence: no change is announced in any [CrUX release note](https://developer.chrome.com/docs/crux/release-notes) (2026-09-08, all 12 monthly entries Jan–Aug 2026), and Google I/O 2026 announced none. **The numeric thresholds have no 2026-dated source** — every page printing 2500ms / 200ms / 0.1 is dated 2023–2025, and is recorded here as a gap rather than cited.

**August 2026 field baseline**, 18,294,881 origins: 68.1% good LCP, 81.5% good CLS, 85.3% good INP, **55.6% passing all three**. Chrome's own comment: *"The continued regression of INP in particular is a cause for concern, but we don't have a definitive reason for this."* MEASURED.

**Budget against INP, not LCP or CLS.** CLS measured 0.00 on both test sites — the CLS fear is misplaced. LCP is winnable. Long animation frames are where the exposure lives: 747 ms on the well-built site, 18,703 ms on the full-canvas one, against the LoAF **50 ms** threshold. Instrument with [LoAF](https://w3c.github.io/long-animation-frames/) (draft 2026-09-03) `blockingDuration`.

## 8. Platform Mechanisms Worth Using

- **Scroll-driven animations run on the compositor thread in Safari 26.4** — *"separate from the main thread"* — automatic, no opt-in, with `animation-timeline: scroll()` or `view()`. ([WebKit](https://webkit.org/blog/17862/), 2026-03-24.) The strongest 2026 mechanism for keeping scroll smooth while a WebGL main thread saturates. **But SDA did not reach Baseline in Jan–Aug 2026** — ship a fallback.
- **CPU Performance API, Chrome 152** (stable 2026-08-25) — lets a page determine device CPU performance and respond by *"scaling graphical fidelity, adjusting heavy computations, or tailoring background tasks."* The most directly actionable 2026 API for a heavy WebGL site, and a degrade-ladder trigger that actually exists.
- **Element-scoped view transitions, Chrome 147** (2026-04-07): `element.startViewTransition()` lets multiple transitions run concurrently without a full-page freeze.
- **`web-vitals` v6.2.2** (2026-09-14) caps pending LoAFs to avoid a memory leak — directly relevant to a continuous rAF loop.
- **Interop 2026** includes scroll-driven animations, view transitions, anchor positioning, scroll snap, Navigation API. It **excludes WebGL, WebGPU, canvas, and fonts entirely**.

**What the 2026 exclusions mean for this project — and what they do not.** The exclusion list explains why WebGPU, canvas and font behaviour are uneven across browsers. It is background, not a task. Standards-process participation is not this project's work.

**Two concerns that must not be conflated:**

| | What it needs | What it does **not** need |
| --- | --- | --- |
| **SEO / GEO** | Real DOM text in the prerendered HTML | Anything about the rendering layer |
| **Visitor browser support** | A product decision about who the audience is | Any bearing on discoverability |

Crawlers and AI engines read the prerendered DOM. Whether a human visitor's GPU supports WebGPU is irrelevant to that. **WebGPU and first-rate SEO/GEO are simultaneously achievable — this is a solved problem, not a constraint to design around.**

**This project's stance: WebGPU-first, no compatibility ladder.** Mocubix is a frontier exhibition, not a mass-market product, and targeting capable hardware deliberately is an established position in this tier of work. Chrome is the development and measurement target. Effort goes into the work, not into fallbacks for audiences the project is not for.

The architectural conclusions elsewhere in this document survive unchanged, because none of them were ever about browser support — canvas is not an LCP candidate, canvas carries no accessibility semantics, and real prose is what earns citation. All three are satisfied by **DOM owns the words**, regardless of what renders the pixels.

## 9. Tooling Status

**Healthy:** three.js — four 2026 releases (r183 through r186, 2026-09-08). GSAP 3.15.0 (2026-04-13). Lenis — 9 releases in 2026, and **v1.3.26 (2026-08-05) added respect for `prefers-reduced-motion: reduce`**. react-three-fiber v9.7.0 stable (2026-07-31).

**Do not depend on:**

| | Status |
| --- | --- |
| **r3f-scroll-rig** | The canonical library for this exact DOM+WebGL pattern — **zero 2026 commits or releases**; last release 2024-12-04 |
| **OGL** | Dormant; last commit 2025-04-13 |
| **Theatre.js** | Effectively abandoned; last release 2024-04-11 |
| **react-three-fiber v10** | In alpha all year (alpha.1 2026-01-17 → alpha.5 2026-09-08); not production-ready |
| **WebGPU** | **Not a safe 2026 baseline.** Safari ships by default; Firefox partial — Windows 141+, Mac Apple Silicon 145+, **Linux and Android still in development**; Chrome Linux Intel Gen12+ only. caniuse's 87.35% conflicts with the gpuweb implementation-status wiki (2026-08-13) and should be distrusted |

## 10. What a Static Host Can and Cannot Do

**Can:**
- **Be indexed exactly as well as SSR.** Google draws no distinction favouring per-request SSR over build-time static HTML. This is the key permission.
- Ship Speculation Rules via an inline `<script type="speculationrules">` — the header form is an alternative, not a requirement (MDN, 2026-09-10). Chromium-only; not Baseline.
- Serve HTTP/2 with gzip. MEASURED here on `octocat.github.io` and `resume.github.io`: HTTP/2, `content-encoding: gzip`, `cache-control: max-age=600`, fronted by Fastly. **No Brotli observed.**
- Use Search Console Generative AI performance reports (rolled out worldwide 2026-08-31 — impressions, pages, countries, devices; **no click data**) and Bing Webmaster Tools AI Performance (2026-02-10 — citations, and **grounding queries**: *"the key phrases the AI used when retrieving content"*).

**Cannot:**
- **Set any custom HTTP header.** No CSP, no `Link:` preload, no 103 Early Hints, no `Vary: Accept`, no bot-specific responses. GitHub staff: *"This is not an area that is being prioritized"*; 2026-dated user comments (2026-09-05 and 2026-09-13) confirm it is still unresolved.
- Do dynamic rendering or serve crawler-specific representations. Given §5, this costs almost nothing.
- **See server logs** — so AI-crawler hits are unmeasurable. GSC and BWT report impressions and grounding queries, never raw fetches.

## Hard Constraints

1. **Every word of meaningful content must be in the prerendered HTML, as real DOM text.** Not injected, not canvas-drawn.
2. **Keep the HTML document under 2MB**, with `<title>`, meta, canonical and structured data at the very top.
3. **Never let the canvas be the only source of any content, heading, link, or LCP candidate.**
4. **Guarantee a DOM LCP candidate** — a text block or `<img>` that paints early and independently of WebGL init — or the site will have no LCP at all.
5. **Budget against INP.** Instrument LoAF at the 50 ms threshold.
6. **Prefer CSS `animation-timeline` over JS scroll handlers**, with a fallback, since it is not Baseline.
7. **Run one `requestAnimationFrame` loop.** Two causes a one-frame scroll desync.
8. **Honour `prefers-reduced-motion: reduce`.** EN 301 549 V4.1.1 (2026-09-02) moves the EU baseline to WCAG 2.2, though v3.2.1 / WCAG 2.1 AA still governs until cited in the OJEU.
9. **Do not ship `llms.txt` expecting retrieval benefit** — and if shipped, verify it returns `text/plain`.
10. **Do not invest in schema.org for AI citation.** Keep JSON-LD only for classical rich results.
11. **Give every meaningful state its own real, prerendered URL.** Fragment URLs are unreliable, and the WRS clears storage between requests.
12. **Do not depend on WebGPU, HTML-in-Canvas, r3f v10, OGL, Theatre.js, or r3f-scroll-rig.**
13. **Design around the absence of custom headers** — inline everything.

## Open Questions

1. The numeric CWV thresholds cannot be sourced to 2026.
2. **No published measurement compares DOM+WebGL against full-canvas** for indexability or CWV. The A/B in §1 is lab data on two sites — directionally consistent with the specs, not a study.
3. **Whether GPTBot / ClaudeBot / PerplexityBot execute JavaScript has not been re-measured in 2026.** The canonical evidence (Vercel/MERJ, 500M+ fetches, zero JS execution) is dated 2024-12-17 and fails the date rule. Vendor docs are *silent*, not negative. Applebot does render and says so (2026-09-04); ChatGPT-User reportedly extracts text only (single-site log study, 2026-03-20). **This is the most load-bearing assumption in the GEO section and it rests on out-of-date evidence.**
4. *"Canvas content is not indexed"* cannot be cited to 2026 — Google states it only on a page dated 2025-12-10. The mechanism is sound; the citation is not available.
5. `OffscreenCanvas` + Web Workers has **no 2026-dated vendor source** and no quantified gain, despite being the obvious way to move WebGL off the main thread.
6. **No 2026 performance budgets exist** — no main-thread task budget, no JS bundle budget, no frame budget. Only LoAF's 50 ms and Googlebot's 2MB are 2026-dated numbers.
7. **Field CWV will be untestable for this cohort.** Neither award site measured has CrUX data; award sites are mostly low-traffic and never reach the reporting threshold. Expect the same, and rely on lab measurement plus own RUM.
8. Bingbot's JS rendering status in 2026 is undocumented anywhere.
