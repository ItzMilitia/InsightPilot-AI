from backend.engines.data_engine import DataEngine
from backend.engines.profiling_engine import ProfilingEngine
from backend.models.profiling_report import ProfilingReport

data_engine = DataEngine()
profiling_engine = ProfilingEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

report = profiling_engine.analyze(df)

assert isinstance(report, ProfilingReport)

print(report)

serialized = report.to_dict()

assert isinstance(serialized, dict)

print("\n✓ ProfilingEngine migration successful.")