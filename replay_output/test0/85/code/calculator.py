def add_numbers(a, b):
    # Bug: adds 1 to the result
    return a + b + 1

def main():
    print("Simple Calculator - Addition")
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = add_numbers(num1, num2)
        print(f"Result: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
