import streamlit as st
from pathlib import Path

from backend.engines.data_engine import DataEngine
from backend.engines.quality_engine import QualityEngine

from backend.managers.session_manager import SessionManager

from backend.services.metadata_service import (
    get_dataset_metadata,
)
from backend.services.report_pipeline import ReportPipeline
from backend.services.validation_service import (
    validate_file,
)

# ======================================================
# Streamlit Configuration
# ======================================================

st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide",
)

st.title("📊 InsightPilot AI")
st.subheader(
    "Enterprise Decision Intelligence Platform"
)

# ======================================================
# Dataset Upload
# ======================================================

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file is not None:

    is_valid, message = validate_file(
        uploaded_file
    )

    if not is_valid:

        st.error(message)

    else:

        try:

            engine = DataEngine()

            df = engine.load_dataset(
                uploaded_file
            )

            SessionManager.save_dataset(
                df,
                uploaded_file.name,
            )

            st.success(
                "✅ Dataset uploaded successfully!"
            )

        except Exception as exc:

            st.error(str(exc))

# ======================================================
# Dataset View
# ======================================================

if SessionManager.has_dataset():

    df = SessionManager.get_dataset()

    pipeline = ReportPipeline()

    explorer = pipeline.explorer_service

    st.divider()

    # --------------------------------------------------
    # Dataset Preview
    # --------------------------------------------------

    st.subheader("📋 Dataset Preview")

    st.caption(
        "General information about the uploaded banking dataset."
    )

    st.dataframe(
        df.head(),
        width="stretch",
    )

    # --------------------------------------------------
    # Dataset Metadata
    # --------------------------------------------------

    st.divider()

    st.subheader("📊 Dataset Metadata")

    metadata = get_dataset_metadata(
        df,
        SessionManager.get_file_name(),
    )

    st.json(metadata)

    # --------------------------------------------------
    # Data Quality Report
    # --------------------------------------------------

    st.divider()

    st.subheader("🛡️ Data Quality Report")

    st.caption(
        "Automatically generated using the "
        "InsightPilot Quality Engine."
    )

    quality_engine = QualityEngine()

    report = quality_engine.analyze(df)

    col1, col2 = st.columns([2, 1])

    with col1:

        st.metric(
            "Quality Score",
            f"{report.summary.score:.2f}/100",
        )

        st.progress(
            report.summary.score / 100
        )

    with col2:

        if report.summary.grade == "Excellent":

            st.success(report.summary.grade)

        elif report.summary.grade == "Good":

            st.info(report.summary.grade)

        elif report.summary.grade == "Fair":

            st.warning(report.summary.grade)

        else:

            st.error(report.summary.grade)

    st.divider()

    metric1, metric2 = st.columns(2)

    metric3, metric4 = st.columns(2)

    metric1.metric(
        "Missing Values",
        report.missing.total_missing,
    )

    metric2.metric(
        "Duplicate Rows",
        report.duplicates.duplicate_rows,
    )

    metric3.metric(
        "Duplicate Columns",
        report.duplicates.duplicate_columns,
    )

    metric4.metric(
        "Outlier Columns",
        len(report.outliers.columns),
    )

    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------

    st.divider()

    with st.expander(
        "📌 Missing Value Analysis",
        expanded=False,
    ):

        if report.missing.columns:

            st.dataframe(
                report.missing.columns,
                width="stretch",
            )

        else:

            st.success(
                "No missing values detected."
            )

    # --------------------------------------------------
    # Outliers
    # --------------------------------------------------

    st.divider()

    with st.expander(
        "📈 Outlier Analysis",
        expanded=False,
    ):

        if report.outliers.columns:

            st.json(
                report.outliers.columns
            )

        else:

            st.success(
                "No outliers detected."
            )

    # --------------------------------------------------
    # Data Types
    # --------------------------------------------------

    st.divider()

    with st.expander(
        "🧾 Data Type Analysis",
        expanded=False,
    ):

        st.dataframe(
            report.data_types.summary,
            width="stretch",
        )

    # --------------------------------------------------
    # Recommendations
    # --------------------------------------------------

    st.divider()

    st.subheader("💡 Recommendations")

    st.caption(
        "Actionable recommendations based on "
        "the detected data quality issues."
    )

    if report.recommendations:

        for recommendation in report.recommendations:

            st.info(recommendation)

    else:

        st.success(
            "No recommendations. Dataset looks clean."
        )

        # ======================================================
    # Enterprise Report Generation
    # ======================================================

    st.divider()

    st.subheader("📄 Enterprise Report Generation")

    st.caption(
        "Generate a complete enterprise report package "
        "using the InsightPilot Report Pipeline."
    )

    generate_pdf = st.checkbox(
        "Generate PDF Report",
        value=True,
    )

    generate_json = st.checkbox(
        "Generate JSON Report",
        value=True,
    )

    persist_reports = st.checkbox(
        "Persist Reports",
        value=True,
    )

    if st.button(
        "🚀 Generate Enterprise Report",
        type="primary",
    ):

        try:

            with st.spinner(
                "Generating enterprise report..."
            ):

                package = pipeline.run(
                    dataframe=df,
                    file_name=SessionManager.get_file_name(),
                    generate_pdf=generate_pdf,
                    generate_json=generate_json,
                    persist_reports=persist_reports,
                    return_package=True,
                )

            st.success(
                "✅ Enterprise report generated successfully!"
            )

            metadata = package.metadata

            st.divider()

            st.subheader("📋 Report Metadata")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Report ID",
                    metadata.report_id,
                )

                st.metric(
                    "Dataset",
                    metadata.dataset_name,
                )

            with col2:

                st.metric(
                    "Version",
                    metadata.version,
                )

                st.metric(
                    "Generated At",
                    str(metadata.generated_at),
                )

            # --------------------------------------------------
            # Generated Package
            # --------------------------------------------------

            st.divider()

            st.subheader("📦 Generated Report Package")

            formats = package.available_formats()

            if formats:

                st.write("**Available Formats**")

                for report_format in formats:

                    st.success(
                        report_format.upper()
                    )

            else:

                st.warning(
                    "No report formats were generated."
                )

            # --------------------------------------------------
            # Generated Artifacts
            # --------------------------------------------------

            st.divider()

            st.subheader("📁 Generated Artifacts")

            if package.artifacts:

                for name, path in package.artifacts.items():

                    artifact_path = Path(path)

                    st.text_input(
                        label=name.replace(
                            "_",
                            " ",
                        ).title(),
                        value=str(artifact_path),
                        disabled=True,
                    )

                    if (
                        artifact_path.exists()
                        and artifact_path.is_file()
                    ):

                        with open(
                            artifact_path,
                            "rb",
                        ) as file:

                            st.download_button(
                                label=(
                                    f"⬇ Download "
                                    f"{name.replace('_', ' ').title()}"
                                ),
                                data=file.read(),
                                file_name=artifact_path.name,
                                key=f"download_{name}",
                            )

                    elif artifact_path.exists():

                        st.info(
                            "Directory artifact "
                            "(not downloadable)."
                        )

                    else:

                        st.warning(
                            "Artifact not found."
                        )

            else:

                st.info(
                    "No persisted artifacts available."
                )

            # --------------------------------------------------
            # Report Summary
            # --------------------------------------------------

            st.divider()

            st.subheader("📊 Report Summary")

            st.info(
                f"""
            Report **{metadata.title}** was generated successfully.

            Dataset: **{metadata.dataset_name}**

            Version: **{metadata.version}**

            Generated Formats: **{", ".join(formats) if formats else "None"}**
            """ 
            )

        except Exception as exc:

            st.exception(exc)

    # ======================================================
    # Report Explorer
    # ======================================================

    st.divider()

    st.subheader("📚 Report Explorer")
    st.subheader("🔍 Compare Reports")

    st.caption(
        "Showing the 5 most recently generated reports."
    )

    try:

        reports = explorer.sort_reports(
            explorer.list_reports()
        )

        MAX_RECENT_REPORTS = 5

        reports = reports[:MAX_RECENT_REPORTS]

        if reports:

            rows = []

            for report in reports:

                rows.append(
                    {
                        "Report ID": report.metadata.report_id,
                        "Dataset": report.metadata.dataset_name,
                        "Version": report.metadata.version,
                        "Generated": report.metadata.generated_at,
                    }
                )

            st.dataframe(
                rows,
                width="stretch",
            )

            st.caption(
                f"Displaying {len(rows)} recent report(s)."
            )

            # ----------------------------------------------
            # Dataset Filter
            # ----------------------------------------------

            datasets = explorer.datasets()

            if datasets:

                selected_dataset = st.selectbox(
                    "Filter by Dataset",
                    ["All"] + datasets,
                )

                if selected_dataset != "All":

                    filtered = (
                        explorer.filter_by_dataset(
                            selected_dataset,
                        )
                    )

                    st.write(
                        f"Found {len(filtered)} report(s)."
                    )

                    st.dataframe(
                        [
                            {
                                "Report ID": r.metadata.report_id,
                                "Version": r.metadata.version,
                                "Generated": r.metadata.generated_at,
                            }
                            for r in filtered
                        ],
                        width="stretch",
                    )

            # ----------------------------------------------
            # Search
            # ----------------------------------------------

            search = st.text_input(
                "Search Reports",
            )

            if search:

                results = explorer.search(search)

                st.write(
                    f"{len(results)} result(s)"
                )

                st.dataframe(
                    [
                        {
                            "Report ID": r.metadata.report_id,
                            "Dataset": r.metadata.dataset_name,
                            "Version": r.metadata.version,
                        }
                        for r in results
                    ],
                    width="stretch",
                )

            # ----------------------------------------------
            # Selected Report
            # ----------------------------------------------

            selected_report = st.selectbox(
                "Select a Report",
                reports,
                format_func=lambda report: (
                    f"{report.metadata.dataset_name} | "
                    f"{report.metadata.version} | "
                    f"{report.metadata.report_id[:8]}"
                )
            )

            loaded_report = explorer.load_report(
                selected_report.metadata.report_id
            )

            package = loaded_report.package

            report_context = loaded_report.context

            # ReportContext is available for:
            # - Report Comparison
            # - Insight Drill-down
            # - Future Analytics

            st.divider()

            st.subheader("📄 Selected Report")

            left, right = st.columns(2)

            with left:

                st.metric(
                    "Dataset",
                    selected_report.metadata.dataset_name,
                )

                st.metric(
                    "Version",
                    selected_report.metadata.version,
                )

            with right:

                st.metric(
                    "Report ID",
                    selected_report.metadata.report_id,
                )

                st.metric(
                    "Generated",
                    str(selected_report.metadata.generated_at),
                )

            formats = package.available_formats()

            if formats:

                st.divider()

                st.subheader("📦 Available Formats")

                for report_format in formats:

                    st.success(
                        report_format.upper()
                    )

            baseline_report = st.selectbox(
                "Baseline Report",
                reports,
                format_func=lambda report: (
                    f"{report.metadata.dataset_name} | "
                    f"{report.metadata.version} | "
                    f"{report.metadata.report_id[:8]}"
                ),
                key="baseline_report",
            )

            comparison_report = st.selectbox(
                "Comparison Report",
                reports,
                format_func=lambda report: (
                    f"{report.metadata.dataset_name} | "
                    f"{report.metadata.version} | "
                    f"{report.metadata.report_id[:8]}"
                ),
                key="comparison_report",
            )

            if st.button("Compare Reports"):

                comparison = explorer.compare_reports(
                    baseline_report.metadata.report_id,
                    comparison_report.metadata.report_id,
                )

                st.divider()

                st.subheader("📊 Report Comparison")

                # ------------------------------------------
                # KPI Summary
                # ------------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Quality Score",
                        f"{comparison.quality_score_after:.2f}",
                        delta=f"{comparison.quality_score_delta:+.2f}",
                    )

                with col2:
                    st.metric(
                        "Missing Values",
                        comparison.missing_value_delta,
                    )

                with col3:
                    st.metric(
                        "Duplicate Rows",
                        comparison.duplicate_row_delta,
                    )

                # ------------------------------------------
                # Executive Summary
                # ------------------------------------------

                st.divider()

                st.subheader("Executive Summary")

                st.info(
                    comparison.summary.executive_summary
                )

                # ------------------------------------------
                # Improvements
                # ------------------------------------------

                st.subheader("✅ Improvements")

                if comparison.summary.improvements:

                    for item in comparison.summary.improvements:
                        st.success(item)

                else:
                    st.write("No improvements detected.")

                # ------------------------------------------
                # Regressions
                # ------------------------------------------

                st.subheader("⚠️ Regressions")

                if comparison.summary.regressions:

                    for item in comparison.summary.regressions:
                        st.error(item)

                else:
                    st.write("No regressions detected.")

                # ------------------------------------------
                # Recommendations
                # ------------------------------------------

                st.subheader("💡 Recommendations")

                if comparison.summary.recommendations:

                    for item in comparison.summary.recommendations:
                        st.info(item)

                # ------------------------------------------
                # Section Changes
                # ------------------------------------------

                st.divider()

                st.subheader("📂 Section Changes")

                st.json(comparison.section_changes)

        else:

            st.info(
                "No reports have been generated yet."
            )


    except Exception as exc:

        st.exception(exc)