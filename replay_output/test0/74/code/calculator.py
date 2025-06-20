def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int or float): First number
        b (int or float): Second number
        
    Returns:
        int or float: Sum of a and b
    """
    return a + b

def main():
    print("Simple Calculator - Addition")
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = add_numbers(num1, num2)
        print(f"The sum of {num1} and {num2} is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
