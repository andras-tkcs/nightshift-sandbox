# Definition of done: sbx-x4 (feature/x4 @ e9b51fd)

| Check | Result | Detail |
|---|---|---|
| `.venv/bin/pytest -q` | PASS | 17 passed |
| `.venv/bin/ruff check .` | PASS | All checks passed! |
| Test added for the change | ok | tests/test_text.py (5 tests), tests/test_acceptance_sbx_x4.py (6, xfail markers removed) |
| README current | ok | `### titlecase` section added |
| No new dependencies | ok | pyproject.toml unchanged |
| `.nightshift/` absent from PR branch | ok | `git ls-files` finds none |

No `docs.dod` is set in the profile; rows come from CLAUDE.md. Branch is up to date with origin/e2e/20261002-5 (0 commits behind).

Verdict: ready to open a pull request.
