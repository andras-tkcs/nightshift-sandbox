"""Acceptance tests for run sbx-x3 (word_count and clamp).

Each test is a strict expected failure until the phase that implements its
criterion removes the marker in the same commit as the implementation:

- p1-word-count: test_ac1_*, test_ac2_*
- p2-clamp: test_ac3_*, test_ac4_*, test_ac5_*
- p3-retire: test_ac7_*

The functions are imported inside each test so that collection succeeds
before they exist.
"""

import ast
from pathlib import Path

import pytest

ACCEPTANCE = pytest.mark.xfail(strict=True, reason="ns:sbx-x3 acceptance")

README = Path(__file__).resolve().parent.parent / "README.md"


# AC-1: word_count counts whitespace-separated words, like reverse_words.


@ACCEPTANCE
@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("the quick brown fox", 4),
        ("  one\ttwo\nthree  ", 3),
        ("it's a-b", 2),
        ("it's a-b - c", 4),
    ],
)
def test_ac1_word_count_counts_words(text, expected):
    from sandbox_pkg.text import word_count

    assert word_count(text) == expected


@ACCEPTANCE
def test_ac1_word_count_matches_reverse_words():
    from sandbox_pkg.text import reverse_words, word_count

    text = "  alpha\tbeta\n gamma  -  "
    assert word_count(text) == len(reverse_words(text).split(" "))


# AC-2: word_count returns 0 for empty and whitespace-only text.


@ACCEPTANCE
@pytest.mark.parametrize("text", ["", "  \t\n "])
def test_ac2_word_count_empty_is_zero(text):
    from sandbox_pkg.text import word_count

    assert word_count(text) == 0


# AC-3: clamp returns value, low or high; bounds inclusive; ints and floats.


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        ((5, 0, 10), 5),
        ((-3, 0, 10), 0),
        ((15, 0, 10), 10),
        ((0, 0, 10), 0),
        ((10, 0, 10), 10),
        ((2.5, 0.0, 1.0), 1.0),
        ((7, 4, 4), 4),
        ((float("inf"), 0, 10), 10),
        ((float("-inf"), 0, 10), 0),
    ],
)
def test_ac3_clamp_limits_value(args, expected):
    from sandbox_pkg.numbers import clamp

    result = clamp(*args)
    assert result == expected
    assert type(result) is type(expected)


def test_ac3_clamp_check_command_output():
    from sandbox_pkg.numbers import clamp as c

    printed = " ".join(
        str(x)
        for x in (
            c(5, 0, 10),
            c(-3, 0, 10),
            c(15, 0, 10),
            c(0, 0, 10),
            c(10, 0, 10),
            c(2.5, 0.0, 1.0),
            c(7, 4, 4),
        )
    )
    assert printed == "5 0 10 0 10 1.0 4"


# AC-4: clamp raises ValueError when low > high.


def test_ac4_clamp_reversed_bounds_raises():
    from sandbox_pkg.numbers import clamp

    with pytest.raises(ValueError):
        clamp(5, 10, 0)


# AC-5: clamp raises ValueError when any argument is NaN.


@pytest.mark.parametrize(
    "args",
    [
        (float("nan"), 0, 10),
        (5, float("nan"), 10),
        (5, 0, float("nan")),
        (5, float("nan"), float("nan")),
    ],
    ids=["value", "low", "high", "both-bounds"],
)
def test_ac5_clamp_nan_raises(args):
    from sandbox_pkg.numbers import clamp

    with pytest.raises(ValueError):
        clamp(*args)


# AC-7: README Usage block documents both functions with checked examples.


def _usage_lines():
    text = README.read_text(encoding="utf-8")
    block = text.split("```python", 1)[1].split("```", 1)[0]
    return [line for line in block.splitlines() if line.strip()]


def _check_example(name):
    from sandbox_pkg.numbers import clamp
    from sandbox_pkg.text import word_count

    examples = [line for line in _usage_lines() if line.startswith(name + "(")]
    assert len(examples) == 1, examples
    code, comment = examples[0].split("#", 1)
    namespace = {"word_count": word_count, "clamp": clamp}
    assert eval(code.strip(), namespace) == ast.literal_eval(comment.strip())


@ACCEPTANCE
def test_ac7_readme_documents_word_count():
    lines = _usage_lines()
    imports = [
        line for line in lines if line.startswith("from sandbox_pkg.text import")
    ]
    assert len(imports) == 1
    assert "word_count" in imports[0].split("import", 1)[1].replace(",", " ").split()
    _check_example("word_count")


@ACCEPTANCE
def test_ac7_readme_documents_clamp():
    lines = _usage_lines()
    imports = [
        line for line in lines if line.startswith("from sandbox_pkg.numbers import")
    ]
    assert len(imports) == 1
    assert "clamp" in imports[0].split("import", 1)[1].replace(",", " ").split()
    _check_example("clamp")
