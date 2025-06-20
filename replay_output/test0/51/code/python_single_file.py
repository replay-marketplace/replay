"""
This program adds two numbers provided by the user.

Run the code with 'python3 python_single_file.py' and follow the prompts to enter two numbers.
"""

def add_numbers(num1, num2):
    """
    Add two numbers and return the result.
    
    Args:
        num1: First number
        num2: Second number
        
    Returns:
        The sum of num1 and num2
    """
    return num1 + num2

def main():
    # Get input from the user
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(num1, num2)
        
        # Display the result
        print(f"The sum of {num1} and {num2} is {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()