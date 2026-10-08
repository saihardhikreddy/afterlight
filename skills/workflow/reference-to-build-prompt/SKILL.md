---
name: reference-to-build-prompt
description: Turn a visual reference (screenshot, screen recording, live site or existing HTML) into a precise, paste-ready build prompt an agent can one-shot. Use when the user shares a reference and says "make this", "recreate this", "write a prompt for this", or when iterating on a visual that keeps drifting from the reference.
---

# Reference To Build Prompt

## Steps

1. **Look properly.** For video, pull frames at the key moments (start, mid-motion, settled) with `ffmpeg -i ref.mp4 -vf fps=2 frames/%03d.png`. For a live page, take a full-page screenshot plus desktop and phone viewports. For HTML, read the source; source behavior beats guessing from pixels.
2. **Extract, don't describe.** Write down:
   - palette as hex values sampled from the frames
   - type: families (or closest free match), sizes, weights, case, tracking
   - layout: grid, alignment, spacing rhythm, what is pinned or layered
   - the one focal element and how it's made (DOM, canvas, WebGL, video)
   - motion: what moves, trigger, duration, easing, order
3. **Name the technique.** "Organic sphere" is vague; "domain-warped field, cosine-banded, displaced icosphere" is buildable. If a skill in this repo covers it, reference the skill by name.
4. **Write the prompt** using [prompts/build-prompt-template.md](../../../prompts/build-prompt-template.md): Experience, Layout, Motion, Interaction and quality. Concrete values where they matter, ranges where taste should decide.
5. **Add the checks** the agent must pass: viewports, console, assets, reduced motion.
6. **Iterate one or two things at a time.** Compare a new screenshot side by side with the reference and change only what differs most. Rewriting the whole prompt each round loses what was already right.

## Pitfalls

- Copying identity (logos, exact copy, brand names) instead of principles. Recreate the technique and feel, not the brand.
- Adjectives without numbers ("soft glow", "subtle") get generic output. Pair each with a value or a reference frame.
- Prompts that list every detail at equal weight. Lead with the focal element; the rest supports it.
