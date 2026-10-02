tier: T0
size_tier: T0
risk_floor: none
tags: [python, docs]
budget_hours: 1
summary: Fix the typo "recieve" to "receive" in README.md

## Reasons
- Size: one-word documentation fix in a single file, no code or behaviour change.
- Risk: the profile defines no risk zones, platform paths or specialists, so no floor applies (risk_floor none).
- Not higher: no invariant or trust boundary is touched. README.md is not a runtime path.
- Note: CLAUDE.md asks for a test per change, but a pure docs typo has no testable behaviour. The caller may waive this.
