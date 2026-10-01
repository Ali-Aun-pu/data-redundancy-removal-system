
import pandas as pd

from src.validation import validate_data


def test_valid_data():
    data = pd.DataFrame([
        {
            "customer_id": 1,
            "name": "Ali Ahmed",
            "email": "ali@gmail.com",
            "phone": "03001234567",
            "city": "Lahore"
        }
    ])

    result = validate_data(data)

    assert len(result) == 1
    assert result.iloc[0]["name"] == "Ali Ahmed"


def test_missing_required_field():
    data = pd.DataFrame([
        {
            "customer_id": 2,
            "name": "Ahmed Khan",
            "email": "ahmed@gmail.com",
            "phone": "03101234567"
        }
    ])

    try:
        validate_data(data)
        assert False, "Expected ValueError for missing city column"
    except ValueError as e:
        assert "Missing required column: city" in str(e)

