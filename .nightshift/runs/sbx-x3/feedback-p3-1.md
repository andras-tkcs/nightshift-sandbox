# Restart feedback (conductor)
Blocked because the AC-7 tests in `tests/test_acceptance_sbx_x3.py` (test_ac7_readme_documents_word_count, test_ac7_readme_documents_clamp) are still `xfail(strict=True)` and now XPASS once the README is edited.
Allowed exception to `touches`: remove ONLY the xfail markers on those two AC-7 tests (no assertion changes), in the same commit as the README edits. Then delete the plan doc as the brief says (if the acceptance file is also to be retired per the brief, follow the brief). Ruff and full pytest must pass; commit and push.
