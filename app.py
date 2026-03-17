import streamlit as st
from utils.data_loader import load_data
from utils.ui import apply_global_style, hero_banner, info_card, page_header

st.set_page_config(page_title="Heart Disease Dashboard", page_icon="🫀", layout="wide", initial_sidebar_state="expanded")
apply_global_style()

page_header(
    "Dashboard Phân Tích Bệnh Tim",
    "Bộ dashboard gồm 5 trang phân tích chi tiết về bệnh tim dựa trên tập dữ liệu đã lọc. Sử dụng menu bên trái để điều hướng.",
)
hero_banner(
    "Hệ thống dashboard 5 trang cho đề tài Heart Disease",
    "Quy trình phân tích: xử lý dữ liệu → EDA → trực quan hóa → đề xuất hành động.",
)

df = load_data("heart.csv")

c1, c2, c3 = st.columns(3)
c1.metric("Tổng số hồ sơ", f"{len(df):,}")
c2.metric("Tỷ lệ có bệnh tim", f"{df['target'].mean() * 100:.1f}%")
c3.metric("Số biến gốc", "14")
st.markdown("<div class='kpi-note'>Dùng menu bên trái để mở từng page phân tích chi tiết.</div>", unsafe_allow_html=True)

st.subheader("Điều hướng")
left, right = st.columns([1, 1])

with left:
    info_card("Page 1 – Tổng quan", "KPI chính, cơ cấu bệnh tim, tổng hợp theo giới tính và nhóm tuổi.")
    st.page_link("pages/1_Tong_quan_benh_tim.py", label="Mở Page 1", icon="📊")

    info_card("Page 2 – Khám phá dữ liệu (EDA)", "Xử lý dữ liệu trước/sau, thiếu dữ liệu, ngoại lệ, thống kê mô tả, GroupBy, Pivot Table, tương quan.")
    st.page_link("pages/2_Phan_bo_chi_so_suc_khoe.py", label="Mở Page 2", icon="🧪")

    info_card("Page 3 – Nhóm nguy cơ", "So sánh tỷ lệ bệnh tim theo nhóm, stacked chart và khoảng tin cậy 95%.")
    st.page_link("pages/3_So_sanh_nhom_nguy_co.py", label="Mở Page 3", icon="📈")

with right:
    info_card("Page 4 – Yếu tố liên quan", "Top N yếu tố, scatter so sánh 2 nhóm, pivot và odds ratio biến nhị phân.")
    st.page_link("pages/4_Top_yeu_to_lien_quan.py", label="Mở Page 4", icon="🧠")

    info_card("Page 5 – Insight", "Xu hướng theo nhóm tuổi, benchmark chỉ số và ma trận ưu tiên hành động.")
    st.page_link("pages/5_Tuong_tac_va_insight.py", label="Mở Page 5", icon="✅")

    
