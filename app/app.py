import streamlit as st

# Configure the page (must be the first Streamlit command)
st.set_page_config(
    page_title="InsightPilot AI",
    page_icon="📊",
    layout="wide"
)

# Main heading
st.title("🚀 InsightPilot AI")

# Subtitle
st.subheader("Enterprise Decision Intelligence Platform")

# Welcome message
st.success("Project initialized successfully!")

# A little information
st.write(
    """
    Welcome to InsightPilot AI!

    This platform will help business analysts:
    - Upload datasets
    - Analyze data quality
    - Discover KPIs
    - Generate insights
    - Forecast trends
    - Create executive reports
    """
)