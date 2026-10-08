# Signal mission page: build prompt

Use the sentinel-design-system, editorial-scroll-story and liquid-glass-workbench skills. Build one self-contained `index.html`, no libraries.

## Experience

- A fixed full-viewport canvas behind everything: a deep-navy starfield with a large planet limb on the right whose atmosphere rim glows ice blue (#8ecbff). It drifts with the smoothed scroll progress.
- Four chapters: hero, two story chapters (the second with its copy on the right), and a workbench.

## Layout

- Hero: eyebrow "Chapter 00 — Deep space relay", H1 with the last word in the accent, a lede, a "Scroll to fly" cue with an animated hairline, three numbered chips along the bottom, and a huge outlined wordmark behind.
- Story chapters: eyebrow, H2 with an accent phrase, one paragraph, a spec list (label left in small caps, mono value right), buttons or a source line.
- Workbench: glass nav on the left (search, grouped tools), one glass tool on stage with "01 · Input" and "02 · Output" columns. Two tools that really run in the browser: SHA-256 via Web Crypto, and text readings (bytes, unique symbols, Shannon entropy) with a verdict.

## Motion

- Native scroll drives a fractional chapter value; the canvas follows a damped copy of it.
- Heading words rise from masks one by one; eyebrow, body, spec and actions fade up in sequence after.
- Rail dashes grow and reveal their label for the current chapter. The scrim flips to the copy's side.
- Reduced motion: everything visible, no damping, no animation.

## Interaction and quality

- Skip link, semantic landmarks, headings keep an `aria-label` with the full text after word splitting.
- Responsive at 1440x900 and 390x844: rail hidden, copy anchored to the bottom over a vertical scrim, chips in two columns.
- No CDN, no remote fonts. Verify with screenshots of the hero, a right-side chapter and the workbench at both sizes, and an empty console.
