---
name: screenshot-verify-loop
description: Verify UI work in a real headless browser by screenshotting desktop and phone viewports and failing on console errors, page errors or 404s, then looking at the images. Use when about to say any page, demo or visual "works", and after every meaningful visual change.
---

# Screenshot Verify Loop

Source code that looks right is not evidence. A screenshot and an empty console are.

## Run it

```bash
node scripts/verify.mjs                     # every skills/**/demo
node scripts/verify.mjs path/to/demo        # one folder with an index.html
SETTLE_MS=1000 node scripts/verify.mjs ...  # capture mid-animation
```

It serves the repo locally, opens each page at 1280x720 and 390x844, waits, saves PNGs to `.verify/`, and exits non-zero on any console error, uncaught exception or HTTP status of 400 or more.

Needs Playwright (`npm i -D playwright`, or a global install). WebGL runs through SwiftShader, so it works on CI and headless machines; expect it to be slower than a GPU.

## Then actually look

Open the PNGs and check:

- the focal element is visible, centered as intended and not clipped on phone
- text doesn't overlap controls at 390px
- colors match the reference (headless color is close but not exact; judge hue and contrast, not the last 2%)
- for animated pieces, one capture mid-animation and one settled

## Pitfalls

- Waiting on `load` only. Shaders compile and fonts load after it; keep a settle delay.
- Animation clocks that start at script time finish before the first frame on slow machines. Start them on the first frame.
- A black canvas with no errors usually means WebGL context creation failed silently or the camera is inside the mesh. Log the context and the camera distance.
