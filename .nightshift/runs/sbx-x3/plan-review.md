# Plan review: docs/sbx-x3-plan.md

Reviewer: ns:code-reviewer, fresh context. What I read: the plan, the plan and plan-manifest skills, acceptance.md, design.md, adr-nan-policy.md, research.md, triage.md, CLAUDE.md, .claude/project-profile.yaml, sandbox_pkg/, tests/, README.md, pyproject.toml and .github/workflows/tests.yml. I was not given any worker log. I ran no project commands: the sandbox did not approve running `ruff --show-settings`, so finding 1 rests on reading the config files.

## Findings

1. non-blocking · docs/sbx-x3-plan.md:62 (D2) and the p2-clamp brief, step 3 · The plan says the resolved ruff settings turn on PLR0124, so the `# noqa: PLR0124` is required. Nothing in the repo supports that. `pyproject.toml` has no `[tool.ruff]` section, there is no `ruff.toml` or `.ruff.toml` in the repo or its parent directories, and there is no `~/.config/ruff/`. With no config, ruff runs its default rules (E4, E7, E9, F), and those do not include PLR0124. CI installs a fresh ruff with the same lack of config. The comment is harmless because RUF100 is also off, so no check fails. But the plan states as checked fact something that looks false, and it would ship a noqa comment that does nothing. · Fix: run `.venv/bin/ruff check --show-settings sandbox_pkg/numbers.py` again. If PLR0124 is not in `linter.rules`, remove the noqa from D2 and from p2 step 3 and correct the reason. If it is listed, name the config file that turns it on.

2. non-blocking · docs/sbx-x3-plan.md:24 (Current state, "Checks (profile)") · `.claude/project-profile.yaml` has `commands: {}` and lists no checks. The commands come from CLAUDE.md (`.venv/bin/pytest -q`, `.venv/bin/ruff check .`). The plan's `.venv/bin/python -m ...` forms do the same thing (ruff and pytest are both installed in the venv), so nothing breaks, but the plan names the wrong source. · Fix: say "Checks (CLAUDE.md)", or use the CLAUDE.md commands as they are written.

3. non-blocking · docs/sbx-x3-plan.md:181 and the p3-retire brief, step 1 · Both ask the worker to confirm that "README.md lines 10-17 match the Usage block in Current state". Current state only describes the block in words; it never quotes it. So the worker cannot compare mechanically. · Fix: quote the current README lines 10-17 word for word in Current state (fence, two import lines, blank line, three example lines, fence).

4. non-blocking · docs/sbx-x3-plan.md:153-164 (D4) · D4 says "lines 10-19 read exactly" and then shows 8 lines. Lines 10 and 19 are the ```` ``` ```` fences, which the shown block leaves out. Read literally, that is ambiguous. The column math is right: 20+5 and 16+9 both put `#` at column 25. · Fix: say "lines 11-18 read exactly", or show the fences.

5. non-blocking · manifest `final_checks`: "README.md Usage block matches Design D4 of the plan" · p3-retire deletes the plan, and final_checks run after that. So this check points to a document that no longer exists on the feature branch, and it is not mechanical. · Fix: write the check as the four `grep -nF` lines from p3's acceptance, or quote the expected lines inside the check.

6. non-blocking · acceptance of p1-word-count and p2-clamp: "git diff --name-only for the phase's commits lists only ..." · This gives no command or range, so it is less mechanical than the other items. AC-9 needs it, so it should be exact. · Fix: give the command, for example `git diff --name-only <phase base>...HEAD`, and say the conductor fills in the base.

7. non-blocking · p2-clamp acceptance: "grep -c 'import math' sandbox_pkg/numbers.py prints 0" · When there is no match, `grep -c` prints `0` and exits with status 1. A worker who checks the exit status could read that as a failure. · Fix: write "prints 0 (exit status 1 is expected)", or use `! grep -q 'import math' sandbox_pkg/numbers.py exits 0`.

8. non-blocking · p3-retire acceptance · Brief step 6 says "do not change any other README line". Only the "recieve" count checks that. · Fix: add `git diff --numstat HEAD~1 -- README.md` (or the phase-base range) prints `4	2	README.md`. That is 2 lines changed and 2 lines added.

## Checked and found correct

- Manifest validation: the ids are unique and in `p<n>-kebab` form. Every `depends_on` names a phase in the list, and there is no cycle. Complexity is S everywhere. Every phase has a non-empty brief, acceptance and touches. `max_parallel` is 2 and both `manual_*` lists are empty. The last phase, p3-retire, depends on every other phase and deletes the plan (rule 7).
- Waves: p1 (`sandbox_pkg/text.py`, `tests/test_text.py`) and p2 (`sandbox_pkg/numbers.py`, `tests/test_numbers.py`) have disjoint touches. Only p3 touches README.md, and it depends on both (rule 3, AC-9).
- Sizing for Sonnet: every step is numbered and names files and symbols. The code and tests are given word for word. The briefs contain none of "choose", "decide", "consider", "if appropriate" or "e.g.". There are stop conditions for already-existing functions, changed import lines, an existing test failing, and ruff flagging the plan's own code.
- Manual steps: none, and correctly so. CI already runs ruff and pytest, so nothing needs ci-dispatch.
- Code as it is: the `path:line` references for text.py, numbers.py, both test files and README lines 5-6 and 10-17 are accurate. README lines 11 and 12 are the import lines, as p3 steps 2-3 assume.
- The design matches design.md, the ADR draft and acceptance.md: NaN check first, `x != x`, no `import math`, the exact error messages, inclusive bounds, infinities accepted, the selected argument object returned, punctuation-only tokens counted as words, no `__init__` re-exports, no new dependencies.
- Acceptance values, checked by hand: AC-1 gives `4 3 2` and AC-2 gives `0 0`. AC-3 gives `5 0 10 0 10 1.0 4`. `-k word_count` selects 5 tests and `-k clamp` selects 12. The tracebacks end in `ValueError: clamp() ...`. The README examples evaluate to `3 10`. The YAML `\"` escapes become the intended shell quoting.
- AC-8 base ref: there is no local `e2e/20261002-4` branch in this worktree, so the fallback to `origin/e2e/20261002-4` is needed and is given.
- The 3-phase deviation (a note for the owner, not a finding) is explained correctly. Rule 3 stops p1 and p2 from both touching README.md. A `depends_on` edge would break AC-9. Rule 7 calls for a retirement phase that handles reference docs. The cost to revertibility is stated honestly.

## Summary

The plan is sound and the manifest passes validation. Phases 1 and 2 are mechanical and independent. There are no blocking findings. The main thing to fix is the stated reason for `# noqa: PLR0124` (finding 1), which does not match the repo's ruff config. The rest are small changes to make the checks more exact.

REVIEW verdict=approve
