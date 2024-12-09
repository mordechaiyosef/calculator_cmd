### Design Overview

#### 1\. **Tokenization**

*   **Input**: A raw string representing the expression (e.g., `"x = 3 + y"`).
*   **Process**:
    *   The `tokenizer` function breaks the string into a list of `Token` instances.
    *   Each `Token` represents a meaningful element, such as numbers, variables, operators, or parentheses.
    *   Basic structural checks (e.g., invalid characters or ambiguous syntax) are handled here.
*   **Output**: A list of `Token` instances.

- - -

#### 2\. **Expression Validation and Conversion**

*   **Input**: The list of `Token` instances from the tokenizer.
*   **Process**:
    *   A `pydantic` object called `Expression` is created from the tokens, validating the syntax and semantics.
    *   The `Expression` provides a `.to_postfix()` method to convert infix notation (e.g., `3 + 4`) into postfix notation (e.g., `3 4 +`), simplifying evaluation.
*   **Output**: A validated `Expression` object with a method to retrieve its postfix representation.

- - -

#### 3\. **Execution**

*   **Input**:
    *   A validated `Expression` object.
    *   An `ExecutionContext` object that stores variable states (e.g., `{x: 5, y: 10}`).
*   **Process**:
    *   The `ExpressionExecutor` class is initialized with the `ExecutionContext`.
    *   The `execute_expression` method converts the expression to postfix using `.to_postfix()` and evaluates it:
        *   Uses a stack to handle arithmetic operations.
        *   Updates or retrieves variables in the `ExecutionContext` as needed.
    *   Errors are caught and appropriately handled (e.g., undefined variables or division by zero).
*   **Output**: The evaluated result of the expression and the updated `ExecutionContext`.

- - -

#### 4\. **User Interface**

*   **Input**: User commands and expressions via a prompt-based shell.
*   **Features**:
    *   **Prompt and Styling**:
        *   A stylized interface using `prompt_toolkit`, with a dynamic auto-completer for commands and variable names.
        *   Styled UI elements (e.g., blue prompt and ASCII art header).
    *   **Commands**:
        *   `help`: Displays a list of supported commands.
        *   `show`: Lists the current variable values.
        *   `clear`: Clears all variables in the `ExecutionContext`.
        *   `exit`: Exits the calculator.
        *   `<expression>`: Evaluates a mathematical expression or assignment.
*   **Process**:
    *   Displays the ASCII art banner and a welcome message at startup.
    *   Provides dynamic auto-completion for commands and variable names.
    *   Executes user input via `execute_expression`.
    *   Handles exceptions gracefully, providing error messages for invalid inputs.
*   **Output**: Interactive shell behavior with real-time feedback on executed commands and expressions.

### Linting and Formatting

The project uses `black` for code formatting and `sonar lint` for code quality checks and static analysis.

* **Black**: Ensures consistent code formatting. To format the code, run:
    ```bash
    black .
    ```
* **Sonar Lint**: Provides static code analysis and quality checks. I run sonar lint in my IDE to ensure code quality.
  
- - -

### Summary of Components

1.  **Tokenizer**: Breaks down input into `Token` instances.
2.  **Expression (Pydantic)**: Validates tokens and prepares them for execution.
3.  **ExecutionContext**: Manages variables and their states.
4.  **ExpressionExecutor**: Evaluates the validated expressions using postfix notation.
5.  **UI Shell**: Provides an interactive interface for users with auto-completion and a styled prompt.

This modular structure ensures clear separation of concerns, making the code maintainable, testable, and user-friendly.