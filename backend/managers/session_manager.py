from __future__ import annotations

from typing import Optional

import pandas as pd
import streamlit as st


class SessionManager:
    """
    Handles Streamlit session state for InsightPilot AI.
    """

    DATASET_KEY = "dataset"
    FILE_NAME_KEY = "file_name"

    @staticmethod
    def save_dataset(df: pd.DataFrame, file_name: str) -> None:
        """
        Save the uploaded dataset into the Streamlit session.
        """
        st.session_state[SessionManager.DATASET_KEY] = df
        st.session_state[SessionManager.FILE_NAME_KEY] = file_name

    @staticmethod
    def get_dataset() -> Optional[pd.DataFrame]:
        """
        Retrieve the current dataset from the session.
        """
        return st.session_state.get(SessionManager.DATASET_KEY)

    @staticmethod
    def get_file_name() -> Optional[str]:
        """
        Retrieve the uploaded filename.
        """
        return st.session_state.get(SessionManager.FILE_NAME_KEY)

    @staticmethod
    def has_dataset() -> bool:
        """
        Check whether a dataset is available.
        """
        return SessionManager.DATASET_KEY in st.session_state

    @staticmethod
    def clear() -> None:
        """
        Remove all dataset-related session data.
        """
        st.session_state.pop(SessionManager.DATASET_KEY, None)
        st.session_state.pop(SessionManager.FILE_NAME_KEY, None)