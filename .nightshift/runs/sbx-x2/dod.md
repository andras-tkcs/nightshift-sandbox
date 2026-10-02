# Definition of done: sbx-x2

Base: origin/e2e/20261002-3 (profile `git.base_branch`). The profile lists no checks and sets no `docs.dod`; the commands come from CLAUDE.md.

| Check | Result | Detail |
|---|---|---|
| `.venv/bin/pytest -q` | PASS | 21 passed |
| `.venv/bin/ruff check .` | PASS | All checks passed! |
| Conditional rows | n/a | no `docs.dod` section |
| README current (CLAUDE.md) | ok | README.md mentions slugify in intro and Usage |
| Test for every change (CLAUDE.md) | ok | tests/test_text.py, tests/test_slugify_acceptance.py |
| No new dependencies | ok | pyproject.toml unchanged |

Verdict: ready to open a pull request against e2e/20261002-3.
