
import sys
import os

# Add src directory to path so we can import calculator
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from calculator import add, subtract, multiply, divide

def main():
    print("Simple Calculator")
    print("Available operations: +, -, *, /")
    
    try:
        num1 = float(input("Enter first number: "))
        op = input("Enter operation: ")
        num2 = float(input("Enter second number: "))
        
        if op == '+':
            print(f"Result: {add(num1, num2)}")
        elif op == '-':
            print(f"Result: {subtract(num1, num2)}")
        elif op == '*':
            print(f"Result: {multiply(num1, num2)}")
        elif op == '/':
            print(f"Result: {divide(num1, num2)}")
        else:
            print("Error: Invalid operator.")
            
    except ValueError:
        print("Error: Invalid number input.")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
