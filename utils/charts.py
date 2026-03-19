import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def iqr_outlier_count(series: pd.Series) -> int:
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return int(((series < lower) | (series > upper)).sum())


def create_gauge_chart(value: float, title: str, max_value: float = 100, color: str = "#0e7490") -> go.Figure:
    """Create a gauge chart for displaying percentage or ratio"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 16, 'color': '#0f172a', 'family': 'Inter'}},
        number={'suffix': "%", 'font': {'size': 40, 'color': color}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#e2e8f0",
            'steps': [
                {'range': [0, max_value * 0.3], 'color': '#dcfce7'},
                {'range': [max_value * 0.3, max_value * 0.7], 'color': '#fef3c7'},
                {'range': [max_value * 0.7, max_value], 'color': '#fee2e2'},
            ],
            'threshold': {
                'line': {'color': "#0f172a", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'family': 'Inter', 'color': '#334155'}
    )

    return fig


def create_funnel_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str = "") -> go.Figure:
    """Create a funnel chart for showing conversion or progression"""
    fig = go.Figure(go.Funnel(
        y=data[y_col],
        x=data[x_col],
        textposition="inside",
        textinfo="value+percent initial",
        marker={
            "color": ["#0e7490", "#0ea5e9", "#10b981", "#f59e0b", "#ef4444"],
            "line": {"width": 2, "color": "white"}
        },
        connector={"line": {"color": "#cbd5e1", "width": 2}},
    ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.01, xanchor="left", font=dict(size=18, color="#0f172a")),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'family': 'Inter', 'color': '#334155'}
    )

    return fig


def create_waterfall_chart(categories: list, values: list, title: str = "") -> go.Figure:
    """Create a waterfall chart for showing incremental changes"""
    fig = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        x=categories,
        y=values,
        text=[f"+{v}" if v > 0 else str(v) for v in values],
        textposition="outside",
        connector={"line": {"color": "#cbd5e1", "width": 2}},
        increasing={"marker": {"color": "#10b981"}},
        decreasing={"marker": {"color": "#ef4444"}},
        totals={"marker": {"color": "#0e7490"}},
    ))

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.01, xanchor="left", font=dict(size=18, color="#0f172a")),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        showlegend=False,
        font={'family': 'Inter', 'color': '#334155'}
    )

    return fig


def create_sunburst_chart(data: pd.DataFrame, path_cols: list, value_col: str, title: str = "") -> go.Figure:
    """Create a sunburst chart for hierarchical data"""
    fig = px.sunburst(
        data,
        path=path_cols,
        values=value_col,
        color=value_col,
        color_continuous_scale="Blues",
    )

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.01, xanchor="left", font=dict(size=18, color="#0f172a")),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'family': 'Inter', 'color': '#334155'}
    )

    return fig


def create_treemap_chart(data: pd.DataFrame, path_cols: list, value_col: str, title: str = "") -> go.Figure:
    """Create a treemap chart for hierarchical data"""
    fig = px.treemap(
        data,
        path=path_cols,
        values=value_col,
        color=value_col,
        color_continuous_scale="RdYlGn_r",
    )

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.01, xanchor="left", font=dict(size=18, color="#0f172a")),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'family': 'Inter', 'color': '#334155'}
    )

    return fig


def create_radar_chart(categories: list, values_dict: dict, title: str = "") -> go.Figure:
    """Create a radar chart for multi-dimensional comparison

    Args:
        categories: List of category names
        values_dict: Dict with format {"Series Name": [values]}
        title: Chart title
    """
    fig = go.Figure()

    colors = ["#0e7490", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6"]

    for idx, (name, values) in enumerate(values_dict.items()):
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=name,
            line=dict(color=colors[idx % len(colors)], width=2),
            fillcolor=colors[idx % len(colors)],
            opacity=0.6,
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max([max(v) for v in values_dict.values()]) * 1.1],
                gridcolor="#e5e7eb",
            ),
            angularaxis=dict(gridcolor="#e5e7eb"),
            bgcolor="rgba(248, 250, 252, 0.4)",
        ),
        title=dict(text=f"<b>{title}</b>", x=0.01, xanchor="left", font=dict(size=18, color="#0f172a")),
        margin=dict(l=60, r=60, t=80, b=60),
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        font={'family': 'Inter', 'color': '#334155'}
    )

    return fig


def create_violin_chart(data: pd.DataFrame, x_col: str, y_col: str, color_col: str = None, title: str = "") -> go.Figure:
    """Create a violin plot for distribution comparison"""
    fig = px.violin(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        box=True,
        points="outliers",
        color_discrete_sequence=["#0e7490", "#ef4444", "#10b981", "#f59e0b"],
    )

    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.01, xanchor="left", font=dict(size=18, color="#0f172a")),
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        plot_bgcolor="rgba(248, 250, 252, 0.4)",
        font={'family': 'Inter', 'color': '#334155'}
    )

    return fig
