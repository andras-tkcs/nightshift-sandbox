"""Acceptance tests for run sbx-x2: sandbox_pkg.text.slugify (AC-1 to AC-4, AC-7).

Written before the implementation; they now run as normal tests.
"""

import ast
import re
from pathlib import Path

import pytest

from sandbox_pkg import text as text_module

README = Path(__file__).resolve().parent.parent / "README.md"

# A README example line such as: slugify("Hello World")   # "hello-world"
README_EXAMPLE = re.compile(r"""slugify\((?P<arg>.+?)\)\s*#\s*(?P<result>(["']).*\3)""")


def _slugify():
    """Return sandbox_pkg.text.slugify, failing with an assertion if it is missing."""
    func = getattr(text_module, "slugify", None)
    assert callable(func), "sandbox_pkg.text.slugify does not exist"
    return func


def test_ac1_slugify_lowercases_and_hyphenates_space():
    assert _slugify()("Hello World") == "hello-world"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello,  World!!  Again", "hello-world-again"),
        ("a--b__c..d", "a-b-c-d"),
    ],
)
def test_ac2_slugify_collapses_separator_runs(text, expected):
    assert _slugify()(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("  --Hello World!--  ", "hello-world"),
        ("!!!", ""),
        ("", ""),
    ],
)
def test_ac3_slugify_has_no_leading_or_trailing_hyphen(text, expected):
    assert _slugify()(text) == expected


def test_ac4_slugify_keeps_digits():
    assert _slugify()("Python 3.10 Release") == "python-3-10-release"


def test_ac7_readme_slugify_example_matches_function():
    examples = README_EXAMPLE.findall(README.read_text(encoding="utf-8"))
    assert examples, "README.md has no slugify example of the form slugify(...)  # '...'"
    slugify = _slugify()
    for arg, result, _quote in examples:
        assert slugify(ast.literal_eval(arg)) == ast.literal_eval(result)
