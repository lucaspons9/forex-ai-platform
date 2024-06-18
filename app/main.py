from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader, APIKey
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os

from utils.configs import read_config
from utils.logger import configure_logger

app = FastAPI()

# Define API key header
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Get API key from environment variables
API_KEY = os.getenv("FAST_API_KEY")

LOGGER = configure_logger(__file__)

# Database connection settings
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

SQL_COMMANDS = read_config(file_path="/app/config/sql_commands.yaml")

# Dependency function to validate API key
def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")


class TableQuery(BaseModel):
    table_name: str
    n: int


def get_db_connection():
    """Establishes and returns a database connection."""
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME,
    )
    return conn


@app.get("/health")
def health_check(api_key: APIKey = Depends(get_api_key)):
    """Check the health status of the API and the database connection."""
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "healthy"}
    except:
        raise HTTPException(status_code=500, detail="Database connection failed")


@app.get("/tables")
def get_existing_tables(api_key: APIKey = Depends(get_api_key)):
    """List all existing tables in the database."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    get_tables_sql = SQL_COMMANDS.get("get_existing_tables")
    cursor.execute(get_tables_sql)
    tables = [table["table_name"] for table in cursor.fetchall()]
    cursor.close()
    conn.close()
    return {"tables": tables}


@app.get("/latest-dates")
def get_latest_date(api_key: APIKey = Depends(get_api_key)):
    """Retrieve the latest date for each table in the database."""
    tables = get_existing_tables(api_key).get("tables", [])
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    latest_dates = {}
    # import os
    # LOGGER.critical(f"Current path: \n{os.getcwd()}, directories: {os.listdir(os.getcwd())}")
    latest_date_sql = SQL_COMMANDS.get("get_latest_date")
    for table in tables:
        cursor.execute(latest_date_sql.format(table_name=table))
        latest_date = cursor.fetchone()["max"]
        latest_dates[table] = latest_date
    cursor.close()
    conn.close()
    return {"latest_dates": latest_dates}


@app.post("/top-rows")
def get_top_rows(table_query: TableQuery, api_key: APIKey = Depends(get_api_key)):
    """Get the top n rows of a specified table."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = SQL_COMMANDS.get("get_top_rows").format(
            table_name=table_query.table_name, n=table_query.n
        )
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
    return result
