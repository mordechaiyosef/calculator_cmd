import pytest
from decimal import Decimal
from calculator import ExpressionExecutor, ExecutionContext
from models.expression import Expression


@pytest.fixture
def initial_context():
    """Fixture to provide a fresh execution context."""
    variables = {"x": Decimal(1), "y": Decimal(2), "z": Decimal(3)}
    return ExecutionContext(variables)


@pytest.fixture
def executor(initial_context):
    """Fixture to provide an expression executor."""
    return ExpressionExecutor(initial_context)


def test_get_variable(initial_context):
    assert initial_context.get_variable("x") == 1
    assert initial_context.get_variable("y") == 2


def test_set_variable(initial_context):
    initial_context.set_variable("x", Decimal(10))
    assert initial_context.get_variable("x") == 10


def test_rollback(initial_context):
    initial_context.set_variable("x", Decimal(10))
    initial_context.rollback()
    assert initial_context.get_variable("x") == Decimal(1)


def test_commit(initial_context):
    initial_context.set_variable("x", 10)

    initial_context.commit()
    assert initial_context.variables["x"] == 10


def test_undefined_variable_access(initial_context):
    with pytest.raises(ValueError, match="Undefined variable: a"):
        initial_context.get_variable("a")


def test_undefined_variable_set(initial_context):
    with pytest.raises(ValueError, match="Undefined variable: a"):
        initial_context.set_variable("a", Decimal(10))


@pytest.mark.parametrize(
    "raw_expression, expected_variables",
    [
        # Simple operations
        ("x = 5 + 4", {"x": Decimal("9"), "y": Decimal("2"), "z": Decimal("3")}),
        ("y = 5 * 4", {"x": Decimal("1"), "y": Decimal("20"), "z": Decimal("3")}),
        ("z = 5 / 2", {"x": Decimal("1"), "y": Decimal("2"), "z": Decimal("2.5")}),
        ("z = 5 % 2", {"x": Decimal("1"), "y": Decimal("2"), "z": Decimal("1")}),
        # Operations with parentheses
        (
            "x = 4 + (5 / 2)",
            {"x": Decimal("6.5"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        (
            "x = 5 * 4 + (5 / 2)",
            {"x": Decimal("22.5"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        ("x = (5 + 4) * 2", {"x": Decimal("18"), "y": Decimal("2"), "z": Decimal("3")}),
        (
            "x = (5 + 4) * (2 + 3)",
            {"x": Decimal("45"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        # Operations with mixed types
        ("x = 5 + 4.5", {"x": Decimal("9.5"), "y": Decimal("2"), "z": Decimal("3")}),
        (
            "x = 5 + 4 + 1.5",
            {"x": Decimal("10.5"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        # Operations with variables
        ("x = y + 5", {"x": Decimal("7"), "y": Decimal("2"), "z": Decimal("3")}),
        (
            "x = y + 5 * 4 + (5 / 2)",
            {"x": Decimal("24.5"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        # Complex multi-operator operations
        ("x = 5 + 4 * 2", {"x": Decimal("13"), "y": Decimal("2"), "z": Decimal("3")}),
        (
            "x = 5 + 4 * 2 - 3",
            {"x": Decimal("10"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        (
            "x = 5 + 4 * (2 - 3)",
            {"x": Decimal("1"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        # Mixed addition, subtraction, multiplication, and division
        (
            "x = y + 5 - 4 * 2 / 2",
            {"x": Decimal("3"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        # Check behavior of division
        ("x = 10 / 2", {"x": Decimal("5"), "y": Decimal("2"), "z": Decimal("3")}),
        ("x = 5 / 2", {"x": Decimal("2.5"), "y": Decimal("2"), "z": Decimal("3")}),
        # Test result as a float with decimal
        (
            "x = 7 / 3",
            {"x": Decimal("7") / Decimal("3"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        # Complex expressions with both operators and variables
        (
            "x = (y + 2) * 5 - 2",
            {"x": Decimal("18"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        (
            "x = y + 5 * 4 + (5 / 2) + z",
            {"x": Decimal("27.5"), "y": Decimal("2"), "z": Decimal("3")},
        ),
        # Edge cases
        ("x = 0", {"x": Decimal("0"), "y": Decimal("2"), "z": Decimal("3")}),
        ("x = -5 + 4", {"x": Decimal("-1"), "y": Decimal("2"), "z": Decimal("3")}),
        ("x = 5 + -4", {"x": Decimal("1"), "y": Decimal("2"), "z": Decimal("3")}),
        ("x = -5 * 4", {"x": Decimal("-20"), "y": Decimal("2"), "z": Decimal("3")}),
        # Testing with only variables
        ("x = y + z", {"x": Decimal("5"), "y": Decimal("2"), "z": Decimal("3")}),
        ("y = x + z", {"x": Decimal("1"), "y": Decimal("4"), "z": Decimal("3")}),
        # Repeated expressions to test multiple runs
        ("x = 5 + 4", {"x": Decimal("9"), "y": Decimal("2"), "z": Decimal("3")}),
        ("x = 10 + 5", {"x": Decimal("15"), "y": Decimal("2"), "z": Decimal("3")}),
        # Increment/Decrement operators
        ("x++", {"x": Decimal("2"), "y": Decimal("2"), "z": Decimal("3")}),
        ("x--", {"x": Decimal("0"), "y": Decimal("2"), "z": Decimal("3")}),
        ("++x", {"x": Decimal("2"), "y": Decimal("2"), "z": Decimal("3")}),
        ("--x", {"x": Decimal("0"), "y": Decimal("2"), "z": Decimal("3")}),
        # Increment/Decrement operators with assignment
        ("x = y++", {"x": Decimal("2"), "y": Decimal("3"), "z": Decimal("3")}),
        ("x = ++y", {"x": Decimal("3"), "y": Decimal("3"), "z": Decimal("3")}),
        ("x = y--", {"x": Decimal("2"), "y": Decimal("1"), "z": Decimal("3")}),
        ("x = --y", {"x": Decimal("1"), "y": Decimal("1"), "z": Decimal("3")}),
        ("x += y++", {"x": Decimal("3"), "y": Decimal("3"), "z": Decimal("3")}),
        ("x += ++y", {"x": Decimal("4"), "y": Decimal("3"), "z": Decimal("3")}),
        ("x -= y--", {"x": Decimal("-1"), "y": Decimal("1"), "z": Decimal("3")}),
        ("x -= --y", {"x": Decimal("0"), "y": Decimal("1"), "z": Decimal("3")}),
        ("x *= y++", {"x": Decimal("2"), "y": Decimal("3"), "z": Decimal("3")}),
        ("x *= ++y", {"x": Decimal("3"), "y": Decimal("3"), "z": Decimal("3")}),
        ("x /= y--", {"x": Decimal("0.5"), "y": Decimal("1"), "z": Decimal("3")}),
        ("x /= --y", {"x": Decimal("1"), "y": Decimal("1"), "z": Decimal("3")}),
        ("x /= --y", {"x": Decimal("1"), "y": Decimal("1"), "z": Decimal("3")}),
        ("x %= 1", {"x": Decimal("0"), "y": Decimal("2"), "z": Decimal("3")}),
    ],
)
def test_execute_expression_valid(executor, raw_expression, expected_variables):
    expression = Expression.from_expression(raw_expression)
    executor.execute_expression(expression)

    assert executor.context.variables == expected_variables


@pytest.mark.parametrize(
    "expression",
    [
        # Invalid number of operands for the operator
        ("x /"),  # Operator without enough operands
        ("x +"),  # Operator without enough operands
        # Invalid postfix expression (too many operators, wrong order of operands)
        ("x y z +"),  # Operand order error (extra operands)
        # Division by zero
        ("x / 0"),  # Division by zero
        # Undefined variable
        ("a"),  # Referencing an undefined variable
        # Invalid use of unary operator (e.g., consecutive increments or invalid positioning)
        ("x ++ ++"),  # Consecutive increment operators
        # Invalid operator usage
        ("x + +"),  # Extra '+' operator without a valid operand
        # Invalid variable or unsupported syntax
        ("x & y"),  # Unsupported operator (&)
        # Syntax errors
        ("5 + (4 *"),  # Mismatched parentheses
        # Invalid character or unsupported operator
        ("x $ y"),  # Unsupported operator '$'
        # Nested parentheses without closing
        ("(x + y"),  # Missing closing parenthesis
        # Unsupported use of operators
        ("5 * 4 ^ 2"),  # Unsupported operator '^'
        # Redundant parentheses
        ("(x + y) +"),  # Closing parentheses with no operand after
        # Missing operand after operator
        ("x + + y"),  # Invalid use of '++' after a binary operator
        # Invalid use of increment operator
        ("x+ a++"),  # Invalid use of '++' after a variable
    ],
)
def test_execute_postfix_errors(executor, expression):
    with pytest.raises(ValueError):
        expression = Expression.from_expression(expression)
        executor.execute_expression(expression)

    # Ensure the context is rolled back correctly after an error
    assert executor.context.variables == {"x": 1, "y": 2, "z": 3}
