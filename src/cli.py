from src.engine import Calculator
from src.validator import validate_number, validate_operator

def run_cli():
    calc = Calculator()
    print("Welcome to the Python Calculator!")
    
    while True:
        print("\nEnter 'exit' to quit.")
        num1_str = input("Enter first number: ")
        if num1_str.lower() == 'exit': break
        
        op = input("Enter operator (+, -, *, /): ")
        
        num2_str = input("Enter second number: ")
        
        try:
            n1 = validate_number(num1_str)
            n2 = validate_number(num2_str)
            operator = validate_operator(op)
            
            if operator == '+': result = calc.add(n1, n2)
            elif operator == '-': result = calc.subtract(n1, n2)
            elif operator == '*': result = calc.multiply(n1, n2)
            elif operator == '/': result = calc.divide(n1, n2)
            
            print(f"Result: {result}")
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
