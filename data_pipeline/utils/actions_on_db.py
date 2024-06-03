import os
import time
from typing import Dict, List, Optional

import pandas as pd
import psycopg2
from psycopg2 import OperationalError

from utils.logger import configure_logger

LOGGER = configure_logger(__file__)


class DatabaseManager:
    def __init__(self):
        self.db_host: str = os.getenv("DB_HOST")
        self.db_user: str = os.getenv("DB_USER")
        self.db_password: str = os.getenv("DB_PASSWORD")
        LOGGER.info(f"password {self.db_password}")
        self.db_name: str = os.getenv("DB_NAME")

    def wait_for_postgres(self, timeout: int = 60) -> bool:
        """Wait for PostgreSQL to be ready before proceeding."""
        start_time = time.time()
        while True:
            try:
                conn = psycopg2.connect(
                    host=self.db_host,
                    user=self.db_user,
                    password=self.db_password,
                    dbname=self.db_name,
                )
                conn.close()
                LOGGER.info("PostgreSQL is ready!")
                return True
            except OperationalError:
                if time.time() - start_time > timeout:
                    raise Exception("Timed out waiting for PostgreSQL to be ready")
                LOGGER.info("Waiting for PostgreSQL...")
                time.sleep(1)

    def get_existing_tables(self) -> List[str]:
        """Get the list of existing tables in the PostgreSQL database.

        Returns:
        List[str]: List of existing table names.
        """
        conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            dbname=self.db_name,
        )
        cur = conn.cursor()

        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
        """
        )
        existing_tables = [row[0] for row in cur.fetchall()]

        cur.close()
        conn.close()

        return existing_tables

    def create_tables(self, tickers: Dict[str, List[str]]) -> None:
        """Create tables in the PostgreSQL database as specified in the config file.

        Parameters:
        config_path (str): The path to the YAML configuration file containing table names.
        """
        tables: List[str] = [
            table for tables_list in tickers.values() for table in tables_list
        ]
        existing_tables = self.get_existing_tables()

        conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            dbname=self.db_name,
        )
        cur = conn.cursor()

        for table in tables:
            if table not in existing_tables:
                cur.execute(
                    f"""
                    CREATE TABLE "{table}" (
                        id SERIAL PRIMARY KEY,
                        date DATE,
                        close FLOAT,
                        high FLOAT,
                        low FLOAT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """
                )

        conn.commit()
        cur.close()
        conn.close()

    def add_column(self, table_name: str, column_name: str, data_type: str) -> None:
        """Add a new column to an existing table.

        Parameters:
        table_name (str): The name of the table to modify.
        column_name (str): The name of the new column to add.
        data_type (str): The data type of the new column.
        """
        conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            dbname=self.db_name,
        )
        cur = conn.cursor()

        cur.execute(
            f"""
            ALTER TABLE "{table_name}" ADD COLUMN IF NOT EXISTS "{column_name}" {data_type};
        """
        )

        conn.commit()
        cur.close()
        conn.close()

    def upload_to_db(self, data: Dict[str, pd.DataFrame]) -> None:
        """
        Uploads data from a dictionary of DataFrames to the specified tables in the PostgreSQL database.

        Parameters:
        data (Dict[str, pd.DataFrame]): A dictionary where keys are table names and values are DataFrames
                                        containing the data to be uploaded to the corresponding tables.

        Each DataFrame's rows are converted to JSON format and inserted into the 'data' column of the specified table.
        Assumes that the table structure includes a 'data' column of type JSONB.
        """
        conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            dbname=self.db_name,
        )
        cur = conn.cursor()
        for table_name, df in data.items():
            for _, row in df.iterrows():
                cur.execute(
                    f"""
                        INSERT INTO "{table_name}" (close, high, low) VALUES (%s, %s, %s)
                        """,
                    (row["Close"], row["High"], row["Low"]),
                )
        conn.commit()
        cur.close()
        conn.close()

        LOGGER.info(f"Successfully uploaded data to tables: {list(data.keys())}.")

    def get_latest_date(self, table_name) -> Optional[str]:
        """Get the latest 'created_at' date across all tables in the PostgreSQL database.

        Returns:
        Optional[str]: The latest 'updated_at' date as a string, or None if no dates are found.
        """
        if table_name not in self.get_existing_tables():
            return None
        conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            dbname=self.db_name,
        )
        cur = conn.cursor()
        cur.execute(
            f"""
            SELECT MAX(updated_at) FROM "{table_name}";
        """
        )
        date = cur.fetchone()[0]
        cur.close()
        conn.close()
        return date


# Usage Example:
# db_manager = DatabaseManager()
# latest_date = db_manager.get_latest_date('test1')
# print(latest_date)
