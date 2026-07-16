from __future__ import annotations

from backend.config import default_config


class Settings:
    """
    Central configuration object used throughout the application.
    """

    def __init__(self) -> None:

        # Correlation

        self.correlation_threshold = (
            default_config.CORRELATION_THRESHOLD
        )

        self.default_correlation_method = (
            default_config.DEFAULT_CORRELATION_METHOD
        )

        # Visualization

        self.generate_heatmap = (
            default_config.GENERATE_HEATMAP
        )

        self.generate_histograms = (
            default_config.GENERATE_HISTOGRAMS
        )

        self.generate_boxplots = (
            default_config.GENERATE_BOXPLOTS
        )

        # Reports

        self.report_title = (
            default_config.REPORT_TITLE
        )

        self.report_author = (
            default_config.REPORT_AUTHOR
        )

        # Quality

        self.quality_warning_threshold = (
            default_config.QUALITY_WARNING_THRESHOLD
        )

        # Profiling

        self.max_categorical_unique = (
            default_config.MAX_CATEGORICAL_UNIQUE
        )


settings = Settings()