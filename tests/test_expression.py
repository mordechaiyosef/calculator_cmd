import pytest
from models.expression import Expression

POSTFIX_FIXTURES = [
    # Simple arithmetic
    ("x = 5 + 4", ["5", "4", "+"]),
    ("5 + 4", ["5", "4", "+"]),
]


@pytest.mark.parametrize("expression, expected", POSTFIX_FIXTURES)
def test_tokenize(expression, expected):
    result = Expression.from_expression(expression)
    result = result.to_postfix()
    result = [token.value for token in result]
    assert result == expected


VALID_EXPRESSIONS = [
    # Assignments with expected variable_name, operator, and tokens
    ("x = y++ + ++z", ("x", "=", ["y", "++post", "+", "++pre", "z"])),
    ("x = y + ++z", ("x", "=", ["y", "+", "++pre", "z"])),
    ("x = ++y + ++z", ("x", "=", ["++pre", "y", "+", "++pre", "z"])),
    ("x = y + x++", ("x", "=", ["y", "+", "x", "++post"])),
    # No assignment, variable_name and operator should be None
    ("x++ + ++y", (None, None, ["x", "++post", "+", "++pre", "y"])),
    ("y-- - x++", (None, None, ["y", "--post", "-", "x", "++post"])),
    # Whitespace variations
    ("  x++  +  ++y  ", (None, None, ["x", "++post", "+", "++pre", "y"])),
    ("x =  y++   +   ++z", ("x", "=", ["y", "++post", "+", "++pre", "z"])),
    (" y--   -   x++ ", (None, None, ["y", "--post", "-", "x", "++post"])),
    ("x =   y  +  ++z", ("x", "=", ["y", "+", "++pre", "z"])),
    ("x   =   y   +   x++", ("x", "=", ["y", "+", "x", "++post"])),
    # Special spacing patterns
    ("\tx\t=\ty++\t+\t++z", ("x", "=", ["y", "++post", "+", "++pre", "z"])),
    ("  x=++y  +  ++z  ", ("x", "=", ["++pre", "y", "+", "++pre", "z"])),
    ("x++\n+\n++y", (None, None, ["x", "++post", "+", "++pre", "y"])),
    ("x = y++ + \n++z", ("x", "=", ["y", "++post", "+", "++pre", "z"])),
    ("x =\n++y\n+\n++z", ("x", "=", ["++pre", "y", "+", "++pre", "z"])),
]

INVALID_EXPRESSIONS = [
    # Redundant or invalid increment/decrement operators
    ("++x++",),  # Double increment wrapping
    ("x = y++ + ++x++",),  # Chained increments
    ("x = ++y++",),  # Increment around a variable
    ("x = ++y + ++y",),  # Double prefix increment
    ("x = y+++z",),  # Postfix and infix combined
    ("x = y++++z",),  # Invalid double postfix increment
    # Invalid syntax
    ("x x",),  # Two variables without an operator
    ("x z += y",),  # Misplaced variable
    (" x = ++ y + ++ z ",),  # Whitespace-separated increments
    ("x = y \t++  + ++  z",),  # Tab-separated increments
    ("++(x + y)",),  # Increment before parenthetical expression
    # Missing operands
    ("x +",),  # Operator without a second operand
    ("+ x",),  # Operator before a variable
    ("x = ++",),  # Increment without operand
    ("x = --",),  # Decrement without operand
    # Invalid nesting or parentheses
    ("x = (y + )",),  # Unbalanced parentheses
    ("x = y + ( z",),  # Missing closing parenthesis
    ("x = y * (z + * 2)",),  # Operator after opening parenthesis
    ("x = (y++) + (z++) ++",),  # Increment operator after parenthetical expression
    # Edge cases with special operators
    ("x = y % ++z",),  # Modulus and increment
    ("x = y / --z",),  # Division and decrement
    ("x = y ** z++",),  # Exponentiation with postfix increment (if ** is not supported)
    ("x = y * * z",),  # Invalid space-separated operators
    # Duplicate or misplaced tokens
    ("x = y += += z",),  # Double assignment operator
    ("x = y ++ ++ z",),  # Misplaced increments
    ("x = y + z -- x ++",),  # Mixed postfix operators
    ("++ ++x",),  # Double prefix increment
    # Invalid characters
    ("x = y @ z",),  # Unsupported operator
    ("x = y ! z",),  # Unsupported logical negation
    ("x = y & z",),  # Unsupported bitwise operator
    # unary negation for variables is not supported
    ("x = -y",),  # unary negation for variables
    ("x = -y + 3",),  # unary negation for variables
]


@pytest.mark.parametrize("expression, expected", VALID_EXPRESSIONS)
def test_valid_expression(expression, expected):
    """Test valid expressions with correct operator sequences, including assignments."""
    # Parse the expression
    expr = Expression.from_expression(expression)

    # Unpack the expected results
    expected_variable, expected_operator, expected_tokens = expected

    # Validate the assignment components
    if expected_variable:
        assert expr.variable_name is not None
        assert expr.variable_name.value == expected_variable
        assert expr.assignment is not None
        assert expr.assignment.value == expected_operator
    else:
        assert expr.variable_name is None
        assert expr.assignment is None

    # Validate the remaining tokens
    token_values = [token.value for token in expr.tokens]
    assert token_values == expected_tokens

    # Convert to postfix to ensure the expression is valid
    postfix = expr.to_postfix()
    assert isinstance(postfix, list)
    assert len(postfix) > 0


@pytest.mark.parametrize("expression", INVALID_EXPRESSIONS)
def test_invalid_expression(expression):
    """Test invalid expressions to ensure they raise validation errors."""
    with pytest.raises(ValueError):
        Expression.from_expression(expression)  # This should raise a validation error


OPERATOR_PRECEDENCE_FIXTURES = [
    # Test cases with expected postfix results (using correct operator prefixes)
    ("x++ + y++", ["x", "++post", "y", "++post", "+"]),
    ("x + y++ + z++", ["x", "y", "++post", "+", "z", "++post", "+"]),
    ("x + y + z", ["x", "y", "+", "z", "+"]),
    ("x - y - z", ["x", "y", "-", "z", "-"]),
    ("++x + y", ["++pre", "x", "y", "+"]),
    ("++x + y++", ["++pre", "x", "y", "++post", "+"]),
    ("x++ + ++y", ["x", "++post", "++pre", "y", "+"]),
    ("x + y + ++z", ["x", "y", "+", "++pre", "z", "+"]),
    ("x++ + ++y", ["x", "++post", "++pre", "y", "+"]),
    ("x++ + ++y + z", ["x", "++post", "++pre", "y", "+", "z", "+"]),
    # Parentheses test cases
    ("(x++ + y++) * z", ["x", "++post", "y", "++post", "+", "z", "*"]),
    ("x * (y++ + z)", ["x", "y", "++post", "z", "+", "*"]),
    ("(x + y) + z++", ["x", "y", "+", "z", "++post", "+"]),
    # More complex cases with mixed operators
    ("x * y++ + z", ["x", "y", "++post", "*", "z", "+"]),
    ("x++ * y / z", ["x", "++post", "y", "*", "z", "/"]),
    ("x + y * z++", ["x", "y", "z", "++post", "*", "+"]),
    # Multiple unary operators and combinations
    ("x++ + y-- - z++", ["x", "++post", "y", "--post", "+", "z", "++post", "-"]),
    ("x++ + --y - z++", ["x", "++post", "--pre", "y", "+", "z", "++post", "-"]),
    ("x * y-- + z++ / w", ["x", "y", "--post", "*", "z", "++post", "w", "/", "+"]),
]


@pytest.mark.parametrize("expression, expected", OPERATOR_PRECEDENCE_FIXTURES)
def test_operator_precedence_and_associativity(expression, expected):
    """Test operator precedence and associativity."""
    expr = Expression.from_expression(expression)
    postfix = expr.to_postfix()
    postfix = [token.value for token in postfix]
    assert postfix == expected
