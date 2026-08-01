"""Project details and repository guidance."""
from __future__ import annotations

import streamlit as st

from mindbalance.config import APP_VERSION, TEAM_ID, TEAM_MEMBERS
from mindbalance.ui import footer, notice, page_header, section_title


def render_about() -> None:
    page_header(
        "CODING CAMP 2026 · HEALTHY LIVES & WELL-BEING",
        "About the project",
        "MindBalance was developed as a data-science and AI engineering demonstration for structured anxiety-pattern screening and wellness education.",
        "info-circle",
    )

    section_title("Project identity", "Core information included in the repository.", "01")
    c1, c2 = st.columns([0.9, 1.1], gap="large")
    with c1:
        st.markdown(
            f"""
            <div class="mb-about-card">
              <div class="mb-small-kicker">TEAM ID</div><h2>{TEAM_ID}</h2>
              <div class="mb-small-kicker">APP VERSION</div><h3>{APP_VERSION}</h3>
              <div class="mb-small-kicker">THEME</div><p>Healthy Lives & Well-being</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown("#### Team members")
        for member in TEAM_MEMBERS:
            st.markdown(f"<div class='mb-member'><i class='bi bi-person-circle'></i><span>{member}</span></div>", unsafe_allow_html=True)

    section_title("Repository structure", "The ZIP is organized for direct GitHub upload and Streamlit deployment.", "02")
    st.code(
        """MindBalance-GitHub/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/config.toml
├── data/cleaned_anxiety_data.csv
├── models/*.keras
├── notebooks/MindBalance_training_notebook.ipynb
├── mindbalance/
│   ├── pages/
│   ├── features.py
│   ├── model_engine.py
│   ├── recommendations.py
│   ├── charts.py
│   └── ...
├── tests/
└── .github/workflows/quality.yml""",
        language="text",
    )

    section_title("Deploy on Streamlit Community Cloud", "Use the included repository without changing file paths.", "03")
    steps = [
        "Create a new GitHub repository.",
        "Upload the contents of this ZIP so app.py is at the repository root.",
        "Open Streamlit Community Cloud and choose New app.",
        "Select the repository, branch, and app.py as the entrypoint.",
        "Choose Python 3.11 for the deployment environment.",
        "Deploy and review the build logs if TensorFlow installation fails.",
    ]
    for index, step in enumerate(steps, start=1):
        st.markdown(f"<div class='mb-deploy-step'><span>{index}</span><p>{step}</p></div>", unsafe_allow_html=True)

    notice(
        "The repository does not require API keys. It contains the model and dataset directly, so the dashboard can run as a self-contained demonstration.",
        "success",
    )

    section_title("License and contribution", "The ZIP includes an MIT license, contribution guide, security notes, tests, and a basic GitHub Actions workflow.", "04")
    st.markdown(
        "Use the project as a starting point. Before any production or clinical use, complete external validation, privacy review, security hardening, accessibility testing, and professional governance."
    )
    footer()
