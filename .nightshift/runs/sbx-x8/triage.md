tier: T0
size_tier: T0
risk_floor: none
tags: [python, docs]
budget_hours: 1
summary: Add NOTES.md containing the line "second run"

## Reasons
- Size: one new plain-text file, no code or behavior change, a single line of content.
- Risk: the profile defines no risk zones, no platform_paths and no specialists. No invariant or trust boundary is touched, so risk_floor is none.
- tier = max(T0, none) = T0. Budget is budgets.T0.hours = 1.
- CLAUDE.md asks for a test per change and a current README. A docs-only file has no behavior to test. A README mention is optional.
