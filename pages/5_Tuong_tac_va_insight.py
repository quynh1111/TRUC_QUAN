import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import apply_common_filters, load_data
from utils.ui import AGE_GROUP_ORDER, TARGET_COLOR_MAP, apply_global_style, page_header, style_figure


df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("Page 5 – Tương tác và nhận định", "Tổng hợp xu hướng rủi ro theo nhóm tuổi và đề xuất hành động.")

if df.empty:
    st.warning("Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["Xu hướng theo nhóm tuổi", "Nhận định chính", "Khuyến nghị"])

with tab1:
    age_trend = (
        df.groupby("age_group", observed=False)
        .agg(so_ho_so=("target", "size"), ty_le_benh_tim=("target", "mean"))
        .reset_index()
        .sort_values("age_group")
    )
    age_trend["ty_le_benh_tim"] = age_trend["ty_le_benh_tim"] * 100

    fig_line = px.line(age_trend, x="age_group", y="ty_le_benh_tim", markers=True, title="Xu hướng tỷ lệ bệnh tim theo nhóm tuổi")
    fig_line.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
    fig_line = style_figure(fig_line)
    st.plotly_chart(fig_line, use_container_width=True)

    fig_bar = px.bar(
        age_trend,
        x="age_group",
        y="so_ho_so",
        title="Quy mô mẫu theo nhóm tuổi",
        text="so_ho_so",
        color_discrete_sequence=[TARGET_COLOR_MAP["Không bệnh tim"]],
    )
    fig_bar.update_xaxes(categoryorder="array", categoryarray=AGE_GROUP_ORDER)
    fig_bar = style_figure(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

    benchmark = (
        df.groupby("age_group", observed=False)
        .agg(
            ty_le_benh_tim=("target", "mean"),
            oldpeak_tb=("oldpeak", "mean"),
            thalach_tb=("thalach", "mean"),
        )
        .reset_index()
    )
    benchmark["ty_le_benh_tim"] = (benchmark["ty_le_benh_tim"] * 100).round(2)
    benchmark[["oldpeak_tb", "thalach_tb"]] = benchmark[["oldpeak_tb", "thalach_tb"]].round(2)
    st.caption("Bảng chuẩn tham chiếu theo nhóm tuổi để hỗ trợ diễn giải kết quả.")
    st.dataframe(benchmark, use_container_width=True)

with tab2:
    disease_rate = df["target"].mean() * 100
    male_rate = df[df["sex_label"] == "Nam"]["target"].mean() * 100 if (df["sex_label"] == "Nam").any() else np.nan
    female_rate = df[df["sex_label"] == "Nữ"]["target"].mean() * 100 if (df["sex_label"] == "Nữ").any() else np.nan
    age_risk = df.groupby("age_group", observed=False)["target"].mean().sort_values(ascending=False)
    top_age_group = age_risk.index[0] if not age_risk.empty else "N/A"

    st.markdown(
        f"""
        ### 5 nhận định chính
        1. Tỷ lệ bệnh tim chung trong tập đang lọc là **{disease_rate:.1f}%**.
        2. Tỷ lệ bệnh tim ở nam là **{male_rate:.1f}%**, ở nữ là **{female_rate:.1f}%**.
        3. Nhóm tuổi có nguy cơ cao nhất là **{top_age_group}**.
        4. Các biến lâm sàng như `oldpeak`, `thalach`, `ca` thường có chênh lệch rõ giữa 2 nhóm target.
        5. Loại đau ngực và đau thắt ngực khi gắng sức là 2 yếu tố phân nhóm rủi ro tốt.
        """
    )

with tab3:
    st.markdown(
        """
        ### Gợi ý ra quyết định (góc nhìn y tế)
        - Ưu tiên sàng lọc sớm cho nhóm tuổi cao và nhóm có dấu hiệu đau ngực bất thường.
        - Tăng tần suất theo dõi cho hồ sơ có `oldpeak` cao và nhịp tim tối đa thấp.
        - Xây dựng cảnh báo nguy cơ nội bộ dựa trên tổ hợp chỉ số (`cp`, `exang`, `ca`, `oldpeak`).
        - Truyền thông dự phòng tim mạch theo nhóm dân số có tỷ lệ bệnh tim cao hơn.
        """
    )

    with st.expander("Ghi chú kỹ thuật"):
        st.write("- Dashboard dùng `@st.cache_data` để tăng tốc tải dữ liệu.")
        st.write("- Bộ dữ liệu gốc không có cột thời gian, nên xu hướng được thay bằng xu hướng theo nhóm tuổi.")

    st.markdown("### Ma trận ưu tiên hành động")
    action_df = pd.DataFrame(
        {
            "Hạng mục": [
                "Nhóm tuổi có tỷ lệ bệnh tim cao",
                "Nhóm có oldpeak trung bình cao",
                "Nhóm có thalach trung bình thấp",
                "Nhóm có exang = Có",
            ],
            "Mức ưu tiên": ["Rất cao", "Cao", "Cao", "Trung bình"],
            "Hành động gợi ý": [
                "Ưu tiên khám sàng lọc định kỳ",
                "Theo dõi tim mạch chuyên sâu",
                "Đánh giá khả năng gắng sức sớm",
                "Tư vấn phòng ngừa cá nhân hóa",
            ],
        }
    )
    st.dataframe(action_df, use_container_width=True, hide_index=True)
