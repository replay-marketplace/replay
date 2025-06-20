"""
A simple program that adds two numbers and prints the result.

Run this program with: python3 python_single_file.py
The program will prompt you to enter two numbers and then display their sum.
"""

def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: The sum of a and b
    """
    return a + b

def main():
    # Get input from user
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