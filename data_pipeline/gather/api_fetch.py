import pandas as pd
import yfinance as yf

from utils.logger import configure_logger

LOGGER = configure_logger(__file__)


def fetch_ticker_data(ticker: str, start_date, type: str = "pair") -> pd.DataFrame:
    LOGGER.info(f"Fetching")
    if type == "pair":
        ticker = ticker + "=X"
    data = yf.download(ticker, start=start_date, progress=False).reset_index()[
        ["Date", "Close", "High", "Low"]
    ]
    LOGGER.info(f"Obtained data shape: {data.shape}")
    return data
