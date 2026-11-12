# ⚙️ Kế Hoạch Quản Lý Cấu Hình (CONFIG.md)

**Dự án:** Ứng dụng đặt đồ ăn trực tuyến `food-app-cse3045`  
**Sinh viên thực hiện:** Trịnh Đình Thạch (MSV: 23110218)

---

## 1. Trả lời 7 câu hỏi Quản lý Cấu hình (Configuration Management)

1. **Quản lý những gì (Configuration Items - CIs):**
   * **Mã nguồn (Source Code):** Backend FastAPI (`backend/`), Frontend HTML/CSS/JS (`frontend/`).
   * **Cấu hình CSDL:** Các tệp khởi tạo schema (`database/init_db.sql`, `seed.py`).
   * **Tài liệu dự án:** Thư mục `docs/` (`TEAM.md`, `SPRINT0-REPORT.md`, `CONFIG.md`, v.v.).
   * **Tệp tĩnh (Static Assets):** Ảnh giao diện, ảnh thực đơn (`frontend/images/`), ảnh đại diện (`frontend/uploads/`).
   * **Cấu hình môi trường:** Dịch vụ systemd (`foodapp.service`), biến môi trường kết nối MySQL.

2. **Vai trò & Trách nhiệm:**
   * **Trịnh Đình Thạch (Solo Developer):** Đảm nhận vai trò **Configuration Manager (CM)** chịu trách nhiệm kiểm soát phiên bản, sao lưu CSDL, phê duyệt mã nguồn và gắn tag phát hành.

3. **Công cụ quản lý:**
   * **Quản lý mã nguồn:** Git & GitHub (`food-app-cse3045`).
   * **Quản lý dịch vụ máy chủ:** Systemd trên VPS Ubuntu (`sv25.bcse-vju.com`).
   * **Quản lý CSDL:** MySQL Database Server & Python scripts.

4. **Điểm mốc cấu hình (Baselines):**
   * **Baseline 0 (v0.1.0):** Hoàn thành Sprint 0 — Xác thực 3 vai trò, thực đơn, đặt hàng VietQR, deploy VPS thành công.
   * **Baseline 1 (v0.2.0):** Hoàn thành Sprint 1 — Kênh Shipper nhận đơn và Quản lý đơn hàng Chủ quán.
   * **Baseline Final (v1.0.0):** Sản phẩm nghiệm thu cuối kỳ.

5. **Quy ước đặt tên (Naming Conventions):**
   * **Tệp ảnh tải lên:** `prod_{tên_món}_{tên_file}` cho món ăn và `{username}_{tên_file}` cho avatar.
   * **Tệp tài liệu:** Viết hoa toàn bộ tên file trong thư mục `docs/` (`CONFIG.md`, `GIT.md`).

6. **Quy ước quản lý thay đổi (Change Control):**
   * Mọi thay đổi code phải được chạy kiểm thử tính năng cục bộ trước khi push lên nhánh `main`.
   * Các thay đổi làm ảnh hưởng tới CSDL (thêm cột, sửa bảng) bắt buộc phải cập nhật đồng bộ vào `seed.py` và lưu lại câu lệnh SQL.

7. **Kế hoạch Sao lưu & Phục hồi (Backup & Recovery):**
   * **CSDL:** Sao lưu dữ liệu MySQL định kỳ thông qua lệnh `mysqldump` hoặc tệp khởi tạo `seed.py`.
   * **Tệp tải lên:** Lưu trữ trực tiếp trên ổ đĩa VPS tại `frontend/images/` và `frontend/uploads/`.
   * **Phục hồi:** Khi VPS gặp sự cố, chạy tệp script `seed.py` hoặc khôi phục từ commit gần nhất trên GitHub.

---

## 2. Quy ước Đánh số Phiên bản (Semantic Versioning - SemVer)

Dự án tuân thủ quy chuẩn **SemVer (`MAJOR.MINOR.PATCH`)**:

* **MAJOR (Số chính - X.0.0):** Thay đổi lớn, phá vỡ tính tương thích cũ (ví dụ: Tái cấu trúc lại toàn bộ API hoặc đổi CSDL từ MySQL sang PostgreSQL).
* **MINOR (Số phụ - 0.X.0):** Thêm tính năng mới nhưng vẫn tương thích ngược (ví dụ: Bổ sung Kênh Shipper, thêm tính năng lọc món ăn).
* **PATCH (Số bản vá - 0.0.X):** Sửa lỗi nhỏ, tối ưu hiệu năng hoặc sửa lỗi giao diện (ví dụ: Fix lỗi 502 Bad Gateway, fix hiển thị ảnh).

**Quy ước Tag:** Mọi phiên bản phát hành được đánh tag ký tự `v` phía trước (Ví dụ: `v0.1.0`, `v0.2.0`).