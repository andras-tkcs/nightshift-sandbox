# Restart feedback (conductor)
The first attempt stopped as blocked: `tests/test_acceptance_sbx_x3.py` already exists on the branch with `xfail(strict=True, reason="ns:sbx-x3 acceptance")` markers on the tests for your phase. Once your function exists they XPASS and strict mode fails `pytest -q`.
Per that file's own docstring, the phase that implements a function removes the xfail markers of its own acceptance tests in the same commit. So, as an allowed exception to the brief's `touches` and "single commit" rules:
- Implement as the brief says.
- In `tests/test_acceptance_sbx_x3.py`, remove ONLY the xfail markers on the acceptance tests that cover your own function (word_count: AC-1, AC-2 tests; clamp: the clamp ACs). Do not weaken or edit any assertion, and leave other phases' and the README markers alone.
- Run ruff and the full pytest; both must pass. One commit, then push.
