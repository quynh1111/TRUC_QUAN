# BÁO CÁO BÀI TẬP LỚN
## Môn: Trực quan hóa dữ liệu
## Đề tài 4: Phân tích nguy cơ bệnh tim từ bộ dữ liệu Heart Disease

---

## 1. Giới thiệu bài toán

### 1.1 Bối cảnh
Bệnh tim mạch là một trong các nhóm bệnh có tỷ lệ mắc cao và ảnh hưởng lớn đến sức khỏe cộng đồng. Việc phân tích dữ liệu khám sức khỏe có thể hỗ trợ nhận diện nhóm nguy cơ và hỗ trợ ra quyết định sàng lọc sớm.

### 1.2 Mục tiêu
- Hiểu dữ liệu và bối cảnh bài toán.
- Thực hiện EDA để phát hiện đặc điểm dữ liệu.
- Xây dựng dashboard tương tác 5 page bằng Streamlit.
- Trình bày insight và đề xuất hành động.

### 1.3 Công cụ sử dụng
- Python: Pandas, NumPy, Plotly
- Streamlit (Multipage app)

---

## 2. Mô tả dữ liệu (PHẦN 1 – 10%)

### 2.1 Nguồn dữ liệu
- Bộ dữ liệu: Heart Disease Dataset (Kaggle)
- File sử dụng: `heart.csv`

### 2.2 Quy mô dữ liệu
- Số dòng: 1026
- Số cột: 14 biến gốc

### 2.3 Danh sách biến chính
`age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target`

### 2.4 Ý nghĩa biến
- `age`: tuổi
- `sex`: giới tính (1=Nam, 0=Nữ)
- `cp`: loại đau ngực
- `trestbps`: huyết áp lúc nghỉ
- `chol`: cholesterol
- `fbs`: đường huyết lúc đói
- `restecg`: ECG lúc nghỉ
- `thalach`: nhịp tim tối đa
- `exang`: đau thắt ngực khi gắng sức
- `oldpeak`: ST depression
- `slope`: độ dốc đoạn ST
- `ca`: số mạch máu chính
- `thal`: tình trạng thalassemia
- `target`: nhãn bệnh tim (1=có bệnh/nguy cơ, 0=không)

---

## 3. Khám phá và xử lý dữ liệu (PHẦN 2 – 25%)

### 3.1 Quy trình xử lý dữ liệu
Thực hiện theo chuỗi:
1. Đọc dữ liệu thô (`load_raw_data`).
2. Chuẩn hóa kiểu dữ liệu số.
3. Xử lý giá trị thiếu bằng trung vị (median).
4. Loại bỏ dòng trùng lặp.
5. Tạo biến mới phục vụ phân tích (`sex_label`, `cp_label`, `age_group`, ...).

### 3.2 Kiểm tra dữ liệu thiếu
- Kiểm tra bằng `isnull().sum()`.
- Trình bày trên Page 2, tab “Thiếu dữ liệu & ngoại lệ”.

### 3.3 Kiểm tra ngoại lệ
- Áp dụng IQR cho: `age, chol, trestbps, thalach, oldpeak`.
- Thống kê số lượng ngoại lệ theo từng biến.

### 3.4 Thống kê mô tả
- Dùng `describe()` cho nhóm biến số.
- Trình bày trên tab “Thống kê mô tả”.

### 3.5 Lọc điều kiện
- Ví dụ: `age > 60` và `target = 1` để xác định nhóm nguy cơ cao.

### 3.6 GroupBy / tổng hợp
- Tổng hợp theo giới tính, loại đau ngực, nhóm tuổi.
- Chỉ số tổng hợp: số hồ sơ, tỷ lệ bệnh tim, tuổi TB, cholesterol TB.

### 3.7 Pivot Table
- Pivot theo `sex_label × cp_label` với giá trị `target` (mean).
- Dùng để so sánh tỷ lệ bệnh tim theo từng tổ hợp nhóm.

---

## 4. Trực quan hóa dữ liệu (PHẦN 3 – 30%)

### 4.1 Biểu đồ so sánh
- Bar chart so sánh tỷ lệ bệnh tim theo các nhóm (giới tính, cp, exang, nhóm tuổi).

### 4.2 Biểu đồ phân phối
- Histogram và Boxplot cho các biến số quan trọng.

### 4.3 Biểu đồ xu hướng
- Do dữ liệu không có thời gian, sử dụng xu hướng theo nhóm tuổi (risk trend by age group).

### 4.4 Biểu đồ tổng hợp
- Stacked bar và 100% stacked bar cho so sánh cơ cấu target theo nhóm.

---

## 5. Dashboard tương tác (PHẦN 4 – 25%)

### 5.1 Cấu trúc 5 page
1. **Page 1**: Tổng quan bệnh tim (KPI + cơ cấu + tổng hợp theo giới tính/tuổi)
2. **Page 2**: EDA (xử lý trước/sau + thiếu dữ liệu + ngoại lệ + mô tả + pivot + tương quan)
3. **Page 3**: So sánh nhóm nguy cơ (bar, stacked, CI 95%)
4. **Page 4**: Yếu tố liên quan (Top N, scatter, Odds Ratio)
5. **Page 5**: Nhận định & khuyến nghị (trend tuổi, benchmark, ma trận ưu tiên)

### 5.2 Tính tương tác
- Sidebar filter: tuổi, giới tính, loại đau ngực, tình trạng bệnh tim.
- Tabs/Columns ở nhiều page.
- Biểu đồ cập nhật theo filter.

### 5.3 UI/UX
- Theme đồng nhất, màu nhất quán giữa các page.
- Trình bày rõ ràng, phù hợp báo cáo học thuật.

---

## 6. Nhận xét và Insight (PHẦN 5 – 10%)

### 6.1 Nhận định chính (mẫu)
1. Tỷ lệ bệnh tim trong tập dữ liệu đã lọc ở mức cao.
2. Có sự khác biệt rõ giữa các nhóm giới tính.
3. Nhóm tuổi cao có xu hướng rủi ro lớn hơn.
4. Các biến lâm sàng (`oldpeak`, `thalach`, `ca`) có chênh lệch đáng kể giữa 2 nhóm target.
5. Triệu chứng đau ngực và đau khi gắng sức là yếu tố phân nhóm rủi ro tốt.

### 6.2 Gợi ý hành động
- Ưu tiên sàng lọc định kỳ cho nhóm nguy cơ cao.
- Theo dõi chuyên sâu với nhóm có chỉ số lâm sàng bất lợi.
- Áp dụng ma trận ưu tiên để phân bổ nguồn lực sàng lọc.

---

## 7. Đánh giá theo thang điểm đề xuất

- Dữ liệu & EDA: đã triển khai đầy đủ
- Trực quan hóa: đủ các nhóm biểu đồ yêu cầu
- Dashboard: đủ 5 page, có filter, có tabs/columns
- Insight & trình bày: có nhận định + khuyến nghị
- Kỹ thuật & sáng tạo: có chuẩn hóa UI, thêm chỉ số CI 95%, Odds Ratio

---

## 8. Kết luận
Nhóm đã xây dựng thành công hệ thống dashboard phân tích nguy cơ bệnh tim với quy trình đầy đủ từ xử lý dữ liệu, EDA, trực quan hóa đến khuyến nghị hành động. Hệ thống đáp ứng các yêu cầu của bài tập lớn và có thể mở rộng cho các bộ dữ liệu y tế khác trong tương lai.

---

## 9. Phụ lục (điền khi nộp)
- Link GitHub: ...................................................
- Ảnh chụp minh họa 5 page: (chèn hình)
- Thành viên nhóm và phân công:
  - SV1: ................................
  - SV2: ................................
  - SV3: ................................
  - SV4: ................................
  - SV5: ................................
