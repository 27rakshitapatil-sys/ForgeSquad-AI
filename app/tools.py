def calculator(expression: str) -> str:
    """Evaluate a simple math expression like '12 * (3 + 4)'."""
    allowed = set("0123456789+-*/(). ")
    if not set(expression) <= allowed:
        return "Error: only numbers and + - * / ( ) are allowed."
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


def get_time() -> str:
    """Return the current date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")