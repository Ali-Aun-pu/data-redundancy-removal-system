from src.database import get_connection, log_potential_duplicate


def test_log_potential_duplicate():
    customer = {
        "customer_id": 99992,
        "name": "Test Potential",
        "email": "test.potential@example.com",
        "phone": "03888888888",
        "city": "Lahore",
        "similarity_score": 90.91
    }

    # Remove previous test record if it exists
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM duplicate_review_queue
        WHERE customer_id = %s
        """,
        (99992,)
    )

    connection.commit()
    cursor.close()
    connection.close()

    # First logging should succeed
    result = log_potential_duplicate(customer)

    assert result is True

    # Second logging should be prevented
    result_again = log_potential_duplicate(customer)

    assert result_again is False