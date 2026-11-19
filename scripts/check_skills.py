#!/usr/bin/env python3
"""Lint every SKILL.md: frontmatter present, name matches folder, description says when to use it,
and relative Markdown links resolve. Also check that demos are self-contained: nothing loaded from
the network (CDNs, fonts) and every local file they load exists. Exits non-zero on any problem."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote as url_unquote

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)#\s<]+)(?:#[^)]*)?(?:\s[^)]*)?\)")
# The other two ways CommonMark writes a link target, which the check above never saw:
# [text](<my file.md>) and reference definitions, "[ref]: path.md" on a line of their own.
LINK_ANGLE = re.compile(r"\]\(<([^>#\n]+)(?:#[^>\n]*)?>")
LINK_REF = re.compile(r"^ {0,3}\[[^\]\n]+\]:[ \t]*<?([^\s>#]+)", re.M)
# Code is shown, not followed: a link-shaped example inside ``` fences or `inline code` isn't a link.
CODE = re.compile(r"^(```|~~~).*?^\1[^\n]*$|`[^`\n]+`", re.S | re.M)
# /* block */ and <!-- HTML --> comments; // line comments only at the start of a line, so URLs survive.
CODE_COMMENT = re.compile(r"/\*.*?\*/|<!--.*?-->|^\s*//[^\n]*", re.S | re.M)
problems = []
verbose = "-v" in sys.argv or "--verbose" in sys.argv

skills = sorted((ROOT / "skills").rglob("SKILL.md"))

# Layout: skills/<category>/<skill-name>/SKILL.md. A skill folder without its SKILL.md was never
# looked at (only SKILL.md files were), so it passed while no agent could ever load it.
for folder in sorted(p for p in (ROOT / "skills").glob("*/*") if p.is_dir()):
    if not (folder / "SKILL.md").is_file():
        problems.append(f"{folder.relative_to(ROOT)}: skill folder has no SKILL.md")
for skill in skills:
    if len(skill.relative_to(ROOT / "skills").parts) != 3:
        problems.append(f"{skill.relative_to(ROOT)}: SKILL.md belongs in skills/<category>/<skill-name>/")
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
    # Limits the skill loaders enforce on upload: a skill that breaks them is refused there
    # even though it reads fine here.
    if len(name) > 64:
        problems.append(f"{rel}: name over 64 characters")
    if re.search(r"anthropic|claude", name):
        problems.append(f"{rel}: name may not contain the reserved words 'anthropic' or 'claude'")
    if re.search(r"<[^>]*>", desc):
        problems.append(f"{rel}: description may not contain XML/HTML tags (angle brackets)")

    if verbose and len(problems) == before:  # this skill added no problems
        print(f"  [OK] verified skill: {skill.parent.name}")

# Skills are portable (CLAUDE.md): a path into one person's home folder works on their machine
# only, and an agent elsewhere follows it to nothing. Checked in skill files and demos alike.
MACHINE_PATH = re.compile(r"(?:/Users/|/home/)(?!user\b|you\b|name\b|me\b)[A-Za-z0-9._-]+/|\b[A-Za-z]:[\\/]Users[\\/]", re.I)
for f in sorted((ROOT / "skills").rglob("*")):
    if f.is_file() and f.suffix in {".md", ".html", ".js", ".mjs", ".css", ".py", ".json"} and "vendor" not in f.parts:
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for hit in MACHINE_PATH.finditer(line):
                problems.append(f"{f.relative_to(ROOT)}:{n}: machine-specific path '{hit.group(0)}'; skills must be portable")

for md in sorted(ROOT.rglob("*.md")):
    if any(part.startswith(".") or part == "node_modules" for part in md.relative_to(ROOT).parts):
        continue
    prose = CODE.sub("", md.read_text(encoding="utf-8"))
    for target in LINK.findall(prose) + LINK_ANGLE.findall(prose) + LINK_REF.findall(prose):
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
IMPORT_MAP = re.compile(r"<script\b[^>]*\btype\s*=\s*[\"']importmap[\"'][^>]*>(.*?)</script>", re.I | re.S)


def import_map_targets(text, rel):
    """URLs an import map points bare module names at. A bare import is only as offline as these."""
    targets = []
    for block in IMPORT_MAP.findall(text):
        try:
            data = json.loads(block)
        except ValueError:
            problems.append(f"{rel}: import map is not valid JSON")
            continue
        scopes = [data.get("imports", {})] + list(data.get("scopes", {}).values())
        targets += [v for scope in scopes for v in scope.values() if isinstance(v, str)]
    return targets


for demo_file in sorted((ROOT / "skills").rglob("demo/**/*")):
    if demo_file.suffix not in {".html", ".js", ".mjs", ".css"} or "vendor" in demo_file.parts:
        continue
    text = CODE_COMMENT.sub("", demo_file.read_text(encoding="utf-8"))
    rel = demo_file.relative_to(ROOT)
    found = [(pattern, t) for pattern in LOADS for t in pattern.findall(text)]
    found += [(IMPORT_MAP, t) for t in import_map_targets(text, rel)]
    for pattern, target in found:
        target = target.strip()
        if re.match(r"^(https?:)?//", target):
            problems.append(f"{rel}: loads {target} from the network; demos must be self-contained")
        elif target.startswith("/"):
            problems.append(f"{rel}: loads {target} from the filesystem root; use a relative path")
        elif re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#") or "${" in target:
            continue  # data:, blob:, an in-page anchor or a template string
        elif not target.startswith(".") and pattern is LOADS[2]:
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
