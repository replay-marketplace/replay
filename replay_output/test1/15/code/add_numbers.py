#!/usr/bin/env python3

def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int or float): First number to add
        b (int or float): Second number to add
        
    Returns:
        int or float: The sum of a and b
    """
    return a + b

def get_user_input():
    """
    Get two numbers from the user.
    
    Returns:
        tuple: A tuple containing the two numbers entered by the user
    """
    print("\n===== Number Addition Program =====\n")
    
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        return num1, num2
    except ValueError:
        print("\nError: Please enter valid numbers.")
        return get_user_input()

def main():
    """
    Main function to run the program.
    """
    num1, num2 = get_user_input()
    result = add_numbers(num1, num2)
    
    # Convert to int if the result is a whole number
    if result.is_integer():
        result = int(result)
    
    print(f"\nResult: {num1} + {num2} = {result}")
    print("\nThank you for using the Number Addition Program!")

if __name__ == "__main__":
    main()
