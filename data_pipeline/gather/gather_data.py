# data_pipeline/gather/gather_data.py
from typing import Dict, List

import pandas as pd

from data_pipeline.utils.actions_on_db import DatabaseManager
from utils.configs import read_config
from utils.logger import configure_logger

from .api_fetch import fetch_ticker_data

LOGGER = configure_logger(__file__)


class GatherData:
    def __init__(self, tickers_to_extract: Dict[str, List[str]]):
        self.db_manager = DatabaseManager()
        self.tickers_to_extract: Dict[str, List[str]] = tickers_to_extract
        # self.web_scraper = WebScraper()

        # dictionary of extracted data per ticker
        self.extracted_data_dict: Dict[str, pd.DataFrame] = {}

    def gather_data(self):
        # gather data for pairs
        self.gather_data_of_pairs()

        return self.extracted_data_dict

    def gather_data_of_pairs(self):
        for ticker in self.tickers_to_extract.get("pairs"):
            latest_date = self.db_manager.get_latest_date(ticker)
            if not latest_date:
                latest_date = read_config(
                    file_path="/app/config/data_pipeline_configs.yaml"
                ).get("start_date")
            self.extracted_data_dict[ticker] = fetch_ticker_data(ticker, latest_date)
