
from src.database import (
    approve_review,
    reject_review,
    update_review_status
)


def test_update_review_status():
    review_id = 99991

    result = update_review_status(
        review_id,
        "APPROVED"
    )

    assert result == 0


def test_approve_non_existing_review():
    result = approve_review(99991)

    assert result is False


def test_reject_non_existing_review():
    result = reject_review(99992)

    assert result is False

