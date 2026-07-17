"""
Application Settings.

Provides strongly-typed access to application configuration.
"""

from dataclasses import dataclass

from backend.config import default_config


# ==========================================================
# Rule Engine Settings
# ==========================================================

@dataclass(frozen=True)
class RuleEngineSettings:
    """
    Configuration for the Rule Engine.
    """

    enabled: bool
    default_rule_pack: str
    stop_on_first_failure: bool
    default_severity: str

    minimum_rows: int
    max_duplicate_rows: int

    banking_required_columns: list[str]
    enable_banking_validations: bool


# ==========================================================
# Global Settings
# ==========================================================

class Settings:
    """
    Global application settings.
    """

    def __init__(self) -> None:
        # --------------------------------------------------
        # Existing configuration
        # --------------------------------------------------

        self.correlation_threshold = (
            default_config.CORRELATION_THRESHOLD
        )

        self.default_correlation_method = (
            default_config.DEFAULT_CORRELATION_METHOD
        )

        self.generate_heatmap = (
            default_config.GENERATE_HEATMAP
        )

        self.generate_histograms = (
            default_config.GENERATE_HISTOGRAMS
        )

        self.generate_boxplots = (
            default_config.GENERATE_BOXPLOTS
        )

        self.report_title = (
            default_config.REPORT_TITLE
        )

        self.report_author = (
            default_config.REPORT_AUTHOR
        )

        self.quality_warning_threshold = (
            default_config.QUALITY_WARNING_THRESHOLD
        )

        self.max_categorical_unique = (
            default_config.MAX_CATEGORICAL_UNIQUE
        )

        # --------------------------------------------------
        # Rule Engine
        # --------------------------------------------------

        self.rule_engine = RuleEngineSettings(
            enabled=default_config.RULE_ENGINE_ENABLED,
            default_rule_pack=default_config.DEFAULT_RULE_PACK,
            stop_on_first_failure=default_config.STOP_ON_FIRST_FAILURE,
            default_severity=default_config.DEFAULT_RULE_SEVERITY,
            minimum_rows=default_config.MINIMUM_ROWS,
            max_duplicate_rows=default_config.MAX_DUPLICATE_ROWS,
            banking_required_columns=list(
                default_config.BANKING_REQUIRED_COLUMNS
            ),
            enable_banking_validations=(
                default_config.ENABLE_BANKING_VALIDATIONS
            ),
        )


# Singleton instance
settings = Settings()