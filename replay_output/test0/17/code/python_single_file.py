"""
Program to add two numbers.

Run this code by executing it directly with Python:
python3 python_single_file.py

You will be prompted to enter two numbers, and the program will display their sum.
"""

def add_numbers(a, b):
    """
    Function to add two numbers and return the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b

def main():
    # Get input from user
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result
        print(f"The sum of {num1} and {num2} is {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()