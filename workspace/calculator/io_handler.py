from typing import Tuple, Optional

def get_numbers() -> Tuple[float, float]:
    while True:
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            return num1, num2
        except ValueError:
            print("Invalid input. Please enter numeric values.")

def get_operator() -> str:
    allowed = ['+', '-', '*', '/']
    while True:
        op = input("Enter operator (+, -, *, /) or 'q' to quit: ").strip()
        if op == 'q':
            return op
        if op in allowed:
            return op
        print(f"Invalid operator. Please choose from {allowed}")
