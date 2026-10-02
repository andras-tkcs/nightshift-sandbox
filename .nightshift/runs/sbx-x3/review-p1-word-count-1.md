# Review p1-word-count, round 1

Range: `git diff origin/feature/x3...origin/feature/x3--p1-word-count` (1 commit, 6096e1d "Add word_count to sandbox_pkg.text").
Plan: docs/sbx-x3-plan.md, phase p1-word-count (Design D1, D3).

## Findings

- non-blocking · tests/test_acceptance_sbx_x3.py:1 · Acceptance criterion "git diff --name-only HEAD~1 HEAD prints exactly sandbox_pkg/text.py and tests/test_text.py" is literally unmet because the commit also touches tests/test_acceptance_sbx_x3.py and the manifest `touches` does not list that file. The caller states an owner-approved exception for removing this phase's own xfail markers, and the change is limited to deleting three `@ACCEPTANCE` lines (test_ac1_* x2, test_ac2_*) with no assertion changes · no change needed; mention the exception in the PR body.
- non-blocking · README.md · README not updated for word_count in this phase · intended by the plan (README edits are deferred to p3-retire per the gate-1 deviation); no action in this phase.

## Summary

- Correctness: `word_count` in sandbox_pkg/text.py matches Design D1 verbatim, placed after `reverse_words` and before `count_vowels` with two blank lines on each side.
- Tests: tests/test_text.py import line and the five tests match Design D3 verbatim. Marker removal covers only the AC-1 and AC-2 tests; AC-3/4/5/7 markers stay; `ACCEPTANCE` is still used, so no unused name. No test weakened, skipped or with changed assertions.
- Scope: no files outside the brief except the excepted acceptance file; no README, numbers.py or test_numbers.py edits; no `.nightshift/` files, no secrets, no dependencies. Single commit with the exact message the brief requires.
- Untrusted text: none found.
- Checks were not run (not requested by the caller).

REVIEW verdict=approve