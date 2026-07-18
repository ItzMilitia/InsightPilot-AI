from backend.engines.data_engine import DataEngine
from backend.engines.analysis_engine import AnalysisEngine
from backend.engines.insight_engine import InsightEngine
from backend.models.insight_report import InsightReport

print("Loading dataset...")

data_engine = DataEngine()
analysis_engine = AnalysisEngine()
insight_engine = InsightEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

analysis_report = analysis_engine.analyze(df)

print("Running Insight Engine...")

report = insight_engine.analyze(
    analysis_report
)

assert isinstance(report, InsightReport)

print(report)

serialized = report.to_dict()

assert isinstance(serialized, dict)

print("\n✓ InsightEngine migration successful.")