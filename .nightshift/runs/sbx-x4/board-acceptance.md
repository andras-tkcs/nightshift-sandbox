# Board acceptance: sbx-x4 (origin/feature/x4 @ e9b51fd)

Note: origin/main (6189a9d) and origin/feature/x4 share no history, so `git diff origin/main...origin/feature/x4` fails with "no merge base". The diff below is against the run base origin/e2e/20261002-5 (5065efe), which is the root commit of the feature branch. The checks ran on a `git archive` export of origin/feature/x4 in /tmp/tmp.tL2yeSSmmS, using `PYTHONPATH=<export>` because the worktree .venv has the package installed as editable from the plan worktree.

AC-1 met: `pytest tests/test_acceptance_sbx_x4.py::test_ac1_import_and_basic_slug` passed, also tests/test_text.py::test_titlecase_basic; python check: titlecase("Hello World") -> 'hello-world', titlecase("Hello, World!") -> 'hello-world'
AC-2 met: test_ac2_separator_runs_become_one_hyphen passed; python check: "a  ,-;  b" -> 'a-b', "a_b.c" -> 'a-b-c'
AC-3 met: test_ac3_no_leading_or_trailing_hyphen passed; python check: "  --Hi there!!  " -> 'hi-there'
AC-4 met: test_ac4_degenerate_input passed; python check: "" -> '', "!?  ..." -> ''
AC-5 met: test_ac5_letters_and_digits_kept_lowercased passed; python check: "Version 2 ÉTÉ" -> 'version-2-été'
AC-6 met: `python -m pytest -q` on the export -> 17 passed (6 in tests/test_acceptance_sbx_x4.py); `ruff check --no-cache .` -> "All checks passed!" (exit 0)
AC-7 met: README.md has a "### titlecase" section with `titlecase("Hello, World!")  # "hello-world"` and `titlecase("  --Hi there!!  ")  # "hi-there"`; test_ac7_readme_section_shows_titlecase_example passed
AC-8 met: `git diff origin/e2e/20261002-5...origin/feature/x4 -- pyproject.toml` -> empty (0 lines)

Non-goals: no change to sandbox_pkg/numbers.py (empty diffstat); reverse_words and count_vowels are unchanged (text.py diff only appends titlecase).

Blocking findings: none. Non-blocking: the open question from acceptance.md (rename to `slugify`?) is still open, and the README says the name does not match the behaviour.

REVIEW verdict=approve
