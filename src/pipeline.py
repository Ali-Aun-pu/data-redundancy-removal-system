
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

    # Pipeline counters
    total_records = 0
    unique_inserted = 0
    duplicates_found = 0
    potential_duplicates = 0
    skipped_records = 0
    rejected_by_database = 0
    errors = 0

    # Step 1: Load existing data from PostgreSQL
    existing_data = get_existing_customers()

    # Load new incoming data
    new_data = load_data("data/new_data.csv")

    total_records = len(new_data)

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

        try:

            customer_id = int(record["customer_id"])

            # Skip records that have already been processed
            if customer_id in processed_ids:

                skipped_records += 1

                logger.info(
                    f"SKIPPED: Customer {customer_id} already processed"
                )

                continue

            # Process UNIQUE records
            if record["status"] == "UNIQUE":

                inserted = insert_if_unique(record)

                if inserted:

                    unique_inserted += 1

                    logger.info(
                        f"INSERTED: {record['name']}"
                    )

                    mark_customer_processed(customer_id)

                else:

                    rejected_by_database += 1

                    logger.info(
                        f"REJECTED BY DATABASE: {record['name']}"
                    )

            # Process DUPLICATE records
            elif record["status"] == "DUPLICATE":

                duplicates_found += 1

                log_duplicate(
                    record,
                    "DUPLICATE",
                    record["duplicate_field"]
                )

                logger.info(
                    f"DUPLICATE: {record['name']} | "
                    f"Field: {record['duplicate_field']}"
                )

                mark_customer_processed(customer_id)

            # Process POTENTIAL_DUPLICATE records
            elif record["status"] == "POTENTIAL_DUPLICATE":

                logged = log_potential_duplicate(record)

                if logged:

                    potential_duplicates += 1

                    logger.info(
                        f"POTENTIAL DUPLICATE: {record['name']}"
                    )

                else:

                    logger.info(
                        f"ALREADY IN REVIEW QUEUE: {record['name']}"
                    )

                # Do NOT mark as processed yet.
                # It is waiting for a review decision.

        except Exception as e:

            errors += 1

            logger.error(
                f"ERROR processing customer "
                f"{record.get('customer_id')}: {e}"
            )

    # Pipeline summary
    logger.info("")
    logger.info("========== PIPELINE SUMMARY ==========")
    logger.info(f"Records loaded:         {total_records}")
    logger.info(f"Unique inserted:        {unique_inserted}")
    logger.info(f"Duplicates found:       {duplicates_found}")
    logger.info(f"Potential duplicates:   {potential_duplicates}")
    logger.info(f"Skipped records:        {skipped_records}")
    logger.info(f"Rejected by database:   {rejected_by_database}")
    logger.info(f"Errors:                 {errors}")
    logger.info("======================================")
    logger.info("")


if __name__ == "__main__":

    run_pipeline()

