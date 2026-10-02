# Board acceptance: sbx-x3

Branch origin/feature/x3 (01418fe) against base e2e/20261002-4. Checks ran on a `git archive` export of origin/feature/x3 in /tmp/bx3.WrMk with PYTHONPATH set to it (sandbox_pkg.__file__ confirmed resolving to the export), using the worktree's .venv.

AC-1 met: `python -c '... print(w("the quick brown fox"), w("  one\ttwo\nthree  "), w("it'"'"'s a-b"))'` printed `4 3 2`; sandbox_pkg/text.py `word_count` returns `len(text.split())`, the same split as `reverse_words`.
AC-2 met: `python -c '... print(w(""), w("  \t\n "))'` printed `0 0`.
AC-3 met: `python -c '... print(c(5,0,10), c(-3,0,10), c(15,0,10), c(0,0,10), c(10,0,10), c(2.5,0.0,1.0), c(7,4,4))'` printed `5 0 10 0 10 1.0 4`.
AC-4 met: `clamp(5, 10, 0)` exited 1 with stderr `ValueError: clamp() low is greater than high`.
AC-5 met: `clamp(float("nan"), 0, 10)`, `clamp(5, float("nan"), 10)` and `clamp(5, 0, float("nan"))` each exited 1 with stderr `ValueError: clamp() argument is NaN`.
AC-6 met: tests/test_text.py:20-37 has word_count tests incl. empty (l.24) and whitespace-only (l.28); tests/test_numbers.py:49-66 has `pytest.raises(ValueError)` for low > high (l.49) and NaN value/low/high (l.54, 59, 64); `pytest -q -k "word_count or clamp"` gave `41 passed, 6 deselected`.
AC-7 met: README.md:11 `from sandbox_pkg.text import reverse_words, count_vowels, word_count`, README.md:12 `from sandbox_pkg.numbers import mean, clamp`, README.md:16 `word_count("a b  c")     # 3`, README.md:18 `clamp(15, 0, 10)         # 10`; running both examples printed `3 10`.
AC-8 met: `pytest -q` gave `47 passed`, exit 0; `ruff check .` gave `All checks passed!`, exit 0; `git diff --stat origin/e2e/20261002-4 origin/feature/x3 -- pyproject.toml` is empty (the AC's `git diff origin/main -- pyproject.toml` shows the whole file as new because origin/main has no pyproject.toml; it was added by the e2e base commit 19afe03, not by this branch, so the branch adds no dependency).
AC-9 met: commit 6096e1d (p1 word_count) touches sandbox_pkg/text.py, tests/test_text.py, tests/test_acceptance_sbx_x3.py only; commit e47055b (p2 clamp) touches sandbox_pkg/numbers.py, tests/test_numbers.py only; plan docs/sbx-x3-plan.md at 4990687 lines 212 and 237 give `depends_on: []` for both p1-word-count and p2-clamp.

Non-goals: the diff to sandbox_pkg/ and tests/test_text.py, tests/test_numbers.py only adds lines (reverse_words, count_vowels, mean and their tests unchanged); README typo untouched; no change to sandbox_pkg/__init__.py or pyproject.toml.

REVIEW verdict=approve
