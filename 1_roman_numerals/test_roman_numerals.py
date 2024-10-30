from hypothesis import given, strategies
import roman

from roman_numerals import to_roman_numerals

@given(strategies.integers(min_value=1, max_value=4999))
def test_round_trip_roman_numeral_conversion(number):
    roman_numeral = to_roman_numerals(number)
    result = roman.fromRoman(roman_numeral)
    assert result == number, f"Expected {number}, got {result}"