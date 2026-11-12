# 🌿 Quy Ước Nhánh & Đánh Tag Git (GIT.md)

**Dự án:** Ứng dụng đặt đồ ăn trực tuyến `food-app-cse3045`  
**Sinh viên thực hiện:** Trịnh Đình Thạch (MSV: 23110218)

---

## 1. Quy Ước Luồng Nhánh (Branching Strategy)

Dự án áp dụng mô hình luồng nhánh rút gọn phù hợp với dự án cá nhân:

* **`main` (Nhánh chính):** Chứa mã nguồn ổn định nhất đã được kiểm thử và đang chạy thực tế trên máy chủ VPS (`sv25.bcse-vju.com`).
* **`feature/*` (Nhánh tính năng):** Dùng để phát triển các tính năng mới độc lập (Ví dụ: `feature/shipper-dashboard`, `feature/vietqr-payment`).
* **`fix/*` hoặc `bugfix/*` (Nhánh sửa lỗi):** Dùng để sửa các sự cố phát sinh (Ví dụ: `fix/bad-gateway-502`, `fix/db-connection`).

---

## 2. Quy Cách Commit Message & Pull Request (PR)

Các thông điệp Commit được viết theo chuẩn **Conventional Commits**:

* `feat:` Thêm tính năng mới (Ví dụ: `feat: add order creation API and VietQR popup`).
* `fix:` Sửa lỗi mã nguồn (Ví dụ: `fix: add missing CreateOrderSchema model`).
* `docs:` Cập nhật tài liệu (Ví dụ: `docs: add CONFIG.md and STAKEHOLDERS.md`).
* `refactor:` Tối ưu hóa mã nguồn nhưng không đổi tính năng.

---

## 3. Quy Trình Tạo Tag Phát Hành (Release Tagging)

Mỗi khi hoàn thành một mốc Sprint, sinh viên thực hiện đánh tag phát hành theo chuẩn **SemVer** và đẩy lên GitHub bằng các lệnh sau:

```bash
# 1. Kiểm tra trạng thái Git
git status

# 2. Tạo Tag kèm thông điệp phát hành
git tag -a v0.1.0 -m "Release Sprint 1: Completed Auth, Seller Dashboard, Customer VietQR Checkout"

# 3. Đẩy Tag lên GitHub Repo
git push origin v0.1.0
# 🌿 Quy Ước Nhánh & Đánh Tag Git (GIT.md)

**Dự án:** Ứng dụng đặt đồ ăn trực tuyến `food-app-cse3045`  
**Sinh viên thực hiện:** Trịnh Đình Thạch (MSV: 23110218)

---

## 1. Quy Ước Luồng Nhánh (Branching Strategy)

Dự án áp dụng mô hình luồng nhánh rút gọn phù hợp với dự án cá nhân:

* **`main` (Nhánh chính):** Chứa mã nguồn ổn định nhất đã được kiểm thử và đang chạy thực tế trên máy chủ VPS (`sv25.bcse-vju.com`).
* **`feature/*` (Nhánh tính năng):** Dùng để phát triển các tính năng mới độc lập (Ví dụ: `feature/shipper-dashboard`, `feature/vietqr-payment`).
* **`fix/*` hoặc `bugfix/*` (Nhánh sửa lỗi):** Dùng để sửa các sự cố phát sinh (Ví dụ: `fix/bad-gateway-502`, `fix/db-connection`).

---

## 2. Quy Cách Commit Message & Pull Request (PR)

Các thông điệp Commit được viết theo chuẩn **Conventional Commits**:

* `feat:` Thêm tính năng mới (Ví dụ: `feat: add order creation API and VietQR popup`).
* `fix:` Sửa lỗi mã nguồn (Ví dụ: `fix: add missing CreateOrderSchema model`).
* `docs:` Cập nhật tài liệu (Ví dụ: `docs: add CONFIG.md and STAKEHOLDERS.md`).
* `refactor:` Tối ưu hóa mã nguồn nhưng không đổi tính năng.

---

## 3. Quy Trình Tạo Tag Phát Hành (Release Tagging)

Mỗi khi hoàn thành một mốc Sprint, sinh viên thực hiện đánh tag phát hành theo chuẩn **SemVer** và đẩy lên GitHub bằng các lệnh sau:

```bash
# 1. Kiểm tra trạng thái Git
git status

# 2. Tạo Tag kèm thông điệp phát hành
git tag -a v0.1.0 -m "Release Sprint 1: Completed Auth, Seller Dashboard, Customer VietQR Checkout"

# 3. Đẩy Tag lên GitHub Repo
git push origin v0.1.0