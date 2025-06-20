def add_numbers(a, b):
    """
    Add two numbers together.
    
    Args:
        a (int or float): First number
        b (int or float): Second number
        
    Returns:
        int or float: The sum of a and b plus 1 (intentional bug)
    """
    # Intentional bug: adding 1 to the result
    return a + b + 1

def main():
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = add_numbers(num1, num2)
        print(f"The sum is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
