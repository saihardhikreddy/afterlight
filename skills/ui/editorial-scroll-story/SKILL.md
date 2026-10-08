---
name: editorial-scroll-story
description: The DOM layer of a scroll-driven story over a live 3D or canvas scene - chapters, word-by-word heading reveals, a chapter rail, side-aware scrims instead of text panels, a preloader that never blocks, and a fine-pointer cursor. Use when building a cinematic scrolling landing page, a "mission" or case-study story, or any page where copy sits over a moving scene.
---

# Editorial Scroll Story

From SentinelSpread. Pairs with [scroll-chapter-camera](../../webgl/scroll-chapter-camera/SKILL.md) for the scene and [sentinel-design-system](../sentinel-design-system/SKILL.md) for the look. Working example: [sentinel-design-system/demo](../sentinel-design-system/demo/index.html).

## Structure

```html
<canvas id="world" aria-hidden="true"></canvas>   <!-- fixed, z 0 -->
<div class="scrim" aria-hidden="true"></div>       <!-- fixed, z 1 -->
<header class="bar">…</header>                      <!-- fixed, z 40 -->
<nav class="rail">…</nav>                           <!-- fixed, right edge -->
<main>
  <section class="chapter" data-chapter="0" data-side="left">…</section>
  <section class="chapter chapter--right" data-chapter="1" data-side="right">…</section>
  …
</main>
```

- Each chapter is `min-height: 140vh` (125vh on phones) with one `.copy` block, max 30rem. The extra height is dwell time for the camera.
- One scroll conductor turns scroll into a fractional chapter value: `exact` toggles `.is-active` and the rail, `smooth` drives the scene. See [scroll-conductor.js](../../webgl/scroll-chapter-camera/references/scroll-conductor.js).

## Readability without panels

- A fixed scrim: `linear-gradient(90deg, ink 86% → 60% at 32% → transparent at 58%)` plus a bottom fade. Set `body[data-side]` from the active chapter and mirror the gradient to 270deg for right-side copy.
- Body copy gets a two-layer text shadow (`0 1px 2px` at 85% and `0 0 18px` at 75% of the ink color).
- On phones, swap to a vertical scrim and anchor copy to the bottom of each chapter.
- Never let 3D annotation tags sit under the active copy; hide them when their projected point is inside the copy rect plus 24px.

## Reveal choreography

1. Split each heading into words: `<span class="w"><span style="--i:n">word</span></span>`, `aria-hidden` on the wrappers and the full sentence as the heading's `aria-label`.
2. Outer span `overflow: hidden`; inner span starts at `translateY(110%)` and rises with `transition-delay: calc(var(--i) * 72ms + 120ms)` when the chapter becomes active.
3. Then eyebrow and body at 0.4s, spec at 0.52s, actions and source at 0.62s, each fading up 14px.
4. Shadow the heading with `filter: drop-shadow`, not `text-shadow`, or the masks clip it into boxes.

## Supporting pieces

- **Rail**: buttons with a dash (`::after`, 18px → 34px when current) and a label that fades in on hover, focus or `aria-current="step"`. Click scrolls to the chapter anchor.
- **Preloader**: wordmark, "Acquiring signal", a 1px bar and a mono percentage. It creeps to 88% on a timer, jumps to 94% when assets load, finishes on the scene's first rendered frame, and always finishes by 6 seconds.
- **Cursor**: only when `(pointer: fine)` and motion is allowed. A 30px ring with a 3px accent dot, lerped at 0.22 per frame, growing to 54px over links and buttons. Hide it over the workbench.
- **No WebGL**: add `body.no-webgl`, hide the canvas, show a soft radial background and a one-line notice. The story and tools must still work.

## Reduced motion

Add `body.reduce-motion`: headings and copy fully visible, no transitions, the conductor uses `exact` directly, the scroll jump is instant.
