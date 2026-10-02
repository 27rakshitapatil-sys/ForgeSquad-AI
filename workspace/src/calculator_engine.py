def calculate(a: float, b: float, op: str) -> float:
    """Performs arithmetic operations."""
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b
    else:
        raise ValueError(f"Invalid operator: {op}")
