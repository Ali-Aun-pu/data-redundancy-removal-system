from src.database import update_review_status


result = update_review_status(2, "REJECTED")


if result == 1:
    print("Review status updated successfully!")
else:
    print("Review was not updated.")