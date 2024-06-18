import os
import time
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd
import psycopg2
from psycopg2 import OperationalError

from utils.configs import read_config
from utils.logger import configure_logger

LOGGER = configure_logger(__file__)


class DatabaseManager:
    def __init__(self):
        self.db_host: str = os.getenv("DB_HOST")
        self.db_user: str = os.getenv("DB_USER")
        self.db_password: str = os.getenv("DB_PASSWORD")
        self.db_name: str = os.getenv("DB_NAME")
        self.sql_commands = read_config(file_path="config/sql_commands.yaml")

    def postgres_running_check(self, timeout: int = 60) -> bool:
        """Wait for PostgreSQL to be ready before proceeding. Return True when it is running."""
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
        get_tables_sql = self.sql_commands["get_existing_tables"]
        cur.execute(get_tables_sql)
        existing_tables = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
        return existing_tables

    def create_table(self, table_name: str, df: pd.DataFrame):
        conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            dbname=self.db_name,
        )
        cur = conn.cursor()
        columns = ", ".join(
            [
                f"{col} DOUBLE PRECISION"
                for col in df.columns
                if col != "date" and col != "Date"
            ]
        )
        create_table_sql = self.sql_commands["create_table"].format(
            table_name=table_name, columns=columns
        )
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
        conn.close()

    def upload_to_db(
        self, extracted_data_dict: Dict[str, Dict[str, Dict[str, pd.DataFrame]]]
    ):
        existing_tables = self.get_existing_tables()

        for category, data_types in extracted_data_dict.items():
            for data_type, data in data_types.items():
                for name, df in data.items():
                    table_name = f"{category}_{data_type}_{name}".lower()

                    if table_name not in existing_tables:
                        self.create_table(table_name, df)

                    self.insert_data(table_name, df)

                    LOGGER.warning(
                        f"Successfully uploaded data to table: {table_name}."
                    )

    def insert_data(self, table_name: str, df: pd.DataFrame):
        conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            dbname=self.db_name,
        )
        cur = conn.cursor()

        for index, row in df.iterrows():
            values = []
            for col in df.columns:
                value = row[col]
                if pd.isna(value):
                    values.append("NULL")
                elif isinstance(value, datetime):
                    values.append(f"'{value.strftime('%Y-%m-%d')}'")
                elif isinstance(value, str):
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))

            columns = ", ".join([col for col in df.columns])
            values_str = ", ".join(values)
            update_columns = ", ".join(
                [
                    f"{col} = EXCLUDED.{col}"
                    for col in df.columns
                    if col.lower() != "date"
                ]
            )

            insert_data_sql = self.sql_commands["insert_data"].format(
                table_name=table_name,
                columns=columns,
                values=values_str,
                update_columns=update_columns,
            )
            cur.execute(insert_data_sql)

        conn.commit()
        cur.close()
        conn.close()

    def get_latest_date(self, table_name: str) -> Optional[str]:
        if table_name not in self.get_existing_tables():
            return None
        conn = psycopg2.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            dbname=self.db_name,
        )
        cur = conn.cursor()
        get_latest_date_sql = self.sql_commands["get_latest_date"].format(
            table_name=table_name
        )
        cur.execute(get_latest_date_sql)
        latest_date = cur.fetchone()[0]
        cur.close()
        conn.close()
        return latest_date
