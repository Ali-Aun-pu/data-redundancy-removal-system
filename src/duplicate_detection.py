from rapidfuzz.fuzz import ratio


def calculate_name_similarity(name1, name2):
    """
    Calculate similarity between two names.
    Returns a score from 0 to 100.
    """

    return ratio(
        name1.lower().strip(),
        name2.lower().strip()
    )


def classify_records(new_data, existing_data):
    """
    Classify incoming records as:
    UNIQUE, DUPLICATE, or POTENTIAL_DUPLICATE.
    """

    existing_customer_ids = set(
        existing_data["customer_id"]
    )

    existing_emails = set(
        existing_data["email"]
    )

    existing_phones = set(
        existing_data["phone"]
    )

    results = []

    for _, new_record in new_data.iterrows():

        customer_id = int(new_record["customer_id"])
        email = new_record["email"]
        phone = new_record["phone"]
        name = new_record["name"]

        duplicate_field = None

        # Check customer ID
        if customer_id in existing_customer_ids:
            duplicate_field = "CUSTOMER_ID"

        # Check email
        elif email in existing_emails:
            duplicate_field = "EMAIL"

        # Check phone
        elif phone in existing_phones:
            duplicate_field = "PHONE"

        # Exact duplicate found
        if duplicate_field:

            status = "DUPLICATE"
            similarity_score = None

        else:

            highest_similarity = 0

            # Check name similarity
            for _, existing_record in existing_data.iterrows():

                similarity = calculate_name_similarity(
                    name,
                    existing_record["name"]
                )

                if similarity > highest_similarity:
                    highest_similarity = similarity

            if highest_similarity >= 85:

                status = "POTENTIAL_DUPLICATE"

                similarity_score = highest_similarity

            else:

                status = "UNIQUE"

                similarity_score = highest_similarity

        record = new_record.copy()

        record["status"] = status
        record["similarity_score"] = similarity_score
        record["duplicate_field"] = duplicate_field

        results.append(record)

        existing_customer_ids.add(customer_id)
        existing_emails.add(email)
        existing_phones.add(phone)

    return results