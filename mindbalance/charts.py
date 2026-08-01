"""Plotly chart factories with a consistent visual system."""
from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from mindbalance.config import CLASS_COLORS, CLASS_ORDER, MODEL_METRICS

PLOT_FONT = "Plus Jakarta Sans, Inter, Arial, sans-serif"
GRID = "rgba(148,163,184,0.12)"
TEXT = "#CBD5E1"
TITLE = "#F8FAFC"


def style_figure(fig: go.Figure, *, height: int = 380, title: str | None = None) -> go.Figure:
    fig.update_layout(
        height=height,
        title=title,
        font=dict(family=PLOT_FONT, color=TEXT, size=12),
        title_font=dict(size=17, color=TITLE),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=16, r=16, t=58 if title else 30, b=18),
        hoverlabel=dict(bgcolor="#0F172A", bordercolor="#334155", font_color="#F8FAFC"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
        ),
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor="rgba(148,163,184,0.15)")
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor="rgba(148,163,184,0.15)")
    return fig


def probability_donut(probabilities: dict[str, float]) -> go.Figure:
    labels = list(CLASS_ORDER)
    values = [probabilities[label] for label in labels]
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.68,
            sort=False,
            marker=dict(colors=[CLASS_COLORS[x] for x in labels], line=dict(color="#07111F", width=3)),
            textinfo="label+percent",
            textfont=dict(size=12),
            hovertemplate="%{label}: %{value:.1%}<extra></extra>",
        )
    )
    fig.add_annotation(
        text=f"{max(values):.0%}<br><span style='font-size:11px'>top probability</span>",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=23, color=TITLE),
    )
    return style_figure(fig, height=320)


def wellness_radar(scores: dict[str, int]) -> go.Figure:
    labels = list(scores)
    values = list(scores.values())
    fig = go.Figure(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor="rgba(45,212,191,0.18)",
            line=dict(color="#2DD4BF", width=3),
            marker=dict(size=6, color="#99F6E4"),
            hovertemplate="%{theta}: %{r}/100<extra></extra>",
            name="Profile",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor=GRID, linecolor=GRID),
            angularaxis=dict(
                gridcolor=GRID,
                linecolor=GRID,
                tickfont=dict(size=12, color="#D7E2EF"),
            ),
        ),
        showlegend=False,
    )
    return style_figure(fig, height=390)


def category_distribution(df: pd.DataFrame) -> go.Figure:
    counts = df["Anxiety_Category"].value_counts().reindex(CLASS_ORDER, fill_value=0)
    pct = counts / max(counts.sum(), 1)
    fig = go.Figure(
        go.Bar(
            x=list(CLASS_ORDER),
            y=counts.values,
            marker_color=[CLASS_COLORS[x] for x in CLASS_ORDER],
            customdata=np.column_stack([pct.values]),
            hovertemplate="%{x}: %{y:,} records (%{customdata[0]:.1%})<extra></extra>",
            text=[f"{v:,}<br>{p:.1%}" for v, p in zip(counts.values, pct.values)],
            textposition="outside",
        )
    )
    return style_figure(fig, title="Anxiety category distribution", height=380)


def anxiety_histogram(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df,
        x="Anxiety Level (1-10)",
        color="Anxiety_Category",
        color_discrete_map=CLASS_COLORS,
        category_orders={"Anxiety_Category": list(CLASS_ORDER)},
        nbins=10,
        barmode="overlay",
        opacity=0.78,
        labels={"Anxiety Level (1-10)": "Self-reported anxiety level", "count": "Records"},
    )
    return style_figure(fig, title="Anxiety score distribution", height=380)


def feature_boxplot(df: pd.DataFrame, feature: str) -> go.Figure:
    fig = px.box(
        df,
        x="Anxiety_Category",
        y=feature,
        color="Anxiety_Category",
        color_discrete_map=CLASS_COLORS,
        category_orders={"Anxiety_Category": list(CLASS_ORDER)},
        points="outliers",
    )
    fig.update_layout(showlegend=False)
    return style_figure(fig, title=f"{feature} by anxiety category", height=390)


def feature_profile(df: pd.DataFrame, features: Iterable[str]) -> go.Figure:
    features = list(features)
    means = df.groupby("Anxiety_Category")[features].mean().reindex(CLASS_ORDER)
    normalized = means.copy()
    for column in normalized:
        low = float(df[column].min())
        high = float(df[column].max())
        normalized[column] = 100 * (normalized[column] - low) / max(high - low, 1e-9)
    fig = go.Figure()
    for category in CLASS_ORDER:
        fig.add_trace(
            go.Scatterpolar(
                r=normalized.loc[category].tolist() + [normalized.loc[category].iloc[0]],
                theta=features + [features[0]],
                name=category,
                line=dict(color=CLASS_COLORS[category], width=2.5),
                fill="toself",
                opacity=0.72,
                hovertemplate=f"{category}<br>%{{theta}}: %{{r:.0f}} normalized<extra></extra>",
            )
        )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor=GRID),
            angularaxis=dict(gridcolor=GRID),
        )
    )
    return style_figure(fig, title="Normalized category signatures", height=470)


def correlation_heatmap(df: pd.DataFrame, columns: list[str]) -> go.Figure:
    corr = df[columns].corr(numeric_only=True)
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
    )
    fig.update_coloraxes(colorbar_title="r")
    return style_figure(fig, title="Correlation matrix", height=600)


def sleep_caffeine_heatmap(df: pd.DataFrame) -> go.Figure:
    sleep = pd.cut(
        df["Sleep Hours"],
        bins=[-np.inf, 6, 8, np.inf],
        labels=["<6 h", "6–8 h", ">8 h"],
    )
    caffeine = pd.cut(
        df["Caffeine Intake (mg/day)"],
        bins=[-np.inf, 100, 300, np.inf],
        labels=["<100 mg", "100–300 mg", ">300 mg"],
    )
    pivot = (
        df.assign(_sleep=sleep, _caffeine=caffeine)
        .groupby(["_sleep", "_caffeine"], observed=False)["Anxiety Level (1-10)"]
        .mean()
        .unstack()
    )
    fig = px.imshow(
        pivot,
        text_auto=".2f",
        color_continuous_scale="YlOrRd",
        aspect="auto",
        labels={"x": "Daily caffeine", "y": "Nightly sleep", "color": "Mean anxiety"},
    )
    return style_figure(fig, title="Sleep × caffeine interaction", height=390)


def demographic_bar(df: pd.DataFrame, column: str) -> go.Figure:
    table = (
        df.groupby([column, "Anxiety_Category"], observed=False)
        .size()
        .rename("count")
        .reset_index()
    )
    total = table.groupby(column)["count"].transform("sum")
    table["share"] = table["count"] / total
    fig = px.bar(
        table,
        x=column,
        y="share",
        color="Anxiety_Category",
        color_discrete_map=CLASS_COLORS,
        category_orders={"Anxiety_Category": list(CLASS_ORDER)},
        barmode="stack",
        labels={"share": "Share", "Anxiety_Category": "Risk"},
    )
    fig.update_yaxes(tickformat=".0%")
    return style_figure(fig, title=f"Category share by {column.lower()}", height=420)


def occupation_ranking(df: pd.DataFrame) -> go.Figure:
    ranking = (
        df.groupby("Occupation")["Anxiety Level (1-10)"]
        .agg(["mean", "count"])
        .sort_values("mean")
        .reset_index()
    )
    fig = px.bar(
        ranking,
        x="mean",
        y="Occupation",
        orientation="h",
        color="mean",
        color_continuous_scale="Tealgrn",
        custom_data=["count"],
        labels={"mean": "Mean anxiety score"},
    )
    fig.update_traces(hovertemplate="%{y}<br>Mean: %{x:.2f}<br>Records: %{customdata[0]:,}<extra></extra>")
    fig.update_layout(coloraxis_showscale=False)
    return style_figure(fig, title="Average anxiety score by occupation", height=480)


def model_metrics_bar() -> go.Figure:
    rows = []
    for label, values in MODEL_METRICS["class_report"].items():
        for metric in ("precision", "recall", "f1"):
            rows.append({"Class": label, "Metric": metric.title(), "Value": values[metric]})
    table = pd.DataFrame(rows)
    fig = px.bar(
        table,
        x="Class",
        y="Value",
        color="Metric",
        barmode="group",
        category_orders={"Class": list(CLASS_ORDER)},
        range_y=[0, 1],
        text_auto=".2f",
    )
    fig.update_yaxes(tickformat=".0%")
    return style_figure(fig, title="Per-class test performance", height=410)


def confusion_matrix_figure() -> go.Figure:
    matrix = np.asarray(MODEL_METRICS["approx_confusion_matrix"])
    fig = px.imshow(
        matrix,
        x=list(CLASS_ORDER),
        y=list(CLASS_ORDER),
        text_auto="d",
        color_continuous_scale="Blues",
        labels={"x": "Predicted", "y": "Actual", "color": "Records"},
    )
    return style_figure(fig, title="Approximate confusion matrix", height=410)


def gauge(value: float, title: str, suffix: str = "") -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": suffix, "font": {"color": TITLE, "size": 28}},
            title={"text": title, "font": {"color": TEXT, "size": 13}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": TEXT},
                "bar": {"color": "#2DD4BF"},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(251,113,133,0.18)"},
                    {"range": [40, 70], "color": "rgba(251,191,36,0.16)"},
                    {"range": [70, 100], "color": "rgba(45,212,191,0.16)"},
                ],
            },
        )
    )
    return style_figure(fig, height=250)
