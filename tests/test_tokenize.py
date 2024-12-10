import pytest

from tokenizer import tokenize


TOKENIZE_FIXTURES = [
    # Simple arithmetic
    ("5 + 4", ["5", "+", "4"]),
    ("x_y = 5 + 4", ["x_y", "=", "5", "+", "4"]),
    ("5 + 4 * x_y", ["5", "+", "4", "*", "x_y"]),
    ("5 + (4 - 2)", ["5", "+", "(", "4", "-", "2", ")"]),
    # Unary plus/minus
    ("-5 + 4", ["-5", "+", "4"]),  # negative number
    ("5 + -4", ["5", "+", "-4"]),  # negative number after operator
    ("x = -y + 4", ["x", "=", "-", "y", "+", "4"]),  # unary minus on variable
    ("x = -3 + 4", ["x", "=", "-3", "+", "4"]),  # negative number as expression
    ("x = y + -3", ["x", "=", "y", "+", "-3"]),  # negative number after variable
    # More complex expressions with parentheses and mixed operations
    ("x = 5 + 4", ["x", "=", "5", "+", "4"]),
    (
        "x = y + 5 * 4 + (5 / 2)",
        ["x", "=", "y", "+", "5", "*", "4", "+", "(", "5", "/", "2", ")"],
    ),
    # Increment/Decrement operators
    ("x = y++", ["x", "=", "y", "++post"]),
    ("x = ++y", ["x", "=", "++pre", "y"]),
    ("x = y++ - 1", ["x", "=", "y", "++post", "-", "1"]),
    ("x = ++y - 1", ["x", "=", "++pre", "y", "-", "1"]),
    ("x = y++ + ++z", ["x", "=", "y", "++post", "+", "++pre", "z"]),
    ("x = y++ + z", ["x", "=", "y", "++post", "+", "z"]),
    # ("x = y+++++z", ["x", "=", "y", "++", "+", "++", "z"]),
    ("x = y++ + z--", ["x", "=", "y", "++post", "+", "z", "--post"]),
    ("x = y-- + z++", ["x", "=", "y", "--post", "+", "z", "++post"]),
    ("x = --y + z--", ["x", "=", "--pre", "y", "+", "z", "--post"]),
    ("x = --y + --z", ["x", "=", "--pre", "y", "+", "--pre", "z"]),
    ("--y + --z", ["--pre", "y", "+", "--pre", "z"]),
    ("y++ + z++", ["y", "++post", "+", "z", "++post"]),
    ("y-- + z--", ["y", "--post", "+", "z", "--post"]),
    # Compound assignment operators
    ("x +=++z", ["x", "+=", "++pre", "z"]),
    ("x -= x-- - --y", ["x", "-=", "x", "--post", "-", "--pre", "y"]),
    ("x -= x-- + --y", ["x", "-=", "x", "--post", "+", "--pre", "y"]),
    ("x -= x-- + ++y", ["x", "-=", "x", "--post", "+", "++pre", "y"]),
    # Edge cases
    (
        "x = y++ * --z",
        ["x", "=", "y", "++post", "*", "--pre", "z"],
    ),  # Mixture of increment and multiplication
    ("x =++y", ["x", "=", "++pre", "y"]),  # Complex operator combinations
    ("x + = y", ["x", "+", "=", "y"]),  # Spaces around operator
    (
        "x++ + y",
        ["x", "++post", "+", "y"],
    ),  # Simple combination of increment and addition
    (
        "x++ + ++y",
        ["x", "++post", "+", "++pre", "y"],
    ),  # Five consecutive operators (split correctly)
    (
        "x = y++ + ++z",
        ["x", "=", "y", "++post", "+", "++pre", "z"],
    ),  # Consecutive increments mixed
]


@pytest.mark.parametrize("expression, expected", TOKENIZE_FIXTURES)
def test_tokenize(expression, expected):
    result = tokenize(expression)
    result = [token.value for token in result]
    assert result == expected


INVALID_EQUALITY_FIXTURES = ["x == 5", "x != 5", "x == y", "x  === 5", "x = y = 5"]

TOO_MANY_OPERATORS_FIXTURES = [
    "x ++++++ y",
    "x+++y",
]  # tokenizing doesn't validate everything, only the structure of the expression


@pytest.mark.parametrize(
    "expression", INVALID_EQUALITY_FIXTURES + TOO_MANY_OPERATORS_FIXTURES
)
def test_invalid_tokenize(expression):
    with pytest.raises(ValueError):
        tokenize(expression)
