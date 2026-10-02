# Review 1: sbx-2 (count_vowels ignores uppercase vowels)

Range reviewed: `git diff origin/e2e/20261002-2...origin/fix/sbx-2`. The caller named `origin/main`, but `.claude/project-profile.yaml` sets `git.base_branch: "e2e/20261002-2"`, and `origin/main` has no merge base with the branch.
Commits: `95960d4 test: failing test for sbx-2`, `b253a48 Make count_vowels case-insensitive`.

## Findings

- non-blocking · sandbox_pkg/text.py:11 · `ch.lower() in "aeiou"` does a substring check, not a single-character check. For the rare characters whose lowercase form is more than one character (for example "İ" becomes "i" plus a combining dot), membership is a substring test. No character's lowercase form is a substring of "aeiou", so the result is correct today. · No change needed. If the function is later changed to take a vowel set, use a `set`/`frozenset` lookup.

No blocking findings.

## Summary

- The fix matches the mini-plan exactly: a case-insensitive comparison through `ch.lower()`, kept to one line.
- Tests: the two cases the plan asked for (`"AEIOU" == 5` and mixed-case `"Banana" == 3`) were added in `tests/test_text.py`. The commit history shows the failing test committed first as `test: failing test for sbx-2`, as the plan required.
- README: the uppercase example `count_vowels("AEIOU")    # 5` was added, and its alignment matches the nearby lines.
- Scope: only the three files in the plan were changed. No new dependencies. Nothing was copied from untrusted text.
- I did not run the checks (pytest/ruff) because the caller did not ask for them. The change is simple and is not expected to cause lint problems.

REVIEW verdict=approve