tier: T3
size_tier: T1
risk_floor: none
tags: [python]
budget_hours: 4
summary: Add word_count(text) and clamp(value, low, high) as two independent phases, each with tests and a README line
## Reasons
- Size signals: two small pure functions in two separate existing modules, with tests and README lines. No new dependencies. Size alone is T1.
- Risk: the profile defines no risk zones, no platform_paths and no specialists. No invariant or trust boundary is touched, so risk_floor is none.
- The owner set tier T3, so tier is T3 and budget_hours is 4 (budgets.T3.hours). This is an owner override of the size estimate.
- The request asks for two phases with disjoint files (sandbox_pkg/text.py with tests/test_text.py, and sandbox_pkg/numbers.py with tests/test_numbers.py). The only shared file is README.md, so the phases may conflict there at merge.
