def calculate_factorial(n):
    """
    Calculate the factorial of a given number.

    Args:
    n (int): The number to calculate the factorial for.

    Returns:
    int: The factorial of the given number.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * calculate_factorial(n-1)

# Specify the number to calculate the factorial for
number = 7

try:
    result = calculate_factorial(number)
    print(f"The factorial of {number} is: {result}")
except ValueError as e:
    print(f"Error: {e}")
