tier: T1
size_tier: T1
risk_floor: none
tags: [python]
budget_hours: 2
summary: Add slugify(text) to sandbox_pkg/text.py with tests and a README section
## Reasons
- Size: one new pure function in sandbox_pkg/text.py, one test file (tests/test_text.py) and a README section. Three files, no unknowns, no packaging or cross-platform impact.
- New public surface is a single small function, which keeps this at T1 rather than T0. It is more than a one-file obvious fix, and CLAUDE.md requires tests and README updates.
- Risk: the profile declares no risk_zones, no platform_paths and no specialists. No invariant or trust boundary is touched, so the floor is none.
- Tier is max(T1, none) = T1. Budget is budgets.T1.hours = 2.
