## Summary

Adds `word_count(text)` to `sandbox_pkg/text.py` and `clamp(value, low, high)` to `sandbox_pkg/numbers.py`, each with tests, and documents both in the README. `clamp` raises `ValueError` on NaN arguments and on low > high. Tier T3, one review round per phase, board verdicts (code, security, acceptance) all approve with no blocking findings.

## Phases

| Phase | Merge commit |
|---|---|
| p1-word-count | 72131bd |
| p2-clamp | 8d4589f |
| p3-retire (README, retire plan) | 01418fe |

## Checks

From `dod.md`: `pytest -q` 47 passed; `ruff check .` clean; no dependency change; branch not behind base.

## Non-blocking findings and open items

- p2-clamp and p3-retire each landed as two commits (e47055b + 187c011, daf280c + 75e7ba2), so the literal `HEAD~1` phase acceptance checks are unmet. Squash on merge if one commit per phase is wanted.
- Phase commits edit tests/test_acceptance_sbx_x3.py (owner-approved exception): only `@ACCEPTANCE` xfail markers were removed, no assertion changed.
- tests/test_acceptance_sbx_x3.py:19: `ACCEPTANCE` constant is now unused and the module docstring is stale.
- tests/test_acceptance_sbx_x3.py:149: `eval()` runs README examples. Not exploitable today; parse with `ast` or restrict builtins.
- AC-8 as written diffs `origin/main`, which has no pyproject.toml; against the base the diff is empty, so no dependency was added.
- The manifest names `feature/sbx-x3`; the run used `feature/x3`. Delete the phase branches after merge.

## Manual verification

None.

## Desk link

Run files (plan, review and board files, handoff report) are published on the review desk for sbx-x3; see `ns status sbx-x3`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
