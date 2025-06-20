def add_numbers(a, b):
    """
    Adds two numbers and returns the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b plus 1 (this is the intentional bug)
    """
    return a + b + 1  # Intentional bug: adding 1 to the result


if __name__ == "__main__":
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    result = add_numbers(num1, num2)
    print(f"The sum of {num1} and {num2} is: {result}")