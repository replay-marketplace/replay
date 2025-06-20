def add_numbers(a, b):
    """
    Function to add two numbers
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b

def main():
    try:
        # Get input from the user
        a = float(input("Enter the first number: "))
        b = float(input("Enter the second number: "))
        
        # Calculate the sum
        result = add_numbers(a, b)
        
        # Display the result
        print(f"The sum of {a} and {b} is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()