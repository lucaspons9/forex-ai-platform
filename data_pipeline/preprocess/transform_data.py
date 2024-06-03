# data_pipeline/preprocess/transform_data.py
import pandas as pd


class TransformData:
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        # Perform data transformation operations, e.g., feature engineering
        data["new_feature"] = data["item"].apply(lambda x: len(x))
        return data
