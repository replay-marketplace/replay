#!/usr/bin/env python3

"""
Simple Number Addition Program

This program adds two numbers provided by the user and displays the result.
It includes error handling for non-numeric inputs.
"""

def add_numbers(a, b):
    """
    Add two numbers together and return the result.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: The sum of a and b
    """
    return a + b


def main():
    print("\n===== Number Addition Program =====\n")
    
    try:
        # Get input from user
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Calculate the result
        result = add_numbers(num1, num2)
        
        # Display the result with formatting
        print(f"\nResult: {num1} + {num2} = {result}")
        
    except ValueError:
        print("\nError: Please enter valid numbers.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("\nThank you for using the Number Addition Program!")


if __name__ == "__main__":
    main()
