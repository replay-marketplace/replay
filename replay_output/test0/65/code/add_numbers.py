def add_numbers(a, b):
    """
    Function that adds two numbers together.
    
    Args:
        a (int/float): First number
        b (int/float): Second number
        
    Returns:
        int/float: Sum of a and b
    """
    return a + b

def main():
    # Get input from user
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        # Calculate sum
        result = add_numbers(num1, num2)
        
        # Display result
        print(f"The sum of {num1} and {num2} is {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()