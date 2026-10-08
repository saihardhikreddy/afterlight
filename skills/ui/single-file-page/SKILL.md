---
name: single-file-page
description: Ship a page, demo or visual as one self-contained HTML file with inline CSS and JS, relative paths and no build step, so it runs from a double-click, any static server or a GitHub Pages subpath. Use when the deliverable is a demo, prototype, hero visual, WebGL piece or anything that should "just open".
---

# Single File Page

Start from [templates/single-file-page.html](../../../templates/single-file-page.html).

## Rules

- One `index.html`. CSS in a `<style>`, JS in a `<script>`. Anything that can't be inline (images, fonts, models, a vendored library) goes in `assets/` next to it and is referenced with a relative path (`assets/x.webp`, never `/assets/x.webp`), so it still works under `user.github.io/repo/`.
- No CDN, analytics, remote fonts or runtime network calls. Vendor a library file if you truly need one, and keep its license header.
- Design tokens as CSS custom properties on `:root`. Set an explicit `body` background.
- `<meta name="viewport">`, a real `<title>`, `lang` on `<html>`.
- Canvas pieces: cap device pixel ratio at 2, handle resize, show a readable fallback if WebGL/WebGL2 is missing, and give the canvas `role="img"` plus an `aria-label` describing what it shows.
- Respect `prefers-reduced-motion`: keep the full content and a finished static state, drop the motion.
- Controls are real `<button>`s with a visible `:focus-visible` style.

## Before calling it done

- Open it from `file://` once and from a static server once (`python3 -m http.server`).
- Run the [screenshot-verify-loop](../../workflow/screenshot-verify-loop/SKILL.md): desktop and 390x844, empty console, no 404s.
