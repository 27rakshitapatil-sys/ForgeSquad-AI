from calculator.engine import add, subtract, multiply, divide
from calculator.io_handler import get_number, get_operator

def main():
    print("Welcome to the Python Calculator!")
    print("Type 'exit' as an operator to quit.")

    while True:
        num1 = get_number("Enter first number: ")
        op = get_operator()
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
            
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
        
        cont = input("\nPerform another calculation? (y/n): ").lower()
        if cont != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
