import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_connection():

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "data_redundancy_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", "5432")
    )

    return connection


def insert_customer(customer):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO customers (customer_id, name, email, phone, city)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            int(customer["customer_id"]),
            str(customer["name"]),
            str(customer["email"]),
            str(customer["phone"]),
            str(customer["city"])
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def insert_if_unique(customer):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Check whether customer already exists
        query = """
            SELECT customer_id
            FROM customers
            WHERE customer_id = %s
               OR email = %s
               OR phone = %s
        """

        cursor.execute(
            query,
            (
                int(customer["customer_id"]),
                str(customer["email"]),
                str(customer["phone"])
            )
        )

        existing_customer = cursor.fetchone()

        # Reject duplicate found during pre-check
        if existing_customer:

            return False

        # Insert unique customer
        insert_query = """
            INSERT INTO customers
            (customer_id, name, email, phone, city)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (
                int(customer["customer_id"]),
                str(customer["name"]),
                str(customer["email"]),
                str(customer["phone"]),
                str(customer["city"])
            )
        )

        connection.commit()

        return True

    except psycopg2.IntegrityError:

        # Undo the failed transaction
        connection.rollback()

        return False

    finally:

        cursor.close()
        connection.close()


def get_existing_customers():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT customer_id, name, email, phone, city
        FROM customers
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    columns = [
        "customer_id",
        "name",
        "email",
        "phone",
        "city"
    ]

    cursor.close()
    connection.close()

    return pd.DataFrame(rows, columns=columns)



def log_duplicate(customer, reason, duplicate_field):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Check whether this duplicate has already been logged
        check_query = """
            SELECT log_id
            FROM duplicate_logs
            WHERE customer_id = %s
              AND duplicate_field = %s
        """

        cursor.execute(
            check_query,
            (
                int(customer["customer_id"]),
                str(duplicate_field)
            )
        )

        existing_log = cursor.fetchone()

        # Do not create another duplicate log
        if existing_log:

            return False

        # Insert new duplicate log
        insert_query = """
            INSERT INTO duplicate_logs
            (
                customer_id,
                name,
                email,
                phone,
                reason,
                duplicate_field
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (
                int(customer["customer_id"]),
                str(customer["name"]),
                str(customer["email"]),
                str(customer["phone"]),
                str(reason),
                str(duplicate_field)
            )
        )

        connection.commit()

        return True

    finally:

        cursor.close()
        connection.close()



def log_potential_duplicate(customer):

    connection = get_connection()
    cursor = connection.cursor()

    # Check if this customer is already pending review
    check_query = """
        SELECT review_id
        FROM duplicate_review_queue
        WHERE customer_id = %s
          AND status = 'PENDING'
    """

    cursor.execute(
        check_query,
        (int(customer["customer_id"]),)
    )

    existing_review = cursor.fetchone()

    # If already pending, do not insert another record
    if existing_review:

        cursor.close()
        connection.close()

        return False

    # Insert new potential duplicate
    insert_query = """
        INSERT INTO duplicate_review_queue
        (
            customer_id,
            name,
            email,
            phone,
            city,
            similarity_score
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        insert_query,
        (
            int(customer["customer_id"]),
            str(customer["name"]),
            str(customer["email"]),
            str(customer["phone"]),
            str(customer["city"]),
            float(customer["similarity_score"])
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return True

def update_review_status(review_id, new_status):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE duplicate_review_queue
        SET status = %s
        WHERE review_id = %s
          AND status = 'PENDING'
    """

    cursor.execute(
        query,
        (
            str(new_status),
            int(review_id)
        )
    )

    connection.commit()

    rows_updated = cursor.rowcount

    cursor.close()
    connection.close()

    return rows_updated


def approve_review(review_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Get the pending review
        select_query = """
            SELECT
                customer_id,
                name,
                email,
                phone,
                city
            FROM duplicate_review_queue
            WHERE review_id = %s
              AND status = 'PENDING'
        """

        cursor.execute(
            select_query,
            (int(review_id),)
        )

        review = cursor.fetchone()

        # Review does not exist or is not pending
        if not review:

            return False

        customer_id, name, email, phone, city = review

        # Insert the approved customer
        insert_query = """
            INSERT INTO customers
            (
                customer_id,
                name,
                email,
                phone,
                city
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            insert_query,
            (
                customer_id,
                name,
                email,
                phone,
                city
            )
        )

        # Mark review as approved
        update_query = """
            UPDATE duplicate_review_queue
            SET status = 'APPROVED'
            WHERE review_id = %s
        """

        cursor.execute(
            update_query,
            (int(review_id),)
        )

        # Mark customer as processed
        processed_query = """
            INSERT INTO processed_records (customer_id)
            VALUES (%s)
            ON CONFLICT (customer_id)
            DO NOTHING
        """

        cursor.execute(
            processed_query,
            (customer_id,)
        )

        # Commit all changes together
        connection.commit()

        return True

    except psycopg2.IntegrityError:

        # Undo all changes if something fails
        connection.rollback()

        return False

    finally:

        cursor.close()
        connection.close()

def get_processed_customer_ids():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT customer_id
        FROM processed_records
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return {row[0] for row in rows}

def mark_customer_processed(customer_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO processed_records (customer_id)
        VALUES (%s)
        ON CONFLICT (customer_id)
        DO NOTHING
    """

    cursor.execute(
        query,
        (int(customer_id),)
    )

    connection.commit()

    cursor.close()
    connection.close()

def reject_review(review_id):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # Get the pending review
        select_query = """
            SELECT customer_id
            FROM duplicate_review_queue
            WHERE review_id = %s
              AND status = 'PENDING'
        """

        cursor.execute(
            select_query,
            (int(review_id),)
        )

        review = cursor.fetchone()

        # Review does not exist or is not pending
        if not review:

            return False

        customer_id = review[0]

        # Mark review as rejected
        update_query = """
            UPDATE duplicate_review_queue
            SET status = 'REJECTED'
            WHERE review_id = %s
              AND status = 'PENDING'
        """

        cursor.execute(
            update_query,
            (int(review_id),)
        )

        # Mark customer as processed
        processed_query = """
            INSERT INTO processed_records (customer_id)
            VALUES (%s)
            ON CONFLICT (customer_id)
            DO NOTHING
        """

        cursor.execute(
            processed_query,
            (customer_id,)
        )

        # Commit both operations together
        connection.commit()

        return True

    except psycopg2.IntegrityError:

        connection.rollback()

        return False

    finally:

        cursor.close()
        connection.close()