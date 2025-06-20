from adder import add_two_numbers

def main():
    print("Simple Number Adder Program")
    
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        result = add_two_numbers(num1, num2)
        
        print(f"The result is: {result}")
    except ValueError:
        print("Error: Please enter valid numbers.")

if __name__ == "__main__":
    main()
