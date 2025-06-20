"""
This program adds two numbers provided by the user.

Run this program from the command line using: python3 python_single_file.py
"""

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
    # Get input from user
    print("Welcome to the number adder program!")
    
    # Get first number from user with error handling
    while True:
        try:
            num1 = float(input("Enter the first number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Get second number from user with error handling
    while True:
        try:
            num2 = float(input("Enter the second number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # Calculate the sum
    result = add_numbers(num1, num2)
    
    # Display the result
    print(f"The sum of {num1} and {num2} is: {result}")

if __name__ == "__main__":
    main()