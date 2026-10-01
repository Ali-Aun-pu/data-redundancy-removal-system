
import pandas as pd

from src.duplicate_detection import classify_records


def test_exact_duplicate():
    existing_data = pd.DataFrame([
        {
            "customer_id": 1,
            "name": "Zain Abbas",
            "email": "zain@gmail.com",
            "phone": "03051234567",
            "city": "Lahore"
        }
    ])

    new_data = pd.DataFrame([
        {
            "customer_id": 2,
            "name": "Zain Abbas",
            "email": "zain@gmail.com",
            "phone": "03151234567",
            "city": "Lahore"
        }
    ])

    results = classify_records(new_data, existing_data)

    assert results[0]["status"] == "DUPLICATE"
    assert results[0]["duplicate_field"] == "EMAIL"


def test_potential_duplicate():
    existing_data = pd.DataFrame([
        {
            "customer_id": 1,
            "name": "Ali Ahamed",
            "email": "ali@gmail.com",
            "phone": "03001234567",
            "city": "Lahore"
        }
    ])

    new_data = pd.DataFrame([
        {
            "customer_id": 2,
            "name": "Ali Ahamed",
            "email": "ali.new@gmail.com",
            "phone": "03121234567",
            "city": "Lahore"
        }
    ])

    results = classify_records(new_data, existing_data)

    assert results[0]["status"] == "POTENTIAL_DUPLICATE"
    assert results[0]["similarity_score"] >= 85
