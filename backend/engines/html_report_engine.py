from __future__ import annotations

from datetime import datetime

from backend.models.analysis_report import AnalysisReport
from backend.models.html_report import HTMLReport
from backend.models.insight_report import InsightReport
from backend.config.settings import settings

class HTMLReportEngine:
    """
    Generates a professional HTML report from the analysis
    and insight reports.
    """

    def generate(
        self,
        analysis_report: AnalysisReport,
        insight_report: InsightReport,
    ) -> HTMLReport:

        html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<title>{settings.report_title}</title>

<style>

body {{
    font-family: Arial, Helvetica, sans-serif;
    background: #f4f6f8;
    margin: 40px;
    color: #222;
}}

.container {{
    max-width: 1200px;
    margin: auto;
}}

h1 {{
    color: #0f62fe;
}}

.section {{
    background: white;
    margin-top: 20px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0,0,0,.08);
}}

table {{
    width:100%;
    border-collapse: collapse;
}}

th, td {{
    border:1px solid #ddd;
    padding:8px;
}}

th {{
    background:#f0f0f0;
}}

.card {{
    border-left:5px solid #0f62fe;
    padding:15px;
    margin-bottom:12px;
    background:#fafafa;
}}

.footer {{
    margin-top:40px;
    text-align:center;
    color:#777;
}}

</style>

</head>

<body>

<div class="container">

{self._build_header()}

{self._build_quality_section(analysis_report)}

{self._build_insight_section(insight_report)}

{self._build_profile_section(analysis_report)}

{self._build_correlation_section(analysis_report)}

{self._build_visualization_section(analysis_report)}

{self._build_recommendation_section(analysis_report)}

{self._build_footer()}

</div>

</body>

</html>
"""

        return HTMLReport(
            title=settings.report_title,
            html=html,
        )

    # ============================================================
    # Header
    # ============================================================

    def _build_header(self) -> str:

        return f"""
<div class="section">

<h1>{settings.report_title}</h1>

<h3>Enterprise Data Analysis Report</h3>

<p>
Generated:
{datetime.now().strftime("%d %B %Y %H:%M:%S")}
</p>

</div>
"""

    # ============================================================
    # Quality
    # ============================================================

    def _build_quality_section(
        self,
        report: AnalysisReport,
    ) -> str:

        q = report.quality

        return f"""
<div class="section">

<h2>Dataset Quality</h2>

<table>

<tr>
<th>Metric</th>
<th>Value</th>
</tr>

<tr>
<td>Quality Score</td>
<td>{q.quality_score}</td>
</tr>

<tr>
<td>Quality Grade</td>
<td>{q.quality_grade}</td>
</tr>

<tr>
<td>Missing Values</td>
<td>{q.missing_values}</td>
</tr>

<tr>
<td>Duplicate Rows</td>
<td>{q.duplicate_rows}</td>
</tr>

<tr>
<td>Duplicate Columns</td>
<td>{q.duplicate_columns}</td>
</tr>

</table>

</div>
"""

    # ============================================================
    # Insights
    # ============================================================

    def _build_insight_section(
        self,
        report: InsightReport,
    ) -> str:

        html = """
<div class="section">

<h2>AI Insights</h2>
"""

        for insight in report.insights:

            html += f"""
<div class="card">

<h3>{insight.title}</h3>

<p><strong>Category:</strong> {insight.category}</p>

<p><strong>Severity:</strong> {insight.severity}</p>

<p>{insight.description}</p>

<p>
<strong>Recommendation:</strong>
{insight.recommendation}
</p>

</div>
"""

        html += "</div>"

        return html

    # ============================================================
    # Profiling
    # ============================================================

    def _build_profile_section(
        self,
        report: AnalysisReport,
    ) -> str:

        profiling = report.profiling

        return f"""
<div class="section">

<h2>Profiling Summary</h2>

<ul>

<li>
Numeric Columns:
{len(profiling.numeric_profiles)}
</li>

<li>
Categorical Columns:
{len(profiling.categorical_profiles)}
</li>

<li>
Datetime Columns:
{len(profiling.datetime_profiles)}
</li>

</ul>

</div>
"""

    # ============================================================
    # Correlation
    # ============================================================

    def _build_correlation_section(
        self,
        report: AnalysisReport,
    ) -> str:

        correlation = report.correlation

        return f"""
<div class="section">

<h2>Correlation Summary</h2>

<p>
Method:
{correlation.method}
</p>

<p>
Strong Positive:
{len(correlation.strong_positive)}
</p>

<p>
Strong Negative:
{len(correlation.strong_negative)}
</p>

</div>
"""

    # ============================================================
    # Visualization
    # ============================================================

    def _build_visualization_section(
        self,
        report: AnalysisReport,
    ) -> str:

        html = """
<div class="section">

<h2>Visualization Summary</h2>

<ul>
"""

        for chart in report.visualization.charts:

            html += f"""
<li>
{chart.title}
({chart.chart_type})
</li>
"""

        html += """
</ul>

</div>
"""

        return html

    # ============================================================
    # Recommendations
    # ============================================================

    def _build_recommendation_section(
        self,
        report: AnalysisReport,
    ) -> str:

        html = """
<div class="section">

<h2>Recommendations</h2>

<ul>
"""

        for recommendation in report.quality.recommendations:

            html += f"""
<li>{recommendation}</li>
"""

        html += """
</ul>

</div>
"""

        return html

    # ============================================================
    # Footer
    # ============================================================

    def _build_footer(self) -> str:

        return """
<div class="footer">

<hr>

<p>
Generated by InsightPilot AI
</p>

</div>
"""