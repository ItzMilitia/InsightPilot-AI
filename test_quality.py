from backend.engines.data_engine import DataEngine
from backend.engines.quality_engine import QualityEngine

data_engine = DataEngine()
quality_engine = QualityEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

report = quality_engine.analyze(df)

print("\nQuality Score")
print(report.quality_score)

print("\nQuality Grade")
print(report.quality_grade)