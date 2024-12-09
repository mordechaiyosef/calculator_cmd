from pydantic import BaseModel, model_validator
import re
from consts import (
    VALID_UNARY_OPERATORS,
    VALID_ARITHMETIC_OPERATORS,
    VALID_EQUALITY_OPERATORS,
    VARIABLE_VALID_CHARS,
    NUMBER_PATTERN,
)
import enum


class TokenType(enum.Enum):
    number = "number"
    variable = "variable"
    operator = "operator"
    parentheses = "parentheses"


class Token(BaseModel):
    value: str
    token_type: TokenType

    @model_validator(mode="after")
    def validate_values(self):
        if self.token_type == TokenType.number and not re.match(
            NUMBER_PATTERN, self.value
        ):
            raise ValueError(f"Invalid number: {self.value}")
        if (
            self.token_type == TokenType.variable
            and set(self.value) - VARIABLE_VALID_CHARS
            and self.value[0].isalpha()
        ):
            raise ValueError(f"Invalid variable name: {self.value}")
        if (
            self.token_type == TokenType.operator
            and self.value
            not in VALID_UNARY_OPERATORS
            | VALID_ARITHMETIC_OPERATORS
            | VALID_EQUALITY_OPERATORS
        ):
            raise ValueError(f"Invalid operator: {self.value}")
        return self
