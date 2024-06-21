import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from typing import Tuple, List, Union


class DataTransformer:
    def __init__(self, window_size: int, val_size: float = 0.1, test_size: float = 0.1):
        self.window_size = window_size
        self.val_size = val_size
        self.test_size = test_size

    def add_time_periodicity(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Seconds"] = df.index.map(pd.Timestamp.timestamp)
        day = 60 * 60 * 24
        year = 365.2425 * day
        df["Year sin"] = np.sin(df["Seconds"] * (2 * np.pi / year))
        df["Year cos"] = np.cos(df["Seconds"] * (2 * np.pi / year))
        df = df.drop("Seconds", axis=1)
        return df

    def split_data(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        if len(df) == 0:
            raise Exception("Data set is empty, cannot split.")

        train_idx = round(len(df) * (1 - self.test_size - self.val_size))
        val_idx = round(len(df) * self.val_size) + train_idx

        train = df[:train_idx]
        val = df[train_idx:val_idx]
        test = df[val_idx:]

        return train, val, test

    def df_to_X_y2(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        window_size = self.window_size
        X = []
        y = []
        for i in range(len(df) - window_size):
            row = df.iloc[i : i + window_size].values
            X.append(row)
            label = df.iloc[i + window_size].values[0]
            y.append(label)
        return np.array(X), np.array(y)

    def scale(
        self, train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        scaler = MinMaxScaler(feature_range=(-1, 1))

        train_scaled = scaler.fit_transform(train)
        val_scaled = scaler.transform(val)
        test_scaled = scaler.transform(test)

        return train_scaled, val_scaled, test_scaled

    def to_supervised(
        self, df: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        df = self.add_time_periodicity(df)
        train, val, test = self.split_data(df)
        train, val, test = self.scale(train, val, test)

        train_X, train_y = self.df_to_X_y2(pd.DataFrame(train))
        val_X, val_y = self.df_to_X_y2(pd.DataFrame(val))
        test_X, test_y = self.df_to_X_y2(pd.DataFrame(test))

        return train_X, train_y, val_X, val_y, test_X, test_y


if __name__ == "__main__":
    # Create a dummy DataFrame with a datetime index and multiple features
    dates = pd.date_range(start="2022-01-01", periods=100, freq="D")
    data = np.random.randn(100, 10)  # Dummy data with 3 features
    df = pd.DataFrame(
        data, index=dates, columns=["feature" + str(i) for i in range(10)]
    )

    # Initialize the DataTransformer
    data_transformer = DataTransformer(window_size=5)

    # Transform the dummy DataFrame into supervised learning format
    train_X, train_y, val_X, val_y, test_X, test_y = data_transformer.to_supervised(df)

    # Print the shapes of the results
    print(f"Train X shape: {train_X.shape}")
    print(f"Train y shape: {train_y.shape}")
    print(f"Validation X shape: {val_X.shape}")
    print(f"Validation y shape: {val_y.shape}")
    print(f"Test X shape: {test_X.shape}")
    print(f"Test y shape: {test_y.shape}")
