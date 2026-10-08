---
name: verify-agent-claims
description: Confirm what a coding agent reports (commits, pushes, deploys, test runs, file writes) against ground truth before trusting it. Use whenever an agent's summary says something was committed, pushed, deployed, passed or fixed, especially across many repos or after a long autonomous run.
---

# Verify Agent Claims

Agent tool-call summaries can report success that never happened, including invented commit hashes and pushes that silently failed. Check the system, not the summary.

## Ground-truth checks

| Claim | Check |
|:--|:--|
| "Committed" | `git log --oneline -3` shows the message and the hash it quoted |
| "Pushed" | `git fetch origin && git log origin/<branch> --oneline -3` matches local |
| "Fixed the README / file" | `git show origin/<branch>:README.md \| head`, or open it on GitHub in a fresh browser tab |
| "Tests pass" | Run them yourself; read the summary line, not the agent's paraphrase |
| "Deployed" | Load the live URL in a fresh session and check the change is there |
| "Page works" | [screenshot-verify-loop](../screenshot-verify-loop/SKILL.md) |

## Across many repos

Loop and print one line per repo so gaps are obvious:

```powershell
Get-ChildItem -Directory | ForEach-Object {
  Push-Location $_.FullName
  git fetch origin -q
  "{0,-40} local {1}  remote {2}" -f $_.Name, (git rev-parse --short HEAD), (git rev-parse --short '@{u}')
  Pop-Location
}
```

```bash
for d in */; do (cd "$d" && git fetch -q origin && printf '%-40s local %s  remote %s\n' "$d" "$(git rev-parse --short HEAD)" "$(git rev-parse --short @{u})"); done
```

## Pitfalls

- Windows paths with spaces break unquoted CLI calls, often without an error. Quote every path.
- Cached web fetches of GitHub pages can show stale state. Use `git` or the API, not a cached page.
- "No changes to commit" is a success message for the agent and a failure for you if you expected changes.
