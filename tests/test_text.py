from sandbox_pkg.text import count_vowels, reverse_words, titlecase


def test_reverse_words():
    assert reverse_words("a b c") == "c b a"


def test_reverse_words_extra_spaces():
    assert reverse_words("  one   two ") == "two one"


def test_count_vowels_lowercase():
    assert count_vowels("banana") == 3


def test_count_vowels_none():
    assert count_vowels("rhythm") == 0


def test_titlecase_basic():
    assert titlecase("Hello World") == "hello-world"
    assert titlecase("Hello, World!") == "hello-world"


def test_titlecase_collapses_separator_runs():
    assert titlecase("a  ,-;  b") == "a-b"
    assert titlecase("a_b.c") == "a-b-c"


def test_titlecase_strips_edge_separators():
    assert titlecase("  --Hi there!!  ") == "hi-there"


def test_titlecase_degenerate_input():
    assert titlecase("") == ""
    assert titlecase("!?  ...") == ""


def test_titlecase_keeps_unicode_letters_and_digits():
    assert titlecase("Version 2 ÉTÉ") == "version-2-été"
