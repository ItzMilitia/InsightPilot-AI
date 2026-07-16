import pandas as pd

from backend.engines.analysis_engine import AnalysisEngine

df = pd.DataFrame(
    {
        "Age": [21, 22, 23, 24],
        "Salary": [25000, 27000, 29000, 31000],
        "Department": ["IT", "HR", "IT", "Finance"],
    }
)

engine = AnalysisEngine()

report = engine.analyze(df)

print(type(report.quality).__name__)
print(type(report.profiling).__name__)
print(type(report.correlation).__name__)
print(type(report.visualization).__name__)