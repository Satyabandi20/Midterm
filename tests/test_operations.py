# tests/test_arithmetic_operations.py
import pytest
from calculator.operations import add, subtract, multiply, divide

def test_add():
    # Test basic addition
    assert add(2, 3) == 5
    assert add(-2, 3) == 1
    assert add(0, 0) == 0

def test_subtract():
    # Test basic subtraction
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(0, 0) == 0

def test_multiply():
    # Test basic multiplication
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 3) == 0

def test_divide():
    # Test basic division
    assert divide(6, 3) == 2
    assert divide(-6, 3) == -2
    assert divide(0, 3) == 0

    # Test division by zero
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(6, 0)