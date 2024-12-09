from models.expression import Expression
from decimal import Decimal

from models.token import Token, TokenType
from settings import logger


class ExecutionContext:
    def __init__(self, variables: dict[str, Decimal]):
        self.variables = variables.copy()
        self._rollback_stack = []

    def get_variable(self, name: str) -> Decimal:
        if name not in self.variables:
            raise ValueError(f"Undefined variable: {name}")
        return self.variables[name]

    def get_or_create_variable(self, name: str) -> Decimal:
        if name not in self.variables:
            self.variables[name] = Decimal("nan")
        return self.variables[name]

    def set_variable(self, name: str, value: Decimal):
        if name not in self.variables:
            raise ValueError(f"Undefined variable: {name}")
        # Save the current state for rollback
        self._rollback_stack.append(self.variables.copy())
        self.variables[name] = value

    def rollback(self):
        if self._rollback_stack:
            self.variables = self._rollback_stack.pop()

    def commit(self):
        self._rollback_stack.clear()

    def __repr__(self):
        return (
            "("
            + ", ".join(f"{var}={value}" for var, value in self.variables.items())
            + ")"
        )


class ExpressionExecutor:
    def __init__(self, context: ExecutionContext):
        self.context = context

    def apply_assignment(self, variable_name: str, value: Decimal, operator: str):
        current_value = self.context.get_or_create_variable(variable_name)
        if operator == "=":
            return value
        elif current_value.is_nan():
            raise ValueError(
                f"Undefined variable: {variable_name} cannot be assigned with {operator}"
            )
        elif operator == "+=":
            return current_value + value
        elif operator == "-=":
            return current_value - value
        elif operator == "*=":
            return current_value * value
        elif operator == "%=":
            return current_value % value
        elif operator == "/=":
            if value == 0:
                raise ValueError("Division by zero")
            return current_value / value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def execute_expression(self, expression: Expression) -> str:
        expression_postfix = expression.to_postfix()
        value = self.execute_postfix(expression_postfix)
        if expression.variable_name is not None:
            logger.debug(
                f"Variable assignment: {expression.variable_name.value} = {value}"
            )
            new_assigned = self.apply_assignment(
                expression.variable_name.value, value, expression.assignment.value
            )
            self.context.set_variable(expression.variable_name.value, new_assigned)
            logger.debug(
                f"Variable {expression.variable_name} assigned to {new_assigned}"
            )

            value = "{:f}".format(new_assigned)
        else:
            value = "{:f}".format(value)
        self.context.commit()
        return value

    def execute_postfix(self, postfix: list[Token]) -> Decimal:
        logger.debug("Postfix: " + " ".join(str(token.value) for token in postfix))
        stack = []

        try:
            i = 0
            while i < len(postfix):
                token = postfix[i]

                if token.token_type == TokenType.number:
                    stack.append(Decimal(token.value))
                elif token.token_type == TokenType.variable:
                    stack.append(self.context.get_variable(token.value))
                elif token.value in {"++post", "--post"}:
                    self._apply_post_operator(token, stack)
                elif token.value in {"++pre", "--pre"}:
                    self._apply_pre_operator(token, postfix, i, stack)
                    i += 1  # Skip the next variable
                elif token.value in {"+", "-", "*", "/", "%"}:
                    self._apply_operator(token, stack)
                else:
                    raise ValueError(f"Unknown token: {token}")

                i += 1

            if len(stack) != 1:
                raise ValueError("Invalid expression")
            logger.debug(f"Result: {stack[0]}")
            return stack[0]

        except Exception as e:
            # Rollback state in case of error
            self.context.rollback()
            raise e

    def _apply_post_operator(self, token: str, stack: list[Decimal]):
        """Apply post-increment or post-decrement operators."""
        if not stack:
            raise ValueError(f"Invalid use of '{token}'")

        value = stack.pop()
        stack.append(value)  # Push the value as-is

        # Update the corresponding variable in context
        self._update_variable(token, value)

    def _apply_pre_operator(
        self, token: Token, postfix: list[Token], i: int, stack: list[Decimal]
    ):
        """Apply pre-increment or pre-decrement operators."""
        var = postfix[i + 1]
        if var.token_type != TokenType.variable:
            raise ValueError(f"Invalid use of '{postfix[i+1]}' after '{token}'")
        if i + 1 >= len(postfix) or var.token_type != TokenType.variable:
            raise ValueError(f"{token} operator must be followed by a variable")

        value = self.context.get_variable(var.value)
        new_value = value + 1 if token.value == "++pre" else value - 1
        self.context.set_variable(var.value, new_value)
        stack.append(new_value)

    def _apply_operator(self, token: Token, stack: list[Decimal]):
        """Apply arithmetic operators."""
        if len(stack) < 2:
            raise ValueError(f"Insufficient operands for '{token}'")

        b = stack.pop()
        a = stack.pop()
        result = self._apply_operator_logic(a, b, token)
        stack.append(result)

    @staticmethod
    def _apply_operator_logic(a: Decimal, b: Decimal, operator: Token) -> Decimal:
        """Perform the actual arithmetic operation."""
        operator = operator.value
        if operator == "+":
            return a + b
        elif operator == "-":
            return a - b
        elif operator == "*":
            return a * b
        elif operator == "/":
            if b == 0:
                raise ValueError("Division by zero")
            return a / b
        elif operator == "%":
            return a % b
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def _update_variable(self, token: Token, value: Decimal):
        """Find the variable corresponding to the value and update it."""
        for var, var_value in self.context.variables.items():
            if var_value == value:
                self.context.set_variable(
                    var, var_value + (1 if token.value == "++post" else -1)
                )
                break
        else:
            raise ValueError(f"Undefined variable for value: {value}")


def execute_expression(expression: str, context: ExecutionContext) -> str:
    """Execute the expression and return the result."""
    # Initialize the calculator and execute the expression
    calc = ExpressionExecutor(context)
    expression = Expression.from_expression(expression)
    return calc.execute_expression(expression)
