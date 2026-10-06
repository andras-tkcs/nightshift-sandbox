tier: T0
size_tier: T0
risk_floor: none
tags: [python, docs]
budget_hours: 1
summary: Fix the typo "recieve" to "receive" in README.md
---

## Reasons

- Size: a one-word typo fix on README.md line 3, one file, no code or behaviour change.
- Risk: the profile lists no risk zones, platform paths or specialists. README.md matches none, and no invariant or trust boundary is touched, so the floor is none.
- Tier: max(T0, none) = T0. This matches the owner's T0. The T0 budget is 1 hour.
- Note: CLAUDE.md asks for a test per change and a current README. A docs-only typo fix needs no new test.
