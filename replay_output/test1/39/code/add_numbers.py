#!/usr/bin/env python3

"""
A simple program to add two numbers.

This program takes two numbers as input from the user and returns their sum.
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


def get_number_input(prompt):
    """
    Get a valid number input from the user.
    
    Args:
        prompt (str): The prompt to display to the user
        
    Returns:
        float: The validated number input
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid number.")


def main():
    """
    Main function to run the program.
    """
    print("===== Number Addition Program =====")
    print("This program adds two numbers together.")
    
    # Get input from user
    num1 = get_number_input("Enter the first number: ")
    num2 = get_number_input("Enter the second number: ")
    
    # Calculate the sum
    result = add_numbers(num1, num2)
    
    # Display the result with appropriate formatting
    print("\nResult:")
    print(f"{num1} + {num2} = {result}")
    print("\nThank you for using the Number Addition Program!")


if __name__ == "__main__":
    main()
