from __future__ import annotations

from backend.models.report_context import ReportContext
from backend.models.html_report import HTMLReport
from backend.config.settings import settings

class HTMLReportEngine:
    """
    Generates a professional HTML report from the analysis
    and insight reports.
    """

    def generate(
        self,
        report_context: ReportContext,
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

    {self._build_header(report_context)}

    {self._build_quality_section(report_context)}

    {self._build_insight_section(report_context)}

    {self._build_profile_section(report_context)}

    {self._build_correlation_section(report_context)}

    {self._build_visualization_section(report_context)}

    {self._build_recommendation_section(report_context)}

    {self._build_footer()}

    </div>

    </body>

    </html>
    """

        return HTMLReport(
            title=report_context.metadata.title,
            html=html,
        )

# ============================================================
# Header
# ============================================================

def _build_header(
    self,
    context: ReportContext,
) -> str:

    metadata = context.metadata
    dataset = context.dataset

    return f"""
<div class="section">

<h1>{metadata.title}</h1>

<h3>Enterprise Data Analysis Report</h3>

<table>

<tr>
<td><strong>Dataset</strong></td>
<td>{dataset.file.name}</td>
</tr>

<tr>
<td><strong>Rows</strong></td>
<td>{dataset.structure.total_rows:,}</td>
</tr>

<tr>
<td><strong>Columns</strong></td>
<td>{dataset.structure.total_columns:,}</td>
</tr>

<tr>
<td><strong>Format</strong></td>
<td>{dataset.file.file_format}</td>
</tr>

<tr>
<td><strong>Generated</strong></td>
<td>{metadata.generated_at.strftime("%d %B %Y %H:%M:%S")}</td>
</tr>

</table>

</div>
"""

# ============================================================
# Quality
# ============================================================

def _build_quality_section(
    self,
    context: ReportContext,
) -> str:

    quality = context.quality
    summary = quality.summary

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
<td>{summary.score:.2f}</td>
</tr>

<tr>
<td>Quality Grade</td>
<td>{summary.grade}</td>
</tr>

<tr>
<td>Total Issues</td>
<td>{summary.total_issues}</td>
</tr>

<tr>
<td>Critical Issues</td>
<td>{summary.critical_issues}</td>
</tr>

<tr>
<td>Warnings</td>
<td>{summary.warning_issues}</td>
</tr>

</table>

</div>
"""

    # ============================================================
# Insights
# ============================================================

def _build_insight_section(
    self,
    context: ReportContext,
) -> str:

    report = context.insights

    html = """
<div class="section">

<h2>AI Insights</h2>
"""

    if not report.insights:

        html += """
<p>No insights were generated.</p>
"""

    else:

        for insight in report.insights:

            html += f"""
<div class="card">

<h3>{insight.title}</h3>

<p>
<strong>Category:</strong>
{insight.category}
</p>

<p>
<strong>Severity:</strong>
{insight.severity}
</p>

<p>
{insight.description}
</p>
"""

            if getattr(insight, "recommendation", None):

                html += f"""
<p>

<strong>Recommendation:</strong>

{insight.recommendation}

</p>
"""

            html += """
</div>
"""

    html += """
</div>
"""

    return html

    # ============================================================
# Profiling
# ============================================================

def _build_profile_section(
    self,
    context: ReportContext,
) -> str:

    profiling = context.profiling
    summary = profiling.summary

    return f"""
<div class="section">

<h2>Profiling Summary</h2>

<table>

<tr>
<th>Metric</th>
<th>Value</th>
</tr>

<tr>
<td>Total Columns</td>
<td>{summary.total_columns}</td>
</tr>

<tr>
<td>Numeric Columns</td>
<td>{summary.numeric_columns}</td>
</tr>

<tr>
<td>Categorical Columns</td>
<td>{summary.categorical_columns}</td>
</tr>

<tr>
<td>Datetime Columns</td>
<td>{summary.datetime_columns}</td>
</tr>

<tr>
<td>Boolean Columns</td>
<td>{summary.boolean_columns}</td>
</tr>

<tr>
<td>Text Columns</td>
<td>{summary.text_columns}</td>
</tr>

</table>

</div>
"""

   # ============================================================
# Correlation
# ============================================================

def _build_correlation_section(
    self,
    context: ReportContext,
) -> str:

    correlation = context.correlation
    summary = correlation.summary

    return f"""
<div class="section">

<h2>Correlation Summary</h2>

<table>

<tr>
<th>Metric</th>
<th>Value</th>
</tr>

<tr>
<td>Method</td>
<td>{summary.method}</td>
</tr>

<tr>
<td>Threshold</td>
<td>{summary.threshold}</td>
</tr>

<tr>
<td>Numeric Columns</td>
<td>{summary.total_numeric_columns}</td>
</tr>

<tr>
<td>Strong Positive</td>
<td>{summary.strong_positive_count}</td>
</tr>

<tr>
<td>Strong Negative</td>
<td>{summary.strong_negative_count}</td>
</tr>

<tr>
<td>Highly Correlated Pairs</td>
<td>{len(correlation.highly_correlated_pairs)}</td>
</tr>

</table>

</div>
"""

    # ============================================================
# Visualization
# ============================================================

def _build_visualization_section(
    self,
    context: ReportContext,
) -> str:

    visualization = context.visualization

    html = """
<div class="section">

<h2>Visualization Summary</h2>
"""

    if not visualization.categories:

        html += """
<p>No visualizations generated.</p>
"""

    else:

        for category in visualization.categories:

            html += f"""
<h3>{category.title}</h3>

<ul>
"""

            for chart in category.charts:

                html += f"""
<li>

<strong>{chart.title}</strong>

({chart.chart_type})

"""

                if chart.description:

                    html += f"""
<br>

<small>{chart.description}</small>
"""

                html += """
</li>
"""

            html += """
</ul>
"""

    html += """
</div>
"""

    return html

    # ============================================================
# Recommendations
# ============================================================

def _build_recommendation_section(
    self,
    context: ReportContext,
) -> str:

    report = context.recommendations

    recommendations = getattr(
        report,
        "recommendations",
        [],
    )

    html = """
<div class="section">

<h2>Recommendations</h2>

<ul>
"""

    if not recommendations:

        html += """
<li>No recommendations generated.</li>
"""

    else:

        for recommendation in recommendations:

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

Generated by <strong>InsightPilot AI</strong>

</p>

</div>
"""