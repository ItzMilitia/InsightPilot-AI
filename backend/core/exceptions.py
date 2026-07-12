class DataEngineError(Exception):
    """Base exception for data engine errors."""


class UnsupportedFileError(DataEngineError):
    """Raised when the uploaded file type is not supported."""


class DatasetReadError(DataEngineError):
    """Raised when a dataset cannot be loaded."""


class EncodingDetectionError(DataEngineError):
    """Raised when file encoding cannot be determined."""