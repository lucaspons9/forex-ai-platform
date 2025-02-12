# Forex Intelligence & Prediction Project

Welcome to the **Forex Intelligence & Prediction Project**, an end-to-end solution that:

1. **Builds a robust Forex Intelligence Platform** — a fully automated data pipeline to gather, process, and store forex-related data.
2. **Implements Machine Learning models and trading strategies** — leveraging the platform’s data to forecast price movements and develop profitable, risk-managed trading systems.

---

## 1. Forex Intelligence Platform

### Overview
This platform is responsible for **fetching, cleaning, and storing** forex data from multiple sources so it’s always up-to-date and ready for analysis. Key components include:

- **Airflow** for job scheduling, ensuring routine data ingestion and database updates.
- **PostgreSQL** for structured storage of all historical and newly acquired forex data.
- **FastAPI** for quick data retrieval and health checks, offering a user-friendly interface to the database.

### Core Features
- **Continuous Data Fetching**: Automated pipelines to pull forex rates, economic indicators, and more.
- **Clean & Standardized Data**: Consolidates messy or fragmented sources into a coherent schema.
- **Centralized Storage**: Maintains a PostgreSQL database with relevant tables, each updated by Airflow DAGs.
- **User-Focused Endpoints**: FastAPI endpoints to explore table lists, retrieve top rows, and track latest data ingestion status.

---

## 2. Machine Learning & Strategy Development

### Overview
Using the Intelligence Platform’s high-quality data, the second part applies advanced **machine learning algorithms** (like LSTMs or other ML models) to forecast forex price movements. The main goals are:

- **Predictive Modeling**: Train, validate, and tune models for short-term or long-term predictions (classification or regression).
- **Backtesting & Evaluation**: Simulate potential strategies on historical data to gauge performance metrics (accuracy, drawdown, etc.).
- **Risk Management**: Incorporate dynamic position sizing, stop-loss and trailing stops, partial take-profit, and other protective measures.
- **Strategy Iteration**: Continuously refine signals, thresholds, and money-management rules for more consistent returns.

This part is currently **under development**, but it already shows promise in generating signals that can be translated into real trades.

---

## Getting Started

You can run this project in two main ways: 
1. **Locally** via [Poetry](https://python-poetry.org/docs/).
2. **Containerized** using [Docker Compose](https://docs.docker.com/compose/).

### Prerequisites
- Docker & Docker Compose  
- Python 3.9+  
- PostgreSQL  
- Poetry  

#### Option 1: Using Poetry

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd forex-prediction
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Run individual scripts**:
   ```bash
   poetry run python path/to/your_script.py
   ```

#### Option 2: Using Docker Compose

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
   FAST_API_KEY=custom_fastapi_key
   ```

3. **Build and run the Docker containers**:
   ```bash
   docker-compose up --build
   ```

This command will build and start all the necessary Docker containers, including the database container. The database will be created and fed with the most up-to-date data.

### Usage

- **Access Airflow**: [http://localhost:8080](http://localhost:8080)
- **Access FastAPI**: [http://localhost:8000/docs](http://localhost:8000)

#### FastAPI Endpoints

- **GET /health**: Check the health status of the API and the database connection.
- **GET /tables**: List all existing tables in the database.
- **GET /latest-dates**: Retrieve the latest date for each table in the database.
- **POST /top-rows**: Get the top n rows of a specified table. You need to pass the table name and the number of rows in the request body.

### Deployment

- **Database**: Start with local PostgreSQL. Migrate to AWS RDS for production.
- **Models**: Deploy using Docker. Consider AWS EC2 or AWS Sagemaker for scalable deployment.

### Contributing

This is an open-source project, and we welcome contributions from the community.

If you'd like to contribute, please fork the repository and make changes as you'd like. Pull requests are warmly welcome.

### License

This project is licensed under the MIT License - see the LICENSE file for details.
