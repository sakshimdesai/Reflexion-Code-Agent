def calculate_factorial(n):
    """
    Calculate the factorial of a given number.

    Args:
        n (int): The number to calculate the factorial of.

    Returns:
        int: The factorial of the given number.
    """
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n-1)


def main():
    number = 9
    factorial = calculate_factorial(number)
    print(f"The factorial of {number} is: {factorial}")


if __name__ == "__main__":
    main()
