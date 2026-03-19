import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np

from utils.data_loader import apply_common_filters, load_data
from utils.ui import apply_global_style, page_header, style_figure, divider_with_text, stat_box
from utils.charts import create_radar_chart


df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("🧠 Page 4 – Yếu tố liên quan bệnh tim", "Xếp hạng và phân tích các biến có mức chênh lệch lớn giữa nhóm có và không có bệnh tim.")

if df.empty:
    st.warning("⚠️ Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter trên sidebar.")
    st.stop()

st.markdown("### 🎯 Tùy chỉnh phân tích")

numeric_features = ["age", "trestbps", "chol", "thalach", "oldpeak", "ca"]

col1, col2 = st.columns(2)
with col1:
    top_n = st.slider("📊 Chọn Top N yếu tố", min_value=3, max_value=len(numeric_features), value=5)

with col2:
    sort_by = st.selectbox("🔢 Sắp xếp theo", ["Chênh lệch tuyệt đối", "Chênh lệch có dấu"], index=0)

mean_1 = df[df["target"] == 1][numeric_features].mean()
mean_0 = df[df["target"] == 0][numeric_features].mean()

diff_df = pd.DataFrame({
    "feature": numeric_features,
    "mean_target_1": mean_1.values,
    "mean_target_0": mean_0.values
})
diff_df["mean_diff"] = diff_df["mean_target_1"] - diff_df["mean_target_0"]
diff_df["abs_mean_diff"] = diff_df["mean_diff"].abs()
diff_df["pct_change"] = ((diff_df["mean_diff"] / diff_df["mean_target_0"].replace(0, 1)) * 100).round(2)

if sort_by == "Chênh lệch tuyệt đối":
    top_df = diff_df.sort_values("abs_mean_diff", ascending=False).head(top_n)
else:
    top_df = diff_df.sort_values("mean_diff", ascending=False).head(top_n)

divider_with_text("TOP YẾU TỐ QUAN TRỌNG")

st.markdown(f"### 📊 Top {top_n} yếu tố có chênh lệch lớn nhất")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.markdown("#### 📊 Biểu đồ chênh lệch trung bình")

    fig_top = px.bar(
        top_df.sort_values("abs_mean_diff", ascending=True),
        x="abs_mean_diff",
        y="feature",
        orientation="h",
        text="mean_diff",
        color="mean_diff",
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
    )

    fig_top.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
        textfont_size=12,
    )

    fig_top = style_figure(fig_top, height=400)
    fig_top.update_layout(
        xaxis_title="Chênh lệch tuyệt đối",
        yaxis_title="",
        showlegend=False,
    )
    st.plotly_chart(fig_top, use_container_width=True)

with viz_col2:
    st.markdown("#### 📈 Phần trăm thay đổi (%)")

    fig_pct = px.bar(
        top_df.sort_values("pct_change", ascending=True),
        x="pct_change",
        y="feature",
        orientation="h",
        text="pct_change",
        color="pct_change",
        color_continuous_scale="RdYlGn_r",
        color_continuous_midpoint=0,
    )

    fig_pct.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        textfont_size=12,
    )

    fig_pct = style_figure(fig_pct, height=400)
    fig_pct.update_layout(
        xaxis_title="% Thay đổi",
        yaxis_title="",
        showlegend=False,
    )
    st.plotly_chart(fig_pct, use_container_width=True)

st.markdown("#### 📋 Bảng chi tiết Top yếu tố")
display_df = top_df[["feature", "mean_target_0", "mean_target_1", "mean_diff", "abs_mean_diff", "pct_change"]].round(3)
display_df.columns = ["Yếu tố", "TB Không bệnh", "TB Có bệnh", "Chênh lệch", "Chênh lệch TĐ", "% Thay đổi"]
st.dataframe(display_df, use_container_width=True, hide_index=True)

st.info("💡 **Giải thích:** Giá trị dương của 'Chênh lệch' nghĩa là giá trị trung bình ở nhóm có bệnh tim cao hơn nhóm không mắc bệnh.")

divider_with_text("SO SÁNH TRỰC QUAN")

st.markdown("### 📊 So sánh trực quan giữa 2 nhóm")

tab1, tab2, tab3 = st.tabs(["🎯 Scatter Plot", "📊 Radar Chart", "📈 Waterfall Chart"])

with tab1:
    st.markdown("#### 🎯 Scatter: So sánh trung bình 2 nhóm")

    fig_scatter = px.scatter(
        diff_df,
        x="mean_target_0",
        y="mean_target_1",
        text="feature",
        size="abs_mean_diff",
        color="mean_diff",
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        size_max=30,
    )

    # Thêm đường y=x để dễ so sánh
    max_val = max(diff_df["mean_target_0"].max(), diff_df["mean_target_1"].max())
    fig_scatter.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(color='gray', dash='dash', width=2),
        name='y=x (bằng nhau)',
        showlegend=True,
    ))

    fig_scatter.update_traces(textposition='top center', textfont_size=11, selector=dict(mode='markers+text'))

    fig_scatter = style_figure(fig_scatter, height=500)
    fig_scatter.update_layout(
        xaxis_title="Trung bình - Không bệnh tim",
        yaxis_title="Trung bình - Có bệnh tim",
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.caption("📌 Các điểm phía trên đường chéo: giá trị cao hơn ở nhóm có bệnh. Dưới đường chéo: giá trị thấp hơn.")

with tab2:
    st.markdown("#### 🎯 Radar Chart: So sánh toàn diện")

    # Chuẩn hóa để hiển thị trên radar
    normalized_0 = ((mean_0 - mean_0.min()) / (mean_0.max() - mean_0.min()) * 100).tolist()
    normalized_1 = ((mean_1 - mean_1.min()) / (mean_1.max() - mean_1.min()) * 100).tolist()

    radar_fig = create_radar_chart(
        numeric_features,
        {
            "Không bệnh tim": normalized_0,
            "Có bệnh tim": normalized_1
        },
        ""
    )

    st.plotly_chart(radar_fig, use_container_width=True)
    st.caption("📌 Biểu đồ radar thể hiện profile đa chiều của hai nhóm (đã chuẩn hóa 0-100).")

with tab3:
    st.markdown("#### 📊 Waterfall: Chênh lệch tích lũy")

    waterfall_data = diff_df.sort_values("mean_diff", ascending=False)

    fig_waterfall = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        x=waterfall_data["feature"],
        y=waterfall_data["mean_diff"],
        text=waterfall_data["mean_diff"].round(2),
        textposition="outside",
        connector={"line": {"color": "#cbd5e1", "width": 2}},
        increasing={"marker": {"color": "#ef4444"}},
        decreasing={"marker": {"color": "#10b981"}},
    ))

    fig_waterfall = style_figure(fig_waterfall, "Waterfall: Chênh lệch các yếu tố", height=450)
    fig_waterfall.update_layout(
        xaxis_title="Yếu tố",
        yaxis_title="Chênh lệch",
        showlegend=False,
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)

divider_with_text("PIVOT TABLE & ODDS RATIO")

st.markdown("### 📋 Phân tích đa chiều")

pivot_tab, odds_tab = st.tabs(["📊 Pivot Table", "🎲 Odds Ratio"])

with pivot_tab:
    st.markdown("#### 📊 Pivot Table: Giới tính × Loại đau ngực")
    st.caption("Tỷ lệ bệnh tim (%) theo từng tổ hợp")

    pivot = pd.pivot_table(
        df,
        index="sex_label",
        columns="cp_label",
        values="target",
        aggfunc="mean",
        fill_value=0
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
    fig_heatmap = style_figure(fig_heatmap, "Heatmap: Tỷ lệ bệnh tim theo giới tính và loại đau ngực", height=400)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("#### 📊 Pivot Table: Nhóm tuổi × Giới tính")

    pivot2 = pd.pivot_table(
        df,
        index="age_group",
        columns="sex_label",
        values="target",
        aggfunc=["mean", "size"],
        fill_value=0
    )

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("**Tỷ lệ bệnh tim (%) theo nhóm tuổi và giới tính**")
        pivot2_mean = (pivot2["mean"] * 100).round(2)
        st.dataframe(pivot2_mean, use_container_width=True)

    with col_p2:
        st.markdown("**Số lượng hồ sơ theo nhóm tuổi và giới tính**")
        st.dataframe(pivot2["size"], use_container_width=True)

with odds_tab:
    st.markdown("#### 🎲 Phân tích Odds Ratio cho biến nhị phân")
    st.caption("Odds Ratio đo lường mức độ liên quan giữa yếu tố và bệnh tim")

    binary_features = ["sex", "fbs", "exang"]
    binary_labels = {
        "sex": "Giới tính (Nam vs Nữ)",
        "fbs": "Đường huyết đói (>120 vs ≤120)",
        "exang": "Đau thắt ngực gắng sức (Có vs Không)"
    }

    or_rows = []
    for feature in binary_features:
        a = len(df[(df[feature] == 1) & (df["target"] == 1)])
        b = len(df[(df[feature] == 1) & (df["target"] == 0)])
        c = len(df[(df[feature] == 0) & (df["target"] == 1)])
        d = len(df[(df[feature] == 0) & (df["target"] == 0)])

        # Thêm 0.5 để tránh division by zero (Haldane-Anscombe correction)
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
        odds_ratio = (a * d) / (b * c)

        # Tính confidence interval (95%)
        log_or = np.log(odds_ratio)
        se_log_or = np.sqrt(1/a + 1/b + 1/c + 1/d)
        ci_lower = np.exp(log_or - 1.96 * se_log_or)
        ci_upper = np.exp(log_or + 1.96 * se_log_or)

        or_rows.append({
            "Biến": binary_labels.get(feature, feature),
            "Odds Ratio": round(float(odds_ratio), 3),
            "CI 95% Thấp": round(float(ci_lower), 3),
            "CI 95% Cao": round(float(ci_upper), 3)
        })

    or_df = pd.DataFrame(or_rows).sort_values("Odds Ratio", ascending=False)

    st.dataframe(or_df, use_container_width=True, hide_index=True)

    # Biểu đồ Forest Plot cho Odds Ratios
    fig_forest = go.Figure()

    for idx, row in or_df.iterrows():
        fig_forest.add_trace(go.Scatter(
            x=[row["CI 95% Thấp"], row["Odds Ratio"], row["CI 95% Cao"]],
            y=[row["Biến"]] * 3,
            mode='lines+markers',
            name=row["Biến"],
            line=dict(width=3),
            marker=dict(size=[8, 14, 8], symbol=['line-ew', 'diamond', 'line-ew']),
            showlegend=False,
        ))

    # Thêm đường tham chiếu OR=1
    fig_forest.add_vline(x=1, line_dash="dash", line_color="red", annotation_text="OR=1 (không liên quan)")

    fig_forest = style_figure(fig_forest, "Forest Plot: Odds Ratio và khoảng tin cậy 95%", height=350)
    fig_forest.update_layout(
        xaxis_title="Odds Ratio (log scale)",
        yaxis_title="",
        xaxis_type="log",
    )
    st.plotly_chart(fig_forest, use_container_width=True)

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.info("""
        **📖 Giải thích Odds Ratio:**
        - **OR > 1:** Yếu tố tăng nguy cơ bệnh tim
        - **OR = 1:** Yếu tố không liên quan
        - **OR < 1:** Yếu tố giảm nguy cơ bệnh tim
        """)

    with col_info2:
        st.success("""
        **✅ Khoảng tin cậy 95%:**
        - Nếu CI không chứa 1: có ý nghĩa thống kê
        - Nếu CI chứa 1: không có bằng chứng mạnh về liên quan
        """)

st.markdown("---")
st.caption("💡 **Tip:** Kết hợp nhiều góc nhìn (scatter, radar, odds ratio) để hiểu rõ hơn về các yếu tố liên quan!")
