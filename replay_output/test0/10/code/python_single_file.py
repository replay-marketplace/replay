"""
A program that adds two numbers together.

Run this program using Python 3:
    python python_single_file.py

The program will prompt you to enter two numbers and will display their sum.
"""

def add_numbers(num1, num2):
    """
    Add two numbers and return the result.
    
    Args:
        num1: The first number
        num2: The second number
        
    Returns:
        The sum of num1 and num2
    """
    return num1 + num2

def main():
    # Get input from the user
    print("Welcome to the addition calculator!")
    
    try:
        # Get the first number
        num1 = float(input("Enter the first number: "))
        
        # Get the second number
        num2 = float(input("Enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result
        print(f"The sum of {num1} and {num2} is {result}")
        
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()