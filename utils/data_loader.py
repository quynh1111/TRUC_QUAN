import pandas as pd
import streamlit as st

VARIABLE_DESCRIPTIONS = {
    "age": "Tuổi",
    "sex": "Giới tính (1=Nam, 0=Nữ)",
    "cp": "Loại đau ngực",
    "trestbps": "Huyết áp lúc nghỉ",
    "chol": "Cholesterol",
    "fbs": "Đường huyết lúc đói > 120 mg/dl",
    "restecg": "Kết quả ECG lúc nghỉ",
    "thalach": "Nhịp tim tối đa",
    "exang": "Đau thắt ngực khi vận động",
    "oldpeak": "ST depression do vận động",
    "slope": "Độ dốc đoạn ST",
    "ca": "Số mạch máu lớn nhuộm màu",
    "thal": "Tình trạng thalassemia",
    "target": "Nhãn bệnh tim (1=có nguy cơ/bệnh)",
}

SEX_MAP = {0: "Nữ", 1: "Nam"}
CP_MAP = {0: "Đau thắt ngực điển hình", 1: "Đau thắt ngực không điển hình", 2: "Đau không do tim", 3: "Không triệu chứng"}
EXANG_MAP = {0: "Không", 1: "Có"}
FBS_MAP = {0: "<=120", 1: ">120"}
TARGET_MAP = {0: "Không bệnh tim", 1: "Có bệnh tim"}
NUMERIC_COLUMNS = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"]


@st.cache_data
def load_raw_data(file_path: str = "heart.csv") -> pd.DataFrame:
    return pd.read_csv(file_path)


def preprocess_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()

    for col in [c for c in NUMERIC_COLUMNS if c in df.columns]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before_drop = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    _ = before_drop - len(df)

    numeric_existing = [c for c in NUMERIC_COLUMNS if c in df.columns]
    for col in numeric_existing:
        df[col] = df[col].fillna(df[col].median())

    df["sex_label"] = df["sex"].map(SEX_MAP).fillna("Không rõ")
    df["cp_label"] = df["cp"].map(CP_MAP).fillna("Không rõ")
    df["exang_label"] = df["exang"].map(EXANG_MAP).fillna("Không rõ")
    df["fbs_label"] = df["fbs"].map(FBS_MAP).fillna("Không rõ")
    df["target_label"] = df["target"].map(TARGET_MAP).fillna("Không rõ")

    bins = [0, 39, 49, 59, 69, 120]
    labels = ["<40", "40-49", "50-59", "60-69", "70+"]
    df["age_group"] = pd.cut(df["age"], bins=bins, labels=labels, right=True)

    return df


@st.cache_data
def get_preprocessing_summary(file_path: str = "heart.csv") -> pd.DataFrame:
    raw_df = load_raw_data(file_path)
    processed_df = preprocess_data(raw_df)

    summary = pd.DataFrame(
        {
            "Chỉ số": [
                "Số dòng",
                "Số cột",
                "Số dòng trùng lặp",
                "Tổng ô thiếu",
            ],
            "Trước xử lý": [
                len(raw_df),
                raw_df.shape[1],
                int(raw_df.duplicated().sum()),
                int(raw_df.isnull().sum().sum()),
            ],
            "Sau xử lý": [
                len(processed_df),
                processed_df.shape[1],
                int(processed_df.duplicated().sum()),
                int(processed_df.isnull().sum().sum()),
            ],
        }
    )
    return summary


@st.cache_data
def load_data(file_path: str = "heart.csv") -> pd.DataFrame:
    raw_df = load_raw_data(file_path)
    return preprocess_data(raw_df)


def apply_common_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Bộ lọc phân tích")
    st.sidebar.caption("Áp dụng cho toàn bộ biểu đồ trên page hiện tại")

    min_age, max_age = int(df["age"].min()), int(df["age"].max())
    age_range = st.sidebar.slider("Khoảng tuổi", min_age, max_age, (min_age, max_age), help="Lọc bệnh nhân theo độ tuổi")

    sex_options = sorted(df["sex_label"].dropna().unique().tolist())
    selected_sex = st.sidebar.multiselect("Giới tính", sex_options, default=sex_options, help="Chọn một hoặc nhiều nhóm giới tính")

    cp_options = sorted(df["cp_label"].dropna().unique().tolist())
    selected_cp = st.sidebar.multiselect("Loại đau ngực", cp_options, default=cp_options, help="Lọc theo nhóm triệu chứng đau ngực")

    target_options = sorted(df["target_label"].dropna().unique().tolist())
    selected_target = st.sidebar.multiselect("Tình trạng bệnh tim", target_options, default=target_options, help="Lọc theo nhóm có/không có bệnh tim")

    st.sidebar.divider()

    filtered = df[
        (df["age"].between(age_range[0], age_range[1]))
        & (df["sex_label"].isin(selected_sex))
        & (df["cp_label"].isin(selected_cp))
        & (df["target_label"].isin(selected_target))
    ].copy()

    st.sidebar.success(f"Số dòng sau lọc: {len(filtered):,}")
    return filtered
