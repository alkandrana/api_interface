import sys
import argparse

def show_help():
    """Prints usage details to the console."""
    print(f"Usage: python {sys.argv[0]} [command] [arguments]")
    print("\nAvailable Commands:")
    print(
        "     greet                                   [name]      : Says hello to the provided name."
    )
    print(
        "     math    add|subtract|multiply|divide    [x] [y]     : Performs arithmetic on two numbers."
    )
    print("     help                                                : Shows this menu.")


def greet(args):
    name = args.name
    print(f"Hello, {name}!")


def add(args):
    try:
        num1 = float(args.number1)
        num2 = float(args.number2)
        print(f"Result: {num1} + {num2} = {num1 + num2}")
    except ValueError:
        print("Error: Arguments must be valid numbers.")
        sys.exit(1)


def subtract(args):
    try:
        num1 = float(args.number1)
        num2 = float(args.number2)
        print(f"Result: {num1} - {num2} = {num1 - num2}")
    except ValueError:
        print("Error: Arguments must be valid numbers.")
        sys.exit(1)


def multiply(args):
    try:
        num1 = float(args.number1)
        num2 = float(args.number2)
        print(f"Result: {num1} * {num2} = {num1 * num2}")
    except ValueError:
        print("Error: Arguments must be valid numbers.")
        sys.exit(1)


def divide(args):
    try:
        num1 = float(args.number1)
        num2 = float(args.number2)
        print(f"Result: {num1} / {num2} = {num1 / num2}")
    except ValueError:
        print("Error: Arguments must be valid numbers.")
        sys.exit(1)


def main():

    # registers the program
    parser = argparse.ArgumentParser("test",
        description="Says hello to the provided name."
    )

    # registers the commands at the current level
    subparsers = parser.add_subparsers(dest="command")

    # greet command
    greet_parser = subparsers.add_parser("greet", help="Says hello to the provided name.")
    greet_parser.add_argument("-n", "--name", help="Name to say hello to.")
    greet_parser.set_defaults(func=greet)

    # math command
    math_parser = subparsers.add_parser("math", help="Performs the indicated arithmetic operations.")
    math_subparsers = math_parser.add_subparsers(dest="subcommand")

    # math subcommands
    add_parser = math_subparsers.add_parser("add", help="Adds two numbers.")
    add_parser.add_argument("-n1", "--number1", help="First number.")
    add_parser.add_argument("-n2", "--number2", help="Second number.")
    add_parser.set_defaults(func=add)

    subtract_parser = math_subparsers.add_parser("subtract", help="Subtracts two numbers.")
    subtract_parser.add_argument("-n1", "--number1", help="First number.")
    subtract_parser.add_argument("-n2", "--number2", help="Second number.")
    subtract_parser.set_defaults(func=subtract)

    multiply_parser = math_subparsers.add_parser("multiply", help="Multiplies two numbers.")
    multiply_parser.add_argument("-n1", "--number1", help="First number.")
    multiply_parser.add_argument("-n2", "--number2", help="Second number.")
    multiply_parser.set_defaults(func=multiply)

    divide_parser = math_subparsers.add_parser("divide", help="Divides two numbers.")
    divide_parser.add_argument("-n1", "--number1", help="First number.")
    divide_parser.add_argument("-n2", "--number2", help="Second number.")
    divide_parser.set_defaults(func=divide)

    # register the properties that the command functions will need
    args = parser.parse_args()

    # automatically executes the function associated with the given command
    args.func(args)
    print(args)

if __name__ == "__main__":
    main()
