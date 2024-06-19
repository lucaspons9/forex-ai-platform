from datetime import datetime
from typing import Dict, List
import pandas as pd
from dotenv import load_dotenv

from data_pipeline.gather.api_fetch import fetch_ticker_data
from data_pipeline.gather.currencies_fundamental_data import GlobalFundamental
from data_pipeline.transform.technical_operations import technical_indicators
from data_pipeline.utils.actions_on_db import DatabaseManager
from utils.configs import read_config
from utils.logger import configure_logger


LOGGER = configure_logger(__file__)


class DataPipeline:
    def __init__(self):
        load_dotenv()
        self.tickers_to_extract: Dict[str, List[str]] = read_config(
            file_path="config/tickers.yaml"
        )
        self.db_manager = DatabaseManager()
        ExtractedDataDictType = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]
        self.extracted_data_dict: ExtractedDataDictType = {
            "pairs": {"technical": {}, "fundamental": {}},
            "currencies": {"technical": {}, "fundamental": {}},
        }

    def gather_data_of_pairs(self):
        self.db_manager.postgres_running_check()
        arbitrary_latest_date = read_config(
            file_path="config/data_pipeline_configs.yaml"
        ).get("start_date")
        for ticker in self.tickers_to_extract.get("pairs"):
            latest_date = self.db_manager.get_latest_date(ticker)
            if not latest_date:
                latest_date = arbitrary_latest_date
            self.extracted_data_dict["pairs"]["technical"][ticker] = fetch_ticker_data(
                ticker, latest_date
            )

    def get_latest_date(self) -> str:
        tables_pairs_technical: List[str] = self.db_manager.get_existing_tables(
            "pairs_technical"
        )
        most_recent_date = None
        for table in tables_pairs_technical:
            latest_date_table: datetime = datetime.strptime(
                self.db_manager.get_latest_date(table), "%Y-%m-%d"
            )
            # latest_date_table: str = self.db_manager.get_latest_date(table)
            if most_recent_date is None or most_recent_date > latest_date_table:
                most_recent_date = latest_date_table

        return None if most_recent_date is None else str(most_recent_date.year)

    def gather_data_of_currencies(self):
        latest_date = self.get_latest_date()
        LOGGER.info(f"latest date is {latest_date}")
        global_fundamental = GlobalFundamental(
            tickers=self.tickers_to_extract.get("pairs")
        )
        fundamentals = global_fundamental.get_fundamentals(start_year=latest_date)
        self.extracted_data_dict["currencies"]["technical"] = fundamentals

    def gather_technical_data(self):
        # gather technical data for pairs
        self.gather_data_of_pairs()

        # gather technical data for currencies
        self.gather_data_of_currencies()

    def compute_technical_operators(self):
        for ticker in self.tickers_to_extract.get("pairs"):
            technical_data = self.extracted_data_dict["pairs"]["technical"].get(
                ticker, pd.DataFrame()
            )
            processed_data = technical_indicators(technical_data)
            self.extracted_data_dict["pairs"]["technical"][ticker] = processed_data

    def _save(self):
        # check connection with postgres
        if self.db_manager.postgres_running_check():
            # upload data to db
            self.db_manager.upload_to_db(self.extracted_data_dict)

    def run_pipeline(self, save_results: bool = False):
        if len(self.tickers_to_extract.get("pairs")) == 0:
            LOGGER.info(f"No pairs in config file. Pipeline finished.")
            return

        # gather data
        self.gather_technical_data()
        # compute technical indicators on pairs
        self.compute_technical_operators()
        LOGGER.info(f"Finished computing technical operators!!!")

        # save to db
        if save_results:
            self._save()


if __name__ == "__main__":
    ####### for local running
    # import os
    # app_dir = os.path.dirname(os.path.abspath(__file__))
    # os.chdir(os.path.dirname(app_dir))
    # print(os.getcwd())
    #######

    pipeline = DataPipeline()
    pipeline.run_pipeline(save_results=True)
