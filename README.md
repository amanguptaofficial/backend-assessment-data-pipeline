# Backend Developer Technical Assessment - Data Pipeline

A complete data pipeline implementation with Flask mock server, FastAPI ingestion service, and PostgreSQL database.

## Architecture

```
Flask Mock Server (Port 5000) → FastAPI Pipeline (Port 8000) → PostgreSQL (Port 5432)
```

**Data Flow:**
1. Flask serves customer data from JSON file
2. FastAPI fetches data from Flask with automatic pagination
3. FastAPI upserts data into PostgreSQL
4. Both services provide REST API endpoints

## Prerequisites

- Docker Desktop (running)
- Git

## Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── .env
├── .env.example
├── mock-server/
│   ├── app.py                  # Flask REST API
│   ├── data/customers.json     # 22 customer records
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py                 # FastAPI application
    ├── database.py             # Database connection
    ├── models/customer.py      # SQLAlchemy model
    ├── services/ingestion.py   # Data ingestion logic
    ├── Dockerfile
    └── requirements.txt
```

## Quick Start

### 1. Setup Environment

```bash
cp .env.example .env
```

The `.env` file contains default configuration:
- PostgreSQL credentials
- Service ports
- Connection URLs

### 2. Start All Services

```bash
docker compose up -d
```

This will:
- Start PostgreSQL container
- Build and start Flask mock server
- Build and start FastAPI pipeline service

**Wait 60 seconds** for all services to initialize.

### 3. Verify Services are Running

```bash
docker compose ps
```

You should see 3 containers running:
- `glynac-ai-assesment-postgres-1`
- `glynac-ai-assesment-mock-server-1`
- `glynac-ai-assesment-pipeline-service-1`

## API Endpoints

### Flask Mock Server (Port 5000)

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/health` | GET | Health check | - |
| `/api/customers` | GET | Get paginated customers | `page`, `limit` |
| `/api/customers/{id}` | GET | Get single customer | - |

**Example Response Format:**
```json
{
  "data": [...],
  "total": 22,
  "page": 1,
  "limit": 10
}
```

### FastAPI Pipeline (Port 8000)

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/health` | GET | Health check | - |
| `/api/ingest` | POST | Ingest data from Flask to PostgreSQL | - |
| `/api/customers` | GET | Get paginated customers from DB | `page`, `limit` |
| `/api/customers/{id}` | GET | Get single customer from DB | - |

**Ingestion Response:**
```json
{
  "status": "success",
  "records_processed": 22
}
```

## Testing

### Test Flask Mock Server

```bash
# Health check
curl http://localhost:5000/api/health

# Get customers with pagination
curl "http://localhost:5000/api/customers?page=1&limit=5"

# Get specific customer
curl http://localhost:5000/api/customers/CUST001
```

### Trigger Data Ingestion

```bash
curl -X POST http://localhost:8000/api/ingest
```

Expected response:
```json
{
  "status": "success",
  "records_processed": 22
}
```

### Query Data from FastAPI

```bash
# Get customers from database
curl "http://localhost:8000/api/customers?page=1&limit=5"

# Get specific customer
curl http://localhost:8000/api/customers/CUST001
```

### Automated Testing Script

```bash
./test-pipeline.sh
```

This script will:
1. Start all services
2. Test Flask endpoints
3. Trigger data ingestion
4. Test FastAPI endpoints
5. Display results

## Database Schema

**Table:** `customers`

| Column | Type | Constraints |
|--------|------|-------------|
| customer_id | VARCHAR(50) | PRIMARY KEY |
| first_name | VARCHAR(100) | NOT NULL |
| last_name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | NOT NULL |
| phone | VARCHAR(20) | - |
| address | TEXT | - |
| date_of_birth | DATE | - |
| account_balance | DECIMAL(15,2) | - |
| created_at | TIMESTAMP | - |

## Features Implemented

### Flask Mock Server
- ✅ Loads 22+ customers from JSON file
- ✅ Pagination support (page, limit parameters)
- ✅ Single customer lookup by ID
- ✅ 404 error handling for missing customers
- ✅ Health check endpoint
- ✅ Dockerized with requirements.txt

### FastAPI Pipeline
- ✅ Automatic pagination handling from Flask API
- ✅ Upsert logic (insert new, update existing records)
- ✅ SQLAlchemy ORM with PostgreSQL
- ✅ Proper data type conversion (dates, decimals)
- ✅ Error handling with appropriate HTTP status codes
- ✅ Database auto-initialization on startup
- ✅ All required endpoints implemented
- ✅ Dockerized with requirements.txt

### Docker Compose
- ✅ PostgreSQL 15 container with health checks
- ✅ Service dependencies configured
- ✅ Environment variables for configuration
- ✅ Port mappings for all services
- ✅ Network isolation and inter-service communication

## Environment Configuration

The `.env` file contains all configuration variables:

```bash
# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=customer_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Database Connection
DATABASE_URL=postgresql://postgres:password@postgres:5432/customer_db

# Flask Mock Server
FLASK_HOST=mock-server
FLASK_PORT=5000
FLASK_API_URL=http://mock-server:5000

# FastAPI Service
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

To customize configuration, edit `.env` and restart services:
```bash
docker compose down
docker compose up -d
```

## Useful Commands

### View Logs

```bash
# All services
docker compose logs

# Specific service
docker compose logs mock-server
docker compose logs pipeline-service
docker compose logs postgres

# Follow logs in real-time
docker compose logs -f
```

### Stop Services

```bash
docker compose down
```

### Stop and Remove Volumes

```bash
docker compose down -v
```

### Rebuild After Code Changes

```bash
docker compose down
docker compose up --build -d
```

### Access PostgreSQL Directly

```bash
docker exec -it glynac-ai-assesment-postgres-1 psql -U postgres -d customer_db
```

Then run SQL commands:
```sql
SELECT * FROM customers;
SELECT COUNT(*) FROM customers;
\q  -- to exit
```

## Troubleshooting

### Services won't start

```bash
docker compose down -v
docker compose up --build -d
```

### Port already in use

Check what's using the port:
```bash
lsof -i :5000
lsof -i :8000
lsof -i :5432
```

Change ports in `.env` file if needed.

### View detailed error logs

```bash
docker compose logs pipeline-service
```

### Verify Docker is running

```bash
docker info
```

## Technical Stack

- **Flask 3.0.0** - Mock server REST API
- **FastAPI 0.109.0** - Pipeline service
- **SQLAlchemy 2.0.25** - ORM for database operations
- **PostgreSQL 15** - Data storage
- **psycopg2-binary 2.9.9** - PostgreSQL adapter
- **Docker & Docker Compose** - Containerization
- **Python 3.10** - Programming language

## Code Quality

- Clean code architecture with separation of concerns
- Environment-based configuration
- Proper error handling and HTTP status codes
- Type hints and proper data validation
- Dockerized for easy deployment
- Health check endpoints for monitoring
- Idempotent ingestion (upsert logic)

## Submission Checklist

- [x] All 3 services start with `docker compose up`
- [x] Flask serves data with pagination
- [x] FastAPI ingests data successfully
- [x] All API endpoints work
- [x] Database schema matches requirements
- [x] Proper error handling
- [x] Documentation complete
- [x] Dockerfile for each service
- [x] requirements.txt for dependencies
