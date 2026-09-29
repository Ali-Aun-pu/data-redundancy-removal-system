from src.database import insert_customer


duplicate_customer = {
    "customer_id": 1,
    "name": "Test Customer",
    "email": "ali@gmail.com",
    "phone": "03199999999",
    "city": "Lahore"
}


try:

    insert_customer(duplicate_customer)

    print("Customer inserted successfully!")

except Exception as error:

    print("Database rejected duplicate:")
    print(error)