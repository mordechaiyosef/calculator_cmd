# Text-Based Calculator

A simple text-based calculator application designed to evaluate assignment expressions in a subset of Java numeric expressions and operators. The app supports a variety of arithmetic and assignment operations with a modular design for extensibility and maintainability. It’s built in Python using the `prompt_toolkit` for an interactive shell interface.

## Features

*   **Support for Arithmetic Operations**: Includes addition, subtraction, multiplication, division, and modulus.
*   **Equality and Assignment Operators**: Supports `=`, `+=`, `-=`, `*=`, `/=`, and `%=` for variable assignments.
*   **Unary Operators**: Pre- and post-increment and pre- and post-decrement (`++`, `--`).
*   **Interactive Shell**: Command-line interface with auto-completion for variables and commands.
*   **Variable Storage**: Evaluates and stores variable values across expressions.

## Operators Supported

*   **Arithmetic Operators**: `+`, `-`, `*`, `/`, `%`
*   **Assignment Operators**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
*   **Unary Operators**: `++pre`, `--pre`, `++post`, `--post`

## Example

### Input

```
i = 0
j = ++i
x = i++ + 5
y = 5 + 3 * 10
i += y
```

### Output


`(i=37,j=1,x=6,y=35)`

## Design Overview

The calculator's design is structured into several components:

1.  **Tokenizer**: Takes the input expression and breaks it down into a series of tokens (e.g., operators, variables, numbers).
2.  **Expression Validation**: Ensures the syntax is valid, handles operator precedence, and applies strict rules for unary operators (no whitespace between increment/decrement and variables).
3.  **Execution Context**: Stores the variables and their values during evaluation. Supports updating and querying variable values.
4.  **Expression Executor**: Converts the expression to postfix notation and evaluates it.

## User Interface

The app provides an interactive command-line interface using `prompt_toolkit`:

*   The prompt displays `(calc) >>>` to indicate the ready state for user input.
*   Commands like `exit`, `help`, `show`, and `clear` are available with auto-completion.
*   Users can evaluate expressions and manage variables with the `show` command to display current variables and `clear` to reset them.

## Installation

You can run the calculator either directly on your local machine or inside a Docker container.

### Running the Calculator Locally

Clone the repository:

```
git clone https://github.com/mordechaiyosef/calculator_cmd.git
cd calculator
```

Install dependencies:

`pip install -r requirements.txt`

To run the calculator, execute the following:

`python ui.py`

### Running the Calculator in Docker

A `Dockerfile` is included in the repository, allowing you to build and run the app within a Docker container. 

1. **Install Docker:**

    If you don't have Docker installed, you can download it from the [official website](https://www.docker.com/products/docker-desktop).

2. **Add Docker permissions:**

    Sometimes you need to run the following command to give Docker permission to run on your machine

    `sudo chmod 777 /var/run/docker.sock`

3. **Build the Docker image:**
   
    `docker build -t calculator .`
    
    
4. **Run the Docker container:**
    
    `docker run -it --rm calculator`
    

This will start the calculator shell inside the Docker container.

## Testing

The application includes unit tests to ensure correctness. To run the tests, use:

```bash
coverage run -m pytest
coverage report
```
