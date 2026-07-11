import streamlit as st
import pandas as pd

from backend.services.validation_service import validate_file
from backend.services.upload_service import load_dataset
from backend.services.metadata_service import get_dataset_metadata

st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 InsightPilot AI")
st.subheader("Enterprise Decision Intelligence Platform")

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx"]
)

if uploaded_file:

    valid, message = validate_file(uploaded_file)

    if not valid:
        st.error(message)

    else:

        st.success(message)

        df = load_dataset(uploaded_file)

        metadata = get_dataset_metadata(df, uploaded_file)

        st.header("Dataset Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", metadata["Rows"])

        with col2:
            st.metric("Columns", metadata["Columns"])

        with col3:
            st.metric("Memory (MB)", metadata["Memory Usage (MB)"])

        st.write("### Metadata")

        st.json(metadata)

        st.write("### Dataset Preview")

        st.dataframe(df.head(10), use_container_width=True)