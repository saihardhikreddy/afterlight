---
name: scroll-chapter-camera
description: Fly a Three.js/WebGL camera through authored shots as the page scrolls, using a native-scroll conductor, a per-chapter ledger of camera and effect values, Bezier swoops between shots, dwell orbits, banking, lens breathing and a drag-to-rotate hero turntable. Use when building a scroll-driven 3D story, product flythrough or "mission" page where each section is a composed camera shot.
---

# Scroll Chapter Camera

From the SentinelSpread world. The conductor is in [references/scroll-conductor.js](references/scroll-conductor.js) (adapted from MengTo/Skills, MIT).

## 1. Conductor

Native scroll stays the source of truth. Measure an anchor scroll position per section (hero at 0, middle chapters centered, last at its top minus 15% of the viewport) and map `scrollY` to a fractional chapter `exact`. Each frame, `smooth = damp(smooth, exact, 5.2, dt)`.

- `exact` → DOM state (active chapter, rail). `smooth` → camera.
- Ignore resize events on coarse pointers when only the height changed (mobile URL bar).
- Re-measure on `document.fonts.ready` and with a `ResizeObserver` on `body`.
- Pause on `visibilitychange`.

## 2. The ledger

One array, one entry per chapter, holding everything the scene needs:

```js
{ id: "transmit", side: "left", part: "hga",
  cam: [4.56, 4.75, 14], tgt: [-0.88, 5.43, 2.11], fov: 44,
  orbit: 22, tilt: 6, roll: 9, ctl: [18, 13, 20],
  fx: { open: 0, beam: 1, holo: 0, bloom: 1.05, warm: 0.25, exposure: 1.05, dim: 1 } }
```

Between chapters `i` and `i+1`, with `t = easeInOutCubic(local)`, lerp every `fx` channel. Effects (a door opening, a beam, bloom, grade) are just numbers in the ledger, so one scroll value drives the whole scene.

## 3. Camera moves

- **Swoop**: position follows a quadratic Bezier `cam[i] → ctl[i] → cam[i+1]`, so each move goes under, over or around instead of a straight drift. The look-at target lerps on a gentler smoothstep.
- **Dwell**: inside a chapter (`dwell = p - round(p)`, −0.5…0.5), rotate the offset by `orbit° * dwell` around Y and `tilt°` around the camera's right axis, faded out near the boundaries.
- **Bank**: roll into lateral velocity, `damp(roll, clamp(-lateral * 0.012, ±0.16), 3, dt)`, plus the authored per-chapter `roll` (a dutch angle).
- **Breathe**: FOV opens with scroll speed, `damp(breathe, min(speed*5, 7), 2.5, dt)`.
- **Parallax**: fine pointers offset the camera in its own plane by `distance * 0.03`.
- **Mobile**: push each shot 1.45x further from its target and add 8° FOV.
- **Hero turntable**: in chapter 0 only, drag rotates yaw and pitch with inertia (`v *= exp(-3.2 dt)`), idle drift after 2.5s, and both ease back to zero as you leave the hero.

## 4. Authoring shots

- Add `?debug` to expose the rig and skip damping, then frame each chapter by hand and paste the numbers.
- Measure clearance from the hull along each swoop; a control point inside the model whips the view. SentinelSpread's ledger comments record the measured clearance per move.
- Compile all programs (`renderer.compileAsync`) before the first visible frame, and finish the preloader on that frame.

## Reduced motion

No damping (`smooth = exact`), no roll, no breathe, no idle drift; the shots are still composed, just cut between.
