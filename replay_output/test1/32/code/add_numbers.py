#!/usr/bin/env python3

"""
A simple program that adds two numbers.

This program takes two numbers as input from the user and returns their sum.
It includes input validation to ensure the user enters valid numbers.
"""


def add_numbers(a, b):
    """
    Add two numbers together and return the result.
    
    Args:
        a (float): The first number
        b (float): The second number
        
    Returns:
        float: The sum of a and b
    """
    return a + b


def get_valid_number(prompt):
    """
    Get a valid number input from the user.
    
    Args:
        prompt (str): The message to display to the user
        
    Returns:
        float: A valid number provided by the user
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def main():
    """
    Main function to run the program.
    """
    print("\n=== Number Addition Program ===")
    print("This program will add two numbers together.\n")
    
    num1 = get_valid_number("Enter the first number: ")
    num2 = get_valid_number("Enter the second number: ")
    
    result = add_numbers(num1, num2)
    
    print(f"\nThe sum of {num1} and {num2} is: {result}")
    print("\nThank you for using the Number Addition Program!")


if __name__ == "__main__":
    main()
