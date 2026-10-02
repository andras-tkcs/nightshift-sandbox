from sandbox_pkg.text import count_vowels, reverse_words


def test_reverse_words():
    assert reverse_words("a b c") == "c b a"


def test_reverse_words_extra_spaces():
    assert reverse_words("  one   two ") == "two one"


def test_count_vowels_lowercase():
    assert count_vowels("banana") == 3


def test_count_vowels_none():
    assert count_vowels("rhythm") == 0


def test_count_vowels_uppercase():
    assert count_vowels("AEIOU") == 5


def test_count_vowels_mixed_case():
    assert count_vowels("Banana") == 3
