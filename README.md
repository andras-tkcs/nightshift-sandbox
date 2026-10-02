# sandbox

A tiny Python package that Nightshift's end-to-end tests work on.

It helps you recieve text and do small things with it: reverse the words of a
sentence, count vowels and compute a mean.

## Usage

```python
from sandbox_pkg.text import reverse_words, count_vowels, word_count
from sandbox_pkg.numbers import mean, clamp

reverse_words("a b c")   # "c b a"
count_vowels("banana")   # 3
word_count("a b  c")     # 3
mean([1, 2, 3])          # 2.0
clamp(15, 0, 10)         # 10
```
