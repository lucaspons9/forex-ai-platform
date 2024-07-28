from typing import List, Optional
import requests
import pandas as pd

from utils.logger import configure_logger

LOGGER = configure_logger(__file__)


class GlobalFundamental:
    def __init__(self, tickers: List[str]):
        self.currency_mapping = {
            "USD": "USA",
            "EUR": "EMU",
            "GBP": "GBR",
            "AUD": "AUS",
            "CAD": "CAN",
            "CHF": "CHE",
            "JPY": "JPN",
            "CNY": "CHN",
        }
        self.indicators = {
            "REAL_GDP": "NY.GDP.MKTP.CD",
            "UNEMPLOYMENT": "SL.UEM.TOTL.ZS",
            "INFLATION": "FP.CPI.TOTL",
            "INTEREST_RATE": "FR.INR.LEND",
            "TRADE_BALANCE": "NE.RSB.GNFS.CD",
            "POPULATION": "SP.POP.TOTL",
            "GDP_PER_CAPITA": "NY.GDP.PCAP.CD",
            "GROSS_SAVINGS": "NY.GNS.ICTR.ZS",
            "CURRENT_ACCOUNT_BALANCE": "BN.CAB.XOKA.CD",
            "EXPORTS": "NE.EXP.GNFS.CD",
            "IMPORTS": "NE.IMP.GNFS.CD",
            "GOVERNMENT_DEBT": "GC.DOD.TOTL.GD.ZS",
            "NET_FOREIGN_ASSETS": "FM.AST.NFRG.CN",
        }
        self.countries = self.get_currency_mapping_from_pairs(tickers)

    def get_currency_mapping_from_pairs(self, tickers: List[str]) -> dict[str, str]:
        unique_currencies = set()
        for pair in tickers:
            unique_currencies.add(pair[:3])
            unique_currencies.add(pair[3:])
        return {
            currency: self.currency_mapping[currency]
            for currency in unique_currencies
            if currency in self.currency_mapping
        }

    def fetch_data(
        self, country_code: str, indicator_code: str, start_date: str
    ) -> Optional[pd.DataFrame]:
        url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format=json&per_page=1000&date={start_date}:2024"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch data for {country_code} and indicator {indicator_code}"
            )
        data = response.json()[1]
        if data is None:
            return None
        df = pd.DataFrame(data)[["date", "value"]]
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by="date")
        return df

    def resample_to_daily(self, df: pd.DataFrame) -> pd.DataFrame:
        # Set 'date' as the index temporarily for resampling
        df = df.set_index("date")
        daily_df = df.resample("D").ffill()
        daily_df = daily_df.reset_index()  # Reset 'date' back to a column
        return daily_df

    def merge_dataframes(self, dataframes: list) -> pd.DataFrame:
        merged_df = dataframes[0]
        for df in dataframes[1:]:
            merged_df = pd.merge(merged_df, df, on="date", how="outer")
        date_columns = [col for col in merged_df.columns if col.startswith("date")]
        if len(date_columns) > 1:
            merged_df = merged_df.drop(columns=date_columns[1:])
        return merged_df

    def get_fundamentals(self, start_year: str = "1960") -> dict[str, pd.DataFrame]:
        result = {}
        for currency, country_code in self.countries.items():
            country_data = []
            for indicator, indicator_code in self.indicators.items():
                df = self.fetch_data(country_code, indicator_code, start_year)
                if df is None:
                    return {}
                df_daily = self.resample_to_daily(df).rename(
                    columns={"value": indicator}
                )
                country_data.append(df_daily)
            result[currency] = self.merge_dataframes(country_data)
            LOGGER.info(f"Fetched economic data for {currency}!")
        return result


if __name__ == "__main__":
    import os
    from utils.configs import read_config

    app_dir = os.path.abspath(os.path.join(__file__, "../../.."))
    os.chdir(app_dir)
    print(os.getcwd())
    tickers = read_config(file_path="config/tickers.yaml").get("pairs")
    # Example usage
    global_fundamental = GlobalFundamental(tickers=tickers)
    fundamentals = global_fundamental.get_fundamentals("2015")
    for currency, df in fundamentals.items():
        print(f"{currency} data:\n{df.head()}")
