# 2026 CJK Web Typography

Evidence window: 2026-01-01 through 2026-09-15. Zero Codrops entries. Dates verified by fetching each source.

## Executive Finding

**Kinetic and scroll-driven CJK typography is an empty field in 2026.** Not thin — empty. No site or case study exists where Chinese, Japanese, or Korean type is demonstrably the animated material, with a verifiable date and a documented mechanism.

What did happen in 2026 happened entirely in **font engineering and standards documentation**. The material exists; the production work does not.

## 1. The Asymmetry That Defines the Field

[Interop 2026](https://github.com/web-platform-tests/interop/blob/main/2026/README.md) (2026-02-12) selected 20 focus areas and 4 investigation areas from 150+ proposals. Verified against both the Igalia announcement and the canonical WPT repo README:

**Nothing on `writing-mode`, ruby, `line-break`, `word-break`, `text-autospace`, `text-spacing-trim`, or fonts.**

Meanwhile scroll-driven animations *are* a focus area.

**Finding:** the platform is funding cross-vendor convergence on the *motion* half of "kinetic CJK typography" and nothing at all on the *CJK typography* half.

## 2. The Material Exists, and It Is Open Source

Every verifiable 2026 CJK variable font with real continuous axes came from open-source or individual designers — **not one from a commercial foundry.**

### 文渊字体 (WenYuan Fonts) v1.000 / v1.010

[Releases](https://github.com/takushun-wu/WenYuanFonts/releases) — v1.000 2026-07-02, v1.010 2026-08-21. OFL, derived from Source Han, GB 18030-2022 level-2.

The most substantive shipped CJK variable work of 2026. v1.000 adds a width axis `wdth` (66.67–100) and a **separate height axis `HGHT` (66.67–100)**, so glyphs compress independently on each dimension rather than scaling — 長體/平體 as continuous space instead of separate cuts. v0.904 added an `ital` axis (range [0,1]) swapping in true Latin italic glyphs inside the Han font, and cut OTF variable file size ~25%. For vertical typesetting, v1.000 adds an **`ss11` stylistic set that swaps the Latin width/height parameters when set vertically**, so Latin embedded in 縦書き/直排 does not render absurdly elongated.

### 嗷呜等高体 (EqHiSans) v1.2.0

[Releases](https://github.com/howlingFounts/EqHiSans/releases) — v1.0 2026-07-03 through v1.2.0 2026-08-17. OFL 1.1.

Solves the mixed-script optical problem **in the font rather than in CSS**: Han characters and Latin capitals/digits are drawn to the *same* height, so a bilingual line needs no per-language `font-size` compensation and no baseline shim. `wght` + `wdth` dual axis, covering SC/TC/Japanese/Latin/Cyrillic/Greek, derived from Roboto Flex crossed with WenYuan Sans.

Its web-delivery strategy is explicit: a separate **Lite** variable build restricted to GB/T 2312-80 plus the Table of General Standard Chinese Characters, shipped specifically to cut file size.

### Adobe ネオクロ (announced, unreleased)

[Adobe Fonts Japan](https://blog.adobe.com/jp/publish/2026/04/10/cc-design-adobefonts-2604) (2026-04-10). In development, no release date, no web availability confirmed.

The mechanism is the interesting part: the width axis is **script-differential within a single font** — kanji hold their square proportion while kana and Latin compress to roughly half-width at the axis extreme. A second dedicated axis controls kana position within the em box.

**This design space has no Latin analogue.** It varies the relationship *between* the scripts sharing a line, rather than varying letterforms uniformly.

### The commercial counter-signal

justfont shipped [金萱 v4.0 / 金萱那提 v3.0](https://blog.justfont.com/2026/05/jinxuan-jinxuanlatte-rise/) (2026-05-29) — flagship Traditional Chinese families rebuilt for mixed-script use, and **deliberately not variable**. Nine discrete weights, no axis. Glyph count ~14,500 → ~15,200. Latin and numerals redrawn at scale: curve refinement, counter spacing, optical compensation, diacritic proportions. Sharpest mechanism: when Latin letters carry Bopomofo-style tone marks (Hakka romanization), the font automatically repositions the tone mark to upper-right per Taiwan MOE convention via substitution.

Morisawa's only variable font (DriveFlux) is 2025-02. Founder Type's 2026 releases are static. Hanyi: nothing dated 2026.

**Finding:** commercial CJK foundries in 2026 are investing in charset coverage and mixed-script correctness, not in variable axes.

## 3. Standards Are Moving; CSS Is Not Connected to Them

**[klreq](https://www.w3.org/TR/klreq/)** — Requirements for Hangul Text Layout and Typography (2026-03-21, Group Note Draft), restructured to the W3C Language Enablement Framework, published bilingually EN/KO. Covers character-unit and word-unit line breaking; prohibited line-start and line-end characters; **line adjustment when proportional-width Latin sits inside Hangul composition**, since Hangul composes evenly without inter-character spaces and Latin does not; standardized letter-face position in the character frame so font swaps do not shift glyphs.

**[clreq](https://www.w3.org/TR/clreq/)** — 中文排版需求 (2026-09-01, Group Note Draft), editors 薛富侨 and Richard Ishida. The operative bilingual rule is quantified: spacing between Han characters and Western letters or Arabic numerals should be **no more than one quarter of a Han character's width** (「不多于四分之一个汉字宽」).

**The notable absence:** clreq never references `text-autospace` or `text-spacing-trim` — the CSS properties that implement its own rule. As of September 2026 the requirements layer and the implementation layer are not cross-linked.

**[Safari 27 beta](https://webkit.org/blog/17967/news-from-wwdc26-webkit-in-safari-27-beta/)** (2026-06-08) is the densest CJK platform movement of the year. Adds the `insert` keyword to `text-autospace`; fixes `text-autospace` on supplementary-plane characters. Three line-layout fixes reveal how unsettled CJK breaking still was in a shipping engine: `word-break: break-all` was letting **CJK closing punctuation start a line** (a kinsoku violation), `word-break: keep-all` was wrongly *suppressing* break opportunities at CJK punctuation, and `glyph-orientation-vertical: auto` now consults UTR#50 for correct vertical rotation. Also fixes underlines splitting when a ruby base is stretched by long ruby text.

## 4. Negative Evidence

What was searched for and not found:

- **Awards.** The full Awwwards Typography Honors list for 2026 contains exactly **one** CJK-language site — 日暮里ゼミナール (studio Lamm, Tokyo; Awwwards Typography Honors Jan 2026, CSSDA Website of the Day 2026-01-05, judge score 7.96) — with no published mechanism. No Chinese, Taiwanese, or Korean studio entry surfaced in any 2026 typography category.
- **たてよこWebアワード** — the one award in the world dedicated to vertical CJK web typography, run by the 縦書きWeb普及委員会 with W3C liaison — **has no 2026 edition. The last editions were 2016 and 2017.** The dedicated institution for this exact subject has been dormant for eight years.
- **Korean.** No 2026 kinetic typography case study. No confirmed 2026 Hangul variable font *release* — Sandoll and Yoon Design are reported as "advancing variable font releases" with no dated product; Pretendard is continuous maintenance, not a 2026 release event.
- **Chinese.** No 2026 case study of scroll-driven Chinese type on a shipped site. 2026 Chinese-language material on the topic is trend commentary and technique explainers, not documented production work.
- **Platform priority.** No CJK or i18n text feature appears in Interop 2026, the Baseline 2026 feature list, or the May 2026 Baseline digest (whose only typographic entry is `text-decoration-skip-ink: all`).

Two frequently-cited works were checked and **do not qualify** — see `RESEARCH-METHOD.md` § Failure 2. The nearest genuine near-miss is **IZANAMI** (baqemono.inc, Awwwards SOTD 2026-07-18, WebGL + GSAP, tagged Typography / Scrolling / Storytelling); its mechanism could not be confirmed, so no classification is recorded.

## 5. Constraint Notes

Documented obstacles to animating CJK type on the web, from 2026 sources only.

1. **Subsetting defeats caching.** Per the [#webfont_study session](https://web-study.connpass.com/event/395240/) (2026-06-15, Tokyo, framed as 「CJKに生きる我々のフォント戦略」): Latin scripts use custom fonts effortlessly while CJK carries structural constraints — **even tuned subsets remain heavy on initial load, and per-page subsetting prevents cache reuse.** That second clause kills the dominant Japanese/Chinese production technique: every page pays again because no two pages request the same subset.
2. **The file-size floor is unresolved.** The W3C IFT Candidate Recommendation Draft states plainly that *"even using WOFF 2, fonts for CJK languages can be too large to be practical."* w3c/clreq issue #403 records that CJK is *"currently unable to use Webfonts due to the very large file sizes,"* with the fallback being OS-preinstalled fonts — which removes typeface choice entirely. Still open, labeled spec-ready against Blink, WebKit and Gecko.
3. **The fix is not shipped.** Incremental Font Transfer — whose primary motivating use case *is* CJK — remains at CR Draft (2025-11-18, **no 2026 publication**) and Intent-to-Prototype in Chrome, with no announced milestones. Nothing in 2026 changed the delivery ceiling.
4. **CJK line-breaking was still broken in a shipping engine mid-2026.** See the Safari 27 beta fixes above. **Any per-character animation that re-flows text risks tripping kinsoku bugs that were live in a major engine in 2026.**
5. **Vertical text is a font-plus-engine contract, not a CSS property.** WenYuan had to add `ss11` because `writing-mode` alone produced unacceptably elongated Latin; Safari separately had to fix `glyph-orientation-vertical: auto` against UTR#50.
6. **Variable CJK builds carry a platform-support tax.** Per the WenYuan repo: OTF (CFF2) variable builds require Windows patch KB5032278 to render correctly, and large TTF variable fonts may fail to expose named instances in the Windows font viewer, falling back to a single regular weight.
7. **`text-autospace` is usable but not uniformly.** MDN (2026-04-20) records it as Baseline "newly available" since November 2025, while flagging varying support — `punctuation` and `replace` are the ragged edge, not the `normal` / `ideograph-alpha` / `ideograph-numeric` core.

## 6. Reading for This Project

The constraints above are real, and they collide with the discoverability requirement in `2026-discoverability-and-performance.md`: font payload lands directly on LCP.

The resolution is the project's own framing rather than a technical workaround. **CJK is exhibited material, not interface language** — so what is needed is a small, fixed, deliberately chosen set of characters, not a large arbitrary glyph set. A fixed exhibition set is subset once and cached across the whole site, which retires constraint 1. Animated material that is composed rather than re-flowed sidesteps constraint 4. All indexable content rides the English wall label on ordinary Latin faces.

Further: clreq's quantified spacing rule, klreq's Hangul composition and line-adjustment rules, and the font-plus-engine contract for vertical setting are **typographic requirements that can become interaction mechanics** — an interaction system derived from the script's own layout logic rather than a generic scroll effect applied to CJK glyphs.

Recorded as this project's reading of the evidence, not as a claim any source makes.

**Risk posture:** this territory differs from the others in kind. The evidence says Mocubix would be **building in open territory, not following existing practice** — no validated path, and no one has cleared the mines.
