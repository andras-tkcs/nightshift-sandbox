Previous attempt reported status=blocked and left changes uncommitted. Checks fail only because
tests/test_acceptance_sbx_x4.py still has the strict xfail marker (6 XPASS(strict)).
This is expected: per test-strategy.md, the phase removes the ACCEPTANCE marker constant and its six
uses in the same commit as the implementation. Do not change test assertions. Then expect 17 passed,
ruff clean, commit and push your branch, and write the phase report with status=done.
