"""
A simple program that adds two numbers provided by the user.

Run this program from the command line with: python3 python_single_file.py
Follow the prompts to enter two numbers, and the program will display their sum.
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
    print("This program adds two numbers.")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Calculate the result
        result = add_numbers(num1, num2)
        
        # Display the result
        print(f"The sum of {num1} and {num2} is {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()