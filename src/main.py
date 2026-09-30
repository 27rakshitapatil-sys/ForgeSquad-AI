from src.calculator import add, subtract, multiply, divide

def main():
    print("Simple Calculator")
    print("Available operations: +, -, *, /")
    
    try:
        num1 = float(input("Enter first number: "))
        operator = input("Enter operator: ")
        num2 = float(input("Enter second number: "))
        
        if operator == '+':
            print(f"Result: {add(num1, num2)}")
        elif operator == '-':
            print(f"Result: {subtract(num1, num2)}")
        elif operator == '*':
            print(f"Result: {multiply(num1, num2)}")
        elif operator == '/':
            print(f"Result: {divide(num1, num2)}")
        else:
            print("Invalid operator.")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
