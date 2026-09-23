# 2026 Scroll Interaction Taxonomy

Evidence window: 2026-01-01 through 2026-09-15.

## Classification Model

Describe an observed experience with five fields:

```text
input + progress mapping + stage + visual action + narrative function
```

Example:

```text
vertical wheel/touch input
+ smoothed continuous progress
+ pinned stage
+ camera movement along a 3D curve
+ spatial portfolio traversal
```

## Input

| Term | Use when |
| --- | --- |
| **Scroll position** | Absolute progress determines the state. |
| **Scroll delta** | Each wheel or touch change advances a custom coordinate. |
| **Scroll velocity** | Speed or direction changes the response independently of position. |
| **View progress** | An element's passage through the viewport determines progress. |
| **Combined input** | Scroll, pointer, or proximity share control of the experience. |

## Progress Mapping

| Term | Use when |
| --- | --- |
| **Triggered** | Crossing a threshold starts a time-based animation. |
| **Scroll-linked / scroll-driven** | Scroll position supplies animation progress. |
| **Scrubbed** | Scroll directly controls a playhead, with optional catch-up smoothing. |
| **Inertial** | A target follows input while the rendered state interpolates toward it. |
| **Stepped** | Progress selects discrete chapters or panels. |
| **Snapped** | Motion settles at defined states after input stops. |
| **Velocity-responsive** | The result depends on speed or direction rather than only progress. |

Mozilla's [Interop 2026 announcement](https://hacks.mozilla.org/2026/02/launching-interop-2026/) uses **scroll-driven animations** for animations whose progress follows scroll position. The initiative treats them as a native platform feature replacing many main-thread JavaScript solutions.

## Stage

| Term | Observable structure |
| --- | --- |
| **Document flow** | Content moves normally through a vertical page. |
| **Pinned stage** | The viewport remains visually fixed while internal state advances. |
| **Pinned horizontal track** | Vertical distance maps to horizontal translation inside a fixed viewport. |
| **Fixed canvas with moving DOM** | DOM scrolls normally while a persistent canvas mirrors or augments it. |
| **Persistent 3D scene** | One rendered scene survives across sections or page transitions. |
| **Infinite gallery** | A finite sequence wraps without a visible terminal edge. |

## Visual Action

### Typography

- weight or width-axis morphing;
- proximity-responsive glyph field;
- character decoding or scrambling;
- split-text reveal;
- reversible panel replacement;
- 3D type rotation.

### Image and Layout

- layered parallax;
- mask or clip reveal;
- background crossfade;
- horizontal track translation;
- grid expansion or reconfiguration;
- shared-element or FLIP transition.

### Spatial and 3D

- object rotation or XYZ translation;
- camera orbit, dolly, or authored camera path;
- proximity scaling or focus gating;
- geometry morphing;
- refraction or material transition;
- shader distortion;
- particle dissolve or disintegration.

## Narrative Function

| Term | Meaning |
| --- | --- |
| **Guided scrolling** | Progress cues preserve orientation and encourage continuation. |
| **Scrollytelling** | Scroll advances meaningful narrative or explanatory states. |
| **Editorial pacing** | Motion controls reading rhythm without enforcing a story. |
| **Spatial traversal** | The visitor moves through an authored 2D or 3D environment. |
| **Product transformation** | Scroll reveals construction, parts, states, or features. |
| **Atmospheric response** | Input changes mood, depth, lighting, or texture. |

## Precision Rules

- Use **vertical-to-horizontal translation** when vertical input moves an x-axis track.
- Use **parallax** only when layers move at different rates.
- Replace **3D effect** with the actual action: camera path, model rotation, shader distortion, geometry morph, or material transition.
- Use **scrollytelling** only when scroll advances semantic content.
- **Progressive disclosure** describes when information appears; it does not name the animation mechanism.
- Name compound work compositionally: `scroll-driven + stage/medium + visual action`.

## Names Used by 2026 Practitioners

- Smooth Horizontal Parallax Gallery
- Sticky Grid Scroll
- Scroll-Reactive 3D Gallery
- SVG Mask Transitions on Scroll
- Scroll-Driven Panels
- Scroll-Driven 3D Cube Gallery
- Scroll-Driven 3D Gallery Along a Blender Camera Path
- DOM and WebGL Scroll Sync

The repeated naming pattern confirms that there is no single agreed term for the complete experience.
