from src.validation import normalize_phone


test_numbers = [
    "03081234567",
    "3081234567",
    "0308-1234567",
    "0308 1234567"
]


for number in test_numbers:

    normalized = normalize_phone(number)

    print(f"{number} -> {normalized}")