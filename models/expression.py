from pydantic import BaseModel, field_validator

from consts import (
    INVALID_PARENTHESIS_ERROR,
    PRECEDENCE,
    VARIABLE_VALID_CHARS,
    VALID_EQUALITY_OPERATORS,
)
from models.token import Token, TokenType
from tokenizer import tokenize


class Expression(BaseModel):
    variable_name: Token | None
    assignment: Token | None  # e.g., '=', '+='
    tokens: list[Token]

    @staticmethod
    def _handle_operator(token, stack, postfix):
        """Handles operator tokens based on precedence and associativity."""
        token_prec, _ = PRECEDENCE.get(
            token.value, (0, "left")
        )  # Get precedence for the operator

        # Special handling for pre-increment and pre-decrement operators
        if token.value in {"++pre", "--pre", "++post", "--post"}:
            postfix.append(token)
            return
        # Handle standard operators (e.g., +, -, *, /)
        while stack:
            top = stack[-1]

            # Ignore postfix operators on the stack (processed separately)
            if top.value in {"++post", "--post"}:
                break

            # Check precedence and associativity for stack's top operator
            top_prec, top_assoc = PRECEDENCE.get(
                top.value, (0, "left")
            )  # Use get() to avoid KeyError

            # Pop from the stack if:
            # - Top operator has higher precedence
            # - Top operator has equal precedence and is left-associative
            if top_prec > token_prec or (
                top_prec == token_prec and top_assoc == "left"
            ):
                postfix.append(stack.pop())
            else:
                break

        # Push the current operator onto the stack
        stack.append(token)

    @staticmethod
    def _handle_parentheses(token, stack, postfix):
        """Handle parentheses - push '(' to stack and pop until '(' for ')'."""
        if token.value == "(":
            stack.append(token)
        elif token.value == ")":
            while stack and stack[-1].value != "(":
                postfix.append(stack.pop())
            if not stack or stack[-1].value != "(":
                raise ValueError(INVALID_PARENTHESIS_ERROR)
            stack.pop()

    def to_postfix(self) -> list[Token]:
        stack = []
        postfix = []

        for token in self.tokens:
            if token.token_type in {TokenType.number, TokenType.variable}:
                # Append the variable to the postfix expression first
                postfix.append(token)
            elif token.token_type == TokenType.parentheses:
                self._handle_parentheses(token, stack, postfix)
            elif token.token_type == TokenType.operator:
                self._handle_operator(token, stack, postfix)

        # Pop any remaining operators in the stack
        while stack:
            postfix.append(stack.pop())

        return postfix

    @classmethod
    def from_expression(cls, expression: str) -> "Expression":
        tokens = tokenize(expression)
        if (
            len(tokens) >= 3
            and tokens[0].token_type == TokenType.variable
            and tokens[1].token_type == TokenType.operator
            and tokens[1].value in VALID_EQUALITY_OPERATORS
        ):
            result = cls(
                variable_name=tokens[0], assignment=tokens[1], tokens=tokens[2:]
            )
        else:
            result = cls(variable_name=None, assignment=None, tokens=tokens)
        return result

    @field_validator("variable_name")
    def validate_variable_name(cls, name: Token):
        if name is None:
            return None
        if (
            name.token_type != TokenType.variable
            or set(name.value) - VARIABLE_VALID_CHARS
        ):
            raise ValueError(f"Invalid variable name: {name}")
        return name

    @field_validator("assignment")
    def validate_operator(cls, op: Token):
        if op and op.value not in VALID_EQUALITY_OPERATORS:
            raise ValueError(f"Unsupported operator: {op}")
        return op

    @field_validator("tokens")
    def is_balanced_parentheses(cls, tokens: list[Token]):
        stack = []
        for token in tokens:
            if token.value == "(":
                stack.append(token)
            elif token.value == ")":
                if not stack:
                    raise ValueError(INVALID_PARENTHESIS_ERROR)
                stack.pop()
        if stack:
            raise ValueError(INVALID_PARENTHESIS_ERROR)
        return tokens

    @field_validator("tokens")
    def validate_consecutive_operators(cls, tokens: list[Token]):
        """Validate that there are no invalid consecutive operators."""
        prev_token = None
        cls._validate_increment_decrement_combinations(tokens)
        for i, token in enumerate(tokens):
            if token.token_type == TokenType.operator:
                if prev_token and prev_token.token_type == TokenType.operator:
                    cls._validate_same_operators(prev_token, token)
            prev_token = token
        return tokens

    @staticmethod
    def _validate_same_operators(prev_token: Token, token: Token):
        """Validate that there are no consecutive same operators like '++ ++' or '-- --'."""
        if prev_token.value == token.value:
            raise ValueError(
                f"Invalid consecutive operators: {prev_token.value} and {token.value}"
            )

    @staticmethod
    def _validate_increment_decrement_combinations(tokens: list[Token]):
        """Validate valid and invalid combinations of pre and post unary operators."""
        last_variable = None  # To track the last seen variable

        for token in tokens:
            if token.token_type == TokenType.variable:
                # If we have seen the same variable previously, it's invalid
                if last_variable == token.value:
                    raise ValueError(
                        f"Multiple unary operators applied to the same variable: {token.value}"
                    )
                last_variable = token.value  # Update the last seen variable

            elif token.token_type == TokenType.operator and token.value in {
                "++pre",
                "--pre",
                "++post",
                "--post",
            }:
                # No action needed for unary operators themselves; we just need to track variables
                continue

        # No further action needed; we just ensure that each variable is only used once in the token list
