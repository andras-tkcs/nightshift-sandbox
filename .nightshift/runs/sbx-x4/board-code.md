# Board review: code, sbx-x4

Range: `git diff origin/e2e/20261002-5...origin/feature/x4` (`origin/main...origin/feature/x4` has no merge base; the ledger has no base field, so I used the run's base branch the caller named).
Inputs: the diff, `docs/sbx-x4-plan.md` (plan/sbx-x4), `.nightshift/runs/sbx-x4/acceptance.md`, `CLAUDE.md`. I did not run the project's checks because the caller did not ask me to.

## Findings

- non-blocking · tests/test_acceptance_sbx_x4.py:1 · The phase removed the strict `xfail` markers from this file. That is the right acceptance flip: all assertions are unchanged and nothing was weakened. But the file is not in the phase's `touches` list, and the phase acceptance line "11 passed" does not count these 6 tests (the suite should now report 17). · In later plans, list the acceptance test file in `touches` and count acceptance tests in the expected pass total.
- non-blocking · tests/test_text.py:20-40 · The five new unit tests repeat the AC-1 to AC-5 assertions in tests/test_acceptance_sbx_x4.py word for word. The plan asked for this (D2), so it is not a defect, but the same assertions now live in two places. · Follow-up: drop one set, or keep the acceptance file as the only AC record.
- non-blocking · docs/sbx-x4-plan.md (manifest) · The manifest says `feature_branch: feature/sbx-x4`, but the run used `feature/x4` (ledger). · Make the manifest match the branch the ledger records.
- non-blocking · sandbox_pkg/text.py:14 · The name `titlecase` does not match what the function does (it slugifies). The README says so, and the plan leaves the name as an owner question. · Put the rename question (`slugify`, maybe with a `titlecase` alias) in the PR body for the owner.

## Summary

- Correctness: `sandbox_pkg/text.py` matches plan D1 exactly. It maps every non-alphanumeric character to a space, then uses `split()`/`join`. That collapses runs of separators, strips them from both ends, returns `""` for input made only of separators, and keeps Unicode letters and digits, lowercased. AC-1 to AC-5 all hold.
- Tests: `tests/test_text.py` matches D2 exactly. The acceptance tests, which were committed earlier as strict xfail, now run as normal tests with unchanged assertions. Nothing was skipped, deleted or weakened.
- Docs: the README section matches D3 exactly. Its two examples match the AC-7 regex and the function's output. The "recieve" typo was left alone, as the plan says.
- AC-8 and scope: `pyproject.toml`, `__init__.py`, `numbers.py` and `test_numbers.py` are unchanged. No dependencies were added. The plan doc was added and then deleted, so its net diff is zero (retirement done). No `.nightshift/` files are on the feature branch.
- Untrusted text (R-SEC-3): none. There is no issue and no external text, and nothing was copied in as instructions.
- No blocking findings.

REVIEW verdict=approve
