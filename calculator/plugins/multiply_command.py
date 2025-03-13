# calculator/plugins/multiply_command.py

from decimal import Decimal
from calculator.command import Command

class MultiplyCommand(Command):

    operation_name = "multiply"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        return num1 * num2

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        result = self.execute(num1, num2)
        result_queue.put(result)