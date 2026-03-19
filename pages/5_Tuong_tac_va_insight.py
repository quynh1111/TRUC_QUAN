import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import apply_common_filters, load_data
from utils.ui import AGE_GROUP_ORDER, TARGET_COLOR_MAP, apply_global_style, page_header, style_figure, divider_with_text, stat_box, info_badge
from utils.charts import create_gauge_chart, create_radar_chart


df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("✅ Page 5 – Tương tác và nhận định", "Tổng hợp xu hướng rủi ro, benchmark các chỉ số và đề xuất hành động dựa trên insight.")

if df.empty:
    st.warning("⚠️ Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter trên sidebar.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["📊 Xu hướng nhóm tuổi", "💡 Nhận định chính", "🎯 Khuyến nghị", "📈 Dashboard tổng hợp"])

with tab1:
    st.markdown("### 📊 Phân tích xu hướng theo nhóm tuổi")

    age_trend = (
        df.groupby("age_group", observed=False)
        .agg(
            so_ho_so=("target", "size"),
            ty_le_benh_tim=("target", "mean"),
            tuoi_tb=("age", "mean"),
            oldpeak_tb=("oldpeak", "mean"),
            thalach_tb=("thalach", "mean"),
            chol_tb=("chol", "mean"),
        )
        .reset_index()
        .sort_values("age_group")
    )
    age_trend["ty_le_benh_tim"] = age_trend["ty_le_benh_tim"] * 100

    trend_col1, trend_col2 = st.columns(2)

    with trend_col1:
        st.markdown("#### 📈 Xu hướng tỷ lệ bệnh tim")

        fig_line = px.line(
            age_trend,
            x="age_group",
            y="ty_le_benh_tim",
            markers=True,
            text="ty_le_benh_tim",
        )

        fig_line.update_traces(
            line=dict(color='#ef4444', width=4),
            marker=dict(size=14, symbol='circle', line=dict(width=3, color='white')),
            textposition='top center',
            texttemplate='%{text:.1f}%',
            textfont_size=12,
        )

        fig_line.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
        fig_line = style_figure(fig_line, height=400)
        fig_line.update_layout(
            xaxis_title="Nhóm tuổi",
            yaxis_title="Tỷ lệ bệnh tim (%)"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with trend_col2:
        st.markdown("#### 📊 Quy mô mẫu theo nhóm tuổi")

        fig_bar = px.bar(
            age_trend,
            x="age_group",
            y="so_ho_so",
            text="so_ho_so",
            color="so_ho_so",
            color_continuous_scale="Blues",
        )

        fig_bar.update_traces(textposition='outside', textfont_size=13)
        fig_bar.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
        fig_bar = style_figure(fig_bar, height=400)
        fig_bar.update_layout(
            xaxis_title="Nhóm tuổi",
            yaxis_title="Số lượng hồ sơ",
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### 📋 Bảng chuẩn tham chiếu (Benchmark)")
    st.caption("Các chỉ số trung bình theo từng nhóm tuổi để hỗ trợ diễn giải kết quả")

    benchmark = age_trend.copy()
    benchmark["ty_le_benh_tim"] = benchmark["ty_le_benh_tim"].round(2)
    benchmark[["tuoi_tb", "oldpeak_tb", "thalach_tb", "chol_tb"]] = benchmark[
        ["tuoi_tb", "oldpeak_tb", "thalach_tb", "chol_tb"]
    ].round(2)

    st.dataframe(benchmark, use_container_width=True, hide_index=True)

    st.markdown("#### 🎯 Heatmap: Chỉ số theo nhóm tuổi")

    heatmap_data = benchmark.set_index("age_group")[["ty_le_benh_tim", "oldpeak_tb", "thalach_tb", "chol_tb"]]
    heatmap_data_norm = (heatmap_data - heatmap_data.min()) / (heatmap_data.max() - heatmap_data.min()) * 100

    fig_heatmap = px.imshow(
        heatmap_data_norm.T,
        text_auto=".1f",
        color_continuous_scale="RdYlGn_r",
        aspect="auto",
        labels=dict(color="Giá trị chuẩn hóa (0-100)"),
    )
    fig_heatmap = style_figure(fig_heatmap, "Heatmap chuẩn hóa các chỉ số theo nhóm tuổi", height=350)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    trend_col3, trend_col4 = st.columns(2)

    with trend_col3:
        st.markdown("#### 📊 Oldpeak trung bình theo nhóm tuổi")

        fig_oldpeak = px.bar(
            age_trend,
            x="age_group",
            y="oldpeak_tb",
            text="oldpeak_tb",
            color="oldpeak_tb",
            color_continuous_scale="Reds",
        )

        fig_oldpeak.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig_oldpeak.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
        fig_oldpeak = style_figure(fig_oldpeak, height=350)
        fig_oldpeak.update_layout(showlegend=False, xaxis_title="", yaxis_title="Oldpeak TB")
        st.plotly_chart(fig_oldpeak, use_container_width=True)

    with trend_col4:
        st.markdown("#### 💓 Nhịp tim tối đa TB theo nhóm tuổi")

        fig_thalach = px.bar(
            age_trend,
            x="age_group",
            y="thalach_tb",
            text="thalach_tb",
            color="thalach_tb",
            color_continuous_scale="Blues",
        )

        fig_thalach.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_thalach.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
        fig_thalach = style_figure(fig_thalach, height=350)
        fig_thalach.update_layout(showlegend=False, xaxis_title="", yaxis_title="Thalach TB")
        st.plotly_chart(fig_thalach, use_container_width=True)

with tab2:
    st.markdown("### 💡 5 Nhận định chính từ phân tích")

    disease_rate = df["target"].mean() * 100
    male_rate = df[df["sex_label"] == "Nam"]["target"].mean() * 100 if (df["sex_label"] == "Nam").any() else np.nan
    female_rate = df[df["sex_label"] == "Nữ"]["target"].mean() * 100 if (df["sex_label"] == "Nữ").any() else np.nan
    age_risk = df.groupby("age_group", observed=False)["target"].mean().sort_values(ascending=False)
    top_age_group = age_risk.index[0] if not age_risk.empty else "N/A"
    top_age_rate = age_risk.iloc[0] * 100 if not age_risk.empty else 0

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:
        st.markdown("#### 📊 Thống kê tổng quan")

        stat_box(f"{disease_rate:.1f}%", "Tỷ lệ bệnh tim chung", "📊", "#ef4444")
        stat_box(f"{male_rate:.1f}%", "Tỷ lệ bệnh tim - Nam", "👨", "#0e7490")
        stat_box(f"{female_rate:.1f}%", "Tỷ lệ bệnh tim - Nữ", "👩", "#8b5cf6")

    with insight_col2:
        st.markdown("#### 🎯 Nhóm nguy cơ cao")

        stat_box(top_age_group, "Nhóm tuổi rủi ro cao nhất", "⚠️", "#f59e0b")
        stat_box(f"{top_age_rate:.1f}%", "Tỷ lệ bệnh nhóm này", "📈", "#ef4444")

        if not pd.isna(male_rate) and not pd.isna(female_rate):
            gender_gap = abs(male_rate - female_rate)
            higher_gender = "Nam" if male_rate > female_rate else "Nữ"
            stat_box(f"{gender_gap:.1f}%", f"Chênh lệch giới ({higher_gender} cao hơn)", "⚖️", "#10b981")

    divider_with_text("INSIGHTS CHI TIẾT")

    st.markdown(f"""
    #### 📌 Nhận định chi tiết

    **1. Tổng quan bệnh tim**
    {info_badge(f'Tỷ lệ chung: {disease_rate:.1f}%', 'danger' if disease_rate > 50 else 'warning')}

    Tỷ lệ bệnh tim trong tập dữ liệu đang phân tích là **{disease_rate:.1f}%**. Đây là một tỷ lệ {'cao' if disease_rate > 50 else 'đáng chú ý'} cần có biện pháp can thiệp và theo dõi.

    ---

    **2. Phân tích theo giới tính**
    {info_badge(f'Nam: {male_rate:.1f}%', 'info')}  {info_badge(f'Nữ: {female_rate:.1f}%', 'info')}

    {'Nam giới có tỷ lệ bệnh tim cao hơn nữ giới' if male_rate > female_rate else 'Nữ giới có tỷ lệ bệnh tim cao hơn nam giới'} với chênh lệch **{abs(male_rate - female_rate):.1f} điểm phần trăm**. Điều này phù hợp với các nghiên cứu y học về yếu tố nguy cơ tim mạch.

    ---

    **3. Nhóm tuổi nguy cơ cao**
    {info_badge(f'Nhóm {top_age_group}: {top_age_rate:.1f}%', 'danger')}

    Nhóm tuổi **{top_age_group}** có nguy cơ mắc bệnh tim cao nhất với tỷ lệ **{top_age_rate:.1f}%**. Đây là nhóm ưu tiên số 1 cho các chương trình sàng lọc và phòng ngừa.

    ---

    **4. Yếu tố lâm sàng quan trọng**
    {info_badge('oldpeak', 'warning')}  {info_badge('thalach', 'warning')}  {info_badge('ca', 'warning')}

    Các biến lâm sàng như **oldpeak** (ST depression), **thalach** (nhịp tim tối đa), và **ca** (số mạch máu lớn) thường có chênh lệch rõ rệt giữa nhóm có và không có bệnh tim. Đây là những chỉ số quan trọng để đánh giá nguy cơ.

    ---

    **5. Triệu chứng phân nhóm tốt**
    {info_badge('Loại đau ngực', 'success')}  {info_badge('Đau khi gắng sức', 'success')}

    Loại đau ngực (**cp**) và đau thắt ngực khi gắng sức (**exang**) là hai yếu tố phân nhóm rủi ro hiệu quả. Các triệu chứng này nên được đánh giá kỹ trong khám lâm sàng.
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 🎯 Khuyến nghị và hành động")

    rec_tab1, rec_tab2 = st.tabs(["🏥 Góc nhìn y tế", "💼 Ma trận ưu tiên"])

    with rec_tab1:
        st.markdown("""
        #### 🏥 Gợi ý ra quyết định (Góc nhìn y tế)

        ##### 1. Chiến lược sàng lọc 🔍
        - **Ưu tiên cao:** Nhóm tuổi cao (60+) và nhóm có dấu hiệu đau ngực bất thường
        - **Tần suất:** Kiểm tra định kỳ 6 tháng/lần cho nhóm nguy cơ cao
        - **Phương pháp:** ECG, test gắng sức, siêu âm tim

        ##### 2. Theo dõi chỉ số 📊
        - **Oldpeak cao:** Theo dõi sát chuyên khoa tim mạch
        - **Thalach thấp:** Đánh giá khả năng gắng sức và chức năng tim sớm
        - **Ca ≥ 2:** Xem xét can thiệp mạch máu nếu cần

        ##### 3. Hệ thống cảnh báo 🚨
        Xây dựng hệ thống cảnh báo nguy cơ dựa trên tổ hợp:
        - Loại đau ngực (cp) = đau thắt ngực điển hình
        - Đau khi gắng sức (exang) = Có
        - Số mạch máu (ca) ≥ 1
        - ST depression (oldpeak) > 1.5

        ##### 4. Truyền thông phòng ngừa 📢
        - **Nhóm mục tiêu:** Nam giới 50+, người có tiền sử gia đình
        - **Nội dung:** Thay đổi lối sống, kiểm soát cholesterol, huyết áp
        - **Kênh:** Tư vấn trực tiếp, phòng khám cộng đồng, app di động

        ##### 5. Can thiệp sớm 💊
        - Statin cho cholesterol cao (>240 mg/dl)
        - Thuốc hạ áp cho huyết áp >140/90 mmHg
        - Aspirin liều thấp cho nhóm nguy cơ cao (theo chỉ định bác sĩ)
        """)

    with rec_tab2:
        st.markdown("#### 💼 Ma trận ưu tiên hành động")

        action_df = pd.DataFrame({
            "Hạng mục": [
                "🔴 Nhóm tuổi 60+ có tỷ lệ bệnh cao",
                "🟠 Nhóm có oldpeak trung bình cao (>1.5)",
                "🟠 Nhóm có thalach trung bình thấp (<130)",
                "🟡 Nhóm có exang = Có",
                "🟡 Nam giới có loại đau ngực điển hình",
                "🟢 Nữ dưới 50 tuổi không triệu chứng",
            ],
            "Mức ưu tiên": ["⭐⭐⭐⭐⭐ Rất cao", "⭐⭐⭐⭐ Cao", "⭐⭐⭐⭐ Cao", "⭐⭐⭐ Trung bình", "⭐⭐⭐ Trung bình", "⭐⭐ Thấp"],
            "Hành động gợi ý": [
                "Sàng lọc định kỳ 6 tháng, theo dõi sát chuyên khoa",
                "Kiểm tra ECG gắng sức, theo dõi chức năng tim mạch chuyên sâu",
                "Đánh giá khả năng gắng sức, test chức năng tim",
                "Tư vấn phòng ngừa cá nhân hóa, điều chỉnh lối sống",
                "Kiểm tra định kỳ hàng năm, tư vấn yếu tố nguy cơ",
                "Kiểm tra sức khỏe định kỳ 1-2 năm/lần",
            ],
            "Thời gian": ["Ngay lập tức", "1-2 tuần", "1-2 tuần", "1 tháng", "3-6 tháng", "Hàng năm"],
            "Chi phí ước tính": ["$$$$$", "$$$$", "$$$$", "$$$", "$$$", "$$"],
        })

        st.dataframe(action_df, use_container_width=True, hide_index=True)

        st.markdown("#### 📊 Biểu đồ độ ưu tiên")

        priority_map = {
            "⭐⭐⭐⭐⭐ Rất cao": 5,
            "⭐⭐⭐⭐ Cao": 4,
            "⭐⭐⭐ Trung bình": 3,
            "⭐⭐ Thấp": 2,
            "⭐ Rất thấp": 1,
        }

        action_df["priority_score"] = action_df["Mức ưu tiên"].map(priority_map)

        fig_priority = px.bar(
            action_df,
            y="Hạng mục",
            x="priority_score",
            orientation="h",
            color="priority_score",
            color_continuous_scale="RdYlGn_r",
            text="Mức ưu tiên",
        )

        fig_priority.update_traces(textposition='inside', textfont_size=11)
        fig_priority = style_figure(fig_priority, "Ma trận ưu tiên hành động", height=400)
        fig_priority.update_layout(
            xaxis_title="Điểm ưu tiên",
            yaxis_title="",
            showlegend=False,
        )
        st.plotly_chart(fig_priority, use_container_width=True)

with tab4:
    st.markdown("### 📈 Dashboard Tổng hợp Toàn diện")

    st.markdown("#### 📊 KPI Dashboard")

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    with kpi1:
        stat_box(f"{len(df):,}", "Tổng hồ sơ", "📋", "#0e7490")

    with kpi2:
        stat_box(f"{disease_rate:.1f}%", "Tỷ lệ bệnh tim", "❤️", "#ef4444")

    with kpi3:
        avg_age = df['age'].mean()
        stat_box(f"{avg_age:.1f}", "Tuổi TB", "👤", "#10b981")

    with kpi4:
        avg_chol = df['chol'].mean()
        stat_box(f"{avg_chol:.0f}", "Cholesterol TB", "🩺", "#f59e0b")

    with kpi5:
        high_risk_pct = (df[df['target'] == 1].shape[0] / len(df) * 100)
        stat_box(f"{high_risk_pct:.1f}%", "% Nguy cơ cao", "🚨", "#8b5cf6")

    divider_with_text("BIỂU ĐỒ TỔNG HỢP")

    dash_col1, dash_col2 = st.columns(2)

    with dash_col1:
        st.markdown("#### 🎯 Gauge: Tỷ lệ bệnh tim tổng thể")
        gauge_overall = create_gauge_chart(disease_rate, "", max_value=100, color="#ef4444")
        st.plotly_chart(gauge_overall, use_container_width=True)

        st.markdown("#### 📊 Phân bố theo giới tính")
        gender_dist = df.groupby(['sex_label', 'target_label']).size().reset_index(name='count')
        fig_gender_pie = px.sunburst(
            gender_dist,
            path=['sex_label', 'target_label'],
            values='count',
            color='count',
            color_continuous_scale='RdYlGn_r',
        )
        fig_gender_pie = style_figure(fig_gender_pie, height=400)
        st.plotly_chart(fig_gender_pie, use_container_width=True)

    with dash_col2:
        st.markdown("#### 🎯 Radar: Profile nhóm bệnh vs không bệnh")

        metrics = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
        categories_radar = ['Tuổi', 'Huyết áp', 'Cholesterol', 'Nhịp tim', 'ST Depression']

        no_disease_vals = df[df['target'] == 0][metrics].mean().values
        has_disease_vals = df[df['target'] == 1][metrics].mean().values

        # Chuẩn hóa
        no_disease_norm = ((no_disease_vals - no_disease_vals.min()) / (no_disease_vals.max() - no_disease_vals.min()) * 100).tolist()
        has_disease_norm = ((has_disease_vals - has_disease_vals.min()) / (has_disease_vals.max() - has_disease_vals.min()) * 100).tolist()

        radar_overall = create_radar_chart(
            categories_radar,
            {
                "Không bệnh tim": no_disease_norm,
                "Có bệnh tim": has_disease_norm
            },
            ""
        )
        st.plotly_chart(radar_overall, use_container_width=True)

        st.markdown("#### 📈 Top 5 nhóm tuổi - Tỷ lệ bệnh")
        age_top5 = age_trend.nlargest(5, 'ty_le_benh_tim')
        fig_age_top = px.bar(
            age_top5,
            x='age_group',
            y='ty_le_benh_tim',
            text='ty_le_benh_tim',
            color='ty_le_benh_tim',
            color_continuous_scale='Reds',
        )
        fig_age_top.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_age_top = style_figure(fig_age_top, height=350)
        fig_age_top.update_layout(showlegend=False, xaxis_title="", yaxis_title="Tỷ lệ (%)")
        st.plotly_chart(fig_age_top, use_container_width=True)

    st.markdown("#### 📊 Bảng tổng hợp theo nhiều chiều")

    multi_dim = df.groupby(['age_group', 'sex_label', 'target_label'], observed=False).size().reset_index(name='count')
    multi_dim_pivot = multi_dim.pivot_table(
        index=['age_group', 'sex_label'],
        columns='target_label',
        values='count',
        fill_value=0
    )

    st.dataframe(multi_dim_pivot, use_container_width=True)

    with st.expander("📝 Ghi chú kỹ thuật và phương pháp"):
        st.markdown("""
        #### 🔧 Kỹ thuật sử dụng

        - **Framework:** Streamlit 1.x + Plotly 5.x
        - **Caching:** Sử dụng `@st.cache_data` để tối ưu hiệu suất tải dữ liệu
        - **Responsiveness:** Layout responsive với `use_container_width=True`
        - **Interactivity:** Bộ lọc động trên sidebar, cập nhật realtime

        #### 📊 Phương pháp phân tích

        - **Confidence Interval:** Wald method với Z=1.96 (95% CI)
        - **Odds Ratio:** Haldane-Anscombe correction (thêm 0.5)
        - **Outlier Detection:** IQR method (Q1 - 1.5×IQR, Q3 + 1.5×IQR)
        - **Normalization:** Min-Max scaling cho visualization

        #### ⚠️ Giới hạn

        - Bộ dữ liệu không có cột thời gian → không phân tích xu hướng theo thời gian
        - Phân tích mang tính mô tả, không thay thế chẩn đoán y khoa
        - Kết quả phụ thuộc vào chất lượng và độ đầy đủ của dữ liệu đầu vào
        """)

st.markdown("---")
st.caption("✅ **Hoàn thành!** Bạn đã khám phá hết 5 page phân tích của dashboard. Quay lại trang chủ để xem tổng quan!")
