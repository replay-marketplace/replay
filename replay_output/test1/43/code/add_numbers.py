#!/usr/bin/env python3

def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int or float): First number
        b (int or float): Second number
        
    Returns:
        int or float: Sum of a and b
    """
    return a + b

def get_user_input():
    """
    Get two numbers from user input.
    
    Returns:
        tuple: Two numbers (a, b)
    """
    print("\n=== Number Addition Program ===\n")
    
    try:
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))
        
        # Convert to integers if the numbers are whole
        a = int(a) if a.is_integer() else a
        b = int(b) if b.is_integer() else b
        
        return a, b
    except ValueError:
        print("\nError: Please enter valid numbers.")
        return get_user_input()

def main():
    a, b = get_user_input()
    result = add_numbers(a, b)
    
    print("\nResult:")
    print(f"{a} + {b} = {result}")
    print("\nThank you for using the Number Addition Program!")

if __name__ == "__main__":
    main()
