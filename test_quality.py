from backend.engines.data_engine import DataEngine
from backend.engines.quality_engine import QualityEngine

data_engine = DataEngine()
quality_engine = QualityEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

report = quality_engine.analyze(df)

print()

print("Quality Score")
print(report.quality_score)

print()

print("Quality Grade")
print(report.quality_grade)

print()

print("Recommendations")

for recommendation in report.recommendations:
    print("-", recommendation)