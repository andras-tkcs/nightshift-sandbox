# sbx-x3 security post-review (board)

Mode: post. Diff: `git diff origin/e2e/20261002-4...origin/feature/x3` (6 files, +267/-4). Read against `sec-pre.md`, `design.md` and `adr-nan-policy.md`. No worker logs or reasoning were offered or read.

## Findings

- non-blocking · tests/test_acceptance_sbx_x3.py:149 · `eval()` runs text taken from `README.md` with the default builtins available (checklist item 4). The README is a file in the repo with the same trust level as the test code, and it only runs under pytest, so it is not exploitable today. But a README edit could run any expression in CI. · Parse the example with `ast` and allow only a single `Call` to `word_count`/`clamp` with literal arguments, or at least pass `{"__builtins__": {}, ...}` as the namespace.

No blocking findings. Checklist results:
1. Secrets: the token, `Authorization:` and private-key greps over the whole diff found nothing.
2/3. Injection and shell: no SQL, shell, HTML or path building, and no shell scripts.
5/6. Authorization and paths: not applicable (pure in-process functions). The only file access is the test reading `README.md` through a fixed path.
7. Supply chain: no new dependencies. `pyproject.toml`, the CI workflows and the ruff config are unchanged.
9/10. Parsing and logging: nothing new in `sandbox_pkg/`. The error messages are constant strings.

## Required controls from sec-pre.md

| Control | Met | Evidence |
|---|---|---|
| `pyproject.toml` unchanged; no imports outside the stdlib; `numbers.py` does not import `math` | yes | Not in the diff file list; there are no added `import` lines in `sandbox_pkg/` |
| No I/O, logging, subprocess, eval/exec, network or file access in the functions | yes | The grep of the `sandbox_pkg/` diff for `open(`, `os.`, `subprocess`, `eval`, `exec`, `print(`, `logging` matched nothing |
| `clamp` checks NaN on all three arguments before comparing, then `low > high`, both raising `ValueError`; tests cover each NaN position and reversed bounds | yes | sandbox_pkg/numbers.py:14-17; tests/test_numbers.py `test_clamp_nan_{value,low,high}` and `test_clamp_low_greater_than_high`; acceptance AC-4 and AC-5 |
| `# noqa: PLR0124` applies to a single line only; no file-level or config suppression | yes | sandbox_pkg/numbers.py:14 is the only `noqa`; no ruff config in the diff |
| No change to `__init__.py`, `.github/workflows/`, or existing functions and tests | yes | None of these is in the diff; existing functions and tests are untouched (additions plus import-line edits only) |
| Error messages are constant strings with no interpolated arguments | yes | `"clamp() argument is NaN"`, `"clamp() low is greater than high"` |

## Risk zones

The profile (`.claude/project-profile.yaml`) defines no `risk_zones`, so the diff touches none. The caller requested this review; no risk zone made it mandatory.

## Compliance

The profile names no security, compliance or contributing docs, so no regime applies and there is no compliance table.

## Summary

The diff matches the design and the ADR: two pure library functions, no new dependencies, no I/O and no trust boundaries crossed. All six controls from the pre-review are met. One non-blocking hardening note covers the README `eval` in the acceptance test.

REVIEW verdict=approve
