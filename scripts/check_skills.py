#!/usr/bin/env python3
"""Lint every SKILL.md: frontmatter present, name matches folder, description says when to use it,
and relative Markdown links resolve. Exits non-zero on any problem."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
problems = []

skills = sorted((ROOT / "skills").rglob("SKILL.md"))
for skill in skills:
    rel = skill.relative_to(ROOT)
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        problems.append(f"{rel}: missing frontmatter")
        continue
    meta = dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)
    name = meta.get("name", "").strip()
    desc = meta.get("description", "").strip()
    if name != skill.parent.name:
        problems.append(f"{rel}: name '{name}' does not match folder '{skill.parent.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or "-"):
        problems.append(f"{rel}: name must be kebab-case")
    if "use when" not in desc.lower():
        problems.append(f"{rel}: description should say 'Use when ...'")
    if len(desc) > 1024:
        problems.append(f"{rel}: description over 1024 characters")

for md in sorted(ROOT.rglob("*.md")):
    if any(part.startswith(".") or part == "node_modules" for part in md.relative_to(ROOT).parts):
        continue
    for target in LINK.findall(md.read_text(encoding="utf-8")):
        if re.match(r"^[a-z]+:", target):
            continue
        if not (md.parent / target).exists():
            problems.append(f"{md.relative_to(ROOT)}: broken link -> {target}")

for p in problems:
    print(p)
print(f"{len(skills)} skills checked, {len(problems)} problem(s)")
sys.exit(1 if problems else 0)
