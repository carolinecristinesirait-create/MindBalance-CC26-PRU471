"""Reusable Streamlit user-interface components."""
from __future__ import annotations

from html import escape

import streamlit as st
import streamlit as st

from mindbalance.config import APP_NAME, APP_VERSION, CLASS_COLORS, NAV_ITEMS


def icon(name: str) -> str:
    return f'<i class="bi bi-{name}"></i>'


def render_sidebar(model_available: bool, model_name: str | None = None) -> str:
    with st.sidebar:
        st.markdown(
            f"""
            <div class="mb-brand">
              <div class="mb-brand-mark">M</div>
              <div><div class="mb-brand-name">{APP_NAME}</div><div class="mb-brand-sub">Wellness intelligence</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        labels = [item[0] for item in NAV_ITEMS]
        page = st.radio("Navigation", labels, key="page", label_visibility="collapsed")
        st.markdown("<div class='mb-sidebar-divider'></div>", unsafe_allow_html=True)
        status_class = "ok" if model_available else "warn"
        status_text = "AI model ready" if model_available else "Fallback mode"
        model_detail = model_name or "No TensorFlow model loaded"
        st.markdown(
            f"""
            <div class="mb-status-card">
              <div class="mb-status-line"><span class="mb-dot {status_class}"></span><strong>{status_text}</strong></div>
              <div class="mb-status-detail">{model_detail}</div>
            </div>
            <div class="mb-privacy-card">
              <div class="mb-small-kicker">PRIVACY</div>
              <div>Assessment data stay in this browser session unless you download a report.</div>
            </div>
            <div class="mb-sidebar-footer">v{APP_VERSION} · Caroline Cristine Sirait</div>
            """,
            unsafe_allow_html=True,
        )
    return page


def page_header(kicker: str, title: str, subtitle: str, icon_name: str = "sparkles") -> None:
    st.markdown(
        f"""
        <section class="mb-page-hero">
          <div class="mb-page-icon">{icon(icon_name)}</div>
          <div>
            <div class="mb-kicker">{kicker}</div>
            <h1>{title}</h1>
            <p>{subtitle}</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def notice(text: str, kind: str = "info", title: str | None = None) -> None:
    icons = {"info": "info-circle", "warning": "exclamation-triangle", "success": "check2-circle", "danger": "heart-pulse"}
    heading = f"<strong>{title}</strong>" if title else ""
    st.markdown(
        f"<div class='mb-notice {kind}'>{icon(icons.get(kind, 'info-circle'))}<div>{heading}<div>{text}</div></div></div>",
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, detail: str, icon_name: str = "activity", tone: str = "teal") -> None:
    st.markdown(
        f"""
        <div class="mb-metric-card {tone}">
          <div class="mb-metric-icon">{icon(icon_name)}</div>
          <div class="mb-metric-label">{label}</div>
          <div class="mb-metric-value">{value}</div>
          <div class="mb-metric-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def result_banner(level: str, score: float, confidence: float, description: str) -> None:
    """Render the large assessment summary card shown at the top of results."""
    color = CLASS_COLORS[level]
    st.markdown(
        f"""
        <section class="mb-result-banner" style="--risk-color:{color}">
          <div class="mb-result-copy">
            <div class="mb-result-kicker">PERSONAL WELLBEING ASSESSMENT</div>
            <h2>{level} Anxiety Risk Level</h2>
            <p>{description}</p>
          </div>
          <div class="mb-result-meta">
            <div class="mb-result-stat"><span>{score:.1f}</span><small>estimated score /10</small></div>
            <div class="mb-result-stat"><span>{confidence:.0%}</span><small>model confidence</small></div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def physiological_index_cards(indexes: list[dict[str, object]]) -> None:
    """Render the three key physiological index cards."""

    cards = ["<div class='mb-index-stack'>"]

    for item in indexes:
        value = max(0, min(100, int(item["value"])))
        risk_direction = str(item.get("direction", "higher-risk"))

        if risk_direction == "higher-protection":
            color = (
                "#2DD4BF"
                if value >= 70
                else "#FBBF24"
                if value >= 45
                else "#FB7185"
            )
        else:
            color = (
                "#FB7185"
                if value >= 65
                else "#FBBF24"
                if value >= 40
                else "#2DD4BF"
            )

        label = str(item["label"])
        detail = str(item["detail"])

        cards.append(
            f'<div class="mb-index-card" '
            f'style="--index-color:{color};--index-value:{value}%">'
            f'<div class="mb-index-head">'
            f'<span>{label}</span>'
            f'<strong>{value}%</strong>'
            f'</div>'
            f'<div class="mb-index-track">'
            f'<div class="mb-index-fill"></div>'
            f'</div>'
            f'<p>{detail}</p>'
            f'</div>'
        )

    cards.append("</div>")

    st.html("".join(cards))

def guidance_panel(
    items: list[dict[str, str]],
    empty_text: str,
) -> None:
    """Render restorative guidance directly as HTML."""

    if not items:
        st.caption(empty_text)
        return

    cards = [
        "<section class='mb-guidance-panel'>",
        "<div class='mb-guidance-heading'><span></span>",
        "<h3>Actionable Guidance &amp; "
        "Restorative Strategies</h3></div>",
        "<div class='mb-guidance-list'>",
    ]

    for item in items:
        title = escape(
            str(item.get("title", "Guidance"))
        )
        detail = escape(
            str(item.get("detail", ""))
        )

        cards.append(
            '<div class="mb-guidance-item">'
            '<div class="mb-guidance-dot"></div>'
            f'<div><strong>{title}</strong>'
            f'<p>{detail}</p></div>'
            '</div>'
        )

    cards.extend([
        "</div>",
        "</section>",
    ])

    st.html("".join(cards))

def section_title(title: str, subtitle: str | None = None, number: str | None = None) -> None:
    number_html = f"<span class='mb-section-number'>{number}</span>" if number else ""
    subtitle_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"<div class='mb-section-head'>{number_html}<div><h2>{title}</h2>{subtitle_html}</div></div>",
        unsafe_allow_html=True,
    )


def list_cards(
    items: list[dict[str, str]],
    empty_text: str,
) -> None:
    """Render signal cards directly as HTML."""

    if not items:
        st.caption(empty_text)
        return

    cards = [
        "<div class='mb-list-grid'>"
    ]

    for item in items:
        title = escape(
            str(item.get("title", "Signal"))
        )
        detail = escape(
            str(item.get("detail", ""))
        )
        icon_name = escape(
            str(
                item.get(
                    "icon",
                    "check-circle",
                )
            )
        )

        cards.append(
            '<div class="mb-list-card">'
            '<div class="mb-list-icon">'
            f'<i class="bi bi-{icon_name}"></i>'
            '</div>'
            f'<div><strong>{title}</strong>'
            f'<p>{detail}</p></div>'
            '</div>'
        )

    cards.append("</div>")

    st.html("".join(cards))

def step_card(number: str, title: str, text: str, icon_name: str) -> None:
    st.markdown(
        f"""
        <div class="mb-step-card">
          <div class="mb-step-top"><span>{number}</span>{icon(icon_name)}</div>
          <h3>{title}</h3><p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        """
        <footer class="mb-footer">
          <div><strong>MindBalance</strong> · Educational AI wellness dashboard</div>
          <div>Not a diagnosis · No automatic data storage</div>
        </footer>
        """,
        unsafe_allow_html=True,
    )
