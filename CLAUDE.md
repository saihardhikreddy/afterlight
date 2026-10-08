# Working in this repo

This repo is a library of agent skills for UI work. Read the narrowest matching `SKILL.md` before acting.

- Skills are portable. Nothing in a skill may depend on a specific machine, path, account or project unless the user supplies it.
- Every `SKILL.md` starts with `name` (kebab-case, same as its folder) and `description` ("what it does. Use when ...").
- Demos are single self-contained HTML files with relative paths. No framework, package manager, CDN or build step.
- Before saying a demo works, run `node scripts/verify.mjs` (or open it at 1280x720 and 390x844) and check the console. A screenshot is evidence; "it should work" is not.
- Never report a commit or push as done without checking `git log origin/<branch> --oneline -3`.
- Run `python3 scripts/check_skills.py` before committing.
