def add_numbers(a, b):
    """
    Add two numbers together and return the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b

def main():
    # Get input from user
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    
    # Calculate the sum
    result = add_numbers(num1, num2)
    
    # Display the result
    print(f"The sum of {num1} and {num2} is {result}")

if __name__ == "__main__":
    main()
