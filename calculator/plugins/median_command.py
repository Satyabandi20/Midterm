from decimal import Decimal
from calculator.command import Command

class MedianCommand(Command):
    operation_name = "median"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        return (num1 + num2)/2
    
    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        result = self.execute(num1, num2)
        result_queue.put(result)