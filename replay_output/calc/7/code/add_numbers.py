def add_numbers(*args):
    """
    Add multiple numbers together.
    
    Args:
        *args: Variable length argument list of numbers to add.
        
    Returns:
        The sum of all numbers provided.
        
    Example:
        >>> add_numbers(1, 2, 3, 4, 5)
        15
        >>> add_numbers(10, 20)
        30
    """
    return sum(args)


def main():
    # Example with hardcoded values
    result1 = add_numbers(1, 2, 3, 4, 5)
    print(f"Sum of 1, 2, 3, 4, 5 = {result1}")
    
    # Example with user input
    print("\nEnter numbers to add (space-separated):")
    try:
        user_input = input("> ")
        numbers = [float(num) for num in user_input.split()]
        result2 = add_numbers(*numbers)
        print(f"Sum of {', '.join(map(str, numbers))} = {result2}")
    except ValueError:
        print("Error: Please enter valid numbers separated by spaces.")


if __name__ == "__main__":
    main()
