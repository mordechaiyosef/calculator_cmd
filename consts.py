from string import ascii_letters, digits

INVALID_PARENTHESIS_ERROR = "Unbalanced parenthesis"
TOO_MANY_OPERATORS_ERROR = "Too many operators"
VALID_EQUALITY_OPERATORS = {"=", "+=", "-=", "*=", "/=", "%="}
VALID_ARITHMETIC_OPERATORS = {"+", "-", "*", "/", "%"}
VALID_UNARY_OPERATORS = {"++post", "--post", "++pre", "--pre"}
VALID_OPERATORS = VALID_EQUALITY_OPERATORS | VALID_ARITHMETIC_OPERATORS


VARIABLE_VALID_CHARS = set(ascii_letters + digits + "_")
SUPPORTED_CHARS = set(ascii_letters + digits + "+-*/%=() ")
GOODBYE_MESSAGE = "Goodbye!"
COMMANDS = ["exit", "show", "clear", "help"]

PRECEDENCE: dict[str, tuple[int, str]] = {
    "++post": (3, None),  # Post-increment (applies tightly to operand)
    "--post": (3, None),  # Post-decrement (applies tightly to operand)
    "++pre": (3, None),  # Pre-increment (applies tightly to operand)
    "--pre": (3, None),  # Pre-decrement (applies tightly to operand)
    "*": (2, "left"),  # Multiplication (left-associative)
    "/": (2, "left"),  # Division (left-associative)
    "%": (2, "left"),  # Modulus (left-associative)
    "+": (1, "left"),  # Addition (left-associative)
    "-": (1, "left"),  # Subtraction (left-associative)
}

NUMBER_PATTERN = r"^-?\d+(\.\d+)?$"
