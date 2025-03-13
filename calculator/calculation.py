# calculator/calculation.py

from decimal import Decimal

class Calculation:

    def __init__(self, a: Decimal, b: Decimal, operation):
        self.a = a
        self.b = b
        self.operation = operation
        self.result = None

    def operate(self) -> Decimal:
        self.result = self.operation.execute(self.a, self.b)
        return self.result

    def __str__(self) -> str:
        return f"Calculation({self.a}, {self.b}, {self.operation.operation_name})"