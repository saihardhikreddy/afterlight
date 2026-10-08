# Contour Band Sphere: build prompt

Use the contour-band-sphere skill. Build a single self-contained `index.html` in plain WebGL2, no libraries.

## Experience

- One glossy organic sphere, centered, slowly rotating, with a slight tilt that follows the pointer.
- The surface is covered in many thin, parallel, swirling ridges, like brain coral or a fingerprint. The ridges are smooth and continuous, never speckled.
- Palette: dark plum valleys, saturated magenta body, pale pink crests, white specular highlights, a soft lavender rim. Background is a radial purple gradient from #4a1a6b in the center to near-black at the edges.

## Technique

- Icosphere at subdivision 7. Domain-warped low-frequency simplex noise as the scalar field. Cosine banding of the field (about 11 bands) drives both displacement and color.
- Normals from finite differences along the tangents in the vertex shader.
- Intro: about 9,000 additive point particles fly in from a wide shell and land on the surface. The mesh grows in by scale under them. Never fade the mesh with opacity.

## Interaction and quality

- A "Replay intro" button. `prefers-reduced-motion` skips the intro and stops rotation.
- Fits the sphere inside the viewport at 1280x720 and 390x844. Device pixel ratio capped at 2.
- Show a readable message if WebGL2 is unavailable.
- Verify with screenshots at both sizes and an empty console before calling it done.
