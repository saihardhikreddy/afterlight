---
name: sentinel-design-system
description: The SentinelSpread visual language (deep navy space, one ice-blue accent, Geist and Geist Mono, editorial chapters over a live scene, clear glass tools). Use when building a technical or scientific product page, a mission/space themed site, a dark tool console, or anything that should look like SentinelSpread.
---

# Sentinel Design System

Extracted from the SentinelSpread site ([reference screenshot](reference-sentinelspread-hero.png)). Runnable demo of the whole page pattern: [demo/index.html](demo/index.html). Tokens to copy: [tokens.css](tokens.css).

## Thesis

A quiet editorial voice over a live, cinematic scene. Copy sits straight on the world with no boxes; numbers are the decoration. Glass appears in exactly one place, the workbench, where the real tools are.

## Color

- Deep navy ink `#04060d` for the page, never pure black. Text `#e9eef6`, secondary `#aab4c4`, muted `#7a8598`.
- **One accent**, ice blue `#8ecbff`. It marks the second half of every heading, the active rail item, readings, focus rings and the primary button. Nothing else gets color.
- Status only: ok `#8fd6a6`, bad `#ff7a66`, always as a small dot plus words.
- Hairlines are translucent text color (`rgba(214,226,245,.09)` and `.17`), not grey.

## Type

| Role | Style |
|:--|:--|
| H1 | Geist 600, `clamp(40px, 5.8vw, 92px)`, line-height 1.02, tracking −0.03em, `text-wrap: balance` |
| H2 | Same, `clamp(30px, 3.6vw, 54px)` |
| Heading accent | `<em>` on the last phrase, not italic, in `--signal`: "Hidden in *the noise.*" |
| Eyebrow | Geist Mono 500 11px, uppercase, 0.12em, after a 6px glowing signal dot: "Chapter 02 — High-gain antenna" |
| Body | Geist 16px / 1.65 in `--text-2`, max 30rem |
| Labels, nav, rail | Geist 9.5 to 11px uppercase, 0.16 to 0.24em tracking |
| Data | Geist Mono, `font-variant-numeric: tabular-nums` |
| Wordmark | Geist 300, 13.5vw, transparent fill, 1px stroke at 12% opacity, behind the hero |

## Components

- **Top bar**: 64px, frosted gradient strip so the logo never sits on a heading. Brand is a tiny signal-colored waveform SVG plus name. Right side: an API/status pill (dot + mono label).
- **Chapter rail**: right edge, dashes that grow and reveal their label when hovered or current (`aria-current="step"`). Hidden under 960px.
- **Spec list** (`dl.spec`): uppercase label left, mono value right, hairline between rows. `spec--readings` tints values in the accent and shows the set-point in `<small>` under it. Follow with a `.source` line saying where the numbers came from.
- **Hero chips**: numbered (`01` in mono accent) one-line claims along the bottom, each a button that jumps to its chapter.
- **Buttons**: pill, 42px. In the story: solid signal fill with dark ink text for primary, ghost for secondary. In the workbench: glass buttons, see [liquid-glass-workbench](../liquid-glass-workbench/SKILL.md).
- **Readings and verdicts** in tool output: small mono tiles, then one line with a colored dot saying good or bad in words.

## Copy voice

Short declarative headlines with a turn at the end. Body explains the mechanism in plain words and ends on a concrete number. Every claim has a reading and a source.

## Pitfalls

- A second accent color. The restraint is the look.
- Panels behind story copy. Use the directional scrim and text shadow from [editorial-scroll-story](../editorial-scroll-story/SKILL.md).
- `text-shadow` on headings whose words are wrapped in `overflow: hidden` reveal masks: over a bright scene the shadow is clipped into dark boxes. Use `filter: drop-shadow()` on the heading.
- Loading Geist from Google Fonts breaks the single-file/no-network rule. Self-host the woff2 in `assets/`, or accept the system fallback stack.
- On phones a generic `.chapter { min-height: 125vh }` media rule will override the hero's `100svh` unless the hero rule is repeated inside the same media query. The hero foot then falls below the fold.
