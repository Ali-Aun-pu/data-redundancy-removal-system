# Data Redundancy Removal System

A Python-based **Data Engineering pipeline** that validates customer data, detects duplicate records, and stores verified records in **PostgreSQL**.

The project demonstrates practical concepts such as **ETL, data validation, data quality, fuzzy matching, database integration, idempotent processing, Docker, and automated testing**.

## Features

* CSV data ingestion
* Required-field validation
* Exact duplicate detection using:

  * Customer ID
  * Email
  * Phone
* Fuzzy name matching using RapidFuzz
* Potential duplicate review queue
* Approve / Reject workflow
* PostgreSQL database integration
* Processed-record tracking
* Idempotent processing
* Logging and pipeline summary
* Docker and Docker Compose
* Automated testing with pytest

## Pipeline

```text
CSV
 |
Data Ingestion
 |
Validation
 |
Duplicate Detection
 |
 +----------------+---------------------+
 |                |                     |
UNIQUE        DUPLICATE        POTENTIAL DUPLICATE
 |                |                     |
Insert DB    Duplicate Log       Review Queue
 |                                      |
Processed                            Approve /
Record Tracking                       Reject
```

## Database

PostgreSQL is used as the target database.

Main tables:

* `customers` - Verified customer records
* `duplicate_logs` - Exact duplicate records
* `duplicate_review_queue` - Potential duplicates
* `processed_records` - Tracks processed records

Potential duplicates are identified using a **name similarity threshold of 85%**.

## Project Structure

```text
data-redundancy-removal-system/
|
+-- data/
|   +-- new_data.csv
+-- src/
|   +-- ingestion.py
|   +-- validation.py
|   +-- duplicate_detection.py
|   +-- database.py
|   +-- pipeline.py
+-- tests/
|   +-- conftest.py
|   +-- test_duplicate_detection.py
|   +-- test_duplicate_log.py
|   +-- test_potential_duplicate.py
|   +-- test_review_workflow.py
|   +-- test_validation.py
+-- sql/
|   +-- seed.sql
+-- Dockerfile
+-- docker-compose.yml
+-- requirements.txt
+-- .gitignore
+-- README.md
```

## Setup

Clone the repository:

```bash
git clone https://github.com/Ali-Aun-pu/data-redundancy-removal-system.git
cd data-redundancy-removal-system
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
DB_HOST=localhost
DB_NAME=data_redundancy_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5433
```

Run the pipeline:

```bash
python -m src.pipeline
```

## Docker

Start the complete Docker environment:

```bash
docker compose up
```

Or run in the background:

```bash
docker compose up -d
```

## Testing

Run all automated tests:

```bash
pytest -v
```

Current test suite:

```text
9 passed
```

## Tech Stack

* Python
* Pandas
* PostgreSQL
* Psycopg2
* RapidFuzz
* SQL
* Docker
* Docker Compose
* pytest
* python-dotenv

## Data Engineering Concepts

This project demonstrates:

**ETL -> Data Validation -> Data Quality -> Deduplication -> Database Loading -> Idempotent Processing**

## Future Improvements

* Apache Airflow orchestration
* PySpark implementation for large datasets
* REST API
* Web-based review dashboard
* Cloud database deployment
* CI/CD with GitHub Actions

## License

MIT License
