# Production-Grade FastAPI REST API (Data Engineering Practice)

A highly robust, production-ready ERP/CRM simulator built with **FastAPI** and **PostgreSQL**. This API acts as the perfect source system for Data Engineers to practice building Bronze, Silver, and Gold data pipelines using tools like Airflow, Spark, Databricks, Snowflake, Kafka, and dbt.

## 🚀 Key Features

* **Data Engineering First**: Tailor-made for CDC (Change Data Capture) and ELT/ETL pipelines.
* **Incremental Loading**: Every endpoint supports `updated_after` and `created_after` query parameters.
* **Bulk Extraction**: Dedicated `/api/v1/export/{resource}` endpoints to stream vast amounts of data in `csv` or `json` formats natively using `pandas`.
* **Chaos Engineering Simulator**: Built-in middleware perfectly simulates real-world anomalies! It randomly injects latencies (up to 2 seconds) and `500 Internal Server Errors` (5% chance) to force you to write resilient extraction pipelines with robust retry logic.
* **Clean Architecture**: Highly modular design utilizing the Repository and Service patterns.
* **Enterprise Security**: JWT Authentication with comprehensive Role-Based Access Control (Admin, Manager, Data Engineer, Analyst, Viewer).
* **Massive Data Generator**: Includes a `generate_data.py` script powered by `Faker` to pump thousands of realistic records into the database.

---

## 🛠️ Technology Stack

* **Language**: Python 3.12
* **Framework**: FastAPI
* **Database**: PostgreSQL
* **ORM & Migrations**: SQLAlchemy 2.0 (Async) & Alembic
* **Validation**: Pydantic v2
* **Authentication**: JWT & `bcrypt`
* **Containerization**: Docker & Docker Compose

---

## 🚦 Quick Start Guide

### 1. Start the Environment
Everything is containerized. Start the PostgreSQL database and FastAPI server using Docker Compose:

```bash
docker compose up -d --build
```

### 2. Apply Database Migrations
Create the tables in the PostgreSQL database:
```bash
docker compose exec api alembic upgrade head
```

### 3. Generate Mock Data
Populate the database with thousands of Customers, Products, Orders, and Payments so you have data to extract:
```bash
docker compose exec api python scripts/generate_data.py
```
*(Note: The script gracefully handles intentional rate limits and 500 errors injected by the Chaos Middleware!)*

### 4. Access the API
* **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc API Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🏗️ Domain Models & Endpoints

The system simulates a complete Enterprise Resource Planning (ERP) environment. 

### Advanced Querying Parameters
Most `GET` endpoints support the following query parameters:
* `skip` (int): Offset pagination.
* `limit` (int): Max records to return.
* `sort_by` (string): Column to sort by.
* `order` (asc|desc): Sort direction.
* `fields` (string): Comma-separated list of fields to return.
* `updated_after` / `created_after` (ISO DateTime): For incremental pipeline loading.

### 1. Data Extraction (Bulk)
Designed specifically for Data Engineers pulling large volumes of data.
* `GET /api/v1/export/{resource}` (Supports `?format=csv` and `?format=json`)
  *(Resources: orders, customers, products, payments, etc.)*

### 2. Authentication & Users
* `POST /api/v1/auth/register`: Create a new user.
* `POST /api/v1/auth/login`: Authenticate and receive a JWT token.
* `GET /api/v1/auth/me`: Get current user info.

### 3. Catalog
* `GET / POST /api/v1/catalog/categories`
* `GET / POST /api/v1/catalog/products`

### 4. People
* `GET / POST /api/v1/people/customers`
* `GET / POST /api/v1/people/employees`
* `GET / POST /api/v1/people/suppliers`

### 5. Transactions
* `GET / POST /api/v1/transactions/orders`
* `GET / POST /api/v1/transactions/payments`
* `GET / POST /api/v1/transactions/invoices`
* `GET / POST /api/v1/transactions/shipments`

### 6. Inventory
* `GET / POST /api/v1/inventory/warehouses`
* `GET / POST /api/v1/inventory/inventory`

### 7. Location
* `GET / POST /api/v1/location/countries`
* `GET / POST /api/v1/location/states`
* `GET / POST /api/v1/location/cities`
* `GET / POST /api/v1/location/stores`
* `GET / POST /api/v1/location/departments`
* `GET / POST /api/v1/location/addresses`

---

## 🧪 Testing

The API includes an integration test suite configured to use an isolated async event loop.
To run the tests:
```bash
docker compose exec -e PYTHONPATH=/app api pytest tests/
```

Enjoy building your Data Engineering pipelines! 🚀
