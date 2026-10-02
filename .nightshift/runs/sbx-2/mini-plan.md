# Mini-plan sbx-2: count_vowels ignores uppercase vowels

## Cause hypothesis
`count_vowels` in `sandbox_pkg/text.py` tests membership in the lowercase string "aeiou", so uppercase vowels are not counted.

## Failing test to add
In `tests/test_text.py`: `count_vowels("AEIOU") == 5` and a mixed-case case, e.g. `count_vowels("Banana") == 3`. Run the checks and see it fail first.
Commit as `test: failing test for sbx-2`, push.

## Fix
Compare case-insensitively (`ch.lower() in "aeiou"`). Keep the change minimal.

## Files
- sandbox_pkg/text.py
- tests/test_text.py
- README.md (add an uppercase example; also fixes nothing else)

## Checks
`.venv/bin/pytest -q` and `.venv/bin/ruff check .`
