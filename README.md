# Nền tảng đặt và giao đồ ăn trực tuyến (Food App)

**Sinh viên thực hiện:** Trịnh Đình Thạch — MSV: 23110218 (Vai trò: Full-stack)

## Bản mô tả dự án sơ bộ (Project Charter Mini)

### 1. Mục tiêu
Xây dựng một trang web giúp sinh viên Đại học Việt Nhật (VJU) dễ dàng đặt đồ ăn nhanh chóng, tiện lợi, hỗ trợ giao tận nơi trong khuôn viên cơ sở Hòa Lạc nhằm tiết kiệm thời gian nghỉ trưa.

### 2. Phạm vi dự án
*   **Sẽ làm:** 
    *   Giao diện xem thực đơn, giỏ hàng, đặt món.
    *   **Tích hợp thanh toán trực tuyến qua thẻ ngân hàng/ví điện tử.**
    *   **Tính năng theo dõi lộ trình shipper thời gian thực (hiển thị bản đồ và vị trí giao hàng).**
*   **Không làm:** Không tích hợp hệ thống hóa đơn điện tử phức tạp của cơ quan thuế hoặc liên kết trực tiếp với ngân hàng nhà nước (sử dụng cổng thanh toán sandbox/mô phỏng).

### 3. Các bên liên quan
*   **Khách hàng:** Sinh viên, giảng viên và nhân viên VJU tại Hòa Lạc.
*   **Người cung cấp:** Căn tin trường hoặc các quán ăn lân cận.
*   **Nhóm phát triển:** Trịnh Đình Thạch (đảm nhiệm toàn bộ frontend, backend và testing).

### 4. Ba (3) ràng buộc
1.  **Ràng buộc thời gian:** Phải hoàn thành các mốc tính năng và báo cáo đúng thời hạn của môn học CSE3045.
2.  **Ràng buộc nguồn lực:** Dự án được thực hiện độc lập bởi 1 người nên quy mô tính năng phải được thu gọn, tập trung vào luồng đặt hàng cốt lõi.
3.  **Ràng buộc kỹ thuật:** Hệ thống bắt buộc phải được deploy và chạy ổn định trên máy chủ VPS do trường cấp (`sv25.bcse-vju.com`).

## 2. Phân công vai trò nhóm (Scrum)
*Dự án này được thực hiện độc lập (1 sinh viên). Do đó, tôi sẽ đảm nhiệm toàn bộ các vai trò trong quy trình Scrum nhằm đảm bảo tiến độ và chất lượng dự án:*
* **Scrum Master (Điều phối & Quản lý tiến độ):** Trịnh Đình Thạch (MSV: 23110218)
* **Product Owner (Quản lý yêu cầu, Báo cáo & Tài liệu):** Trịnh Đình Thạch (MSV: 23110218)
* **Development Team (Full-stack Backend & Frontend):** Trịnh Đình Thạch (MSV: 23110218)

## 3. Backlog Sprint 0 (Chuẩn bị MVP)
- [x] Thiết lập kho lưu trữ GitHub và cấu hình kiểm thử tự động CI (HW1, HW3).
- [x] Thiết lập môi trường triển khai mã nguồn trên VPS tại `sv25.bcse-vju.com` (HW1, HW2).
- [ ] Lên ý tưởng giao diện (Mockup/UI) cho trang đặt đồ ăn.
- [ ] Thiết kế cơ sở dữ liệu (SQLite) lưu trữ thông tin món ăn và đơn hàng.
- [ ] Xây dựng các API cơ bản bằng FastAPI (Backend).

## 4. Demo ý tưởng MVP (Sprint 0)
* **Mô tả hệ thống hiện tại:** Hệ thống đang có giao diện tĩnh ban đầu và module backend chạy Cấu trúc dữ liệu hàng đợi (Queue) để quản lý luồng đơn hàng.
* **Link web demo (nếu có):** http://sv25.bcse-vju.com
* **Mô hình/Ảnh bản vẽ:** *(Bạn có thể up 1 bức ảnh chụp bản vẽ giấy hoặc giao diện thiết kế lên GitHub, sau đó dán link ảnh vào đây)*.
