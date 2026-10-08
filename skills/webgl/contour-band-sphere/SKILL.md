---
name: contour-band-sphere
description: Build a glossy, organic noise-displaced sphere with many thin parallel ridges (brain-coral, fingerprint or topographic look) in dependency-free WebGL2. Use when asked for an organic hero sphere, blob, coral or "displaced sphere with ridges", or when ridged fbm gives one thick ridge per swirl instead of fine rings.
---

# Contour Band Sphere

A warped scalar field on the sphere, terraced into periodic bands, used both to displace the surface and to color it. The fine parallel ridges come from the banding, not from noise detail.

Runnable reference: [demo/index.html](demo/index.html). Recreate it with [demo/PROMPT.md](demo/PROMPT.md).

## Recipe

1. **Mesh.** Icosphere, subdivision 6 (~41k vertices) minimum, 7 (~164k) for crisp crests. UV spheres pinch at the poles; avoid them.
2. **Field.** Domain-warp low-frequency simplex noise:
   ```glsl
   vec3 w = vec3(fbm(p*0.9), fbm(p*0.9 + 5.2), fbm(p*0.9 + 9.1));
   float f = snoise(p*0.85 + warp*w) * 0.5 + snoise(p*1.7 + w) * 0.12;
   ```
   Keep the base noise low frequency. Swirl should come from `warp` (1.0 to 1.6), not from octaves.
3. **Bands.** `ridge = 0.5 - 0.5*cos(2π * f * bands)`, with `bands` around 8 to 14. Each contour of the field becomes one ridge.
4. **Displace.** `p = n * (1 + swell*f + ridge_h*ridge)`, with `swell` about 0.08 and `ridge_h` about 0.02 to 0.03.
5. **Normals.** Displace two nearby points along the tangents and cross the differences, in the vertex shader. Derivative normals (`dFdx`) look faceted.
6. **Shade.** Color by `ridge`: dark plum valley, saturated body, pale crest. Add a tight specular (power ~90), a broad low one, and a restrained fresnel rim. Tone-map before gamma.
7. **Background.** A CSS radial gradient behind a transparent canvas. Cheaper than a full-screen pass and easy to restyle.

## Defaults

| Param | Value | Effect |
|:--|:--|:--|
| subdivisions | 7 | Mesh density; lower if the ridges alias |
| bands | 11 | Number of rings across the field range |
| warp | 1.35 | Swirl strength |
| ridge | 0.028 | Crest height |
| swell | 0.08 | Lumpiness of the overall body |

## Pitfalls

- **Ridged fbm (`1 - abs(noise)`) gives one thick ridge per swirl arm.** Use contour banding of a smooth field instead.
- **A triangle wave (`fract`) makes stair-step crests** at mesh resolution. Use cosine.
- **Too many octaves or too many bands turns the surface into speckle.** If it looks like sandpaper, halve the base frequency first, then the band count.
- **Where the field gradient is steep, bands crowd and alias.** Raise subdivision, or lower `bands`.
- **Fading the mesh in with opacity** shows z-sorting holes on a self-overlapping mesh. Reveal by scale; see [scale-reveal-particle-burst](../scale-reveal-particle-burst/SKILL.md).
- Pale, washed-out color usually means too much fresnel or ambient. Keep ambient near 0.12.

## Verify

Run `node scripts/verify.mjs skills/webgl/contour-band-sphere/demo` and look at both screenshots. Check that the crests read as thin continuous rings, not dots, and that the sphere fits the phone viewport.
