import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import VARIABLE_DESCRIPTIONS, apply_common_filters, load_data
from utils.ui import TARGET_COLOR_MAP, AGE_GROUP_ORDER, apply_global_style, page_header, style_figure, divider_with_text, stat_box
from utils.charts import create_gauge_chart, create_radar_chart


df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("📊 Page 1 – Tổng quan bệnh tim", "Tóm tắt các chỉ số trọng yếu, phân tích cơ cấu bệnh tim và tổng hợp đa chiều trên tập dữ liệu đã lọc.")

if df.empty:
    st.warning("⚠️ Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter trên sidebar.")
    st.stop()

st.markdown("### 📈 KPI Chính")
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    stat_box(f"{len(df):,}", "Tổng hồ sơ", "📋", "#0e7490")

with c2:
    disease_rate = df['target'].mean() * 100
    stat_box(f"{disease_rate:.1f}%", "Tỷ lệ bệnh tim", "❤️", "#ef4444")

with c3:
    stat_box(f"{df['age'].mean():.1f}", "Tuổi TB", "👤", "#10b981")

with c4:
    stat_box(f"{df['chol'].mean():.0f}", "Cholesterol TB", "🩺", "#f59e0b")

with c5:
    stat_box(f"{df['thalach'].mean():.0f}", "Nhịp tim TB", "💓", "#8b5cf6")

st.markdown("<div class='kpi-note'>📊 KPI cập nhật tự động theo bộ lọc ở sidebar.</div>", unsafe_allow_html=True)

divider_with_text("PHÂN TÍCH CƠ CẤU")

left, right = st.columns([1.2, 1])

with left:
    st.markdown("#### 🎯 Cơ cấu bệnh tim (Donut Chart)")
    pie_df = df["target_label"].value_counts().reset_index()
    pie_df.columns = ["target_label", "count"]
    pie_df['percent'] = (pie_df['count'] / pie_df['count'].sum() * 100).round(1)

    fig_pie = px.pie(
        pie_df,
        names="target_label",
        values="count",
        hole=0.5,
        color="target_label",
        color_discrete_map=TARGET_COLOR_MAP,
    )

    fig_pie.update_traces(
        textposition='inside',
        textinfo='label+percent',
        textfont_size=14,
        marker=dict(line=dict(color='white', width=3)),
        hovertemplate="<b>%{label}</b><br>Số lượng: %{value}<br>Tỷ lệ: %{percent}<extra></extra>"
    )

    fig_pie = style_figure(fig_pie, height=350)
    fig_pie.update_layout(showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

    for _, row in pie_df.iterrows():
        badge_type = "danger" if "Có" in row["target_label"] else "info"
        st.markdown(f"<span class='{badge_type}-badge'>{row['target_label']}: {row['count']} ({row['percent']:.1f}%)</span>", unsafe_allow_html=True)

with right:
    st.markdown("#### 📊 Tỷ lệ bệnh tim (Gauge)")
    gauge_fig = create_gauge_chart(disease_rate, "", max_value=100, color="#ef4444")
    st.plotly_chart(gauge_fig, use_container_width=True)

    if disease_rate < 40:
        st.success("✅ Tỷ lệ bệnh tim ở mức thấp trong tập dữ liệu này.")
    elif disease_rate < 60:
        st.warning("⚠️ Tỷ lệ bệnh tim ở mức trung bình, cần theo dõi.")
    else:
        st.error("🚨 Tỷ lệ bệnh tim cao, cần có biện pháp can thiệp.")

divider_with_text("PHÂN TÍCH THEO NHÓM GIỚI TÍNH")

gb_col1, gb_col2 = st.columns([1, 1.2])

with gb_col1:
    st.markdown("#### 👥 GroupBy theo giới tính")
    gb = (
        df.groupby("sex_label")
        .agg(
            so_ho_so=("target", "size"),
            ty_le_benh_tim=("target", "mean"),
            tuoi_tb=("age", "mean"),
            chol_tb=("chol", "mean"),
            thalach_tb=("thalach", "mean"),
        )
        .reset_index()
    )
    gb["ty_le_benh_tim"] = (gb["ty_le_benh_tim"] * 100).round(2)
    gb[["tuoi_tb", "chol_tb", "thalach_tb"]] = gb[["tuoi_tb", "chol_tb", "thalach_tb"]].round(1)

    st.dataframe(gb, use_container_width=True, hide_index=True)

    if not gb.empty:
        top_group = gb.sort_values("ty_le_benh_tim", ascending=False).iloc[0]
        st.info(f"🔍 **Nhóm có tỷ lệ bệnh tim cao hơn:** {top_group['sex_label']} ({top_group['ty_le_benh_tim']:.1f}%)")

with gb_col2:
    st.markdown("#### 📊 So sánh giữa các giới tính")
    gender_comp = df.groupby(['sex_label', 'target_label']).size().unstack(fill_value=0).reset_index()
    gender_comp_melted = gender_comp.melt(id_vars='sex_label', var_name='target_label', value_name='count')

    fig_gender = px.bar(
        gender_comp_melted,
        x='sex_label',
        y='count',
        color='target_label',
        barmode='group',
        color_discrete_map=TARGET_COLOR_MAP,
        text='count',
    )

    fig_gender.update_traces(textposition='outside', textfont_size=12)
    fig_gender = style_figure(fig_gender, "Phân bố bệnh tim theo giới tính", height=350)
    fig_gender.update_layout(xaxis_title="Giới tính", yaxis_title="Số lượng")
    st.plotly_chart(fig_gender, use_container_width=True)

divider_with_text("PHÂN TÍCH MỞ RỘNG")

st.markdown("### 🔍 Phân tích tổng quan mở rộng")

e1, e2 = st.columns(2)

with e1:
    st.markdown("#### 📊 Tỷ lệ bệnh tim theo nhóm tuổi")
    age_summary = (
        df.groupby("age_group", observed=False)
        .agg(so_ho_so=("target", "size"), ty_le_benh_tim=("target", "mean"))
        .reset_index()
    )
    age_summary["ty_le_benh_tim"] = (age_summary["ty_le_benh_tim"] * 100).round(2)
    age_summary = age_summary.sort_values("age_group")

    fig_age = px.line(
        age_summary,
        x="age_group",
        y="ty_le_benh_tim",
        markers=True,
        text="ty_le_benh_tim",
    )

    fig_age.update_traces(
        line=dict(color='#ef4444', width=3),
        marker=dict(size=12, symbol='circle', line=dict(width=2, color='white')),
        textposition='top center',
        texttemplate='%{text:.1f}%',
        textfont_size=11,
    )

    fig_age.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
    fig_age = style_figure(fig_age, height=350)
    fig_age.update_layout(xaxis_title="Nhóm tuổi", yaxis_title="Tỷ lệ bệnh tim (%)")
    st.plotly_chart(fig_age, use_container_width=True)

with e2:
    st.markdown("#### 📊 Tỷ lệ bệnh tim theo loại đau ngực")
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
        color="ty_le_benh_tim",
        color_continuous_scale="Reds",
    )

    fig_cp.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont_size=12,
    )

    fig_cp = style_figure(fig_cp, height=350)
    fig_cp.update_layout(
        xaxis_title="Tỷ lệ bệnh tim (%)",
        yaxis_title="",
        showlegend=False,
    )
    st.plotly_chart(fig_cp, use_container_width=True)

e3, e4 = st.columns(2)

with e3:
    st.markdown("#### 🎯 Radar Chart - So sánh chỉ số trung bình")

    metrics = ['age', 'trestbps', 'chol', 'thalach']
    categories = ['Tuổi', 'Huyết áp', 'Cholesterol', 'Nhịp tim']

    no_disease = df[df['target'] == 0][metrics].mean().values
    has_disease = df[df['target'] == 1][metrics].mean().values

    # Normalize để dễ so sánh
    no_disease_norm = (no_disease / no_disease.max() * 100).tolist()
    has_disease_norm = (has_disease / has_disease.max() * 100).tolist()

    radar_fig = create_radar_chart(
        categories,
        {
            "Không bệnh tim": no_disease_norm,
            "Có bệnh tim": has_disease_norm
        },
        ""
    )

    st.plotly_chart(radar_fig, use_container_width=True)

with e4:
    st.markdown("#### 📈 Phân bố tuổi theo tình trạng bệnh")

    fig_violin = px.violin(
        df,
        x="target_label",
        y="age",
        color="target_label",
        box=True,
        points="outliers",
        color_discrete_map=TARGET_COLOR_MAP,
    )

    fig_violin = style_figure(fig_violin, height=350)
    fig_violin.update_layout(
        xaxis_title="",
        yaxis_title="Tuổi",
        showlegend=False,
    )
    st.plotly_chart(fig_violin, use_container_width=True)

divider_with_text("MÔ TẢ DỮ LIỆU")

st.markdown("### 📋 PHẦN 1 – Mô tả dữ liệu")

d1, d2 = st.columns([1, 1.2])

with d1:
    st.markdown("#### 📊 Thông tin tổng quan")
    st.write(f"- **Số dòng:** {len(df):,}")
    st.write(f"- **Số cột:** {df.shape[1]}")
    st.write(f"- **Nguồn:** Heart Disease Dataset (Kaggle)")
    st.write(f"- **Số biến số:** {df.select_dtypes(include=['number']).shape[1]}")
    st.write(f"- **Số biến phân loại:** {df.select_dtypes(include=['object', 'category']).shape[1]}")

with d2:
    st.markdown("#### 🔢 Kiểu dữ liệu các biến")
    dtype_df = pd.DataFrame({
        "Biến": df.columns,
        "Kiểu dữ liệu": df.dtypes.astype(str).values
    })
    st.dataframe(dtype_df, use_container_width=True, hide_index=True, height=250)

st.markdown("#### 📖 Ý nghĩa các biến")
var_desc_df = pd.DataFrame({
    "Biến": list(VARIABLE_DESCRIPTIONS.keys()),
    "Ý nghĩa": list(VARIABLE_DESCRIPTIONS.values())
})
st.dataframe(var_desc_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("💡 **Tip:** Sử dụng bộ lọc trên sidebar để khám phá các insights khác nhau!")
