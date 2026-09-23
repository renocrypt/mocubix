# Next

Where the work stands and what comes next. Rewrite this file whenever that changes; `DECISIONS.md` keeps the history.

## Standing (2026-09-23)

- The seven exhibits and the index are at the bar; the audit closed on 2026-09-22 (entries in `DECISIONS.md`).
- The Lexicon has 41 terms, each with its own page; 27 are full showcases. Image, Type and Colour are complete. A sweep of all 27 at 1324 and 390 wide was clean.
- Live at https://mocubix.renocrypt.com/: every page and share card answers.

## Next

1. **The 14 scroll terms still at card level.** Scroll-driven: Scroll Progress Timeline, View Progress Timeline, Pinning & Scrub, Parallax, Scroll Velocity Skew, Timeline Scope, Depth of Field. Scroll behaviour: Snap Stop, Scroll Buttons, Sticky State Query, Snapped State Query, Direction State, Infinite Loop Scroll, Overscroll Containment. Start with what Chrome now does natively: Sticky State Query and Snapped State Query (`scroll-state()` container queries) and Scroll Buttons (`::scroll-button()`). Parallax waits for material that really has layers (Redouté on Commons proved too thin and too mixed). Each showcase gets its own body of public-domain material, never one used before.
2. **The first reusable part.** The Scroll-Triggered Count odometer (pure CSS: a scroll trigger, a registered number, one wheel per digit) is the natural first candidate for `site/parts/`.

## For the owner to decide

- **Host the images here?** The pages reference 955 Wikimedia URLs, about 0.5 GB as JPEG and PNG by sampling; as AVIF alone (the site is Chrome only) at the widths actually used, perhaps 100–200 MB. It would bring the images to the same origin, cut their bytes about in half and end the dependence on Wikimedia; the cost is a repository that grows for good, and GitHub Pages fixes `max-age=600`. 242 of the 257 works are public domain or CC0; 15 are CC BY or BY-SA and keep their attribution. Visitors' regions are not a concern.
- **Geist Mono** is Next.js's default face, the most default-looking thing in the site's type.
- **The Marquee's Latin, Greek and Cyrillic greetings** are in Noto Serif Display; a curated face covering all three scripts could replace it.
