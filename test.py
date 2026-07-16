import pandas as pd

from backend.engines.correlation_engine import CorrelationEngine

df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5],
        "B": [2, 4, 6, 8, 10],
        "C": [5, 4, 3, 2, 1],
    }
)

engine = CorrelationEngine()

report = engine.analyze(df)

print(report)