import plotly.graph_objects as go
import streamlit as st

CHART_COLORS = ["#0E7490", "#0EA5E9", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]
TARGET_COLOR_MAP = {"Không bệnh tim": "#0EA5E9", "Có bệnh tim": "#EF4444"}
AGE_GROUP_ORDER = ["<40", "40-49", "50-59", "60-69", "70+"]


def apply_global_style() -> None:
    st.markdown(
        """
        <style>
            .block-container {padding-top: 1rem; padding-bottom: 1.2rem; max-width: 1360px;}
            h1, h2, h3 {letter-spacing: -0.2px; color: #0f172a;}
            [data-testid="stMetricValue"] {font-size: 1.8rem; color: #0f172a;}
            [data-testid="stMetricLabel"] {font-size: 0.95rem; color: #475569;}
            .kpi-note {font-size: 0.86rem; color: #64748b; margin-top: -6px;}
            .hero-card {
                background: linear-gradient(135deg, #0f172a 0%, #0e7490 100%);
                color: #f8fafc;
                border-radius: 14px;
                padding: 18px 20px;
                margin-bottom: 8px;
            }
            .hero-card h3 {color: #f8fafc; margin: 0 0 6px 0;}
            .hero-card p {margin: 0; opacity: 0.95;}
            .section-card {
                border: 1px solid #e2e8f0;
                border-radius: 14px;
                padding: 14px 16px;
                background: #ffffff;
                box-shadow: 0 1px 4px rgba(15,23,42,0.05);
            }
            .section-card h4 {margin: 0 0 6px 0; color: #0f172a;}
            .section-card p {margin: 0; color: #475569; font-size: 0.94rem;}
            [data-testid="stSidebar"] {background: #f8fafc;}
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color: #334155;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str) -> None:
    st.title(title)
    st.caption(subtitle)


def hero_banner(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <h3>{title}</h3>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_figure(fig: go.Figure, title: str | None = None) -> go.Figure:
    if title:
        fig.update_layout(title=title)
    fig.update_layout(
        template="simple_white",
        colorway=CHART_COLORS,
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        title=dict(x=0.01, xanchor="left"),
        hoverlabel=dict(bgcolor="white"),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e5e7eb")
    return fig
