def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    return a + b

def main():
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        result = add_numbers(a, b)
        print(f"The sum is: {result}")
    except ValueError:
        print("Please enter valid numbers.")

if __name__ == "__main__":
    main()