# Python Guild Hypothesis Session

This is a session of the NS Python guilde about property based testing using the [Hypothesis library](https://hypothesis.readthedocs.io/en/latest/).

This session has two exercises that we will tackle in duos. The first is based on the "Roman numerals" kata. We will use an existing "from Roman numerals" function in conjunction with the Hypothesis testing library to guide our development of a not yet existing "to Roman numerals" function. This should familiarize us with Hypothesis' power of generating simple examples of failing test cases.

After we have made ourselves familiar with Hypothesis and with working with our duo, we will continue with a slightly more complicated Reflector Dish exercise based on day 14 of the 2023 [Advent of Code](https://adventofcode.com/2023/day/14).


## Setting up the project

If you haven't already, install Python. Then install Poetry (`pip install poetry` or `apt install python3-poetry`, or whatever works for your system).

After you have installed those dependencies, you should run:

```shell
poetry install
```

This will install Pytest, Hypothesis and Roman, a package that you will need in the first exercise.

## Getting started

Continue to [the Roman Numerals readme](./1_roman_numerals/README.md) to start the first session.
