---
name: cinematic-post-pipeline
description: A small, dependency-free Three.js post stack - HDR scene target, bright pass, 4-level mip bloom, and one composite pass with chromatic aberration, exposure, split-tone grade, ACES, vignette, film grain and optional scanlines, all driven by per-chapter uniforms. Use when a WebGL scene looks flat or "CG", needs bloom without EffectComposer, or needs a grade that changes per section.
---

# Cinematic Post Pipeline

Full code: [references/post.js](references/post.js) (from SentinelSpread, about 140 lines, no addons).

## Passes

1. Render the scene into a HalfFloat target (MSAA 4 on desktop, 0 on coarse pointers). Turn renderer tone mapping off; it happens in the composite.
2. **Bright pass** at half resolution: keep pixels whose max channel passes `smoothstep(0.95, 1.65, l)`. Emissive colors must be authored above 1.0 to bloom.
3. **Mip bloom**: 4 levels, each half the previous; a 9-tap separable Gaussian, horizontal then vertical, per level.
4. **Composite**, in this order:
   - radial chromatic aberration, stronger toward the edges (`off = d * uAberr * (0.004 + r² * 0.05)`)
   - bloom = levels weighted 0.5, 0.65, 0.85, 1.1 (wide levels heavier), times `uBloom`
   - exposure, then a split-tone grade `mix(cool(0.88,0.98,1.12), warm(1.1,0.97,0.84), uWarm)`
   - ACES filmic
   - vignette, optional scanlines, animated grain `±uGrain`
   - gamma 2.2

## Driving it

Expose the composite uniforms (`post.params`) and set `uBloom`, `uWarm`, `uExposure` from the chapter ledger every frame (see [scroll-chapter-camera](../scroll-chapter-camera/SKILL.md)). SentinelSpread defaults: aberration 0.22, grain 0.03, scanlines 0, vignette 0.85, bloom 0.85 to 1.05, exposure 1.0 to 1.05, and exposure 0.62 behind the workbench.

## Pitfalls

- Bloom with everything at or below 1.0 does nothing visible; raise emissive and sun values, don't lower the threshold.
- Aberration above about 0.4 reads as a broken lens, not cinema.
- Cap pixel ratio (1.5 desktop, 1.25 touch) and drop MSAA on phones; the post stack multiplies fill cost.
- On `webglcontextlost`, cancel the loop and fall back to the no-WebGL page state.
