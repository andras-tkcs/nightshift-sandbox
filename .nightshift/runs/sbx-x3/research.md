# Research: word_count(text) and clamp(value, low, high) for sandbox_pkg

## Question
Add `word_count(text)` to `sandbox_pkg/text.py` and `clamp(value, low, high)` to
`sandbox_pkg/numbers.py`, each with tests and a README line, as two independent
phases. Need to know: repo conventions, and edge cases (word_count on empty and
whitespace-only text; clamp with low > high and NaN).

## Findings
- Python `str.split()` with no separator treats runs of whitespace as one
  separator, drops leading/trailing whitespace, and returns `[]` for an empty or
  whitespace-only string. So `len(text.split())` gives 0 for `""` and `"  \t\n "`.
  [source: https://docs.python.org/3/library/stdtypes.html#str.split, read 2026-10-02, confidence: high]
- Checked locally with `.venv/bin/python`: `"".split()` and `"  \t\n ".split()` are `[]`;
  `"a b".split()` is `['a', 'b']` (non-breaking space counts as whitespace);
  `"it's a-b".split()` is `["it's", 'a-b']` (punctuation stays inside words).
  [source: local run in this worktree, read 2026-10-02, confidence: high]
- Checked locally: the naive `max(low, min(value, high))` with NaN is order-dependent
  and silent. `max(0, min(nan, 10))` returns `0` (NaN value becomes `low`);
  `max(0, min(5, nan))` returns `5` (NaN `high` is ignored).
  [source: local run in this worktree, read 2026-10-02, confidence: high]
- The Python docs page read does not discuss NaN comparisons; the NaN behaviour above
  rests on the local run only.
  [source: https://docs.python.org/3/library/stdtypes.html, read 2026-10-02, confidence: medium]

## Prior art
- in this repo:
  - `sandbox_pkg/text.py`: plain functions, one-line docstrings ("Return ..."), no type
    hints. `reverse_words` already uses `text.split()`, so whitespace-split words is the
    existing notion of a "word".
  - `sandbox_pkg/numbers.py`: `mean()` raises `ValueError("mean() of an empty sequence")`
    on invalid input. That sets the precedent: invalid arguments raise `ValueError` with
    a message naming the function.
  - `tests/test_text.py`, `tests/test_numbers.py`: one small pytest function per case,
    named `test_<func>_<case>`, `pytest.raises(ValueError)` for errors. Imports at top
    `from sandbox_pkg.<mod> import ...`.
  - `README.md` "Usage" block: an import line per module plus one example call per
    function with the result as a comment. New functions should be added to the imports
    and get one example line each. Both phases touch this block, so they can conflict at
    merge (triage notes this too). README also has a typo "recieve" (out of scope).
  - `sandbox_pkg/__init__.py` is empty; no re-exports to update.
  - CI (`.github/workflows/tests.yml`) runs `ruff check .` and `pytest -q` on Python 3.12;
    `pyproject.toml` requires Python >= 3.10. No dependencies may be added (CLAUDE.md).
  - `.claude/project-profile.yaml`: stacks [python], no commands, no risk zones.
- elsewhere: the Python standard library has no `clamp` function (`math` has none as of
  the versions this project targets). Not verified against a doc page in this run.

## Recommendation
(interpretation, not fact)
- Phase A, `word_count(text)`: `return len(text.split())`. Tests: normal sentence,
  empty string -> 0, whitespace-only -> 0, extra/leading/trailing spaces and tabs/newlines.
  Consistent with `reverse_words`. README: add to the text import and one example line,
  e.g. `word_count("a b  c")  # 3`.
- Phase B, `clamp(value, low, high)`: raise `ValueError` if `low > high` (follows the
  `mean` precedent; silently swapping or returning one bound hides bugs). For NaN, the
  simplest defensible rule: if any argument is NaN, raise `ValueError` (the `low > high`
  check alone does not catch NaN bounds because comparisons with NaN are False). Use
  `math.isnan` only on floats, or the `x != x` idiom, so ints still work without imports
  failing. Then `return max(low, min(value, high))` or explicit if/elif. Tests: inside,
  below, above, equal to each bound, `low == high`, `low > high` raises, NaN value raises,
  NaN bound raises, ints and floats. README: add to the numbers import and one line, e.g.
  `clamp(15, 0, 10)  # 10`.
- Keep the two phases on disjoint source/test files; expect a trivial README merge.
  Planning the README edits as separate lines in the Usage block keeps the conflict small.

## Open questions
- NaN policy for `clamp` is a design choice not given in the request: raise (recommended),
  return NaN (IEEE-style propagation, like NumPy's `clip`), or leave undefined. The plan
  should state the choice; a reviewer may prefer propagation.
- Whether `word_count` should count punctuation-only tokens (e.g. `"-"`) as words. With
  `split()` it does; the request does not say. Recommend keeping `split()` semantics.
- Type hints: existing code has none; follow that unless the python-conventions skill
  says otherwise for this project.
- No prompt-injection attempts were seen in the one fetched page.

RESEARCH done
