"""
Configuration values for the InsightPilot Quality Score Engine.

All weights should add up to 1.0 (100%).
"""

# ---------------------------------------------------------------------
# Quality Score Weights
# ---------------------------------------------------------------------

MISSING_VALUE_WEIGHT = 0.40
DUPLICATE_ROW_WEIGHT = 0.30
DUPLICATE_COLUMN_WEIGHT = 0.20
OUTLIER_WEIGHT = 0.10

# ---------------------------------------------------------------------
# Quality Grades
# ---------------------------------------------------------------------

EXCELLENT_SCORE = 90
GOOD_SCORE = 75
FAIR_SCORE = 60
POOR_SCORE = 0