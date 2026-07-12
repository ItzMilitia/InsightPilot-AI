import streamlit as st

from backend.engines.data_engine import DataEngine
from backend.managers.session_manager import SessionManager
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