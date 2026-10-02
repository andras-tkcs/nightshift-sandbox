# Review p2-clamp, round 1

Range: `git diff origin/feature/x3...origin/feature/x3--p2-clamp` (merge base 4990687 = origin/feature/x3). Commits: e47055b "Add clamp to sandbox_pkg.numbers", 187c011 "Remove clamp acceptance xfail markers".
Plan: docs/sbx-x3-plan.md, phase p2-clamp (D2, D3). The project checks were not run because the caller did not ask for them.

## Findings

- non-blocking · tests/test_acceptance_sbx_x3.py:65 (commit 187c011) · The xfail markers are removed in a separate commit. The brief says "Make exactly one commit", and the AC file's own docstring says markers come off "in the same commit as the implementation". At e47055b alone, the AC-3/4/5 tests are strict xfail but pass, so they report XPASS(strict) and that commit is red, which breaks bisect. · Squash 187c011 into e47055b as one commit, "Add clamp to sandbox_pkg.numbers", or squash-merge the phase.
- non-blocking · phase acceptance "git diff --name-only HEAD~1 HEAD prints exactly sandbox_pkg/numbers.py and tests/test_numbers.py" · This criterion cannot be met as written now that the conductor allows the AC-file edit. With two commits HEAD~1..HEAD shows only the AC file, and with one commit it would show three files. The conductor's allowance covers this, so it is not a defect in the code. · Record the allowed third file in the phase result or merge note.
- non-blocking · docs/sbx-x3-plan.md manifest `feature_branch: feature/sbx-x3` · The caller reviews against `origin/feature/x3`, which does not match the manifest's feature branch name. · The conductor should confirm which branch is the run's feature branch before merging.

## Checklist

1. Correctness: `clamp` in sandbox_pkg/numbers.py:12-22 matches D2 exactly. The NaN check comes first and includes `# noqa: PLR0124`. Then `low > high`, then the inclusive comparisons. The chosen argument object is returned unchanged, so int stays int. Infinities pass. There is no `import math`. The AC-5 "both-bounds" NaN case is caught by the first check. The error messages match the phase acceptance strings.
2. Simplicity: nothing beyond the plan.
3. Tests: the 12 tests in tests/test_numbers.py match D3 verbatim, and the import is changed to `clamp, mean` as specified. No test was weakened. The AC-file change only removes four `@ACCEPTANCE` decorators on test_ac3_* (2), test_ac4_* and test_ac5_*. No assertion changed, and AC-1/2/7 keep their markers, as the conductor allowed.
4. Acceptance coverage: AC-3, AC-4 and AC-5 are covered by both the unit tests and the now-active acceptance tests. The AC-3 check output "5 0 10 0 10 1.0 4" follows from the code.
5. Docs: the README is deliberately left for p3-retire (plan deviation note), so nothing is missing for this phase.
6. Untrusted text: nothing copied from untrusted sources was found.
7. Hygiene: only the allowed files are touched (numbers.py, test_numbers.py, plus the permitted AC file). There are no `.nightshift/` files, no secrets and no stray files. The commit messages are clear. The commit count issue is noted above.

## Summary

The implementation and tests match the plan verbatim and satisfy AC-3, AC-4 and AC-5. There are no blocking findings. Squashing the two commits is recommended so that every commit is green.

REVIEW verdict=approve
