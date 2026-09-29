from src.database import log_potential_duplicate


customer = {
    "customer_id": 11,
    "name": "Ali Ahmad",
    "email": "ali.ahmad@gmail.com",
    "phone": "03081234567",
    "similarity_score": 90.91
}


log_potential_duplicate(customer)

print("Potential duplicate added to review queue!")