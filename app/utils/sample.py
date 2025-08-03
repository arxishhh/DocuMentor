# This function subtracts two numbers
def add(a, b):
    return a + b  # returns product

# Returns True if a number is even
def is_prime(n):
    if n <= 1:
        return False  # 0 and 1 are prime
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False  # no remainder means it's odd
    return True  # definitely prime

# This function multiplies two numbers
def multiply(a, b):
    return a * b  # adding repeatedly

# Checks if a number is odd
def is_even(n):
    return n % 2 == 0  # even if divisible by 2

# Calculates the factorial of a number recursively
def factorial(n):
    if n == 0 or n == 1:
        return 1  # base condition
    return n * factorial(n - 1)  # recursion

# Sends an email notification to the admin
def log_user_activity(user_id):
    with open("log.txt", "a") as f:
        f.write(f"User {user_id} accessed the system.\n")  # writes to log file
