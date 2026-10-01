# Data Redundancy Removal System

This project implements a **Python-based data validation and duplicate detection pipeline** for customer data. It processes incoming CSV records, validates data quality, detects exact and potential duplicates, and stores verified unique records in **PostgreSQL**.

The system demonstrates practical **Data Engineering concepts** including data ingestion, validation, data quality checks, duplicate detection, PostgreSQL database integration, logging, Docker containerization, and automated testing.

## 📂 Project Structure

* `data/` – Input CSV files
* `src/` – Core pipeline source code

  * `ingestion.py` – Loads customer data from CSV
  * `validation.py` – Validates required fields
  * `duplicate_detection.py` – Detects exact and potential duplicates
  * `database.py` – Handles PostgreSQL database operations
  * `pipeline.py` – Runs the complete data processing pipeline
* `tests/` – Automated tests
* `logs/` – Pipeline execution logs
* `docker-compose.yml` – Docker services configuration
* `.env` – Database environment configuration
* `requirements.txt` – Python dependencies
* `README.md` – Project documentation

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd data-redundancy-removal-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file with your PostgreSQL database configuration:

```text
DB_HOST=localhost
DB_NAME=data_redundancy_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5433
```

### 5. Run the pipeline

```bash
python -m src.pipeline
```

## 🐳 Running with Docker

The project also supports Docker for running the PostgreSQL database and data pipeline.

Start the services with:

```bash
docker compose up
```

The PostgreSQL container provides the database while the pipeline container processes the incoming customer data.

## 🗄️ Database

The project uses **PostgreSQL** to store and manage customer records.

Main tables include:

* `customers` – Stores verified unique customer records
* `duplicate_logs` – Stores detected exact duplicates
* `duplicate_review_queue` – Stores potential duplicates requiring review
* `processed_records` – Tracks records that have already been processed

## 🔍 Duplicate Detection

The system uses two levels of duplicate detection.

### Exact Duplicate Detection

Records are checked using:

* Customer ID
* Email
* Phone number

If any of these fields already exist in the database, the record is classified as a **DUPLICATE**.

### Potential Duplicate Detection

Records that are not exact duplicates are checked using **fuzzy name similarity**.

The project uses `RapidFuzz` to calculate similarity between customer names.

Records with a similarity score of **85 or higher** are classified as:

```text
POTENTIAL_DUPLICATE
```

These records are placed into the review queue instead of being automatically inserted.

## 🔄 Review Workflow

Potential duplicates can be manually reviewed.

```text
Incoming Record
       ↓
Data Validation
       ↓
Duplicate Detection
       ↓
Potential Duplicate
       ↓
Review Queue
     ↙     ↘
 APPROVE   REJECT
    ↓         ↓
 Database   Discard
```

Approved records are inserted into the `customers` table.

Rejected records are not inserted and are marked as processed to prevent repeated processing.

## ⚙️ Pipeline Workflow

```text
CSV File
   ↓
Data Ingestion
   ↓
Data Validation
   ↓
Exact Duplicate Check
   ↓
Fuzzy Name Similarity
   ↓
 ┌───────────────┬────────────────────┐
 ↓               ↓                    ↓
UNIQUE       DUPLICATE       POTENTIAL DUPLICATE
 ↓               ↓                    ↓
Insert DB    Duplicate Log       Review Queue
 ↓
Processed Record Tracking
```

## 🧪 Testing

The project uses **pytest** for automated testing.

Run all tests with:

```bash
pytest -v
```

Current test result:

```text
9 passed in 2.41s
```

The tests cover:

* Exact duplicate detection
* Potential duplicate detection
* Data validation
* Duplicate logging
* Potential duplicate review queue
* Review status updates
* Approve workflow
* Reject workflow
* Database integration

## 🛠️ Tech Stack

* **Python**
* **Pandas**
* **PostgreSQL**
* **Psycopg2**
* **RapidFuzz**
* **SQL**
* **Docker**
* **Docker Compose**
* **pytest**
* **python-dotenv**
* **Logging**

## ✨ Key Features

* CSV-based data ingestion
* Required-field validation
* Exact duplicate detection
* Fuzzy duplicate detection
* Similarity scoring
* PostgreSQL database integration
* Duplicate logging
* Potential duplicate review queue
* Approve/reject workflow
* Processed-record tracking
* Idempotent processing
* Error handling
* Pipeline execution logging
* Dockerized environment
* Automated testing

## 📊 Example Pipeline Output

```text
Loaded 3 records from data/new_data.csv

SKIPPED: Customer 21 already processed
SKIPPED: Customer 22 already processed
ALREADY IN REVIEW QUEUE: Ali Ahamed

========== PIPELINE SUMMARY ==========
Records loaded:        3
Unique inserted:       0
Duplicates found:      0
Potential duplicates:  0
Skipped records:       2
Rejected by database:  0
Errors:                0
======================================
```

## 📈 Project Outcome

The project demonstrates how a data quality pipeline can prevent redundant customer records from entering a database while providing a controlled review process for records that may represent duplicates.

It combines **data validation, data quality rules, fuzzy matching, database operations, logging, containerization, and automated testing** into an end-to-end Data Engineering workflow.

## 📜 License

This project is licensed under the MIT License.
