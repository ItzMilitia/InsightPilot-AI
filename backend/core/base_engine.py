from __future__ import annotations

import time
from abc import ABC

from backend.utils.logger import logger


class BaseEngine(ABC):
    """
    Base class for all InsightPilot engines.

    Provides:
    - Logging
    - Execution timing
    - Shared utilities
    """

    def __init__(self) -> None:
        self.logger = logger

    def log_start(self, operation: str) -> float:
        """
        Log the start of an operation.

        Returns:
            Start time for execution measurement.
        """
        self.logger.info("Starting %s...", operation)
        return time.perf_counter()

    def log_finish(self, operation: str, start_time: float) -> None:
        """
        Log successful completion.
        """
        elapsed = time.perf_counter() - start_time

        self.logger.info(
            "%s completed in %.3f seconds.",
            operation,
            elapsed,
        )

    def log_error(self, operation: str, exception: Exception) -> None:
        """
        Log an exception.
        """
        self.logger.exception(
            "%s failed: %s",
            operation,
            exception,
        )