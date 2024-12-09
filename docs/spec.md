## Specification: Supported Operators and Syntax Rules

### Supported Operators

| **Type**                        | **Operators**                               | **Details** |
|---------------------------------|---------------------------------------------| --- |
| **Equality Operators**          | `=`, `+=`, `-=`, `*=`, `/=`, `%=`           | Assign or combine assignment with arithmetic. |
| **Arithmetic Operators**        | `+`, `-`, `*`, `/`, `%`                     | Perform standard arithmetic operations (addition, subtraction, multiplication, division, modulus). |
| **Unary Operators**             | `++`, `--`                                  | Increment or decrement variables (postfix or prefix inferred from usage). |
| **Unsupported Operators**       | `**`, `//`, `&`, `\|`, `^`, `~`, `<<`, `>>` | Bitwise and other operators are not supported. |
| **Unsupported Unary Operators** | `-`                                         | Unary minus is not supported. |

### Precedence and Associativity

| **Operator** | **Precedence** | **Associativity** | **Details** |
| --- | --- | --- | --- |
| `++` (post) | 3   | N/A | Post-increment: applies tightly to the operand. |
| `--` (post) | 3   | N/A | Post-decrement: applies tightly to the operand. |
| `++` (pre) | 3   | N/A | Pre-increment: applies tightly to the operand. |
| `--` (pre) | 3   | N/A | Pre-decrement: applies tightly to the operand. |
| `*` | 2   | Left | Multiplication. |
| `/` | 2   | Left | Division. |
| `%` | 2   | Left | Modulus. |
| `+` | 1   | Left | Addition. |
| `-` | 1   | Left | Subtraction. |

### Supported Characters in Expressions

| **Category** | **Valid Characters** | **Examples** |
| --- | --- | --- |
| **Variable Names** | Letters (`a-z`, `A-Z`), digits (`0-9`), and underscores (`_`). | `x`, `y1`, `_varName`. |
| **Operators** | As listed in the supported operators table above. | `+`, `-=`, `++`. |
| **Other Characters** | Parentheses `(` and `)`, valid expressions, and strictly placed whitespace. | `(x + 1) * y`. |

### Rules for Whitespace Handling

1.  **Strict Binding for Unary Operators**:
    
    *   Unary operators (`++`, `--`, `-`) must immediately precede or follow their operand, with no whitespace allowed.
        *   ✅ Valid: `x = -1`, `++x`, `x++`.
        *   ❌ Invalid: `x = - 1`, `+ +x`, `x + +`.
2.  **Non-ambiguous Whitespace for Binary Operators**:
    
    *   Binary operators (`+`, `-`, `*`, `/`, `%`) allow optional whitespace between operands.
        *   ✅ Valid: `x + 1`, `x+1`.
        *   ❌ Invalid: `x+++y` (ambiguous).
3.  **Ambiguity Prevention**:
    
    *   Sequences like `x+++y` must be clarified by adding explicit spaces:
        *   ✅ Valid: `x++ + y` or `x+ ++y`.

### Notes

* **Postfix vs Prefix**: The context of the `++` or `--` operator determines whether it is postfix or prefix.
* **Precedence and Associativity**: Operators follow standard mathematical precedence rules. Unary operators bind tightly to their operands, while binary operators are evaluated based on their precedence and left-associativity.
* **Unary Minus**: The unary minus operator (`-`) is not supported. Expressions like `-x` should be rewritten as `0 - x`.
* **Goodbye Message**: Typing `exit` in the CLI will terminate the session with the message: `Goodbye!`.