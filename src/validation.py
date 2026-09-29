import pandas as pd


def normalize_phone(phone):
    """
    Normalize Pakistani phone numbers.

    Example:
    03081234567 -> 03081234567
    3081234567  -> 03081234567
    """

    phone = str(phone).strip()

    # Remove decimal part if Pandas converted the value
    phone = phone.replace(".0", "")

    # Keep digits only
    phone = "".join(char for char in phone if char.isdigit())

    # Convert 10-digit Pakistani mobile number to 11-digit format
    if len(phone) == 10 and phone.startswith("3"):
        phone = "0" + phone

    return phone


def validate_data(df):
    """
    Validate and clean incoming customer data.
    """

    required_columns = [
        "customer_id",
        "name",
        "email",
        "phone",
        "city"
    ]

    # Check that all required columns exist
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    # Remove records with missing required values
    df = df.dropna(subset=required_columns).copy()

    # Convert fields to strings
    df["name"] = df["name"].astype(str).str.strip()
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    df["city"] = df["city"].astype(str).str.strip()

    # Normalize phone numbers
    df["phone"] = df["phone"].apply(normalize_phone)

    # Validate email format
    df = df[df["email"].str.contains("@", na=False)]

    return df