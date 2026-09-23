# Research Method

How evidence enters this project, and the failures that made these rules necessary.

The charter requires design research dated 2026-01-01 or later. That rule is easy to state and hard to enforce, because the layer of the web that *describes* work is systematically unreliable. Three independent research passes, in three unrelated domains, each hit a different variant of the same failure.

## The provenance rule

**A date must come from the work's own source — the studio's project page, a first-party making-of, a release tag, a spec's publication date. Never from a curator, an award page, a search summary, or an aggregator.**

Where a first-party date cannot be found, the work is discarded rather than softened. Negative evidence is a finding; a dated-by-guess entry is contamination.

## Failure 1 — curator feature dates masquerade as launch dates

Showcase sites republish historical work under current feature dates. Four strong candidates were discarded on this:

| Work | Feature date | Actual date |
| --- | --- | --- |
| Igloo Inc | 2026-02-19 | **2024** — won Awwwards Site of the Year 2024 |
| BlueYard (Unseen Studio) | 2026-04-20 | **"Winter, 2021"** per Unseen's own project page |
| Cartier Watches and Wonders | 2026-05-06 | **2025** — the feature itself calls it a digital twin of the 2025 pavilion |
| Elimar / Van Gogh Experience | 2026-05-21 | Unverifiable; underlying story dates to Feb 2025 |

Also caught the same way: Penderecki's Garden (~2021), Bear 71 (2012), Find Your Way to Oz (2013) — all carrying 2026 feature dates.

## Failure 2 — search layers fabricate descriptors

An Awwwards Site of the Day was repeatedly surfaced as "Massive Japanese Typography in Motion." Fetched, it is **RPA COMUNICACIÓN by LaNegrita** — a Spanish agency site on WordPress with no Japanese typography whatsoever. The descriptor was invented by the search layer.

Separately, Hyakuyozu / Daimaru Matsuzakaya is widely cited as Japanese typographic work. The studio's own case study describes a drag-interactive layered-paper pattern generator: **the animated material is paper, not type.**

## Failure 3 — fabricated statistics circulate as fact

- *"Onely, Feb 2026, 6,000 sites, 42% of JS-rendered content never indexed"* — widely repeated; Onely's blog carries 2026 posts but no such study. Treat as fabricated.
- *"LCP tightened from 2.5s to 2.0s in the March 18, 2026 core update"* — no such post exists. The actual March 2026 Search Central posts are "Inside Googlebot," "New Location for the Google Crawlers' IP Range Files," and two Search Central Live announcements.
- Related orphans, equally unsourced: "67% lower rankings," "70% of sites invisible," a merged composite CWV score, an "80ms FID" threshold (FID was retired in 2024), a "Visual Stability Index," "Engagement Reliability."

## Claim labelling

Research notes distinguish three grades, and so should anything built on them:

- **MEASURED** — data with a stated method, or a first-party measurement taken here.
- **VENDOR-DOCUMENTED** — a first-party statement from the party that owns the behaviour.
- **ASSERTED** — claimed without evidence. Usable as a lead, never as a foundation.

An honest "this cannot be met at our date bar" beats a quiet citation of a stale page. The numeric Core Web Vitals thresholds are the working example: every page stating 2.5s / 200ms / 0.1 is dated 2023–2025, so the claim "unchanged in 2026" rests on negative evidence (no change announced in any 2026 CrUX release note), and is recorded that way.

## Source map

Which curation sources actually carry dated 2026 work.

| Source | 2026 work | Depth | Shipped vs demo | Use it |
| --- | --- | --- | --- | --- |
| **webgpu.com** | Yes | Very deep, near-daily; tags for particles, simulation, procedural generation, dataviz, TSL | ~50/50 | **Yes — highest value**, but every launch date must be re-verified against the studio |
| **Awwwards** | Yes | Very deep, daily SOTD with credits, stack, score breakdown | Overwhelmingly shipped | **Yes** — best shipped-work index; descriptions are marketing-level, never mechanism-level |
| **Hoverstat.es** | Yes | Thin — ~12 entries for all of 2026, with a Jan→May gap | Shipped, small studios and portfolios | **Yes, selectively** — the only source surfacing non-WebGL generative and typographic work |
| **SiteInspire** | Yes | Deep, dated daily | Shipped | Breadth only; zero mechanism detail |
| **Are.na** | Yes | Deep — 18 of 20 generative-tagged channels updated in 2026 | Mixed, uncurated | **Yes, via the v2 API only** (`api.are.na/v2/search/channels`); the web UI is JS-rendered and unfetchable, and the API returns `created_at`/`updated_at` |
| **Web Curios** | Yes | Weekly; issue URLs are literal dates | Toys, demos, oddities | Long tail only; low hit rate for product work |
| **Minimal Gallery** | Yes | Moderate | Shipped | Marginal — editorially committed to restraint, structurally unlikely to carry generative work |
| **FWA** | Yes (indirect) | **Unmeasurable** — fetches return 500 or a title-only shell; search indexing stops ~May 2026 | Shipped, experimental | In principle yes; not machine-readable |
| **Codrops** | Yes | Deep, and already over-represented | Tutorial/demo | **Cap at 1–2 entries.** Its 2026 authors publish independently — cite the work, not the tutorial |
| **Godly** | — | **Rebranded**: 301s to recent.design, no visible dates | Shipped | **No** — undated, so nothing from it can satisfy the charter |
| **Httpster** | — | Live (3,116 sites) but **exposes no dates anywhere**; `/2026/` 404s | Shipped | **No** — undated by construction |
| **Studio sites direct** | Yes | Verified dated project pages: Unseen, OddCommon, Immersive Garden, Merci-Michel, basement, Raw Materials, Abeto, Huncwot | Shipped | **Yes — and treat these as the date authority** |
