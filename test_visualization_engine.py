from backend.engines.data_engine import DataEngine
from backend.engines.visualization_engine import VisualizationEngine
from backend.models.visualization_report import VisualizationReport

print("Loading dataset...")

data_engine = DataEngine()
visualization_engine = VisualizationEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

print("Running Visualization Engine...")

report = visualization_engine.analyze(df)

assert isinstance(report, VisualizationReport)

print(report)

serialized = report.to_dict()

assert isinstance(serialized, dict)

print("\n✓ VisualizationEngine migration successful.")