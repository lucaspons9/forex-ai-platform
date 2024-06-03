from typing import Dict, List
import pandas as pd

from data_pipeline.gather.api_fetch import fetch_ticker_data
from data_pipeline.transform.technical_operations import technical_indicators
from data_pipeline.utils.actions_on_db import DatabaseManager
from utils.configs import read_config
from utils.logger import configure_logger


LOGGER = configure_logger(__file__)


class DataPipeline:
    def __init__(self):
        self.tickers_to_extract: Dict[str, List[str]] = read_config(
            file_path="config/tickers.yaml"
        )
        self.db_manager = DatabaseManager()
        ExtractedDataDictType = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]
        extracted_data: ExtractedDataDictType = {
            "pairs": {"technical": {}, "fundamental": {}},
            "currencies": {"technical": {}, "fundamental": {}},
        }
        self.extracted_data_dict: ExtractedDataDictType = extracted_data

    def gather_technical_data(self):
        # gather technical data for pairs
        self.gather_data_of_pairs()

        # gather technical data for currencies

    def gather_data_of_pairs(self):
        for ticker in self.tickers_to_extract.get("pairs"):
            self.db_manager.wait_for_postgres()  # todo: remove this
            latest_date = self.db_manager.get_latest_date(ticker)
            if not latest_date:
                latest_date = read_config(
                    file_path="/app/config/data_pipeline_configs.yaml"
                ).get("start_date")
            self.extracted_data_dict["pairs"]["technical"][ticker] = fetch_ticker_data(
                ticker, latest_date
            )

    def compute_technical_operators(self):
        for ticker in self.tickers_to_extract.get("pairs"):
            technical_data = self.extracted_data_dict["pairs"]["technical"].get(
                ticker, pd.DataFrame()
            )
            processed_data = technical_indicators(technical_data)
            self.extracted_data_dict["pairs"]["technical"][ticker] = processed_data

    def run_pipeline(self):
        # gather data
        self.gather_technical_data()
        # compute technical indicators on pairs
        self.compute_technical_operators()
        LOGGER.info(f"Finished computing technical operators!!!")
        LOGGER.info(self.extracted_data_dict["pairs"]["technical"]["EURUSD"])

        # # wait for connection to postgres
        # if self.db_manager.wait_for_postgres():
        #     # create tables if they don't exist
        #     self.db_manager.create_tables(self.tickers_to_extract)
        # # upload data to db
        # self.db_manager.upload_to_db(data)


if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()
