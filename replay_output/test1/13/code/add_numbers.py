#!/usr/bin/env python3

"""
Addition Program

This program takes two numbers as input and returns their sum.
"""

def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int or float): First number
        b (int or float): Second number
        
    Returns:
        int or float: Sum of the two numbers
    """
    return a + b


def main():
    print("Welcome to the Addition Program!")
    print("-" * 30)
    
    try:
        # Get input from user
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(a, b)
        
        # Display the result
        print(f"\nResult: {a} + {b} = {result}")
        
        # Check if result is an integer to display it nicely
        if result.is_integer():
            print(f"The sum of {int(a) if a.is_integer() else a} and {int(b) if b.is_integer() else b} is {int(result)}")
        else:
            print(f"The sum of {int(a) if a.is_integer() else a} and {int(b) if b.is_integer() else b} is {result}")
            
    except ValueError:
        print("Error: Please enter valid numbers.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    print("\nThank you for using the Addition Program!")


if __name__ == "__main__":
    main()
