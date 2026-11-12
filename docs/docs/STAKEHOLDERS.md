# 👥 Đăng Ký & Phân Tích Bên Liên Quan (STAKEHOLDERS.md)

**Dự án:** Ứng dụng đặt đồ ăn trực tuyến `food-app-cse3045`  
**Sinh viên thực hiện:** Trịnh Đình Thạch (MSV: 23110218)

---

## 1. Bảng Đăng Ký Bên Liên Quan (Stakeholder Register)

Dự án xác định 4 nhóm bên liên quan chính tác động đến quá trình phát triển và vận hành hệ thống:

| STT | Bên liên quan (Stakeholder) | Vai trò / Đại diện | Mức độ Quyền lực (Power) | Mức độ Quan tâm (Interest) | Nhóm Ma Trận |
| :--- | :--- | :--- | :---: | :---: | :--- |
| 1 | **Giảng viên & Trợ giảng môn CSE3045** | Người đánh giá đồ án (Đại học Việt Nhật - VJU) | **Cao (High)** | **Cao (High)** | **Quản lý sát sao** *(Manage Closely)* |
| 2 | **Chủ quán ăn / Người bán hàng** | Các nhà hàng xung quanh campus VJU (Vai trò Seller) | **Cao (High)** | **Thấp (Low)** | **Giữ hài lòng** *(Keep Satisfied)* |
| 3 | **Sinh viên VJU (Khách hàng)** | Người sử dụng ứng dụng đặt đồ ăn (Vai trò Customer) | **Thấp (Low)** | **Cao (High)** | **Giữ cho hiểu rõ** *(Keep Informed)* |
| 4 | **Bộ phận Quản trị VPS / Quản trị Mạng VJU** | Đơn vị cấp hạ tầng server `sv25.bcse-vju.com` | **Thấp (Low)** | **Thấp (Low)** | **Theo dõi** *(Monitor)* |

---

## 2. Ma Trận Quyền Lực $\times$ Quan Tâm (Power vs. Interest Matrix)
QUYỀN LỰC (POWER)
                         High
                          │
   [Giữ Hài Lòng]         │         [Quản Lý Sát Sao]
Chủ quán ăn (Seller)    │   1. Giảng viên / Trợ giảng CSE3045
│
─────────────────────────────┼────────────────────────────── QUAN TÂM (INTEREST)
│
[Theo Dõi]            │        [Giữ Cho Hiểu Rõ]

Quản trị viên VPS VJU     │   3. Sinh viên VJU (Customer)
│
Low
---

## 3. Chiến Lược Ứng Xử & Giao Tiếp Chi Tiết

### 1. Giảng viên & Trợ giảng môn CSE3045 (Quản lý sát sao - Manage Closely)
* **Mục tiêu:** Đáp ứng đầy đủ các yêu cầu môn học, báo cáo tiến độ đúng hạn.
* **Chiến lược:** 
  * Cập nhật đầy đủ tài liệu trong thư mục `docs/` (`TEAM.md`, `SPRINT0-REPORT.md`, `CONFIG.md`, `STAKEHOLDERS.md`, `GIT.md`).
  * Đánh tag phiên bản rõ ràng (SemVer) sau mỗi Sprint.
  * Báo cáo tiến độ và trình bày sản phẩm chạy thực tế trên VPS tại các buổi học trên lớp.

### 2. Chủ quán ăn / Người bán hàng (Giữ hài lòng - Keep Satisfied)
* **Mục tiêu:** Đảm bảo hệ thống quản lý đơn đơn giản, dễ thao tác và không làm gián đoạn kinh doanh.
* **Chiến lược:**
  * Cung cấp giao diện `seller.html` trực quan, cho phép thêm món ăn kèm ảnh nhanh chóng.
  * Giữ hệ thống ổn định 24/7 để không làm thất lạc đơn hàng của quán.

### 3. Sinh viên VJU - Khách đặt món (Giữ cho hiểu rõ - Keep Informed)
* **Mục tiêu:** Mang lại trải nghiệm đặt món tiện lợi, minh bạch về giá và thanh toán.
* **Chiến lược:**
  * Tích hợp thanh toán mã VietQR tự động giúp khách không cần gõ STK thủ công.
  * Hiển thị đầy đủ thực đơn, giá tiền và trạng thái món ăn rõ ràng trên trang chủ `index.html`.

### 4. Quản trị viên VPS / Mạng VJU (Theo dõi - Monitor)
* **Mục tiêu:** Tránh làm quá tải RAM/CPU hoặc nghẽn mạng server trường.
* **Chiến lược:**
  * Tối ưu mã nguồn FastAPI, hạn chế việc ghi đè CSDL liên tục.
  * Giám sát dung lượng RAM/Disk trên VPS để dịch vụ MySQL hoạt động ổn định.