# ⚙️ Kế Hoạch Quản Lý Cấu Hình (CONFIG.md)
**Dự án:** Ứng dụng đặt đồ ăn trực tuyến `food-app-cse3045`  
**Sinh viên thực hiện:** Trịnh Đình Thạch (MSV: 23110218)

## 1. Trả lời 7 câu hỏi Quản lý Cấu hình (CM)
1. **Quản lý những gì (CIs):** Mã nguồn FastAPI/HTML/JS, schema CSDL (`init_db.sql`, `seed.py`), tài liệu `docs/`, ảnh giao diện/uploads, dịch vụ systemd.
2. **Vai trò & Trách nhiệm:** Trịnh Đình Thạch (Configuration Manager) chịu trách nhiệm kiểm soát phiên bản, sao lưu CSDL và gắn tag phát hành.
3. **Công cụ quản lý:** Git & GitHub (`food-app-cse3045`), Systemd trên VPS Ubuntu (`sv25.bcse-vju.com`), MySQL Server.
4. **Điểm mốc cấu hình (Baselines):** Baseline 0 (`v0.1.0`) - Hoàn thành Sprint 0 & 1 với Auth, Seller, VietQR và VPS Deployment.
5. **Quy ước đặt tên:** Tệp tải lên dạng `prod_{tên_món}_{tên_file}` và `{username}_{tên_file}`. Tài liệu viết hoa trong `docs/`.
6. **Quy ước thay đổi:** Test local trước khi push `main`. Thay đổi CSDL bắt buộc cập nhật vào `seed.py`.
7. **Sao lưu & Phục hồi:** Sao lưu CSDL qua `mysqldump`/`seed.py`, lưu trữ ảnh trực tiếp trên VPS tại `frontend/images/` và `frontend/uploads/`.

## 2. Quy ước Đánh số Phiên bản (SemVer)
* **MAJOR (X.0.0):** Thay đổi lớn phá vỡ tương thích.
* **MINOR (0.X.0):** Thêm tính năng mới (Kênh Shipper, tìm kiếm món).
* **PATCH (0.0.X):** Sửa lỗi nhỏ (Fix lỗi 502, fix hiển thị ảnh).
* **Tag Format:** Ký tự `v` phía trước (Ví dụ: `v0.1.0`).