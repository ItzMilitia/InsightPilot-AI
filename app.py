import streamlit as st

from backend.engines.data_engine import DataEngine
from backend.managers.session_manager import SessionManager
from backend.engines.quality_engine import QualityEngine
from backend.services.metadata_service import get_dataset_metadata
from backend.services.validation_service import validate_file


st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide",
)

st.title("📊 InsightPilot AI")
st.subheader("Enterprise Decision Intelligence Platform")

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx", "xls"],
)

# -----------------------------
# Upload Dataset
# -----------------------------
if uploaded_file is not None:

    is_valid, message = validate_file(uploaded_file)

    if not is_valid:
        st.error(message)

    else:
        try:
            engine = DataEngine()

            df = engine.load_dataset(uploaded_file)

            SessionManager.save_dataset(
                df,
                uploaded_file.name,
            )

            st.success("✅ Dataset uploaded successfully!")

        except Exception as e:
            st.error(str(e))

# -----------------------------
# Display Dataset
# -----------------------------
if SessionManager.has_dataset():

    df = SessionManager.get_dataset()

    st.divider()

    st.subheader("📋 Dataset Preview")

    st.caption(
        "General information about the uploaded banking dataset."
    )
    
    st.dataframe(
        df.head(),
        width="stretch",
    )

    st.divider()

    st.subheader("📊 Dataset Metadata")

    metadata = get_dataset_metadata(
        df,
        SessionManager.get_file_name(),
    )

    st.json(metadata)

# -----------------------------
# Data Quality Report
# -----------------------------

    st.divider()

    st.subheader("🛡️ Data Quality Report")

    st.caption(
        "Automatically generated using the InsightPilot Quality Engine."
    )
    
    quality_engine = QualityEngine()

    report = quality_engine.analyze(df)

    col1, col2 = st.columns([2, 1])

    with col1:

        st.metric(
            "Quality Score",
            f"{report.quality_score:.2f}/100",
        )

        st.progress(
            report.quality_score / 100
        )

    with col2:

        if report.quality_grade == "Excellent":

            st.success(report.quality_grade)

        elif report.quality_grade == "Good":

            st.info(report.quality_grade)

        elif report.quality_grade == "Fair":

            st.warning(report.quality_grade)

        else:

            st.error(report.quality_grade)

    st.divider()

    metric1, metric2 = st.columns(2)

    metric3, metric4 = st.columns(2)

    metric1.metric(
        "Missing Values",
        report.missing_values,
    )

    metric2.metric(
        "Duplicate Rows",
        report.duplicate_rows,
    )

    metric3.metric(
        "Duplicate Columns",
        report.duplicate_columns,
    )

    metric4.metric(
        "Outlier Columns",
        len(report.outlier_summary),
    )

    st.divider()

    with st.expander(
        "📌 Missing Value Analysis",
        expanded=False,
    ):

        if report.missing_value_summary:

            st.dataframe(
                report.missing_value_summary,
                width="stretch",
            )

        else:

            st.success(
                "No missing values detected."
            )

    st.divider()

    with st.expander(
        "📈 Outlier Analysis",
        expanded=False,
    ):

        if report.outlier_summary:

            st.json(
                report.outlier_summary
            )

        else:

            st.success(
                "No outliers detected."
            )

        
    st.divider()

    with st.expander(
        "🧾 Data Type Analysis",
        expanded=False,
    ):

        st.dataframe(
            report.data_type_summary,
            width="stretch",
        )

    st.subheader("💡 Recommendations")

    st.caption(
        "Actionable recommendations based on the detected data quality issues."
    )
    
    if report.recommendations:

        for recommendation in report.recommendations:

            st.info(recommendation)

    else:

        st.success(
            "No recommendations. Dataset looks clean."
        )