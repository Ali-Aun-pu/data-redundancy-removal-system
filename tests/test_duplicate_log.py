from src.database import get_connection, log_duplicate


def test_log_duplicate():
    customer = {
        "customer_id": 99991,
        "name": "Test Customer",
        "email": "test.duplicate@example.com",
        "phone": "03999999999",
        "city": "Lahore"
    }

    # Remove previous test record if it exists
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM duplicate_logs
        WHERE customer_id = %s
        """,
        (99991,)
    )

    connection.commit()
    cursor.close()
    connection.close()

    # First logging should succeed
    result = log_duplicate(
        customer,
        "DUPLICATE",
        "EMAIL"
    )

    assert result is True

    # Second logging should be prevented
    result_again = log_duplicate(
        customer,
        "DUPLICATE",
        "EMAIL"
    )

    assert result_again is False