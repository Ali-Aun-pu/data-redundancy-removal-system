-- ============================================
-- Data Redundancy Removal System
-- PostgreSQL Database Schema
-- ============================================


-- ============================================
-- 1. Customers Table
-- ============================================

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL
);


-- ============================================
-- 2. Duplicate Logs Table
-- ============================================

CREATE TABLE duplicate_logs (
    log_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    reason VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duplicate_field VARCHAR(50),

    CONSTRAINT unique_duplicate_log
        UNIQUE (customer_id, duplicate_field)
);


-- ============================================
-- 3. Potential Duplicate Review Queue
-- ============================================

CREATE TABLE duplicate_review_queue (
    review_id SERIAL PRIMARY KEY,
    customer_id INTEGER,
    name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    similarity_score DECIMAL(5,2),
    status VARCHAR(30) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    city VARCHAR(100)
);


-- Prevent multiple PENDING reviews
-- for the same customer.

CREATE UNIQUE INDEX unique_pending_review
ON duplicate_review_queue (customer_id)
WHERE status = 'PENDING';


-- ============================================
-- 4. Processed Records Table
-- ============================================

CREATE TABLE processed_records (
    customer_id INTEGER PRIMARY KEY,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);