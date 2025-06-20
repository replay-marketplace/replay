#!/usr/bin/env python3

"""
A simple program to add two numbers.

This program prompts the user to enter two numbers and displays their sum.
"""


def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b


def main():
    """
    Main function to get user input and display the result.
    """
    print("===== Number Addition Program =====")
    print("This program will add two numbers together.")
    
    try:
        # Get input from user
        num1 = float(input("\nPlease enter the first number: "))
        num2 = float(input("Please enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result
        print(f"\nResult: {num1} + {num2} = {result}")
    except ValueError:
        print("\nError: Please enter valid numbers.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    
    print("\nThank you for using the Number Addition Program!")


if __name__ == "__main__":
    main()
