# sandbox

A tiny Python package that Nightshift's end-to-end tests work on.

It helps you receive text and do small things with it: reverse the words of a
sentence, count vowels, make a slug and compute a mean.

## Usage

```python
from sandbox_pkg.text import reverse_words, count_vowels, slugify
from sandbox_pkg.numbers import mean

reverse_words("a b c")   # "c b a"
count_vowels("banana")   # 3
slugify("Hello World")   # "hello-world"
mean([1, 2, 3])          # 2.0
```
