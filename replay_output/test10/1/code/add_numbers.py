def add_numbers(a, b):
    # Fixed: removed the bug case
    return a + b

def main():
    print("Add Two Numbers Program")
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = add_numbers(num1, num2)
        print(f"The sum of {num1} and {num2} is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
