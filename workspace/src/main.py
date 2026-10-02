
from src.calculator import add, subtract, multiply, divide

def main():
    print("Welcome to the Calculator App")
    print("Operations: +, -, *, /")
    
    while True:
        try:
            num1 = float(input("Enter first number: "))
            op = input("Enter operation (+, -, *, /): ").strip()
            num2 = float(input("Enter second number: "))
            
            if op == '+':
                result = add(num1, num2)
            elif op == '-':
                result = subtract(num1, num2)
            elif op == '*':
                result = multiply(num1, num2)
            elif op == '/':
                result = divide(num1, num2)
            else:
                print("Invalid operation.")
                continue
                
            print(f"Result: {result}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
        cont = input("Do you want to perform another calculation? (y/n): ").lower()
        if cont != 'y':
            break

if __name__ == "__main__":
    main()
