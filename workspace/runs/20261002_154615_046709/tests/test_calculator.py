import pytest
from calculator.calculator_logic import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(1.5, 2.5) == 4.0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(1, 5) == -4
    assert subtract(2.5, 1.5) == 1.0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(1.5, 2) == 3.0

def test_divide():
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
