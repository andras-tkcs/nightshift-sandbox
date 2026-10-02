# Design: sbx-x3 (word_count and clamp)

Two independent phases (AC-9). Reuse existing patterns only; no new modules, no dependencies (AC-8, CLAUDE.md).

## Modules touched

Phase A, `word_count` (AC-1, AC-2, AC-6, AC-7):
- `sandbox_pkg/text.py`: add `word_count` after `reverse_words`.
- `tests/test_text.py`: add `test_word_count_*` tests.
- `README.md`: add `word_count` to the text import line and one example line.

Phase B, `clamp` (AC-3, AC-4, AC-5, AC-6, AC-7):
- `sandbox_pkg/numbers.py`: add `clamp` after `mean`.
- `tests/test_numbers.py`: add `clamp` to the import and `test_clamp_*` tests.
- `README.md`: add `clamp` to the numbers import line and one example line.

Not touched: `sandbox_pkg/__init__.py`, `pyproject.toml`, existing functions and tests.

## Interfaces

- `word_count(text)` returns `int`: `len(text.split())`. Same notion of "word" as `reverse_words`. One-line docstring "Return ...", no type hints (matches module style).
- `clamp(value, low, high)` returns the argument object it selects (`value`, `low` or `high`); int in, int out.
  Check order, all before comparing:
  1. any argument is NaN -> `ValueError("clamp() argument is NaN")` (AC-5);
  2. `low > high` -> `ValueError("clamp() low is greater than high")` (AC-4);
  3. `value < low` -> `low`; `value > high` -> `high`; else `value` (AC-3).
  NaN test: `x != x` (no import; works for int, float, Decimal). Message names the function, following `mean()`.
  Infinities pass through (acceptance assumption).
- README example lines: `word_count("a b  c")  # 3`, `clamp(15, 0, 10)  # 10`, aligned with the existing comment column.

## Data

None. No files, schemas or migrations.

## Risks

- README Usage block is edited by both phases: expect a trivial merge conflict (accepted in acceptance.md). Mitigation: each phase edits only its own import line and appends its example on its own line.
- NaN check must run before `low > high`, because comparisons with NaN are always False and would let a NaN bound through silently (research.md).
- `x != x` on exotic types with odd `__ne__` is unspecified; non-numeric inputs are out of scope.

## Rejected alternatives

- `max(low, min(value, high))` without guards: silent, order-dependent NaN results (research.md).
- Swapping reversed bounds: hides caller bugs; non-goal.
- NaN propagation (NumPy `clip` style): see ADR draft `adr-nan-policy.md`; open question for the owner.
- `math.isnan`: raises `TypeError` on non-float-like types and needs an import; `x != x` is enough.
- Re-exporting from `sandbox_pkg/__init__.py`: non-goal.

## Open questions (owner)

- NaN policy: raise (assumed, AC-5) vs propagate.
- Reject infinities in `clamp`? Assumed no.
- Punctuation-only tokens in `word_count`? Assumed they count.
