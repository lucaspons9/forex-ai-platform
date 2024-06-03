import numpy as np
import pandas as pd


def rsi(close, periods):
    """Returns RSI values"""
    close_delta = close.diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi


def add_time_periodicity(df):
    df["Seconds"] = df.index.map(pd.Timestamp.timestamp)
    day = 60 * 60 * 24
    year = 365.2425 * day
    df["Year sin"] = np.sin(df["Seconds"] * (2 * np.pi / year))
    df["Year cos"] = np.cos(df["Seconds"] * (2 * np.pi / year))
    df = df.drop("Seconds", axis=1)
    return df


def technical_indicators(data, SMA_days=50, EWMA_days=200, RSI_periods=14):
    """Function to calculate technical indicators"""
    data = data.copy()
    data["SMA"] = data["Close"].rolling(SMA_days).mean()
    data["EWMA"] = data["Close"].ewm(span=EWMA_days, min_periods=EWMA_days - 1).mean()
    SD = data.Close.rolling(window=SMA_days).std()
    data["UpperBand"] = data["SMA"] + (2 * SD)
    data["LowerBand"] = data["SMA"] - (2 * SD)
    data["RSI"] = rsi(data["Close"], periods=RSI_periods)
    data["MACD"] = (
        data["Close"].ewm(span=12, adjust=False).mean()
        - data["Close"].ewm(span=26, adjust=False).mean()
    )

    return data
