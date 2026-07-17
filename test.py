import pandas as pd

from backend.engines.rule_engine import RuleEngine

df = pd.DataFrame(
    {
        "CustomerID": [1, 2, 2],
        "Balance": [1000, 2000, 2000],
    }
)

engine = RuleEngine()

report = engine.evaluate(
    dataframe=df,
    required_columns=[
        "CustomerID",
        "Balance",
        "Age",
    ],
)

print(report.overall_status)
print(report.total_rules)

for result in report.results:
    print(result)