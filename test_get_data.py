from src.database import get_existing_customers


existing_data = get_existing_customers()

print("\n========== EXISTING DATABASE DATA ==========")
print(existing_data)