from src.database import insert_if_unique


customer = {
    "customer_id": 1,
    "name": "Different Person",
    "email": "different@gmail.com",
    "phone": "03199999999",
    "city": "Lahore"
}


result = insert_if_unique(customer)


if result:
    print("Customer inserted successfully!")
else:
    print("Duplicate customer rejected!")