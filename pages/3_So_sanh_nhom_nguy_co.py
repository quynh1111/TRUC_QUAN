import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
import pandas as pd

from utils.data_loader import apply_common_filters, load_data
from utils.ui import AGE_GROUP_ORDER, TARGET_COLOR_MAP, apply_global_style, page_header, style_figure, divider_with_text, stat_box


df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("📈 Page 3 – So sánh nhóm nguy cơ", "Phân tích và so sánh tỷ lệ bệnh tim giữa các nhóm để nhận diện phân khúc rủi ro cao.")

if df.empty:
    st.warning("⚠️ Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter trên sidebar.")
    st.stop()

st.markdown("### 🎯 Lựa chọn chiều phân tích")

feature_map = {
    "👥 Giới tính": "sex_label",
    "💔 Loại đau ngực": "cp_label",
    "🏃 Đau thắt ngực khi gắng sức": "exang_label",
    "🍬 Đường huyết lúc đói": "fbs_label",
    "📅 Nhóm tuổi": "age_group",
}

col1, col2 = st.columns(2)

with col1:
    selected_feature_name = st.selectbox("🔍 Chọn chiều phân tích chính", list(feature_map.keys()))
    selected_feature = feature_map[selected_feature_name]

with col2:
    category_options = [str(v) for v in df[selected_feature].dropna().unique().tolist()]
    selected_categories = st.multiselect(
        "📊 Chọn các nhóm để so sánh",
        category_options,
        default=category_options,
        help="Chọn nhiều nhóm để so sánh tỷ lệ bệnh tim"
    )

if not selected_categories:
    st.warning("⚠️ Vui lòng chọn ít nhất một nhóm để phân tích!")
    st.stop()

compare_df = df[df[selected_feature].astype(str).isin(selected_categories)].copy()

summary = (
    compare_df.groupby(selected_feature)
    .agg(so_ho_so=("target", "size"), ty_le_benh_tim=("target", "mean"))
    .reset_index()
)
summary["ty_le_benh_tim"] = (summary["ty_le_benh_tim"] * 100).round(2)

divider_with_text("SO SÁNH TỶ LỆ BỆNH TIM")

st.markdown("### 📊 Biểu đồ so sánh chi tiết")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.markdown("#### 📊 Tỷ lệ bệnh tim theo nhóm")

    fig_bar = px.bar(
        summary,
        x=selected_feature,
        y="ty_le_benh_tim",
        text="ty_le_benh_tim",
        color="ty_le_benh_tim",
        color_continuous_scale="RdYlGn_r",
    )

    fig_bar.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont_size=13,
    )

    if selected_feature == "age_group":
        fig_bar.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)

    fig_bar = style_figure(fig_bar, height=400)
    fig_bar.update_layout(
        xaxis_title="",
        yaxis_title="Tỷ lệ bệnh tim (%)",
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with viz_col2:
    st.markdown("#### 📈 So sánh quy mô mẫu")

    fig_size = px.bar(
        summary,
        x=selected_feature,
        y="so_ho_so",
        text="so_ho_so",
        color_discrete_sequence=["#0e7490"],
    )

    fig_size.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        textfont_size=13,
    )

    if selected_feature == "age_group":
        fig_size.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)

    fig_size = style_figure(fig_size, height=400)
    fig_size.update_layout(
        xaxis_title="",
        yaxis_title="Số lượng hồ sơ",
        showlegend=False,
    )
    st.plotly_chart(fig_size, use_container_width=True)

divider_with_text("BIỂU ĐỒ STACKED")

st.markdown("### 📊 Phân tích tổng hợp (Stacked Charts)")

stacked = compare_df.groupby([selected_feature, "target_label"]).size().reset_index(name="count")

stacked_col1, stacked_col2 = st.columns(2)

with stacked_col1:
    st.markdown("#### 📊 Stacked Bar - Số lượng")

    fig_stacked = px.bar(
        stacked,
        x=selected_feature,
        y="count",
        color="target_label",
        barmode="stack",
        color_discrete_map=TARGET_COLOR_MAP,
        text="count",
    )

    fig_stacked.update_traces(textposition="inside", textfont_size=12)

    if selected_feature == "age_group":
        fig_stacked.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)

    fig_stacked = style_figure(fig_stacked, height=400)
    fig_stacked.update_layout(xaxis_title="", yaxis_title="Số lượng")
    st.plotly_chart(fig_stacked, use_container_width=True)

with stacked_col2:
    st.markdown("#### 📊 Stacked Bar - Phần trăm (100%)")

    normalized = stacked.copy()
    totals = normalized.groupby(selected_feature)["count"].transform("sum")
    normalized["percent"] = (normalized["count"] / totals * 100).round(2)

    fig_norm = px.bar(
        normalized,
        x=selected_feature,
        y="percent",
        color="target_label",
        barmode="stack",
        color_discrete_map=TARGET_COLOR_MAP,
        text="percent",
    )

    fig_norm.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="inside",
        textfont_size=11,
    )

    if selected_feature == "age_group":
        fig_norm.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)

    fig_norm = style_figure(fig_norm, height=400)
    fig_norm.update_layout(xaxis_title="", yaxis_title="Tỷ lệ (%)")
    st.plotly_chart(fig_norm, use_container_width=True)

divider_with_text("BẢNG THỐNG KÊ CHI TIẾT")

st.markdown("### 📋 Bảng thống kê và khoảng tin cậy")

detail = summary.copy()
if not detail.empty:
    p = detail["ty_le_benh_tim"] / 100
    n = detail["so_ho_so"].clip(lower=1)
    ci = 1.96 * np.sqrt((p * (1 - p)) / n)
    detail["CI thấp (95%)"] = ((p - ci).clip(lower=0) * 100).round(2)
    detail["CI cao (95%)"] = ((p + ci).clip(upper=1) * 100).round(2)
    detail["Độ rộng CI"] = (detail["CI cao (95%)"] - detail["CI thấp (95%)"]).round(2)

tab1, tab2 = st.columns(2)

with tab1:
    st.markdown("#### 📊 Bảng tổng hợp")
    st.dataframe(detail, use_container_width=True, hide_index=True)

with tab2:
    st.markdown("#### 📈 Khoảng tin cậy 95%")

    fig_ci = go.Figure()

    for idx, row in detail.iterrows():
        fig_ci.add_trace(go.Scatter(
            x=[row['CI thấp (95%)'], row['ty_le_benh_tim'], row['CI cao (95%)']],
            y=[row[selected_feature]] * 3,
            mode='lines+markers',
            name=str(row[selected_feature]),
            line=dict(width=3),
            marker=dict(size=[8, 12, 8], symbol=['line-ew', 'circle', 'line-ew']),
            showlegend=False,
        ))

    fig_ci = style_figure(fig_ci, height=350)
    fig_ci.update_layout(
        xaxis_title="Tỷ lệ bệnh tim (%)",
        yaxis_title="",
        hovermode='closest'
    )
    st.plotly_chart(fig_ci, use_container_width=True)

st.caption("📌 Khoảng tin cậy 95% thể hiện độ chính xác của ước lượng tỷ lệ bệnh tim cho từng nhóm.")

divider_with_text("INSIGHTS VÀ SO SÁNH")

st.markdown("### 💡 Insights và so sánh nhóm")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

if not summary.empty:
    top_row = summary.sort_values("ty_le_benh_tim", ascending=False).iloc[0]
    bottom_row = summary.sort_values("ty_le_benh_tim", ascending=True).iloc[0]
    gap = top_row["ty_le_benh_tim"] - bottom_row["ty_le_benh_tim"]
    avg_rate = summary["ty_le_benh_tim"].mean()

    with kpi_col1:
        stat_box(f"{top_row['ty_le_benh_tim']:.1f}%", "Tỷ lệ cao nhất", "🔴", "#ef4444")
        st.caption(f"_{top_row[selected_feature]}_")

    with kpi_col2:
        stat_box(f"{bottom_row['ty_le_benh_tim']:.1f}%", "Tỷ lệ thấp nhất", "🟢", "#10b981")
        st.caption(f"_{bottom_row[selected_feature]}_")

    with kpi_col3:
        stat_box(f"{gap:.1f}%", "Chênh lệch", "📊", "#f59e0b")
        st.caption("_Cao nhất - Thấp nhất_")

    with kpi_col4:
        stat_box(f"{avg_rate:.1f}%", "Tỷ lệ trung bình", "📈", "#0e7490")
        st.caption("_Trung bình tất cả nhóm_")

    st.markdown("---")

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        st.info(f"""
        #### 🎯 Nhóm nguy cơ cao nhất

        **{top_row[selected_feature]}** có tỷ lệ bệnh tim cao nhất là **{top_row['ty_le_benh_tim']:.1f}%**
        với **{top_row['so_ho_so']:,}** hồ sơ trong tập dữ liệu.

        👉 Đây là nhóm cần ưu tiên sàng lọc và theo dõi sát sao.
        """)

    with insight_col2:
        st.success(f"""
        #### ✅ Nhóm nguy cơ thấp nhất

        **{bottom_row[selected_feature]}** có tỷ lệ bệnh tim thấp nhất là **{bottom_row['ty_le_benh_tim']:.1f}%**
        với **{bottom_row['so_ho_so']:,}** hồ sơ trong tập dữ liệu.

        👉 Chênh lệch **{gap:.1f} điểm phần trăm** so với nhóm cao nhất.
        """)

    st.markdown("#### 📊 Phân loại mức độ rủi ro")

    risk_classification = []
    for _, row in summary.iterrows():
        if row['ty_le_benh_tim'] >= avg_rate * 1.2:
            risk_level = "🔴 Cao"
            color = "#ef4444"
        elif row['ty_le_benh_tim'] >= avg_rate * 0.8:
            risk_level = "🟡 Trung bình"
            color = "#f59e0b"
        else:
            risk_level = "🟢 Thấp"
            color = "#10b981"

        risk_classification.append({
            'Nhóm': row[selected_feature],
            'Tỷ lệ bệnh tim (%)': row['ty_le_benh_tim'],
            'Số hồ sơ': row['so_ho_so'],
            'Mức độ rủi ro': risk_level
        })

    risk_df = pd.DataFrame(risk_classification).sort_values('Tỷ lệ bệnh tim (%)', ascending=False)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("💡 **Gợi ý:** Kết hợp phân tích nhiều chiều khác nhau để có cái nhìn toàn diện về nhóm nguy cơ!")
