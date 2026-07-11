import pandas as pd
from pathlib import Path


def load_dataset(uploaded_file):
    """
    Load CSV or Excel file into a DataFrame.
    """

    extension = Path(uploaded_file.name).suffix.lower()

    if extension == ".csv":
        return pd.read_csv(uploaded_file)

    if extension == ".xlsx":
        return pd.read_excel(uploaded_file)

    raise ValueError("Unsupported file format.")