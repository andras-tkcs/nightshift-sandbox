# sandbox

A tiny Python package that Nightshift's end-to-end tests work on.

It helps you recieve text and do small things with it: reverse the words of a
sentence, count vowels and compute a mean.

## Usage

```python
from sandbox_pkg.text import reverse_words, count_vowels
from sandbox_pkg.numbers import mean

reverse_words("a b c")   # "c b a"
count_vowels("banana")   # 3
mean([1, 2, 3])          # 2.0
```

### titlecase

`titlecase(text)` turns text into a lowercase slug: each run of spaces and
punctuation becomes one hyphen, with no hyphen at either end. Despite its name,
it does not title-case text.

```python
from sandbox_pkg.text import titlecase

titlecase("Hello, World!")      # "hello-world"
titlecase("  --Hi there!!  ")   # "hi-there"
```
