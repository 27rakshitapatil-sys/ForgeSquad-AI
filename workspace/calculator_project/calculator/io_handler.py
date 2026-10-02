def get_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_operator() -> str:
    while True:
        op = input("Enter operator (+, -, *, /): ").strip()
        if op in ('+', '-', '*', '/'):
            return op
        print("Invalid operator. Please use one of +, -, *, /.")
