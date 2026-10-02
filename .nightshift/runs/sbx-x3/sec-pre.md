# sbx-x3 security pre-review (design)

Inputs: `.nightshift/runs/sbx-x3/design.md`, `docs/sbx-x3-plan.md`, `adr-nan-policy.md` (context), profile `.claude/project-profile.yaml`. No worker logs were offered or read.

## Profile

- `risk_zones`: none defined. No zone is touched; this review was requested by the caller and is not mandated by a zone.
- Profile names no security, compliance or contributing docs, so no regime applies and there is no compliance table.

## Threat-model delta

- New assets: none. No secrets, credentials, files, network, persistent state or schemas (design "Data: None").
- New entry points: two pure library functions, `sandbox_pkg.text.word_count(text)` and `sandbox_pkg.numbers.clamp(value, low, high)`. Callers are in-process Python code only.
- New actors: none. No CLI, server, subprocess or environment input.
- Trust boundaries touched: none. Arguments come from the calling program, which already runs with full privileges in the same process. No deserialization, `eval`/`exec`, shell, path handling, logging or format strings with untrusted data.
- Supply chain: no new dependencies (CLAUDE.md, AC-8); `pyproject.toml` untouched; no `math` import needed.
- Residual, accepted: `word_count` on very large input allocates a list of tokens (O(n) memory), the same as existing `reverse_words`; not a concern for a library helper. `x != x` on exotic types with custom `__ne__` is unspecified; out of scope per design. The safety-relevant property is correctness (no silent wrong answer), covered by the controls below.

## Required controls (checkable)

- [ ] `pyproject.toml` unchanged against base `e2e/20261002-4`; no new imports outside the standard library, and `sandbox_pkg/numbers.py` does not import `math`.
- [ ] Neither function performs I/O, logging, subprocess, `eval`/`exec`, network or file access (grep of the diff for `open(`, `os.`, `subprocess`, `eval`, `exec`, `print(`, `logging` finds nothing new in `sandbox_pkg/`).
- [ ] `clamp` checks NaN for all three arguments before any comparison, then `low > high`, both raising `ValueError` with the messages in plan D2; tests cover NaN in each position and reversed bounds.
- [ ] The `# noqa: PLR0124` suppression is scoped to the single NaN-check line; no file-level or config-level ruff suppression is added and no ruff config is introduced.
- [ ] No change to `sandbox_pkg/__init__.py`, CI workflow (`.github/workflows/`), or existing functions/tests.
- [ ] Error messages are constant strings and do not interpolate argument values.

## Summary

Low-risk design: two pure functions, no I/O, no new assets, entry points across a trust boundary, or dependencies. The design is safe as written; the controls above are for the post-review to confirm.

REVIEW verdict=approve
