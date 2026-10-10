"""A simple command-line calculator."""


def calculate(first_number, operation, second_number):
    """Return the result of applying operation to two numbers."""
    if operation == "+":
        return first_number + second_number
    if operation == "-":
        return first_number - second_number
    if operation == "*":
        return first_number * second_number
    if operation == "/":
        if second_number == 0:
            raise ValueError("cannot divide by zero")
        return first_number / second_number
    raise ValueError("unknown operation; use +, -, *, or /")


def main():
    print("Simple Calculator")
    print("Enter q at any prompt to quit.")

    while True:
        first_value = input("First number: ").strip()
        if first_value.lower() == "q":
            break

        operation = input("Operation (+, -, *, /): ").strip()
        if operation.lower() == "q":
            break

        second_value = input("Second number: ").strip()
        if second_value.lower() == "q":
            break

        try:
            first_number = float(first_value)
            second_number = float(second_value)
            result = calculate(first_number, operation, second_number)
        except ValueError as error:
            print(f"Error: {error}")
            continue

        print(f"Result: {result:g}")


if __name__ == "__main__":
    main()