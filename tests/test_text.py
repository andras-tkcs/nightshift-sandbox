from sandbox_pkg.text import count_vowels, reverse_words, word_count


def test_reverse_words():
    assert reverse_words("a b c") == "c b a"


def test_reverse_words_extra_spaces():
    assert reverse_words("  one   two ") == "two one"


def test_count_vowels_lowercase():
    assert count_vowels("banana") == 3


def test_count_vowels_none():
    assert count_vowels("rhythm") == 0


def test_word_count():
    assert word_count("the quick brown fox") == 4


def test_word_count_empty():
    assert word_count("") == 0


def test_word_count_whitespace_only():
    assert word_count("  \t\n ") == 0


def test_word_count_mixed_whitespace():
    assert word_count("  one\ttwo\nthree  ") == 3


def test_word_count_punctuation():
    assert word_count("it's a-b - c") == 4
