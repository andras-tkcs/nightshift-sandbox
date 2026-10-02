tier: T1
size_tier: T1
risk_floor: none
tags: [python]
budget_hours: 2
summary: Add titlecase(text) slug-style helper to sandbox_pkg/text.py with tests and a README section
---
## Reasons

- Size: one new pure function in one module, one test file, one README section. Three files, no new dependencies, no unknowns, no packaging or cross-platform impact.
- It adds one public function and docs, which is the only thing pushing it above T0. It is a single small phase, so it is T1 and not T2.
- Risk: the profile declares no risk_zones, platform_paths, invariants or specialists. No path match, so risk_floor is none.
- tier = max(T1, none) = T1. budget_hours is 2, from budgets.T1.hours.
- The owner set T2 (budget 3 hours). This file records the triage recommendation only. The owner's override stands.
- Note for the implementer: the name `titlecase` does not match the described behaviour. The request describes slugify (lowercase, hyphens), not title casing. Follow the spec text, and consider confirming the name with the owner.
- Edge cases to test: empty string, only punctuation, runs of mixed spaces and punctuation, leading and trailing separators, non-ASCII input.
