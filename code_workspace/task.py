def generate_fibonacci(n):
    """
    Generates the first n Fibonacci numbers.

    Args:
        n (int): The number of Fibonacci numbers to generate.

    Returns:
        list: A list of Fibonacci numbers.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    fib_sequence = [0, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])

    return fib_sequence

# Generate the first 1090 Fibonacci numbers
num_fib_numbers = 1090
fib_numbers = generate_fibonacci(num_fib_numbers)

# Print the Fibonacci numbers
print(fib_numbers)

# Optional: Save the Fibonacci numbers to a text file
with open('fibonacci_numbers.txt', 'w') as file:
    for num in fib_numbers:
        file.write(str(num) + '\n')
