from backend.engines.data_engine import DataEngine
from backend.engines.quality_engine import QualityEngine

data_engine = DataEngine()
quality_engine = QualityEngine()

df = data_engine.load_dataset("datasets/banking/bank_customers.csv")

# Temporary test
df.loc[0, "Email"] = None
df.loc[3, "Email"] = None
df.loc[5, "CustomerName"] = None

report = quality_engine.analyze(df)

print(report.missing_values)
print(report.missing_value_summary)