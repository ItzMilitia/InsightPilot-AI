"""
Default configuration values for InsightPilot AI.
"""

# ============================================================
# Correlation
# ============================================================

CORRELATION_THRESHOLD = 0.80

DEFAULT_CORRELATION_METHOD = "pearson"

# ============================================================
# Visualization
# ============================================================

GENERATE_HEATMAP = True

GENERATE_HISTOGRAMS = True

GENERATE_BOXPLOTS = True

# ============================================================
# Reports
# ============================================================

REPORT_TITLE = "InsightPilot AI Report"

REPORT_AUTHOR = "InsightPilot AI"

# ============================================================
# Data Quality
# ============================================================

QUALITY_WARNING_THRESHOLD = 80.0

# ============================================================
# Profiling
# ============================================================

MAX_CATEGORICAL_UNIQUE = 100

# ==========================================================
# RULE ENGINE
# ==========================================================

# Enable or disable the Rule Engine.
RULE_ENGINE_ENABLED = True

# Default rule pack used by RuleEngine.
#
# Supported values:
# - "generic"
# - "banking"
#
DEFAULT_RULE_PACK = "generic"

# Stop rule execution immediately after the first
# failed rule.
STOP_ON_FIRST_FAILURE = False

# Default severity assigned to rules unless overridden.
DEFAULT_RULE_SEVERITY = "warning"

# ==========================================================
# GENERIC RULE PACK
# ==========================================================

# Minimum number of rows expected in a dataset.
MINIMUM_ROWS = 10

# Maximum allowed duplicate rows.
MAX_DUPLICATE_ROWS = 0

# ==========================================================
# BANKING RULE PACK
# ==========================================================

# Default required columns for banking datasets.
BANKING_REQUIRED_COLUMNS = [
    "CustomerID",
    "AccountNumber",
    "Balance",
    "TransactionDate",
    "BranchCode",
]

# Enable additional banking-specific validation rules.
ENABLE_BANKING_VALIDATIONS = True