# KẾ HOẠCH BÀI TẬP LỚN – TRỰC QUAN HÓA DỮ LIỆU
## Đề tài 4: Heart Disease Dataset (`heart.csv`)

> Mục tiêu: Tài liệu này dùng để **kiểm tra trước** xem đề tài đã phủ đủ yêu cầu BTL hay chưa, trước khi code Streamlit dashboard.

---

## 1) XÁC NHẬN DỮ LIỆU ĐẦU VÀO

- File dữ liệu: `heart.csv`
- Quy mô dữ liệu hiện tại: **1026 dòng × 14 cột**
- Danh sách biến:
  - `age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target`

### Gợi ý ý nghĩa biến (để đưa vào báo cáo)
- `age`: tuổi
- `sex`: giới tính (1 = nam, 0 = nữ)
- `cp`: loại đau ngực
- `trestbps`: huyết áp lúc nghỉ
- `chol`: cholesterol
- `fbs`: đường huyết lúc đói
- `restecg`: kết quả điện tâm đồ lúc nghỉ
- `thalach`: nhịp tim tối đa đạt được
- `exang`: đau thắt ngực khi vận động
- `oldpeak`: ST depression do vận động
- `slope`: độ dốc đoạn ST
- `ca`: số mạch máu lớn quan sát được
- `thal`: tình trạng thalassemia
- `target`: nhãn bệnh tim (1 = có nguy cơ/bệnh, 0 = không)

---

## 2) KIỂM TRA PHỦ YÊU CẦU THEO RUBRIC

## PHẦN 1 – Mô tả dữ liệu (10%)
Checklist:
- [x] Nguồn dữ liệu (Kaggle: Heart Disease Dataset)
- [x] Số dòng, số cột
- [x] Ý nghĩa các biến
- [x] Kiểu dữ liệu từng biến (`df.dtypes`)

Sản phẩm cần có:
- 1 bảng mô tả cột + kiểu dữ liệu + diễn giải ngắn.

## PHẦN 2 – EDA (25%)
Quy trình thực hiện:
1. Xử lý dữ liệu thô trước (chuẩn hóa kiểu dữ liệu, xử lý thiếu, loại trùng lặp, tạo biến nhóm tuổi/nhãn).
2. Sau đó mới thực hiện EDA và trực quan.

Checklist:
- [x] Kiểm tra dữ liệu thiếu (`isnull().sum()`)
- [x] Kiểm tra ngoại lệ (IQR cho `age, chol, trestbps, thalach, oldpeak`)
- [x] Thống kê mô tả (`describe()`)
- [x] Lọc dữ liệu theo điều kiện (ví dụ: `age > 60`, `target == 1`)
- [x] GroupBy/tổng hợp (theo `sex`, `cp`, `thal`...)
- [x] Pivot Table (ví dụ: `pivot_table(index='sex', columns='cp', values='target', aggfunc='mean')`)

Triển khai trong dashboard:
- Page 2, phần đầu: Bước 1 – Xử lý dữ liệu trước khi EDA (bảng trước/sau xử lý)
- Page 2, tab 1: Thiếu dữ liệu + ngoại lệ (IQR)
- Page 2, tab 2: Thống kê mô tả
- Page 2, tab 3: Lọc điều kiện + GroupBy/tổng hợp
- Page 2, tab 4: Pivot Table

Sản phẩm cần có:
- 3–5 bảng EDA tiêu biểu + nhận xét ngắn cho từng bảng.

## PHẦN 3 – Trực quan hóa dữ liệu (30%)
Yêu cầu bắt buộc và cách đáp ứng:
- [x] Biểu đồ so sánh: Bar chart tỷ lệ bệnh theo giới tính/nhóm tuổi
- [x] Biểu đồ phân phối: Histogram/Boxplot cho `chol`, `trestbps`, `thalach`
- [x] Biểu đồ xu hướng theo nhóm tuổi/mức rủi ro
- [x] Biểu đồ tổng hợp: Grouped/Stacked theo `sex × target` hoặc `cp × target`

⚠️ **Lưu ý quan trọng:** `heart.csv` **không có cột thời gian**, vì vậy dashboard dùng
“xu hướng theo nhóm tuổi/mức rủi ro” thay cho xu hướng theo thời gian thực.

## PHẦN 4 – Dashboard tương tác (25%)
Checklist bắt buộc:
- [x] Sidebar filter (ít nhất 2 điều kiện): ví dụ `age range`, `sex`, `cp`, `target`
- [x] Có Tabs hoặc Columns để bố cục
- [x] Biểu đồ cập nhật theo tương tác filter
- [x] Giao diện rõ ràng, dễ hiểu
- [x] (Khuyến khích) dùng `@st.cache_data`

## PHẦN 5 – Nhận xét & Insight (10%)
Checklist:
- [x] Tối thiểu 5 phát hiện chính từ dữ liệu
- [x] So sánh nhóm nổi bật (giới tính/tuổi/đau ngực...)
- [x] Đề xuất hành động (góc nhìn y tế cộng đồng/phòng ngừa rủi ro)

---

## 3) THIẾT KẾ DASHBOARD 5 PAGE (ĐÃ CHỐT CHÍNH THỨC)

> Vì đề tài gốc hướng bán lẻ, nhóm có thể chuyển ngữ bối cảnh sang **theo dõi nguy cơ bệnh tim** cho bệnh viện/trung tâm y tế.

### Page 1 – Tổng quan bệnh tim
Bắt buộc:
- KPI (`st.metric`):
  - Tổng số hồ sơ
  - Tỷ lệ có bệnh tim (`target=1`)
  - Tuổi trung bình
  - Cholesterol trung bình
- Biểu đồ cơ cấu bệnh/không bệnh
- 1 bảng groupby tổng quan theo giới tính

### Page 2 – Phân bố chỉ số sức khỏe
Bắt buộc:
- Histogram cho các biến: `age, chol, trestbps, thalach, oldpeak`
- Boxplot để quan sát ngoại lệ theo nhóm `target`
- Tích hợp EDA: dữ liệu thiếu, thống kê mô tả, lọc điều kiện, groupby

### Page 3 – So sánh nhóm nguy cơ
Bắt buộc:
- Bar chart so sánh tỷ lệ bệnh theo `sex/cp/exang/fbs/age_group`
- Dữ liệu xử lý bằng groupby
- Cho phép chọn nhiều nhóm (`multiselect`)
- Có biểu đồ tổng hợp stacked và nhận xét nhóm nổi bật

### Page 4 – Top yếu tố liên quan bệnh tim
Bắt buộc:
- Top N yếu tố theo chênh lệch trung bình giữa `target=1` và `target=0`
- Biểu đồ cột ngang (horizontal bar)
- Có filter theo nhóm qua sidebar chung
- Áp dụng Pivot Table (`sex × cp` theo tỷ lệ `target`)

### Page 5 – Tương tác & trải nghiệm người dùng
Bắt buộc:
- Sidebar chứa toàn bộ bộ lọc chung
- Tabs/Expander để tổ chức nội dung
- Có biểu đồ xu hướng theo nhóm tuổi (line chart)
- Tóm tắt insight và gợi ý quyết định

---

## 3.1) Trạng thái triển khai hiện tại

- [x] Đã tạo `app.py` (trang chủ) + đúng 5 page trong thư mục `pages/`
- [x] Đã tạo `requirements.txt`
- [x] Đã có `@st.cache_data` cho nạp dữ liệu
- [x] Đã bỏ phụ thuộc cột thời gian, thay bằng xu hướng theo nhóm tuổi
- [x] Đã nâng cấp UI theo phong cách báo cáo analyst (theme thống nhất, KPI rõ ràng, biểu đồ dễ đọc)
- [x] Đã chuẩn hóa màu và template biểu đồ theo hướng dẫn Streamlit/Plotly (theme nhất quán, legend dễ đọc, thứ tự nhóm tuổi cố định)

Tham khảo cải tiến giao diện:
- Streamlit Design Concepts: bố cục bằng containers/tabs/sidebar để tăng khả năng đọc dashboard
- `st.set_page_config`: dùng `layout="wide"`, `initial_sidebar_state="expanded"`, `page_icon`
- Plotly Templates & Discrete Colors: dùng template thống nhất, `color_discrete_map` cố định cho nhãn bệnh tim

---

## 3.2) Cách chạy ứng dụng

```bash
pip install -r requirements.txt
streamlit run app.py
```

Ghi chú:
- Giao diện đơn giản, dễ hiểu
- Có cache để tăng tốc tải dữ liệu

---

## 4) CẤU TRÚC THƯ MỤC HIỆN TẠI

```text
BaiTapLon/
├─ heart.csv
├─ app.py
├─ pages/
│  ├─ 1_Tong_quan_benh_tim.py
│  ├─ 2_Phan_bo_chi_so_suc_khoe.py
│  ├─ 3_So_sanh_nhom_nguy_co.py
│  ├─ 4_Top_yeu_to_lien_quan.py
│  └─ 5_Tuong_tac_va_insight.py
├─ utils/
│  ├─ data_loader.py
│  └─ charts.py
├─ requirements.txt
├─ README_BTL_Heart.md
└─ report/
  ├─ README.md
  └─ Bao_cao_BTL.docx (sẽ bổ sung khi hoàn thiện báo cáo)
```

---

## 5) TIẾN ĐỘ 2 TUẦN GỢI Ý

### Tuần 1
- Ngày 1–2: Làm sạch dữ liệu + mô tả biến
- Ngày 3–4: EDA + bảng tổng hợp + Pivot
- Ngày 5–7: Dựng 3 page đầu (Page 1, 2, 3)

### Tuần 2
- Ngày 8–10: Hoàn thành Page 4, 5 + tối ưu UI/UX
- Ngày 11–12: Viết insight + hoàn thiện báo cáo
- Ngày 13–14: Làm slide 10–15 trang + luyện thuyết trình

---

## 6) MA TRẬN CHẤM ĐIỂM TỰ ĐÁNH GIÁ (100)

- Dữ liệu & EDA: 25
- Trực quan hóa: 30
- Dashboard: 25
- Insight & trình bày: 10
- Kỹ thuật & sáng tạo: 10

Tự check trước khi nộp:
- [x] Đủ 5 page hoạt động
- [x] Đủ 4 loại biểu đồ bắt buộc
- [x] Có tối thiểu 2 filter ở sidebar
- [x] Có nhận xét/insight cho từng page
- [ ] Có báo cáo + slide + source code

---

## 7) GỢI Ý PHÂN CÔNG 5 THÀNH VIÊN

- SV1: Page 1 + KPI + dữ liệu tổng hợp
- SV2: Page 2 + EDA + phân phối + ngoại lệ
- SV3: Page 3 + phân tích nhóm + nhận xét
- SV4: Page 4 + top yếu tố + pivot table
- SV5: Page 5 + UI/UX + tích hợp toàn hệ thống + kiểm thử

---

## 8) QUYẾT ĐỊNH CẦN THỐNG NHẤT TRƯỚC KHI CODE

1. “Page 3 nhóm nguy cơ” ưu tiên nhóm nào: `giới tính` hay `nhóm tuổi` hay cả hai?
2. Định nghĩa “Top N” ở Page 4 theo tiêu chí nào (chênh lệch trung bình / tỷ lệ bệnh / mô hình đơn giản)?
3. Mẫu insight cuối cùng theo hướng y tế dự phòng hay hỗ trợ sàng lọc lâm sàng?

> Khi nhóm chốt 3 quyết định trên, có thể bắt đầu code dashboard ngay.
