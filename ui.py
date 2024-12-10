from prompt_toolkit import PromptSession, HTML, print_formatted_text
from prompt_toolkit.completion import WordCompleter

from calculator import ExecutionContext, execute_expression
from consts import GOODBYE_MESSAGE, COMMANDS


def main():
    # Initialize the calculator and session
    context = ExecutionContext({})
    session = PromptSession()

    # Define auto-completion commands
    print_formatted_text(
        HTML(
            r"""<ansiblue><pre>
   _____      _            _       _                _____ _          _ _ 
  / ____|    | |          | |     | |              / ____| |        | | |
 | |     __ _| | ___ _   _| | __ _| |_ ___  _ __  | (___ | |__   ___| | |
 | |    / _` | |/ __| | | | |/ _` | __/ _ \| '__|  \___ \| '_ \ / _ \ | |
 | |___| (_| | | (__| |_| | | (_| | || (_) | |     ____) | | | |  __/ | |
  \_____\__,_|_|\___|\__,_|_|\__,_|\__\___/|_|    |_____/|_| |_|\___|_|_|
</pre></ansiblue>""" # noqa
        )
    )
    print("Welcome to the Calculator Shell! Type 'help' for a list of commands.")

    while True:
        try:
            complete = WordCompleter(COMMANDS + list(context.variables.keys()))
            # Prompt user input with auto-completion
            line = session.prompt(HTML("<ansiblue>>> </ansiblue>"), completer=complete)
            if line.strip() == "exit":
                # Exit the shell
                print(GOODBYE_MESSAGE)
                break
            elif line.strip() == "show":
                # Show the current variables
                print(context)
            elif line.strip() == "clear":
                # Clear the current variables
                context.variables.clear()
            elif line.strip() == "" or line.strip() == "help":
                # show command list
                print("Commands: show, clear, exit, help, <expression>")
            else:
                print(execute_expression(line, context))

        except KeyboardInterrupt:
            print(GOODBYE_MESSAGE)
            break
        except EOFError:
            print(GOODBYE_MESSAGE)
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
