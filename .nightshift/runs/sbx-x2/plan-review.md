# Plan review: sbx-x2 (docs/sbx-x2-plan.md)

Verdict: changes. One blocking finding: an acceptance command cannot pass as written.

Inputs read: docs/sbx-x2-plan.md, the plan and plan-manifest skills, .nightshift/runs/sbx-x2/acceptance.md, design.md, triage.md, CLAUDE.md, .claude/project-profile.yaml, sandbox_pkg/text.py, tests/test_text.py, README.md, pyproject.toml and .github/workflows/tests.yml. No worker log was offered.

Checked and found correct:
- The manifest is valid. It has one phase, `depends_on: []`, so there is no unknown id and no cycle. Complexity is S. `brief`, `acceptance` and `touches` are all non-empty. `max_parallel` is 1. There are no `manual_*` items, so there are no id rules to apply.
- The single phase is also the retirement phase, so rule 7 holds.
- `touches` covers every file the brief changes, including the plan file it deletes. With one phase there is no wave conflict.
- No manual steps. The profile has no `ci.workflows`, so there is nothing that should go through ci-dispatch instead.
- I checked the D1 regex `[^a-z0-9]+` followed by `.strip("-")` by hand against all seven AC-1 to AC-4 cases. All seven give the expected value.
- The baseline is 6 passed, as the plan says. 6 + 7 = 13 matches the AC-6 item.
- ruff is installed as a module in `.venv`, so `python -m ruff` works. There is no ruff config, so the defaults apply: E501 is off and isort is off.
- The README alignment is right: `slugify("Hello World")` is 22 characters, the same as the other lines, so the 3-space gap keeps the `#` column.
- The plan does not contradict the acceptance criteria, the design, CLAUDE.md (no new dependencies, tests added, README updated) or the code.

## Findings

1. **blocking** · docs/sbx-x2-plan.md, manifest `acceptance`, last item · `git diff --quiet e2e/20261002-3 -- pyproject.toml sandbox_pkg/numbers.py` names a local branch that does not exist. The base branch exists only as `refs/remotes/origin/e2e/20261002-3` (from `git for-each-ref`). Git resolves `e2e/20261002-3` against `refs/heads/` and `refs/remotes/<name>` only, so the command fails with "ambiguous argument" (exit 128) and the item can never pass. · Use `origin/e2e/20261002-3`, for example `git diff --quiet origin/e2e/20261002-3 -- pyproject.toml sandbox_pkg/numbers.py exits 0`. Base commit `3393439` = `origin/e2e/20261002-3` = the merge-base of HEAD.
2. **non-blocking** · docs/sbx-x2-plan.md, "Current state", README bullet · The line references are wrong. The intro sentence is at `README.md:5-6`, not 3-4, and `## Usage` with its code block is at `README.md:8-17`, not 6-15. D3 also says "Line 3-4". The brief finds the text by its content, so a worker will not go wrong, but the plan's own `path:line` claims are inaccurate. · Change them to 5-6 and 8-17.
3. **non-blocking** · docs/sbx-x2-plan.md, "Current state", Checks bullet · The plan says "Checks (profile)", but `.claude/project-profile.yaml` has `commands: {}`. The commands come from CLAUDE.md, which spells them `.venv/bin/pytest -q` and `.venv/bin/ruff check .`. AC-5 and AC-6 also use those spellings. The `python -m` forms the plan uses are equivalent here, since both are installed in `.venv`. · Cite CLAUDE.md as the source, or use the CLAUDE.md spellings so they match the AC text.
4. **non-blocking** · docs/sbx-x2-plan.md, brief step 7 (and step 5) · The stop rule for ruff failures exists only in "Risks and open questions": fix only formatting, and stop with `status=blocked` if a fix would change behaviour. The brief tells the worker to read D1 to D3 only, so step 7 has no stop condition. · Add to step 7: "If ruff reports a rule that needs a behaviour change to fix, or the full suite is not 13 passed, stop with status=blocked."
5. **non-blocking** · docs/sbx-x2-plan.md, acceptance item labelled AC-7 · `grep -c recieve README.md prints 0` is tagged AC-7, but the typo fix is not an acceptance criterion. design.md says it is optional and out of scope. Also, `grep -c` exits 1 when it prints 0, so a checker that looks at exit codes will report a failure. · Move the typo check to its own item without the AC-7 tag and phrase it as "`grep -q recieve README.md` exits 1", or keep "prints 0" and say that exit 1 is expected.
6. **non-blocking** · docs/sbx-x2-plan.md, scope · Under plan skill section 0 step 5, a change that fits one S phase is "small scope" and should produce `RUN/prompt.md`, not a plan document. The conductor explicitly asked for one phase, and a T2 plan may have 1 to 3 phases, so the plan follows the conductor's request. This is noted only so the hand-back can say so. · No change needed. Mention it in the hand-back note.
7. **non-blocking** · docs/ (untracked) · `docs/sbx-x2-plan.md` is not committed yet (`git status` shows `?? docs/`). Brief step 6 uses `git rm`, which only works on a tracked file. · Commit the plan on `plan/sbx-x2` before `/ns:implement` starts, as plan section 5 requires.

## Summary

The plan is small, settled and mechanical. Design D1 to D3 leave no open decisions, the brief contains no "choose", "consider" or "e.g.", and the manifest passes every plan-manifest validation rule. The one blocker is the last acceptance command, which points at a branch ref that does not exist locally and so always fails. Fix that ref to `origin/e2e/20261002-3`. The other findings are line-reference accuracy and stop-condition wording.

REVIEW verdict=changes
