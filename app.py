import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.ui import apply_global_style, hero_banner, info_card, page_header, divider_with_text, stat_box
from utils.charts import create_gauge_chart

st.set_page_config(page_title="Heart Disease Dashboard", page_icon="🫀", layout="wide", initial_sidebar_state="expanded")
apply_global_style()

page_header(
    "🫀 Dashboard Phân Tích Bệnh Tim",
    "Hệ thống dashboard tích hợp 5 trang phân tích chuyên sâu về bệnh tim dựa trên tập dữ liệu đã được tiền xử lý và làm sạch.",
)
hero_banner(
    "Hệ thống Dashboard 5 Trang Phân Tích Heart Disease",
    "Quy trình phân tích toàn diện: Tiền xử lý dữ liệu → Khám phá EDA → Trực quan hóa đa chiều → Phân tích nhóm nguy cơ → Đề xuất hành động dựa trên insight.",
)

df = load_data("heart.csv")

st.markdown("### 📊 Thống Kê Tổng Quan")
c1, c2, c3, c4 = st.columns(4)

with c1:
    stat_box(f"{len(df):,}", "Tổng số hồ sơ", "📋", "#0e7490")

with c2:
    disease_rate = df['target'].mean() * 100
    stat_box(f"{disease_rate:.1f}%", "Tỷ lệ có bệnh tim", "❤️", "#ef4444")

with c3:
    stat_box("14", "Số biến gốc", "🔢", "#10b981")

with c4:
    stat_box(f"{df['age'].mean():.1f}", "Tuổi trung bình", "👤", "#f59e0b")

st.markdown("<div class='kpi-note'>💡 Dùng menu bên trái để khám phá từng page phân tích chi tiết.</div>", unsafe_allow_html=True)

divider_with_text("PREVIEW DỮ LIỆU")

preview_col1, preview_col2 = st.columns(2)

with preview_col1:
    st.markdown("#### 📈 Phân phối bệnh tim")
    pie_data = df['target_label'].value_counts().reset_index()
    pie_data.columns = ['Trạng thái', 'Số lượng']
    fig_pie = px.pie(
        pie_data,
        names='Trạng thái',
        values='Số lượng',
        hole=0.5,
        color='Trạng thái',
        color_discrete_map={"Không bệnh tim": "#0ea5e9", "Có bệnh tim": "#ef4444"},
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=13,
        marker=dict(line=dict(color='white', width=2))
    )
    fig_pie.update_layout(
        showlegend=False,
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        font={'family': 'Inter', 'color': '#334155'}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with preview_col2:
    st.markdown("#### 🎯 Tỷ lệ bệnh tim")
    gauge_fig = create_gauge_chart(disease_rate, "", max_value=100, color="#ef4444")
    st.plotly_chart(gauge_fig, use_container_width=True)

preview_col3, preview_col4 = st.columns(2)

with preview_col3:
    st.markdown("#### 👥 Phân bố theo giới tính")
    gender_data = df.groupby(['sex_label', 'target_label']).size().reset_index(name='count')
    fig_gender = px.bar(
        gender_data,
        x='sex_label',
        y='count',
        color='target_label',
        barmode='group',
        color_discrete_map={"Không bệnh tim": "#0ea5e9", "Có bệnh tim": "#ef4444"},
        text='count',
    )
    fig_gender.update_traces(textposition='outside', textfont_size=11)
    fig_gender.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="rgba(248, 250, 252, 0.4)",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        xaxis_title="",
        yaxis_title="Số lượng",
        font={'family': 'Inter', 'color': '#334155'}
    )
    fig_gender.update_xaxes(showgrid=False, linecolor="#e2e8f0")
    fig_gender.update_yaxes(gridcolor="#e5e7eb", linecolor="#e2e8f0")
    st.plotly_chart(fig_gender, use_container_width=True)

with preview_col4:
    st.markdown("#### 📊 Phân bố theo nhóm tuổi")
    age_data = df.groupby('age_group', observed=False).size().reset_index(name='count')
    age_data = age_data.sort_values('age_group')
    fig_age = px.bar(
        age_data,
        x='age_group',
        y='count',
        text='count',
        color='count',
        color_continuous_scale='Blues',
    )
    fig_age.update_traces(textposition='outside', textfont_size=11)
    fig_age.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="rgba(248, 250, 252, 0.4)",
        showlegend=False,
        xaxis_title="Nhóm tuổi",
        yaxis_title="Số lượng",
        font={'family': 'Inter', 'color': '#334155'}
    )
    fig_age.update_xaxes(showgrid=False, linecolor="#e2e8f0")
    fig_age.update_yaxes(gridcolor="#e5e7eb", linecolor="#e2e8f0")
    st.plotly_chart(fig_age, use_container_width=True)

divider_with_text("ĐIỀU HƯỚNG CÁC PAGE PHÂN TÍCH")

st.markdown("### 🗺️ Khám Phá 5 Page Phân Tích")

left, right = st.columns([1, 1])

with left:
    info_card("📊 Page 1 – Tổng quan", "Khám phá các KPI chính, cơ cấu bệnh tim theo nhóm, tổng hợp theo giới tính và phân tích nhóm tuổi chi tiết.")
    st.page_link("pages/1_Tong_quan_benh_tim.py", label="🚀 Mở Page 1 - Tổng Quan", icon="📊")
    st.markdown("")

    info_card("🧪 Page 2 – Khám phá dữ liệu (EDA)", "Phân tích tiền xử lý dữ liệu, phát hiện thiếu dữ liệu & ngoại lệ, thống kê mô tả, GroupBy, Pivot Table và ma trận tương quan.")
    st.page_link("pages/2_Phan_bo_chi_so_suc_khoe.py", label="🚀 Mở Page 2 - EDA", icon="🧪")
    st.markdown("")

    info_card("📈 Page 3 – Nhóm nguy cơ", "So sánh tỷ lệ bệnh tim giữa các nhóm, biểu đồ stacked phân tầng và khoảng tin cậy 95% cho từng nhóm.")
    st.page_link("pages/3_So_sanh_nhom_nguy_co.py", label="🚀 Mở Page 3 - Nhóm Nguy Cơ", icon="📈")

with right:
    info_card("🧠 Page 4 – Yếu tố liên quan", "Xếp hạng Top N yếu tố quan trọng, scatter plot so sánh 2 nhóm, pivot table đa chiều và phân tích odds ratio cho biến nhị phân.")
    st.page_link("pages/4_Top_yeu_to_lien_quan.py", label="🚀 Mở Page 4 - Yếu Tố", icon="🧠")
    st.markdown("")

    info_card("✅ Page 5 – Insight & Hành động", "Phân tích xu hướng theo nhóm tuổi, benchmark các chỉ số sức khỏe và ma trận ưu tiên hành động dựa trên insight.")
    st.page_link("pages/5_Tuong_tac_va_insight.py", label="🚀 Mở Page 5 - Insights", icon="✅")
    st.markdown("")

    st.info("💡 **Mẹo:** Sử dụng bộ lọc trên sidebar của mỗi page để điều chỉnh phạm vi phân tích theo nhu cầu của bạn!")

st.markdown("---")
st.caption("♥️ Dashboard được xây dựng bằng Streamlit & Plotly | © 2026 Heart Disease Analysis Team")

