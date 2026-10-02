# Test strategy: sbx-x2

## Pyramid

| Level | Count | Why |
|---|---|---|
| Unit | 7 cases (4 test functions, 2 parametrized) | `slugify` is a pure function; every behaviour in AC-1 to AC-4 is one input/output pair. |
| Integration | 1 | AC-7 reads the real `README.md`, extracts each `slugify(...)  # "..."` example and checks it against the function. |
| End to end | 0 | No user-visible flow beyond a library call; AC-5 and AC-6 are whole-suite commands. |

All acceptance tests are in `tests/test_slugify_acceptance.py`, separate from
`tests/test_text.py` where the implementer adds the plan's own `test_slugify`
(D2). Marker on every test:
`pytest.mark.xfail(strict=True, raises=AssertionError, reason="ns:sbx-x2 acceptance")`.
`raises=AssertionError` makes the tests fail for the right reason only: the
module is imported as `sandbox_pkg.text` and `slugify` is looked up with
`getattr`, so a missing function is an assertion failure, not a collection
error; any other exception (typo, import error) is reported as a real failure.

## AC to test

| AC | Proven by | Kind |
|---|---|---|
| AC-1 | `test_ac1_slugify_lowercases_and_hyphenates_space` | unit test; also the command in acceptance.md |
| AC-2 | `test_ac2_slugify_collapses_separator_runs` (2 cases) | unit test |
| AC-3 | `test_ac3_slugify_has_no_leading_or_trailing_hyphen` (3 cases) | unit test |
| AC-4 | `test_ac4_slugify_keeps_digits` | unit test |
| AC-5 | Command: `.venv/bin/pytest -q tests/test_text.py -k slugify` collects >= 1 test, all pass (plan D2: 7 passed) | command; the tests are the implementer's own in `tests/test_text.py` |
| AC-6 | Commands: `.venv/bin/pytest -q` has 0 failures; `.venv/bin/ruff check .` prints "All checks passed!" | command |
| AC-7 | `test_ac7_readme_slugify_example_matches_function`; plus command `grep -n slugify README.md` prints >= 1 line | integration test + command |

## Fixtures

None. Inputs are literals from acceptance.md; AC-7 reads the checked-in `README.md`.

## State at commit

`.venv/bin/pytest -q`: 6 passed, 8 xfailed. `.venv/bin/ruff check .`: All checks passed.
Sanity check (scratch copy outside the repo, markers removed, design D1 code and
plan D3 README line applied): 8 passed. So the tests pass with the planned
implementation and fail without it.

## For the implementing phase (p1-slugify)

- Remove the `ACCEPTANCE` marker from all tests in `tests/test_slugify_acceptance.py`
  (the decorator lines and the `ACCEPTANCE = ...` definition) in the same commit as
  the implementation.
- The plan's phase acceptance line "pytest -q reports 13 passed" becomes
  **21 passed** (6 existing + 7 `test_slugify` + 8 acceptance) once markers are removed.
