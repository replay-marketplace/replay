def add_numbers(a, b):
    """
    Function to add two numbers and return the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b

def main():
    try:
        # Get input from the user
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Call add_numbers function and display the result
        result = add_numbers(num1, num2)
        print(f"The sum of {num1} and {num2} is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
