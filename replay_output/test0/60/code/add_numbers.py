def add_numbers(a, b):
    """
    Function to add two numbers and return the result
    
    Args:
        a (int or float): First number
        b (int or float): Second number
    
    Returns:
        int or float: Sum of a and b
    """
    return a + b

def main():
    try:
        # Get input from user
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        
        # Calculate the sum
        result = add_numbers(a, b)
        
        # Display the result
        print(f"The sum of {a} and {b} is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
