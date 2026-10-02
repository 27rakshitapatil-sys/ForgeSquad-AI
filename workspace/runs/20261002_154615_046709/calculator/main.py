import sys
import os

# Add the project root to sys.path so we can import calculator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculator.calculator_logic import add, subtract, multiply, divide

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def main():
    print("--- Simple Python Calculator ---")
    
    while True:
        num1 = get_number("Enter first number: ")
        op = input("Enter operation (+, -, *, /): ").strip()
        num2 = get_number("Enter second number: ")
        
        try:
            if op == '+':
                result = add(num1, num2)
            elif op == '-':
                result = subtract(num1, num2)
            elif op == '*':
                result = multiply(num1, num2)
            elif op == '/':
                result = divide(num1, num2)
            else:
                print("Invalid operator.")
                continue
            
            print(f"Result: {result}")
        except ZeroDivisionError as e:
            print(f"Error: {e}")
        
        again = input("Perform another calculation? (y/n): ").lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()
