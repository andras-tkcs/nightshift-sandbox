tier: T0
size_tier: T0
risk_floor: none
tags: [python, docs]
budget_hours: 1
summary: Add THIRD.md containing the line "third run"

## Reasons
- Size: one new plain-text file, one line, no code or logic change.
- Profile has no risk zones, no platform_paths and no specialists, so nothing matches. risk_floor is none.
- No invariant or trust boundary is touched, so nothing raises the tier above T0.
- Budget from profile budgets.T0.hours = 1.
- Note: CLAUDE.md asks for a test for every change and a current README. The implementer should decide whether a trivial doc file needs either. This is not a tier issue.
- Used 1 tool call before writing (profile read only).
