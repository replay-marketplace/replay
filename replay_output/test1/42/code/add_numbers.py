#!/usr/bin/env python3

"""
A simple program to add two numbers.

This program allows the user to input two numbers
and then displays the sum of these numbers.
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


def get_user_input():
    """
    Get two numbers from the user.
    
    Returns:
        tuple: A tuple containing the two numbers (a, b)
    """
    print("\n=== Number Addition Program ===\n")
    
    try:
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))
        return a, b
    except ValueError:
        print("\nError: Please enter valid numbers.")
        return get_user_input()


def main():
    """
    Main function that runs the program.
    """
    a, b = get_user_input()
    result = add_numbers(a, b)
    
    print(f"\nThe sum of {a} and {b} is: {result}")
    print("\nThank you for using the addition calculator!")


if __name__ == "__main__":
    main()
