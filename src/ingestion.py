import pandas as pd


def load_data(file_path):
    """
    Load a CSV file into a Pandas DataFrame.
    """
    df = pd.read_csv(file_path)

    print(f"Loaded {len(df)} records from {file_path}")

    return df