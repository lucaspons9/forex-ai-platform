# Forex Prediction Project

The objective of this project is to build an accurate forex intelligence platform with clean and complete data. The platform gathers, processes, and organizes forex data from various sources. This data will serve as a foundation for future machine learning models and other analytical tools to generate forex predictions and insights.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+
- PostgreSQL
- Poetry

### Setup

You can set up the project in two ways: using Poetry to run the files individually or using Docker Compose to build the entire structure.

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
- **Access FastAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)

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
