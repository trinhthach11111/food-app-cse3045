# 📘 Quy ước Làm việc & Quản lý Dự án Cá nhân (TEAM.md)

**Thực hiện:** Trịnh Đình Thạch (MSV: 23110218)  
**Dự án:** Ứng dụng đặt đồ ăn trực tuyến `food-app-cse3045`

---

## 1. Ma trận RACI & Cơ chế Điều phối Cá nhân

*Ghi chú:* Vì dự án thực hiện cá nhân (Solo Project), sinh viên **Trịnh Đình Thạch** trực tiếp đảm nhiệm cả vai trò **Phê duyệt (Accountable - A)** và **Chịu trách nhiệm thực hiện (Responsible - R)** cho toàn bộ các mảng công việc.

| STT | Mảng công việc | Người Phê duyệt (A) | Người Thực hiện (R) | Ghi chú |
| :--- | :--- | :---: | :---: | :--- |
| 1 | **Thiết kế CSDL & Xác thực (Auth & User System)** | Trịnh Đình Thạch | Trịnh Đình Thạch | Thiết kế MySQL, Bcrypt password, 3 vai trò & Avatar |
| 2 | **Giao diện Khách hàng & Giỏ hàng (Customer UI/UX)** | Trịnh Đình Thạch | Trịnh Đình Thạch | Trang chủ `index.html`, lọc món, giỏ hàng |
| 3 | **Kênh Quản lý Chủ quán & Thêm món (Seller Dashboard)** | Trịnh Đình Thạch | Trịnh Đình Thạch | Trang `seller.html`, thêm món mới & upload ảnh món |
| 4 | **Triển khai VPS & Máy chủ (DevOps & Deployment)** | Trịnh Đình Thạch | Trịnh Đình Thạch | Cấu hình FastAPI systemd `foodapp`, Nginx & MySQL trên VPS |
| 5 | **Kiểm thử & Tích hợp Thanh toán (QA & VietQR Payment)** | Trịnh Đình Thạch | Trịnh Đình Thạch | Tích hợp VietQR API, kiểm thử luồng đăng ký/đăng nhập/đặt hàng |

### Cơ chế Tập trung Vai trò theo Sprint (Sprint Focus Rotation):
Dù làm cá nhân, tiến độ vẫn được phân chia trọng tâm theo từng giai đoạn Sprint:
* **Sprint 0:** Tập trung vai trò **System Architect & DevOps** (Dựng CSDL, Backend API, Deploy VPS).
* **Sprint 1:** Tập trung vai trò **Fullstack Developer** (Hoàn thiện UI/UX và logic nghiệp vụ Shipper/Seller).
* **Sprint 2:** Tập trung vai trò **QA Engineer & Refactoring** (Kiểm thử tải, tối ưu mã nguồn và bảo mật).

---

## 2. Quy ước Giao tiếp & Quản lý Công việc Cá nhân

### a) Kênh Giao tiếp & Báo cáo
* **Đồng bộ (Synchronous):** Trao đổi, tham vấn trực tiếp với Giảng viên / Trợ giảng vào các buổi học/Lab trên lớp để xin phản hồi về kiến trúc hệ thống.
* **Bất đồng bộ (Asynchronous):** Tự quản lý tiến độ công việc thông qua **GitHub Commits**, **GitHub Issues** và ghi chép nhật ký phát triển (Commit Logs).

### b) Quy cách Ghi nhận Quyết định Kỹ thuật
* Mọi tính năng mới hoặc nâng cấp đều được tạo dưới dạng **GitHub Issue** trên Repository trước khi triển khai.
* Các thay đổi mã nguồn lớn được thực hiện thông qua **Pull Request (PR)** hoặc các Commit có thông điệp rõ ràng (`commit message` chuẩn).
* Mọi thay đổi về Schema CSDL hay cấu hình Server VPS đều được lưu lại thành file `.sql` và ghi chú trong kho lưu trữ GitHub.

### c) Quy tắc Báo tin xấu (Bad News Rule for Solo Developer)
* **Nguyên tắc:** Khi gặp sự cố kỹ thuật nghiêm trọng (Blocker) như Server crash, lỗi CSDL hay lỗi mã hóa mật khẩu, không im lặng hoặc bỏ qua lỗi.
* **Thời hạn xử lý:** Nếu tự khắc phục một lỗi kỹ thuật quá **4 tiếng** không thành công, chủ động đăng issue lên GitHub repo, tham khảo ý kiến Giảng viên hoặc thảo luận với bạn học để tìm giải pháp, tránh ảnh hưởng đến tiến độ chung của môn học.