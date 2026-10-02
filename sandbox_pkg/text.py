"""Text helpers."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def reverse_words(text):
    """Return the words of text in reverse order, joined by single spaces."""
    return " ".join(reversed(text.split()))


def count_vowels(text):
    """Return the number of vowels in text."""
    return sum(1 for ch in text if ch in "aeiou")


def slugify(text):
    """Return text as a lowercase, hyphen-separated slug of ASCII letters and digits."""
    return _NON_ALNUM.sub("-", text.lower()).strip("-")
