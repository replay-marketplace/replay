def add_numbers(*args):
    """
    Add multiple numbers together.
    
    Args:
        *args: Variable length argument list of numbers to add.
        
    Returns:
        The sum of all numbers provided.
    """
    return sum(args)

def main():
    # Example usage
    print("Example 1: Adding 1, 2, 3")
    result = add_numbers(1, 2, 3)
    print(f"Result: {result}")
    
    print("\nExample 2: Adding 10, 20, 30, 40, 50")
    result = add_numbers(10, 20, 30, 40, 50)
    print(f"Result: {result}")
    
    # Get user input
    print("\nEnter your own numbers to add:")
    try:
        user_input = input("Enter numbers separated by spaces: ")
        numbers = [float(num) for num in user_input.split()]
        result = add_numbers(*numbers)
        print(f"Result: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
