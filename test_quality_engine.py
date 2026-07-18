from backend.engines.data_engine import DataEngine
from backend.engines.quality_engine import QualityEngine
from backend.reports.report_builder import ReportBuilder

data_engine = DataEngine()
quality_engine = QualityEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

report = quality_engine.analyze(df)

print(report)

builder = ReportBuilder()

context = builder.build(
    quality=report,
)

print("\n===== REPORT BUILDER TEST =====")
print(type(context))
print(type(context.quality))

assert context.quality is report

print("✓ ReportBuilder Integration Passed")