import pytest
from decimal import Decimal
from calculator.calculation import Calculation

class MockAddCommand:
    operation_name = "add"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        return num1 + num2

class MockSubtractCommand:
    operation_name = "subtract"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        return num1 - num2

class MockMultiplyCommand:
    operation_name = "multiply"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        return num1 * num2

class MockDivideCommand:
    operation_name = "divide"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2

@pytest.fixture
def add_calculation():
    return Calculation(Decimal(2), Decimal(3), MockAddCommand())

@pytest.fixture
def subtract_calculation():
    return Calculation(Decimal(5), Decimal(3), MockSubtractCommand())

@pytest.fixture
def multiply_calculation():
    return Calculation(Decimal(2), Decimal(3), MockMultiplyCommand())

@pytest.fixture
def divide_calculation():
    return Calculation(Decimal(6), Decimal(3), MockDivideCommand())

@pytest.fixture
def divide_by_zero_calculation():
    return Calculation(Decimal(6), Decimal(0), MockDivideCommand())

def test_add_operation(add_calculation):
    result = add_calculation.operate()
    assert result == Decimal(5), f"Expected 5 but got {result}"
    assert str(add_calculation) == "Calculation(2, 3, add)"

def test_subtract_operation(subtract_calculation):
    result = subtract_calculation.operate()
    assert result == Decimal(2), f"Expected 2 but got {result}"
    assert str(subtract_calculation) == "Calculation(5, 3, subtract)"

def test_multiply_operation(multiply_calculation):
    result = multiply_calculation.operate()
    assert result == Decimal(6), f"Expected 6 but got {result}"
    assert str(multiply_calculation) == "Calculation(2, 3, multiply)"

def test_divide_operation(divide_calculation):
    result = divide_calculation.operate()
    assert result == Decimal(2), f"Expected 2 but got {result}"
    assert str(divide_calculation) == "Calculation(6, 3, divide)"

def test_divide_by_zero_operation(divide_by_zero_calculation):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide_by_zero_calculation.operate()