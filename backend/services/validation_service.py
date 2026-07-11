from pathlib import Path

# Supported file formats
SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}

# Maximum upload size (200 MB)
MAX_FILE_SIZE = 200 * 1024 * 1024


def validate_file(uploaded_file):
    """
    Validate uploaded file.

    Returns:
        (bool, message)
    """

    if uploaded_file is None:
        return False, "No file uploaded."

    extension = Path(uploaded_file.name).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return False, (
            "Unsupported file format. "
            "Please upload a CSV or Excel (.xlsx) file."
        )

    if uploaded_file.size == 0:
        return False, "Uploaded file is empty."

    if uploaded_file.size > MAX_FILE_SIZE:
        return False, "File size exceeds the 200 MB limit."

    return True, "File validation successful."