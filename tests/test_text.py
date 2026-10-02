import pytest

from sandbox_pkg.text import count_vowels, reverse_words, slugify


def test_reverse_words():
    assert reverse_words("a b c") == "c b a"


def test_reverse_words_extra_spaces():
    assert reverse_words("  one   two ") == "two one"


def test_count_vowels_lowercase():
    assert count_vowels("banana") == 3


def test_count_vowels_none():
    assert count_vowels("rhythm") == 0


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello World", "hello-world"),
        ("Hello,  World!!  Again", "hello-world-again"),
        ("a--b__c..d", "a-b-c-d"),
        ("  --Hello World!--  ", "hello-world"),
        ("!!!", ""),
        ("", ""),
        ("Python 3.10 Release", "python-3-10-release"),
    ],
)
def test_slugify(text, expected):
    assert slugify(text) == expected
