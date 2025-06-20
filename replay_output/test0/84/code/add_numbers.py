def add_numbers(a, b):
    """
    Function to add two numbers with an intentional bug.
    The function adds 1 to the correct result.
    
    Args:
        a (int/float): First number
        b (int/float): Second number
    
    Returns:
        int/float: Sum of a and b plus 1 (the bug)
    """
    return a + b + 1  # Intentional bug: adding 1 to the result

def main():
    print("Welcome to the number adder!")
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = add_numbers(num1, num2)
        print(f"The sum is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
