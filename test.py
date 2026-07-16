import pandas as pd

from backend.engines.visualization_engine import VisualizationEngine

df = pd.DataFrame(
    {
        "Age": [21, 22, 25, 30, None],
        "Salary": [25000, 27000, 31000, 45000, 50000],
        "Department": [
            "IT",
            "HR",
            "IT",
            "Finance",
            "HR",
        ],
    }
)

engine = VisualizationEngine()

report = engine.analyze(df)

print(report)

print(len(report.charts))

for chart in report.charts:
    print(chart.chart_type)

for chart in report.charts:
    print(chart.title)

print(report.charts[0].data)

for chart in report.charts:
    if chart.chart_type == "pie":
        print(chart.data)

for chart in report.charts:
    if chart.chart_type == "heatmap":
        print(chart.data)

for chart in report.charts:
    if chart.chart_type == "histogram":
        print(chart.title)
        print(chart.data)