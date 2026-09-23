# 2026 Observed Scroll Case Studies

Evidence window: 2026-01-01 through 2026-09-15.

Entries link to 2026 publications **and** have been checked so that the *work being described* is itself 2026 — not merely the article describing it. Two entries failed that check on 2026-09-15 and were withdrawn; see the end of this file.

## Horizontal Parallax Gallery — February 19

[Source](https://tympanus.net/codrops/2026/02/19/creating-a-smooth-horizontal-parallax-gallery-from-dom-to-webgl/)

- Vertical wheel delta (`deltaY`) updates a horizontal target coordinate.
- The visible coordinate interpolates toward the target with `lerp`.
- Each image is wider than its clipped frame, allowing an internal counter-movement that creates parallax.
- The article compares a DOM implementation with a shader-based WebGL implementation that offloads rendering to the GPU.

**Classification:** vertical input + inertial mapping + horizontal gallery + layered parallax.

## Sticky Grid Scroll — March 2

[Source](https://tympanus.net/codrops/2026/03/02/sticky-grid-scroll-building-a-scroll-driven-animated-grid/)

- A sticky block creates a fixed visual stage.
- Scroll progress maps to an internal timeline rather than moving the scene normally.
- The sequence reveals grid columns, expands the grid through zoom and offsets, introduces text, then settles.
- The implementation treats layout and motion as one orchestrated system.

**Classification:** scroll-linked progress + pinned stage + phased grid transformation.

## Scroll-Reactive 3D Gallery — March 9

[Source](https://tympanus.net/codrops/2026/03/09/building-a-scroll-reactive-3d-gallery-with-three-js-velocity-and-mood-based-backgrounds/)

- A Three.js gallery arranges images through depth rather than a flat list.
- Scroll moves the camera through the composition.
- Velocity alters the response independently of absolute progress.
- Image palettes influence background mood.

**Classification:** scroll position and velocity + 3D gallery + camera traversal + atmospheric response.

## SVG Mask Transitions — March 11

[Source](https://tympanus.net/codrops/2026/03/11/svg-mask-transitions-on-scroll-with-gsap-and-scrolltrigger/)

- Fullscreen images are stacked as SVG layers.
- Animated mask geometry reveals each layer through grids or blinds.
- A scrubbed timeline keeps mask state synchronized with scroll.
- A segmented progress bar exposes scene state.
- Grid density changes on mobile.

**Classification:** scrubbed progress + fullscreen stage + SVG mask reveal + scene progression.

## Persistent 3D Page Transitions — March 18

[Source](https://tympanus.net/codrops/2026/03/18/building-seamless-3d-transitions-with-webflow-gsap-and-three-js/)

- A persistent Three.js scene remains active across page transitions.
- DOM navigation and WebGL imagery are synchronized rather than recreated per page.
- GSAP and Barba coordinate transition state.

**Classification:** persistent 3D scene + route transition + DOM/WebGL synchronization.

## 3D Cube Gallery — May 26

[Source](https://tympanus.net/codrops/2026/05/26/building-a-scroll-driven-3d-cube-gallery-in-webflow-with-gsap/)

- One scroll timeline coordinates fullscreen background fades and staggered text.
- A six-faced cube displays the same CMS images.
- Per-face data controls transform origin, XYZ translation, and XYZ rotation.
- Section height controls the perceived pace of the sequence.

**Classification:** scroll-driven timeline + image crossfade + text choreography + 3D object transformation.

## Gallery Along a Blender Camera Path — July 7

[Source](https://tympanus.net/codrops/2026/07/07/building-a-scroll-driven-3d-gallery-using-a-blender-camera-path-with-three-js-and-gsap/)

- Image planes are distributed along a Blender-authored closed curve.
- Wheel, touch, and pointer delta update a target path parameter.
- A smoothed proxy moves the camera toward that target.
- Nearby planes scale when they enter a camera-relative focus zone.
- The closed curve wraps continuously in both directions.

**Classification:** scroll delta + smoothed path progress + camera choreography + proximity scaling.

## HAOQI.DESIGN — August 15

[Source](https://tympanus.net/codrops/2026/08/15/inside-haoqi-design-letting-dom-and-webgl-share-a-retro-futurist-stage/)

- DOM scrolls vertically while a fixed WebGL canvas mirrors DOM image rectangles.
- One frame loop supplies the same scroll snapshot to DOM and WebGL, eliminating one-frame drift.
- CSS Grid owns layout and accessibility; WebGL supplies image development, curl, refraction, and transition effects.
- Scroll velocity drives a shader curl with fast attack and slower release.
- A dot-matrix rule recurs across hover, loading, route changes, and the mobile menu.
- `prefers-reduced-motion` skips non-essential image transitions.

**Classification:** native document flow + fixed WebGL augmentation + synchronized scroll state + velocity-responsive shader system.

## Cross-Case Findings

1. Scroll position, delta, direction, and velocity are treated as separate signals.
2. Current work composes multiple coordinated systems rather than one named effect.
3. Pinned stages remain common, but hybrid normal-flow DOM plus fixed WebGL is growing.
4. Masks, cameras, and shaders are increasingly used to explain state—not only decorate it. (The typography half of this finding was withdrawn with Exat; `2026-cjk-typography.md` finds the CJK production field empty outright.)
5. **Withdrawn.** Mobile and reduced-motion adaptation rested on Exat plus HAOQI.DESIGN. With Exat gone, one case remains — and `2026-generative-and-geometric-work.md` measures zero of eleven pieces documenting a `prefers-reduced-motion` path. The honest reading is the opposite of the original finding: **adaptation is rare, and HAOQI.DESIGN is the exception.**

## Withdrawn Evidence

Removed on 2026-09-15 under the provenance rule in `RESEARCH-METHOD.md`. Recorded so neither is re-added.

| Work | Article date | Why withdrawn |
| --- | --- | --- |
| **Exat typography microsite** (exat.hottype.co, RISE2 Studio for Hot Type) | 2026-04-10 | Site footer reads "Hot Type © 2025"; earliest Wayback capture **2025-02-23**, ~14 months before the article. |
| **MERSI** (mersi-architecture.com, FLOT NOIR) | 2026-07-27 | Earliest Wayback capture **2025-06-21**, ~13 months before the article. FLOT NOIR's own site is a placeholder with no project page, so no first-party date contradicts this. |

Both are the same pattern: a genuine 2026 article about work that predates the evidence window. The article date was real; the subject's was not.

**Residual risk, recorded rather than hidden:** HAOQI.DESIGN is retained as clean, but its date rests on circumstantial evidence — a first-person making-of by the site's own creator, a "©2026" footer, and no Wayback capture before mid-2026 — rather than an explicit first-party date declaration.
