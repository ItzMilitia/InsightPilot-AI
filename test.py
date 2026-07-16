import pandas as pd

from backend.engines.analysis_engine import AnalysisEngine
from backend.engines.insight_engine import InsightEngine
from backend.engines.html_report_engine import HTMLReportEngine
from backend.engines.pdf_report_engine import PDFReportEngine

df = pd.DataFrame(
    {
        "Age": [21, 22, None, 24],
        "Salary": [25000, 27000, 29000, 31000],
        "Department": [
            "IT",
            "HR",
            "IT",
            "Finance",
        ],
    }
)

analysis = AnalysisEngine().analyze(df)

insights = InsightEngine().analyze(analysis)

html = HTMLReportEngine().generate(
    analysis,
    insights,
)

pdf = PDFReportEngine().generate(
    html,
    "reports/report.pdf",
)

print(pdf.file_path)