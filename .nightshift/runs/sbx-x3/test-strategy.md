# Test strategy: sbx-x3

Inputs: `acceptance.md` (AC-1 to AC-9), `design.md`, `adr-nan-policy.md`, `docs/sbx-x3-plan.md` (phases p1-word-count, p2-clamp, p3-retire).

Acceptance tests: `tests/test_acceptance_sbx_x3.py` (new file; existing test files untouched). Marker on every test: `pytest.mark.xfail(strict=True, reason="ns:sbx-x3 acceptance")`, bound to the module constant `ACCEPTANCE`. Functions are imported inside each test so collection succeeds before they exist.

## Pyramid

- Unit: 24 test cases (11 test functions, parametrized). Pure functions, no I/O, no clock. Covers AC-1 to AC-5.
- Integration: 2 tests (AC-7) that read the real `README.md`, extract the ```` ```python ```` Usage block, check the import lines and evaluate each example line against its `# result` comment.
- End to end: none. The package is a library with no user-visible flow beyond calling the functions; the AC Check commands (`python -c ...`) serve as the smoke check and are run by the phase acceptance in the plan.

The phase test files written by p1/p2 (`tests/test_text.py`, `tests/test_numbers.py`, per plan D3) are a second, independent set of unit tests; AC-6 requires them there and they are checked by command, not by this file.

## AC to test map

| AC | Proven by | Marker removed by |
|----|-----------|-------------------|
| AC-1 | `test_ac1_word_count_counts_words` (4 cases incl. `"it's a-b"` -> 2 and punctuation-only token), `test_ac1_word_count_matches_reverse_words` | p1-word-count |
| AC-2 | `test_ac2_word_count_empty_is_zero` (`""`, `"  \t\n "`) | p1-word-count |
| AC-3 | `test_ac3_clamp_limits_value` (9 cases incl. inclusive bounds, float, `low == high`, infinities; also asserts result type, so int in gives int out), `test_ac3_clamp_check_command_output` (exact `"5 0 10 0 10 1.0 4"`) | p2-clamp |
| AC-4 | `test_ac4_clamp_reversed_bounds_raises` | p2-clamp |
| AC-5 | `test_ac5_clamp_nan_raises` (value, low, high, both bounds) | p2-clamp |
| AC-6 | Command: `grep -n word_count tests/test_text.py`; `grep -n -e clamp -e 'raises(ValueError)' tests/test_numbers.py`; `.venv/bin/pytest -q -k "word_count or clamp"` exits 0. (Tests about the existence of tests in other files are not written as tests.) | n/a |
| AC-7 | `test_ac7_readme_documents_word_count`, `test_ac7_readme_documents_clamp` (import line contains the name; exactly one example line; evaluated result equals the comment). Plus the plan's p3 grep commands. | p3-retire |
| AC-8 | Command: `.venv/bin/pytest -q` exits 0; `.venv/bin/ruff check .` exits 0; `git diff e2e/20261002-4 -- pyproject.toml` empty | n/a |
| AC-9 | Command: per-phase `git diff --name-only HEAD~1 HEAD`; manifest shows no `depends_on` edge between p1 and p2 | n/a |

## Fixtures

None. Inputs are literals in `parametrize`; the README is read from the repository root via `Path(__file__)`. No new conftest.

## Verification at write time

- `.venv/bin/pytest -q`: `6 passed, 24 xfailed`; no errors, no XPASS.
- `.venv/bin/ruff check .`: all checks passed.
- With the plan's D1/D2/D4 code applied in a scratch copy outside the repository and the markers removed: all 24 tests pass. Before that, the AC-7 tests fail on the README assertion (README is checked before the imports), and AC-1 to AC-5 fail because the function does not exist yet.

## Notes for the phases

- The marker is per test (decorator `@ACCEPTANCE`); each phase deletes the decorator lines of exactly its tests (see table).
- `tests/test_acceptance_sbx_x3.py` is edited by p1, p2 (in parallel) and p3, but is not in any phase's `touches`. The edits are on disjoint lines (p1 the `test_ac1_*`/`test_ac2_*` decorators, p2 the `test_ac3_*` to `test_ac5_*` ones), so a merge should be clean, but under plan-manifest rule 3 the conductor should either add the file to the touches or accept it explicitly.
