# calculator/pandas_facade.py

import pandas as pd

class PandasFacade:
    def __init__(self):
        self.dataframe = pd.DataFrame(columns=["operation", "num1", "num2", "result"])

    def add_record(self, record: dict):
        self.dataframe = pd.concat([self.dataframe, pd.DataFrame([record])], ignore_index=True)

    def clear(self):
        self.dataframe = pd.DataFrame(columns=self.dataframe.columns)

    def filter_by_operation(self, operation: str) -> pd.DataFrame:
        return self.dataframe[self.dataframe["operation"] == operation]

    def save_to_file(self, filepath: str):
        self.dataframe.to_csv(filepath, index=False)

    def load_from_file(self, filepath: str):
        self.dataframe = pd.read_csv(filepath)

    def delete_record(self, index: int):
        if 0 <= index < len(self.dataframe):
            self.dataframe = self.dataframe.drop(index).reset_index(drop=True)
            print(f"Deleted calculation at index {index}.")
        else:
            print(f"Index {index} is out of range. Unable to delete.")