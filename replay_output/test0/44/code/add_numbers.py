def add_numbers(a, b):
    """
    Adds two numbers and returns the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b

def main():
    # Get input from user
    print("This program adds two numbers.")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result
        print(f"The sum of {num1} and {num2} is {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
