---
name: readme-showcase
description: Turn a GitHub README into a product-page style showcase with a banner, badges, a demo GIF, scannable tables and a short setup path. Use when publishing or polishing a repo, or when a README is a wall of text, broken, or missing visuals.
---

# README Showcase

Reference: the `gesture-reactions` README pattern. Banner, one-line hook, demo, a table of what it does, then setup.

## Layout, top to bottom

1. **Banner** `assets/banner.svg`, centered, `width="100%"`, with real alt text. SVG keeps it crisp and tiny; draw it by hand, don't screenshot text.
2. **Badges** in one centered row: CI status first (live, links to the workflow), then platform, language version, key library, license. Five or six at most.
3. **Hook.** One bold sentence that says what happens for the user, then one or two plain lines on where it works.
4. **Demo.** A GIF or WebP under ~5 MB, 640px wide, showing the real thing in under 10 seconds. Generate it with a script (`scripts/make_demo.*`) so it can be refreshed.
5. **What it does.** A table when items share columns (input → output → shortcut). Bullets otherwise.
6. **Setup.** Numbered steps a non-developer can follow. Bold the thing to click. Put "first run is slower because..." notes here.
7. **Updating, troubleshooting, how it works, project structure, license.** In that order, each short.

## Rules

- Every image has alt text and lives in `assets/` in the repo. No hotlinked images.
- Relative links only, so forks and branches render correctly.
- Use GitHub alert blocks (`> [!TIP]`, `> [!WARNING]`) sparingly, for things people actually trip on.
- Check the rendered README on GitHub (or with a Markdown preview) at narrow width before calling it done. Broken image paths are the most common failure.
