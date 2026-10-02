# Review p3-retire, round 1 (run sbx-x3)

Range: `git diff origin/feature/x3...origin/feature/x3--p3-retire` (commits daf280c, 75e7ba2).
Inputs: docs/sbx-x3-plan.md (Design D4, manifest phase p3-retire), the diff, CLAUDE.md. No worker log was offered or read.

## Findings

- non-blocking · tests/test_acceptance_sbx_x3.py:152,162 · The xfail markers are removed in a second commit (75e7ba2), not in the phase's single commit. The brief says "Make exactly one commit", the test module docstring (lines 3-4) says markers go "in the same commit as the implementation", and the acceptance check `git diff --name-only HEAD~1 HEAD prints exactly README.md and docs/sbx-x3-plan.md` fails as written, because HEAD~1..HEAD now holds only the test file. The change is allowed by the caller's exception, and the phase diff as a whole is correct. · Squash 75e7ba2 into daf280c, or check that acceptance line against the phase range (`origin/feature/x3...HEAD`) instead.
- non-blocking · tests/test_acceptance_sbx_x3.py:19 · `ACCEPTANCE = pytest.mark.xfail(...)` is unused now that every AC marker is gone. That is dead code, though ruff does not flag unused module-level names. Removing it is outside this phase's allowed exception. · Follow-up: delete the constant and update the module docstring in a later change, or leave it as the run's template.

## Checks walked

- Correctness / D4: README Usage block lines 11-18 match D4 byte for byte (checked with `cat -A`). The `#` sits at column 25 on both new lines, and the "recieve" typo is unchanged. numstat is `4 2 README.md` as required.
- Plan retirement: docs/sbx-x3-plan.md is deleted (0 additions, 292 deletions), and docs/ is absent on the branch.
- Tests: the only test change is removing `@ACCEPTANCE` from the two AC-7 tests. No assertion was changed, so the caller's exception covers it. The AC-7 tests parse the README block. With the new lines, `word_count("a b  c") == 3` and `clamp(15, 0, 10) == 10`, so each test should pass, and with strict xfail removed they are now real checks. I did not run the test suite because the caller did not ask for it.
- Scope: files touched are README.md, docs/sbx-x3-plan.md (both in `touches`) and the excepted test file. pyproject.toml is unchanged. There are no `.nightshift/` files, no secrets and no new dependencies.
- Untrusted text (R-SEC-3): none. The README lines come verbatim from the plan.
- Commit messages: clear. daf280c matches the brief's message.

## Summary

The phase does what D4 and the manifest ask: both functions are documented in the README Usage block with checked examples, the plan is retired, and the AC-7 acceptance tests are now real checks. There are two non-blocking points. The second commit breaks the literal "exactly one commit / HEAD~1" acceptance wording, and the `ACCEPTANCE` constant is now unused. Neither is blocking.

REVIEW verdict=approve
