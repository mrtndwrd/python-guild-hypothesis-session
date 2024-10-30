# Roman numerals with Hypothesis

## Prerequisites

Make sure you have followed "Setting up the project" in [the project README](../README.md) before you start here.

## Exercise

For this exercise we are going to write a "to Roman numerals" function that accepts an integer and returns its string representation as Roman numeral. Some examples: `1 -> "I"`, `2 -> "II"`, `5 -> "V"`, `9 -> "IX"`, etc. Refer to [Wikipedia](https://en.wikipedia.org/wiki/Roman_numerals) for a complete rule set.

Property based testing works very well if you have two functions that are the inverse of each other (an "encode" and a "decode" function, for example). If you run both functions on some input, they should return that same input. In `test_roman_numerals.py` we have included a Hypothesis test that uses the existing `fromRoman` function from the [roman](https://pypi.org/project/roman/) library. We could of course also use the `toRoman` function from that library, but today we are going to write our own (maybe better? More efficient?) variant. Finish the function in `roman_numerals.py`. We have already given you an implementation that works for integers 1 to 3!

To start the tests, run the following command. It will re-run the test every time you save your code.

```shell
poetry run ptw
```

Let's see how far you can get in the time we're giving you!
