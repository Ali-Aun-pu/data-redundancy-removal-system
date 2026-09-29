from src.database import log_duplicate


customer = {
    "customer_id": 7,
    "name": "Ali Ahmed",
    "email": "ali@gmail.com",
    "phone": "03001234567",
    "city": "Lahore"
}


log_duplicate(
    customer,
    "EMAIL_OR_PHONE_DUPLICATE"
)

print("Duplicate logged successfully!")