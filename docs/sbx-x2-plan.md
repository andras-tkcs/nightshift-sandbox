# Plan: sbx-x2, add `slugify(text)` to `sandbox_pkg.text`

## Goal

Request (run `sbx-x2`, text request, no issue): add `slugify(text)` to
`sandbox_pkg/text.py`. It lowercases the text, turns every run of spaces and
punctuation into a single hyphen, and leaves no leading or trailing hyphen. It
gets tests and a README section. Users of the package can then build URL-safe
slugs with `from sandbox_pkg.text import slugify`. The acceptance criteria are
AC-1 to AC-7 in `.nightshift/runs/sbx-x2/acceptance.md`. The design is in
`.nightshift/runs/sbx-x2/design.md`, and this plan does not reopen it.

## Current state

- `sandbox_pkg/text.py:1-11`: the module docstring `"""Text helpers."""` and two
  pure functions, `reverse_words` (lines 4-6) and `count_vowels` (lines 9-11).
  Neither has type hints. Each has a one-line docstring that starts with "Return".
  The module has no imports.
- `tests/test_text.py:1`: `from sandbox_pkg.text import count_vowels, reverse_words`,
  then four plain `def test_*` functions (lines 4-17). It does not use parametrize yet.
- `README.md:5-6`: the intro sentence "It helps you recieve text and do small things
  with it: reverse the words of a sentence, count vowels and compute a mean."
  (it contains the typo "recieve"). `README.md:8-17`: `## Usage` with one
  `python` code block.
- `pyproject.toml`: no runtime dependencies. `requires-python = ">=3.10"`.
- There is no `CHANGELOG.md`, no `docs/` directory (apart from this plan) and no ADR directory.
- Checks: the resolved profile (`ns profile show`) lists `.venv/bin/python -m ruff check .` and
  `.venv/bin/python -m pytest -q`. CLAUDE.md spells the same tools `.venv/bin/ruff check .` and
  `.venv/bin/pytest -q`. Both forms run the same `.venv` tools, and the plan uses the profile form.
  CI (`.github/workflows/tests.yml`) runs the same two on Python 3.12. Baseline:
  6 tests pass and ruff reports "All checks passed!".

## Design

Everything below is settled. The worker copies it as written.

### D1. `sandbox_pkg/text.py`

The final file is exactly:

```python
"""Text helpers."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def reverse_words(text):
    """Return the words of text in reverse order, joined by single spaces."""
    return " ".join(reversed(text.split()))


def count_vowels(text):
    """Return the number of vowels in text."""
    return sum(1 for ch in text if ch in "aeiou")


def slugify(text):
    """Return text as a lowercase, hyphen-separated slug of ASCII letters and digits."""
    return _NON_ALNUM.sub("-", text.lower()).strip("-")
```

- `reverse_words` and `count_vowels` are unchanged byte for byte.
- `[^a-z0-9]` and not `\W`, because `\W` keeps `_` and Unicode letters (design, "Rejected alternatives").
- No type hints and no input validation (design, "Interfaces" and "Edge cases").

### D2. `tests/test_text.py`

- Change line 1 to `from sandbox_pkg.text import count_vowels, reverse_words, slugify`.
- Add `import pytest` as the first line, above that import, with one blank line
  between the two imports (ruff's isort rules are not enabled, so either order passes,
  but this matches the usual stdlib/third-party/first-party order).
- Leave the four existing tests unchanged. Append at the end of the file:

```python
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello World", "hello-world"),
        ("Hello,  World!!  Again", "hello-world-again"),
        ("a--b__c..d", "a-b-c-d"),
        ("  --Hello World!--  ", "hello-world"),
        ("!!!", ""),
        ("", ""),
        ("Python 3.10 Release", "python-3-10-release"),
    ],
)
def test_slugify(text, expected):
    assert slugify(text) == expected
```

- Do not add tests for non-ASCII input (design, "Edge cases").

### D3. `README.md`

- Lines 5-6: change the intro sentence to exactly:
  "It helps you receive text and do small things with it: reverse the words of a
  sentence, count vowels, make a slug and compute a mean."
  This also fixes the "recieve" typo, because the sentence is being edited anyway. No
  acceptance criterion requires the fix (the design calls it optional). The plan makes it so
  the worker has no choice left to make.
- Usage block: change the import line to
  `from sandbox_pkg.text import reverse_words, count_vowels, slugify` and add the line
  `slugify("Hello World")   # "hello-world"` directly after the `count_vowels` line,
  so the `#` comments stay in one column with the other lines.
- No separate `## slugify` heading. The design allowed either form. This plan picks the
  Usage-block line because the README has one Usage block for every function, and
  AC-7 is met by a line in that block (`grep -n slugify README.md` matches it, and
  `"Hello World"` is an AC-1 case).

## ADRs

None. This is one small pure function, and the repository has no ADR directory or ADR bar.

## Manual steps

None. There is no `manual_before` or `manual_after`, so the plan has no
`.nightshift/runs/sbx-x2/manual-steps.md`. CI runs the same checks the worker
runs locally.

## Risks and open questions

- No open owner decisions.
- The plan assumes `sandbox_pkg/text.py` and `tests/test_text.py` still match the
  "Current state" above (base commit `3393439`). If `slugify` already exists, or
  either file differs, the worker stops with `status=blocked`.
- If any of the seven parametrized cases fails with the D1 code as written, the
  plan is wrong. The worker stops with `status=blocked` and does not change the expected
  values or the regex.
- If `ruff check .` reports a rule on the new code, the worker fixes only formatting
  that keeps the behaviour (for example import placement). If the fix needs a
  behaviour change, the worker stops with `status=blocked`.
- One phase only: the change is about 5 source lines plus tests and a README line,
  so the implementation and the retirement work (delete this plan) fit in a single
  S phase. There is no CHANGELOG to update and there are no ADRs to write.

## Implementation manifest

```yaml
plan_slug: sbx-x2
feature_branch: feature/sbx-x2
max_parallel: 1
manual_before: []
manual_after: []
verify_after_merge:
  - ".venv/bin/python -m ruff check ."
  - ".venv/bin/python -m pytest -q"
final_checks:
  - "docs/sbx-x2-plan.md is deleted"
  - "README.md mentions slugify in the Usage block"
  - "pyproject.toml and sandbox_pkg/numbers.py are unchanged"
phases:
  - id: p1-slugify
    title: Add slugify with tests and README, retire the plan
    depends_on: []
    complexity: S
    touches:
      - sandbox_pkg/text.py
      - tests/test_text.py
      - tests/test_slugify_acceptance.py
      - README.md
      - docs/sbx-x2-plan.md
    brief: |
      Read docs/sbx-x2-plan.md, sections "Design" D1 to D3, before you start.
      1. Check the starting state: sandbox_pkg/text.py has only reverse_words and count_vowels and no import, and tests/test_text.py line 1 is
         "from sandbox_pkg.text import count_vowels, reverse_words". If not, stop with status=blocked.
      2. sandbox_pkg/text.py: make the file exactly the D1 listing. Add "import re" after the module docstring, the module-level
         _NON_ALNUM = re.compile(r"[^a-z0-9]+") and the function slugify(text) at the end of the file. Do not change reverse_words or count_vowels.
      3. tests/test_text.py: add "import pytest" as line 1 followed by a blank line, extend the sandbox_pkg import to
         "from sandbox_pkg.text import count_vowels, reverse_words, slugify", and append the parametrized test_slugify from D2 with all
         seven cases exactly as listed. Do not modify the existing four tests.
      4. Run .venv/bin/python -m pytest -q tests/test_text.py -k slugify. All 7 cases pass. If any case fails, stop with status=blocked
         and do not change the expected values or the regex.
      5. README.md: replace the intro sentence with the exact D3 sentence (this fixes "recieve" to "receive"), change the Usage import line
         to "from sandbox_pkg.text import reverse_words, count_vowels, slugify", and add the line
         'slugify("Hello World")   # "hello-world"' directly after the count_vowels line. No new heading.
      5b. tests/test_slugify_acceptance.py: remove the ACCEPTANCE xfail decorators and the ACCEPTANCE = ... definition (and any import left unused) so the 8 acceptance tests run as normal tests.
      6. Delete docs/sbx-x2-plan.md (git rm). This is the retirement step. There are no ADRs to write and no CHANGELOG.md exists, so do not create one.
      7. Run .venv/bin/python -m ruff check . and .venv/bin/python -m pytest -q. Both pass. Do not touch pyproject.toml or sandbox_pkg/numbers.py.
         If ruff reports a rule that needs more than a formatting fix keeping the behaviour, or any existing test fails, stop with status=blocked.
    acceptance:
      - ".venv/bin/python -c \"from sandbox_pkg.text import slugify; assert slugify('Hello World') == 'hello-world'\" exits 0 (AC-1)"
      - ".venv/bin/python -c \"from sandbox_pkg.text import slugify as s; assert s('Hello,  World!!  Again') == 'hello-world-again' and s('a--b__c..d') == 'a-b-c-d'\" exits 0 (AC-2)"
      - ".venv/bin/python -c \"from sandbox_pkg.text import slugify as s; assert s('  --Hello World!--  ') == 'hello-world' and s('!!!') == '' and s('') == ''\" exits 0 (AC-3)"
      - ".venv/bin/python -c \"from sandbox_pkg.text import slugify; assert slugify('Python 3.10 Release') == 'python-3-10-release'\" exits 0 (AC-4)"
      - ".venv/bin/python -m pytest -q tests/test_text.py -k slugify reports 7 passed (AC-5)"
      - ".venv/bin/python -m pytest -q reports 21 passed and 0 failed, and .venv/bin/python -m ruff check . prints 'All checks passed!' (AC-6)"
      - "grep -n 'slugify(\"Hello World\")   # \"hello-world\"' README.md prints one line (AC-7)"
      - "grep -q recieve README.md exits 1, i.e. the typo is gone (plan decision D3, not an AC)"
      - "test ! -e docs/sbx-x2-plan.md exits 0"
      - "git diff --quiet 3393439 -- pyproject.toml sandbox_pkg/numbers.py exits 0"
```
