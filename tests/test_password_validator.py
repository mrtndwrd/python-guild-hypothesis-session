from password_validator.password_validator import validate_password
from hypothesis import given, strategies as st
from hypothesis.strategies import composite


@composite
def password_and_size(draw, min_size=10, max_size=200):
    # Ensure password is at least 8 characters
    size = draw(st.integers(min_value=max(min_size, 8), max_value=max_size))

    # Required characters from each category
    required_chars = [
        draw(st.sampled_from("abcdefghijklmnopqrstuvwxyz")),
        draw(st.sampled_from("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),
        draw(st.sampled_from("0123456789")),
        draw(st.sampled_from("!@#$%^&*"))
    ]

    # Generate remaining characters and form password
    remaining_chars = draw(
        st.text(
            alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*",
            min_size=size - 4,
            max_size=size - 4
        )
    )

    # Combine required and remaining characters, shuffle, and return
    password = draw(st.permutations(''.join(required_chars) + remaining_chars))

    return ''.join(password), size

      
@given(password_and_size())
def test_password_length_requirement(password_and_size_tuple):
    password, size = password_and_size_tuple
    assert len(password) == size
    if size >= 8:
        assert validate_password(password)  # Check validation if size meets min length


# Test uppercase, lowercase, digit, and special character requirements separately
@given(password_and_size(min_size=8))
def test_password_with_uppercase(password_and_size_tuple):
    password, _ = password_and_size_tuple
    has_uppercase = any(char.isupper() for char in password)
    if has_uppercase:
        assert validate_password(password)


@given(password_and_size(min_size=8))
def test_password_with_lowercase(password_and_size_tuple):
    password, _ = password_and_size_tuple
    has_lowercase = any(char.islower() for char in password)
    if has_lowercase:
        assert validate_password(password)


@given(password_and_size(min_size=8))
def test_password_with_digit(password_and_size_tuple):
    password, _ = password_and_size_tuple
    has_digit = any(char.isdigit() for char in password)
    if has_digit:
        assert validate_password(password)


@given(password_and_size(min_size=8))
def test_password_with_special_character(password_and_size_tuple):
    password, _ = password_and_size_tuple
    has_special = any(char in "!@#$%^&*" for char in password)
    if has_special:
        assert validate_password(password)


# Test completely invalid passwords (e.g., missing all criteria)
@given(st.text(max_size=7, alphabet="abcdefghijklmnopqrstuvwxyz"))
def test_completely_invalid_password(password):
    # Short, lowercase-only passwords should fail
    assert not validate_password(password)
