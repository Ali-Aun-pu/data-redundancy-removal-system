from src.database import (
    approve_review,
    get_existing_customers,
    get_processed_customer_ids
)


review_id = 7

result = approve_review(review_id)

if result:
    print("Review approved and customer inserted!")
else:
    print("Approval failed!")


print("\nCustomers:")

customers = get_existing_customers()

print(customers)


print("\nProcessed customer IDs:")

processed_ids = get_processed_customer_ids()

print(processed_ids)