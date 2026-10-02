## Summary

Adds `slugify(text)` to `sandbox_pkg/text.py` (lowercase, runs of non-alphanumerics become one hyphen, no leading or trailing hyphen), with tests and a README section. Also fixes the "recieve" typo in the README and retires the plan document. Base branch is `e2e/20261002-3`; `main` has no shared history with this branch.

## Phases

- p1-slugify: Add slugify with tests and README, retire the plan (merge bc5f304)

## Checks

- `.venv/bin/pytest -q`: pass (21 passed)
- `.venv/bin/ruff check .`: pass

## Non-blocking findings and open items

- Manifest names `feature/sbx-x2` but the branch is `feature/x2` (process only).
- `tests/test_slugify_acceptance.py:3`: module docstring reworded; accurate, optional cleanup.

## Manual verification

None required.

## Desk link

Run files are published on the review desk by `ns-conductor finish` (no desk URL is recorded in `ns status sbx-x2` yet).
