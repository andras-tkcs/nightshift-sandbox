# Design: sbx-x2 (lite)

## Approach

Add one pure function `slugify(text)` to the existing module `sandbox_pkg/text.py`,
next to `reverse_words` and `count_vowels`. Use the standard library `re` only
(CLAUDE.md: no new dependencies).

Algorithm, in this order:

1. `text.lower()`: uppercase ASCII becomes lowercase (AC-1).
2. `re.sub(r"[^a-z0-9]+", "-", lowered)`: every run of one or more characters
   that are not ASCII letters or digits, including `_`, spaces and punctuation,
   becomes exactly one hyphen (AC-2, acceptance "Assumptions"). Digits are kept (AC-4).
3. `.strip("-")`: removes a leading or trailing hyphen. An input made only of
   separators, or an empty input, gives `""` (AC-3).

Compile the pattern once at module level (`_NON_ALNUM = re.compile(r"[^a-z0-9]+")`).
Add a one-line docstring in the style of the existing functions.

## Files

- `sandbox_pkg/text.py`: add `import re`, the module-level pattern, and `slugify`.
  `reverse_words` and `count_vowels` stay unchanged.
- `tests/test_text.py`: extend the import to include `slugify`. Add tests whose
  names contain `slugify` (so `-k slugify` selects them, AC-5), one per
  criterion or one parametrized test covering all the AC-1 to AC-4 cases:
  `'Hello World'`, `'Hello,  World!!  Again'`, `'a--b__c..d'`,
  `'  --Hello World!--  '`, `'!!!'`, `''`, `'Python 3.10 Release'`.
  Existing tests are not modified.
- `README.md`: add `slugify` to the intro sentence and to the Usage block, e.g.
  `slugify("Hello World")   # "hello-world"`, or a short `## slugify` section with
  the same example (AC-7). The example must be one of the AC cases so it is
  already verified by a test.
- No change to `pyproject.toml` or `sandbox_pkg/numbers.py`.

## Interfaces

`def slugify(text):` takes a `str` and returns a `str`. No type hints, so it
matches the surrounding functions. Public name, importable as
`from sandbox_pkg.text import slugify`.

## Edge cases

- Empty string and separator-only input return `""` (AC-3).
- `_` counts as a separator because the class is `[^a-z0-9]`, not `\W` (`\W` would keep `_`).
- Mixed separators such as `"a -_. b"` collapse to a single hyphen.
- Non-ASCII letters (`é`) are treated as separators. That is not specified and
  not tested (acceptance "Assumptions" and "Non-goals"). Do not add tests that
  fix this behaviour.
- Calling `.lower()` before matching means the regex never needs `re.IGNORECASE`.
- A non-`str` argument raises `AttributeError` from `.lower()`. That is not
  specified, so no handling is added.

## Risks

- Low. A new function in an existing module, with no I/O and no new dependencies.
- ruff (AC-6): place `import re` at the top of the module, after the docstring.

## Rejected alternatives

- `\W+` / `str.isalnum()`: these keep `_` and accept Unicode letters, which conflicts with
  the acceptance definition of "punctuation".
- Splitting on separators then `"-".join(parts)`: same result, but needs a filter
  for empty parts. The sub-then-strip version is shorter.
- Unicode normalisation or transliteration (`unicodedata`): explicitly a non-goal.

## Note (out of scope)

`README.md` has a typo, "recieve". The implementer may fix it while editing that
paragraph. This is not required by any criterion.
