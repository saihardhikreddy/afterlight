---
name: pinned-3d-annotations
description: HTML annotation tags pinned to parts of a 3D model, re-projected every frame, with focus per chapter and collision with page copy handled. Use when labelling parts of a Three.js/WebGL object (a ship, product, machine, building) with callouts that follow it as the camera moves.
---

# Pinned 3D Annotations

From the SentinelSpread ship callouts ("Command module · Cipher core").

## Markup

```html
<div class="tags" aria-hidden="true">
  <p class="tag" data-part="core"><i></i><span><b>Command module</b>Cipher core · AES-256-GCM</span></p>
</div>
```

- `.tags` is fixed, full-screen, `pointer-events: none`. Each tag is absolutely positioned at 0,0 and moved with `transform: translate3d()` only (no top/left, no layout).
- `<i>` is a 9px accent ring with a glowing 1px core; `<span>` holds a small-caps title over a mono detail line, behind a 1px accent rule.

## Per frame

1. Keep anchor points in the model's local space (`ship.anchors.core = new Vector3(...)`).
2. Project: `v.clone().applyMatrix4(object.matrixWorld).project(camera)`, then `x = (v.x+1)/2*innerWidth`, `y = (1-v.y)/2*innerHeight`.
3. Visible only when `v.z < 1` and `|x|,|y| < 1.2` in NDC.
4. Hide any tag whose point falls within 24px of the active copy block's rect. Text over text is unreadable, and over glass it blurs.
5. Classes, not inline opacity: `.is-on` (0.55), `.is-focus` (1, with a ping ring animation) for the part the current chapter is about. Only the focus tag shows on phones.

## Pitfalls

- Updating tags from a separate rAF loop makes them lag the model. Call the placer from the renderer's frame callback.
- Positioning with `left/top` triggers layout every frame. Use transforms and `will-change: transform`.
- Hide all tags over the workbench or any UI that needs the user's attention.
