#!/usr/bin/env python3

def add_numbers(a, b):
    """
    Adds two numbers together and returns the result.
    
    Args:
        a (int or float): The first number.
        b (int or float): The second number.
        
    Returns:
        int or float: The sum of a and b.
    """
    return a + b

def get_user_input():
    """
    Prompts the user to enter two numbers and returns them.
    
    Returns:
        tuple: A tuple containing the two numbers entered by the user.
    """
    print("\n===== Number Addition Program =====\n")
    
    try:
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))
        
        # Convert to int if the number is a whole number
        a = int(a) if a.is_integer() else a
        b = int(b) if b.is_integer() else b
        
        return a, b
    except ValueError:
        print("\nError: Please enter valid numbers.")
        return get_user_input()

def main():
    """
    Main function to run the program.
    """
    a, b = get_user_input()
    result = add_numbers(a, b)
    
    print(f"\nResult: {a} + {b} = {result}")
    print("\nThank you for using the Number Addition Program!")

if __name__ == "__main__":
    main()
