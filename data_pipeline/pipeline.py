from typing import Dict, List

from gather.gather_data import GatherData

from data_pipeline.utils.actions_on_db import DatabaseManager
from utils.configs import read_config
from utils.logger import configure_logger

# than use: LOGGER.info() or LOGGER.critical("message", e) (when doing: except Exception as e)
LOGGER = configure_logger(__file__)
LOGGER.info("first test")


class DataPipeline:
    def __init__(self):
        self.tickers_to_extract: Dict[str, List[str]] = read_config(
            file_path="config/tickers.yaml"
        )
        self.db_manager = DatabaseManager()
        self.gather_data = GatherData(self.tickers_to_extract)
        # self.transform_data = TransformData()
        # self.clean_data = CleanData()

    def run_pipeline(self):
        # wait for connection to postgres
        if self.db_manager.wait_for_postgres():
            # create tables if they don't exist
            self.db_manager.create_tables(self.tickers_to_extract)

        # gather data
        data = self.gather_data.gather_data()
        # transform data

        # upload data to db
        self.db_manager.upload_to_db(data)


if __name__ == "__main__":
    pipeline = DataPipeline()
    pipeline.run_pipeline()
