"""Session-state initialization helpers."""
from __future__ import annotations

import streamlit as st


def initialize_state() -> None:
    defaults = {
        "page": "Home",
        "assessment_result": None,
        "assessment_count": 0,
        "entered": True,
        "toolkit_mood": None,
        "pending_page": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def navigate(page: str) -> None:
    """Queue navigation for the next rerun before the radio widget is created."""
    st.session_state.pending_page = page
    st.rerun()


def clear_assessment() -> None:
    st.session_state.assessment_result = None
