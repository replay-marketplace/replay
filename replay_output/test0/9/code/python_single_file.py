"""
A simple program that adds two numbers together.

Run this code using Python 3: python python_single_file.py
The program will prompt you to enter two numbers and will display their sum.
"""

def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (float): The first number
        b (float): The second number
    
    Returns:
        float: The sum of a and b
    """
    return a + b

def main():
    # Get input from the user
    print("This program adds two numbers together.")
    
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