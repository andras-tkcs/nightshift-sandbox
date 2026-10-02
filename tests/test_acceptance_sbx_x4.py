"""Acceptance tests for sbx-x4: sandbox_pkg.text.titlecase and its README section.

titlecase is imported inside each test so collection works before it exists.
"""

import re
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"


def _titlecase():
    from sandbox_pkg.text import titlecase

    return titlecase


def test_ac1_import_and_basic_slug():
    titlecase = _titlecase()
    assert titlecase("Hello World") == "hello-world"
    assert titlecase("Hello, World!") == "hello-world"


def test_ac2_separator_runs_become_one_hyphen():
    titlecase = _titlecase()
    assert titlecase("a  ,-;  b") == "a-b"
    assert titlecase("a_b.c") == "a-b-c"


def test_ac3_no_leading_or_trailing_hyphen():
    titlecase = _titlecase()
    assert titlecase("  --Hi there!!  ") == "hi-there"


def test_ac4_degenerate_input():
    titlecase = _titlecase()
    assert titlecase("") == ""
    assert titlecase("!?  ...") == ""


def test_ac5_letters_and_digits_kept_lowercased():
    titlecase = _titlecase()
    assert titlecase("Version 2 ÉTÉ") == "version-2-été"


# Matches a README line such as: titlecase("Hello, World!")   # "hello-world"
_EXAMPLE = re.compile(r'titlecase\("((?:[^"\\]|\\.)*)"\)\s*#\s*"([^"]*)"')


def _readme_sections():
    """Split README.md into (heading, body) pairs, ignoring '#' inside code fences."""
    sections = []
    heading, body, in_fence = None, [], False
    for line in README.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and re.match(r"#{1,6} ", line):
            sections.append((heading, "\n".join(body)))
            heading, body = line, []
            continue
        body.append(line)
    sections.append((heading, "\n".join(body)))
    return [(h, b) for h, b in sections if h is not None]


def test_ac7_readme_section_shows_titlecase_example():
    examples = [ex for _, body in _readme_sections() for ex in _EXAMPLE.findall(body)]
    assert examples, "no README section shows titlecase with an input and its output"
    titlecase = _titlecase()
    for given, expected in examples:
        assert titlecase(given) == expected
