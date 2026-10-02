# Plan: sbx-x4, add `titlecase(text)` to `sandbox_pkg/text.py`

## Goal

Users of `sandbox_pkg` get a new function `sandbox_pkg.text.titlecase(text)`. It returns a lowercase, hyphen-separated slug of `text`: every run of spaces and punctuation becomes one hyphen, with no hyphen at either end. The README documents it. There is no issue. The request is the run's text: "Add titlecase(text) to sandbox_pkg/text.py: lowercase, spaces and punctuation become single hyphens, no leading or trailing hyphen. Add tests and a README section." Acceptance criteria: `.nightshift/runs/sbx-x4/acceptance.md` (AC-1 to AC-8). Design: `.nightshift/runs/sbx-x4/design.md`.

The name `titlecase` does not match the behaviour. As requested, we keep the name. Renaming it is an open owner question (see "Risks and open questions").

## Current state

- `sandbox_pkg/text.py` (11 lines) has `reverse_words` (`sandbox_pkg/text.py:4`) and `count_vowels` (`sandbox_pkg/text.py:9`). These are plain functions with one-line docstrings and no type hints. There is no `titlecase` and no import.
- `tests/test_text.py` (17 lines). Line 1 is `from sandbox_pkg.text import count_vowels, reverse_words`, followed by four flat `def test_*` functions with a bare `assert`.
- `README.md` (17 lines). It has one `## Usage` section (`README.md:8`) holding one Python code block (`README.md:10-17`). There are no `###` subsections. Line 5 has a known typo ("recieve"), which is out of scope.
- `sandbox_pkg/__init__.py` is empty. `pyproject.toml` has no runtime dependencies, and `test = ["pytest"]` is optional.
- There is no `docs/` directory (this plan creates it), no `CHANGELOG*`, no ADR directory, and the profile sets no `docs.*` keys.
- Checks: the resolved profile (`ns profile show`) declares `.venv/bin/python -m ruff check .` and `.venv/bin/python -m pytest -q`. `CLAUDE.md` and AC-6 use `.venv/bin/ruff check .` and `.venv/bin/pytest -q`. Both forms pass on the base today (6 tests). Ruff is 0.16.10 with default rules and no `[tool.ruff]` config. CI (`.github/workflows/tests.yml`) runs bare `ruff check .` and `pytest -q` after `pip install -e .`.
- Base branch ref: the phase worktree has no local `e2e/20261002-5` branch, so diffs use `origin/e2e/20261002-5`.

## Design

### D1. The function (verbatim)

Append this to the end of `sandbox_pkg/text.py`, after `count_vowels`, with exactly two blank lines before it and one newline at the end of the file:

```python
def titlecase(text):
    """Return text as a lowercase slug: non-alphanumeric runs become one hyphen."""
    mapped = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return "-".join(mapped.split())
```

How it works: `split()` with no argument drops empty pieces. Runs of separators collapse to one hyphen (AC-2), the edges are stripped (AC-3), and input made only of separators gives `""` (AC-4). `isalnum()` keeps Unicode letters and digits, so `"ÉTÉ"` becomes `"été"` (AC-5). `_`, `-` and tabs are not alphanumeric, so they act as separators. Only the standard library is used, with no imports. I ran this code against every AC example before writing the plan, and all of them pass.

Rejected: `re.sub` with `\w`, because `\w` matches `_`, which AC-2 says is a separator. Real title casing, because it contradicts AC-1 to AC-5. A rename to `slugify`, because that is the owner's call. A new `slug.py` module, because the request names `text.py`. Unicode normalisation or transliteration, because those are non-goals.

### D2. The tests (verbatim)

In `tests/test_text.py`, change line 1 to:

```python
from sandbox_pkg.text import count_vowels, reverse_words, titlecase
```

Append these functions at the end of the file, with two blank lines between functions and one newline at the end of the file:

```python
def test_titlecase_basic():
    assert titlecase("Hello World") == "hello-world"
    assert titlecase("Hello, World!") == "hello-world"


def test_titlecase_collapses_separator_runs():
    assert titlecase("a  ,-;  b") == "a-b"
    assert titlecase("a_b.c") == "a-b-c"


def test_titlecase_strips_edge_separators():
    assert titlecase("  --Hi there!!  ") == "hi-there"


def test_titlecase_degenerate_input():
    assert titlecase("") == ""
    assert titlecase("!?  ...") == ""


def test_titlecase_keeps_unicode_letters_and_digits():
    assert titlecase("Version 2 ÉTÉ") == "version-2-été"
```

These map to the criteria as follows: `test_titlecase_basic` covers AC-1, `test_titlecase_collapses_separator_runs` covers AC-2, `test_titlecase_strips_edge_separators` covers AC-3, `test_titlecase_degenerate_input` covers AC-4 and `test_titlecase_keeps_unicode_letters_and_digits` covers AC-5. The file is saved as UTF-8.

### D3. The README section (verbatim)

Append this to the end of `README.md`, after the closing fence of the existing usage block (`README.md:17`), with one blank line before `### titlecase` and one newline at the end of the file. Leave the existing usage block, the intro paragraph and the "recieve" typo unchanged.

````markdown
### titlecase

`titlecase(text)` turns text into a lowercase slug: each run of spaces and
punctuation becomes one hyphen, with no hyphen at either end. Despite its name,
it does not title-case text.

```python
from sandbox_pkg.text import titlecase

titlecase("Hello, World!")      # "hello-world"
titlecase("  --Hi there!!  ")   # "hi-there"
```
````

(The outer four-backtick fence only delimits the example in this plan. Write the inner content, from `### titlecase` to the closing three-backtick fence, into the README.)

### D4. Files not changed

These files are not changed: `sandbox_pkg/__init__.py`, `sandbox_pkg/numbers.py`, `tests/test_numbers.py`, `pyproject.toml` (AC-8), `CLAUDE.md`, `.github/**` and `.claude/**`.

## ADRs

None. The repo has no ADR directory and no contributing document that sets an ADR bar. The change adds one pure function.

## Manual steps

None. `manual_before` and `manual_after` are empty, and there is no `RUN/manual-steps.md`. Every check is a local command.

## Risks and open questions

1. **Open owner decision: the name.** The function slugifies text and does not title-case it. The plan keeps the requested name `titlecase`. The question for the owner at gate 1: rename it to `slugify` (perhaps with `titlecase` kept as an alias), or keep `titlecase`? This plan does not settle it. If the owner picks a rename, revise D1 to D3 and the manifest before implementation starts.
2. **The repo differs from "Current state".** For example, `titlecase` already exists, line 1 of `tests/test_text.py` differs, or `README.md` already has a `### titlecase` section. The brief is then stale: the worker stops with `status=blocked`.
3. **Ruff flags the verbatim code.** This is unlikely with default rules, and the non-ASCII literal is not flagged by default. The worker does not rewrite the plan's code to silence ruff. It stops with `status=blocked` and quotes the ruff output.
4. **Unicode edge cases.** `"İ".lower()` adds a combining mark, and `"²".isalnum()` is true. Both are accepted per design.md. They are not tested and not special-cased.
5. **AC-8 names `origin/main`, but the real base is `e2e/20261002-5`.** Acceptance checks `pyproject.toml` against `origin/e2e/20261002-5`. If that ref does not resolve (`git rev-parse --verify origin/e2e/20261002-5` fails), the worker stops with `status=blocked` and does not switch to another ref. Either way, the file must not change.
6. **One phase does the work and the retirement.** The change is about 8 source lines plus about 17 test lines and 12 README lines, so a separate retirement phase would be empty overhead. The phase therefore also deletes this plan document. Because there are no ADRs, no reference docs beyond the README and no changelog, retirement is only that deletion.

## Implementation manifest

```yaml
plan_slug: sbx-x4
feature_branch: feature/sbx-x4
max_parallel: 1
manual_before: []
manual_after: []
verify_after_merge:
  - ".venv/bin/python -m ruff check ."
  - ".venv/bin/python -m pytest -q"
  - ".venv/bin/ruff check ."
  - ".venv/bin/pytest -q"
final_checks:
  - "docs/sbx-x4-plan.md is deleted"
  - "git diff --quiet origin/e2e/20261002-5 -- pyproject.toml exits 0 (pyproject.toml unchanged against the base branch)"
  - "grep -c '^### titlecase$' README.md prints 1"
  - "no ADR directory and no CHANGELOG exist in the repo, so no ADR and no changelog entry are required"
phases:
  - id: p1-titlecase
    title: Add titlecase(text) with tests and a README section, and retire the plan
    depends_on: []
    complexity: S
    touches:
      - sandbox_pkg/text.py
      - tests/test_text.py
      - README.md
      - docs/sbx-x4-plan.md
    brief: |
      Read docs/sbx-x4-plan.md sections "Design D1", "Design D2", "Design D3" and "Design D4" first. Copy their code and text verbatim. Do not edit any file outside this phase's touches.
      1. Confirm that "grep -c 'def titlecase' sandbox_pkg/text.py" prints 0, that line 1 of tests/test_text.py is exactly "from sandbox_pkg.text import count_vowels, reverse_words", and that "grep -c '^### titlecase' README.md" prints 0. If any of these differs, stop with status=blocked and report what you found.
      2. Run ".venv/bin/python -m pytest -q" and "git rev-parse --verify origin/e2e/20261002-5". If any existing test fails, or the ref does not resolve, stop with status=blocked.
      3. In sandbox_pkg/text.py, append the function titlecase exactly as in Design D1, after count_vowels, with two blank lines before it and a single trailing newline. Do not change reverse_words or count_vowels.
      4. In tests/test_text.py, replace line 1 with "from sandbox_pkg.text import count_vowels, reverse_words, titlecase".
      5. Append the five test functions from Design D2 (test_titlecase_basic, test_titlecase_collapses_separator_runs, test_titlecase_strips_edge_separators, test_titlecase_degenerate_input, test_titlecase_keeps_unicode_letters_and_digits) to the end of tests/test_text.py, with two blank lines between functions. Save the file as UTF-8.
      6. Append the README section from Design D3 (from "### titlecase" to the closing three-backtick fence) to the end of README.md, with one blank line before "### titlecase". Do not fix the "recieve" typo or change the existing Usage code block.
      7. Run ".venv/bin/python -m ruff check .", ".venv/bin/python -m pytest -q", ".venv/bin/ruff check ." and ".venv/bin/pytest -q". All four must pass. If ruff flags the verbatim code from the plan, do not rewrite it: stop with status=blocked and quote the ruff output. If a titlecase test fails, stop with status=blocked and quote the failure.
      8. Retirement, only after steps 3 to 7 pass: delete docs/sbx-x4-plan.md with "git rm docs/sbx-x4-plan.md". The docs/ directory is then empty and disappears. There are no ADRs, no CHANGELOG and no other reference docs to update (see the plan's "ADRs" section and Design D4).
      9. Commit the changes to sandbox_pkg/text.py, tests/test_text.py and README.md, and the deletion of docs/sbx-x4-plan.md.
    acceptance:
      - ".venv/bin/python -m pytest -q exits 0, and its output includes 11 passed (6 existing tests in tests/test_text.py and tests/test_numbers.py, plus 5 new)"
      - ".venv/bin/python -m pytest -q tests/test_text.py -k titlecase exits 0 with 5 passed"
      - ".venv/bin/python -m ruff check . exits 0 and prints All checks passed!"
      - ".venv/bin/pytest -q exits 0 with 11 passed, and .venv/bin/ruff check . exits 0 (AC-6 exact commands)"
      - ".venv/bin/python -c 'from sandbox_pkg.text import titlecase; print(titlecase(\"Hello, World!\"))' prints hello-world"
      - "grep -c '^### titlecase$' README.md prints 1"
      - "grep -cF 'titlecase(\"Hello, World!\")      # \"hello-world\"' README.md prints 1"
      - "git diff --quiet origin/e2e/20261002-5 -- pyproject.toml sandbox_pkg/__init__.py sandbox_pkg/numbers.py tests/test_numbers.py exits 0"
      - "test ! -e docs/sbx-x4-plan.md exits 0"
```
