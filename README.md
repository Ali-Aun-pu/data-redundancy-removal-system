# Data Redundancy Removal System

A Python and PostgreSQL-based data engineering pipeline that validates incoming customer data, detects duplicate records, identifies potential duplicates using fuzzy matching, and prevents redundant records from being inserted into the database.

## Project Objectives

- Validate incoming customer data
- Normalize phone numbers and other fields
- Detect exact duplicate records
- Detect potential duplicates using fuzzy matching
- Store duplicate records in an audit log
- Send potential duplicates to a manual review queue
- Approve or reject potential duplicates
- Prevent duplicate records using PostgreSQL constraints
- Track processed records to prevent reprocessing
- Maintain pipeline logs

## Architecture

CSV Data
    |
    v
Data Ingestion
    |
    v
Data Validation
    |
    v
Duplicate Detection
    |
    +-------------------+
    |                   |
    v                   v
DUPLICATE          POTENTIAL DUPLICATE
    |                   |
    v                   v
Duplicate Logs     Review Queue
                        |
                  +-----+-----+
                  |           |
                  v           v
               APPROVE      REJECT
                  |           |
                  v           v
             Customers     Not Inserted
                  |
                  +-----+
                        |
                        v
                Processed Records

## Technologies

- Python
- Pandas
- PostgreSQL
- SQL
- RapidFuzz
- Git

## Main Components

### Data Ingestion
Loads incoming CSV data using Pandas.

### Data Validation
Checks required fields, removes invalid records, normalizes text fields, and standardizes Pakistani phone numbers.

### Duplicate Detection
Uses exact matching for customer ID, email, and phone number.

Fuzzy matching with RapidFuzz is used to identify potential duplicate names.

### PostgreSQL Database
Stores:

- Unique customer records
- Duplicate logs
- Potential duplicate review records
- Processed record information

### Review System
Potential duplicates can be manually:

- APPROVED
- REJECTED

Approved records are inserted into the customers table.

Rejected records are not inserted and are marked as processed.

## Project Structure

data-redundancy-removal-system/
|
├── data/
├── src/
│   ├── ingestion.py
│   ├── validation.py
│   ├── duplicate_detection.py
│   ├── pipeline.py
│   └── database.py
|
├── sql/
│   └── database.sql
|
├── logs/
├── tests/
├── requirements.txt
└── README.md

## How to Run

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate