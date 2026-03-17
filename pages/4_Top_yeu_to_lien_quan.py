import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import apply_common_filters, load_data
from utils.ui import apply_global_style, page_header, style_figure


df = load_data("heart.csv")
df = apply_common_filters(df)
apply_global_style()

page_header("Page 4 – Yếu tố liên quan bệnh tim", "Xếp hạng các biến có mức chênh lệch lớn giữa nhóm có và không có bệnh tim.")

if df.empty:
    st.warning("Không có dữ liệu sau lọc. Vui lòng nới điều kiện filter.")
    st.stop()

numeric_features = ["age", "trestbps", "chol", "thalach", "oldpeak", "ca"]
top_n = st.slider("Chọn Top N yếu tố", min_value=3, max_value=len(numeric_features), value=5)

mean_1 = df[df["target"] == 1][numeric_features].mean()
mean_0 = df[df["target"] == 0][numeric_features].mean()

diff_df = pd.DataFrame({"feature": numeric_features, "mean_target_1": mean_1.values, "mean_target_0": mean_0.values})
diff_df["mean_diff"] = diff_df["mean_target_1"] - diff_df["mean_target_0"]
diff_df["abs_mean_diff"] = diff_df["mean_diff"].abs()

top_df = diff_df.sort_values("abs_mean_diff", ascending=False).head(top_n)

fig_top = px.bar(
    top_df.sort_values("abs_mean_diff", ascending=True),
    x="abs_mean_diff",
    y="feature",
    orientation="h",
    title="Top yếu tố theo chênh lệch trung bình giữa 2 nhóm target",
    text="mean_diff",
)
fig_top = style_figure(fig_top)
st.plotly_chart(fig_top, use_container_width=True)

st.dataframe(top_df.round(3), use_container_width=True)
st.caption("`mean_diff` dương: giá trị trung bình ở nhóm có bệnh tim cao hơn nhóm không mắc bệnh.")

fig_scatter = px.scatter(
    diff_df,
    x="mean_target_0",
    y="mean_target_1",
    text="feature",
    title="So sánh trung bình biến giữa 2 nhóm target",
)
fig_scatter = style_figure(fig_scatter)
st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Pivot Table")
pivot = pd.pivot_table(df, index="sex_label", columns="cp_label", values="target", aggfunc="mean", fill_value=0)
pivot = (pivot * 100).round(2)
st.dataframe(pivot, use_container_width=True)

st.subheader("Phân tích Odds Ratio cho biến nhị phân")
binary_features = ["sex", "fbs", "exang"]
or_rows = []
for feature in binary_features:
    a = len(df[(df[feature] == 1) & (df["target"] == 1)])
    b = len(df[(df[feature] == 1) & (df["target"] == 0)])
    c = len(df[(df[feature] == 0) & (df["target"] == 1)])
    d = len(df[(df[feature] == 0) & (df["target"] == 0)])

    a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    odds_ratio = (a * d) / (b * c)
    or_rows.append({"Biến": feature, "Odds Ratio": round(float(odds_ratio), 3)})

or_df = pd.DataFrame(or_rows).sort_values("Odds Ratio", ascending=False)
st.dataframe(or_df, use_container_width=True, hide_index=True)
st.caption("Odds Ratio > 1: nhóm có đặc trưng đó có khả năng mắc bệnh tim cao hơn nhóm đối chứng.")
