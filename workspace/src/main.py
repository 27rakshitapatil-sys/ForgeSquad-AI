import argparse
import sys
from src.calculator import Calculator

def main():
    parser = argparse.ArgumentParser(description="Simple CLI Calculator")
    parser.add_argument("x", type=float, help="First number")
    parser.add_argument("operator", choices=['+', '-', '*', '/'], help="Arithmetic operator")
    parser.add_argument("y", type=float, help="Second number")

    args = parser.parse_args()
    calc = Calculator()

    try:
        if args.operator == '+':
            result = calc.add(args.x, args.y)
        elif args.operator == '-':
            result = calc.subtract(args.x, args.y)
        elif args.operator == '*':
            result = calc.multiply(args.x, args.y)
        elif args.operator == '/':
            result = calc.divide(args.x, args.y)
        
        print(f"Result: {result}")
    except ZeroDivisionError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
