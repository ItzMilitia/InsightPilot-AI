def get_dataset_metadata(df, uploaded_file):
    """
    Generate metadata for the uploaded dataset.
    """

    return {
        "Filename": uploaded_file.name,
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Memory Usage (MB)": round(
            df.memory_usage(deep=True).sum() / (1024 * 1024),
            2
        ),
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
    }