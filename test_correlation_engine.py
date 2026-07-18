from backend.engines.data_engine import DataEngine
from backend.engines.correlation_engine import CorrelationEngine
from backend.models.correlation_report import CorrelationReport

print("Loading dataset...")

data_engine = DataEngine()
correlation_engine = CorrelationEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

print("Running Correlation Engine...")

report = correlation_engine.analyze(df)

assert isinstance(report, CorrelationReport)

print(report)

serialized = report.to_dict()

assert isinstance(serialized, dict)

print("\n✓ CorrelationEngine migration successful.")