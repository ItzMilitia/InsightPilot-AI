from backend.engines.analysis_engine import AnalysisEngine
from backend.engines.data_engine import DataEngine
from backend.engines.insight_engine import InsightEngine
from backend.engines.rule_engine import RuleEngine

from backend.services.report_builder import ReportBuilder

from backend.models.dataset_report import DatasetReport
from backend.models.recommendation_report import RecommendationReport

print("Loading dataset...")

data_engine = DataEngine()

df = data_engine.load_dataset(
    "datasets/banking/bank_customers.csv"
)

analysis = AnalysisEngine().analyze(df)

rules = RuleEngine().evaluate(
    dataframe=df,
    pack="banking",
)

insights = InsightEngine().analyze(
    analysis,
)

builder = ReportBuilder()

dataset = DatasetReport()

recommendations = RecommendationReport()

context = builder.build(
    dataset=dataset,
    analysis=analysis,
    rules=rules,
    insights=insights,
    recommendations=recommendations,
    dataset_name="bank_customers.csv",
)

print(context)

print()

print(context.to_dict())

print()

print("✓ ReportBuilder test passed.")