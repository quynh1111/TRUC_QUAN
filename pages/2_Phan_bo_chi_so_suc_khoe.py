import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.charts import iqr_outlier_count, create_violin_chart
from utils.data_loader import apply_common_filters, get_preprocessing_summary, load_data, load_raw_data
from utils.ui import TARGET_COLOR_MAP, apply_global_style, page_header, style_figure, divider_with_text, stat_box


raw_df = load_raw_data("heart.csv")
df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("🧪 Page 2 – Phân bố chỉ số sức khỏe", "Khám phá dữ liệu toàn diện (EDA): tiền xử lý, phân phối, ngoại lệ, thống kê mô tả và tương quan.")

if df.empty:
    st.warning("⚠️ Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter trên sidebar.")
    st.stop()

st.markdown("### 🔧 Bước 1 – Tiền xử lý dữ liệu")
st.caption("Quy trình: đọc dữ liệu thô → chuẩn hóa kiểu → xử lý thiếu → loại trùng lặp → tạo biến phân tích.")

with st.expander("📊 Xem chi tiết trước/sau xử lý", expanded=True):
    summary_df = get_preprocessing_summary("heart.csv")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        stat_box(f"{summary_df.loc[0, 'Trước xử lý']:,}", "Số dòng ban đầu", "📋", "#0e7490")
    with col2:
        stat_box(f"{summary_df.loc[2, 'Trước xử lý']}", "Dòng trùng lặp", "🔄", "#f59e0b")
    with col3:
        stat_box(f"{summary_df.loc[3, 'Trước xử lý']}", "Ô thiếu ban đầu", "❌", "#ef4444")
    with col4:
        stat_box(f"{summary_df.loc[0, 'Sau xử lý']:,}", "Số dòng cuối cùng", "✅", "#10b981")

    st.markdown("#### 📋 Bảng tóm tắt xử lý")
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    col_sample1, col_sample2 = st.columns(2)

    with col_sample1:
        st.markdown("**📄 Mẫu dữ liệu thô (5 dòng đầu)**")
        st.dataframe(raw_df.head(5), use_container_width=True)

    with col_sample2:
        st.markdown("**✨ Mẫu dữ liệu sau xử lý (5 dòng đầu)**")
        st.dataframe(df.head(5), use_container_width=True)

divider_with_text("PHÂN TÍCH PHÂN PHỐI")

st.markdown("### 📊 Phân tích phân phối biến liên tục")

numeric_cols = ["age", "chol", "trestbps", "thalach", "oldpeak"]
c1, c2 = st.columns(2)
hist_col = c1.selectbox("🔍 Chọn biến cho Histogram", numeric_cols, index=1, key="hist")
box_col = c2.selectbox("🔍 Chọn biến cho Boxplot", numeric_cols, index=4, key="box")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.markdown(f"#### 📊 Histogram: {hist_col}")
    fig_hist = px.histogram(
        df,
        x=hist_col,
        nbins=35,
        color="target_label",
        barmode="overlay",
        opacity=0.7,
        color_discrete_map=TARGET_COLOR_MAP,
        marginal="box",
    )

    fig_hist = style_figure(fig_hist, height=400)
    fig_hist.update_layout(
        xaxis_title=hist_col,
        yaxis_title="Tần suất",
        bargap=0.1,
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with viz_col2:
    st.markdown(f"#### 📦 Boxplot: {box_col}")
    fig_box = px.box(
        df,
        y=box_col,
        x="target_label",
        color="target_label",
        points="outliers",
        color_discrete_map=TARGET_COLOR_MAP,
        notched=True,
    )

    fig_box = style_figure(fig_box, height=400)
    fig_box.update_layout(
        xaxis_title="",
        yaxis_title=box_col,
        showlegend=False,
    )
    st.plotly_chart(fig_box, use_container_width=True)

viz_col3, viz_col4 = st.columns(2)

with viz_col3:
    st.markdown("#### 🎻 Violin Plot - Phân phối chi tiết")
    violin_var = st.selectbox("Chọn biến", numeric_cols, index=0, key="violin")

    fig_violin = create_violin_chart(df, "target_label", violin_var, "target_label", "")
    fig_violin = style_figure(fig_violin, height=400)
    fig_violin.update_layout(showlegend=False, xaxis_title="", yaxis_title=violin_var)
    st.plotly_chart(fig_violin, use_container_width=True)

with viz_col4:
    st.markdown("#### 📈 Density Plot - Mật độ phân phối")
    density_var = st.selectbox("Chọn biến", numeric_cols, index=2, key="density")

    fig_density = px.histogram(
        df,
        x=density_var,
        color="target_label",
        marginal="violin",
        color_discrete_map=TARGET_COLOR_MAP,
        nbins=30,
        opacity=0.6,
    )

    fig_density = style_figure(fig_density, height=400)
    fig_density.update_layout(barmode='overlay', xaxis_title=density_var, yaxis_title="Tần suất")
    st.plotly_chart(fig_density, use_container_width=True)

divider_with_text("PHÂN TÍCH CHI TIẾT EDA")

st.markdown("### 🔍 PHẦN 2 – EDA Chi tiết")
st.caption("Nội dung: dữ liệu thiếu, ngoại lệ, thống kê mô tả, lọc & GroupBy, Pivot Table, ma trận tương quan.")

t1, t2, t3, t4, t5 = st.tabs([
    "🔍 Thiếu & Ngoại lệ",
    "📊 Thống kê mô tả",
    "🎯 Lọc & GroupBy",
    "📋 Pivot Table",
    "🔗 Tương quan",
])

with t1:
    st.markdown("#### ❌ Dữ liệu thiếu")
    missing_df = df.isnull().sum().reset_index()
    missing_df.columns = ["Biến", "Số lượng thiếu"]
    missing_df["Tỷ lệ thiếu (%)"] = ((missing_df["Số lượng thiếu"] / len(df)) * 100).round(2)

    fig_missing = px.bar(
        missing_df[missing_df["Số lượng thiếu"] > 0],
        x="Biến",
        y="Số lượng thiếu",
        text="Tỷ lệ thiếu (%)",
        color="Tỷ lệ thiếu (%)",
        color_continuous_scale="Reds",
    )
    fig_missing = style_figure(fig_missing, "Phân bố dữ liệu thiếu theo biến")
    fig_missing.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig_missing, use_container_width=True)

    st.dataframe(missing_df, use_container_width=True, hide_index=True)

    st.markdown("#### 📊 Phát hiện ngoại lệ (IQR method)")
    outlier_df = pd.DataFrame({
        "Biến": numeric_cols,
        "Số ngoại lệ (IQR)": [iqr_outlier_count(df[col]) for col in numeric_cols],
        "Tỷ lệ ngoại lệ (%)": [(iqr_outlier_count(df[col]) / len(df) * 100) for col in numeric_cols]
    })
    outlier_df["Tỷ lệ ngoại lệ (%)"] = outlier_df["Tỷ lệ ngoại lệ (%)"].round(2)

    fig_outlier = px.bar(
        outlier_df,
        x="Biến",
        y="Số ngoại lệ (IQR)",
        text="Tỷ lệ ngoại lệ (%)",
        color="Số ngoại lệ (IQR)",
        color_continuous_scale="Oranges",
    )
    fig_outlier = style_figure(fig_outlier, "Số lượng ngoại lệ theo biến")
    fig_outlier.update_traces(texttemplate='%{text}%', textposition='outside')
    st.plotly_chart(fig_outlier, use_container_width=True)

    st.dataframe(outlier_df, use_container_width=True, hide_index=True)
    st.caption("⚠️ Các biến có số lượng ngoại lệ cao cần được lưu ý khi diễn giải kết quả.")

with t2:
    st.markdown("#### 📊 Thống kê mô tả toàn diện")
    desc_df = df[numeric_cols].describe().T.round(2)
    desc_df['range'] = desc_df['max'] - desc_df['min']
    desc_df['cv'] = (desc_df['std'] / desc_df['mean'] * 100).round(2)

    st.dataframe(desc_df, use_container_width=True)

    st.markdown("#### 📈 So sánh phân phối các biến")
    fig_box_multi = px.box(
        df[numeric_cols],
        y=numeric_cols[0],
        points="outliers",
        color_discrete_sequence=["#0e7490"],
    )

    for col in numeric_cols[1:]:
        fig_box_multi.add_trace(
            px.box(df, y=col, points="outliers").data[0]
        )

    # Normalize để so sánh dễ dàng
    normalized_data = pd.DataFrame()
    for col in numeric_cols:
        normalized_data[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    fig_normalize = px.box(
        normalized_data,
        y=numeric_cols,
        points=False,
        color_discrete_sequence=["#0e7490", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6"],
    )
    fig_normalize = style_figure(fig_normalize, "Phân phối chuẩn hóa (0-1) của các biến")
    st.plotly_chart(fig_normalize, use_container_width=True)

with t3:
    st.markdown("#### 🎯 Lọc điều kiện: age > 60 AND target = 1")
    condition_df = df[(df["age"] > 60) & (df["target"] == 1)]
    st.write(f"**Số hồ sơ thỏa điều kiện:** {len(condition_df):,} / {len(df):,} ({len(condition_df)/len(df)*100:.1f}%)")

    if not condition_df.empty:
        cond_col1, cond_col2 = st.columns(2)
        with cond_col1:
            st.dataframe(condition_df.head(10), use_container_width=True)
        with cond_col2:
            stats = condition_df[numeric_cols].mean().round(2)
            st.markdown("**📊 Thống kê trung bình nhóm này:**")
            for idx, val in stats.items():
                st.write(f"- {idx}: **{val}**")

    st.markdown("#### 👥 GroupBy theo loại đau ngực")
    gb_cp = (
        df.groupby("cp_label")
        .agg(
            so_ho_so=("target", "size"),
            ty_le_benh_tim=("target", "mean"),
            tuoi_tb=("age", "mean"),
            chol_tb=("chol", "mean"),
            trestbps_tb=("trestbps", "mean"),
            thalach_tb=("thalach", "mean"),
        )
        .reset_index()
    )
    gb_cp["ty_le_benh_tim"] = (gb_cp["ty_le_benh_tim"] * 100).round(2)
    gb_cp[["tuoi_tb", "chol_tb", "trestbps_tb", "thalach_tb"]] = gb_cp[["tuoi_tb", "chol_tb", "trestbps_tb", "thalach_tb"]].round(2)

    st.dataframe(gb_cp, use_container_width=True)

    fig_gb = px.bar(
        gb_cp,
        x="cp_label",
        y=["tuoi_tb", "chol_tb", "trestbps_tb", "thalach_tb"],
        barmode="group",
        title="So sánh các chỉ số trung bình theo loại đau ngực",
    )
    fig_gb = style_figure(fig_gb)
    st.plotly_chart(fig_gb, use_container_width=True)

with t4:
    st.markdown("#### 📋 Pivot Table: Giới tính × Loại đau ngực")
    st.write("**Tỷ lệ bệnh tim (%)**")

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

    # Heatmap
    fig_heatmap = px.imshow(
        pivot,
        text_auto=True,
        color_continuous_scale="RdYlGn_r",
        aspect="auto",
        labels=dict(color="Tỷ lệ bệnh tim (%)"),
    )
    fig_heatmap = style_figure(fig_heatmap, "Heatmap: Tỷ lệ bệnh tim theo giới tính và loại đau ngực")
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("#### 📊 Pivot Table: Nhóm tuổi × Giới tính")
    pivot2 = pd.pivot_table(
        df,
        index="age_group",
        columns="sex_label",
        values="target",
        aggfunc=["mean", "size"],
        fill_value=0,
    )

    st.write("**Tỷ lệ bệnh tim (%)**")
    pivot2_mean = pivot2["mean"] * 100
    st.dataframe(pivot2_mean.round(2), use_container_width=True)

    st.write("**Số lượng hồ sơ**")
    st.dataframe(pivot2["size"], use_container_width=True)

with t5:
    st.markdown("#### 🔗 Ma trận tương quan")
    corr_cols = ["age", "trestbps", "chol", "thalach", "oldpeak", "ca", "target"]
    corr_df = df[corr_cols].corr(numeric_only=True).round(2)

    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        aspect="auto",
    )
    fig_corr = style_figure(fig_corr, "Ma trận tương quan Pearson", height=500)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.dataframe(corr_df, use_container_width=True)

    st.markdown("#### 🔍 Top 10 cặp biến có tương quan cao nhất")
    corr_pairs = []
    for i in range(len(corr_df.columns)):
        for j in range(i+1, len(corr_df.columns)):
            corr_pairs.append({
                'Biến 1': corr_df.columns[i],
                'Biến 2': corr_df.columns[j],
                'Tương quan': corr_df.iloc[i, j]
            })

    corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('Tương quan', key=abs, ascending=False).head(10)
    st.dataframe(corr_pairs_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("💡 **Insight:** Sử dụng các biểu đồ phân phối để phát hiện pattern và outliers trong dữ liệu!")
