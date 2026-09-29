
import logging

from src.ingestion import load_data
from src.validation import validate_data
from src.duplicate_detection import classify_records

from src.database import (
    insert_if_unique,
    get_existing_customers,
    log_duplicate,
    log_potential_duplicate,
    get_processed_customer_ids,
    mark_customer_processed
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_pipeline():

    # Step 1: Load existing data from PostgreSQL
    existing_data = get_existing_customers()

    # Load new incoming data
    new_data = load_data("data/new_data.csv")

    # Get already processed customer IDs
    processed_ids = get_processed_customer_ids()

    # Step 2: Validate new data
    validated_data = validate_data(new_data)

    # Step 3: Classify records
    classified_records = classify_records(
        validated_data,
        existing_data
    )

    # Step 4: Process classified records
    for record in classified_records:

        customer_id = int(record["customer_id"])

        # Skip records that have already been processed
        if customer_id in processed_ids:

            logger.info(
                f"SKIPPED: Customer {customer_id} already processed"
            )

            continue

        # Process UNIQUE records
        if record["status"] == "UNIQUE":

            inserted = insert_if_unique(record)

            if inserted:

                logger.info(
                    f"INSERTED: {record['name']}"
                )

                # Mark successfully inserted record as processed
                mark_customer_processed(customer_id)

            else:

                logger.info(
                    f"REJECTED BY DATABASE: {record['name']}"
                )

        # Process DUPLICATE records
        elif record["status"] == "DUPLICATE":

            log_duplicate(
                record,
                "DUPLICATE",
                record["duplicate_field"]
            )

            logger.info(
                f"DUPLICATE: {record['name']} | "
                f"Field: {record['duplicate_field']}"
            )

            # Mark duplicate record as processed
            mark_customer_processed(customer_id)

        # Process POTENTIAL_DUPLICATE records
        elif record["status"] == "POTENTIAL_DUPLICATE":

            log_potential_duplicate(record)

            logger.info(
                f"POTENTIAL DUPLICATE: {record['name']}"
            )

            # Do NOT mark as processed yet.
            # It is waiting for a review decision.


if __name__ == "__main__":

    run_pipeline()
