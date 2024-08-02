# Use the official Apache Airflow image
FROM apache/airflow:2.3.3

# Copy requirements.txt and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Airflow
ENV AIRFLOW_HOME=/opt/airflow

# Expose the port Airflow runs on
EXPOSE 8080

# Command to run the webserver
CMD ["airflow", "webserver"]
