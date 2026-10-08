---
name: scale-reveal-particle-burst
description: Intro animation where particles converge onto a 3D mesh's surface while the mesh appears, without transparency sorting artifacts. Use when building a particle-to-object reveal, a "materialize" intro, or when a mesh fade-in shows holes, flicker or see-through patches.
---

# Scale Reveal Particle Burst

## The rule

Never fade an opaque, self-overlapping mesh in with alpha. With blending on and depth writes on, back faces drawn after front faces get rejected or show through depending on triangle order, so the mesh flickers and shows holes while it fades. Reveal it by **scale** (or a clip/dissolve threshold) and keep it fully opaque.

## Recipe

1. **Targets.** Pick N random vertices of the final mesh as particle end points. Sample vertices, not random sphere points, so particles land on the real surface.
2. **Starts.** Random points on a wide shell (radius 3x to 7x the mesh). Give each a random delay in 0 to 0.35 of the intro.
3. **Motion on the GPU.** Pass start, end and delay as attributes and one `uProgress` uniform. In the vertex shader:
   ```glsl
   float t = clamp((uProgress - aDelay) / (1.0 - aDelay*0.6), 0.0, 1.0);
   float e = 1.0 - pow(1.0 - t, 3.0);          // easeOutCubic
   vec3 p = mix(aStart, aEnd * 1.02, e);       // land just above the surface
   ```
4. **Blend additively** (`gl.blendFunc(gl.ONE, gl.ONE)`, `depthMask(false)`). Additive is order-independent, so particles need no sorting either.
5. **Mesh reveal.** Scale from 0 to 1 over roughly 45% to 95% of the intro with an in-out cubic. Particles fade out over the last 18%.
6. **Timing.** Start the clock on the first rendered frame, not when the script runs. Shader compile can eat most of a short intro otherwise.
7. **Reduced motion.** Jump straight to progress 1.

## Pitfalls

- Opacity fade on the mesh: the artifact this skill exists to avoid.
- Particles at exactly the surface radius z-fight with it. Land at 1.02x.
- Point size must be multiplied by device pixel ratio or particles vanish on Retina screens.
- If the mesh is displaced in the shader, particles land on the undisplaced position. That's usually fine under the 1.02 offset; for heavy displacement, run the same displacement on particle targets.

Working example: the intro in [contour-band-sphere/demo](../contour-band-sphere/demo/index.html).
