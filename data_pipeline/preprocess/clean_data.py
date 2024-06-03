# data_pipeline/preprocess/clean_data.py
import pandas as pd


class CleanData:
    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        # Perform data cleaning operations, e.g., removing null values
        data = data.dropna()
        return data
