# 👥 Đăng Ký Bên Liên Quan (STAKEHOLDERS.md)
**Dự án:** Ứng dụng đặt đồ ăn trực tuyến `food-app-cse3045`  
**Sinh viên thực hiện:** Trịnh Đình Thạch (MSV: 23110218)

## 1. Bảng Đăng Ký Bên Liên Quan
| STT | Bên liên quan | Quyền lực (Power) | Quan tâm (Interest) | Nhóm Ma Trận |
| :--- | :--- | :---: | :---: | :--- |
| 1 | Giảng viên & Trợ giảng CSE3045 | **Cao (High)** | **Cao (High)** | **Quản lý sát sao** |
| 2 | Chủ quán ăn (Seller) | **Cao (High)** | **Thấp (Low)** | **Giữ hài lòng** |
| 3 | Sinh viên VJU (Customer) | **Thấp (Low)** | **Cao (High)** | **Giữ cho hiểu rõ** |
| 4 | Quản trị VPS VJU | **Thấp (Low)** | **Thấp (Low)** | **Theo dõi** |

## 2. Chiến Lược Giao Tiếp
* **Giảng viên CSE3045:** Nộp báo cáo `docs/`, đánh tag SemVer `v0.1.0`, demo app thực tế trên VPS.
* **Chủ quán ăn:** Giao diện `seller.html` đơn giản, đăng món ăn kèm ảnh nhanh chóng.
* **Sinh viên VJU:** Tích hợp thanh toán mã VietQR tự động, xem menu thời gian thực.
* **Quản trị VPS VJU:** Tối ưu hiệu năng FastAPI, tránh làm quá tải RAM/Disk trên server.