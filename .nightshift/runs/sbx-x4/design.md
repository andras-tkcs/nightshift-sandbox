# Design: sbx-x4 (T2, lite)

Add `titlecase(text)` to `sandbox_pkg/text.py`. It returns a lowercase,
hyphen-separated slug. The name does not match the behaviour (see Risks).

## Modules touched

- `sandbox_pkg/text.py`: add one pure function `titlecase` after
  `count_vowels`. Leave `reverse_words` and `count_vowels` unchanged (non-goal).
- `tests/test_text.py`: add tests for AC-1 to AC-5. Keep using the existing
  flat `def test_*` style and add `titlecase` to the existing import line.
- `README.md`: add a `### titlecase` subsection under `## Usage`, or add the
  call to the existing usage block, with at least one input and its output
  (AC-7). Example: `titlecase("Hello, World!")   # "hello-world"`.
- `sandbox_pkg/__init__.py`, `pyproject.toml`: no change (AC-8).

## Interfaces

```python
def titlecase(text):
    """Return text as a lowercase slug: runs of non-alphanumeric characters
    become one hyphen, with no leading or trailing hyphen."""
```

- Input `str`, output `str`. No type hints, to match the module style.
- Suggested algorithm, standard library only, no `re` needed:
  1. Map each character `ch` to `ch.lower()` if `ch.isalnum()`, else to `" "`.
  2. `"-".join(mapped.split())`.
  `split()` with no argument drops empty pieces, so runs collapse (AC-2),
  edges are stripped (AC-3) and all-separator input gives `""` (AC-4).
  `isalnum()` keeps Unicode letters and digits, so `"ÉTÉ"` becomes `"été"` (AC-5).
- An equivalent `re.sub(r"[^\w]+|_+", ...)` is allowed but not preferred.
  `\w` matches `_`, which AC-2 says is a separator, so it would need special
  handling.

## Data

None. No files, schemas or migrations.

## Risks

- Name and behaviour do not match. The function slugifies text and does not
  title-case it. We keep the requested name `titlecase` as instructed. Open
  question for the owner: rename to `slugify` (perhaps keeping `titlecase` as an
  alias), or keep `titlecase`? This is a public-name decision and stays open.
- `str.lower()` can change string length for a few characters, for example
  `"İ".lower()` gives `"i̇"` with a combining mark. Unicode normalisation is a
  non-goal, so we accept this and do not test it.
- `isalnum()` is true for some characters that are not ASCII digits, for
  example `"²"`. That matches the assumption in acceptance.md ("letters and
  digits kept"), so no special case.
- AC-8 diffs against `origin/main`, but the profile's `git.base_branch` is
  `e2e/20261002-5`. The verifier should use the run's real base branch.
  Either way, `pyproject.toml` must not change.
- README already has a typo ("recieve"). Out of scope, so leave it.

## Rejected alternatives

- Implement real title casing to match the name: contradicts AC-1 to AC-5.
- Rename to `slugify` now: the request says to keep the name. That is the
  owner's call (open question above).
- `unicodedata` normalisation or ASCII transliteration: listed as non-goals.
- Separate module `sandbox_pkg/slug.py`: the request names `text.py`.
