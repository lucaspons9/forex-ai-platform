import psycopg2
import os
import yaml


def create_tables():
    with open('/app/config/tables.yaml', 'r') as file:
        tables = yaml.safe_load(file)['tables']

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )
    cur = conn.cursor()

    for table in tables:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id SERIAL PRIMARY KEY,
                data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

    conn.commit()
    cur.close()
    conn.close()


def main():
    create_tables()


if __name__ == '__main__':
    main()
