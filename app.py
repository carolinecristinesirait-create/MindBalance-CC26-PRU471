"""MindBalance Streamlit entrypoint.

Run locally with:
    streamlit run app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="MindBalance | AI Wellness Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://docs.streamlit.io/",
        "Report a bug": "https://github.com/",
        "About": "MindBalance v2.0 · Educational AI wellness dashboard",
    },
)

from mindbalance.pages.about import render_about
from mindbalance.pages.assessment import render_assessment
from mindbalance.pages.home import render_home
from mindbalance.pages.insights import render_insights
from mindbalance.pages.toolkit import render_toolkit
from mindbalance.pages.transparency import render_transparency
from mindbalance.resources import get_model_bundle, load_dataset
from mindbalance.state import initialize_state
from mindbalance.theme import inject_particles, inject_theme
from mindbalance.ui import render_sidebar


def main() -> None:
    initialize_state()
    inject_theme()
    inject_particles()

    pending_page = st.session_state.get("pending_page")
    if pending_page:
        st.session_state.page = pending_page
        st.session_state.pending_page = None

    df = load_dataset()
    bundle = get_model_bundle()
    model_name = bundle.path.name if bundle.path else None
    page = render_sidebar(bundle.available, model_name)

    routes = {
        "Home": lambda: render_home(df, bundle.available),
        "Assessment": lambda: render_assessment(bundle),
        "Insights": lambda: render_insights(df),
        "Wellness Toolkit": render_toolkit,
        "Model & Data": lambda: render_transparency(df, bundle),
        "About": render_about,
    }
    renderer = routes.get(page, routes["Home"])
    renderer()


if __name__ == "__main__":
    main()
