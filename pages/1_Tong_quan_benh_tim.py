import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import VARIABLE_DESCRIPTIONS, apply_common_filters, load_data
from utils.ui import TARGET_COLOR_MAP, apply_global_style, page_header, style_figure


df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("Page 1 – Tổng quan bệnh tim", "Tóm tắt chỉ số trọng yếu và cơ cấu bệnh tim trên tập dữ liệu đã lọc.")

if df.empty:
    st.warning("Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tổng số hồ sơ", f"{len(df):,}")
c2.metric("Tỷ lệ có bệnh tim", f"{df['target'].mean() * 100:.1f}%")
c3.metric("Tuổi trung bình", f"{df['age'].mean():.1f}")
c4.metric("Cholesterol TB", f"{df['chol'].mean():.1f}")
st.markdown("<div class='kpi-note'>KPI cập nhật tự động theo bộ lọc ở sidebar.</div>", unsafe_allow_html=True)

left, right = st.columns([1.1, 1])
with left:
    st.subheader("Cơ cấu bệnh tim")
    pie_df = df["target_label"].value_counts().reset_index()
    pie_df.columns = ["target_label", "count"]
    fig_pie = px.pie(
        pie_df,
        names="target_label",
        values="count",
        hole=0.45,
        color="target_label",
        color_discrete_map=TARGET_COLOR_MAP,
    )
    fig_pie = style_figure(fig_pie)
    st.plotly_chart(fig_pie, use_container_width=True)

with right:
    st.subheader("GroupBy theo giới tính")
    gb = (
        df.groupby("sex_label")
        .agg(
            so_ho_so=("target", "size"),
            ty_le_benh_tim=("target", "mean"),
            tuoi_tb=("age", "mean"),
            chol_tb=("chol", "mean"),
        )
        .reset_index()
    )
    gb["ty_le_benh_tim"] = (gb["ty_le_benh_tim"] * 100).round(2)
    st.dataframe(gb, use_container_width=True)
    if not gb.empty:
        top_group = gb.sort_values("ty_le_benh_tim", ascending=False).iloc[0]
        st.caption(f"Nhóm có tỷ lệ bệnh tim cao hơn: {top_group['sex_label']} ({top_group['ty_le_benh_tim']:.1f}%).")

st.subheader("Phân tích tổng quan mở rộng")
e1, e2 = st.columns(2)

with e1:
    age_summary = (
        df.groupby("age_group", observed=False)
        .agg(so_ho_so=("target", "size"), ty_le_benh_tim=("target", "mean"))
        .reset_index()
    )
    age_summary["ty_le_benh_tim"] = (age_summary["ty_le_benh_tim"] * 100).round(2)
    fig_age = px.line(age_summary, x="age_group", y="ty_le_benh_tim", markers=True, title="Tỷ lệ bệnh tim theo nhóm tuổi")
    fig_age = style_figure(fig_age)
    st.plotly_chart(fig_age, use_container_width=True)

with e2:
    cp_summary = (
        df.groupby("cp_label")
        .agg(so_ho_so=("target", "size"), ty_le_benh_tim=("target", "mean"))
        .reset_index()
    )
    cp_summary["ty_le_benh_tim"] = (cp_summary["ty_le_benh_tim"] * 100).round(2)
    fig_cp = px.bar(
        cp_summary.sort_values("ty_le_benh_tim", ascending=False),
        x="ty_le_benh_tim",
        y="cp_label",
        orientation="h",
        text="ty_le_benh_tim",
        title="Xếp hạng tỷ lệ bệnh tim theo loại đau ngực",
    )
    fig_cp.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_cp = style_figure(fig_cp)
    st.plotly_chart(fig_cp, use_container_width=True)

st.subheader("PHẦN 1 – Mô tả dữ liệu")
d1, d2 = st.columns([1, 1.2])
with d1:
    st.write(f"- Số dòng: **{len(df):,}**")
    st.write(f"- Số cột: **{df.shape[1]}**")
    st.write("- Nguồn: Heart Disease Dataset (Kaggle)")

with d2:
    dtype_df = pd.DataFrame({"Biến": df.columns, "Kiểu dữ liệu": df.dtypes.astype(str).values})
    st.dataframe(dtype_df, use_container_width=True, hide_index=True)

var_desc_df = pd.DataFrame({"Biến": list(VARIABLE_DESCRIPTIONS.keys()), "Ý nghĩa": list(VARIABLE_DESCRIPTIONS.values())})
st.dataframe(var_desc_df, use_container_width=True, hide_index=True)
