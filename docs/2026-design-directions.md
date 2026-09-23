# 2026 Scroll-Driven Design Directions

Evidence window: 2026-01-01 through 2026-09-15. No pre-2026 design references are used.

## Executive Finding

Scroll-driven design in 2026 is moving away from isolated reveal effects. The strongest work treats scroll as one or more of the following:

- a timeline that controls state;
- a wayfinding system that preserves orientation;
- a spatial input for cameras, objects, and depth;
- a shared signal connecting DOM, typography, WebGL, and transitions.

The forward trend is **coordinated interaction systems**, not more animation per page.

## 1. Guided Scrolling

[Webflow's 2026 trend report](https://webflow.com/blog/web-design-trends-2026) separates guided scrolling from scrollytelling. Its examples use progress indicators, numbered steps, active elements, visual markers, and scroll-velocity feedback.

**Finding:** scroll is becoming navigation metadata. It communicates current position, remaining distance, direction, and pace.

## 2. Scroll as Structure — WITHDRAWN

This section rested entirely on the Exat microsite, which fails the provenance rule: the site's own footer reads "Hot Type © 2025" and the earliest Wayback capture is 2025-02-23, roughly fourteen months before the 2026 article that featured it.

**The finding that scroll is used to organize pacing, comparison and state — rather than to launch animations — currently has no qualifying 2026 evidence behind it.** It may well be true. It is not evidenced here. See § Withdrawn Evidence.

## 3. Spatial and Cinematic Control

[Figma's 2026 report](https://www.figma.com/resource-library/web-design-trends/) places interactive 3D, experimental navigation, kinetic typography, motion, and scrollytelling in the current mainstream vocabulary. Practitioner work makes the direction more specific:

- [3D Cube Gallery](https://tympanus.net/codrops/2026/05/26/building-a-scroll-driven-3d-cube-gallery-in-webflow-with-gsap/) coordinates background images, type, cube rotation, and XYZ movement.
- [3D Gallery Along a Blender Path](https://tympanus.net/codrops/2026/07/07/building-a-scroll-driven-3d-gallery-using-a-blender-camera-path-with-three-js-and-gsap/) maps scroll input to a camera moving along an authored curve.

**Finding:** the 2026 direction is not generic “3D effects.” It is authored camera movement, object choreography, depth, and focus controlled by scroll.

## 4. Hybrid DOM and WebGL

The [HAOQI.DESIGN case study](https://tympanus.net/codrops/2026/08/15/inside-haoqi-design-letting-dom-and-webgl-share-a-retro-futurist-stage/) gives DOM and WebGL distinct roles:

- DOM and CSS own typography, layout, responsive behavior, and accessibility.
- A fixed WebGL canvas mirrors DOM geometry and renders effects that CSS would struggle to express.
- A shared frame loop keeps scroll state synchronized across both layers.

**Finding:** hybrid composition is replacing the choice between a conventional DOM page and a fully rendered WebGL world.

## 5. Typography as the Interface — WITHDRAWN

This section also rested entirely on the Exat microsite, and falls with it.

**The finding that kinetic and variable typography are moving from hero decoration into navigable, explanatory systems has no qualifying 2026 evidence behind it.** Note that `2026-cjk-typography.md` reaches a compatible but much narrower conclusion for CJK specifically — there, the production field is verifiably empty. See § Withdrawn Evidence.

## 6. Transition Systems

Current 2026 work uses transitions as a visual language:

- [SVG Mask Transitions](https://tympanus.net/codrops/2026/03/11/svg-mask-transitions-on-scroll-with-gsap-and-scrolltrigger/) uses grid and blind geometry to reveal fullscreen images.
- [Seamless 3D Transitions](https://tympanus.net/codrops/2026/03/18/building-seamless-3d-transitions-with-webflow-gsap-and-three-js/) keeps a persistent Three.js scene across page changes.
- HAOQI.DESIGN repeats a dot-matrix rule across card hovers, loading, route changes, and the mobile menu.

**Finding:** the trend is a repeatable transition grammar shared across states, not a different effect for every section.

## 7. Velocity as an Input

In 2026 examples, velocity is distinct from position:

- [Scroll-Reactive 3D Gallery](https://tympanus.net/codrops/2026/03/09/building-a-scroll-reactive-3d-gallery-with-three-js-velocity-and-mood-based-backgrounds/) changes motion and atmosphere in response to scrolling.
- HAOQI.DESIGN derives a shader curl from distance travelled per frame, using fast attack and slower release to suppress trackpad noise.
- Webflow's guided-scrolling examples include a speedometer driven by scroll velocity.

**Finding:** interfaces increasingly respond to how the visitor scrolls, not only where they are.

## 8. Adaptation Instead of Replication

One qualifying 2026 case study avoids copying desktop behavior onto smaller or motion-sensitive contexts:

- HAOQI.DESIGN skips its image-development transition under `prefers-reduced-motion` and keeps DOM content independent of WebGL effects.

(A second example, Exat, was withdrawn on provenance — see § Withdrawn Evidence.)

**Finding, now resting on a single case:** some high-end work treats mobile, reduced motion, and rendering cost as separate experience modes. `2026-generative-and-geometric-work.md` measures the opposite across a wider sample — zero of eleven pieces document a `prefers-reduced-motion` path — so HAOQI.DESIGN should be read as the exception, not the trend.

## Forward Trajectory

| Moving away from | Moving toward |
| --- | --- |
| isolated entrance animations | coordinated state systems |
| scroll as page displacement | scroll as time, direction, and pace |
| decorative 3D objects | authored cameras and spatial choreography |
| effect-by-effect styling | reusable motion and transition grammars |
| DOM or WebGL | synchronized DOM plus WebGL |
| desktop effects compressed for mobile | context-specific adaptation |

## Withdrawn Evidence

Removed on 2026-09-15 when the provenance rule in `RESEARCH-METHOD.md` was applied retroactively. Recorded here so it is not re-added.

| Work | Why withdrawn |
| --- | --- |
| **Exat typography microsite** (exat.hottype.co, RISE2 Studio for Hot Type) | Site footer reads "Hot Type © 2025"; earliest Wayback capture 2025-02-23 — roughly fourteen months before the 2026-04-10 article featuring it. The article date is real; the subject's is not. |

This is the exact contamination pattern the rule was written to catch: a 2026-dated feature republishing older work. Two of this corpus's most heavily-cited flagship examples failed it.
