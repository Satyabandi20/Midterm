# tests/test_command.py
import pytest
from decimal import Decimal
from calculator.command import Command
from multiprocessing import Queue

class MockCommand(Command):
    operation_name = "mock"

    def execute(self, num1: Decimal, num2: Decimal) -> Decimal:
        return num1 + num2

    def execute_multiprocessing(self, num1: Decimal, num2: Decimal, result_queue):
        result = self.execute(num1, num2)
        result_queue.put(result)

def test_command_abstract_methods():
    # Try to instantiate the abstract Command class directly, which should raise a TypeError
    with pytest.raises(TypeError):
        Command()

def test_mock_command_execute():
    # Create an instance of MockCommand
    mock_command = MockCommand()
    
    # Perform an execution and check the result
    result = mock_command.execute(Decimal(2), Decimal(3))
    assert result == Decimal(5)

def test_mock_command_execute_multiprocessing():
    # Create an instance of MockCommand
    mock_command = MockCommand()
    
    # Set up a multiprocessing queue
    result_queue = Queue()
    
    # Perform an execution using multiprocessing and check the result
    mock_command.execute_multiprocessing(Decimal(2), Decimal(3), result_queue)
    result = result_queue.get()  # Get the result from the queue
    assert result == Decimal(5)