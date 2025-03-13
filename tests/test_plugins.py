import pytest
import multiprocessing
from decimal import Decimal, DivisionByZero
from calculator.plugins.add_command import AddCommand
from calculator.plugins.square_command import SquareCommand
from calculator.plugins.subtract_command import SubtractCommand
from calculator.plugins.multiply_command import MultiplyCommand
from calculator.plugins.divide_command import DivideCommand
from multiprocessing import Queue

def test_add_command():
    command = AddCommand()
    result = command.execute(Decimal(2), Decimal(3))
    assert result == Decimal(5)

def test_add_command_multiprocessing():
    command = AddCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(2), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(5)

def test_subtract_command():
    command = SubtractCommand()
    result = command.execute(Decimal(5), Decimal(3))
    assert result == Decimal(2)

def test_subtract_command_multiprocessing():
    command = SubtractCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(5), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

def test_multiply_command():
    command = MultiplyCommand()
    result = command.execute(Decimal(2), Decimal(3))
    assert result == Decimal(6)

def test_multiply_command_multiprocessing():
    command = MultiplyCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(2), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(6)

def test_divide_command():
    command = DivideCommand()
    result = command.execute(Decimal(6), Decimal(3))
    assert result == Decimal(2)

def test_divide_command_multiprocessing():
    command = DivideCommand()
    result_queue = Queue()
    command.execute_multiprocessing(Decimal(6), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

def test_divide_by_zero():
    command = DivideCommand()
    with pytest.raises(ZeroDivisionError):
        command.execute(Decimal(6), Decimal(0))

def test_divide_command_execute():
    divide_command = DivideCommand()

    # Test normal division
    assert divide_command.execute(Decimal(6), Decimal(3)) == Decimal(2)
    assert divide_command.execute(Decimal(-6), Decimal(3)) == Decimal(-2)
    assert divide_command.execute(Decimal(0), Decimal(3)) == Decimal(0)

    # Test division by zero
    with pytest.raises(DivisionByZero, match="Division by zero is not allowed."):
        divide_command.execute(Decimal(6), Decimal(0))

def test_divide_command_execute_multiprocessing():
    divide_command = DivideCommand()
    result_queue = Queue()

    # Test normal division using multiprocessing
    divide_command.execute_multiprocessing(Decimal(6), Decimal(3), result_queue)
    assert result_queue.get() == Decimal(2)

    # Test division by zero using multiprocessing
    divide_command.execute_multiprocessing(Decimal(6), Decimal(0), result_queue)
    result = result_queue.get()
    assert isinstance(result, DivisionByZero)
    assert str(result) == "Division by zero is not allowed."


def test_execute():
    """Test the execute method of SquareCommand."""
    command = SquareCommand()
    result = command.execute(Decimal(4), Decimal(0))  # Second parameter is ignored
    assert result == Decimal(16)

def test_execute_with_zero():
    """Test the execute method with zero."""
    command = SquareCommand()
    result = command.execute(Decimal(0), Decimal(0))
    assert result == Decimal(0)

def test_execute_multiprocessing():
    """Test the execute_multiprocessing method of SquareCommand."""
    command = SquareCommand()
    result_queue = multiprocessing.Queue()
    
    command.execute_multiprocessing(Decimal(5), Decimal(0), result_queue)
    
    # Retrieve the result from the queue
    result = result_queue.get()
    assert result == Decimal(25)

def test_execute_multiprocessing_with_zero():
    """Test the execute_multiprocessing method with zero."""
    command = SquareCommand()
    result_queue = multiprocessing.Queue()
    
    command.execute_multiprocessing(Decimal(0), Decimal(0), result_queue)
    
    # Retrieve the result from the queue
    result = result_queue.get()
    assert result == Decimal(0)