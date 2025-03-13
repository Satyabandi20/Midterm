# calculator/calculations.py
"""
A class to manage calculations using the PandasFacade for DataFrame operations.
"""

import pandas as pd
from calculator.calculation import Calculation
from calculator.pandas_facade import PandasFacade

class Calculations:
    facade = PandasFacade()

    @classmethod
    def add_calculation(cls, calculation: Calculation):
        new_record = {
            "operation": calculation.operation.operation_name,
            "num1": calculation.a,
            "num2": calculation.b,
            "result": calculation.result
        }
        cls.facade.add_record(new_record)

    @classmethod
    def clear_history(cls):
        cls.facade.clear()

    @classmethod
    def get_all_calculations(cls) -> pd.DataFrame:
        return cls.facade.dataframe

    @classmethod
    def filter_with_operation(cls, operation: str) -> pd.DataFrame:
        return cls.facade.filter_by_operation(operation)

    @classmethod
    def save_history(cls, filepath: str):
        cls.facade.save_to_file(filepath)

    @classmethod
    def load_history(cls, filepath: str):
        cls.facade.load_from_file(filepath)

    @classmethod
    def delete_history(cls, index: int):
        cls.facade.delete_record(index)