def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int or float): The first number
        b (int or float): The second number
        
    Returns:
        int or float: The sum of a and b
    """
    return a + b

def main():
    # Get input from user
    print("This program adds two numbers.")
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        # Calculate and display the result
        result = add_numbers(num1, num2)
        print(f"The sum of {num1} and {num2} is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
