def add_numbers(num1, num2):
    """
    Add two numbers together and return the result.
    
    Args:
        num1: First number to add
        num2: Second number to add
    
    Returns:
        Sum of num1 and num2
    """
    return num1 + num2

def main():
    # Get input from the user
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Call the function and display the result
        result = add_numbers(num1, num2)
        print(f"The sum of {num1} and {num2} is {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

# Execute the main function when the script is run directly
if __name__ == "__main__":
    main()
