from src.database import (
    reject_review,
    get_existing_customers,
    get_processed_customer_ids
)


review_id = 3

result = reject_review(review_id)

if result:
    print("Review rejected successfully!")
else:
    print("Rejection failed!")


print("\nCustomers:")

customers = get_existing_customers()

print(customers)


print("\nProcessed customer IDs:")

processed_ids = get_processed_customer_ids()

print(processed_ids)