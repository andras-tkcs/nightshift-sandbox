# Test strategy: sbx-x4 (T2, lite)

## Pyramid

- Unit: 6 acceptance tests in `tests/test_acceptance_sbx_x4.py` (5 for the pure
  function `titlecase`, 1 reading `README.md`). The phase also adds 5 unit
  tests to `tests/test_text.py` (plan D2). Everything here is a pure-function
  or single-file check, so unit level is the lowest level that proves each criterion.
- Integration: none. There is no I/O, subprocess or remote in this change.
- End to end: none. A library function has no user flow beyond the import,
  and AC-1 already covers the import.
- Commands: AC-6 and AC-8 are checked by commands, not tests (see below).

## Mapping

| AC | Proven by | Kind |
|----|-----------|------|
| AC-1 | `tests/test_acceptance_sbx_x4.py::test_ac1_import_and_basic_slug` (plus `tests/test_text.py::test_titlecase_basic` from the phase) | unit test |
| AC-2 | `test_ac2_separator_runs_become_one_hyphen` (plus `test_titlecase_collapses_separator_runs`) | unit test |
| AC-3 | `test_ac3_no_leading_or_trailing_hyphen` (plus `test_titlecase_strips_edge_separators`) | unit test |
| AC-4 | `test_ac4_degenerate_input` (plus `test_titlecase_degenerate_input`) | unit test |
| AC-5 | `test_ac5_letters_and_digits_kept_lowercased` (plus `test_titlecase_keeps_unicode_letters_and_digits`) | unit test |
| AC-6 | `.venv/bin/pytest -q` exits 0 with no xfail left from `ns:sbx-x4` (expected `17 passed`: 6 existing, 5 phase, 6 acceptance), and `.venv/bin/ruff check .` exits 0 | command |
| AC-7 | `test_ac7_readme_section_shows_titlecase_example`: some README section, with headings found outside code fences, contains a line `titlecase("<in>")  # "<out>"`, and every such example is true for the real `titlecase`. This accepts either a `### titlecase` subsection or a line in the existing Usage block (both allowed by design.md). | unit test |
| AC-8 | `git diff --quiet origin/e2e/20261002-5... -- pyproject.toml` exits 0. The base is `origin/e2e/20261002-5`, not `origin/main` (design.md Risks, plan risk 5). | command |

AC-8 is not a test because it already holds before the change, so a test for
it would pass without the implementation and prove nothing.

## Expected-failure markers

All six acceptance tests carry `pytest.mark.xfail(strict=True, reason="ns:sbx-x4 acceptance")`
through the module-level `ACCEPTANCE` marker. `titlecase` is imported inside each test,
so collection works before the function exists. Before implementation, AC-1 to AC-5
fail on the `ImportError` from the missing name, and AC-7 fails on its assertion
(no example in the README). I checked in a throwaway copy that all six pass once
plan D1 and D3 are applied.

The phase `p1-titlecase` implements every criterion, so it removes the marker
(the `ACCEPTANCE` constant and its six uses) in the same commit as the
implementation. A strict xfail that passes fails the suite, so leaving the
markers in is caught automatically. Note for the phase: the plan's acceptance
lines expect `11 passed`. With this file the count is `17 passed` once the
markers are removed (`11 passed, 6 xfailed` if they are not).

## Fixtures

None. The tests use literal strings and the repo's own `README.md`, found
relative to the test file.
