## data_pipeline/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements.txt from the data_pipeline directory
COPY data_pipeline/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory to /app in the container
# Copy the data_pipeline and utils directories
COPY data_pipeline /app/data_pipeline
COPY utils /app/utils
COPY config /app/config

# Set PYTHONPATH to include the /app directory
ENV PYTHONPATH /app

CMD ["python", "data_pipeline/pipeline.py"]
