tier: T0
size_tier: T0
risk_floor: none
tags: [python]
budget_hours: 1
summary: Add NOTES.md containing the line 'second run'

## Reasons
- Size: one new plain-text file, no code, no behavior change.
- Profile has no risk zones or platform_paths, so no path match. No invariant or trust boundary is touched. risk_floor is none.
- tier = max(T0, none) = T0. Budget comes from budgets.T0.hours = 1.
- CLAUDE.md asks for a test per change and a current README. For a docs-only file these likely don't apply. The implementer should confirm.
