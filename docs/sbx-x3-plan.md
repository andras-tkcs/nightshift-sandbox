# Plan sbx-x3: `word_count` and `clamp`

Run sbx-x3, tier T3 (owner override; size alone is T1). Inputs: `.nightshift/runs/sbx-x3/acceptance.md`, `design.md`, `adr-nan-policy.md`, `research.md`.

**Phase structure (option A) and a deviation for the owner at gate 1.** The request and `design.md` describe two phases, each adding its own README line. This plan has three phases instead:

- `p1-word-count` and `p2-clamp` are the two function phases. They stay fully independent: neither depends on the other, their `touches` are disjoint, and they run in parallel in one wave (AC-9).
- `p3-retire` exists only to satisfy plan-manifest rules 3 and 7. Rule 3 forbids two parallel phases sharing a path in `touches`, so both phases cannot edit `README.md`. Rule 7 requires a last retirement phase that depends on every other phase and deletes this plan. So both README edits (the two import names and the two example lines, AC-7) move into `p3-retire`.

Consequence for the owner: neither function phase on its own updates the README, so reverting one function after merge means also reverting its README line by hand. **Owner: confirm or reject this deviation from "two phases, each adds its own README line" at gate 1.**

## Goal

Users of `sandbox_pkg` get two new helpers: `word_count(text)` in `sandbox_pkg/text.py`, which counts whitespace-separated words, and `clamp(value, low, high)` in `sandbox_pkg/numbers.py`, which limits a number to an inclusive range and raises `ValueError` instead of returning a silently wrong answer when the range is reversed or any argument is NaN. Both are tested and documented in the README Usage block. There is no issue link; the request came as text through the conductor.

## Current state

- `sandbox_pkg/text.py:4-6` `reverse_words(text)` uses `text.split()`, which defines a "word" today. `sandbox_pkg/text.py:9-11` `count_vowels(text)`. Style: plain functions, one-line `"""Return ..."""` docstrings, no type hints, two blank lines between functions.
- `sandbox_pkg/numbers.py:4-9` `mean(values)` raises `ValueError("mean() of an empty sequence")`. That is the module's error convention: `ValueError` with a message naming the function.
- `tests/test_text.py:1` imports `count_vowels, reverse_words` (alphabetical); four tests named `test_<func>_<case>`.
- `tests/test_numbers.py:1-3` imports `pytest` and `mean`; `test_mean_empty` uses `pytest.raises(ValueError)`.
- `README.md:10-17` Usage block: one import line per module, then one example per function with the result as a comment starting at column 25 (0-based; `reverse_words("a b c")` is 22 characters followed by 3 spaces). Line 10 is the opening fence ```python, line 17 the closing fence ```; lines 11-16 read exactly:

```text
from sandbox_pkg.text import reverse_words, count_vowels
from sandbox_pkg.numbers import mean

reverse_words("a b c")   # "c b a"
count_vowels("banana")   # 3
mean([1, 2, 3])          # 2.0
```
- `sandbox_pkg/__init__.py` is empty. No CHANGELOG, no `docs/` directory, no ADR directory (the profile sets no `docs.adr_dir`).
- Checks (resolved profile `checks`, via `ns profile show`; equivalent to the CLAUDE.md commands `.venv/bin/ruff check .` and `.venv/bin/pytest -q`): `.venv/bin/python -m ruff check .` and `.venv/bin/python -m pytest -q`. CI `.github/workflows/tests.yml` runs the same on Python 3.12; `pyproject.toml` requires Python >= 3.10.

## Design

All decisions come from `design.md` and `adr-nan-policy.md`; the conductor restated the settled points for this run: NaN raises `ValueError`, infinities are allowed, punctuation-only tokens count as words.

### D1 `word_count`

Insert in `sandbox_pkg/text.py` directly after `reverse_words` (before `count_vowels`):

```python
def word_count(text):
    """Return the number of whitespace-separated words in text."""
    return len(text.split())
```

`""` and whitespace-only text give 0. Punctuation-only tokens such as `"-"` count as words. No Unicode segmentation.

### D2 `clamp`

Append in `sandbox_pkg/numbers.py` after `mean`, with two blank lines before it:

```python
def clamp(value, low, high):
    """Return value limited to the inclusive range [low, high]."""
    if value != value or low != low or high != high:  # noqa: PLR0124
        raise ValueError("clamp() argument is NaN")
    if low > high:
        raise ValueError("clamp() low is greater than high")
    if value < low:
        return low
    if value > high:
        return high
    return value
```

- The NaN check comes first, because every comparison with NaN is False and a NaN bound would otherwise pass the `low > high` check.
- `x != x` is the NaN test: no import, works for int and float. `math.isnan` is rejected (needs an import, raises `TypeError` on some types).
- The `# noqa: PLR0124` comment is required: the resolved ruff settings for this repo enable PLR0124 (comparison-with-itself), which flags the `x != x` idiom; checked by the planner on 2026-10-02 with ruff 0.16.10 from `.venv`: `ruff check --show-settings` lists PLR0124 with no ruff config in the repo, and `ruff check` on the D2 code without the comment fails with three PLR0124 errors, so the rule is in this ruff version's defaults. Keep the comment exactly as written.
- The selected argument object is returned unchanged: int in, int out; `clamp(2.5, 0.0, 1.0)` is `1.0`; `clamp(7, 4, 4)` is `4`.
- Infinities are accepted: `clamp(float("inf"), 0, 10)` is `10`, `clamp(float("-inf"), 0, 10)` is `0`.
- Rejected: `max(low, min(value, high))` without guards (silent, order-dependent with NaN); swapping reversed bounds (hides caller bugs); NaN propagation as in NumPy `clip` (contradicts the user story and the `mean()` precedent; see `adr-nan-policy.md`).

### D3 Tests

`tests/test_text.py`: change line 1 to `from sandbox_pkg.text import count_vowels, reverse_words, word_count` and append:

```python
def test_word_count():
    assert word_count("the quick brown fox") == 4


def test_word_count_empty():
    assert word_count("") == 0


def test_word_count_whitespace_only():
    assert word_count("  \t\n ") == 0


def test_word_count_mixed_whitespace():
    assert word_count("  one\ttwo\nthree  ") == 3


def test_word_count_punctuation():
    assert word_count("it's a-b - c") == 4
```

`tests/test_numbers.py`: change line 3 to `from sandbox_pkg.numbers import clamp, mean` and append:

```python
def test_clamp_inside():
    assert clamp(5, 0, 10) == 5


def test_clamp_below():
    assert clamp(-3, 0, 10) == 0


def test_clamp_above():
    assert clamp(15, 0, 10) == 10


def test_clamp_on_bounds():
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10


def test_clamp_equal_bounds():
    assert clamp(7, 4, 4) == 4


def test_clamp_float():
    assert clamp(2.5, 0.0, 1.0) == 1.0


def test_clamp_int_stays_int():
    assert type(clamp(15, 0, 10)) is int


def test_clamp_infinity():
    assert clamp(float("inf"), 0, 10) == 10
    assert clamp(float("-inf"), 0, 10) == 0


def test_clamp_low_greater_than_high():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)


def test_clamp_nan_value():
    with pytest.raises(ValueError):
        clamp(float("nan"), 0, 10)


def test_clamp_nan_low():
    with pytest.raises(ValueError):
        clamp(5, float("nan"), 10)


def test_clamp_nan_high():
    with pytest.raises(ValueError):
        clamp(5, 0, float("nan"))
```

Each function phase adds its tests in the same phase as the code (CLAUDE.md: "add a test for every change").

### D4 README Usage block

After `p3-retire`, `README.md` lines 11-18 (between the fences at lines 10 and 19) read exactly (comments start at column 25: `word_count("a b  c")` is followed by 5 spaces, `clamp(15, 0, 10)` by 9 spaces):

```python
from sandbox_pkg.text import reverse_words, count_vowels, word_count
from sandbox_pkg.numbers import mean, clamp

reverse_words("a b c")   # "c b a"
count_vowels("banana")   # 3
word_count("a b  c")     # 3
mean([1, 2, 3])          # 2.0
clamp(15, 0, 10)         # 10
```

The prose paragraph at `README.md:5-6`, including the typo "recieve", stays unchanged (non-goal).

## ADRs

None committed to the repo. The profile sets no `docs.adr_dir`, so there is no ADR directory or numbering. The decision "clamp raises `ValueError` on NaN and on reversed bounds; infinities pass" is recorded in the unnumbered draft `.nightshift/runs/sbx-x3/adr-nan-policy.md` and in D2. If the owner names an ADR directory at gate 1, the plan is revised to add the ADR to `p3-retire`.

## Manual steps

None. `manual_before` and `manual_after` are empty and there is no `RUN/manual-steps.md`. Everything is checked by pytest, ruff, grep and CI.

## Risks and open questions

- **Owner decision (gate 1): phase structure.** See the deviation note at the top: README edits are in `p3-retire`, not in each function phase.
- **Owner confirmation (gate 1): behaviour.** NaN raises `ValueError` (not propagation), infinities are accepted, punctuation-only tokens count. These come from the design, the ADR draft and the conductor's instructions. If the owner chooses NaN propagation, D2, `test_clamp_nan_*` and AC-5 change, and the plan must be revised before any phase runs.
- **AC-8 base ref.** `acceptance.md` says `git diff origin/main -- pyproject.toml`; this run's base branch is `e2e/20261002-4` (profile `git.base_branch`). The `p3-retire` acceptance diffs against `e2e/20261002-4` (or `origin/e2e/20261002-4` when the local ref is missing). No phase lists `pyproject.toml` in `touches`, so either base gives the same answer.
- **Stop conditions for workers.** Stop with `status=blocked` and do not improvise if: `sandbox_pkg/text.py` or `sandbox_pkg/numbers.py` already defines `word_count` or `clamp`; the existing test lines named in D3 (`tests/test_text.py:1`, `tests/test_numbers.py:3`) differ from what Current state describes; an existing test fails before your change; ruff reports a rule violation in the code given verbatim in D1-D3 (that means the plan is wrong); in `p3-retire`, `README.md` lines 10-17 differ from the block in Current state.
- `x != x` on exotic types with an unusual `__ne__` is unspecified; non-numeric inputs are out of scope.

## Implementation manifest

```yaml
plan_slug: sbx-x3
feature_branch: feature/sbx-x3
max_parallel: 2
manual_before: []
manual_after: []
verify_after_merge:
  - ".venv/bin/python -m ruff check ."
  - ".venv/bin/python -m pytest -q"
final_checks:
  - "docs/sbx-x3-plan.md is deleted"
  - "grep -cF -e 'word_count(\"a b  c\")     # 3' -e 'clamp(15, 0, 10)         # 10' -e 'from sandbox_pkg.text import reverse_words, count_vowels, word_count' -e 'from sandbox_pkg.numbers import mean, clamp' README.md prints 4"
  - "pyproject.toml is unchanged against the base branch e2e/20261002-4"
  - "no CHANGELOG exists in the repo, so no changelog entry is required"
phases:
  - id: p1-word-count
    title: Add word_count(text) to sandbox_pkg/text.py with tests
    depends_on: []
    complexity: S
    touches:
      - sandbox_pkg/text.py
      - tests/test_text.py
    brief: |
      Read docs/sbx-x3-plan.md sections "Design D1" and "Design D3" first. Do not edit README.md, sandbox_pkg/numbers.py or tests/test_numbers.py.
      1. Confirm sandbox_pkg/text.py has no word_count and tests/test_text.py line 1 is "from sandbox_pkg.text import count_vowels, reverse_words". If not, stop with status=blocked.
      2. Run ".venv/bin/python -m pytest -q"; if any existing test fails, stop with status=blocked.
      3. In sandbox_pkg/text.py insert the function word_count exactly as in Design D1, directly after reverse_words and before count_vowels, with two blank lines on each side.
      4. In tests/test_text.py change line 1 to "from sandbox_pkg.text import count_vowels, reverse_words, word_count".
      5. Append the five test functions from Design D3 (test_word_count, test_word_count_empty, test_word_count_whitespace_only, test_word_count_mixed_whitespace, test_word_count_punctuation) to tests/test_text.py, two blank lines between functions.
      6. Run ".venv/bin/python -m ruff check ." and ".venv/bin/python -m pytest -q"; both must pass. If ruff flags the verbatim code from the plan, stop with status=blocked.
      7. Make exactly one commit, with message "Add word_count to sandbox_pkg.text".
    acceptance:
      - ".venv/bin/python -m pytest -q tests/test_text.py passes, including test_word_count, test_word_count_empty, test_word_count_whitespace_only, test_word_count_mixed_whitespace, test_word_count_punctuation"
      - ".venv/bin/python -m pytest -q -k word_count selects 5 tests and all pass"
      - "the AC-1 Check command in .nightshift/runs/sbx-x3/acceptance.md, run verbatim, prints '4 3 2'"
      - "the AC-2 Check command in .nightshift/runs/sbx-x3/acceptance.md, run verbatim, prints '0 0'"
      - "grep -c '^def word_count(text):' sandbox_pkg/text.py prints 1"
      - ".venv/bin/python -m ruff check . exits 0"
      - ".venv/bin/python -m pytest -q exits 0"
      - "git diff --name-only HEAD~1 HEAD prints exactly sandbox_pkg/text.py and tests/test_text.py"
  - id: p2-clamp
    title: Add clamp(value, low, high) to sandbox_pkg/numbers.py with tests
    depends_on: []
    complexity: S
    touches:
      - sandbox_pkg/numbers.py
      - tests/test_numbers.py
    brief: |
      Read docs/sbx-x3-plan.md sections "Design D2" and "Design D3" first. Do not edit README.md, sandbox_pkg/text.py or tests/test_text.py.
      1. Confirm sandbox_pkg/numbers.py has no clamp and tests/test_numbers.py line 3 is "from sandbox_pkg.numbers import mean". If not, stop with status=blocked.
      2. Run ".venv/bin/python -m pytest -q"; if any existing test fails, stop with status=blocked.
      3. Append the function clamp exactly as in Design D2 to sandbox_pkg/numbers.py after mean, with two blank lines before it, including the trailing comment "# noqa: PLR0124" on the NaN check line. Keep the check order: NaN check first, then low > high, then the comparisons. Do not import math.
      4. In tests/test_numbers.py change line 3 to "from sandbox_pkg.numbers import clamp, mean".
      5. Append the twelve test functions from Design D3 (test_clamp_inside through test_clamp_nan_high) to tests/test_numbers.py, two blank lines between functions.
      6. Run ".venv/bin/python -m ruff check ." and ".venv/bin/python -m pytest -q"; both must pass. If ruff flags the verbatim code from the plan, stop with status=blocked.
      7. Make exactly one commit, with message "Add clamp to sandbox_pkg.numbers".
    acceptance:
      - ".venv/bin/python -m pytest -q tests/test_numbers.py passes, including test_clamp_low_greater_than_high, test_clamp_nan_value, test_clamp_nan_low, test_clamp_nan_high"
      - ".venv/bin/python -m pytest -q -k clamp selects 12 tests and all pass"
      - "the AC-3 Check command in .nightshift/runs/sbx-x3/acceptance.md, run verbatim, prints '5 0 10 0 10 1.0 4'"
      - ".venv/bin/python -c 'from sandbox_pkg.numbers import clamp; clamp(5, 10, 0)' exits non-zero and stderr contains 'ValueError: clamp() low is greater than high'"
      - "each of clamp(float('nan'), 0, 10), clamp(5, float('nan'), 10), clamp(5, 0, float('nan')) run via .venv/bin/python -c exits non-zero and stderr contains 'ValueError: clamp() argument is NaN'"
      - "! grep -q 'import math' sandbox_pkg/numbers.py exits 0"
      - ".venv/bin/python -m ruff check . exits 0"
      - ".venv/bin/python -m pytest -q exits 0"
      - "git diff --name-only HEAD~1 HEAD prints exactly sandbox_pkg/numbers.py and tests/test_numbers.py"
  - id: p3-retire
    title: Document both functions in the README and retire the plan
    depends_on: [p1-word-count, p2-clamp]
    complexity: S
    touches:
      - README.md
      - docs/sbx-x3-plan.md
    brief: |
      Read docs/sbx-x3-plan.md section "Design D4" first. This phase only edits README.md and deletes the plan.
      1. Confirm sandbox_pkg/text.py defines word_count and sandbox_pkg/numbers.py defines clamp, and README.md lines 10-17 match the Usage block in the plan's "Current state". If not, stop with status=blocked.
      2. In README.md change line 11 to "from sandbox_pkg.text import reverse_words, count_vowels, word_count".
      3. In README.md change line 12 to "from sandbox_pkg.numbers import mean, clamp".
      4. Insert the line 'word_count("a b  c")     # 3' directly after the count_vowels example line (5 spaces before "#", so "#" is at column 25 like the existing lines).
      5. Insert the line 'clamp(15, 0, 10)         # 10' directly after the mean example line (9 spaces before "#").
      6. Do not change any other README line, including the typo "recieve".
      7. Delete docs/sbx-x3-plan.md with "git rm docs/sbx-x3-plan.md". If docs/ is then empty, leave it absent.
      8. Run ".venv/bin/python -m ruff check ." and ".venv/bin/python -m pytest -q"; both must pass.
      9. Make exactly one commit, with message "Document word_count and clamp in README; retire sbx-x3 plan".
    acceptance:
      - "grep -n 'from sandbox_pkg.text import reverse_words, count_vowels, word_count' README.md prints one line"
      - "grep -n 'from sandbox_pkg.numbers import mean, clamp' README.md prints one line"
      - "grep -nF 'word_count(\"a b  c\")     # 3' README.md prints one line"
      - "grep -nF 'clamp(15, 0, 10)         # 10' README.md prints one line"
      - ".venv/bin/python -c 'from sandbox_pkg.text import word_count; from sandbox_pkg.numbers import clamp; print(word_count(\"a b  c\"), clamp(15, 0, 10))' prints '3 10' (the two README example lines evaluated)"
      - "grep -c recieve README.md prints 1"
      - "git diff --numstat HEAD~1 HEAD -- README.md prints '4<TAB>2<TAB>README.md' (2 lines changed, 2 lines added)"
      - "test ! -e docs/sbx-x3-plan.md exits 0"
      - "git diff --name-only HEAD~1 HEAD prints exactly README.md and docs/sbx-x3-plan.md"
      - "git diff --quiet e2e/20261002-4 -- pyproject.toml exits 0 (use origin/e2e/20261002-4 if the local ref is missing)"
      - ".venv/bin/python -m ruff check . exits 0"
      - ".venv/bin/python -m pytest -q exits 0"
```
