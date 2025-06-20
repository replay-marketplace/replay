#!/usr/bin/env python3

"""
A simple program to add two numbers.

This program takes two numbers as input from the user and prints their sum.
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
        prompt (str): The message to display to the user
        
    Returns:
        float: The number entered by the user
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
    print("\n===== Number Addition Program =====\n")
    
    # Get input from user
    num1 = get_number_input("Enter the first number: ")
    num2 = get_number_input("Enter the second number: ")
    
    # Calculate the sum
    result = add_numbers(num1, num2)
    
    # Display the result with formatting
    print(f"\nResult: {num1} + {num2} = {result}")
    print("\nThank you for using the Number Addition Program!")


if __name__ == "__main__":
    main()
