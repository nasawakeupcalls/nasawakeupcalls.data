# nasawakeupcalls.data

Data extracts and analysis from the NASA wake-up call project. This is a remix
project. Source Data is licensed to NASA. If NASA would like to commit to a
creative-commons license for this work to be used more widely, that would be
lovely.

Credit for the source material goes to Colin Fries of the NASA historical
division.

## Requirements

* `pip install nltk`
* With `nltk` installed run `python3`:

```
		import nltk
		nltk.download("punkt")
```
## Process

1. Tokenize output using `tokenize-nasawakeup.py`
2. This will leave `6779` lines that can be manipulated, I expect a mix of
   automated and manual intervention, e.g. to separate logical components,
   the intro, and the sources, from the data are two examples.
3. Not yet known.
