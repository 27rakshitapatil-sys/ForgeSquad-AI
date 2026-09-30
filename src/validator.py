def validate_number(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid input: '{value}' is not a valid number.")

def validate_operator(operator: str) -> str:
    valid_operators = ['+', '-', '*', '/']
    if operator not in valid_operators:
        raise ValueError(f"Invalid operator: '{operator}'. Must be one of {valid_operators}")
    return operator
