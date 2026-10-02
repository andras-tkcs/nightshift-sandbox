# Acceptance: sbx-x3

Goal: add `word_count(text)` to `sandbox_pkg/text.py` and `clamp(value, low, high)` to `sandbox_pkg/numbers.py`, each with tests and a README usage line, delivered as two phases that do not depend on each other.

## User stories

- As a user of `sandbox_pkg` I want `word_count(text)` so that I can count the whitespace-separated words in a string.
- As a user of `sandbox_pkg` I want `clamp(value, low, high)` so that I can limit a number to a range and get an error instead of a silent wrong answer when the range or input is invalid.
- As a maintainer I want each function shipped as its own phase so that either can be merged or reverted without the other.

## Acceptance criteria

All commands run from the repository root.

AC-1 `word_count` counts whitespace-separated words, the same notion of "word" as `reverse_words`.
Check: `.venv/bin/python -c 'from sandbox_pkg.text import word_count as w; print(w("the quick brown fox"), w("  one\ttwo\nthree  "), w("it'"'"'s a-b"))'` prints `4 3 2`.

AC-2 `word_count` returns 0 for empty and whitespace-only text.
Check: `.venv/bin/python -c 'from sandbox_pkg.text import word_count as w; print(w(""), w("  \t\n "))'` prints `0 0`.

AC-3 `clamp` returns the value when it lies within `[low, high]` (bounds inclusive), `low` when below, `high` when above, for ints and floats, and works when `low == high`.
Check: `.venv/bin/python -c 'from sandbox_pkg.numbers import clamp as c; print(c(5,0,10), c(-3,0,10), c(15,0,10), c(0,0,10), c(10,0,10), c(2.5,0.0,1.0), c(7,4,4))'` prints `5 0 10 0 10 1.0 4`.

AC-4 `clamp` raises `ValueError` when `low > high`.
Check: `.venv/bin/python -c 'from sandbox_pkg.numbers import clamp; clamp(5, 10, 0)'` exits non-zero with `ValueError` in stderr.

AC-5 `clamp` raises `ValueError` when any argument is NaN (value, low or high).
Check: each of `clamp(float("nan"), 0, 10)`, `clamp(5, float("nan"), 10)`, `clamp(5, 0, float("nan"))` run via `.venv/bin/python -c 'from sandbox_pkg.numbers import clamp; ...'` exits non-zero with `ValueError` in stderr.

AC-6 Tests cover the new behaviour: `tests/test_text.py` has at least one test calling `word_count` including the empty/whitespace-only case, and `tests/test_numbers.py` has tests calling `clamp` including a `pytest.raises(ValueError)` case for `low > high` and for NaN.
Check: `grep -n word_count tests/test_text.py` and `grep -n -e clamp -e 'raises(ValueError)' tests/test_numbers.py` show these tests; `.venv/bin/pytest -q -k "word_count or clamp"` passes with at least 1 selected test per function.

AC-7 README Usage block documents both functions: the text import line includes `word_count`, the numbers import line includes `clamp`, and there is one example line per function with its result as a comment.
Check: `grep -n -e 'word_count' -e 'clamp' README.md` shows the two import lines and one example each, e.g. `word_count("a b  c")  # 3` and `clamp(15, 0, 10)  # 10`; running each example line in `.venv/bin/python` gives the commented result.

AC-8 The full suite and lint pass, and no dependency is added.
Check: `.venv/bin/pytest -q` exits 0 with no failures; `.venv/bin/ruff check .` exits 0; `git diff origin/main -- pyproject.toml` shows no change to `dependencies` or `optional-dependencies`.

AC-9 The two phases are independent: the word_count phase changes no code in `sandbox_pkg/numbers.py` or `tests/test_numbers.py`, the clamp phase changes no code in `sandbox_pkg/text.py` or `tests/test_text.py`, and neither phase lists the other as a dependency in the plan.
Check: per-phase `git diff --name-only` for each phase's commits; plan shows no dependency edge between the two phases.

## Non-goals

- Existing functions `reverse_words`, `count_vowels` and `mean` and their tests stay unchanged.
- No fixing of the README typo "recieve".
- No Unicode word segmentation or punctuation stripping in `word_count`; punctuation-only tokens such as `"-"` count as words.
- No swapping of reversed bounds or NaN propagation in `clamp`.
- No re-exports in `sandbox_pkg/__init__.py`, no type hints required, no new dependencies.

## Assumptions

- "Word" means a token from `str.split()` with no separator (research recommendation; consistent with `reverse_words`).
- `clamp` bounds are inclusive; `low == high` is valid and returns that bound.
- NaN policy is raise `ValueError` (research recommendation, following the `mean` precedent), not IEEE propagation.
- Non-numeric arguments (e.g. strings, None) are out of scope; behaviour for them is unspecified.
- `clamp` returns the argument object it selects, so `clamp(2.5, 0.0, 1.0)` is `1.0` and int inputs give int results.
- A README merge conflict between the phases in the Usage block is acceptable and expected to be trivial.

## Open questions

- NaN policy: a reviewer may prefer propagation (return NaN, like NumPy `clip`). This file assumes raise; change AC-5 if the owner decides otherwise.
- Should `word_count` ignore punctuation-only tokens? Assumed no.
- Should `clamp` reject infinities? Assumed no: `clamp(float("inf"), 0, 10)` returns `10`.
