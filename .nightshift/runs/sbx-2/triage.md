tier: T0
size_tier: T0
risk_floor: none
tags: [python]
budget_hours: 1
summary: Make count_vowels count uppercase vowels (case-insensitive)

## Reasons
- Size: one-line change in sandbox_pkg/text.py (`ch in "aeiou"` is case-sensitive), plus one test and a README check.
- Profile defines no risk zones, platform_paths or specialists; nothing matched, so risk_floor is none.
- No invariant or trust boundary at stake. Tier stays T0.
