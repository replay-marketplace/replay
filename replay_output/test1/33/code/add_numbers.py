#!/usr/bin/env python3

"""
A simple program to add two numbers.

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
    """
    Main function to run the program.
    """
    print("Welcome to the Number Adder Program!")
    print("-" * 40)
    
    try:
        # Get input from user
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result
        print("\nResult:")
        print(f"{num1} + {num2} = {result}")
        
    except ValueError:
        print("\nError: Please enter valid numbers.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    
    print("\nThank you for using the Number Adder Program!")


if __name__ == "__main__":
    main()
