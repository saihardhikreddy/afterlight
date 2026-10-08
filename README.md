# Afterlight

Reusable skills, build prompts and starter files for making interfaces with AI coding agents (Claude Code, Codex, Cursor, Antigravity). The core is the design language and techniques behind [SentinelSpread](https://sentinelspread.vercel.app/). Each skill is a technique or workflow that worked once and is written down so an agent can do it again without rediscovering it.

![The SENTINEL ring station from SentinelSpread](skills/webgl/sentinel-ring-station/demo/preview.png)

Modeled on [MengTo/kage](https://github.com/MengTo/kage) and its companion library [MengTo/Skills](https://github.com/MengTo/Skills): small static files, no build step, prompts treated as versioned assets.

## SentinelSpread skills

The main set: everything that makes [sentinelspread.vercel.app](https://sentinelspread.vercel.app/) look and move the way it does, taken from its source.

| Skill | Use it when |
|:--|:--|
| [sentinel-ring-station](skills/webgl/sentinel-ring-station/SKILL.md) | **The signature piece.** The SENTINEL ring space station: a Blender script that models it, a GLB with named anchors, and live three.js effects (bay door and cipher core, downlink beam with 16-chip packets, hologram, waveform ring). Includes the build script, the model and a runnable [station viewer](skills/webgl/sentinel-ring-station/demo/index.html). |
| [sentinel-design-system](skills/ui/sentinel-design-system/SKILL.md) | You want the SentinelSpread look: deep navy, one ice-blue accent, Geist + Geist Mono, editorial chapters, spec lists. Includes [tokens.css](skills/ui/sentinel-design-system/tokens.css) and a runnable [mission page demo](skills/ui/sentinel-design-system/demo/index.html). |
| [editorial-scroll-story](skills/ui/editorial-scroll-story/SKILL.md) | Copy sits over a moving scene: chapters, word-by-word reveals, chapter rail, side-aware scrims instead of panels, a preloader that never blocks. |
| [liquid-glass-workbench](skills/ui/liquid-glass-workbench/SKILL.md) | Working tools under a landing page: clear glass console, one tool on stage, Input/Output split, readings and verdicts. |
| [scroll-chapter-camera](skills/webgl/scroll-chapter-camera/SKILL.md) | A 3D camera that flies authored shots as you scroll: conductor, chapter ledger, Bezier swoops, banking, drag-to-rotate hero. |
| [cinematic-post-pipeline](skills/webgl/cinematic-post-pipeline/SKILL.md) | Bloom, grade, aberration, grain and ACES in ~140 lines of Three.js, driven per chapter. |
| [pinned-3d-annotations](skills/ui/pinned-3d-annotations/SKILL.md) | HTML callouts that follow parts of a 3D model. |

Start with the [mission page build prompt](prompts/sentinel-mission-page.md) to rebuild the whole thing, or the [demo](skills/ui/sentinel-design-system/demo/index.html) to see the pieces working together.

## Also included

General workflow skills, plus two from the earlier WebGL sphere experiment.

| Skill | Use it when |
|:--|:--|
| [contour-band-sphere](skills/webgl/contour-band-sphere/SKILL.md) | You want a glossy, organic noise-displaced hero sphere (brain-coral / fingerprint ridges) in plain WebGL2. Includes a runnable [demo](skills/webgl/contour-band-sphere/demo/index.html). |
| [scale-reveal-particle-burst](skills/webgl/scale-reveal-particle-burst/SKILL.md) | An intro where particles converge onto a mesh and the mesh appears, without transparency sorting glitches. |
| [single-file-page](skills/ui/single-file-page/SKILL.md) | Shipping a page as one self-contained HTML file that works from GitHub Pages or a double-click. |
| [design-quality-gate](skills/ui/design-quality-gate/SKILL.md) | Any UI task. A short checklist that stops generic, reflexive design choices. |
| [readme-showcase](skills/ui/readme-showcase/SKILL.md) | Making a repo's README look like a product page: banner, badges, demo GIF, scannable tables. |
| [reference-to-build-prompt](skills/workflow/reference-to-build-prompt/SKILL.md) | Turning a screenshot, screen recording or live site into a precise build prompt. |
| [screenshot-verify-loop](skills/workflow/screenshot-verify-loop/SKILL.md) | Checking UI work in a real browser at desktop and phone sizes before calling it done. |
| [verify-agent-claims](skills/workflow/verify-agent-claims/SKILL.md) | An agent says it committed, pushed or deployed. Confirm against ground truth. |

Prompts you can paste straight into an agent live in [prompts/](prompts/). The [build prompt template](prompts/build-prompt-template.md) follows the same shape as kage's `PROMPT.md`.

## Using a skill

The format is plain Markdown folders, so it works with any agent.

- **Claude Code**: copy or symlink a skill folder into `~/.claude/skills/` (personal) or `.claude/skills/` (per repo). The `name` and `description` frontmatter is what Claude uses to decide when to load it.
  ```bash
  ln -s "$PWD/skills/ui/sentinel-design-system" ~/.claude/skills/sentinel-design-system
  ```
- **Codex**: reference the skill from `AGENTS.md`, or say "load skills/ui/sentinel-design-system/SKILL.md first".
- **Cursor / Antigravity / others**: attach the `SKILL.md` as context, then give the task.

## Run the demos

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Then open `http://127.0.0.1:4173/skills/webgl/sentinel-ring-station/demo/` (the station), `http://127.0.0.1:4173/skills/ui/sentinel-design-system/demo/` or `http://127.0.0.1:4173/skills/webgl/contour-band-sphere/demo/`. There is no build step and no runtime network dependency.

To screenshot every demo at desktop and phone size and fail on console errors or missing files:

```bash
npm i -D playwright   # once
node scripts/verify.mjs
```

## Adding a skill

1. Copy [templates/SKILL.template.md](templates/SKILL.template.md) to `skills/<category>/<skill-name>/SKILL.md`.
2. Write the description as "what it does. Use when ...". That one line decides whether an agent picks the skill up.
3. Keep the body to steps, defaults and pitfalls. Put long background in `REFERENCES.md` next to it.
4. If the skill produces something visual, add `demo/index.html` (self-contained) and `demo/PROMPT.md` (the exact prompt that recreates it).
5. Run `python3 scripts/check_skills.py` before committing. CI runs it too.

## Structure

```text
afterlight/
├── README.md
├── CLAUDE.md                 # how agents should work in this repo
├── skills/
│   ├── webgl/                # rendering techniques
│   ├── ui/                   # layout, design quality, presentation
│   └── workflow/             # capture, prompt, verify loops
├── prompts/                  # paste-ready build prompts
├── templates/                # skill template and single-file page starter
├── scripts/
│   ├── check_skills.py       # frontmatter and link lint
│   └── verify.mjs            # Playwright screenshots + console/404 check
└── .github/workflows/        # CI for the lint
```

## License

MIT for the code and prompts here. Third-party references keep their own licenses.
