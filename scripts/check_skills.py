#!/usr/bin/env python3
"""Lint every SKILL.md: frontmatter present, name matches folder, description says when to use it,
and relative Markdown links resolve. Also check that demos are self-contained: nothing loaded from
the network (CDNs, fonts) and every local file they load exists. Exits non-zero on any problem."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote as url_unquote

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)#\s]+)(?:#[^)]*)?\)")
# Code is shown, not followed: a link-shaped example inside ``` fences or `inline code` isn't a link.
CODE = re.compile(r"^(```|~~~).*?^\1[^\n]*$|`[^`\n]+`", re.S | re.M)
# /* block */ and <!-- HTML --> comments; // line comments only at the start of a line, so URLs survive.
CODE_COMMENT = re.compile(r"/\*.*?\*/|<!--.*?-->|^\s*//[^\n]*", re.S | re.M)
problems = []
verbose = "-v" in sys.argv or "--verbose" in sys.argv

skills = sorted((ROOT / "skills").rglob("SKILL.md"))
for skill in skills:
    rel = skill.relative_to(ROOT)
    before = len(problems)
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        problems.append(f"{rel}: missing frontmatter")
        continue

    meta = {}
    current_key = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") or line.startswith("\t"):
            if current_key:
                meta[current_key] += " " + line.strip()
        elif ":" in line:
            k, v = line.split(":", 1)
            current_key = k.strip()
            meta[current_key] = v.strip()

    def unquote(value):
        """YAML allows name: "x" and description: 'y'; compare the value, not the quotes."""
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        return value

    name = unquote(meta.get("name", ""))
    desc = unquote(meta.get("description", ""))
    if name != skill.parent.name:
        problems.append(f"{rel}: name '{name}' does not match folder '{skill.parent.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name or "-"):
        problems.append(f"{rel}: name must be kebab-case")
    if "use when" not in desc.lower():
        problems.append(f"{rel}: description should say 'Use when ...'")
    if len(desc) > 1024:
        problems.append(f"{rel}: description over 1024 characters")

    if verbose and len(problems) == before:  # this skill added no problems
        print(f"  [OK] verified skill: {skill.parent.name}")

for md in sorted(ROOT.rglob("*.md")):
    if any(part.startswith(".") or part == "node_modules" for part in md.relative_to(ROOT).parts):
        continue
    for target in LINK.findall(CODE.sub("", md.read_text(encoding="utf-8"))):
        target = url_unquote(target)  # my%20file.md is the file "my file.md"
        if re.match(r"^[a-zA-Z]+:", target) or target.startswith("//") or target.startswith("mailto:"):
            continue
        if not (md.parent / target).exists():
            problems.append(f"{md.relative_to(ROOT)}: broken link -> {target}")

# Demos must work offline from a plain folder (see CLAUDE.md): no CDN, and no missing local files.
LOADS = [
    re.compile(r"<(?:script|img|source|audio|video|iframe)\b[^>]*?\bsrc\s*=\s*[\"']([^\"']+)", re.I),
    re.compile(r"<link\b[^>]*?\bhref\s*=\s*[\"']([^\"']+)", re.I),
    re.compile(r"""(?:\bimport\b[^'"`;]*?\bfrom\s*|\bimport\s*\(?\s*)['"]([^'"]+)['"]"""),
    re.compile(r"""url\(\s*['"]?([^'")]+)"""),
]
for demo_file in sorted((ROOT / "skills").rglob("demo/**/*")):
    if demo_file.suffix not in {".html", ".js", ".mjs", ".css"} or "vendor" in demo_file.parts:
        continue
    text = CODE_COMMENT.sub("", demo_file.read_text(encoding="utf-8"))
    rel = demo_file.relative_to(ROOT)
    for pattern in LOADS:
        for target in pattern.findall(text):
            target = target.strip()
            if re.match(r"^(https?:)?//", target):
                problems.append(f"{rel}: loads {target} from the network; demos must be self-contained")
            elif re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#") or "${" in target:
                continue  # data:, blob:, an in-page anchor or a template string
            elif not target.startswith((".", "/")) and pattern is LOADS[2]:
                continue  # a bare module name ("three") resolved by an import map
            else:
                path = (demo_file.parent / url_unquote(target.split("?")[0].split("#")[0]))
                if not path.exists():
                    problems.append(f"{rel}: loads {target}, which does not exist")

for p in problems:
    print(p)

if problems:
    print(f"[FAIL] {len(skills)} skills checked, {len(problems)} problem(s) found.")
    sys.exit(1)
else:
    print(f"[PASS] {len(skills)} skills checked successfully with 0 problems.")
    sys.exit(0)
