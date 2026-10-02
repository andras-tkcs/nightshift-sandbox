# Plan review: sbx-x4

I checked the plan against the `plan` skill ("Sizing for Sonnet", manual steps, retirement), the `plan-manifest` validation rules, `acceptance.md`, `design.md`, `triage.md`, `.claude/project-profile.yaml`, `CLAUDE.md` and the repo code (`sandbox_pkg/text.py`, `tests/test_text.py`, `tests/test_numbers.py`, `README.md`, `pyproject.toml`, `.github/workflows/tests.yml`). No worker log or reasoning was offered, and I used none.

## Findings

1. **non-blocking · docs/sbx-x4-plan.md:16 · The plan says the checks come "from the profile", but the profile has `commands: {}` and declares no checks.** The project's commands are in `CLAUDE.md` (`.venv/bin/pytest -q`, `.venv/bin/ruff check .`), and AC-6 uses those exact forms. CI also runs bare `ruff check .` / `pytest -q` after `pip install -e .`, so it is not "the same two commands." The plan uses `.venv/bin/python -m pytest` instead. That form puts the current directory on `sys.path`, so it can pass where `.venv/bin/pytest` fails to import `sandbox_pkg` (for example, if the venv lacks an editable install). The manifest could then go green while AC-6, checked literally, fails. **Fix:** give the right source (`CLAUDE.md`) in "Current state". Use AC-6's exact commands `.venv/bin/pytest -q` and `.venv/bin/ruff check .` in brief steps 2 and 7, in the phase `acceptance` and in `verify_after_merge`, or add them alongside the current ones.

2. **non-blocking · docs/sbx-x4-plan.md:131,162 · `git diff --quiet e2e/20261002-5 -- …` assumes a local branch `e2e/20261002-5` exists in the phase worktree and the conductor's checkout.** A fresh worktree may only have `origin/e2e/20261002-5`. The command then fails with "unknown revision", which is a false failure rather than a real one. **Fix:** use `origin/e2e/20261002-5` (or `$(git merge-base HEAD origin/e2e/20261002-5)`). Add a stop condition: if the ref does not resolve, stop with `status=blocked` rather than switching to another ref.

3. **non-blocking · docs/sbx-x4-plan.md:153 · The only phase deletes the plan document that it is reviewed against.** This is allowed: with one phase, rule 7 is met because the last phase depends on all the (zero) other phases and does the retirement. The per-phase reviewer and `/ns:implement` will need the plan from the plan branch, not from the phase branch. This is a note for the conductor, and no change to the plan is needed. It would be optional to make step 8 explicit: "delete only after steps 3–7 pass."

4. **non-blocking · docs/sbx-x4-plan.md:27-31 · D1's docstring has several lines.** "Current state" itself says the module uses one-line docstrings (`text.py:5,10`). It is harmless, and ruff's default rules don't flag it. **Fix (optional):** shorten it to one line, such as `"""Return text as a lowercase slug: non-alphanumeric runs become one hyphen."""`, to match the module style.

## Checks that passed

- **Sizing for Sonnet:** one phase, complexity S. About 7 source lines in one source file; tests and the README are on top of that. The steps are numbered and name every file and symbol, with all code and text given verbatim in D1–D3. No brief contains "choose / decide / consider / if appropriate / e.g.". Every risky step has a stop condition: a stale "Current state" (step 1), a red baseline (step 2), ruff or a test failing (step 7).
- **No open decision in the brief:** the rename question is kept as an owner question for gate 1 (Risks 1), as the conductor asked. The brief keeps the name `titlecase`.
- **Waves and touches:** there is only one phase and `max_parallel: 1`, so no two phases can share touches. `touches` lists every file the brief changes, including the plan deletion.
- **Manual steps:** none. Everything is a local command, there is nothing manual in the middle, and nothing is called manual that CI could run.
- **Contradictions:** the plan matches `design.md` (algorithm, placement, the `###` subsection under `## Usage`, no type hints, `re`/`\w` rejected) and the code as it is (line numbers, line 1 of the test file, README layout). The 6 existing tests (4 + 2) plus 5 new tests give 11. The plan adds no dependencies, which matches `CLAUDE.md`. There is no contributing doc or ADR directory to contradict.
- **Manifest validation:** `plan_slug`, `feature_branch` and `phases` are present. The id `p1-titlecase` is unique and matches `p<n>-<kebab>`. `depends_on: []` means there is no cycle. Complexity is S. `brief`, `acceptance` and `touches` are not empty. `max_parallel` is 1. No `model` key is set. `manual_*` are empty. The single phase is the retirement phase.
- **AC coverage:**
  - AC-1, AC-2, AC-3, AC-4 and AC-5 are each covered by one named test (D2). I traced each example through D1 by hand, and all of them give the expected values.
  - AC-6 is covered by the pytest and ruff acceptance (see finding 1 about the command form).
  - AC-7 is covered by D3 plus two greps.
  - AC-8 is covered by `git diff --quiet … -- pyproject.toml` (see finding 2 about the ref).

## Summary

The plan is ready to implement. It has one phase, it is mechanical, everything the worker copies is given verbatim, and it covers AC-1 to AC-8. It keeps the requested name `titlecase` and leaves the rename as an owner question for gate 1, as the conductor asked. I found no blocking issues. I recommend fixing the check commands (finding 1) and the base ref (finding 2) before handing it over.

Verdict: approve (no blocking findings; 4 non-blocking).
