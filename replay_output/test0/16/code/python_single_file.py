"""
This program adds two numbers provided by the user.

Run this program from the command line with:
python3 python_single_file.py
"""

def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (float): First number
        b (float): Second number
        
    Returns:
        float: The sum of a and b
    """
    return a + b

def main():
    # Get input from the user
    print("Addition Program")
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result
        print(f"The sum of {num1} and {num2} is {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()