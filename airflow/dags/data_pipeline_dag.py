# airflow/dags/data_pipeline_dag.py

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Assuming you have a function named 'run_pipeline' in your data pipeline script
from data_pipeline.pipeline import DataPipeline

# Define default_args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate the DAG
dag = DAG(
    'data_pipeline_daily',
    default_args=default_args,
    description='Run DataPipeline daily',
    schedule_interval='@daily',
)


# Define the task function
def run_data_pipeline():
    pipeline = DataPipeline()
    pipeline.run_pipeline(save_results=True)


# Create a PythonOperator to run the task
run_pipeline_task = PythonOperator(
    task_id='run_data_pipeline',
    python_callable=run_data_pipeline,
    dag=dag,
)
