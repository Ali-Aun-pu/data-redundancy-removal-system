from src.database import (
    get_processed_customer_ids,
    mark_customer_processed
)


customer_id = 15

mark_customer_processed(customer_id)

processed_ids = get_processed_customer_ids()

print("Processed customer IDs:")
print(processed_ids)