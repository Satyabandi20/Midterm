# calculator/calculation.py
"""
This module defines the Calculation class, which represents a mathematical calculation 
and allows for performing arithmetic operations using a specified operation.
"""

from decimal import Decimal

class Calculation:
    """
    A class representing a mathematical calculation.
    """
    def __init__(self, a: Decimal, b: Decimal, operation):
        """
        Initialize a Calculation instance.

        Args:
            a (Decimal): The first operand.
            b (Decimal): The second operand.
            operation: The operation to perform, which should implement an execute method.
        """
        self.a = a
        self.b = b
        self.operation = operation
        self.result = None

    def operate(self) -> Decimal:
        """
        Perform the arithmetic operation on the operands.

        Returns:
            Decimal: The result of the arithmetic operation.
        """
        self.result = self.operation.execute(self.a, self.b)
        return self.result

    def __str__(self) -> str:
        """
        Return a string representation of the Calculation instance.

        Returns:
            str: A string describing the calculation.
        """
        return f"Calculation({self.a}, {self.b}, {self.operation.operation_name})"