#!/usr/bin/env python3
"""
Add Two Numbers

A simple program that adds two numbers provided by the user.

Author: AI Assistant
Date: 2023
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
    """
    Main function to handle user input and display results.
    """
    print("\n===== Number Addition Program =====\n")
    
    try:
        # Get input from user
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result
        print(f"\nThe sum of {num1} and {num2} is: {result}")
        
    except ValueError:
        print("\nError: Please enter valid numbers.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    
    print("\n===== Thank you for using the program! =====\n")


if __name__ == "__main__":
    main()
