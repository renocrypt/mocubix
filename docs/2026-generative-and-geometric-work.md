# 2026 Generative and Geometric Interactive Work

Evidence window: 2026-01-01 through 2026-09-15. Material that is generative, procedural, geometric, or data-driven — deliberately excluding photo galleries and image carousels, which `2026-observed-case-studies.md` already covers.

One Codrops entry, by exception. Every other entry is drawn from elsewhere; see `RESEARCH-METHOD.md` for the source map and the date-verification rules this pass established.

## Executive Finding

Two structural gaps define this field in 2026, and both are open territory.

**First: shipped work is described, never explained.** The split is strict — shipped commercial work (Evian, Lacoste, Cerebrium, San Rita) gets described by curators and never gets a published breakdown; work *with* published internals (False Earth, Still, WebRF, SDF Editor) is independent or tooling, not a commercial site. **No 2026 shipped brand site published a technical breakdown of a scroll-driven generative system.** Bridging that gap is unsolved.

**Second: the field has no reduced-motion story at all.** Of eleven findings, **zero** document a `prefers-reduced-motion` path. Where degradation exists it is performance-triggered, not preference-triggered.

## 1. Findings

### Evian — Celebrating 200
[celebrating200.evian.com](https://celebrating200.evian.com) · featured 2026-06-12; the site marks Evian's 1826–2026 bicentennial · shipped brand site

A persistent alpine valley, not a page. Rain spawns on the peaks and is moved by a **shallow-water simulation that advects along the heightmap's pressure gradient**, cutting runoff channels down the slopes — the terrain's own geometry authors the water's path rather than an animator. Wind is a **single world-space texture** that grass, trees, particles, the water stream and the character's coat all sample, which is why everything leans the same way on the same frame: one field, many consumers. ~20,000 particles collide against a **baked signed distance field rather than mesh geometry**, making collision a texture lookup instead of a traversal. Expensive lighting passes (SSGI, GTAO, fog) render at half resolution with blue-noise-jittered samples, average against a reprojected history buffer, then bilaterally upsample so edges do not bleed across silhouettes. **Render resolution auto-scales to hold framerate and recovers slowly as load eases.** No documented reduced-motion or mobile path.

`pointer/camera exploration + continuous real-time simulation + persistent 3D scene + SDF-collided particle and shallow-water advection + atmospheric response`

### WebRF — Longley-Rice propagation in compute shaders
[romanliutikov.com/projects/webrf](https://romanliutikov.com/projects/webrf) · 2026-03-04 · shipped tool

The purest data-as-form piece found. Terrain elevation plus a transmitter position are the only inputs; the visible form is entirely derived. A **two-pass radial sweep**: pass one runs one thread per ray fanning outward to build terrain profiles; pass two runs one thread per ray-step *pair*, executing the full ITM algorithm against every prefix of each profile simultaneously. That restructuring yields roughly **500× the parallelism of a naive sequential port** — which is what makes an atmospheric propagation model interactive in a browser. ~1,200 lines of WGSL. Diffraction and terrain shadowing become visible shape.

`pointer placement + direct-manipulation recompute + fixed canvas + compute-derived coverage field + data-as-form`

### WebGPU SDF Editor
[renderqueue.dev/sdf-editor](https://renderqueue.dev/sdf-editor) · 2026-01-08 · shipped tool

Notable because it is **explicitly not raymarched**. Six primitives in a hierarchical scene graph with union/subtraction/intersection and a configurable blend radius. Rather than marching rays per pixel, the pipeline **extracts an actual surface on the GPU each edit**: Marching Cubes while editing, Surface Nets in view mode. The seven-stage pipeline — primitive buffer update, space partitioning, **dirty-mask detection**, octree splitting, surface extraction, shadow-map AO, TAA — turns on that dirty mask: an edit re-meshes only the affected region, which is what keeps blending interactive.

`parameter and gizmo input + direct manipulation + persistent 3D scene + SDF boolean blending with incremental re-meshing + tool-state transformation`

### ChartGPU
[chartgpu.github.io/ChartGPU](https://chartgpu.github.io/ChartGPU/examples) · 2026-04-21 · shipped library

Data-as-form at the infrastructure layer. The move is putting the *reduction* step on the GPU: **LTTB downsampling runs as a compute shader**, so data is thinned on the device rather than thinned on the CPU and uploaded. Each series renders through a single instanced draw call; hit-testing for tooltips is GPU-accelerated too. 1M points pan and zoom at 60fps; a benchmark holds ~72fps at 35M points. Relevant less as a visual reference than as proof the compute-shader-first pattern has reached shipped, installable tooling.

`pan/zoom input + continuous range mapping + fixed canvas + GPU-downsampled series rendering with GPU hit-testing + data-as-form`

### False Earth
[false-earth.mingjyunhung.com](https://false-earth.mingjyunhung.com) · featured 2026-03-28; author's technical write-up 2026-04-21 · independent art piece

The most complete procedural-geometry pipeline found with published internals. Over **1M grass blades**, each a real blade with controllable shape, colour and movement rather than a billboard field. Compute shaders own positioning, **Voronoi-based clumping**, wind, terrain sampling and character interaction. Placement uses **PCG hashing with CPU grid indexing** for a stable, tile-free pattern — the specific fix for the repeating-lattice artefact that kills most large grass fields. Terrain is FBM heightmaps with normals sampled in compute; roses are vertex-animation-texture driven with their own LOD.

The author's stated reason for moving off WebGL is the useful part: GPGPU in WebGL meant encoding state as pixels and juggling FBO read/write, whereas **storage buffers let structured data be written on the GPU and read from any shader**. That is the actual 2026 platform shift — not "WebGPU is faster."

Degradation is documented: **LOD reduces blade segment counts by distance, and a PerformanceMonitor drives adaptive DPR.** No reduced-motion path.

`character movement + continuous simulation + persistent 3D scene + compute-driven grass/terrain deformation and VAT bloom + spatial traversal`

### Atelier San Rita
[sanrita.ca](https://sanrita.ca) · 2026-02-26 · shipped studio site

A portfolio whose navigation *is* the geometry: projects are waypoints in a topographic landscape rather than cards in a grid. The production method transfers. Terrain volume was generated by applying **a high-detail depth texture to a flat mesh in Blender**; the team then kept two meshes — an ultra-dense one used only to bake normal and displacement maps in Substance Painter, and a drastically decimated one actually shipped. **That bake-down took the payload from ~60MB to 3–4MB as Draco-compressed glTF.** Next.js + React Three Fiber with custom fragment shader work.

Directly relevant to a GitHub Pages payload budget.

`pointer navigation + inertial + persistent 3D scene + terrain traversal with waypoint focus gating + spatial traversal`

### Lacoste Members Experience
[membersexperience-create.lacoste.com](https://membersexperience-create.lacoste.com/gb/en/) · 2026-03-15 · shipped brand product · Merci-Michel

Generative-as-manufacturing, not generative-as-decoration. Members draw, sticker and pattern a polo in real time. Two mechanisms matter. **Three separate UV maps on one garment**: one for standard dynamic rendering, one tiled for deep zoom, and one clean set whose only job is export to actual production — the customiser's output is a manufacturing file. And **metadata encoded as colour data directly in the mesh vertices**, marking join zones, paintable regions and rollover areas, so the interaction system knows which geometry is live without a parallel data structure.

Mobile is explicitly *not* a squeezed desktop build: a "completely rethought interface, leaner but still fun," described as parallel projects sharing a pipeline. Adaptation over replication, applied to a commerce flow.

`pointer draw input + direct manipulation + persistent 3D scene + vertex-gated material and texture compositing + product transformation`

### Patina Preview
[patina-preview.vibe-coded.com](https://patina-preview.vibe-coded.com) · 2026-04-19 · demo

The cleanest example of a **generative material system**. Weathering is "a node graph, not a baked texture stack": Three.js TSL on WebGPU composing **cavity masks, noise fields and roughness modulation as shader nodes**. Oxidation pools into surface cavities because cavity occlusion drives its distribution; highlights travel from mirror to matte via roughness; colour migrates copper/bronze → verdigris. Because it is derived rather than sampled, moving a slider **re-derives the whole material live**.

The inversion matters: material becomes a parameter space traversable at runtime, rather than an asset you ship.

`slider parameters + direct parameter mapping + orbiting fixed canvas + procedural PBR re-derivation + material exploration`

### Cerebrium
[cerebrium.ai](https://www.cerebrium.ai) · Awwwards SOTD + Developer Award 2026-09-10 · shipped product site

Evidence that geometric and data-driven form does explanatory work on real B2B product sites. Cerebrium sells serverless AI infrastructure; the brief was making cold starts, autoscaling and global deployment legible to developers. The build answers with an **interactive WebGL globe carrying force-field dynamics** (deployment regions as a field, not pins on a map) and animated infographics rather than static diagrams. GSAP + Three.js + Cinema 4D on a two-colour palette.

Caveat: this description comes from the Awwwards listing and credits, not a published breakdown. Treat the force-field implementation as unverified.

`scroll position + scroll-linked + fixed canvas with moving DOM + force-field globe and animated infographics + product transformation`

### Lona Lih
[lonalih.com](https://lonalih.com) · 2026-05-27 (Hoverstat.es) · shipped portfolio

Included deliberately as the counterweight: **generative and typographic-as-form with no WebGL at all.** Content stacks like a cairn, built from **randomly generated stone shapes** and an **SVG text distortion effect** giving the type textural depth.

It matters twice over. It demonstrates that procedural geometry and type-as-material are achievable in SVG/DOM — which survives reduced motion, low-power devices and no-GPU contexts *by construction*, and costs nothing against a static-hosting budget. And it corrects the WebGL monoculture that both the existing corpus and every gallery checked will otherwise push this project toward.

`scroll position + scroll-linked + document flow + randomized SVG geometry and SVG text distortion + editorial pacing`

### Still — generative garden in WebGPU
[Codrops](https://tympanus.net/codrops/2026/09/09/still-from-akira-to-ink-wash-building-a-generative-garden-in-webgpu/) · 2026-09-09 · demo with published internals · *(the one Codrops entry)*

Kept past the cap because its progress model is unlike anything in the existing corpus: **progress is not scroll, it is seeded autonomous time.** Each plant instance carries a seeded age and duration and moves through a four-stage lifecycle (Delay → Grow → Keep → Die); a **single 0→1 growth value orchestrates every component** — the lifecycle decides *when* each part acts, its local progress decides *how* that part appears. Stems are Catmull-Rom curves swept into tubes; flowers open via VAT with per-petal procedural shedding. Placement uses a **density field of four body-contact anchors with warped elliptical falloff plus deliberate bare patches** to defeat uniformity. Tendrils are dual-path: **MeshBVH geometric queries for wrap curves, Dijkstra pathfinding over a surface graph for ground routes.**

`seeded autonomous time + per-instance local progress + fixed canvas + procedural growth, bloom and shed + atmospheric response`

**Also verified 2026, mechanism thinner:** Flight Path (2026-04-22, OpenFlights data as 30k GPU-instanced planes on parabolic curves, UTC scrub); Sedon (2026-06-09, Gregg Tavares — node-graph procedural forest from ~9k gzipped data, runtime LOD tessellation); 3D Life Sim (2026-08-01, particle-life compute with live audio and MIDI); Crystal Words (2026-05-09, typed text → six-fold ice lattice).

## 2. WebGPU Is the Material Question, Not a Rendering Detail

The recurring 2026 justification across these findings is **storage buffers replacing FBO pixel-packing for GPGPU state.** That is what makes 1M-blade fields, SDF particle collision and compute-shader downsampling tractable at all. The existing corpus does not mention WebGPU once.

**Counterweight, from `2026-discoverability-and-performance.md` § 9: WebGPU is not a safe 2026 baseline** — Firefox is partial with Linux and Android still in development, and Chrome Linux is Intel Gen12+ only. Both facts are true at once. The frontier material work is happening in WebGPU; deploying it as a floor is not yet defensible. Progressive enhancement over a WebGL path is the only honest posture.

## 3. Cross-Case Findings

1. **Compute-first is the 2026 pattern.** Simulation, placement, collision, and even data reduction moved onto the GPU as structured buffers rather than encoded textures.
2. **One field, many consumers.** Evian's single wind texture and Still's single growth value are the same idea: coherence comes from shared state, not from synchronised separate animations.
3. **Deriving beats sampling.** Patina's material node graph, WebRF's propagation field, and Lona Lih's stone shapes are all computed rather than authored — which is also what makes them cheap to ship.
4. **Reduced motion is an empty field.** Zero of eleven document a preference-triggered path; Evian and False Earth degrade on *performance* signals only. The charter already requires reduced-motion verification, so **this project's existing discipline is a genuine differentiator here** — nothing new needs inventing.
5. **The explanation gap is the opportunity.** Shipped work is never explained, and explanatory content is exactly what earns retrieval and citation per `2026-discoverability-and-performance.md` § 6.
