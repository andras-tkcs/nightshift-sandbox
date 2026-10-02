# Review: sbx-x4 phase p1-titlecase, round 1

Range: `git diff origin/feature/x4...origin/feature/x4--p1-titlecase` (1 commit, 92ad7e9).
Plan: docs/sbx-x4-plan.md (on plan/sbx-x4), phase p1-titlecase. Profile docs: CLAUDE.md.
No worker log or reasoning was offered or read. The project's checks were not run, because the caller did not ask for them.

## Findings

- non-blocking · tests/test_acceptance_sbx_x4.py:1 · This file is not in the phase's `touches`. The caller says removing the xfail(strict=True) markers is intended. The removal is clean: all 6 `@ACCEPTANCE` decorators, the `ACCEPTANCE` constant and the now-unused `import pytest` are gone, and no test body or assertion changed, so no test was weakened. · Add the acceptance file to `touches` in future manifests so the brief matches the intended scope.
- non-blocking · docs/sbx-x4-plan.md (manifest acceptance) · The phase acceptance says "11 passed". With the acceptance markers removed, the 6 AC tests now pass too, so the real total should be 17 (6 existing + 5 new + 6 acceptance). This is a mistake in the plan, not in the code. · Expect 17 passed in verify_after_merge and the final checks, or count the tests per file.
- non-blocking · plan manifest `feature_branch: feature/sbx-x4` · The review range uses `feature/x4`, not `feature/sbx-x4`. · Ask the orchestrator to confirm which name is right. The diff content is unaffected.
- non-blocking · sandbox_pkg/text.py:14 · The name `titlecase` does not match the slug behaviour. The plan records this as an open owner decision, and the README says so plainly ("Despite its name, it does not title-case text."). · Put the rename question in the PR body for the owner.

## Checklist

1. Correctness: `titlecase` matches D1 verbatim. Mapping non-alphanumeric characters to spaces and then running `split()`/`join` collapses runs, strips the edges, returns "" for empty or all-separator input and keeps Unicode alphanumerics lowercased. This covers AC-1 to AC-5.
2. Simplicity: there are no imports, no dependencies and no extra code. reverse_words and count_vowels are unchanged.
3. Tests: tests/test_text.py has the D2 import line and the five D2 tests verbatim. The strict-xfail acceptance tests were the failing tests written first, and they are now active.
4. Acceptance coverage: AC-1 to AC-5 are covered by unit and acceptance tests, and AC-7 by the README acceptance test. pyproject.toml, sandbox_pkg/__init__.py, sandbox_pkg/numbers.py and tests/test_numbers.py do not appear in the diff (AC-8 / D4). The plan doc is deleted.
5. Docs: the README `### titlecase` section matches D3 verbatim, follows the usage block and ends in a single newline. The "recieve" typo is left alone, as the plan says.
6. Untrusted text: none. There is no issue, and no command or URL was copied in.
7. Commit hygiene: one commit with a clear message. There are no secrets, no `.nightshift/` files and no stray files. The only file outside `touches` is the acceptance file, which the caller says is intended.

## Summary

The phase does exactly what the plan says, copying the code, tests and README text verbatim and retiring the plan document. I found no blocking problems. The non-blocking notes cover a wrong test count in the plan, the branch-name mismatch and the open naming question, which belongs in the PR body.

REVIEW verdict=approve
