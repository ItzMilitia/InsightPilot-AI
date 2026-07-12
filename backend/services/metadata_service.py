from __future__ import annotations

import pandas as pd


def get_dataset_metadata(
    df: pd.DataFrame,
    file_name: str | None = None,
) -> dict:
    """
    Generate metadata for the uploaded dataset.
    """

    metadata = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Memory Usage (MB)": round(
            df.memory_usage(deep=True).sum() / (1024 * 1024),
            2,
        ),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
    }

    if file_name:
        metadata["Filename"] = file_name

    return metadata