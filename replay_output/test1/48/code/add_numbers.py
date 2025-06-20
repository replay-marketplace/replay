def add_numbers(a, b):
    # Fixed: removed the +1 that was causing the bug
    return a + b

def main():
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    result = add_numbers(num1, num2)
    print(f"The sum is: {result}")

if __name__ == "__main__":
    main()