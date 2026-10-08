---
name: design-quality-gate
description: A short pass/fail checklist so UI choices are made for the product rather than by reflex. Use when building, revising or reviewing any page, component or visual, and before handing UI work back.
---

# Design Quality Gate

Keep the chosen direction. This gate removes reflexive choices; it is not a reason to redesign.

## Before designing

- Name the one thing the screen is for and its one primary action.
- Write a one-line visual thesis ("a single glossy object on deep purple, nothing else competing").
- If the project has tokens, components or screenshots, read them first and reuse them.

## While building, check each addition

- **Earns its place.** Would removing it lose information, state, action or meaning? If not, remove it.
- **One focal point** per viewport. Supporting elements are quieter in size, weight and contrast.
- **System.** Same type scale, spacing rhythm, radii, colors and motion language as the rest.
- **Proximity before boxes.** Group by spacing first; add cards and borders only when spacing can't do it.
- **Motion explains something:** a state change, a cause, continuity. Not "proof that it's interactive".
- **Specific, not generic.** Could this section be pasted into an unrelated product unchanged? Then it's filler.

## Common reflexes to catch

- Gradient text, glassmorphism and glow added for no reason.
- Three identical feature cards with an icon tile each.
- Eyebrow labels and pill badges on every heading.
- Placeholder stats, fake logos or fake testimonials.
- Centered everything, with no asymmetry or tension.
- Low-contrast grey body text on a tinted background.

## Before handing back

- Look at a real render at desktop and phone width, not only the code.
- Text contrast meets WCAG AA (4.5:1 body, 3:1 large text).
- Fix the single most visible problem first, then re-check.
