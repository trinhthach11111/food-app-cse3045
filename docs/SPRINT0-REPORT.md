# 🚀 Báo Cáo Hoàn Thiện Sprint 0 (SPRINT0-REPORT.md)

**Dự án:** Ứng dụng đặt đồ ăn trực tuyến dành cho sinh viên VJU (`food-app-cse3045`)  
**Sinh viên thực hiện:** Trịnh Đình Thạch (MSV: 23110218)  
**Địa chỉ VPS Thử nghiệm:** `http://sv25.bcse-vju.com`  
**GitHub Repository:** `https://github.com/trinhthach11111/food-app-cse3045`

---

## 1. Trạng thái Hạng mục Backlog Sprint 0

| STT | Hạng mục công việc (Sprint 0 Backlog) | Trạng thái | Minh chứng & Link sản phẩm |
| :--- | :--- | :---: | :--- |
| 1 | Thiết kế & Khởi tạo CSDL MySQL (`users`, `products`, `orders`) | **Xong** | File `database/init_db.sql` & Bảng MySQL trên VPS |
| 2 | Đăng ký / Đăng nhập 3 vai trò (Customer, Seller, Shipper) + Upload Avatar | **Xong** | API `/api/register`, `/api/login` trong `backend/main.py` |
| 3 | Giao diện Đăng nhập nhanh 1-Click cho 3 tài khoản Test | **Xong** | File `frontend/login.html` |
| 4 | Kênh Quản lý Chủ quán: Danh sách thực đơn, Thêm món & Tải ảnh món | **Xong** | API `/api/products` & giao diện `frontend/seller.html` |
| 5 | Trang chủ Khách hàng: Xem thực đơn, Giỏ hàng & Tạo mã VietQR tự động | **Xong** | API `/api/orders` & giao diện `frontend/index.html` |
| 6 | Triển khai web app chạy 24/7 trên máy chủ VPS Ubuntu | **Xong** | Dịch vụ `systemd` (`foodapp`) tại `http://sv25.bcse-vju.com` |

---

## 2. Phạm vi Sprint 1 (Sprint 1 Scope - 1 đến 2 tuần tới)

Trong Sprint 1, dự án sẽ tiếp tục phát triển và hoàn thiện các tính năng sau:

1. **Kênh Người giao hàng (Shipper Dashboard - `frontend/shipper.html`):** 
   * Hiển thị danh sách các đơn hàng đang chờ giao (`Pending`).
   * Tích hợp nút nhận đơn và cập nhật trạng thái đơn hàng sang `Delivering` (Đang giao) và `Completed` (Đã giao).
2. **Quản lý Đơn hàng cho Chủ quán (Seller Order Management):**
   * Cho phép Chủ quán xem các đơn hàng khách vừa đặt theo thời gian thực.
   * Xử lý xác nhận đơn hoặc hủy đơn hàng.
3. **Trang Lịch sử đơn hàng Khách hàng (Customer Order History):**
   * Cho phép Khách hàng xem lại các đơn hàng cá nhân đã đặt và hiển thị lại mã VietQR để thanh toán nếu cần.
   