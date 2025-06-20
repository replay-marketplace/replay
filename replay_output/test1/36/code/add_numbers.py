#!/usr/bin/env python3

"""
Simple program to add two numbers.

This program prompts the user for two numbers and displays their sum.
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
    print("=== Number Addition Program ===")
    print("Welcome! This program will add two numbers for you.")
    
    try:
        # Get input from the user
        num1 = float(input("\nPlease enter the first number: "))
        num2 = float(input("Please enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result with formatting
        print(f"\nThe sum of {num1} and {num2} is: {result}")
        print("\nThank you for using the Number Addition Program!")
        
    except ValueError:
        print("\nError: Please enter valid numbers.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
