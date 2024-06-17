import pandas as pd
import yfinance as yf

from utils.logger import configure_logger

LOGGER = configure_logger(__file__)


def fetch_ticker_data(ticker: str, start_date: str, type: str = "pair") -> pd.DataFrame:
    LOGGER.info(f"Fetching historical data on {ticker} from date: {start_date}")
    if type == "pair":
        ticker = ticker + "=X"
    data: pd.DataFrame = (
        yf.download(ticker, start=start_date, progress=False)
        .reset_index()[["Date", "Close", "High", "Low"]]
        .rename(columns={"Date": "date"})
    )
    LOGGER.info(f"Obtained data shape: {data.shape}")
    return data


# if __name__ == "__main__":
# from fredapi import Fred
# import pandas as pd
#
# fred = Fred(api_key='3a1a0a67a79106abc72a0c15e3ea0964')
# series_id = 'DEXUSEU'  # Example series ID for EUR/USD exchange rate
# data = fred.get_series(series_id)
#
# # Convert to DataFrame
# df = pd.DataFrame(data, columns=['Exchange Rate'])
# print(df.head())
