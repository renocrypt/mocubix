# 2026 Platform and Production Signals

Evidence window: 2026-01-01 through 2026-09-15.

## Native Scroll Timelines Are Becoming Cross-Browser Infrastructure

Mozilla's [Interop 2026 announcement](https://hacks.mozilla.org/2026/02/launching-interop-2026/) names scroll-driven animations as a focus area and describes them as a native replacement for many main-thread JavaScript solutions. The same announcement includes CSS scroll-snap reliability work.

[WebKit's Interop 2026 announcement](https://webkit.org/blog/17818/announcing-interop-2026/) reports Safari support and cross-browser convergence work.

**Signal:** scroll-linked progress is moving from framework-specific technique toward web-platform infrastructure.

## Native Progress Does Not Replace Creative Rendering

The 2026 case studies divide responsibility:

- native or smoothed document scroll supplies progress;
- GSAP coordinates multi-part timelines;
- Three.js or WebGL renders spatial scenes, shaders, and materials;
- DOM retains semantics, layout, and text.

**Signal:** the forward architecture is layered, not framework-exclusive.

## One Authoritative Frame Source

HAOQI.DESIGN originally allowed Lenis and React Three Fiber to run separate animation loops, creating a one-frame mismatch at speed. The production solution advances smooth scroll, records a shared snapshot, and lets every later consumer read the same state within one frame.

**Signal:** precise DOM/WebGL work depends on shared timing and state, not additional interpolation.

## DOM Owns Meaning; WebGL Owns Exceptional States

In HAOQI.DESIGN:

- CSS Grid determines structure and responsive layout;
- transparent DOM placeholders retain document geometry;
- WebGL mirrors those rectangles for shader-based states;
- only near-viewport meshes remain active.

**Signal:** WebGL is increasingly used as an augmentation layer rather than a replacement for the document.

## GPU Rendering Is Moving Into Gallery and Transition Work

The [Horizontal Parallax Gallery](https://tympanus.net/codrops/2026/02/19/creating-a-smooth-horizontal-parallax-gallery-from-dom-to-webgl/) explicitly compares DOM transforms with GPU-rendered shader parallax. The WebGL version targets cases with many images, continuous motion, and main-thread pressure.

**Signal:** GPU rendering is becoming a practical performance and visual-design choice for image systems, not only 3D spectacle.

## Velocity Requires Its Own Smoothing Model

HAOQI.DESIGN derives velocity from distance per frame, then uses a fast attack and slower release to prevent trackpad fluctuations from becoming visual noise.

**Signal:** velocity-responsive design needs temporal filtering distinct from ordinary scroll-position smoothing.

## Current Production Patterns

| Pattern | 2026 evidence |
| --- | --- |
| Pause off-screen motion | Exat pauses loops and interactions outside the viewport. |
| Simplify rather than shrink | Exat replaces unclear touch interactions with static or simplified modes. |
| Preserve semantic DOM | HAOQI.DESIGN keeps type, structure, and accessibility in HTML/CSS. |
| Skip non-essential motion | HAOQI.DESIGN removes its image-development transition under `prefers-reduced-motion`. |
| Cull distant rendering | HAOQI.DESIGN hides or reduces updates for off-screen meshes. |
| Share visual rules | HAOQI.DESIGN repeats dot-matrix logic across otherwise different effects. |
| Author paths externally | The Blender-path gallery separates spatial art direction from browser rendering. |

## Platform Direction

1. Native CSS increasingly handles the mapping from scroll to progress.
2. JavaScript remains relevant for orchestration, custom inputs, and 3D state.
3. DOM and WebGL increasingly share one experience while retaining different responsibilities.
4. Performance modes, touch behavior, and reduced motion are becoming explicit parts of the interaction model.
