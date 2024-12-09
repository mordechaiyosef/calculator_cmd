from typing import Literal

from consts import TOO_MANY_OPERATORS_ERROR, VARIABLE_VALID_CHARS
from models.token import Token, TokenType


def is_number(expression: str, i: int, char: str) -> bool:
    """Check if the character is a number."""
    n = len(expression)
    return char.isdigit() or (
        i + 1 < n
        and (char == "-" and expression[i + 1] in ".0123456789")
        or (char == "." and i > 0 and expression[i - 1].isdigit())
    )


def tokenize(expression: str) -> list[Token]:
    """Tokenize the expression into numbers, variables, operators, and parentheses."""
    tokens: list[Token] = []
    i: int = 0
    n: int = len(expression)

    if _check_too_many_operators(expression):
        raise ValueError(TOO_MANY_OPERATORS_ERROR)

    while i < n:
        char = expression[i]

        if char.isspace():
            i += 1
        elif is_number(expression, i, char):
            i, new_tokens = _tokenize_number(expression, i)
            tokens.extend(new_tokens)
        elif char.isalpha() or char == "_":
            i, new_tokens = _tokenize_variable(expression, i)
            tokens.extend(new_tokens)
        elif char in "()":
            tokens.append(Token(value=char, token_type=TokenType.parentheses))
            i += 1
        elif char in "*/%=+-":
            i, new_tokens = _tokenize_operator(
                expression, i, previous_token=tokens[-1] if tokens else None
            )
            tokens.extend(new_tokens)
        else:
            raise ValueError(f"Unexpected character: {char}")

    return tokens


def _check_too_many_operators(expression: str) -> bool:
    count = 0
    for char in expression:
        if char == "=":
            count += 1
        if count == 2:
            return True
    return False


def _tokenize_number(expression: str, i: int) -> tuple[int, list[Token]]:
    start: int = i
    n: int = len(expression)

    # Handle the optional negative sign at the beginning
    if i < n and expression[i] == "-":
        i += 1

    # Now, let's allow digits and at most one decimal point
    has_dot = False
    while i < n and (expression[i].isdigit() or (expression[i] == "." and not has_dot)):
        if expression[i] == ".":
            has_dot = True
        i += 1

    # Return the number token
    return i, [Token(value=expression[start:i], token_type=TokenType.number)]


def _tokenize_variable(expression: str, i: int) -> tuple[int, list[Token]]:
    start: int = i
    while i < len(expression) and (expression[i].isalnum() or expression[i] == "_"):
        i += 1
    return i, [Token(value=expression[start:i], token_type=TokenType.variable)]


def _tokenize_operator(
    expression: str, i: int, previous_token: Token = None
) -> tuple[int, list[Token]]:
    tokens = []
    n = len(expression)

    # Handle operators followed by '=' (e.g., +=, -=, *=, /=)
    if i + 1 < n and expression[i] in "+-*/%" and expression[i + 1] == "=":
        tokens.append(Token(value=expression[i : i + 2], token_type=TokenType.operator))
        i += 2  # Skip the operator and '='
    # Handle single "=" operator
    elif expression[i] == "=":
        tokens.append(Token(value=expression[i : i + 1], token_type=TokenType.operator))
        i += 1  # Skip the '='
    elif expression[i] in "+-":
        # Handle consecutive '+' and '-' operators and other single operators
        i, new_token = _handle_consecutive_plus_minus(
            expression, i, previous_token=previous_token
        )
        tokens.append(new_token)
    else:
        tokens.append(Token(value=expression[i], token_type=TokenType.operator))
        i += 1

    return i, tokens


def check_if_unary_is_pre(
    expression: str, start: int, end: int, previous_token: Token
) -> Literal["pre", "post"]:
    """Check if the unary operator is pre-increment/decrement or post-increment/decrement."""
    n = len(expression)

    # Pre-increment or decrement if it's at the start, or followed by an operand
    if (
        previous_token
        and previous_token.token_type == TokenType.variable
        and expression[start - 1] in VARIABLE_VALID_CHARS
    ):  # ie x++ or x-- without whitespace
        return "post"
    elif (
        end < n and expression[end] in VARIABLE_VALID_CHARS
    ):  # ie ++x or --x without whitespace
        return "pre"
    else:
        raise ValueError(f"Invalid unary operator: {expression[start:end]}")


def _handle_consecutive_plus_minus(
    expression: str, i: int, previous_token: Token = None
) -> tuple[int, Token]:
    token = None
    n = len(expression)
    count = 1

    # Count consecutive '+' or '-' operators
    while (
        i + count < n
        and expression[i + count] == expression[i]
        and expression[i] in "+-"
    ):
        count += 1

    # If too many consecutive operators, raise an error
    if count >= 3:  # Limit consecutive operators to 3 (adjustable)
        raise ValueError(TOO_MANY_OPERATORS_ERROR)
    if count == 2:
        # Determine if it's pre or post increment/decrement
        is_pre = check_if_unary_is_pre(expression, i, i + 2, previous_token)
        value = expression[i : i + 2] + is_pre
        token = Token(value=value, token_type=TokenType.operator)
        i += count  # Skip the consecutive operators
    elif count == 1:
        token = Token(value=expression[i], token_type=TokenType.operator)
        i += 1
    return i, token
