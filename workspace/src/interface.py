import sys
from src.operations import add, subtract, multiply, divide

def get_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def run_calculator():
    print("Welcome to the Python Calculator!")
    
    operations = {
        '+': add,
        '-': subtract,
        '*': multiply,
        '/': divide
    }
    
    while True:
        print("\nOperations: +, -, *, /")
        op = input("Choose an operation (or 'q' to quit): ")
        
        if op == 'q':
            break
        
        if op not in operations:
            print("Invalid operation. Please try again.")
            continue
            
        a = get_number("Enter first number: ")
        b = get_number("Enter second number: ")
        
        try:
            result = operations[op](a, b)
            print(f"Result: {result}")
        except ZeroDivisionError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
