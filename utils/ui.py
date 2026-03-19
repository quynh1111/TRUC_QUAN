import plotly.graph_objects as go
import streamlit as st

CHART_COLORS = ["#0E7490", "#0EA5E9", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#F97316"]
TARGET_COLOR_MAP = {"Không bệnh tim": "#0EA5E9", "Có bệnh tim": "#EF4444"}
AGE_GROUP_ORDER = ["<40", "40-49", "50-59", "60-69", "70+"]


def apply_global_style() -> None:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

            * {font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;}

            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                max-width: 1400px;
            }

            h1 {
                letter-spacing: -0.5px;
                color: #0f172a;
                font-weight: 700;
                font-size: 2.2rem;
                margin-bottom: 0.5rem;
            }

            h2 {
                letter-spacing: -0.3px;
                color: #1e293b;
                font-weight: 600;
                font-size: 1.6rem;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }

            h3 {
                letter-spacing: -0.2px;
                color: #334155;
                font-weight: 600;
                font-size: 1.3rem;
            }

            [data-testid="stMetricValue"] {
                font-size: 2.2rem;
                color: #0f172a;
                font-weight: 700;
            }

            [data-testid="stMetricLabel"] {
                font-size: 0.95rem;
                color: #64748b;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            [data-testid="stMetricDelta"] {
                font-size: 0.9rem;
            }

            .kpi-note {
                font-size: 0.88rem;
                color: #64748b;
                margin-top: -8px;
                font-style: italic;
            }

            .hero-card {
                background: linear-gradient(135deg, #0f172a 0%, #1e40af 50%, #0e7490 100%);
                color: #f8fafc;
                border-radius: 16px;
                padding: 24px 28px;
                margin-bottom: 16px;
                box-shadow: 0 10px 30px rgba(15,23,42,0.15);
                border: 1px solid rgba(255,255,255,0.1);
                animation: fadeInUp 0.6s ease-out;
            }

            .hero-card h3 {
                color: #f8fafc;
                margin: 0 0 8px 0;
                font-weight: 700;
                font-size: 1.5rem;
            }

            .hero-card p {
                margin: 0;
                opacity: 0.95;
                font-size: 1.05rem;
                line-height: 1.6;
            }

            .section-card {
                border: 1px solid #e2e8f0;
                border-radius: 16px;
                padding: 20px 24px;
                background: #ffffff;
                box-shadow: 0 2px 8px rgba(15,23,42,0.06);
                transition: all 0.3s ease;
                margin-bottom: 12px;
            }

            .section-card:hover {
                box-shadow: 0 8px 20px rgba(15,23,42,0.12);
                transform: translateY(-2px);
                border-color: #cbd5e1;
            }

            .section-card h4 {
                margin: 0 0 8px 0;
                color: #0f172a;
                font-weight: 600;
                font-size: 1.15rem;
            }

            .section-card p {
                margin: 0;
                color: #475569;
                font-size: 0.95rem;
                line-height: 1.5;
            }

            .metric-card {
                background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                border: 2px solid #e2e8f0;
                border-radius: 14px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(15,23,42,0.05);
                transition: all 0.3s ease;
            }

            .metric-card:hover {
                border-color: #0e7490;
                box-shadow: 0 6px 16px rgba(14,116,144,0.15);
                transform: translateY(-3px);
            }

            .metric-card .value {
                font-size: 2.5rem;
                font-weight: 700;
                color: #0e7490;
                margin-bottom: 4px;
            }

            .metric-card .label {
                font-size: 0.9rem;
                color: #64748b;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 500;
            }

            .info-badge {
                display: inline-block;
                background: #dbeafe;
                color: #1e40af;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin: 4px;
            }

            .success-badge {
                display: inline-block;
                background: #dcfce7;
                color: #166534;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin: 4px;
            }

            .warning-badge {
                display: inline-block;
                background: #fef3c7;
                color: #92400e;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin: 4px;
            }

            .danger-badge {
                display: inline-block;
                background: #fee2e2;
                color: #991b1b;
                padding: 6px 14px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 600;
                margin: 4px;
            }

            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
                border-right: 1px solid #e2e8f0;
            }

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
                color: #334155;
            }

            [data-testid="stSidebar"] h2 {
                color: #0f172a;
                font-size: 1.2rem;
                font-weight: 600;
            }

            div[data-testid="stExpander"] {
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                background: #ffffff;
                box-shadow: 0 1px 3px rgba(15,23,42,0.04);
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
            }

            .stTabs [data-baseweb="tab"] {
                background-color: #f8fafc;
                border-radius: 8px 8px 0 0;
                padding: 12px 24px;
                font-weight: 500;
                color: #64748b;
            }

            .stTabs [aria-selected="true"] {
                background-color: #ffffff;
                color: #0e7490;
                border-bottom: 3px solid #0e7490;
            }

            .stDataFrame {
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                overflow: hidden;
            }

            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            @keyframes pulse {
                0%, 100% {
                    opacity: 1;
                }
                50% {
                    opacity: 0.8;
                }
            }

            .animate-fade-in {
                animation: fadeInUp 0.6s ease-out;
            }
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


def style_figure(fig: go.Figure, title: str | None = None, height: int | None = None) -> go.Figure:
    if title:
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b>",
                x=0.01,
                xanchor="left",
                font=dict(size=18, color="#0f172a", family="Inter"),
            )
        )

    layout_config = dict(
        template="simple_white",
        colorway=CHART_COLORS,
        margin=dict(l=20, r=20, t=70, b=20),
        legend_title_text="",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e2e8f0",
            borderwidth=1,
            font=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Inter",
            bordercolor="#cbd5e1",
        ),
        plot_bgcolor="rgba(248, 250, 252, 0.4)",
        paper_bgcolor="white",
        font=dict(family="Inter", color="#334155"),
    )

    if height:
        layout_config["height"] = height

    fig.update_layout(**layout_config)
    fig.update_xaxes(showgrid=False, linecolor="#e2e8f0", tickfont=dict(size=11))
    fig.update_yaxes(gridcolor="#e5e7eb", linecolor="#e2e8f0", tickfont=dict(size=11))

    return fig


def metric_card(label: str, value: str, delta: str | None = None, delta_color: str = "normal") -> None:
    """Create an enhanced metric card with custom styling"""
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)


def info_badge(text: str, badge_type: str = "info") -> str:
    """Create a colored badge. Types: info, success, warning, danger"""
    badge_classes = {
        "info": "info-badge",
        "success": "success-badge",
        "warning": "warning-badge",
        "danger": "danger-badge",
    }
    badge_class = badge_classes.get(badge_type, "info-badge")
    return f'<span class="{badge_class}">{text}</span>'


def divider_with_text(text: str) -> None:
    """Create a divider with text in the middle"""
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin: 24px 0;">
            <div style="flex: 1; height: 1px; background: #e2e8f0;"></div>
            <div style="padding: 0 16px; color: #64748b; font-weight: 500; font-size: 0.9rem;">
                {text}
            </div>
            <div style="flex: 1; height: 1px; background: #e2e8f0;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_box(value: str, label: str, icon: str = "📊", color: str = "#0e7490") -> None:
    """Create a stat box with icon"""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
            border-left: 4px solid {color};
            border-radius: 10px;
            padding: 20px;
            margin: 10px 0;
        ">
            <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
            <div style="font-size: 2rem; font-weight: 700; color: {color}; margin-bottom: 4px;">
                {value}
            </div>
            <div style="font-size: 0.9rem; color: #64748b; text-transform: uppercase; font-weight: 500; letter-spacing: 0.5px;">
                {label}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
