# ADR (unnumbered draft): clamp rejects NaN and reversed bounds

Status: Proposed
Date: 2026-10-02

Note: the project profile sets no `docs.adr_dir`, so this draft carries no number. It gets one when the owner names an ADR directory and the run is integrated.

## Context

- `clamp(value, low, high)` is new in `sandbox_pkg/numbers.py` (run sbx-x3, AC-3 to AC-5).
- The user story asks for "an error instead of a silent wrong answer when the range or input is invalid".
- The naive `max(low, min(value, high))` is silent and order-dependent with NaN: a NaN value becomes `low`, a NaN `high` is ignored (research.md, local run).
- Any comparison with NaN is False, so a `low > high` check alone does not catch NaN bounds.
- Precedent in the same module: `mean()` raises `ValueError("mean() of an empty sequence")` on invalid input.
- No dependencies may be added (CLAUDE.md), so NumPy semantics are not available as a library anyway.
- Open for the owner: propagation (return NaN, as NumPy `clip` does) is a reasonable alternative; acceptance.md assumes raise and says AC-5 changes if the owner decides otherwise. Whether infinities should be rejected is also open (assumed no).

## Decision

We will make `clamp` raise `ValueError` when any of `value`, `low` or `high` is NaN, checked first with the `x != x` idiom, and then raise `ValueError` when `low > high`. Messages name the function, as `mean()` does. Bounds are inclusive, `low == high` is valid, infinities are accepted, and the selected argument object is returned unchanged.

## Consequences

- Invalid input fails loudly at the call site; no silent wrong answers (user story, AC-4, AC-5).
- Callers that want IEEE propagation must check for NaN themselves before calling.
- Behaviour matches `mean()`, so the module has one error convention.
- Changing to propagation later is a behaviour change for callers and would need a superseding ADR.
- Tests must cover NaN in each of the three positions and `low > high` (AC-6).

## Alternatives considered

- Propagate NaN (return NaN if any argument is NaN): IEEE-consistent and matches NumPy `clip`, but contradicts the "error instead of silent wrong answer" story and the `mean()` precedent. Owner may still choose this.
- Leave NaN undefined: yields the order-dependent results above; rejected as a silent wrong answer.
- Swap reversed bounds: hides caller bugs; listed as a non-goal.
- Use `math.isnan`: requires an import and raises `TypeError` for types without a float conversion; `x != x` covers int and float without it.

## Appendix

Modules, interfaces, risks and rejected alternatives for the whole run are in `design.md` in this directory.
