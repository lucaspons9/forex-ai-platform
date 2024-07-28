# Forex Prediction Project

This project aims to build an accurate forex prediction system. The project is divided into two main parts: data gathering and model configuration and deployment. The architecture leverages Docker for containerization and Airflow for automation of data gathering tasks. The models are built using PyTorch and deployed using FastAPI.

## Project Structure

```plaintext
forex-prediction/
├── config/
│   ├── tables.yaml
├── dags/
│   ├── data_pipeline_dag.py
├── database/
│   ├── init.sql
├── data_pipeline/
│   ├── gather/
│   │   ├── gather_data.py
│   │   ├── scrape_web.py
│   │   ├── api_fetch.py
│   ├── preprocess/
│   │   ├── clean_data.py
│   │   ├── transform_data.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
├── models/
│   ├── model.py
│   ├── train.py
│   ├── requirements.txt
│   ├── Dockerfile
├── app/
│   ├── main.py
│   ├── endpoints/
│   │   ├── predict.py
│   │   ├── query.py
│   ├── requirements.txt
│   ├── Dockerfile
├── airflow/
│   ├── dags/
│   ├── Dockerfile
│   ├── requirements.txt
├── docker-compose.yml
├── .env
└── README.md
```

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- PostgreSQL

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd forex-prediction
   ```

2. **Setup environment variables**:
   Create a `.env` file with the following variables:
   ```env
   DB_HOST=db
   DB_USER=user
   DB_PASSWORD=password
   DB_NAME=forex
   AIRFLOW__CORE__FERNET_KEY=your_fernet_key
   ```

3. **Build and run the Docker containers**:
   ```bash
   docker-compose up --build
   ```

### Components

#### 1. Data Pipeline

- **Gathering**: Scripts for web scraping and API data fetching.
  - `gather_data.py`
  - `scrape_web.py`
  - `api_fetch.py`

- **Preprocessing**: Scripts for cleaning and transforming data.
  - `clean_data.py`
  - `transform_data.py`

- **Main script**: Orchestrates data gathering and preprocessing.
  - `main.py`

#### 2. Models

- **model.py**: PyTorch model definition.
- **train.py**: Script to train the model.

#### 3. FastAPI Application

- **main.py**: Entry point for the FastAPI application.
- **endpoints/predict.py**: Endpoint for model predictions.
- **endpoints/query.py**: Endpoint for querying the database.

#### 4. Airflow

- **data_pipeline_dag.py**: Defines the Airflow DAG for data pipeline automation.

### Usage

- **Access Airflow**: [http://localhost:8080](http://localhost:8080)
- **Access FastAPI**: [http://localhost:8000/docs](http://localhost:8000)
  - `POST /predict` to get model predictions.
  - `GET /query` to query the database.

### Deployment

- **Database**: Start with local PostgreSQL. Migrate to AWS RDS for production.
- **Models**: Deploy using Docker. Consider AWS EC2 or AWS Sagemaker for scalable deployment.

### Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
