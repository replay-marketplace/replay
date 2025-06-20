def add_numbers(a, b):
    """
    Add two numbers and return the result.
    
    Args:
        a (int or float): First number
        b (int or float): Second number
        
    Returns:
        int or float: Sum of the two numbers
    """
    return a + b

def main():
    print("Simple Number Addition Program")
    try:
        a = float(input("Enter first number: "))
        b = float(input("Enter second number: "))
        result = add_numbers(a, b)
        print(f"The sum of {a} and {b} is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
