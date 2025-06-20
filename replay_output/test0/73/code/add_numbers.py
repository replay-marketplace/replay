def add_numbers(a, b):
    """
    Adds two numbers and returns the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b


def main():
    print("This program adds two numbers.")
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        result = add_numbers(a, b)
        print(f"The sum is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")


if __name__ == "__main__":
    main()
