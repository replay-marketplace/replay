def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int or float): First number
        b (int or float): Second number
        
    Returns:
        int or float: The sum of the two numbers
    """
    return a + b

def main():
    print("Welcome to the Number Adder Program!")
    print("-" * 35)
    
    try:
        num1 = float(input("Please enter the first number: "))
        num2 = float(input("Please enter the second number: "))
        
        result = add_numbers(num1, num2)
        
        # Check if result is an integer to display it nicely
        if result.is_integer():
            result = int(result)
            
        print("\nResult: {} + {} = {}".format(num1, num2, result))
        print("\nThank you for using the Number Adder Program!")
        
    except ValueError:
        print("\nError: Please enter valid numbers.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
