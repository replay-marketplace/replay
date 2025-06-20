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
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))
        result = add_numbers(a, b)
        print(f"The sum of {a} and {b} is {result}")
    except ValueError:
        print("Error: Please enter valid numbers")

if __name__ == "__main__":
    main()