from calculator.engine import add, subtract, multiply, divide
from calculator.io_handler import get_numbers, get_operator

def main():
    print("Welcome to the Python Calculator!")
    
    while True:
        op = get_operator()
        if op == 'q':
            print("Exiting...")
            break
            
        num1, num2 = get_numbers()
        
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
            print(e)

if __name__ == "__main__":
    main()
