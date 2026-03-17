import pandas as pd
import plotly.express as px
import streamlit as st

from utils.charts import iqr_outlier_count
from utils.data_loader import apply_common_filters, get_preprocessing_summary, load_data, load_raw_data
from utils.ui import TARGET_COLOR_MAP, apply_global_style, page_header, style_figure


raw_df = load_raw_data("heart.csv")
df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("Page 2 – Phân bố chỉ số sức khỏe", "Khám phá dữ liệu (EDA): phân phối dữ liệu, ngoại lệ và thống kê mô tả.")

if df.empty:
    st.warning("Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter.")
    st.stop()

st.subheader("Bước 1 – Xử lý dữ liệu trước khi EDA")
st.caption("Quy trình: đọc dữ liệu thô → chuẩn hóa kiểu dữ liệu → xử lý giá trị thiếu → loại bỏ trùng lặp → tạo biến phục vụ phân tích.")

with st.expander("Xem chi tiết trước/sau xử lý", expanded=True):
    summary_df = get_preprocessing_summary("heart.csv")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown("**Mẫu dữ liệu thô (5 dòng đầu)**")
    st.dataframe(raw_df.head(5), use_container_width=True)

    st.markdown("**Mẫu dữ liệu sau xử lý (5 dòng đầu)**")
    st.dataframe(df.head(5), use_container_width=True)

numeric_cols = ["age", "chol", "trestbps", "thalach", "oldpeak"]
c1, c2 = st.columns(2)
hist_col = c1.selectbox("Chọn biến cho Histogram", numeric_cols, index=1)
box_col = c2.selectbox("Chọn biến cho Boxplot", numeric_cols, index=4)

fig_hist = px.histogram(
    df,
    x=hist_col,
    nbins=30,
    color="target_label",
    barmode="overlay",
    opacity=0.75,
    color_discrete_map=TARGET_COLOR_MAP,
)
fig_hist = style_figure(fig_hist, f"Histogram: phân phối {hist_col}")
st.plotly_chart(fig_hist, use_container_width=True)

fig_box = px.box(
    df,
    y=box_col,
    x="target_label",
    color="target_label",
    points="outliers",
    color_discrete_map=TARGET_COLOR_MAP,
)
fig_box = style_figure(fig_box, f"Boxplot: {box_col} theo nhóm bệnh tim")
st.plotly_chart(fig_box, use_container_width=True)

st.subheader("PHẦN 2 – EDA")
st.caption("Nội dung gồm: dữ liệu thiếu, ngoại lệ, thống kê mô tả, lọc điều kiện, GroupBy/tổng hợp, Pivot Table và tương quan biến.")
t1, t2, t3, t4, t5 = st.tabs([
    "1) Thiếu dữ liệu & ngoại lệ",
    "2) Thống kê mô tả",
    "3) Lọc điều kiện + GroupBy",
    "4) Pivot Table",
    "5) Tương quan biến",
])

with t1:
    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Biến", "Số lượng thiếu"]
    missing_df["Tỷ lệ thiếu (%)"] = ((missing_df["Số lượng thiếu"] / len(df)) * 100).round(2)
    st.dataframe(missing_df, use_container_width=True, hide_index=True)

    outlier_df = pd.DataFrame({"Biến": numeric_cols, "Số ngoại lệ (IQR)": [iqr_outlier_count(df[col]) for col in numeric_cols]})
    st.dataframe(outlier_df, use_container_width=True, hide_index=True)
    st.caption("Các biến có số lượng ngoại lệ cao cần được lưu ý khi diễn giải kết quả.")

with t2:
    desc_df = df[numeric_cols].describe().T.round(2)
    st.dataframe(desc_df, use_container_width=True)

with t3:
    condition_df = df[(df["age"] > 60) & (df["target"] == 1)]
    st.write(f"Số hồ sơ thỏa điều kiện `age > 60` và `target = 1`: **{len(condition_df)}**")
    st.dataframe(condition_df.head(20), use_container_width=True)

    gb_cp = (
        df.groupby("cp_label")
        .agg(
            so_ho_so=("target", "size"),
            ty_le_benh_tim=("target", "mean"),
            tuoi_tb=("age", "mean"),
            chol_tb=("chol", "mean"),
        )
        .reset_index()
    )
    gb_cp["ty_le_benh_tim"] = (gb_cp["ty_le_benh_tim"] * 100).round(2)
    gb_cp[["tuoi_tb", "chol_tb"]] = gb_cp[["tuoi_tb", "chol_tb"]].round(2)
    st.dataframe(gb_cp, use_container_width=True)

with t4:
    st.write("Pivot tỷ lệ bệnh tim theo giới tính × loại đau ngực")
    pivot = pd.pivot_table(
        df,
        index="sex_label",
        columns="cp_label",
        values="target",
        aggfunc="mean",
        fill_value=0,
    )
    pivot = (pivot * 100).round(2)
    st.dataframe(pivot, use_container_width=True)

with t5:
    corr_cols = ["age", "trestbps", "chol", "thalach", "oldpeak", "ca", "target"]
    corr_df = df[corr_cols].corr(numeric_only=True).round(2)
    fig_corr = px.imshow(corr_df, text_auto=True, color_continuous_scale="RdBu", zmin=-1, zmax=1, title="Ma trận tương quan")
    fig_corr = style_figure(fig_corr)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.dataframe(corr_df, use_container_width=True)
