#!/usr/bin/env python3

"""
Simple Addition Program

This program adds two numbers provided by the user and displays the result.
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
    Repeatedly prompt the user until they enter a valid number.
    
    Args:
        prompt (str): The message to display to the user
        
    Returns:
        float: The validated number input
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def main():
    """
    Main function to run the addition program.
    """
    print("\n===== Number Addition Program =====\n")
    
    # Get input from user
    num1 = get_valid_number("Enter the first number: ")
    num2 = get_valid_number("Enter the second number: ")
    
    # Calculate the sum
    result = add_numbers(num1, num2)
    
    # Display the result
    print(f"\nThe sum of {num1} and {num2} is: {result}")
    print("\nThank you for using the Number Addition Program!")


if __name__ == "__main__":
    main()
