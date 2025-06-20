#!/usr/bin/env python3

"""
Simple Calculator Program

This program adds two numbers provided by the user and displays the result.
"""


def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (float): First number
        b (float): Second number
    
    Returns:
        float: Sum of a and b
    """
    return a + b


def main():
    """
    Main function to run the calculator program.
    Gets input from user, validates it, and displays the result.
    """
    print("\n===== Welcome to the Simple Calculator =====\n")
    
    try:
        # Get input from user
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Calculate the result
        result = add_numbers(num1, num2)
        
        # Display the result with proper formatting
        print(f"\nResult: {num1} + {num2} = {result}")
        
    except ValueError:
        print("\nError: Please enter valid numbers.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    
    print("\n===== Thank you for using Simple Calculator =====\n")


if __name__ == "__main__":
    main()