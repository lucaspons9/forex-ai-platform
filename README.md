# **Forex Intelligence & Prediction Platform**

The **Forex Intelligence & Prediction Platform** is an end-to-end solution designed to harness financial data and machine learning to make informed forex trading decisions. It combines a **robust data infrastructure** with **advanced predictive models**, enabling systematic trade execution based on data-driven signals.

## 🚀 Project Overview

This platform consists of two integrated components:

1. **Forex Intelligence Platform**: A fully automated data pipeline that gathers, processes, and stores forex-related data in a structured and accessible format.
2. **Machine Learning & Strategy Development**: A predictive modeling framework that utilizes historical data to generate trading signals, optimize risk management, and backtest profitable strategies.

---

## 📡 **1. Forex Intelligence Platform**
### **Data Infrastructure & Management**
The Forex Intelligence Platform is responsible for continuously fetching, cleaning, and structuring forex data from multiple sources. It ensures high-quality, up-to-date financial data for analysis and trading strategy development.

### **Key Features**
- **Automated Data Ingestion**: Uses **Apache Airflow** to schedule, extract, and update forex data.
- **Centralized Storage**: Stores structured forex data in a **PostgreSQL** database.
- **API for Data Access**: A **FastAPI** service provides endpoints to query forex data efficiently.
- **Scalability & Monitoring**: Designed for seamless deployment with **Docker Compose**, allowing local and cloud execution.

---

## 📊 **2. Machine Learning & Strategy Development**
### **Predictive Modeling for Forex Trading**
Leveraging structured data from the intelligence platform, this component applies advanced **machine learning models** (LSTM-based deep learning architectures) to predict market movements and generate actionable trading signals.

### **Core Functionalities**
- **Trend Classification**: Uses **LSTMs** to forecast the probability of an upward, downward, or neutral trend.
- **Backtesting & Evaluation**: Simulates trading strategies on historical data to assess profitability and risk-adjusted returns.
- **Risk Management Strategies**: Implements dynamic **position sizing, stop-loss tiers, and volatility-adjusted trade execution**.
- **Automated Strategy Iteration**: Continuously optimizes signals, thresholds, and risk parameters for better consistency.

This system demonstrates how even models with moderate accuracy can yield profitable results when paired with **robust trading rules**.

---

## 🛠 **Getting Started**
This platform can be deployed **containerized** using Docker Compose.

### **Prerequisites**
- Python 3.9+
- Docker & Docker Compose
- PostgreSQL
- Poetry

### **Steps**
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd forex-intelligence-platform
   ```
2. Configure environment variables:  
   Create a `.env` file with:
   ```env
   DB_HOST=db
   DB_USER=user
   DB_PASSWORD=password
   DB_NAME=forex
   FAST_API_KEY=custom_fastapi_key
   ```
3. Build and start all services:
   ```bash
   docker-compose up --build
   ```

This will launch the data pipeline, database, and API services in separate containers.

---

🔍 **Usage & API Endpoints**
- **Access Airflow:** [http://localhost:8080](http://localhost:8080) – Monitor data ingestion tasks.
- **Access FastAPI:** [http://localhost:8000/docs](http://localhost:8000/docs) – Explore API endpoints.

**Example API Endpoints**

| Endpoint              | Description                                                          |
|-----------------------|----------------------------------------------------------------------|
| **GET /health**       | Checks API and database connection status.                           |
| **GET /tables**       | Lists available database tables.                                     |
| **GET /latest-dates** | Retrieves the latest data update for each table.                     |
| **POST /top-rows**    | Fetches top rows from a specific table (requires request body).        |

---

📈 **Future Enhancements**
- **Cloud Deployment:** Move PostgreSQL to AWS RDS and deploy models via AWS EC2 or SageMaker.
- **Reinforcement Learning Strategies:** Integrate RL-based decision-making for adaptive trading strategies.
- **Sentiment Analysis:** Incorporate news sentiment analysis to improve predictive accuracy.

---

🤝 **Contributing**

This is an open-source project, and contributions are welcome!  
To contribute:
1. Fork the repository.
2. Create a feature branch (`feature-branch-name`).
3. Submit a pull request with a detailed explanation.
