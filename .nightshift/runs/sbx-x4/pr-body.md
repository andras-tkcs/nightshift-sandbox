## Summary

Adds `titlecase(text)` to `sandbox_pkg/text.py`: lowercases, turns runs of spaces and punctuation into single hyphens, and leaves no leading or trailing hyphen. Includes unit tests and a README section. Tier T2, one phase, one review round; the review board approved with no blocking findings.

## Phases

| Phase | Title | Merge commit | Status |
|---|---|---|---|
| p1-titlecase | Add titlecase(text) with tests and a README section, and retire the plan | e9b51fd | merged |

## Checks

From `dod.md`:

- `.venv/bin/pytest -q`: PASS (17 passed)
- `.venv/bin/ruff check .`: PASS
- pyproject.toml unchanged, no dependencies added: ok

## Non-blocking findings and open items

- **Open owner question: rename?** `titlecase` slugifies text rather than title-casing it (README says so). Rename to `slugify`, perhaps keeping `titlecase` as an alias, or keep the requested name? (board-code.md, review-p1-titlecase-1.md, board-acceptance.md; `sandbox_pkg/text.py:14`)
- `tests/test_acceptance_sbx_x4.py:1`: the xfail markers were removed (assertions unchanged); the file was not in the phase `touches`, and the plan's "11 passed" should read 17.
- `tests/test_text.py:20-40`: the unit tests duplicate the AC-1 to AC-5 assertions in the acceptance file. Follow-up: keep one set.
- Plan manifest says `feature_branch: feature/sbx-x4`; the run used `feature/x4`.
- Note: origin/main shares no history with this branch, so the base is `e2e/20261002-5`.

## Manual verification

None (`manual_after` is empty).

## Desk link

Run files are published by `ns-conductor finish` at gate 2; `ns status sbx-x4` shows no desk URL yet.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
