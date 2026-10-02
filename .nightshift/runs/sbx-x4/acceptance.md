# Acceptance: sbx-x4 (T2, lite)

Goal: `sandbox_pkg.text.titlecase(text)` returns a lowercase, hyphen-separated slug of `text`, with tests and a README section.

1. AC-1: `from sandbox_pkg.text import titlecase` succeeds; `titlecase("Hello World")` returns `"hello-world"` and `titlecase("Hello, World!")` returns `"hello-world"` (checked by a pytest test in `tests/`).
2. AC-2: Any run of spaces and/or punctuation becomes exactly one hyphen: `titlecase("a  ,-;  b")` returns `"a-b"` and `titlecase("a_b.c")` returns `"a-b-c"`.
3. AC-3: No leading or trailing hyphen: `titlecase("  --Hi there!!  ")` returns `"hi-there"`.
4. AC-4: Degenerate input: `titlecase("")` returns `""` and `titlecase("!?  ...")` returns `""`.
5. AC-5: Letters and digits are kept, lowercased: `titlecase("Version 2 ÉTÉ")` returns `"version-2-été"`.
6. AC-6: `.venv/bin/pytest -q` passes with tests covering AC-1 to AC-5, and `.venv/bin/ruff check .` reports no errors.
7. AC-7: `README.md` has a section showing `titlecase` usage with an input and its expected output.
8. AC-8: No new dependencies: `git diff origin/main... -- pyproject.toml` shows no change to dependency lists.

## Assumptions

- The name `titlecase` does not match the slug behaviour asked for. We follow the spec text and keep the name as requested. Open question for the owner: rename to `slugify`, or keep `titlecase`?
- "Punctuation" means any character that is not a letter or digit (`str.isalnum()` is false), including `_`, `-` and other whitespace such as tabs. Non-ASCII letters count as letters and are kept, lowercased.

## Non-goals

- Actual title casing ("Hello World" style output).
- Transliterating non-ASCII to ASCII, or Unicode normalisation.
- Changes to `reverse_words`, `count_vowels` or `sandbox_pkg/numbers.py`.
