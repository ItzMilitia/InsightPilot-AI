from backend.engines.analysis_engine import AnalysisEngine
from backend.engines.data_engine import DataEngine
from backend.models.analysis_report import AnalysisReport

print("Loading dataset...")

data_engine = DataEngine()
analysis_engine = AnalysisEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

print("Running Analysis Engine...")

report = analysis_engine.analyze(df)

assert isinstance(report, AnalysisReport)

serialized = report.to_dict()

assert isinstance(serialized, dict)

print(report)

print("\n✓ AnalysisEngine migration successful.")