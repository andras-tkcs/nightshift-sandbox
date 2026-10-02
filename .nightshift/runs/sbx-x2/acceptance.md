# Acceptance: sbx-x2

Goal: `sandbox_pkg.text.slugify(text)` turns a string into a lowercase, hyphen-separated slug with no leading or trailing hyphen, and it has tests and a README section.

## Criteria

- AC-1: `.venv/bin/python -c "from sandbox_pkg.text import slugify; assert slugify('Hello World') == 'hello-world'"` exits 0. Uppercase becomes lowercase and a space becomes a hyphen.
- AC-2: A run of spaces or punctuation becomes one hyphen: `slugify('Hello,  World!!  Again') == 'hello-world-again'` and `slugify('a--b__c..d') == 'a-b-c-d'`.
- AC-3: The result has no leading or trailing hyphen: `slugify('  --Hello World!--  ') == 'hello-world'`, and `slugify('!!!') == ''` and `slugify('') == ''`.
- AC-4: Digits stay as they are: `slugify('Python 3.10 Release') == 'python-3-10-release'`.
- AC-5: `tests/test_text.py` has tests that call `slugify` and check the cases in AC-1 to AC-4. `.venv/bin/pytest -q tests/test_text.py -k slugify` collects at least one test and all of them pass.
- AC-6: `.venv/bin/pytest -q` passes with no failures, and `.venv/bin/ruff check .` reports no errors.
- AC-7: `README.md` has a section that names `slugify`, shows an example call and its result, and the example matches what the function returns. Check: `grep -n slugify README.md` prints at least one line, and running the example gives the documented output.

## Assumptions

- "Punctuation" means every character that is not an ASCII letter or digit, including `_`. Behaviour for non-ASCII letters (for example `é`) is not specified and is not checked here.
- The triage file says T1; the conductor asked for lite mode, so this file uses the lite format.
- `slugify` is a pure function with no new dependencies (CLAUDE.md), so the standard library (`re`) is enough.

## Non-goals

- No Unicode transliteration (`é` to `e`) and no maximum slug length.
- `reverse_words`, `count_vowels` and `sandbox_pkg/numbers.py` stay unchanged; their existing tests keep passing unmodified.
- No new dependencies in `pyproject.toml`.
