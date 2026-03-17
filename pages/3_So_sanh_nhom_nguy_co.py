import plotly.express as px
import streamlit as st
import numpy as np

from utils.data_loader import apply_common_filters, load_data
from utils.ui import AGE_GROUP_ORDER, TARGET_COLOR_MAP, apply_global_style, page_header, style_figure


df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("Page 3 – So sánh nhóm nguy cơ", "So sánh tỷ lệ bệnh tim giữa các nhóm nhằm nhận diện phân khúc rủi ro.")

if df.empty:
    st.warning("Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter.")
    st.stop()

feature_map = {
    "Giới tính": "sex_label",
    "Loại đau ngực": "cp_label",
    "Đau thắt ngực khi gắng sức": "exang_label",
    "Đường huyết lúc đói": "fbs_label",
    "Nhóm tuổi": "age_group",
}

selected_feature_name = st.selectbox("Chọn chiều phân tích", list(feature_map.keys()))
selected_feature = feature_map[selected_feature_name]

category_options = [str(v) for v in df[selected_feature].dropna().unique().tolist()]
selected_categories = st.multiselect("Chọn nhiều nhóm để so sánh", category_options, default=category_options)

compare_df = df[df[selected_feature].astype(str).isin(selected_categories)].copy()
summary = (
    compare_df.groupby(selected_feature)
    .agg(so_ho_so=("target", "size"), ty_le_benh_tim=("target", "mean"))
    .reset_index()
)
summary["ty_le_benh_tim"] = (summary["ty_le_benh_tim"] * 100).round(2)

fig_bar = px.bar(summary, x=selected_feature, y="ty_le_benh_tim", text="ty_le_benh_tim", title="So sánh tỷ lệ bệnh tim giữa các nhóm")
fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
if selected_feature == "age_group":
    fig_bar.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
fig_bar = style_figure(fig_bar)
st.plotly_chart(fig_bar, use_container_width=True)

stacked = compare_df.groupby([selected_feature, "target_label"]).size().reset_index(name="count")
fig_stacked = px.bar(
    stacked,
    x=selected_feature,
    y="count",
    color="target_label",
    barmode="stack",
    title="Biểu đồ tổng hợp (stacked)",
    color_discrete_map=TARGET_COLOR_MAP,
)
if selected_feature == "age_group":
    fig_stacked.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
fig_stacked = style_figure(fig_stacked)
st.plotly_chart(fig_stacked, use_container_width=True)

st.dataframe(summary, use_container_width=True)

detail = summary.copy()
if not detail.empty:
    p = detail["ty_le_benh_tim"] / 100
    n = detail["so_ho_so"].clip(lower=1)
    ci = 1.96 * np.sqrt((p * (1 - p)) / n)
    detail["CI thấp (95%)"] = ((p - ci).clip(lower=0) * 100).round(2)
    detail["CI cao (95%)"] = ((p + ci).clip(upper=1) * 100).round(2)
    st.caption("Bảng chi tiết tỷ lệ bệnh tim và khoảng tin cậy 95% theo từng nhóm đối tượng.")
    st.dataframe(detail, use_container_width=True)

normalized = stacked.copy()
totals = normalized.groupby(selected_feature)["count"].transform("sum")
normalized["percent"] = (normalized["count"] / totals * 100).round(2)
fig_norm = px.bar(
    normalized,
    x=selected_feature,
    y="percent",
    color="target_label",
    barmode="stack",
    title="Biểu đồ tổng hợp tỷ lệ 100% theo nhóm",
    color_discrete_map=TARGET_COLOR_MAP,
)
if selected_feature == "age_group":
    fig_norm.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
fig_norm = style_figure(fig_norm)
st.plotly_chart(fig_norm, use_container_width=True)

if not summary.empty:
    top_row = summary.sort_values("ty_le_benh_tim", ascending=False).iloc[0]
    bottom_row = summary.sort_values("ty_le_benh_tim", ascending=True).iloc[0]
    gap = top_row["ty_le_benh_tim"] - bottom_row["ty_le_benh_tim"]
    st.info(f"Nhóm nổi bật: **{top_row[selected_feature]}** có tỷ lệ bệnh tim cao nhất khoảng **{top_row['ty_le_benh_tim']:.1f}%**.")
    st.caption(f"Chênh lệch giữa nhóm cao nhất và thấp nhất: {gap:.1f} điểm phần trăm.")
